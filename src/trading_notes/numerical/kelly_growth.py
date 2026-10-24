"""Kelly growth: the optimal fraction, half Kelly, daily rebalancing and estimation error.

Library gap-filling Batch L1, package P5 (2026-10-21): the worked examples of
res:kelly-growth-optimal-fraction.

Continuous model: constant mu = 8 percent, r = 2 percent, sigma = 20 percent, a constant fraction f
of wealth in the risky asset and the rest in cash, no costs or leverage limits. Acceptance, fixed
before the first run:
  - the continuous identity is tested with its matching model, exact continuous-time log-wealth
    sampling (200,000 draws over 10 years, seed 20261041);
  - daily rebalancing is tested separately against its expectation, computed by 80-point
    Gauss-Hermite quadrature (20,000 paths x 2,520 steps, seed 20261042), with the discretisation
    bias below 5e-4 a year and a first-order refinement ratio in [0.4, 0.6];
  - discrete bets show that the 3/4 half-Kelly identity is a property of the continuous model only.
The estimation-error illustration (seed 20261043) uses a stated criterion of its own. Synthetic
data only.

Correction, 2026-10-21 (L1 audit finding L1-F1): the first version ran the daily-rebalancing checks
at f = 0.75, 1.5 and 3 and called the quadrature value an exact expectation. For f > 1 the one-day
gross factor (1 - f) e^(r dt) + f R is nonpositive on a Gaussian tail of positive probability
(about 1e-227 at f = 3), so E[ln] is not defined; the quadrature nodes and the simulated paths
simply missed that tail. The daily checks now use the admissible unlevered fractions 0.25, 0.5 and
0.75 (half Kelly), with the same seed, tolerances and refinement test; the quadrature is treated as
a numerical approximation and its convergence is checked. The leveraged fractions stay in the
continuous-model checks, where wealth is always positive.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.kelly_growth
(numpy, scipy). Exits 1 on failure. About 5 seconds.
"""

# standard library imports
import math
import sys
from typing import Final

# third party library imports
import numpy as np
import scipy
import scipy.integrate
import scipy.stats

# project library imports
from trading_notes.numerical.report import CheckReport

MU: Final = 0.08
R: Final = 0.02
SG: Final = 0.20
F_STAR: Final = (MU - R) / SG**2
DT: Final = 1 / 252  # one day of daily rebalancing


def g(f: float) -> float:
    """Continuous log growth rate of wealth with fraction f in the asset (Ito)."""
    return R + f * (MU - R) - 0.5 * f**2 * SG**2


def z_ruin(f: float, step: float) -> float:
    """Return the draw Z at or below which one step's gross factor is nonpositive (f > 1)."""
    return (math.log((f - 1) * math.exp(R * step) / f) - (MU - SG**2 / 2) * step) / (
        SG * math.sqrt(step)
    )


def g_discrete(f: float, step: float, nodes: int = 80) -> float:
    """Expected log growth per year with the fraction 0 <= f <= 1 restored every step.

    GBM within the step. Gauss-Hermite quadrature: a numerical approximation, checked for
    convergence below.
    """
    z, w = np.polynomial.hermite_e.hermegauss(nodes)
    w = w / w.sum()
    gross = (1 - f) * math.exp(R * step) + f * np.exp(
        (MU - SG**2 / 2) * step + SG * math.sqrt(step) * z
    )
    return float(np.sum(w * np.log(gross))) / step


def g_adaptive(f: float, step: float) -> float:
    """The same expectation by adaptive integration against the normal density.

    Independent of the quadrature nodes.
    """

    def integrand(z: float) -> float:
        gross = (1 - f) * math.exp(R * step) + f * math.exp(
            (MU - SG**2 / 2) * step + SG * math.sqrt(step) * z
        )
        return math.log(gross) * scipy.stats.norm.pdf(z)

    return (
        scipy.integrate.quad(integrand, -np.inf, np.inf, epsabs=1e-15, epsrel=1e-13, limit=200)[0]
        / step
    )


def G(f: float, p: float, b: float) -> float:
    """Return the expected log growth of betting the fraction f at win probability p, odds b."""
    return p * math.log(1 + b * f) + (1 - p) * math.log(1 - f)


def check_identities(report: CheckReport) -> None:
    """Part 1: the Kelly fraction and the half-Kelly identities of the continuous model."""
    print("== continuous model: identities")
    report.ok("f* = (mu - r)/sigma^2 = 1.5", abs(F_STAR - 1.5) < 1e-12)
    ex_full, ex_half = g(F_STAR) - R, g(F_STAR / 2) - R
    report.ok(
        "excess growth 0.045 at Kelly and 0.03375 at half Kelly, ratio 0.75 exactly",
        abs(ex_full - 0.045) < 1e-12
        and abs(ex_half - 0.03375) < 1e-12
        and abs(ex_half / ex_full - 0.75) < 1e-12,
    )
    report.ok(
        "variance-rate ratio (f sigma)^2 of half Kelly to Kelly is 0.25",
        abs((0.5) ** 2 - 0.25) < 1e-15,
    )
    report.ok("twice Kelly earns no excess growth: g(2 f*) = r", abs(g(2 * F_STAR) - R) < 1e-12)


def check_log_wealth(report: CheckReport) -> None:
    """Part 2: exact log-wealth sampling over 10 years against g(f)."""
    print("== continuous model: exact log-wealth sampling over 10 years")
    T = 10.0
    rng = np.random.default_rng(20261041)
    WT = rng.standard_normal(200_000) * math.sqrt(T)
    fracs = {"half Kelly": F_STAR / 2, "Kelly": F_STAR, "twice Kelly": 2 * F_STAR}
    for name, f in fracs.items():
        lw = (g(f) * T + f * SG * WT) / T
        m, se, sd = lw.mean(), lw.std(ddof=1) / math.sqrt(len(lw)), lw.std(ddof=1)
        report.ok(
            f"{name} (f = {f:.4g}): mean ln W_T / T within 3 s.e. of g(f) = {g(f):.5f}; s.d. within"
            " 1% of f sigma / sqrt(T)",
            abs(m - g(f)) <= 3 * se and abs(sd / (f * SG / math.sqrt(T)) - 1) < 0.01,
            f"{m:.5f} (s.e. {se:.5f}), s.d. {sd:.4f}",
        )


def check_levered_ruin(report: CheckReport) -> None:
    """Part 3: why the levered fractions are excluded from daily rebalancing."""
    print("== daily rebalancing: why the levered fractions are excluded")
    # With the fraction f restored at the start of each day, the gross factor over the day is
    # (1 - f) e^(r dt) + f R, R = exp((mu - sigma^2/2) dt + sigma sqrt(dt) Z). For f > 1 it is
    # nonpositive when Z <= z_ruin, so ln W_T has no (unconditional, real) expectation however
    # small that probability is.
    for f in (F_STAR, 2 * F_STAR):
        zr = z_ruin(f, DT)
        log10_p = scipy.stats.norm.logcdf(zr) / math.log(10)
        gross = (1 - f) * math.exp(R * DT) + f * math.exp(
            (MU - SG**2 / 2) * DT + SG * math.sqrt(DT) * (zr - 1)
        )
        report.ok(
            f"f = {f:g}: one-day wealth is nonpositive for Z <= {zr:.2f}, a positive probability"
            f" (10^{log10_p:.0f})",
            gross < 0 and math.isfinite(log10_p) and log10_p > -math.inf,
            f"gross factor {gross:+.4f} at Z = {zr - 1:.2f}",
        )


def check_daily_rebalancing(report: CheckReport) -> None:
    """Part 4: daily rebalancing of unlevered fractions against its quadrature expectation."""
    print("== daily rebalancing with unlevered fractions against its quadrature expectation")
    daily = {"quarter": 0.25, "half": 0.5, "half Kelly": F_STAR / 2}
    report.ok(
        "f = 1 needs no rebalancing: quadrature gives mu - sigma^2/2 = g(1) exactly (to 1e-12)",
        abs(g_discrete(1.0, DT) - (MU - SG**2 / 2)) < 1e-12
        and abs(g(1.0) - (MU - SG**2 / 2)) < 1e-15,
    )
    steps, n_paths = 2520, 20_000
    rng = np.random.default_rng(20261042)
    logw = {name: np.zeros(n_paths) for name in daily}
    for _ in range(steps):
        R_step = np.exp((MU - SG**2 / 2) * DT + SG * math.sqrt(DT) * rng.standard_normal(n_paths))
        for name, f in daily.items():
            logw[name] += np.log((1 - f) * math.exp(R * DT) + f * R_step)
    for name, f in daily.items():
        gd, gh = g_discrete(f, DT), g_discrete(f, DT / 2)
        bias, bias_half = gd - g(f), gh - g(f)
        quad_err = max(
            abs(g_discrete(f, DT, 40) - gd),
            abs(g_discrete(f, DT, 160) - gd),
            abs(g_adaptive(f, DT) - gd),
            abs(g_discrete(f, DT / 2, 160) - gh),
            abs(g_adaptive(f, DT / 2) - gh),
        )
        report.ok(
            f"{name} (f = {f:g}): 40-, 80- and 160-node quadrature and adaptive integration agree"
            " within 1e-10 a"
            " year, below 1/1000 of the bias",
            quad_err < 1e-10 and quad_err < 1e-3 * abs(bias_half),
            f"largest difference {quad_err:.1e}",
        )
        x = logw[name] / (steps * DT)
        m, se = x.mean(), x.std(ddof=1) / math.sqrt(n_paths)
        report.ok(
            f"{name}: simulated daily-rebalanced mean within 3 s.e. of the quadrature value"
            f" {gd:.6f}",
            abs(m - gd) <= 3 * se,
            f"{m:.5f} (s.e. {se:.5f})",
        )
        report.ok(
            f"{name}: discretisation bias {bias:+.2e} a year is below 5e-4; halving the step scales"
            " it by"
            " [0.4, 0.6]",
            abs(bias) < 5e-4 and 0.4 <= bias_half / bias <= 0.6,
            f"ratio {bias_half / bias:.3f}",
        )


def check_discrete_bets(report: CheckReport) -> None:
    """Part 5: discrete bets, where the 3/4 half-Kelly identity does not carry over."""
    print("== discrete bets: the 3/4 identity does not carry over")
    for p, b, f_exp, ratio_exp in ((0.6, 1.0, 0.2, 0.7470), (0.3, 4.0, 0.125, 0.7727)):
        fk = p - (1 - p) / b
        grid = np.linspace(0, 0.99, 99_001)
        numeric = grid[np.argmax([G(x, p, b) for x in grid])]
        ratio = G(fk / 2, p, b) / G(fk, p, b)
        report.ok(
            f"p = {p}, b = {b}: f* = p - q/b = {f_exp} (grid search agrees); half-Kelly growth"
            f" ratio {ratio_exp},"
            " not 0.75",
            abs(fk - f_exp) < 1e-12
            and abs(numeric - fk) < 1e-4
            and abs(ratio - ratio_exp) < 5e-5
            and abs(ratio - 0.75) > 1e-3,
            f"{ratio:.4f}",
        )


def check_estimation_error(report: CheckReport) -> None:
    """Part 6: expected excess growth of fractions of a Kelly bet on an estimated mu."""
    print("== estimation error in mu")
    # mu estimated from 10 years of returns: mu_hat ~ N(mu, sigma^2 / 10). Expected excess growth
    # of the fraction c (mu_hat - r) / sigma^2 is
    # c f* (mu - r) - 0.5 c^2 sigma^2 (f*^2 + s^2 / sigma^4), s^2 = sigma^2 / 10. Criterion fixed
    # before running: Monte Carlo (200,000 estimates) within 3 s.e. of the formula for c = 1 and
    # c = 1/2, with full Kelly negative and half Kelly positive in expectation.
    s2 = SG**2 / 10
    rng = np.random.default_rng(20261043)
    mu_hat = MU + math.sqrt(s2) * rng.standard_normal(200_000)
    for c, sign in ((1.0, -1), (0.5, 1)):
        f_hat = c * (mu_hat - R) / SG**2
        sim = f_hat * (MU - R) - 0.5 * f_hat**2 * SG**2
        formula = c * F_STAR * (MU - R) - 0.5 * c**2 * SG**2 * (F_STAR**2 + s2 / SG**4)
        report.ok(
            f"fraction {c} of estimated Kelly: expected excess growth {formula:+.5f}, sign"
            f" {sign:+d}",
            abs(sim.mean() - formula) <= 3 * sim.std(ddof=1) / math.sqrt(len(sim))
            and formula * sign > 0,
            f"simulated {sim.mean():+.5f}",
        )


def main() -> int:
    """Print the versions, then run the six parts with one report.

    Parts 2, 4 and 6 each draw from their own seeded generator.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
    report = CheckReport()
    check_identities(report)
    check_log_wealth(report)
    check_levered_ruin(report)
    check_daily_rebalancing(report)
    check_discrete_bets(report)
    check_estimation_error(report)
    if report.failures:
        print("FAILED:", ", ".join(report.failures))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
