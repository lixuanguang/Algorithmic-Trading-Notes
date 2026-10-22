"""Library gap-filling Batch L2, package P8 (2026-10-21): the worked examples of
mod:gaussian-copula-default-correlation and meth:tranche-loss-base-correlation.

Part 1 reproduces published numbers: Hull, Options, Futures, and Other Derivatives, 11th Global ed., sec. 25.9 (the
binomial basket probabilities) and Example 25.2 (iTraxx 3-6% tranche, 348 bp); Hull, Risk Management and Financial
Institutions, 6th ed., Table 9.5 (Gaussian copula of two triangular marginals) and Example 9.2 (WCDR 12.8%); and the
Basel IRB corporate risk weights of CRE99 Table 1 from the CRE31.5 formula (Basel Framework, CRE31 and CRE99 versions
in force from 1 January 2023, retrieved 2026-10-21).

Part 2 is synthetic, one period: a homogeneous pool with PD = 2 percent to the horizon, copula correlation 0.3, LGD
60 percent, and the tranches 0-3, 3-7, 7-10, 10-15, 15-30 and 30-100 percent of pool notional. Expected tranche losses
are measured in units of pool notional and are not discounted. The large-pool value integrates the tranche payoff of
LGD p(M) over the factor; the exact finite pool integrates the conditional binomial(N, p(M)) sum, with Gauss-Hermite
composite Gauss-Legendre panels doubled until the value changes by less than 1e-10. The Monte Carlo draws each name's latent variable (1,000
names, 50,000 scenarios, seed 20261081, fixed before the first run). Part 3 builds a synthetic "market" from an equal
mixture of Gaussian copulas with correlations 0.1 and 0.6 and reads off compound and base correlations.

Criteria were fixed before the first run. The finite-versus-large-pool gaps at 250, 500 and 1,000 names
are reported, not tested, following the correction made before implementation.

Run: uv run python default-correlation-checks.py   (numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import itertools
import math
import sys

# third party library imports
import numpy as np
import scipy
from scipy import integrate, optimize, stats

print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
fails = []
N, G = stats.norm.cdf, stats.norm.ppf


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


def gh(n):
    """Gauss-Hermite nodes and weights for E[g(M)], M standard normal."""
    x, w = np.polynomial.hermite_e.hermegauss(n)
    return x, w / math.sqrt(2 * math.pi)


def cond_pd(pd, rho, m):
    """Hull eq. (24.9) / RMFI eq. (9.13): default probability conditional on the factor."""
    return N((G(pd) - math.sqrt(rho) * m) / math.sqrt(1 - rho))


print("== Part 1: published examples")
p_one = 1 - 0.98**100
p_ten = stats.binom.sf(9, 100, 0.02)
ok(
    "Hull sec. 25.9: 100 names, 2% each, independent: P(>=1 default) 86.74%, P(>=10) 0.0034%",
    abs(100 * p_one - 86.74) < 5e-3 and abs(100 * p_ten - 0.0034) < 5e-5,
    f"{100 * p_one:.4f}%, {100 * p_ten:.5f}%",
)


def cdo_tranche(aL, aH, n, R, rho, lam, r, T, freq, M):
    """Hull eqs. (25.1)-(25.12): A, B, C for a synthetic CDO tranche, principal 1, Gauss-Hermite with M points."""
    x, w = gh(M)
    t = np.arange(1, T * freq + 1) / freq
    t0 = np.concatenate(([0.0], t))
    nL, nH = aL * n / (1 - R), aH * n / (1 - R)
    mL, mH = math.floor(nL) + 1, math.floor(nH) + 1  # smallest integer greater than x
    k = np.arange(n + 1)
    principal = np.where(k < mL, 1.0, np.where(k >= mH, 0.0, (aH - k * (1 - R) / n) / (aH - aL)))
    A = B = C = 0.0
    for f, wk in zip(x, w, strict=True):
        q = 1 - np.exp(-lam * t0)
        qf = N((G(np.maximum(q, 1e-300)) - math.sqrt(rho) * f) / math.sqrt(1 - rho))
        qf[0] = 0.0
        E = np.array([stats.binom.pmf(k, n, p) @ principal for p in qf])
        mid = 0.5 * (t0[:-1] + t0[1:])
        A += wk * np.sum(np.diff(t0) * E[1:] * np.exp(-r * t))
        B += wk * np.sum(0.5 * np.diff(t0) * (E[:-1] - E[1:]) * np.exp(-r * mid))
        C += wk * np.sum((E[:-1] - E[1:]) * np.exp(-r * mid))
    return A, B, C


A, B, C = cdo_tranche(0.03, 0.06, 125, 0.4, 0.15, 0.0083, 0.035, 5, 4, 60)
s = C / (A + B)
ok(
    "Hull Example 25.2: A = 4.2846, B = 0.0187, C = 0.1496, breakeven 348 bp",
    abs(A - 4.2846) < 5e-4
    and abs(B - 0.0187) < 5e-4
    and abs(C - 0.1496) < 5e-4
    and round(1e4 * s) == 348,
    f"A {A:.4f}, B {B:.4f}, C {C:.4f}, spread {1e4 * s:.1f} bp",
)


def cdf_tri(v, peak):
    """Triangular density on [0, 1] with height 2 at the peak (RMFI Figure 9.2)."""
    return v * v / peak if v <= peak else 1 - (1 - v) ** 2 / (1 - peak)


biv = lambda u1, u2: stats.multivariate_normal(mean=[0, 0], cov=[[1, 0.5], [0.5, 1]]).cdf([u1, u2])
cells = {
    (0.1, 0.1): 0.006,
    (0.5, 0.5): 0.417,
    (0.9, 0.9): 0.970,
    (0.3, 0.7): 0.364,
    (0.8, 0.2): 0.080,
}
got = {c: biv(G(cdf_tri(c[0], 0.2)), G(cdf_tri(c[1], 0.5))) for c in cells}
ok(
    "RMFI Table 9.5 (Gaussian copula, correlation 0.5): five cells reproduced to 3 decimals",
    all(abs(got[c] - v) < 5e-4 for c, v in cells.items()),
    ", ".join(f"{got[c]:.4f}" for c in cells),
)
wcdr = N((G(0.02) + math.sqrt(0.1) * G(0.999)) / math.sqrt(1 - 0.1))
ok(
    "RMFI Example 9.2: WCDR(1, 0.999) at PD 2%, rho 0.1 is 0.128",
    abs(wcdr - 0.128) < 5e-4,
    f"{wcdr:.5f}",
)


def irb_corporate(pd, lgd, m=2.5):
    """CRE31.5: correlation R, maturity adjustment b, capital K and risk weight 12.5 K (no SME adjustment)."""
    w = (1 - math.exp(-50 * pd)) / (1 - math.exp(-50))
    R = 0.12 * w + 0.24 * (1 - w)
    b = (0.11852 - 0.05478 * math.log(pd)) ** 2
    cond = N(G(pd) / math.sqrt(1 - R) + math.sqrt(R / (1 - R)) * G(0.999))
    K = (lgd * cond - pd * lgd) * (1 + (m - 2.5) * b) / (1 - 1.5 * b)
    return R, b, cond, K, 12.5 * K


cre99 = {
    0.0005: 17.47, 0.001: 26.36, 0.0025: 43.97, 0.004: 55.75, 0.005: 61.88,
    0.0075: 73.58, 0.01: 82.06, 0.013: 89.73, 0.015: 93.86, 0.02: 102.09,
}  # fmt: skip
gaps = {pd: abs(100 * irb_corporate(pd, 0.40)[4] - rw) for pd, rw in cre99.items()}
ok(
    "CRE31.5 reproduces CRE99 Table 1 corporate risk weights (LGD 40%, M 2.5, turnover 50) to 0.005 points",
    max(gaps.values()) < 5e-3,
    f"largest gap {max(gaps.values()):.4f}; 1% PD gives {100 * irb_corporate(0.01, 0.40)[4]:.2f}%",
)
for pd, rho_test in ((0.01, None), (0.02, None)):
    R, b, cond, K, rw = irb_corporate(pd, 0.45)
    wc = N((G(pd) + math.sqrt(R) * G(0.999)) / math.sqrt(1 - R))
    ok(
        f"the conditional default rate inside the IRB formula equals RMFI's WCDR at PD {pd:.0%} (R = {R:.4f}) to 1e-12",
        abs(cond - wc) < 1e-12,
        f"{cond:.6f}; K {K:.5f}, risk weight {100 * rw:.2f}% at LGD 45%",
    )

print("== Part 2: tranche expected losses (PD 2%, rho 0.3, LGD 60%)")
PD, RHO, LGD = 0.02, 0.3, 0.6
pts = [0, 0.03, 0.07, 0.10, 0.15, 0.30, 1.0]
tranches = list(itertools.pairwise(pts))


def payoff(L, a, d):
    return np.clip(L, a, d) - a


def large_pool(a, d, rho=RHO, pd=PD):
    """E[min(max(LGD p(M) - a, 0), d - a)], splitting the factor line where the loss crosses a and d."""
    cuts = []
    for x in (a, d):
        if 0 < x / LGD < 1:
            cuts.append((G(pd) - math.sqrt(1 - rho) * G(x / LGD)) / math.sqrt(rho))
    edges = sorted([-40.0, 40.0, *cuts])
    f = lambda m: float(payoff(LGD * cond_pd(pd, rho, m), a, d)) * stats.norm.pdf(m)
    return sum(
        integrate.quad(f, lo, hi, epsabs=1e-15, epsrel=1e-13, limit=400)[0]
        for lo, hi in itertools.pairwise(edges)
    )


lp = [large_pool(a, d) for a, d in tranches]
ok(
    "large-pool tranche expected losses sum to the pool's PD x LGD = 0.012 to 1e-12",
    abs(sum(lp) - PD * LGD) < 1e-12,
    f"{sum(lp):.15f}",
)


def legendre_nodes(panels, per=20, lo=-10.0, hi=10.0):
    """Composite Gauss-Legendre nodes and weights for E[g(M)] on [lo, hi] (tails beyond +-10 below 1e-22)."""
    x, w = np.polynomial.legendre.leggauss(per)
    edges = np.linspace(lo, hi, panels + 1)
    h = np.diff(edges) / 2
    xs = (edges[:-1, None] + h[:, None] * (x[None, :] + 1)).ravel()
    ws = (h[:, None] * w[None, :]).ravel() * stats.norm.pdf(xs)
    return xs, ws


def finite_pool(n, a, d, panels):
    x, w = legendre_nodes(panels)
    k = np.arange(n + 1)
    pay = payoff(LGD * k / n, a, d)
    pmf = stats.binom.pmf(k[None, :], n, cond_pd(PD, RHO, x)[:, None])
    return float(w @ (pmf @ pay))


def finite_pool_converged(n, a, d):
    panels, prev = 16, finite_pool(n, a, d, 16)
    while True:
        panels *= 2
        cur = finite_pool(n, a, d, panels)
        if abs(cur - prev) < 1e-10 or panels >= 1024:
            return cur, panels * 20, abs(cur - prev)
        prev = cur


exact = {}
for n in (250, 500, 1000):
    exact[n] = [finite_pool_converged(n, a, d) for a, d in tranches]
conv = all(e[2] < 1e-10 for n in exact for e in exact[n])
ok(
    "exact finite-pool values converge: doubling the Gauss-Legendre panels changes each by < 1e-10",
    conv,
    "nodes used up to " + str(max(e[1] for n in exact for e in exact[n])),
)
ok(
    "exact finite-pool tranche losses (1,000 names) also sum to PD x LGD to 1e-10",
    abs(sum(e[0] for e in exact[1000]) - PD * LGD) < 1e-10,
)
qcheck = integrate.quad(
    lambda m: (
        float(
            stats.binom.pmf(np.arange(1001), 1000, cond_pd(PD, RHO, m))
            @ payoff(LGD * np.arange(1001) / 1000, 0.03, 0.07)
        )
        * stats.norm.pdf(m)
    ),
    -12,
    12,
    epsabs=1e-13,
    limit=500,
)[0]
print(
    f"  cross-check by adaptive quadrature, 3-7% tranche, 1,000 names: {qcheck:.12f} against {exact[1000][1][0]:.12f}"
)

rng = np.random.default_rng(20261081)
n_names, n_scen = 1000, 50_000
cth = G(PD)
losses = np.empty(n_scen)
for lo in range(0, n_scen, 2_000):
    m = rng.standard_normal(2_000)
    z = rng.standard_normal((2_000, n_names))
    defaults = (math.sqrt(RHO) * m[:, None] + math.sqrt(1 - RHO) * z < cth).sum(axis=1)
    losses[lo : lo + 2_000] = LGD * defaults / n_names
print("  tranche      large pool      exact N=1,000   Monte Carlo (s.e.)        z")
for (a, d), l_large, e in zip(tranches, lp, exact[1000], strict=True):
    tl = payoff(losses, a, d)
    mc, se = float(tl.mean()), float(tl.std(ddof=1) / math.sqrt(n_scen))
    z = (mc - e[0]) / se if se > 0 else 0.0
    print(
        f"  {100 * a:4.0f}-{100 * d:<4.0f}%  {l_large:.8f}    {e[0]:.8f}      {mc:.8f} ({se:.8f})  {z:+.2f}"
    )
    ok(
        f"Monte Carlo (1,000 names, 50,000 scenarios) within 3 s.e. of the exact value, {100 * a:.0f}-{100 * d:.0f}%",
        abs(mc - e[0]) <= 3 * se or (se == 0 and abs(mc - e[0]) < 1e-9),
    )
print("  reported (not tested): exact finite pool minus large pool, units of pool notional")
for j, (a, d) in enumerate(tranches):
    g = [exact[n][j][0] - lp[j] for n in (250, 500, 1000)]
    print(
        f"    {100 * a:4.0f}-{100 * d:<4.0f}%  N=250 {g[0]:+.3e}  N=500 {g[1]:+.3e}  N=1,000 {g[2]:+.3e}"
    )

print("== Part 3: compound and base correlation against a synthetic two-correlation 'market'")


def market_el(a, d):
    return 0.5 * (large_pool(a, d, rho=0.1) + large_pool(a, d, rho=0.6))


def base_el(d, rho):
    return large_pool(0.0, d, rho=rho)


base = {}
for d in pts[1:-1]:
    target = market_el(0.0, d)
    base[d] = optimize.brentq(lambda r, d=d, t=target: base_el(d, r) - t, 1e-4, 0.999, xtol=1e-14)
recon = max(abs(base_el(d, base[d]) - market_el(0.0, d)) for d in base)
ok(
    "each base correlation reprices its 0-d tranche's expected loss to 1e-10",
    recon < 1e-10,
    f"{recon:.1e}",
)
diff_ok = all(
    abs((base_el(d, base[d]) - (base_el(a, base[a]) if a > 0 else 0.0)) - market_el(a, d)) < 1e-10
    for a, d in tranches[:-1]
)
ok(
    "differences of base-correlation 0-d losses reproduce every tranche's market loss to 1e-10",
    diff_ok,
)
print(
    "  base correlations (0-3, 0-7, 0-10, 0-15, 0-30): "
    + ", ".join(f"{base[d]:.4f}" for d in pts[1:-1])
)
grid = np.linspace(0.005, 0.995, 199)
for a, d in tranches[:-1]:
    f = np.array([large_pool(a, d, rho=r) for r in grid]) - market_el(a, d)
    roots = int(np.sum(np.sign(f[:-1]) != np.sign(f[1:])))
    print(f"  compound correlation for {100 * a:.0f}-{100 * d:.0f}%: {roots} solution(s) on (0, 1)")
# a non-standard 4-8% tranche: interpolate base correlations linearly in detachment, against the market value
ib = lambda x: float(np.interp(x, pts[1:-1], [base[d] for d in pts[1:-1]]))
via_base = base_el(0.08, ib(0.08)) - base_el(0.04, ib(0.04))
true_48 = market_el(0.04, 0.08)
el_curve = lambda x: float(np.interp(x, pts[1:-1], [market_el(0.0, d) for d in pts[1:-1]]))
via_el = el_curve(0.08) - el_curve(0.04)
print(
    f"  4-8% tranche: market {true_48:.6f}; interpolated base correlation {via_base:.6f};"
    f" interpolated 0-x expected loss {via_el:.6f}"
)
thin = [
    base_el(x + 0.0025, ib(x + 0.0025)) - base_el(x, ib(x)) for x in np.arange(0.005, 0.29, 0.0025)
]
neg = sum(1 for v in thin if v < 0)
ups = [(b2 - b1) for b1, b2 in itertools.pairwise(thin) if b2 > b1 + 1e-15]
mono = not ups
print(
    f"  0.25%-wide tranches priced from interpolated base correlations: {neg} negative expected losses;"
    f" expected loss per unit width non-increasing in x (no-arbitrage concavity): {mono}"
    + (f" ({len(ups)} increases, largest {max(ups):.2e})" if ups else "")
)

if fails:
    print("FAILED:", ", ".join(fails))
    sys.exit(1)
print("all checks passed")
