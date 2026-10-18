"""Batch 2 portfolio risk and return (2026-10-18): the worked examples of meth:portfolio-return-moments and
mech:diversification-correlation.

All data are invented for illustration and are not evidence about any market.

Example 1, scenario model: one year, values in US dollars, total returns (income reinvested, no fees, no external
cash flows during the year). Beginning value 1,000,000: 600,000 in an equity fund E and 400,000 in a bond fund B.
Three states with probabilities 0.3, 0.5, 0.2. A second portfolio Q holds 30/70.

Example 2, short synthetic history: six monthly total returns in percent for E and B, typed in by hand (no random
draw), with the portfolio rebalanced to 60/40 at the start of each month.

Example 3, correlation sensitivity: long-only weights 0.6/0.4, volatilities 20 and 10 percent; equal-weighted
portfolios of N assets with equal volatility and pairwise correlation.

Example 4, Longin and Solnik's illustration: a bivariate normal with constant correlation 0.5, split by the size
of the first return at its median absolute value, gives conditional correlations of about 0.21 and 0.62.

Every formula is checked against direct aggregation of the scenario or sample portfolio returns, or against an
independent route (numpy covariance, scipy integration, exact enumeration). No seeds are used.

Run: uv run python portfolio-moments-checks.py   (numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import math
import sys

# third party library imports
import numpy as np
import scipy
from scipy import integrate, stats

print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
fails = []


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


print("== example 1: scenario (population) moments")
p = np.array([0.3, 0.5, 0.2])  # boom, normal, recession
R = np.array([[25.0, -2.0], [8.0, 4.0], [-20.0, 10.0]])  # percent per year: E, B
V0 = np.array([600_000.0, 400_000.0])
w = V0 / V0.sum()
v = np.array([0.3, 0.7])
V1 = (V0 * (1 + R / 100)).sum(1)
Rp_value = 100 * (V1 / V0.sum() - 1)
Rp = R @ w
ok("beginning-of-period value weights are 0.6 and 0.4", np.allclose(w, [0.6, 0.4]))
ok(
    "portfolio return from end values equals the weighted return in every state: 14.2, 6.4, -8.0",
    np.allclose(Rp_value, Rp) and np.allclose(Rp, [14.2, 6.4, -8.0]),
    f"{Rp}",
)
mu = p @ R
dev = R - mu
Sigma = (p[:, None] * dev).T @ dev
sE, sB = np.sqrt(np.diag(Sigma))
rho = Sigma[0, 1] / (sE * sB)
ok(
    "E[R_E] = 7.5, E[R_B] = 3.4; Var 243.25 and 17.64; s.d. 15.60 and 4.20; Cov -64.5; rho -0.9847",
    np.allclose(mu, [7.5, 3.4])
    and close(Sigma[0, 0], 243.25)
    and close(Sigma[1, 1], 17.64)
    and close(Sigma[0, 1], -64.5)
    and close(rho, -0.984655, 1e-6),
    f"sE {sE:.4f} sB {sB:.4f} rho {rho:.4f}",
)
Ep_direct = p @ Rp
Vp_direct = p @ (Rp - Ep_direct) ** 2
Ep_formula = w @ mu
Vp_expanded = w[0] ** 2 * Sigma[0, 0] + w[1] ** 2 * Sigma[1, 1] + 2 * w[0] * w[1] * Sigma[0, 1]
Vp_matrix = w @ Sigma @ w
ok(
    "E[R_P] = w'mu = 5.86 equals the probability-weighted portfolio return",
    close(Ep_direct, Ep_formula) and close(Ep_formula, 5.86),
)
ok(
    "Var(R_P): direct = expanded 87.57 + 2.8224 - 30.96 = w'Sigma w = 59.4324; s.d. 7.7092",
    close(Vp_direct, Vp_expanded)
    and close(Vp_expanded, Vp_matrix)
    and close(Vp_matrix, 59.4324, 1e-9),
    f"s.d. {math.sqrt(Vp_matrix):.4f}",
)
wavg_sd = w @ np.sqrt(np.diag(Sigma))
ok(
    "portfolio s.d. 7.71 is below the weighted average of the two s.d.s, 11.04, and above the bond's 4.20",
    math.sqrt(Vp_matrix) < wavg_sd and math.sqrt(Vp_matrix) > sB,
    f"weighted average {wavg_sd:.4f}",
)
Rq = R @ v
Eq = p @ Rq
cov_pq_direct = p @ ((Rp - Ep_direct) * (Rq - Eq))
cov_pq = w @ Sigma @ v
Vq = v @ Sigma @ v
corr_pq = cov_pq / math.sqrt(Vp_matrix * Vq)
ok(
    "Q 30/70: E 4.63, Var 3.4461; Cov(P, Q) = w'Sigma v = 13.8942 = direct covariance; corr(P, Q) 0.9709",
    close(cov_pq_direct, cov_pq)
    and close(cov_pq, 13.8942, 1e-9)
    and close(Eq, 4.63)
    and close(Vq, 3.4461, 1e-9)
    and close(corr_pq, cov_pq_direct / math.sqrt(Vp_direct * (p @ (Rq - Eq) ** 2)))
    and close(corr_pq, 0.970863, 1e-6),
    f"Cov {cov_pq:.4f}, Var(Q) {Vq:.4f}, corr {corr_pq:.4f}",
)

print("== example 2: estimates from a short synthetic history")
hist = np.array(
    [[3.0, 0.4], [-1.5, 0.9], [4.2, -0.3], [-2.8, 1.2], [1.6, 0.1], [0.9, 0.5]]
)  # percent per month, E then B
n = len(hist)
m = hist.mean(0)
S1 = np.cov(hist, rowvar=False, ddof=1)
S0 = np.cov(hist, rowvar=False, ddof=0)
by_hand = (hist - m).T @ (hist - m)
ok(
    "means 0.9, 0.4667; over N-1: var 7.048, 0.2907, cov -1.336 (numpy = hand sums; also over N)",
    np.allclose(m, [0.9, 0.466667], atol=1e-6)
    and np.allclose(S1, by_hand / (n - 1))
    and np.allclose(S0, by_hand / n)
    and np.allclose(S1, [[7.048, -1.336], [-1.336, 0.290667]], atol=1e-6),
    f"S(N-1) var {S1[0, 0]:.4f}, {S1[1, 1]:.4f}, cov {S1[0, 1]:.4f}",
)
r1 = S1[0, 1] / math.sqrt(S1[0, 0] * S1[1, 1])
r0 = S0[0, 1] / math.sqrt(S0[0, 0] * S0[1, 1])
ok(
    "sample correlation -0.9334 is the same with either denominator",
    close(r1, r0, 1e-12) and close(r1, -0.933417, 1e-6),
)
rp_hist = hist @ w
ok(
    "rebalanced 60/40 series 1.96 ... 0.74: mean 0.7267 = w'xbar; var 1.9425 = w'S w (N-1); over N, w'S0 w",
    np.allclose(rp_hist, [1.96, -0.54, 2.4, -1.2, 1.0, 0.74])
    and close(rp_hist.mean(), w @ m)
    and close(rp_hist.var(ddof=1), 1.942507, 1e-6)
    and close(rp_hist.var(ddof=1), w @ S1 @ w)
    and close(rp_hist.var(ddof=0), w @ S0 @ w),
    f"mean {rp_hist.mean():.4f}, var {rp_hist.var(ddof=1):.4f}, s.d. {rp_hist.std(ddof=1):.4f}",
)
mixed = S1[0, 1] / math.sqrt(S0[0, 0] * S0[1, 1])
ok(
    "mixing denominators inflates the correlation by N/(N-1) = 1.2",
    close(mixed / r1, n / (n - 1), 1e-12),
)
# Buy and hold: weights drift with relative performance, so the constant-weight identity no longer describes the
# portfolio's monthly returns after the first month.
values = V0.copy()
bh = []
for row in hist:
    start = values.sum()
    values = values * (1 + row / 100)
    bh.append(100 * (values.sum() / start - 1))
bh = np.array(bh)
w2 = (V0 * (1 + hist[0] / 100)) / (V0 * (1 + hist[0] / 100)).sum()
ok(
    "buy and hold: month 1 matches 60/40; month 2 uses the drifted weights 0.6061/0.3939",
    close(bh[0], rp_hist[0])
    and not close(bh[1], rp_hist[1], 1e-6)
    and close(bh[1], w2 @ hist[1])
    and np.allclose(w2, [0.606120, 0.393880], atol=1e-6),
    f"w2 {w2.round(4)}, month 2 {bh[1]:.4f} against {rp_hist[1]:.4f}",
)

print("== example 3: correlation sensitivity, long only")
a, b = 0.6, 0.4
s1, s2 = 20.0, 10.0


def sd(rho_, wa=a):
    return math.sqrt(wa**2 * s1**2 + (1 - wa) ** 2 * s2**2 + 2 * wa * (1 - wa) * rho_ * s1 * s2)


ok(
    "rho +1: s.d. 16.00 = weighted average; rho 0: 12.65; rho -1: |12 - 4| = 8.00",
    close(sd(1.0), 16.0) and close(sd(0.0), math.sqrt(160)) and close(sd(-1.0), 8.0),
    f"{sd(1.0):.4f}, {sd(0.0):.4f}, {sd(-1.0):.4f}",
)
grid = np.linspace(-1, 1, 2001)
ok(
    "s.d. rises with rho and never exceeds the weighted average 16 (long only)",
    all(np.diff([sd(r) for r in grid]) > 0) and max(sd(r) for r in grid) <= 16 + 1e-12,
)
ok(
    "at rho 0 and rho 0.3 the 60/40 s.d. (12.65, 13.74) is below 16 but above the safer asset's 10",
    10 < sd(0.0) < 16 and 10 < sd(0.3) < 16,
    f"rho 0.3: {sd(0.3):.4f}",
)
wz = s2 / (s1 + s2)
ok(
    "rho -1: zero variance at w_E = s2/(s1 + s2) = 1/3, a long-only weight",
    close(sd(-1.0, wz), 0.0, 1e-12),
)
wgrid = np.linspace(0, 1, 100_001)
ok(
    "rho 0 and rho +1: no long-only weight gives zero variance (minimum s.d. 8.94 and 10)",
    min(sd(0.0, x) for x in wgrid) > 8.9 and close(min(sd(1.0, x) for x in wgrid), 10.0, 1e-9),
    f"rho 0 minimum {min(sd(0.0, x) for x in wgrid):.4f}",
)
ok(
    "rho +1: zero variance needs a short position, w_E = -s2/(s1 - s2) = -1",
    close(sd(1.0, -s2 / (s1 - s2)), 0.0, 1e-12),
)
thr = s2 / s1
ok(
    "a small equity holding lowers s.d. below the bond's 10 only if rho < s2/s1 = 0.5",
    sd(0.3, 0.05) < 10 and sd(0.7, 0.05) > 10 and close(sd(thr, 1e-6), 10.0, 1e-5),
    f"w_E 0.05: rho 0.3 {sd(0.3, 0.05):.4f}, rho 0.7 {sd(0.7, 0.05):.4f}",
)
ok("rho 0: w_E = 0.2 gives 8.94, below the bond's 10", close(sd(0.0, 0.2), math.sqrt(80)))
# Equal weights over N assets with equal s.d. sigma and pairwise correlation r: var = sigma^2 (1/N + (1 - 1/N) r).
sig, r = 20.0, 0.3
for N in (1, 2, 10, 100):
    C = np.full((N, N), r * sig**2)
    np.fill_diagonal(C, sig**2)
    ew = np.full(N, 1 / N)
    assert close(ew @ C @ ew, sig**2 * (1 / N + (1 - 1 / N) * r), 1e-9)
lim = sig * math.sqrt(r)
ok(
    "equal weights, s.d. 20, rho 0.3: s.d. 20, 16.12, 12.17, 11.08 for N = 1, 2, 10, 100; limit 10.95",
    close(math.sqrt(sig**2 * (1 / 2 + 0.5 * r)), 16.1245, 1e-4)
    and close(math.sqrt(sig**2 * (0.1 + 0.9 * r)), 12.1655, 1e-4)
    and close(math.sqrt(sig**2 * (0.01 + 0.99 * r)), 11.0815, 1e-4)
    and close(lim, 10.9545, 1e-4),
)

print(
    "== example 4: correlation conditional on the size of one return (Longin and Solnik's illustration)"
)
c = stats.norm.ppf(0.75)  # median of |X| for a standard normal, 0.674
rho0 = 0.5


def cond_corr(var_x):
    # Y = rho X + sqrt(1 - rho^2) Z with Z independent: conditioning on X changes Var(X) only.
    return rho0 * math.sqrt(var_x) / math.sqrt(rho0**2 * var_x + 1 - rho0**2)


small = integrate.quad(lambda x: x * x * stats.norm.pdf(x), -c, c)[0] / 0.5
large = 2 * integrate.quad(lambda x: x * x * stats.norm.pdf(x), c, np.inf)[0] / 0.5
ok(
    "threshold 0.674; Var(X | |X| < c) = 0.1427 and Var(X | |X| > c) = 1.8573 (closed form = integration)",
    close(c, 0.674490, 1e-6)
    and close(small, 1 - 2 * c * stats.norm.pdf(c) / 0.5, 1e-9)
    and close(large, 1 + 2 * c * stats.norm.pdf(c) / 0.5, 1e-9),
    f"{small:.4f}, {large:.4f}",
)
ok(
    "constant correlation 0.5, yet conditional correlations 0.21 (small) and 0.62 (large) as the paper reports",
    round(cond_corr(small), 2) == 0.21 and round(cond_corr(large), 2) == 0.62,
    f"{cond_corr(small):.4f}, {cond_corr(large):.4f}",
)

if fails:
    print("FAILED:", ", ".join(fails))
    sys.exit(1)
print("all checks passed")
