"""Library gap-filling Batch L5, package L5-a (2026-10-21): the worked examples of meth:lookback-option-valuation.

Inputs and acceptance were frozen before the first run. Model: GBM with constant r, q and sigma, r != q. Hull's floating formulas (OFOD 11th Global
ed., sec. 26.11, pp. 623-624) are evaluated with T read as the remaining time tau and S_min/S_max the extreme recorded
to date; Wilmott's sec. 26.6 forms (PWOQF 2nd ed., pp. 450-452) are an independent transcription.

Part 1, deterministic: Hull's Example 26.2 to its printed rounding (put 7.79, call 8.04) and intermediates; the two
sources against each other for floating and fixed-strike options; the pricing-equation residual; the boundary
condition dV/dM = 0 on S = M; deep-seasoned limits and monotonicity in the recorded extreme.
Part 2, seasoned Monte Carlo: exact one-step simulation of the terminal price and the continuous extreme of the
remaining life (Brownian-bridge extreme, inverse of the barrier entry's crossing probability), default_rng(20261022),
400,000 paths, against the closed forms within 4 standard errors.
Part 3, monitoring: new issue, default_rng(20261021), 100,000 paths of 1,008 log-exact steps in 20 blocks of 5,000
(per block: normals, then uniforms for the minimum, then uniforms for the maximum). Nested grids m = 7, 21, 63, 252,
1,008, each including S_0 and S_T; the continuous extreme on the same paths from exact bridge extremes on every step.
Sampling error (continuous estimate against the closed form) is separated from monitoring bias (paired gap).

Synthetic model data only. Run: uv run --frozen --no-editable python lookback-option-check.py   Exits 1 on failure. About 15 seconds.
"""

# standard library imports
import itertools
import math
import sys

# third party library imports
import numpy as np
import scipy
from scipy import stats

print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
fails = []
N = stats.norm.cdf


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


# ---------------------------------------------------------------- formulas
def hull_floating_call(S, smin, tau, r, q, sig):
    """Hull eq. for c_fl with the minimum to date; tau is the remaining time."""
    st = sig * math.sqrt(tau)
    a1 = (math.log(S / smin) + (r - q + sig**2 / 2) * tau) / st
    a2 = a1 - st
    a3 = (math.log(S / smin) + (-r + q + sig**2 / 2) * tau) / st
    Y1 = -2 * (r - q - sig**2 / 2) * math.log(S / smin) / sig**2
    w = sig**2 / (2 * (r - q))
    return (
        S * math.exp(-q * tau) * N(a1)
        - S * math.exp(-q * tau) * w * N(-a1)
        - smin * math.exp(-r * tau) * (N(a2) - w * math.exp(Y1) * N(-a3))
    )


def hull_floating_put(S, smax, tau, r, q, sig, parts=False):
    """Hull eq. for p_fl with the maximum to date; tau is the remaining time."""
    st = sig * math.sqrt(tau)
    b1 = (math.log(smax / S) + (-r + q + sig**2 / 2) * tau) / st
    b2 = b1 - st
    b3 = (math.log(smax / S) + (r - q - sig**2 / 2) * tau) / st
    Y2 = 2 * (r - q - sig**2 / 2) * math.log(smax / S) / sig**2
    w = sig**2 / (2 * (r - q))
    value = (
        smax * math.exp(-r * tau) * (N(b1) - w * math.exp(Y2) * N(-b3))
        + S * math.exp(-q * tau) * w * N(-b2)
        - S * math.exp(-q * tau) * N(b2)
    )
    return (value, b1, b2, b3, Y2) if parts else value


def _wd(S, M, tau, r, D, sig):
    st = sig * math.sqrt(tau)
    d1 = (math.log(S / M) + (r - D + sig**2 / 2) * tau) / st
    return (
        d1,
        d1 - st,
        sig**2 / (2 * (r - D)),
        (S / M) ** (-2 * (r - D) / sig**2),
        2 * (r - D) * math.sqrt(tau) / sig,
    )


def wilmott_floating_call(S, M, tau, r, D, sig):
    d1, d2, w, pw, sh = _wd(S, M, tau, r, D, sig)
    return (
        S * math.exp(-D * tau) * N(d1)
        - M * math.exp(-r * tau) * N(d2)
        + S * math.exp(-r * tau) * w * (pw * N(-d1 + sh) - math.exp((r - D) * tau) * N(-d1))
    )


def wilmott_floating_put(S, M, tau, r, D, sig):
    d1, d2, w, pw, sh = _wd(S, M, tau, r, D, sig)
    return (
        M * math.exp(-r * tau) * N(-d2)
        - S * math.exp(-D * tau) * N(-d1)
        + S * math.exp(-r * tau) * w * (-pw * N(d1 - sh) + math.exp((r - D) * tau) * N(d1))
    )


def wilmott_fixed_call(S, M, E, tau, r, D, sig):
    """Fixed-strike call on the maximum M to date (sec. 26.6, both cases)."""
    if E > M:
        d1, d2, w, pw, sh = _wd(S, E, tau, r, D, sig)
        return (
            S * math.exp(-D * tau) * N(d1)
            - E * math.exp(-r * tau) * N(d2)
            + S * math.exp(-r * tau) * w * (-pw * N(d1 - sh) + math.exp((r - D) * tau) * N(d1))
        )
    d1, d2, w, pw, sh = _wd(S, M, tau, r, D, sig)
    return (
        (M - E) * math.exp(-r * tau)
        + S * math.exp(-D * tau) * N(d1)
        - M * math.exp(-r * tau) * N(d2)
        + S * math.exp(-r * tau) * w * (-pw * N(d1 - sh) + math.exp((r - D) * tau) * N(d1))
    )


def wilmott_fixed_put(S, M, E, tau, r, D, sig):
    """Fixed-strike put on the minimum M to date (sec. 26.6, both cases)."""
    if E < M:
        d1, d2, w, pw, sh = _wd(S, E, tau, r, D, sig)
        return (
            E * math.exp(-r * tau) * N(-d2)
            - S * math.exp(-D * tau) * N(-d1)
            + S * math.exp(-r * tau) * w * (pw * N(-d1 + sh) - math.exp((r - D) * tau) * N(-d1))
        )
    d1, d2, w, pw, sh = _wd(S, M, tau, r, D, sig)
    return (
        (E - M) * math.exp(-r * tau)
        - S * math.exp(-D * tau) * N(-d1)
        + M * math.exp(-r * tau) * N(-d2)
        + S * math.exp(-r * tau) * w * (pw * N(-d1 + sh) - math.exp((r - D) * tau) * N(-d1))
    )


def hull_fixed_call(S, smax, K, tau, r, q, sig):
    """c_fix = p*_fl + S e^{-q tau} - K e^{-r tau} with S*_max = max(S_max, K) (p. 625)."""
    return (
        hull_floating_put(S, max(smax, K), tau, r, q, sig)
        + S * math.exp(-q * tau)
        - K * math.exp(-r * tau)
    )


def hull_fixed_put(S, smin, K, tau, r, q, sig):
    """p_fix = c*_fl + K e^{-r tau} - S e^{-q tau} with S*_min = min(S_min, K) (p. 625)."""
    return (
        hull_floating_call(S, min(smin, K), tau, r, q, sig)
        + K * math.exp(-r * tau)
        - S * math.exp(-q * tau)
    )


S0, sig, r, q, T = 50.0, 0.4, 0.10, 0.0, 0.25  # Hull Example 26.2

# ---------------------------------------------------------------- part 1
print("== part 1: Example 26.2, two sources, pricing equation, boundary condition, history")
put0, b1, b2, b3, Y2 = hull_floating_put(S0, S0, T, r, q, sig, parts=True)
call0 = hull_floating_call(S0, S0, T, r, q, sig)
ok(
    "Example 26.2 new-issue put rounds to 7.79 (S_max = S_0) and call to 8.04 (S_min = S_0)",
    round(put0, 2) == 7.79 and round(call0, 2) == 8.04,
    f"put {put0:.6f}, call {call0:.6f}",
)
ok(
    "printed intermediates b1 = -0.025, b2 = -0.225, b3 = 0.025 and Y2 = 0",
    abs(b1 + 0.025) <= 5e-4
    and abs(b2 + 0.225) <= 5e-4
    and abs(b3 - 0.025) <= 5e-4
    and abs(Y2) <= 1e-15,
    f"{b1:.6f}, {b2:.6f}, {b3:.6f}, {Y2:.1e}",
)

points = [
    (50.0, 0.25, 0.10, 0.00, 0.40),
    (50.0, 0.25, 0.10, 0.02, 0.40),
    (100.0, 1.00, 0.05, 0.02, 0.25),
]
worst = 0.0
for S, tau, rr, qq, ss in points:
    for smin, smax in ((S, S), (0.9 * S, 1.12 * S)):
        pairs = [
            (
                hull_floating_call(S, smin, tau, rr, qq, ss),
                wilmott_floating_call(S, smin, tau, rr, qq, ss),
            ),
            (
                hull_floating_put(S, smax, tau, rr, qq, ss),
                wilmott_floating_put(S, smax, tau, rr, qq, ss),
            ),
        ]
        for K in (0.95 * smax, 1.1 * smax):
            pairs.append(
                (
                    hull_fixed_call(S, smax, K, tau, rr, qq, ss),
                    wilmott_fixed_call(S, smax, K, tau, rr, qq, ss),
                )
            )
        for K in (0.9 * smin, 1.05 * smin):
            pairs.append(
                (
                    hull_fixed_put(S, smin, K, tau, rr, qq, ss),
                    wilmott_fixed_put(S, smin, K, tau, rr, qq, ss),
                )
            )
        worst = max(worst, max(abs(a - b) / abs(b) for a, b in pairs))
ok(
    "Hull and Wilmott agree: floating call and put, fixed call and put in both strike cases (6 points, q = 0 and 0.02)",
    worst <= 1e-12,
    f"largest relative difference {worst:.1e}",
)


def pde_residual(f, S, M, tau, rr, qq, ss, hS=0.01, ht=1e-5):
    v = f(S, M, tau, rr, qq, ss)
    vS = (f(S + hS, M, tau, rr, qq, ss) - f(S - hS, M, tau, rr, qq, ss)) / (2 * hS)
    vSS = (f(S + hS, M, tau, rr, qq, ss) - 2 * v + f(S - hS, M, tau, rr, qq, ss)) / hS**2
    vtau = (f(S, M, tau + ht, rr, qq, ss) - f(S, M, tau - ht, rr, qq, ss)) / (2 * ht)
    return -vtau + 0.5 * ss**2 * S**2 * vSS + (rr - qq) * S * vS - rr * v


# Harness correction after the first run (recorded in the L5 review record): the frozen steps hS = 0.01, ht = 1e-5
# left a truncation error of up to 3.6e-6 near the running extreme (it falls as hS^2: -3.5e-4, -3.2e-5, -3.6e-6,
# -3.3e-7 at hS = 0.1, 0.03, 0.01, 0.003 for S = 50, S_min = 48, tau = 0.1). The frozen 1e-6 tolerance is kept and
# applied to the Richardson-extrapolated residual (4 R(0.01) - R(0.02)) / 3, which removes the hS^2 term.
pts = [
    (hull_floating_call, 52.0, 45.0, 0.25, 0.10, 0.02, 0.40),
    (hull_floating_call, 50.0, 48.0, 0.10, 0.10, 0.00, 0.40),
    (hull_floating_put, 50.0, 56.0, 0.25, 0.10, 0.02, 0.40),
    (hull_floating_put, 95.0, 110.0, 1.00, 0.05, 0.02, 0.25),
]
raw = [pde_residual(*p) for p in pts]
res = [(4 * pde_residual(*p, hS=0.01) - pde_residual(*p, hS=0.02)) / 3 for p in pts]
print(f"    raw residuals at hS = 0.01: {', '.join(f'{x:.1e}' for x in raw)}")
ok(
    "pricing-equation residual at interior points (S strictly inside the extreme), extrapolated in hS, <= 1e-6",
    max(abs(x) for x in res) <= 1e-6,
    f"largest {max(abs(x) for x in res):.1e}",
)

interior = (
    hull_floating_call(50, 45 + 1e-3, T, r, q, sig)
    - hull_floating_call(50, 45 - 1e-3, T, r, q, sig)
) / 2e-3
fd = {h: (call0 - hull_floating_call(S0, S0 - h, T, r, q, sig)) / h for h in (1e-2, 1e-3)}
ok(
    "dV/dS_min = 0 on S = S_min: one-sided difference small against the interior derivative and linear in h",
    abs(fd[1e-3]) <= 1e-2 * abs(interior) and 5 <= fd[1e-2] / fd[1e-3] <= 20,
    f"interior dc/dS_min {interior:.5f}; at S = S_min {fd[1e-2]:.2e} (h = 0.01), {fd[1e-3]:.2e} (h = 0.001)",
)

deep_c = hull_floating_call(S0, 20.0, T, r, q, sig) - (
    S0 * math.exp(-q * T) - 20.0 * math.exp(-r * T)
)
deep_p = hull_floating_put(S0, 120.0, T, r, q, sig) - (
    120.0 * math.exp(-r * T) - S0 * math.exp(-q * T)
)
ok(
    "deep-seasoned limits: S_min = 20 gives S e^{-q tau} - 20 e^{-r tau}, S_max = 120 gives 120 e^{-r tau} - S e^{-q tau}",
    0 <= deep_c <= 1e-4 and 0 <= deep_p <= 1e-4,
    f"excess {deep_c:.1e} and {deep_p:.1e}; values {hull_floating_call(S0, 20.0, T, r, q, sig):.4f} and "
    f"{hull_floating_put(S0, 120.0, T, r, q, sig):.4f} against new issue {call0:.4f} and {put0:.4f}",
)
cgrid = [hull_floating_call(S0, m, T, r, q, sig) for m in np.arange(20.0, 50.01, 2.5)]
pgrid = [hull_floating_put(S0, m, T, r, q, sig) for m in np.arange(50.0, 120.01, 5.0)]
ok(
    "c_fl strictly decreasing in S_min (20 to 50) and p_fl strictly increasing in S_max (50 to 120)",
    all(a > b for a, b in itertools.pairwise(cgrid))
    and all(a < b for a, b in itertools.pairwise(pgrid)),
)

# ---------------------------------------------------------------- part 2
print(
    "== part 2: seasoned contracts by exact simulation of the remaining life (tau = 0.25, S = 50)"
)
rng = np.random.default_rng(20261022)
n2 = 400_000
x0 = math.log(S0)
z = rng.standard_normal(n2)
u_min = 1.0 - rng.random(n2)
u_max = 1.0 - rng.random(n2)
x1 = x0 + (r - q - sig**2 / 2) * T + sig * math.sqrt(T) * z
spread = (x1 - x0) ** 2
m_fut = np.exp(0.5 * (x0 + x1 - np.sqrt(spread - 2 * sig**2 * T * np.log(u_min))))
M_fut = np.exp(0.5 * (x0 + x1 + np.sqrt(spread - 2 * sig**2 * T * np.log(u_max))))
ST = np.exp(x1)
disc = math.exp(-r * T)
cases = [
    (
        "floating call, S_min = 45",
        disc * (ST - np.minimum(45.0, m_fut)),
        hull_floating_call(S0, 45.0, T, r, q, sig),
    ),
    (
        "floating put, S_max = 56",
        disc * (np.maximum(56.0, M_fut) - ST),
        hull_floating_put(S0, 56.0, T, r, q, sig),
    ),
    (
        "fixed call K = 52, S_max = 56",
        disc * np.maximum(np.maximum(56.0, M_fut) - 52.0, 0),
        hull_fixed_call(S0, 56.0, 52.0, T, r, q, sig),
    ),
    (
        "fixed call K = 60, S_max = 56",
        disc * np.maximum(np.maximum(56.0, M_fut) - 60.0, 0),
        hull_fixed_call(S0, 56.0, 60.0, T, r, q, sig),
    ),
]
se_seasoned = {}
for name, x, cf in cases:
    m, se = x.mean(), x.std(ddof=1) / math.sqrt(n2)
    se_seasoned[name] = se
    ok(
        f"{name}: simulation within 4 s.e. of the closed form",
        abs(m - cf) <= 4 * se,
        f"{m:.4f} (s.e. {se:.4f}) against {cf:.4f}, z = {(m - cf) / se:+.2f}",
    )
gap_c = hull_floating_call(S0, 45.0, T, r, q, sig) - call0
gap_p = hull_floating_put(S0, 56.0, T, r, q, sig) - put0
ok(
    "power: seasoned and new-issue closed forms differ by more than 20 s.e. (ignoring history would fail)",
    abs(gap_c) > 20 * se_seasoned["floating call, S_min = 45"]
    and abs(gap_p) > 20 * se_seasoned["floating put, S_max = 56"],
    f"call +{gap_c:.4f} ({gap_c / se_seasoned['floating call, S_min = 45']:.0f} s.e.), "
    f"put +{gap_p:.4f} ({gap_p / se_seasoned['floating put, S_max = 56']:.0f} s.e.)",
)

# ---------------------------------------------------------------- part 3
print("== part 3: discrete against continuous monitoring on coupled nested grids (new issue)")
rng = np.random.default_rng(20261021)
n_paths, n_steps, block = 100_000, 1008, 5000
grids = (7, 21, 63, 252, 1008)
dt = T / n_steps
keys = [("call", "cont"), ("put", "cont")] + [(k, m) for k in ("call", "put") for m in grids]
acc = {k: [0.0, 0.0] for k in keys}  # sums and sums of squares of discounted payoffs
gacc = {(k, m): [0.0, 0.0] for k in ("call", "put") for m in grids}  # paired gaps
ordered = True
for _ in range(n_paths // block):
    z = rng.standard_normal((block, n_steps))
    um = 1.0 - rng.random((block, n_steps))
    uM = 1.0 - rng.random((block, n_steps))
    x = np.empty((block, n_steps + 1))
    x[:, 0] = x0
    np.cumsum((r - q - sig**2 / 2) * dt + sig * math.sqrt(dt) * z, axis=1, out=x[:, 1:])
    x[:, 1:] += x0
    a, b = x[:, :-1], x[:, 1:]
    d2 = (b - a) ** 2
    mc = np.exp(0.5 * (a + b - np.sqrt(d2 - 2 * sig**2 * dt * np.log(um))).min(axis=1))
    Mc = np.exp(0.5 * (a + b + np.sqrt(d2 - 2 * sig**2 * dt * np.log(uM))).max(axis=1))
    ST = np.exp(x[:, -1])
    pay = {("call", "cont"): disc * (ST - mc), ("put", "cont"): disc * (Mc - ST)}
    for m in grids:
        sub = x[:, :: n_steps // m]
        pay[("call", m)] = disc * (ST - np.exp(sub.min(axis=1)))
        pay[("put", m)] = disc * (np.exp(sub.max(axis=1)) - ST)
    for k in ("call", "put"):
        chain = [pay[(k, "cont")]] + [pay[(k, m)] for m in reversed(grids)]
        ordered &= all(bool((hi >= lo - 1e-12).all()) for hi, lo in itertools.pairwise(chain))
    for key, v in pay.items():
        acc[key][0] += v.sum()
        acc[key][1] += (v**2).sum()
    for k in ("call", "put"):
        for m in grids:
            g = pay[(k, "cont")] - pay[(k, m)]
            gacc[(k, m)][0] += g.sum()
            gacc[(k, m)][1] += (g**2).sum()


def mean_se(s):
    m = s[0] / n_paths
    return m, math.sqrt((s[1] / n_paths - m**2) / (n_paths - 1))


ok(
    "pathwise: continuous >= m = 1,008 >= 252 >= 63 >= 21 >= 7 payoff on every path (call and put)",
    ordered,
)
for k, cf in (("call", call0), ("put", put0)):
    m, se = mean_se(acc[(k, "cont")])
    ok(
        f"{k}: continuous (bridge) estimate within 4 s.e. of the closed form",
        abs(m - cf) <= 4 * se,
        f"{m:.4f} (s.e. {se:.4f}) against {cf:.4f}, z = {(m - cf) / se:+.2f}",
    )
    gaps = {}
    for mm in grids:
        g, gse = mean_se(gacc[(k, mm)])
        gaps[mm] = (g, gse)
        print(
            f"    m = {mm:5d}: value {mean_se(acc[(k, mm)])[0]:.4f}, gap {g:.4f} (paired s.e. {gse:.5f}), gap*sqrt(m) {g * math.sqrt(mm):.3f}"
        )
    ok(
        f"{k}: every monitoring gap positive by more than 4 paired s.e.",
        all(g > 4 * s for g, s in gaps.values()),
    )
    ok(
        f"{k}: convergence, gap at m = 1,008 at most half the gap at m = 63",
        gaps[1008][0] <= 0.5 * gaps[63][0],
        f"{gaps[1008][0]:.4f} against {gaps[63][0]:.4f} (ratio {gaps[1008][0] / gaps[63][0]:.3f})",
    )

if fails:
    print("FAILED:", ", ".join(fails))
    sys.exit(1)
print("all checks passed")
