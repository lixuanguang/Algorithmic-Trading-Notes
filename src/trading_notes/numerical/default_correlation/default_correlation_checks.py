"""Gaussian copula default correlation: tranche losses, base and compound correlations."""

import itertools
import math
import sys
from typing import Final

import numpy as np
import scipy
from scipy import integrate, optimize, stats

from trading_notes.numerical.default_correlation.factor_model import (
    VasicekFactorModel,
    irb_corporate,
)
from trading_notes.numerical.default_correlation.tranche_pricing import (
    HomogeneousPool,
    SyntheticCdoTranche,
    tranche_payoff,
)
from trading_notes.numerical.report import CheckReport

G: Final = stats.norm.ppf
POOL: Final = HomogeneousPool(pd=0.02, rho=0.3, lgd=0.6)
PTS: Final = (0, 0.03, 0.07, 0.10, 0.15, 0.30, 1.0)  # tranche boundaries, as fractions of the pool
SEED: Final = 20261081
ITRAXX_3_6: Final = SyntheticCdoTranche(
    attach=0.03,
    detach=0.06,
    names=125,
    recovery=0.4,
    rho=0.15,
    hazard=0.0083,
    rate=0.035,
    maturity=5,
    frequency=4,
)


def tranches_of(points: tuple[float, ...]) -> list[tuple[float, float]]:
    """Return the tranches between consecutive boundaries of points."""
    return list(itertools.pairwise(points))


def cdf_tri(v: float, peak: float) -> float:
    """Triangular density on [0, 1] with height 2 at the peak (RMFI Figure 9.2)."""
    return v * v / peak if v <= peak else 1 - (1 - v) ** 2 / (1 - peak)


def biv(u1: float, u2: float) -> float:
    """Bivariate normal cdf with correlation 0.5 at (u1, u2)."""
    return stats.multivariate_normal(mean=[0, 0], cov=[[1, 0.5], [0.5, 1]]).cdf([u1, u2])


def market_el(a: float, d: float) -> float:
    """Return the expected tranche loss of the equal mixture of correlations 0.1 and 0.6."""
    return 0.5 * (
        POOL.model_copy(update={"rho": 0.1}).large_pool_loss(a, d)
        + POOL.model_copy(update={"rho": 0.6}).large_pool_loss(a, d)
    )


def base_el(d: float, rho: float) -> float:
    """Expected loss of the base-correlation tranche 0-d at correlation rho."""
    return POOL.model_copy(update={"rho": rho}).large_pool_loss(0.0, d)


def check_published(report: CheckReport) -> None:
    """Part 1: published examples of the Gaussian copula, the CDO tranche and the IRB formula.

    Args:
        report: The run's report.
    """
    print("== Part 1: published examples")
    p_one = 1 - 0.98**100
    p_ten = stats.binom.sf(9, 100, 0.02)
    report.ok(
        "Hull sec. 25.9: 100 names, 2% each, independent: P(>=1 default) 86.74%, P(>=10) 0.0034%",
        abs(100 * p_one - 86.74) < 5e-3 and abs(100 * p_ten - 0.0034) < 5e-5,
        f"{100 * p_one:.4f}%, {100 * p_ten:.5f}%",
    )
    A, B, C = ITRAXX_3_6.legs(60)
    s = C / (A + B)
    report.ok(
        "Hull Example 25.2: A = 4.2846, B = 0.0187, C = 0.1496, breakeven 348 bp",
        abs(A - 4.2846) < 5e-4
        and abs(B - 0.0187) < 5e-4
        and abs(C - 0.1496) < 5e-4
        and round(1e4 * s) == 348,
        f"A {A:.4f}, B {B:.4f}, C {C:.4f}, spread {1e4 * s:.1f} bp",
    )
    cells = {
        (0.1, 0.1): 0.006,
        (0.5, 0.5): 0.417,
        (0.9, 0.9): 0.970,
        (0.3, 0.7): 0.364,
        (0.8, 0.2): 0.080,
    }
    got = {c: biv(G(cdf_tri(c[0], 0.2)), G(cdf_tri(c[1], 0.5))) for c in cells}
    report.ok(
        "RMFI Table 9.5 (Gaussian copula, correlation 0.5): five cells reproduced to 3 decimals",
        all(abs(got[c] - v) < 5e-4 for c, v in cells.items()),
        ", ".join(f"{got[c]:.4f}" for c in cells),
    )
    wcdr = VasicekFactorModel(pd=0.02, rho=0.1).worst_case_default_rate(0.999)
    report.ok(
        "RMFI Example 9.2: WCDR(1, 0.999) at PD 2%, rho 0.1 is 0.128",
        abs(wcdr - 0.128) < 5e-4,
        f"{wcdr:.5f}",
    )
    cre99 = {
        0.0005: 17.47,
        0.001: 26.36,
        0.0025: 43.97,
        0.004: 55.75,
        0.005: 61.88,
        0.0075: 73.58,
        0.01: 82.06,
        0.013: 89.73,
        0.015: 93.86,
        0.02: 102.09,
    }
    gaps = {pd: abs(100 * irb_corporate(pd, 0.40).risk_weight - rw) for pd, rw in cre99.items()}
    report.ok(
        "CRE31.5 reproduces CRE99 Table 1 corporate risk weights (LGD 40%, M 2.5, turnover 50) to"
        " 0.005 points",
        max(gaps.values()) < 5e-3,
        f"largest gap {max(gaps.values()):.4f}; 1% PD gives"
        f" {100 * irb_corporate(0.01, 0.40).risk_weight:.2f}%",
    )
    for pd in (0.01, 0.02):
        irb = irb_corporate(pd, 0.45)
        R, cond = irb.correlation, irb.conditional_pd
        wc = VasicekFactorModel(pd=pd, rho=R).worst_case_default_rate(0.999)
        report.ok(
            f"the conditional default rate inside the IRB formula equals RMFI's WCDR at PD {pd:.0%}"
            f" (R = {R:.4f}) to 1e-12",
            abs(cond - wc) < 1e-12,
            f"{cond:.6f}; K {irb.capital:.5f}, risk weight {100 * irb.risk_weight:.2f}% at LGD 45%",
        )


def check_tranches(report: CheckReport) -> None:
    """Part 2: tranche expected losses by large pool, exact finite pool and Monte Carlo.

    Args:
        report: The run's report.
    """
    print("== Part 2: tranche expected losses (PD 2%, rho 0.3, LGD 60%)")
    pts = PTS
    tranches = tranches_of(pts)
    lp = [POOL.large_pool_loss(a, d) for a, d in tranches]
    report.ok(
        "large-pool tranche expected losses sum to the pool's PD x LGD = 0.012 to 1e-12",
        abs(sum(lp) - POOL.pd * POOL.lgd) < 1e-12,
        f"{sum(lp):.15f}",
    )
    exact: dict[int, list[tuple[float, int, float]]] = {}
    for n in (250, 500, 1000):
        exact[n] = [POOL.finite_pool_loss_converged(n, a, d) for a, d in tranches]
    conv = all(e[2] < 1e-10 for n in exact for e in exact[n])
    report.ok(
        "exact finite-pool values converge: doubling the Gauss-Legendre panels changes each by <"
        " 1e-10",
        conv,
        "nodes used up to " + str(max(e[1] for n in exact for e in exact[n])),
    )
    report.ok(
        "exact finite-pool tranche losses (1,000 names) also sum to PD x LGD to 1e-10",
        abs(sum(e[0] for e in exact[1000]) - POOL.pd * POOL.lgd) < 1e-10,
    )

    model = VasicekFactorModel(pd=POOL.pd, rho=POOL.rho)

    def integrand(m: float) -> float:
        return float(
            stats.binom.pmf(np.arange(1001), 1000, model.conditional_pd(m))
            @ tranche_payoff(POOL.lgd * np.arange(1001) / 1000, 0.03, 0.07)
        ) * stats.norm.pdf(m)

    qcheck = integrate.quad(integrand, -12, 12, epsabs=1e-13, limit=500)[0]
    print(
        f"  cross-check by adaptive quadrature, 3-7% tranche, 1,000 names: {qcheck:.12f} against"
        f" {exact[1000][1][0]:.12f}"
    )

    rng = np.random.default_rng(SEED)
    n_names, n_scen = 1000, 50_000
    pd, rho, lgd = POOL.pd, POOL.rho, POOL.lgd
    cth = G(pd)
    losses = np.empty(n_scen)
    for lo in range(0, n_scen, 2_000):
        m = rng.standard_normal(2_000)
        z = rng.standard_normal((2_000, n_names))
        defaults = (math.sqrt(rho) * m[:, None] + math.sqrt(1 - rho) * z < cth).sum(axis=1)
        losses[lo : lo + 2_000] = lgd * defaults / n_names
    print("  tranche      large pool      exact N=1,000   Monte Carlo (s.e.)        z")
    for (a, d), l_large, e in zip(tranches, lp, exact[1000], strict=True):
        tl = tranche_payoff(losses, a, d)
        mc, se = float(tl.mean()), float(tl.std(ddof=1) / math.sqrt(n_scen))
        zscore = (mc - e[0]) / se if se > 0 else 0.0
        print(
            f"  {100 * a:4.0f}-{100 * d:<4.0f}%  {l_large:.8f}    {e[0]:.8f}      {mc:.8f}"
            f" ({se:.8f})  {zscore:+.2f}"
        )
        report.ok(
            f"Monte Carlo (1,000 names, 50,000 scenarios) within 3 s.e. of the exact value,"
            f" {100 * a:.0f}-{100 * d:.0f}%",
            abs(mc - e[0]) <= 3 * se or (se == 0 and abs(mc - e[0]) < 1e-9),
        )
    print("  reported (not tested): exact finite pool minus large pool, units of pool notional")
    for j, (a, d) in enumerate(tranches):
        g = [exact[n][j][0] - lp[j] for n in (250, 500, 1000)]
        print(
            f"    {100 * a:4.0f}-{100 * d:<4.0f}%  N=250 {g[0]:+.3e}  N=500 {g[1]:+.3e}"
            f"  N=1,000 {g[2]:+.3e}"
        )


def check_base_correlation(report: CheckReport) -> None:
    """Part 3: compound and base correlation against a synthetic two-correlation market.

    Args:
        report: The run's report.
    """
    print("== Part 3: compound and base correlation against a synthetic two-correlation 'market'")
    pts = PTS
    tranches = tranches_of(pts)
    base: dict[float, float] = {}
    for d in pts[1:-1]:
        target = market_el(0.0, d)

        def gap_at(r: float, d: float = d, target: float = target) -> float:
            return base_el(d, r) - target

        base[d] = optimize.brentq(gap_at, 1e-4, 0.999, xtol=1e-14)
    recon = max(abs(base_el(d, base[d]) - market_el(0.0, d)) for d in base)
    report.ok(
        "each base correlation reprices its 0-d tranche's expected loss to 1e-10",
        recon < 1e-10,
        f"{recon:.1e}",
    )
    diff_ok = all(
        abs((base_el(d, base[d]) - (base_el(a, base[a]) if a > 0 else 0.0)) - market_el(a, d))
        < 1e-10
        for a, d in tranches[:-1]
    )
    report.ok(
        "differences of base-correlation 0-d losses reproduce every tranche's market loss to 1e-10",
        diff_ok,
    )
    print(
        "  base correlations (0-3, 0-7, 0-10, 0-15, 0-30): "
        + ", ".join(f"{base[d]:.4f}" for d in pts[1:-1])
    )
    grid = np.linspace(0.005, 0.995, 199)
    for a, d in tranches[:-1]:
        f = np.array(
            [POOL.model_copy(update={"rho": r}).large_pool_loss(a, d) for r in grid]
        ) - market_el(a, d)
        roots = int(np.sum(np.sign(f[:-1]) != np.sign(f[1:])))
        print(
            f"  compound correlation for {100 * a:.0f}-{100 * d:.0f}%: {roots} solution(s) on (0,"
            " 1)"
        )

    # a non-standard 4-8% tranche: interpolate base correlations linearly in detachment, against the
    # market value
    def ib(x: float) -> float:
        return float(np.interp(x, pts[1:-1], [base[d] for d in pts[1:-1]]))

    via_base = base_el(0.08, ib(0.08)) - base_el(0.04, ib(0.04))
    true_48 = market_el(0.04, 0.08)

    def el_curve(x: float) -> float:
        return float(np.interp(x, pts[1:-1], [market_el(0.0, d) for d in pts[1:-1]]))

    via_el = el_curve(0.08) - el_curve(0.04)
    print(
        f"  4-8% tranche: market {true_48:.6f}; interpolated base correlation {via_base:.6f};"
        f" interpolated 0-x expected loss {via_el:.6f}"
    )
    thin = [
        base_el(x + 0.0025, ib(x + 0.0025)) - base_el(x, ib(x))
        for x in np.arange(0.005, 0.29, 0.0025)
    ]
    neg = sum(1 for v in thin if v < 0)
    ups = [(b2 - b1) for b1, b2 in itertools.pairwise(thin) if b2 > b1 + 1e-15]
    mono = not ups
    print(
        f"  0.25%-wide tranches priced from interpolated base correlations: {neg} negative expected"
        " losses; expected loss per unit width non-increasing in x (no-arbitrage concavity):"
        f" {mono}" + (f" ({len(ups)} increases, largest {max(ups):.2e})" if ups else "")
    )


def main() -> int:
    """Print the versions, then run the three parts with one report.

    Worked examples of mod:gaussian-copula-default-correlation and
    meth:tranche-loss-base-correlation.

    Part 1 reproduces published numbers: Hull, Options, Futures, and Other Derivatives, 11th Global
    ed., sec. 25.9 (the binomial basket probabilities) and Example 25.2 (iTraxx 3-6% tranche, 348
    bp); Hull, Risk Management and Financial Institutions, 6th ed., Table 9.5 (Gaussian copula of
    two triangular marginals) and Example 9.2 (WCDR 12.8%); and the Basel IRB corporate risk weights
    of CRE99 Table 1 from the CRE31.5 formula (Basel Framework, CRE31 and CRE99 versions in force
    from 1 January 2023).

    Part 2 is synthetic, one period: a homogeneous pool with PD = 2 percent to the horizon, copula
    correlation 0.3, LGD 60 percent, and the tranches 0-3, 3-7, 7-10, 10-15, 15-30 and 30-100
    percent of pool notional. Expected tranche losses are measured in units of pool notional and are
    not discounted. The large-pool value integrates the tranche payoff of LGD p(M) over the factor;
    the exact finite pool integrates the conditional binomial(N, p(M)) sum on composite
    Gauss-Legendre panels doubled until the value changes by less than 1e-10. The Monte Carlo draws
    each name's latent variable (1,000 names, 50,000 scenarios, seed 20261081). The
    finite-versus-large-pool gaps at 250, 500 and 1,000 names are reported, not tested.

    Part 3 builds a synthetic "market" from an equal mixture of Gaussian copulas with correlations
    0.1 and 0.6 and reads off compound and base correlations; it draws nothing. The
    base-correlation solves take nearly all of the run's thirty seconds.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
    report = CheckReport()
    check_published(report)
    check_tranches(report)
    check_base_correlation(report)
    if report.failures:
        print("FAILED:", ", ".join(report.failures))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
