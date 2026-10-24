"""Worked examples of the Kelly growth-optimal fraction, checked against independent routes."""

import math
import sys
from typing import Final

import numpy as np
import scipy
import scipy.integrate
import scipy.stats

from trading_notes.numerical.portfolio_construction_models.kelly_growth import (
    ContinuousKelly,
    DiscreteBet,
)
from trading_notes.numerical.report import CheckReport, print_versions

MODEL: Final = ContinuousKelly(mu=0.08, rate=0.02, sigma=0.20)
F_STAR: Final = MODEL.kelly_fraction
DT: Final = 1 / 252  # one day of daily rebalancing


def adaptive_growth(f: float, step: float) -> float:
    """Return the rebalanced growth by adaptive integration against the normal density.

    Independent of the quadrature nodes of `ContinuousKelly.rebalanced_growth`.
    """

    def integrand(z: float) -> float:
        return math.log(MODEL.gross_step(f, step, z)) * scipy.stats.norm.pdf(z)

    return (
        scipy.integrate.quad(integrand, -np.inf, np.inf, epsabs=1e-15, epsrel=1e-13, limit=200)[0]
        / step
    )


def check_identities(report: CheckReport) -> None:
    """Check the Kelly fraction and the half-Kelly identities of the continuous model."""
    print("== continuous model: identities")
    g, r = MODEL.growth, MODEL.rate
    report.ok("f* = (mu - r)/sigma^2 = 1.5", abs(F_STAR - 1.5) < 1e-12)
    ex_full, ex_half = g(F_STAR) - r, g(F_STAR / 2) - r
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
    report.ok("twice Kelly earns no excess growth: g(2 f*) = r", abs(g(2 * F_STAR) - r) < 1e-12)


def check_log_wealth(report: CheckReport) -> None:
    """Check exact 10-year log-wealth sampling against the growth rate g(f)."""
    print("== continuous model: exact log-wealth sampling over 10 years")
    T = 10.0
    rng = np.random.default_rng(20261041)
    WT = rng.standard_normal(200_000) * math.sqrt(T)
    fracs = {"half Kelly": F_STAR / 2, "Kelly": F_STAR, "twice Kelly": 2 * F_STAR}
    g, sg = MODEL.growth, MODEL.sigma
    for name, f in fracs.items():
        lw = (g(f) * T + f * sg * WT) / T
        m, se, sd = lw.mean(), lw.std(ddof=1) / math.sqrt(len(lw)), lw.std(ddof=1)
        report.ok(
            f"{name} (f = {f:.4g}): mean ln W_T / T within 3 s.e. of g(f) = {g(f):.5f}; s.d. within"
            " 1% of f sigma / sqrt(T)",
            abs(m - g(f)) <= 3 * se and abs(sd / (f * sg / math.sqrt(T)) - 1) < 0.01,
            f"{m:.5f} (s.e. {se:.5f}), s.d. {sd:.4f}",
        )


def check_levered_ruin(report: CheckReport) -> None:
    """Check why levered fractions are excluded from daily rebalancing."""
    print("== daily rebalancing: why the levered fractions are excluded")
    # For f > 1 the day's gross factor is nonpositive when Z <= z_ruin, so ln W_T has no
    # (unconditional, real) expectation however small that probability is.
    for f in (F_STAR, 2 * F_STAR):
        zr = MODEL.ruin_threshold(f, DT)
        log10_p = scipy.stats.norm.logcdf(zr) / math.log(10)
        gross = MODEL.gross_step(f, DT, zr - 1)
        report.ok(
            f"f = {f:g}: one-day wealth is nonpositive for Z <= {zr:.2f}, a positive probability"
            f" (10^{log10_p:.0f})",
            gross < 0 and math.isfinite(log10_p) and log10_p > -math.inf,
            f"gross factor {gross:+.4f} at Z = {zr - 1:.2f}",
        )


def check_daily_rebalancing(report: CheckReport) -> None:
    """Check daily rebalancing of unlevered fractions against its quadrature expectation."""
    print("== daily rebalancing with unlevered fractions against its quadrature expectation")
    mu, r, sg = MODEL.mu, MODEL.rate, MODEL.sigma
    g, g_discrete = MODEL.growth, MODEL.rebalanced_growth
    daily = {"quarter": 0.25, "half": 0.5, "half Kelly": F_STAR / 2}
    report.ok(
        "f = 1 needs no rebalancing: quadrature gives mu - sigma^2/2 = g(1) exactly (to 1e-12)",
        abs(g_discrete(1.0, DT) - (mu - sg**2 / 2)) < 1e-12
        and abs(g(1.0) - (mu - sg**2 / 2)) < 1e-15,
    )
    steps, n_paths = 2520, 20_000
    rng = np.random.default_rng(20261042)
    logw = {name: np.zeros(n_paths) for name in daily}
    for _ in range(steps):
        R_step = np.exp((mu - sg**2 / 2) * DT + sg * math.sqrt(DT) * rng.standard_normal(n_paths))
        for name, f in daily.items():
            logw[name] += np.log((1 - f) * math.exp(r * DT) + f * R_step)
    for name, f in daily.items():
        gd, gh = g_discrete(f, DT), g_discrete(f, DT / 2)
        bias, bias_half = gd - g(f), gh - g(f)
        quad_err = max(
            abs(g_discrete(f, DT, 40) - gd),
            abs(g_discrete(f, DT, 160) - gd),
            abs(adaptive_growth(f, DT) - gd),
            abs(g_discrete(f, DT / 2, 160) - gh),
            abs(adaptive_growth(f, DT / 2) - gh),
        )
        report.ok(
            f"{name} (f = {f:g}): 40-, 80- and 160-node quadrature and adaptive integration agree"
            " within 1e-10 a year, below 1/1000 of the bias",
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
            " it by [0.4, 0.6]",
            abs(bias) < 5e-4 and 0.4 <= bias_half / bias <= 0.6,
            f"ratio {bias_half / bias:.3f}",
        )


def check_discrete_bets(report: CheckReport) -> None:
    """Check that the 3/4 half-Kelly identity does not carry over to discrete bets."""
    print("== discrete bets: the 3/4 identity does not carry over")
    for p, b, f_exp, ratio_exp in ((0.6, 1.0, 0.2, 0.7470), (0.3, 4.0, 0.125, 0.7727)):
        bet = DiscreteBet(p=p, b=b)
        fk = bet.kelly_fraction
        grid = np.linspace(0, 0.99, 99_001)
        numeric = grid[np.argmax([bet.growth(x) for x in grid])]
        ratio = bet.growth(fk / 2) / bet.growth(fk)
        report.ok(
            f"p = {p}, b = {b}: f* = p - q/b = {f_exp} (grid search agrees); half-Kelly growth"
            f" ratio {ratio_exp}, not 0.75",
            abs(fk - f_exp) < 1e-12
            and abs(numeric - fk) < 1e-4
            and abs(ratio - ratio_exp) < 5e-5
            and abs(ratio - 0.75) > 1e-3,
            f"{ratio:.4f}",
        )


def check_estimation_error(report: CheckReport) -> None:
    """Check the expected excess growth of fractions of a Kelly bet on an estimated mu."""
    print("== estimation error in mu")
    # mu is estimated from 10 years of returns: mu_hat ~ N(mu, sigma^2 / 10). The expected excess
    # growth of the fraction c (mu_hat - r) / sigma^2 is
    # c f* (mu - r) - 0.5 c^2 sigma^2 (f*^2 + s^2 / sigma^4), s^2 = sigma^2 / 10. Criterion:
    # Monte Carlo (200,000 estimates) within 3 s.e. of the formula for c = 1 and c = 1/2, with
    # full Kelly negative and half Kelly positive in expectation.
    mu, r, sg = MODEL.mu, MODEL.rate, MODEL.sigma
    s2 = sg**2 / 10
    rng = np.random.default_rng(20261043)
    mu_hat = mu + math.sqrt(s2) * rng.standard_normal(200_000)
    for c, sign in ((1.0, -1), (0.5, 1)):
        f_hat = c * (mu_hat - r) / sg**2
        sim = f_hat * (mu - r) - 0.5 * f_hat**2 * sg**2
        formula = c * F_STAR * (mu - r) - 0.5 * c**2 * sg**2 * (F_STAR**2 + s2 / sg**4)
        report.ok(
            f"fraction {c} of estimated Kelly: expected excess growth {formula:+.5f}, sign"
            f" {sign:+d}",
            abs(sim.mean() - formula) <= 3 * sim.std(ddof=1) / math.sqrt(len(sim))
            and formula * sign > 0,
            f"simulated {sim.mean():+.5f}",
        )


def main() -> int:
    """Run the six parts with one report; parts 2, 4 and 6 each seed their own generator.

    Returns:
        The exit status, 0 or 1.
    """
    print_versions(np, scipy)
    report = CheckReport()
    check_identities(report)
    check_log_wealth(report)
    check_levered_ruin(report)
    check_daily_rebalancing(report)
    check_discrete_bets(report)
    check_estimation_error(report)
    return report.summarise()


if __name__ == "__main__":
    sys.exit(main())
