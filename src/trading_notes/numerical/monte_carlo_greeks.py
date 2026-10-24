"""The worked example of meth:monte-carlo-greeks.

Library gap-filling Batch L4, package L4-a (2026-10-21).

Model: risk-neutral GBM, S0 = 100, r = 3 percent, q = 0, sigma = 20 percent, T = 1 (the inputs
of meth:monte-carlo-simulation). A European call struck at 105 and a unit cash-or-nothing call
struck at 105. Estimators after Broadie and Glasserman (1996): pathwise (eqs. (5)-(9)) and
likelihood ratio (eqs. (14)-(16), scores rewritten in the standard normal Z), and resimulation
with common random numbers for the digital (reported only).

Frozen before the first run: NumPy default_rng(20261021), one vector of 100,000 standard normals
shared by every estimator; deterministic checks to relative 1e-6 (finite differences) or 1e-12
(identities); each stochastic estimate within 4 standard errors of its closed form. Synthetic
inputs only: not evidence about markets.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.monte_carlo_greeks
(numpy, scipy). Exits 1 on failure. About one second.
"""

# standard library imports
import sys
from dataclasses import dataclass
from typing import Final

# third party library imports
import numpy as np
import scipy
from numpy.typing import NDArray
from scipy import stats

# project library imports
from trading_notes.numerical.report import CheckReport

type Floats = NDArray[np.float64]

S0: Final = 100.0
K: Final = 105.0
SIG: Final = 0.20
R: Final = 0.03
T: Final = 1.0
M: Final = 100_000  # draws shared by every estimator
SEED: Final = 20261021
ZMAX: Final = 4.0  # standard errors allowed
# NumPy's exp and sqrt, as first run, so the scalars match it to the last bit.
DISC: Final = np.exp(-R * T)
SQT: Final = np.sqrt(T)


def rel(a: float, b: float) -> float:
    """Return |a - b| / |b|."""
    return abs(a - b) / abs(b)


@dataclass(frozen=True)
class ClosedForms:
    """The BSM values and Greeks (q = 0) the estimators are checked against.

    Attributes:
        call: The call's value.
        call_delta: Its delta.
        call_vega: Its vega.
        call_gamma: Its gamma.
        call_dK: Its derivative with respect to the strike.
        dig_delta: The cash digital's delta.
        dig_dK: The cash digital's derivative with respect to the strike.
    """

    call: float
    call_delta: float
    call_vega: float
    call_gamma: float
    call_dK: float
    dig_delta: float
    dig_dK: float

    @classmethod
    def bsm(cls) -> ClosedForms:
        """Return the closed forms at the module's inputs."""
        d1 = (np.log(S0 / K) + (R + SIG**2 / 2) * T) / (SIG * SQT)
        d2 = d1 - SIG * SQT
        return cls(
            call=S0 * stats.norm.cdf(d1) - K * DISC * stats.norm.cdf(d2),
            call_delta=stats.norm.cdf(d1),
            call_vega=S0 * SQT * stats.norm.pdf(d1),
            call_gamma=stats.norm.pdf(d1) / (S0 * SIG * SQT),
            call_dK=-DISC * stats.norm.cdf(d2),
            dig_delta=DISC * stats.norm.pdf(d2) / (S0 * SIG * SQT),
            dig_dK=-DISC * stats.norm.pdf(d2) / (K * SIG * SQT),
        )


def path(s0: float, vol: float, z: Floats) -> Floats:
    """Terminal price as a function of the parameters on fixed normals z (B-G eq. (4))."""
    st: Floats = s0 * np.exp((R - vol**2 / 2) * T + vol * SQT * z)
    return st


def log_density(x: float, s0: float, vol: float) -> float:
    """Log of the lognormal density of S_T (eqs. (10)-(11))."""
    d = (np.log(x / s0) - (R - vol**2 / 2) * T) / (vol * SQT)
    return float(stats.norm.logpdf(d) - np.log(x * vol * SQT))


def z_of(x: float, s0: float, vol: float) -> float:
    """Return the standard normal that puts S_T at x."""
    z: float = (np.log(x / s0) - (R - vol**2 / 2) * T) / (vol * SQT)
    return z


def check_deterministic(report: CheckReport, cf: ClosedForms) -> None:
    """1. Path derivatives and scores against finite differences, and the gamma boundary term."""
    print("== 1. deterministic: path derivatives, scores and the gamma boundary term")
    zs = np.array([-2.0, -0.5, 0.0, 0.7, 2.3])
    h = 1e-5
    dS_dS0_fd = (path(S0 + h, SIG, zs) - path(S0 - h, SIG, zs)) / (2 * h)
    dS_dsig_fd = (path(S0, SIG + h * 1e-2, zs) - path(S0, SIG - h * 1e-2, zs)) / (2 * h * 1e-2)
    ST_z = path(S0, SIG, zs)
    err1 = max(rel(a, b) for a, b in zip(dS_dS0_fd, ST_z / S0, strict=True))
    err2 = max(rel(a, b) for a, b in zip(dS_dsig_fd, ST_z * (-SIG * T + SQT * zs), strict=True))
    report.ok("dS_T/dS0 = S_T/S0 (eq. (9))", err1 <= 1e-6, f"max rel err {err1:.1e}")
    report.ok(
        "dS_T/dsigma = S_T(-sigma T + sqrt(T) Z) (eq. (5))", err2 <= 1e-6, f"max rel err {err2:.1e}"
    )
    worst_s, worst_v = 0.0, 0.0
    for x in (80.0, 105.0, 130.0):
        z = z_of(x, S0, SIG)
        fd_s = (log_density(x, S0 + 1e-4, SIG) - log_density(x, S0 - 1e-4, SIG)) / 2e-4
        fd_v = (log_density(x, S0, SIG + 1e-6) - log_density(x, S0, SIG - 1e-6)) / 2e-6
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
        np.max(np.abs(path(S0 + 1.0, SIG, zs) / (S0 + 1.0) - ST_z / S0) / (ST_z / S0))
    )
    report.ok(
        "S_T/S0 does not depend on S0 (naive pathwise gamma is 0 a.s.)",
        ratio_err <= 1e-12,
        f"{ratio_err:.1e}",
    )
    g_K = np.exp(log_density(K, S0, SIG))
    gamma_eq18 = DISC * (K / S0) ** 2 * g_K
    report.ok(
        "eq. (18) boundary term e^{-rT}(K/S0)^2 g(K) = BSM gamma",
        rel(gamma_eq18, cf.call_gamma) <= 1e-12,
        f"{gamma_eq18:.10f} vs {cf.call_gamma:.10f}",
    )


@dataclass(frozen=True)
class Draws:
    """The shared normals and what every estimator computes from them.

    Attributes:
        z: The standard normals.
        st: The terminal prices.
        itm: Whether each path ends above the strike.
        pay: The discounted call payoff.
        score_s0: The likelihood-ratio score for S0.
        score_sig: The likelihood-ratio score for sigma.
    """

    z: Floats
    st: Floats
    itm: NDArray[np.bool_]
    pay: Floats
    score_s0: Floats
    score_sig: Floats

    @classmethod
    def draw(cls, rng: np.random.Generator) -> Draws:
        """Draw the M normals and compute the shared quantities."""
        Z = rng.standard_normal(M)
        ST = path(S0, SIG, Z)
        return cls(
            z=Z,
            st=ST,
            itm=ST > K,
            pay=DISC * np.maximum(ST - K, 0.0),
            score_s0=Z / (S0 * SIG * SQT),
            score_sig=(Z * Z - 1) / SIG - SQT * Z,
        )


def mean_se(x: Floats) -> tuple[float, float]:
    """Return the sample mean and its standard error."""
    return float(x.mean()), float(x.std(ddof=1) / np.sqrt(x.size))


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
        * ((path(S0 + eps, SIG, Z) > K).astype(float) - (path(S0 - eps, SIG, Z) > K))
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
        fd = DISC * ((path(S0 + hh, SIG, d.z) > K).astype(float) - d.itm) / hh
        m, se = mean_se(fd)
        print(
            f"  digital resimulation delta, h = {hh:g}: {m:.6f} (s.e. {se:.6f}), minus exact"
            f" {m - cf.dig_delta:+.6f}"
        )
    print(f"  digital LR delta for comparison: {dig_lr[0]:.6f} (s.e. {dig_lr[1]:.6f})")


def check_fd_variance(report: CheckReport, d: Draws) -> None:
    """4. Shared-path finite-difference variance: finite for the call, about 1/h for the digital.

    Added 2026-10-21 (C1 pass, L4 correction). Call: the difference tends path by path to the
    pathwise delta, so its variance stays finite as h -> 0. Digital: a path contributes
    e^{-rT}/h only if S_T crosses K, with probability about g(K) K h / S0, so the variance is
    about e^{-2rT} g(K) K / (S0 h). The digital is computed exactly from the lognormal CDF.
    """
    print("== 4. shared-path finite-difference variance: call finite, digital about 1/h")
    Z, ST, itm = d.z, d.st, d.itm
    var_pw = float(np.var(DISC * itm * ST / S0, ddof=1))
    call_var = {}
    for hh in (1.0, 0.1, 0.01, 0.001):
        fd = DISC * (np.maximum(path(S0 + hh, SIG, Z) - K, 0.0) - np.maximum(ST - K, 0.0)) / hh
        call_var[hh] = float(np.var(fd, ddof=1))
        print(
            f"  call, h = {hh:g}: sample variance {call_var[hh]:.6f} (pathwise delta {var_pw:.6f})"
        )
    report.ok(
        "call: shared-path difference variance tends to the pathwise variance (h = 0.001, rel 1%)",
        rel(call_var[0.001], var_pw) <= 0.01,
        f"{call_var[0.001]:.6f} vs {var_pw:.6f}",
    )
    limit = DISC**2 * np.exp(log_density(K, S0, SIG)) * K / S0
    dig_hvar = {}
    for hh in (1.0, 0.1, 0.01, 0.001):
        p_cross = stats.norm.cdf(z_of(K, S0, SIG)) - stats.norm.cdf(
            z_of(K * S0 / (S0 + hh), S0, SIG)
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
    fd = DISC * ((path(S0 + 1.0, SIG, Z) > K).astype(float) - itm) / 1.0
    print(
        f"  digital, h = 1 sample variance on the shared paths: {np.var(fd, ddof=1):.6f} (exact"
        " above)"
    )


def main() -> int:
    """Print the versions and closed forms, then run the four parts with one report.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
    report = CheckReport()
    cf = ClosedForms.bsm()
    print(
        f"closed forms: call {cf.call:.4f}, delta {cf.call_delta:.5f}, vega {cf.call_vega:.4f},"
        f" gamma {cf.call_gamma:.6f}"
    )
    print(
        f"  dC/dK {cf.call_dK:.5f}; digital delta {cf.dig_delta:.6f}, digital dD/dK {cf.dig_dK:.6f}"
    )
    check_deterministic(report, cf)
    d = Draws.draw(np.random.default_rng(SEED))
    res, dig_lr = check_estimators(report, cf, d)
    report_comparisons(cf, d, res, dig_lr)
    check_fd_variance(report, d)
    print("FAILED:" + ", ".join(report.failures) if report.failures else "all checks passed")
    return 1 if report.failures else 0


if __name__ == "__main__":
    sys.exit(main())
