"""Short-rate and forward-rate models on the GSW curve: CIR, Hull-White, HJM and a caplet."""

import csv
import itertools
import math
import sys
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Final

import numpy as np
import scipy
from numpy.typing import NDArray
from scipy import integrate, stats

from trading_notes.numerical.arbitrage_free_valuation.short_rate_models import (
    GSW_2026_09_30,
    GSW_CURVE,
    CoxIngersollRoss,
    HullWhite,
)
from trading_notes.numerical.report import CheckReport, print_versions
from trading_notes.numerical.repository import repository_root

type Floats = NDArray[np.float64]

GSW_FILE: Final = Path("reading_materials/derivatives-validation/empirical/feds200628.csv")
CURVE: Final = GSW_CURVE
HW: Final = HullWhite(curve=CURVE, a=0.1, sigma=0.01)  # illustrative, not calibrated
CIR: Final = CoxIngersollRoss(a=0.5, b=0.04, sigma=0.10)
CIR_RATE: Final = 0.03
CIR_MATURITY: Final = 5.0
MATURITIES: Final = tuple(range(1, 31))


def check_curve(report: CheckReport, root: Path) -> Floats:
    """The GSW curve: the stored parameters, the published yields and the forward slope.

    Args:
        report: The run's report.
        root: The repository root; the published file is read when it is present.

    Returns:
        The GSW discount factors at 1-30 years.
    """
    print("== The GSW curve of 30 September 2026")
    published = None
    if (root / GSW_FILE).exists():
        with (root / GSW_FILE).open() as fh:
            rows = list(csv.reader(fh))
        header = next(r for r in rows if r and r[0] == "Date")
        row = dict(zip(header, next(r for r in rows if r and r[0] == "2026-09-30"), strict=True))
        report.ok(
            "the six parameters written in the module equal the file's row for 2026-09-30",
            all(float(row[k]) == v for k, v in GSW_2026_09_30.items()),
        )
        published = {n: float(row[f"SVENY{n:02d}"]) for n in range(1, 31)}
    else:
        print("  (feds200628.csv not present: the published-yield comparison is skipped)")
    P_gsw = np.array([CURVE.discount(T) for T in MATURITIES])
    report.ok(
        "the zero yield is the average of the forward curve (quadrature) to 1e-12 at 1-30 years",
        bool(
            max(
                abs(
                    integrate.quad(CURVE.forward, 0, T, epsabs=1e-14, epsrel=1e-12)[0]
                    - CURVE.zero_yield(T) * T
                )
                for T in MATURITIES
            )
            < 1e-12
        ),
    )
    if published is not None:
        gap = max(abs(100 * CURVE.zero_yield(n) - published[n]) for n in range(1, 31))
        report.ok(
            "the zero yields reproduce the published SVENY01-SVENY30 (4 decimals) to 5e-5"
            " percentage points",
            gap <= 5e-5 + 1e-9,
            f"largest gap {gap:.2e}",
        )
    h = 1e-4
    report.ok(
        "the analytic forward slope matches a central difference to 1e-8",
        max(
            abs(CURVE.forward_slope(t) - (CURVE.forward(t + h) - CURVE.forward(t - h)) / (2 * h))
            for t in (0.5, 2, 7, 15, 29)
        )
        < 1e-8,
    )
    fwd, y, P = CURVE.forward, CURVE.zero_yield, CURVE.discount
    print(
        f"  f(0,0) = {100 * fwd(0):.4f}%, y(1) = {100 * y(1):.4f}%, y(10) = {100 * y(10):.4f}%,"
        f" y(30) = {100 * y(30):.4f}%; P(0,10) = {P(10):.6f}, P(0,30) = {P(30):.6f}"
    )
    return P_gsw


def check_closed_forms(report: CheckReport) -> float:
    """Vasicek's four-year zero again, and the CIR closed form against its pricing PDE.

    Args:
        report: The run's report.

    Returns:
        The CIR five-year zero price.
    """
    print("== Vasicek (reused) and CIR closed forms")
    a_v, b_v, s_v, r_v = 0.1, 0.05, 0.01, 0.04
    B4 = (1 - math.exp(-a_v * 4)) / a_v
    A4 = math.exp((B4 - 4) * (a_v**2 * b_v - s_v**2 / 2) / a_v**2 - s_v**2 * B4**2 / (4 * a_v))
    report.ok(
        "Vasicek four-year zero (Hull eqs. 31.6-31.8) is the existing 0.846849",
        abs(A4 * math.exp(-B4 * r_v) - 0.846849) < 5e-7,
        f"{A4 * math.exp(-B4 * r_v):.6f}",
    )
    a_c, b_c, s_c = CIR.a, CIR.b, CIR.sigma
    P_cir = CIR.price(CIR_RATE, CIR_MATURITY)
    report.ok("Feller condition 2ab >= sigma^2 holds (0.04 >= 0.01)", 2 * a_c * b_c >= s_c**2)

    # The bond price must solve P_t + a(b - r) P_r + 0.5 sigma^2 r P_rr = r P (Hull eq. 31.5).
    def pde_residual(r: float, tau: float, hr: float = 1e-4, ht: float = 1e-5) -> float:
        p = CIR.price(r, tau)
        p_r = (CIR.price(r + hr, tau) - CIR.price(r - hr, tau)) / (2 * hr)
        p_rr = (CIR.price(r + hr, tau) - 2 * p + CIR.price(r - hr, tau)) / hr**2
        p_t = -(CIR.price(r, tau + ht) - CIR.price(r, tau - ht)) / (2 * ht)
        return p_t + a_c * (b_c - r) * p_r + 0.5 * s_c**2 * r * p_rr - r * p

    res = max(abs(pde_residual(r, tau)) for r in (0.01, 0.03, 0.08) for tau in (0.5, 5.0))
    report.ok(
        "the CIR closed form solves the bond-pricing PDE (residual < 1e-6)",
        res < 1e-6,
        f"{res:.1e}",
    )
    print(f"  CIR five-year zero, closed form: {P_cir:.6f}")
    return P_cir


def check_cir_exact(report: CheckReport, P_cir: float) -> None:
    """The CIR five-year zero by exact non-central chi-square transitions, grid halved to converge.

    Args:
        report: The run's report.
        P_cir: The closed-form price.
    """
    print("== CIR by exact non-central chi-square transitions (200,000 paths)")
    a_c, b_c, s_c = CIR.a, CIR.b, CIR.sigma
    n_cir, h_min = 200_000, 1 / 128
    steps = round(CIR_MATURITY / h_min)
    c_fac = s_c**2 * (1 - math.exp(-a_c * h_min)) / (4 * a_c)
    dof = 4 * a_c * b_c / s_c**2
    rng = np.random.default_rng(20261062)
    r_path = np.full(n_cir, CIR_RATE)
    min_cir = CIR_RATE
    # Trapezoid sums of the exact rate samples on grids h = 1/4, 1/8, ..., 1/128, on the same paths.
    levels = [32, 16, 8, 4, 2, 1]  # stride in units of h_min
    trap = {k: np.zeros(n_cir) for k in levels}
    prev = {k: r_path.copy() for k in levels}
    for i in range(1, steps + 1):
        r_path = c_fac * rng.noncentral_chisquare(dof, r_path * math.exp(-a_c * h_min) / c_fac)
        min_cir = min(min_cir, float(r_path.min()))
        for k in levels:
            if i % k == 0:
                trap[k] += 0.5 * (prev[k] + r_path) * k * h_min
                prev[k] = r_path.copy()
    report.ok("exact CIR samples are never negative", min_cir >= 0, f"minimum {min_cir:.2e}")
    est = {}
    for k in levels:
        df = np.exp(-trap[k])
        est[k] = (float(df.mean()), float(df.std(ddof=1) / math.sqrt(n_cir)))
    chosen = None
    for coarse, fine in itertools.pairwise(levels):
        change = abs(est[fine][0] - est[coarse][0])
        print(
            f"  h = 1/{round(1 / (fine * h_min))}: {est[fine][0]:.6f} (s.e. {est[fine][1]:.6f}),"
            f" change from 1/{round(1 / (coarse * h_min))} {change:.2e}"
        )
        if change < 0.1 * est[fine][1]:
            chosen = fine
            break
    report.ok(
        "halving the integration grid changes the price by less than 0.1 s.e. at some h >= 1/128",
        chosen is not None,
    )
    if chosen is not None:
        m, se = est[chosen]
        report.ok(
            "CIR closed-form five-year zero lies within 3 s.e. of the exact-transition Monte Carlo",
            abs(m - P_cir) <= 3 * se,
            f"{m:.6f} (s.e. {se:.6f}) against {P_cir:.6f}, z = {(m - P_cir) / se:+.2f}",
        )


def check_cir_euler(report: CheckReport) -> None:
    """CIR with the Feller condition failing: untruncated Euler against exact sampling.

    Args:
        report: The run's report.
    """
    print(
        "== CIR with sigma = 25 percent (Feller fails): Euler against exact sampling (10,000 paths)"
    )
    a_c, b_c = CIR.a, CIR.b
    s_hi, n_e, dt_e = 0.25, 10_000, 1 / 12
    rng = np.random.default_rng(20261063)
    r_eu = np.full(n_e, CIR_RATE)
    r_ex = np.full(n_e, CIR_RATE)
    neg_eu = np.zeros(n_e, dtype=bool)
    min_ex = np.inf
    c_hi = s_hi**2 * (1 - math.exp(-a_c * dt_e)) / (4 * a_c)
    for _ in range(round(CIR_MATURITY / dt_e)):
        z = rng.standard_normal(n_e)
        live = ~neg_eu
        r_eu[live] = (
            r_eu[live]
            + a_c * (b_c - r_eu[live]) * dt_e
            + s_hi * np.sqrt(r_eu[live] * dt_e) * z[live]
        )
        neg_eu |= r_eu < 0  # an untruncated Euler step cannot continue past a negative rate
        r_ex = c_hi * rng.noncentral_chisquare(
            4 * a_c * b_c / s_hi**2, r_ex * math.exp(-a_c * dt_e) / c_hi
        )
        min_ex = min(min_ex, float(r_ex.min()))
    report.ok(
        "untruncated monthly Euler produces negative rates on some paths; exact sampling never"
        " does",
        bool(neg_eu.sum() > 0 and min_ex >= 0),
        f"Euler negative on {neg_eu.sum()} of {n_e} paths; exact minimum {min_ex:.2e}",
    )


def int_alpha(T: float) -> float:
    """Return int_0^T alpha by quadrature of theta: r0 B(0,T) + int theta(s) B(T - s) ds."""
    q = integrate.quad(
        lambda s: HW.theta(s) * HW.b(T - s), 0, T, epsabs=1e-14, epsrel=1e-12, limit=200
    )[0]
    return CURVE.forward(0.0) * HW.b(T) + q


def check_hull_white(report: CheckReport, P_gsw: Floats) -> None:
    """Hull-White fitted to the GSW curve: zero prices and the mean short rate.

    Args:
        report: The run's report.
        P_gsw: The GSW discount factors at 1-30 years.
    """
    print("== Hull-White fitted to the GSW curve (a = 0.1, sigma = 1 percent, illustrative)")
    a = HW.a
    r0 = CURVE.forward(0.0)
    # Wilmott eq. (31.2) with Hull's theta:
    # ln P(0,T) = -int theta B - r0 B + (sigma^2/2a^2)[T - 2B + (1-e^{-2aT})/2a].
    P_hw = np.array([math.exp(-int_alpha(T) + 0.5 * HW.var_int(T)) for T in MATURITIES])
    gap = float(np.max(np.abs(P_hw - P_gsw)))
    report.ok(
        "analytic Hull-White zero prices equal the GSW discount factors at 1-30 years to 1e-10",
        gap < 1e-10,
        f"{gap:.1e}",
    )

    def alpha_quad(t: float) -> float:
        q = integrate.quad(
            lambda s: math.exp(-a * (t - s)) * HW.theta(s), 0, t, epsabs=1e-14, epsrel=1e-12
        )[0]
        return r0 * math.exp(-a * t) + q

    report.ok(
        "the mean short rate implied by theta equals F(0,t) + sigma^2 (1 - e^{-at})^2 / (2a^2) to"
        " 1e-10",
        max(abs(alpha_quad(t) - HW.alpha(t)) for t in (0.5, 1, 5, 10, 20, 30)) < 1e-10,
    )
    print(
        f"  theta/a at t = 0, 5, 20 years: {HW.theta(0) / a:.4f}, {HW.theta(5) / a:.4f},"
        f" {HW.theta(20) / a:.4f}; forward premium alpha - F at 30 years"
        f" {1e4 * (HW.alpha(30) - CURVE.forward(30)):.1f} bp"
    )


def check_hull_white_paths(report: CheckReport, P_gsw: Floats) -> None:
    """Hull-White Monte Carlo by exact joint sampling of the factor and its integral.

    Args:
        report: The run's report.
        P_gsw: The GSW discount factors at 1-30 years.
    """
    print("== Hull-White Monte Carlo: exact joint sampling of (x, integral of x), 100,000 paths")
    a, sg = HW.a, HW.sigma
    n_hw, sub = 100_000, 24  # half-monthly steps; monthly results by aggregation on the same paths
    dt = 1 / sub
    e1 = math.exp(-a * dt)
    var_x = sg**2 * (1 - e1**2) / (2 * a)
    var_i = HW.var_int(dt)
    cov = sg**2 / (2 * a**2) * (1 - e1) ** 2
    L = np.linalg.cholesky(np.array([[var_x, cov], [cov, var_i]]))
    rng = np.random.default_rng(20261061)
    x = np.zeros(n_hw)
    integ = np.zeros(n_hw)
    trap_m = np.zeros(n_hw)
    trap_h = np.zeros(n_hw)
    x_prev_m = np.zeros(n_hw)
    I_at = {}
    trap_m_at, trap_h_at = {}, {}
    for k in range(1, 30 * sub + 1):
        t_prev, t_now = (k - 1) * dt, k * dt
        z = rng.standard_normal((2, n_hw))
        eps = L @ z
        x_new = x * e1 + eps[0]
        integ += x * HW.b(dt) + eps[1]
        # trapezoid on the exact short-rate samples r = x + alpha, half-monthly and monthly
        trap_h += 0.5 * dt * ((x + HW.alpha(t_prev)) + (x_new + HW.alpha(t_now)))
        x = x_new
        if k % 2 == 0:
            trap_m += (
                0.5 * (2 * dt) * ((x_prev_m + HW.alpha(t_now - 2 * dt)) + (x + HW.alpha(t_now)))
            )
            x_prev_m = x.copy()
        if k % sub == 0:
            T = k // sub
            I_at[T] = integ.copy()
            trap_m_at[T], trap_h_at[T] = trap_m.copy(), trap_h.copy()
    z_scores = []
    for T, P in zip(MATURITIES, P_gsw, strict=True):
        df = math.exp(-int_alpha(T)) * np.exp(-I_at[T])
        m, se = float(df.mean()), float(df.std(ddof=1) / math.sqrt(n_hw))
        z_scores.append((m - P) / se)
    zs = np.array(z_scores)
    report.ok(
        "simulated discount factors lie within 4 s.e. of the GSW discount factors at all 30"
        " maturities",
        bool(np.all(np.abs(zs) <= 4)),
        f"largest |z| {np.abs(zs).max():.2f} at {MATURITIES[int(np.abs(zs).argmax())]} years",
    )
    print(
        "  z at 1, 5, 10, 20, 30 years: "
        + ", ".join(f"{zs[T - 1]:+.2f}" for T in (1, 5, 10, 20, 30))
    )
    df_m = np.exp(-trap_m_at[30])
    df_h = np.exp(-trap_h_at[30])
    se30 = float(df_h.std(ddof=1) / math.sqrt(n_hw))
    change = abs(float(df_h.mean()) - float(df_m.mean()))
    verdict = "usable" if change < 0.1 * se30 else "biased (reported, not used)"
    print(
        f"  diagnostic: trapezoid 30-year discount factor {df_m.mean():.6f} monthly,"
        f" {df_h.mean():.6f} half-monthly (change {change:.2e}, 0.1 s.e. {0.1 * se30:.2e}):"
        f" {verdict}; GSW {P_gsw[-1]:.6f}"
    )
    neg_share = float(np.mean(x + HW.alpha(30.0) < 0))
    print(f"  share of paths with a negative short rate at 30 years: {neg_share:.4f}")


def hjm_short_rate_det(t: float, vol: Callable[[float, float], float]) -> float:
    """Return the deterministic part of r(t) = F(t,t) under HJM with volatility vol(s, T).

    F(0,t) + int_0^t m(s,t) ds with the drift m(s,T) = v(s,T) int_s^T v(s,u) du.
    """

    def m(s: float) -> float:
        return vol(s, t) * integrate.quad(lambda u: vol(s, u), s, t, epsabs=1e-14, epsrel=1e-12)[0]

    return CURVE.forward(t) + integrate.quad(m, 0, t, epsabs=1e-14, epsrel=1e-12)[0]


def richardson_slope(f: Callable[[float], float], t: float, h: float = 1e-2) -> float:
    """Return the derivative of f at t by Richardson extrapolation of two central differences."""
    d1 = (f(t + h) - f(t - h)) / (2 * h)
    d2 = (f(t + h / 2) - f(t - h / 2)) / h
    return (4 * d2 - d1) / 3


def check_hjm(report: CheckReport) -> None:
    """The HJM drift condition reproduces the Ho-Lee and Hull-White short-rate drifts.

    Args:
        report: The run's report.
    """
    print("== HJM drift condition on the GSW curve")
    a, sg = HW.a, HW.sigma
    s_h = 0.01

    def const(s: float, u: float) -> float:
        return s_h

    for t in (1.0, 5.0, 12.0):
        slope = richardson_slope(lambda u: hjm_short_rate_det(u, const), t)
        report.ok(
            f"constant volatility: the short-rate drift at t = {t:g} equals dF(0,t)/dt + sigma^2 t"
            " (Ho-Lee) to 1e-10",
            abs(slope - (CURVE.forward_slope(t) + s_h**2 * t)) < 1e-10,
            f"{slope:.12f}",
        )

    def expo(s: float, u: float) -> float:
        return sg * math.exp(-a * (u - s))

    for t in (1.0, 5.0, 12.0):
        det = hjm_short_rate_det(t, expo)
        slope = richardson_slope(lambda u: hjm_short_rate_det(u, expo), t)
        report.ok(
            f"sigma e^(-a(T-t)): drift at t = {t:g} plus a times the deterministic rate equals"
            " Hull's theta (32.5) to 1e-10",
            abs(slope + a * det - HW.theta(t)) < 1e-10,
        )


def check_forward_market(report: CheckReport) -> None:
    """A caplet in the forward market model under the rolling spot measure, against Black.

    Args:
        report: The run's report.
    """
    print("== Forward market model: a caplet under the rolling spot measure (100,000 paths)")
    lam, n_fm, sub_fm, k_cap = 0.20, 100_000, 12, 5  # caplet on the year-5 to year-6 forward
    Pk = np.array([CURVE.discount(t) for t in range(0, k_cap + 2)])
    F0 = Pk[:-1] / Pk[1:] - 1  # annual forwards F_0..F_{k_cap}, actual/actual with delta = 1
    K = float(F0[k_cap])  # at the money
    rng = np.random.default_rng(20261064)
    logF = np.tile(np.log(F0), (n_fm, 1))
    disc = 1 / (1 + F0[0]) * np.ones(n_fm)
    d = 1 / sub_fm
    for j in range(k_cap):  # periods (t_j, t_{j+1}]; forwards j+1..k_cap are alive
        for _ in range(sub_fm):
            z = rng.standard_normal(n_fm)
            F = np.exp(logF[:, j + 1 :])
            w = F * lam / (1 + F)  # delta_i F_i Lambda / (1 + delta_i F_i), Hull eq. (33.10)
            drift = lam * np.cumsum(w, axis=1) - 0.5 * lam**2
            logF[:, j + 1 :] += drift * d + lam * math.sqrt(d) * z[:, None]
        disc /= 1 + np.exp(logF[:, j + 1])  # roll the numeraire at t_{j+1} at the rate just set
    payoff = np.maximum(np.exp(logF[:, k_cap]) - K, 0.0) * disc
    mc, se = float(payoff.mean()), float(payoff.std(ddof=1) / math.sqrt(n_fm))
    sd = lam * math.sqrt(k_cap)
    d1 = (math.log(F0[k_cap] / K) + sd**2 / 2) / sd
    black = Pk[k_cap + 1] * (F0[k_cap] * stats.norm.cdf(d1) - K * stats.norm.cdf(d1 - sd))
    report.ok(
        "the simulated caplet agrees with Black's formula (Hull eq. 29.7) within 3 s.e.",
        bool(abs(mc - black) <= 3 * se),
        f"{1e4 * mc:.3f} bp (s.e. {1e4 * se:.3f}) against {1e4 * black:.3f} bp per unit notional,"
        f" z = {(mc - black) / se:+.2f}",
    )
    zc = (float(disc.mean()) - Pk[k_cap + 1]) / float(disc.std(ddof=1) / math.sqrt(n_fm))
    report.ok(
        "the rolled numeraire reprices the six-year zero within 3 s.e. (the curve is an input)",
        bool(abs(zc) <= 3),
        f"z = {zc:+.2f}",
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Print the versions, then run the eight parts with one report.

    The worked examples of mod:affine-short-rate-models, mod:hjm-forward-rate-models and the
    curve-fitting extension of mod:term-structure-models-simulation.

    Curve: the Federal Reserve Board's Gurkaynak-Sack-Wright Svensson parameters for 30 September
    2026, from feds200628.csv (source fed-gsw-data; the file is kept outside Git, SHA-256
    7286435090933f0d...0bb89335c). The six parameters are written in the shared short-rate module
    so that the checks run without the file; when the file is present at
    reading_materials/derivatives-validation/empirical/feds200628.csv under the root, the row is
    read again and the published zero yields are checked too. The curve is a fitted off-the-run
    nominal Treasury zero curve, not SOFR or OIS. The mean-reversion and volatility parameters
    (a = 0.1, sigma = 1 percent) are illustrative and not calibrated: calibration needs cap or
    swaption volatilities, which are not held.

    Seeds: 20261061 Hull-White paths, 20261062 CIR exact paths, 20261063 the CIR Euler and exact
    comparison, 20261064 the forward-market caplet. Every check except the curve shows that a
    model is implemented correctly under its own assumptions; none is evidence about markets.

    Args:
        argv: Command-line arguments: `--root DIR`, the repository root that may hold the
            published file (default: the working directory).

    Returns:
        The exit status, 0 or 1.
    """
    root = repository_root(__doc__ or "", argv)
    print_versions(np, scipy)
    report = CheckReport()
    P_gsw = check_curve(report, root)
    P_cir = check_closed_forms(report)
    check_cir_exact(report, P_cir)
    check_cir_euler(report)
    check_hull_white(report, P_gsw)
    check_hull_white_paths(report, P_gsw)
    check_hjm(report)
    check_forward_market(report)
    return report.summarise()


if __name__ == "__main__":
    sys.exit(main())
