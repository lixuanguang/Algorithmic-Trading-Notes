"""Numerical checks for the closed forms in model-derivations.tex (this folder).

1. Grossman-Miller with per-share fees: the date-1 price and LT1's date-1 holding solved by root-finding
   (brentq, xtol 1e-14) against the closed forms (mu=10, gamma=2, sigma^2=0.04, n=5 market makers, imbalance i=3,
   fee eta=0.01); tolerance 1e-9.
2. Grossman-Miller liquidity measures: lambda = -gamma sigma^2 / n = -0.016, and Cov(Delta1, Delta2) = -lambda^2 Var(Q)
   by simulation (seed 1, N=400,000, Q ~ N(0,1), news eps1, eps2 ~ N(0, 0.1^2)); tolerance 3e-5.
3. Kyle single auction (sigma_v=2, sigma_u=3, m=1): beta = sigma_u/sigma_v, lambda = sigma_v/(2 sigma_u) = 1/3,
   expected profit sigma_v sigma_u / 2 = 3 and Var(v|y) = sigma_v^2/2 = 2, by simulation (seed 2, N=1,000,000);
   relative tolerance 1 percent; the projection slope by regression, tolerance 0.005.
4. Static limit-order depth: delta* = 1/kappa maximises delta exp(-kappa delta); grid of 200,001 points on [0, 2]
   with kappa=4 gives 0.25, tolerance 1e-5; second-order condition negative.
5. Roll: Var(dP) = sigma^2 + S^2/2 and Cov(dP_t, dP_{t-1}) = -S^2/4 (S=0.2, sigma=0.1, Q = +/-1), by simulation
   (seed 3, N=1,000,000); tolerance 5e-4; lag-2 autocovariance within 5e-4 of zero.
Run: uv run python model-derivations-checks.py   (numpy and scipy). Exits non-zero on failure.
"""

# standard library imports
import sys

# third party library imports
import numpy as np
from scipy import optimize

failures = []


def check(name, ok, detail):
    print(("ok   " if ok else "FAIL ") + name + ": " + detail)
    if not ok:
        failures.append(name)


# 1. Grossman-Miller with per-share fees (model-derivations.tex, "Per-share fees"): for i > 0 LT1's fee cancels,
# q1_LT1 = (mu - S1)/(gamma sigma^2), while a market maker pays a round trip, q1_MM = (mu - S1 - 2 eta)/(gamma sigma^2);
# clearing i = n q1_MM + q1_LT1.
mu, g, s2, n, i, eta = 10.0, 2.0, 0.04, 5, 3.0, 0.01
P1_closed = mu - g * s2 * i / (n + 1) - 2 * n * eta / (n + 1)
q_lt_closed = i / (n + 1) + 2 * n / (n + 1) * eta / (g * s2)


def excess(P1):
    q_mm = (mu - P1 - 2 * eta) / (g * s2)
    q_lt = (mu - P1) / (g * s2)
    return n * q_mm + q_lt - i


P1_root = optimize.brentq(excess, mu - 10, mu + 10, xtol=1e-14)
q_lt_root = (mu - P1_root) / (g * s2)
check(
    "GM fee price",
    abs(P1_root - P1_closed) < 1e-9 and abs(P1_root - 9.943333333333333) < 1e-9,
    f"P1 root {P1_root:.9f}, closed {P1_closed:.9f}",
)
check(
    "GM fee LT demand",
    abs(q_lt_root - q_lt_closed) < 1e-9 and abs(q_lt_root - 0.708333333333333) < 1e-9,
    f"q_LT1 root {q_lt_root:.9f}, closed {q_lt_closed:.9f}",
)

# 2. Liquidity measures: P1 - mu = lambda Q with lambda = -g s2 / n; dP2 = noise - lambda Q.
lam = -g * s2 / n
check("GM lambda", abs(lam + 0.016) < 1e-15, f"lambda {lam}")
rng = np.random.default_rng(1)
N = 400_000
Q = rng.normal(0.0, 1.0, N)
e1 = rng.normal(0.0, 0.1, N)
e2 = rng.normal(0.0, 0.1, N)
dP1 = e1 + lam * Q
dP2 = e2 - lam * Q
cov = np.cov(dP1, dP2)[0, 1]
check(
    "GM autocovariance",
    abs(cov - (-(lam**2))) < 3e-5,
    f"simulated {cov:.6f}, closed {-(lam**2):.6f}",
)

# 3. Kyle single auction.
sv, su, m = 2.0, 3.0, 1.0
beta = su / sv
lk = sv / (2 * su)
rng = np.random.default_rng(2)
N = 1_000_000
v = m + rng.normal(0.0, sv, N)
u = rng.normal(0.0, su, N)
x = beta * (v - m)
y = x + u
p = m + lk * y
profit = np.mean(x * (v - p))
slope = np.cov(v, y)[0, 1] / np.var(y, ddof=1)
resid_var = np.var(v - (m + slope * y))
check("Kyle lambda", abs(lk - 1 / 3) < 1e-15, f"lambda {lk:.6f}")
check("Kyle projection", abs(slope - lk) < 0.005, f"regression slope {slope:.5f}")
check(
    "Kyle profit",
    abs(profit / (sv * su / 2) - 1) < 0.01,
    f"simulated {profit:.4f}, closed {sv * su / 2}",
)
check(
    "Kyle posterior variance",
    abs(resid_var / (sv**2 / 2) - 1) < 0.01,
    f"simulated {resid_var:.4f}, closed {sv**2 / 2}",
)

# 4. Static limit-order depth.
k = 4.0
grid = np.linspace(0.0, 2.0, 200_001)
arg = grid[np.argmax(grid * np.exp(-k * grid))]
soc = (k**2 * (1 / k) - 2 * k) * np.exp(
    -1.0
)  # (k^2 delta - 2k) e^{-k delta} at delta = 1/k, i.e. -k/e
check(
    "limit-order argmax",
    abs(arg - 1 / k) < 1e-5 and soc < 0,
    f"grid argmax {arg:.6f}, SOC {soc:.4f}",
)

# 5. Roll.
S, sig = 0.2, 0.1
rng = np.random.default_rng(3)
N = 1_000_000
eps = rng.normal(0.0, sig, N)
Qs = rng.choice([-1.0, 1.0], N)
V = np.cumsum(eps)
P = V + 0.5 * S * Qs
dP = np.diff(P)
var = np.var(dP)
c1 = np.cov(dP[1:], dP[:-1])[0, 1]
c2 = np.cov(dP[2:], dP[:-2])[0, 1]
check(
    "Roll variance",
    abs(var - (sig**2 + S**2 / 2)) < 5e-4,
    f"simulated {var:.5f}, closed {sig**2 + S**2 / 2}",
)
check(
    "Roll autocovariance",
    abs(c1 + S**2 / 4) < 5e-4 and abs(c2) < 5e-4,
    f"lag 1 {c1:.5f} (closed {-(S**2) / 4}), lag 2 {c2:.5f}",
)

sys.exit(1 if failures else 0)
