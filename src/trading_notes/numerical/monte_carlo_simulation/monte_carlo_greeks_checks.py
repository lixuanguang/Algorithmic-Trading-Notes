"""The worked example of meth:monte-carlo-greeks: pathwise and likelihood-ratio estimators."""

import sys
from typing import Final

import numpy as np
import scipy
from numpy.typing import NDArray
from scipy import stats

from trading_notes.numerical.monte_carlo_simulation.greek_estimators import (
    ClosedForms,
    Draws,
    GbmModel,
    mean_se,
)
from trading_notes.numerical.report import CheckReport

type Floats = NDArray[np.float64]

MODEL: Final = GbmModel(spot=100.0, rate=0.03, volatility=0.20, maturity=1.0)
S0: Final = MODEL.spot
K: Final = 105.0
SIG: Final = MODEL.volatility
T: Final = MODEL.maturity
M: Final = 100_000  # draws shared by every estimator
SEED: Final = 20261021
ZMAX: Final = 4.0  # standard errors allowed
DISC: Final = MODEL.discount
SQT: Final = MODEL.sqrt_t


def rel(a: float, b: float) -> float:
    """Return |a - b| / |b|."""
    return abs(a - b) / abs(b)


def check_deterministic(report: CheckReport, cf: ClosedForms) -> None:
    """1. Path derivatives and scores against finite differences, and the gamma boundary term."""
    print("== 1. deterministic: path derivatives, scores and the gamma boundary term")
    zs = np.array([-2.0, -0.5, 0.0, 0.7, 2.3])
    h = 1e-5
    dS_dS0_fd = (MODEL.terminal(S0 + h, SIG, zs) - MODEL.terminal(S0 - h, SIG, zs)) / (2 * h)
    dS_dsig_fd = (
        MODEL.terminal(S0, SIG + h * 1e-2, zs) - MODEL.terminal(S0, SIG - h * 1e-2, zs)
    ) / (2 * h * 1e-2)
    ST_z = MODEL.terminal(S0, SIG, zs)
    err1 = max(rel(a, b) for a, b in zip(dS_dS0_fd, ST_z / S0, strict=True))
    err2 = max(rel(a, b) for a, b in zip(dS_dsig_fd, ST_z * (-SIG * T + SQT * zs), strict=True))
    report.ok("dS_T/dS0 = S_T/S0 (eq. (9))", err1 <= 1e-6, f"max rel err {err1:.1e}")
    report.ok(
        "dS_T/dsigma = S_T(-sigma T + sqrt(T) Z) (eq. (5))", err2 <= 1e-6, f"max rel err {err2:.1e}"
    )
    worst_s, worst_v = 0.0, 0.0
    for x in (80.0, 105.0, 130.0):
        z = MODEL.normal_of(x, S0, SIG)
        fd_s = (MODEL.log_density(x, S0 + 1e-4, SIG) - MODEL.log_density(x, S0 - 1e-4, SIG)) / 2e-4
        fd_v = (MODEL.log_density(x, S0, SIG + 1e-6) - MODEL.log_density(x, S0, SIG - 1e-6)) / 2e-6
        worst_s = max(worst_s, rel(fd_s, z / (S0 * SIG * SQT)))
        worst_v = max(worst_v, rel(fd_v, (z * z - 1) / SIG - SQT * z))
    report.ok(
        "S0 score = Z/(S0 sigma sqrt T) (eq. (16) in Z)",
        worst_s <= 1e-6,
        f"max rel err {worst_s:.1e}",
    )
    report.ok(
        "sigma score = (Z^2 - 1)/sigma - sqrt(T) Z (eq. (15) in Z)",
        worst_v <= 1e-6,
        f"max rel err {worst_v:.1e}",
    )
    # the per-path pathwise delta depends on S0 only through the indicator: S_T/S0 is unchanged by
    # a bump
    ratio_err = float(
        np.max(np.abs(MODEL.terminal(S0 + 1.0, SIG, zs) / (S0 + 1.0) - ST_z / S0) / (ST_z / S0))
    )
    report.ok(
        "S_T/S0 does not depend on S0 (naive pathwise gamma is 0 a.s.)",
        ratio_err <= 1e-12,
        f"{ratio_err:.1e}",
    )
    g_K = np.exp(MODEL.log_density(K, S0, SIG))
    gamma_eq18 = DISC * (K / S0) ** 2 * g_K
    report.ok(
        "eq. (18) boundary term e^{-rT}(K/S0)^2 g(K) = BSM gamma",
        rel(gamma_eq18, cf.call_gamma) <= 1e-12,
        f"{gamma_eq18:.10f} vs {cf.call_gamma:.10f}",
    )


def check_estimators(
    report: CheckReport, cf: ClosedForms, d: Draws
) -> tuple[dict[str, tuple[float, float]], tuple[float, float]]:
    """2. Each estimator against its closed form; return the call estimates and the digital LR's."""
    print(f"== 2. estimators on {M:,} draws, seed {SEED}")
    Z, ST, itm, pay = d.z, d.st, d.itm, d.pay
    est = {
        "call pathwise delta": (DISC * itm * ST / S0, cf.call_delta),
        "call LR delta": (pay * d.score_s0, cf.call_delta),
        "call pathwise vega": (DISC * itm * ST * (-SIG * T + SQT * Z), cf.call_vega),
        "call LR vega": (pay * d.score_sig, cf.call_vega),
        "call pathwise dC/dK": (-DISC * itm.astype(float), cf.call_dK),
    }
    res = {}
    for name, (x, exact) in est.items():
        m, se = mean_se(x)
        res[name] = (m, se)
        zsc = (m - exact) / se
        report.ok(
            f"{name} within {ZMAX:g} s.e.",
            abs(zsc) <= ZMAX,
            f"{m:.5f} (s.e. {se:.5f}) vs {exact:.5f}, z {zsc:+.2f}",
        )
    print(
        f"  call by simulation {mean_se(pay)[0]:.4f} (s.e. {mean_se(pay)[1]:.4f}) vs {cf.call:.4f}"
    )

    dig = DISC * itm.astype(float)
    # pathwise: the per-path derivative of e^{-rT} 1{S_T > K}, taken on the fixed draws by a
    # central difference far smaller than any path's distance from the strike, is zero on every
    # path
    eps = 1e-9
    gap = float(np.min(np.abs(ST - K)))
    dig_pw_delta = (
        DISC
        * (
            (MODEL.terminal(S0 + eps, SIG, Z) > K).astype(float)
            - (MODEL.terminal(S0 - eps, SIG, Z) > K)
        )
        / (2 * eps)
    )
    dig_pw_dK = DISC * ((ST > K + eps).astype(float) - (ST > K - eps)) / (2 * eps)
    report.ok(
        "digital pathwise delta is 0 on every path",
        gap > 1e3 * eps and not np.any(dig_pw_delta),
        f"mean 0 vs exact {cf.dig_delta:.6f} (closest path {gap:.1e} from K)",
    )
    report.ok(
        "digital pathwise dD/dK is 0 on every path",
        not np.any(dig_pw_dK),
        f"mean 0 vs exact {cf.dig_dK:.6f}",
    )
    m, se = mean_se(dig * d.score_s0)
    zsc = (m - cf.dig_delta) / se
    report.ok(
        f"digital LR delta within {ZMAX:g} s.e.",
        abs(zsc) <= ZMAX,
        f"{m:.6f} (s.e. {se:.6f}) vs {cf.dig_delta:.6f}, z {zsc:+.2f}",
    )
    return res, (m, se)


def report_comparisons(
    cf: ClosedForms, d: Draws, res: dict[str, tuple[float, float]], dig_lr: tuple[float, float]
) -> None:
    """3. Standard-error ratios and the digital's resimulation delta, reported only."""
    print("== 3. reported, not binding")
    for g in ("delta", "vega"):
        ratio = res[f"call LR {g}"][1] / res[f"call pathwise {g}"][1]
        print(f"  call {g}: LR / pathwise standard error = {ratio:.2f}")
    for hh in (1.0, 0.01):
        fd = DISC * ((MODEL.terminal(S0 + hh, SIG, d.z) > K).astype(float) - d.itm) / hh
        m, se = mean_se(fd)
        print(
            f"  digital resimulation delta, h = {hh:g}: {m:.6f} (s.e. {se:.6f}), minus exact"
            f" {m - cf.dig_delta:+.6f}"
        )
    print(f"  digital LR delta for comparison: {dig_lr[0]:.6f} (s.e. {dig_lr[1]:.6f})")


def check_fd_variance(report: CheckReport, d: Draws) -> None:
    """4. Shared-path finite-difference variance: finite for the call, about 1/h for the digital.

    Call: the difference tends path by path to the
    pathwise delta, so its variance stays finite as h -> 0. Digital: a path contributes
    e^{-rT}/h only if S_T crosses K, with probability about g(K) K h / S0, so the variance is
    about e^{-2rT} g(K) K / (S0 h). The digital is computed exactly from the lognormal CDF.
    """
    print("== 4. shared-path finite-difference variance: call finite, digital about 1/h")
    Z, ST, itm = d.z, d.st, d.itm
    var_pw = float(np.var(DISC * itm * ST / S0, ddof=1))
    call_var = {}
    for hh in (1.0, 0.1, 0.01, 0.001):
        fd = (
            DISC
            * (np.maximum(MODEL.terminal(S0 + hh, SIG, Z) - K, 0.0) - np.maximum(ST - K, 0.0))
            / hh
        )
        call_var[hh] = float(np.var(fd, ddof=1))
        print(
            f"  call, h = {hh:g}: sample variance {call_var[hh]:.6f} (pathwise delta {var_pw:.6f})"
        )
    report.ok(
        "call: shared-path difference variance tends to the pathwise variance (h = 0.001, rel 1%)",
        rel(call_var[0.001], var_pw) <= 0.01,
        f"{call_var[0.001]:.6f} vs {var_pw:.6f}",
    )
    limit = DISC**2 * np.exp(MODEL.log_density(K, S0, SIG)) * K / S0
    dig_hvar = {}
    for hh in (1.0, 0.1, 0.01, 0.001):
        p_cross = stats.norm.cdf(MODEL.normal_of(K, S0, SIG)) - stats.norm.cdf(
            MODEL.normal_of(K * S0 / (S0 + hh), S0, SIG)
        )
        var_exact = DISC**2 * p_cross * (1 - p_cross) / hh**2
        dig_hvar[hh] = hh * var_exact
        print(
            f"  digital, h = {hh:g}: exact variance {var_exact:.6f}, h x variance"
            f" {hh * var_exact:.6f}"
        )
    report.ok(
        "digital: h x variance tends to e^{-2rT} g(K) K / S0 (h = 0.001, rel 1%)",
        rel(dig_hvar[0.001], limit) <= 0.01,
        f"{dig_hvar[0.001]:.6f} vs {limit:.6f}",
    )
    report.ok(
        "digital variance grows about 1000-fold from h = 1 to 0.001; the call's stays within a"
        " factor 2",
        0.5 <= dig_hvar[0.001] / dig_hvar[1.0] <= 2 and 0.5 <= call_var[0.001] / call_var[1.0] <= 2,
        f"h x var ratio {dig_hvar[0.001] / dig_hvar[1.0]:.3f}; call var ratio"
        f" {call_var[0.001] / call_var[1.0]:.3f}",
    )
    fd = DISC * ((MODEL.terminal(S0 + 1.0, SIG, Z) > K).astype(float) - itm) / 1.0
    print(
        f"  digital, h = 1 sample variance on the shared paths: {np.var(fd, ddof=1):.6f} (exact"
        " above)"
    )


def main() -> int:
    """Print the versions and closed forms, then run the four parts with one report.

    Model: risk-neutral GBM, S0 = 100, r = 3 percent, q = 0, sigma = 20 percent, T = 1 (the inputs
    of meth:monte-carlo-simulation). A European call struck at 105 and a unit cash-or-nothing call
    struck at 105. Estimators after Broadie and Glasserman (1996): pathwise (eqs. (5)-(9)) and
    likelihood ratio (eqs. (14)-(16), scores rewritten in the standard normal Z), and resimulation
    with common random numbers for the digital (reported only).

    Settings: NumPy default_rng(20261021), one vector of 100,000 standard normals
    shared by every estimator; deterministic checks to relative 1e-6 (finite differences) or 1e-12
    (identities); each stochastic estimate within 4 standard errors of its closed form. Synthetic
    inputs only: not evidence about markets.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
    report = CheckReport()
    cf = MODEL.closed_forms(K)
    print(
        f"closed forms: call {cf.call:.4f}, delta {cf.call_delta:.5f}, vega {cf.call_vega:.4f},"
        f" gamma {cf.call_gamma:.6f}"
    )
    print(
        f"  dC/dK {cf.call_dK:.5f}; digital delta {cf.dig_delta:.6f}, digital dD/dK {cf.dig_dK:.6f}"
    )
    check_deterministic(report, cf)
    d = Draws.draw(MODEL, K, np.random.default_rng(SEED), M)
    res, dig_lr = check_estimators(report, cf, d)
    report_comparisons(cf, d, res, dig_lr)
    check_fd_variance(report, d)
    print("FAILED:" + ", ".join(report.failures) if report.failures else "all checks passed")
    return 1 if report.failures else 0


if __name__ == "__main__":
    sys.exit(main())
