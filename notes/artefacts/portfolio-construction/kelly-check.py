"""Library gap-filling Batch L1, package P5 (2026-10-21): the worked examples of res:kelly-growth-optimal-fraction.

Continuous model: constant mu = 8 percent, r = 2 percent, sigma = 20 percent, a constant fraction f of wealth
in the risky asset and the rest in cash, no costs or leverage limits. Acceptance (implementation_plan_v2.md
Section 6, P5, as corrected before any run):
  - the continuous identity is tested with its matching model, exact continuous-time log-wealth sampling
    (200,000 draws over 10 years, seed 20261041);
  - daily rebalancing is tested separately against its expectation, computed by 80-point Gauss-Hermite
    quadrature (20,000 paths x 2,520 steps, seed 20261042), with the discretisation bias below 5e-4 a year and a
    first-order refinement ratio in [0.4, 0.6];
  - discrete bets show that the 3/4 half-Kelly identity is a property of the continuous model only.
The estimation-error illustration (seed 20261043) uses a stated criterion of its own. Synthetic data only.

Correction, 2026-10-21 (L1 audit finding L1-F1): the first version ran the daily-rebalancing checks at f = 0.75,
1.5 and 3 and called the quadrature value an exact expectation. For f > 1 the one-day gross factor
(1 - f) e^(r dt) + f R is nonpositive on a Gaussian tail of positive probability (about 1e-227 at f = 3), so
E[ln] is not defined; the quadrature nodes and the simulated paths simply missed that tail. The daily checks now
use the admissible unlevered fractions 0.25, 0.5 and 0.75 (half Kelly), with the same seed, tolerances and
refinement test; the quadrature is treated as a numerical approximation and its convergence is checked. The
leveraged fractions stay in the continuous-model checks, where wealth is always positive.

Run: uv run python kelly-check.py   Exits 1 on failure. About 5 seconds.
"""

# standard library imports
import math
import sys

# third party library imports
import numpy as np
import scipy
import scipy.integrate
import scipy.stats

print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
fails = []


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


mu, r, sg = 0.08, 0.02, 0.20


def g(f):
    """Continuous log growth rate of wealth with fraction f in the asset (Ito)."""
    return r + f * (mu - r) - 0.5 * f**2 * sg**2


f_star = (mu - r) / sg**2
fracs = {"half Kelly": f_star / 2, "Kelly": f_star, "twice Kelly": 2 * f_star}

print("== continuous model: identities")
ok("f* = (mu - r)/sigma^2 = 1.5", abs(f_star - 1.5) < 1e-12)
ex_full, ex_half = g(f_star) - r, g(f_star / 2) - r
ok(
    "excess growth 0.045 at Kelly and 0.03375 at half Kelly, ratio 0.75 exactly",
    abs(ex_full - 0.045) < 1e-12
    and abs(ex_half - 0.03375) < 1e-12
    and abs(ex_half / ex_full - 0.75) < 1e-12,
)
ok("variance-rate ratio (f sigma)^2 of half Kelly to Kelly is 0.25", abs((0.5) ** 2 - 0.25) < 1e-15)
ok("twice Kelly earns no excess growth: g(2 f*) = r", abs(g(2 * f_star) - r) < 1e-12)

print("== continuous model: exact log-wealth sampling over 10 years")
T = 10.0
rng = np.random.default_rng(20261041)
WT = rng.standard_normal(200_000) * math.sqrt(T)
for name, f in fracs.items():
    lw = (g(f) * T + f * sg * WT) / T
    m, se, sd = lw.mean(), lw.std(ddof=1) / math.sqrt(len(lw)), lw.std(ddof=1)
    ok(
        f"{name} (f = {f:.4g}): mean ln W_T / T within 3 s.e. of g(f) = {g(f):.5f}; s.d. within 1% of f sigma / sqrt(T)",
        abs(m - g(f)) <= 3 * se and abs(sd / (f * sg / math.sqrt(T)) - 1) < 0.01,
        f"{m:.5f} (s.e. {se:.5f}), s.d. {sd:.4f}",
    )

print("== daily rebalancing: why the levered fractions are excluded")
# With the fraction f restored at the start of each day, the gross factor over the day is
# (1 - f) e^(r dt) + f R, R = exp((mu - sigma^2/2) dt + sigma sqrt(dt) Z). For f > 1 it is nonpositive when
# Z <= z_ruin, so ln W_T has no (unconditional, real) expectation however small that probability is.
dt = 1 / 252


def z_ruin(f, step):
    return (math.log((f - 1) * math.exp(r * step) / f) - (mu - sg**2 / 2) * step) / (
        sg * math.sqrt(step)
    )


for f in (f_star, 2 * f_star):
    zr = z_ruin(f, dt)
    log10_p = scipy.stats.norm.logcdf(zr) / math.log(10)
    gross = (1 - f) * math.exp(r * dt) + f * math.exp(
        (mu - sg**2 / 2) * dt + sg * math.sqrt(dt) * (zr - 1)
    )
    ok(
        f"f = {f:g}: one-day wealth is nonpositive for Z <= {zr:.2f}, a positive probability (10^{log10_p:.0f})",
        gross < 0 and math.isfinite(log10_p) and log10_p > -math.inf,
        f"gross factor {gross:+.4f} at Z = {zr - 1:.2f}",
    )

print("== daily rebalancing with unlevered fractions against its quadrature expectation")
daily = {"quarter": 0.25, "half": 0.5, "half Kelly": f_star / 2}


def g_discrete(f, step, nodes=80):
    """Expected log growth per year with the fraction 0 <= f <= 1 restored every step (GBM within the step).

    Gauss-Hermite quadrature: a numerical approximation, checked for convergence below.
    """
    z, w = np.polynomial.hermite_e.hermegauss(nodes)
    w = w / w.sum()
    gross = (1 - f) * math.exp(r * step) + f * np.exp(
        (mu - sg**2 / 2) * step + sg * math.sqrt(step) * z
    )
    return float(np.sum(w * np.log(gross))) / step


def g_adaptive(f, step):
    """The same expectation by adaptive integration against the normal density (independent of the nodes)."""

    def integrand(z):
        gross = (1 - f) * math.exp(r * step) + f * math.exp(
            (mu - sg**2 / 2) * step + sg * math.sqrt(step) * z
        )
        return math.log(gross) * scipy.stats.norm.pdf(z)

    return (
        scipy.integrate.quad(integrand, -np.inf, np.inf, epsabs=1e-15, epsrel=1e-13, limit=200)[0]
        / step
    )


ok(
    "f = 1 needs no rebalancing: quadrature gives mu - sigma^2/2 = g(1) exactly (to 1e-12)",
    abs(g_discrete(1.0, dt) - (mu - sg**2 / 2)) < 1e-12 and abs(g(1.0) - (mu - sg**2 / 2)) < 1e-15,
)
steps, n_paths = 2520, 20_000
rng = np.random.default_rng(20261042)
logw = {name: np.zeros(n_paths) for name in daily}
for _ in range(steps):
    R = np.exp((mu - sg**2 / 2) * dt + sg * math.sqrt(dt) * rng.standard_normal(n_paths))
    for name, f in daily.items():
        logw[name] += np.log((1 - f) * math.exp(r * dt) + f * R)
for name, f in daily.items():
    gd, gh = g_discrete(f, dt), g_discrete(f, dt / 2)
    bias, bias_half = gd - g(f), gh - g(f)
    quad_err = max(
        abs(g_discrete(f, dt, 40) - gd),
        abs(g_discrete(f, dt, 160) - gd),
        abs(g_adaptive(f, dt) - gd),
        abs(g_discrete(f, dt / 2, 160) - gh),
        abs(g_adaptive(f, dt / 2) - gh),
    )
    ok(
        f"{name} (f = {f:g}): 40-, 80- and 160-node quadrature and adaptive integration agree within 1e-10 a"
        " year, below 1/1000 of the bias",
        quad_err < 1e-10 and quad_err < 1e-3 * abs(bias_half),
        f"largest difference {quad_err:.1e}",
    )
    x = logw[name] / (steps * dt)
    m, se = x.mean(), x.std(ddof=1) / math.sqrt(n_paths)
    ok(
        f"{name}: simulated daily-rebalanced mean within 3 s.e. of the quadrature value {gd:.6f}",
        abs(m - gd) <= 3 * se,
        f"{m:.5f} (s.e. {se:.5f})",
    )
    ok(
        f"{name}: discretisation bias {bias:+.2e} a year is below 5e-4; halving the step scales it by"
        " [0.4, 0.6]",
        abs(bias) < 5e-4 and 0.4 <= bias_half / bias <= 0.6,
        f"ratio {bias_half / bias:.3f}",
    )

print("== discrete bets: the 3/4 identity does not carry over")


def G(f, p, b):
    return p * math.log(1 + b * f) + (1 - p) * math.log(1 - f)


for p, b, f_exp, ratio_exp in ((0.6, 1.0, 0.2, 0.7470), (0.3, 4.0, 0.125, 0.7727)):
    fk = p - (1 - p) / b
    grid = np.linspace(0, 0.99, 99_001)
    numeric = grid[np.argmax([G(x, p, b) for x in grid])]
    ratio = G(fk / 2, p, b) / G(fk, p, b)
    ok(
        f"p = {p}, b = {b}: f* = p - q/b = {f_exp} (grid search agrees); half-Kelly growth ratio {ratio_exp},"
        " not 0.75",
        abs(fk - f_exp) < 1e-12
        and abs(numeric - fk) < 1e-4
        and abs(ratio - ratio_exp) < 5e-5
        and abs(ratio - 0.75) > 1e-3,
        f"{ratio:.4f}",
    )

print("== estimation error in mu")
# mu estimated from 10 years of returns: mu_hat ~ N(mu, sigma^2 / 10). Expected excess growth of the fraction
# c (mu_hat - r) / sigma^2 is c f* (mu - r) - 0.5 c^2 sigma^2 (f*^2 + s^2 / sigma^4), s^2 = sigma^2 / 10.
# Criterion fixed before running: Monte Carlo (200,000 estimates) within 3 s.e. of the formula for c = 1 and
# c = 1/2, with full Kelly negative and half Kelly positive in expectation.
s2 = sg**2 / 10
rng = np.random.default_rng(20261043)
mu_hat = mu + math.sqrt(s2) * rng.standard_normal(200_000)
for c, sign in ((1.0, -1), (0.5, 1)):
    f_hat = c * (mu_hat - r) / sg**2
    sim = f_hat * (mu - r) - 0.5 * f_hat**2 * sg**2
    formula = c * f_star * (mu - r) - 0.5 * c**2 * sg**2 * (f_star**2 + s2 / sg**4)
    ok(
        f"fraction {c} of estimated Kelly: expected excess growth {formula:+.5f}, sign {sign:+d}",
        abs(sim.mean() - formula) <= 3 * sim.std(ddof=1) / math.sqrt(len(sim))
        and formula * sign > 0,
        f"simulated {sim.mean():+.5f}",
    )

if fails:
    print("FAILED:", ", ".join(fails))
    sys.exit(1)
print("all checks passed")
