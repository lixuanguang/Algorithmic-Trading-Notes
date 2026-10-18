"""Portfolio choice (2026-10-18): the worked examples of def:asset-class-characteristics,
def:risk-aversion-utility, meth:efficient-frontier and meth:capital-allocation-line.

Part 1 reads us-asset-class-returns-1928-2025.csv, transcribed from Damodaran's histretSP.xls (January 2026
update; provenance in the CSV header). It recomputes the arithmetic and geometric means that the workbook reports
and adds standard deviations, worst years and real geometric means. These are dated historical statistics of one
country's realised returns, not expected returns.

Parts 2-4 use invented inputs, labelled as such in the entries: one-year horizon, US dollars, total returns in
decimals; three risky funds E (equity), B (bond) and P (property) and a risk-free rate of 3 percent.

Every closed form is checked against an independent route: numerical optimisation (scipy SLSQP), numerical
integration, brute-force grids or the KKT conditions. The figure coordinates in
compendium/portfolio-construction-risk/figures/mean-sd-frontier.tikz are recomputed and compared. No random draws.

Run: uv run python portfolio-choice-checks.py   (numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import csv
import math
import re
import sys
from pathlib import Path

# third party library imports
import numpy as np
import scipy
from scipy import integrate, optimize, stats

print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
fails = []


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


print("== part 1: US asset-class history, 1928-2025 (Damodaran, January 2026 update)")
with open("us-asset-class-returns-1928-2025.csv") as f:
    rows = list(csv.reader(line for line in f if line[0] != "#"))
header, data = rows[0], np.array([[float(x) for x in r] for r in rows[1:]])
years = data[:, 0].astype(int)
series = {name: data[:, i] for i, name in enumerate(header) if name != "year"}
ok(
    "98 years, 1928 to 2025, no gaps",
    len(years) == 98 and (np.diff(years) == 1).all() and years[-1] == 2025,
)
# Damodaran's own summary rows ('Returns by year', rows 'Arithmetic Average' and 'Geometric Average', 1928-2025),
# to four decimals as printed in the workbook.
reported = {
    "sp500": (0.1185, 0.1002),
    "tbill_3m": (0.0341, 0.0337),
    "tbond_10y": (0.0482, 0.0453),
    "baa_corp": (0.0690, 0.0663),
    "real_estate": (0.0438, 0.0420),
    "gold": (0.0736, 0.0561),
}
stats_tab = {}
for name, (arith_rep, geo_rep) in reported.items():
    r = series[name]
    arith = r.mean()
    geo = np.prod(1 + r) ** (1 / len(r)) - 1
    sd = r.std(ddof=1)
    real_geo = np.prod((1 + r) / (1 + series["cpi_inflation"])) ** (1 / len(r)) - 1
    worst = (r.min(), int(years[r.argmin()]))
    stats_tab[name] = (arith, geo, sd, real_geo, worst)
    ok(
        f"{name}: arithmetic {arith:.4f}, geometric {geo:.4f} match the workbook's {arith_rep}, {geo_rep}",
        abs(arith - arith_rep) < 5e-5 and abs(geo - geo_rep) < 5e-5,
        f"s.d. {sd:.4f}, real geometric {real_geo:.4f}, worst {worst[0]:.4f} in {worst[1]}",
    )
infl = series["cpi_inflation"]
ok(
    "CPI inflation 1928-2025: geometric mean 3.04 percent",
    close(np.prod(1 + infl) ** (1 / 98) - 1, 0.030357, 5e-6),
    f"{np.prod(1 + infl) ** (1 / 98) - 1:.6f}",
)
ok(
    "geometric below arithmetic for every series, by roughly half the variance",
    all(v[1] < v[0] and abs((v[0] - v[1]) - v[2] ** 2 / 2) < 0.012 for v in stats_tab.values()),
    ", ".join(
        f"{k} gap {v[0] - v[1]:.4f} vs s^2/2 {v[2] ** 2 / 2:.4f}" for k, v in stats_tab.items()
    ),
)
excess = series["sp500"] - series["tbond_10y"]
ok(
    "stocks minus T.bonds, 1928-2025: arithmetic mean 7.03 percent, standard error 2.10 percent",
    close(excess.mean(), 0.070323, 5e-6)
    and close(excess.std(ddof=1) / math.sqrt(98), 0.021028, 5e-6),
    f"mean {excess.mean():.6f}, s.e. {excess.std(ddof=1) / math.sqrt(98):.6f}",
)
last10 = years >= 2016
ok(
    "2016-2025 arithmetic means differ from the full sample (stocks 15.75, T.bonds 1.22, gold 16.53)",
    close(series["sp500"][last10].mean(), 0.1575, 5e-5)
    and close(series["tbond_10y"][last10].mean(), 0.0122, 5e-5)
    and close(series["gold"][last10].mean(), 0.1653, 5e-5),
)
stock_neg = int((series["sp500"] < 0).sum())
ok("stocks fell in 26 of the 98 years", stock_neg == 26, f"{stock_neg}")
ok(
    "the T.bill never had a negative annual return; real T.bill return negative in 40 years",
    (series["tbill_3m"] >= 0).all()
    and int(((1 + series["tbill_3m"]) / (1 + infl) < 1).sum()) == 40,
    f"{int(((1 + series['tbill_3m']) / (1 + infl) < 1).sum())}",
)

print("== part 2: risk aversion and mean-variance utility")
A = 3.0


def U(m, s, a=A):
    return m - 0.5 * a * s * s


ok(
    "A = 3: E 0.07, s.d. 0.15 gives U = 0.03625 (decimals); in percent units U = 7 - 0.005 x 3 x 225 = 3.625",
    close(U(0.07, 0.15), 0.03625) and close(7 - 0.5 * A * 15**2 / 100, 3.625),
)
ok(
    "the same risky portfolio is worth less than a 4 percent riskless rate to A = 3 and more to A = 1",
    U(0.07, 0.15) < 0.04 and U(0.07, 0.15, 1.0) > 0.04,
    f"A = 1: {U(0.07, 0.15, 1.0):.5f}",
)
ok("A = 0 (risk neutral) ranks by expected return only", close(U(0.07, 0.15, 0.0), 0.07))
# CARA utility u(W) = -exp(-a W) with normal W: the certainty equivalent is exactly mu_W - a s_W^2 / 2.
W0, a_abs = 100.0, 0.03  # wealth in dollars and absolute risk aversion per dollar; a W0 = 3
muW, sW = W0 * 1.07, W0 * 0.15
EU = integrate.quad(
    lambda w: -math.exp(-a_abs * w) * stats.norm.pdf(w, muW, sW), muW - 12 * sW, muW + 12 * sW
)[0]
CE = -math.log(-EU) / a_abs
ok(
    "CARA-normal: certainty equivalent by integration = mu - a s^2 / 2 = 103.625 (a W0 = 3, i.e. A = 3)",
    close(CE, muW - 0.5 * a_abs * sW**2, 1e-6) and close(CE / W0 - 1, U(0.07, 0.15), 1e-8),
    f"CE {CE:.6f}",
)
# Log utility (relative risk aversion 1) and a two-point return: the Arrow-Pratt approximation of the risk
# premium, s^2 R / 2 for returns, is close for small risks and poor for large ones.
for h in (0.05, 0.40):
    ce_log = math.exp(0.5 * math.log(1 + h) + 0.5 * math.log(1 - h)) - 1  # mean return 0
    prem = 0.0 - ce_log
    approx = 0.5 * h * h
    print(f"    two-point +/-{h:.2f}: exact premium {prem:.6f}, approximation {approx:.6f}")
ce5 = math.sqrt(1 - 0.05**2) - 1
ce40 = math.sqrt(1 - 0.40**2) - 1
ok(
    "log utility, +/-5 percent: premium 0.1251 percent vs 0.1250; +/-40 percent: 8.35 vs 8.00 percent",
    close(-ce5, 0.0012508, 1e-7) and close(-ce40, 0.083485, 1e-6),
)
ok(
    "concave utility rejects a fair bet: E[ln(1 + r)] < ln(1 + E r) for r = +/-0.2",
    0.5 * math.log(1.2) + 0.5 * math.log(0.8) < 0.0,
)

print("== part 3: feasible set, minimum-variance frontier and efficient frontier (invented inputs)")
names = ["E", "B", "P"]
mu = np.array([0.08, 0.035, 0.06])
sd = np.array([0.18, 0.06, 0.12])
Corr = np.array([[1.0, 0.1, 0.6], [0.1, 1.0, 0.3], [0.6, 0.3, 1.0]])
S = np.outer(sd, sd) * Corr
one = np.ones(3)
ok(
    "covariance matrix positive definite (eigenvalues > 0)",
    np.linalg.eigvalsh(S).min() > 0,
    f"{np.linalg.eigvalsh(S)}",
)
Si = np.linalg.inv(S)
a_, b_, c_ = one @ Si @ one, one @ Si @ mu, mu @ Si @ mu
d_ = a_ * c_ - b_**2
ok(
    "D = AC - B^2 > 0 because mu is not proportional to the vector of ones",
    d_ > 0,
    f"A {a_:.4f} B {b_:.4f} C {c_:.4f} D {d_:.4f}",
)
wg = Si @ one / a_
mg, sg = wg @ mu, math.sqrt(wg @ S @ wg)
print(f"    GMV weights {wg.round(4)}, mean {mg:.6f}, s.d. {sg:.6f}")
res = optimize.minimize(
    lambda w: w @ S @ w,
    one / 3,
    constraints=[{"type": "eq", "fun": lambda w: w.sum() - 1}],
    method="SLSQP",
    options={"ftol": 1e-15, "maxiter": 500},
)
ok(
    "GMV: Sigma^-1 1 / (1' Sigma^-1 1) = numerical minimum; weights 0.0536, 0.8933, 0.0531; mean 3.874, s.d. 5.821",
    np.allclose(res.x, wg, atol=1e-6)
    and np.allclose(wg, [0.053563, 0.893327, 0.053109], atol=1e-6)
    and close(mg, b_ / a_)
    and close(sg**2, 1 / a_)
    and close(mg, 0.038738, 1e-6)
    and close(sg, 0.058211, 1e-6),
)


def frontier_w(m):
    lam, gam = (c_ - b_ * m) / d_, (a_ * m - b_) / d_
    return Si @ (lam * one + gam * mu)


def frontier_var(m):
    return (a_ * m * m - 2 * b_ * m + c_) / d_


def num_frontier(m, long_only=False):
    cons = [
        {"type": "eq", "fun": lambda w: w.sum() - 1},
        {"type": "eq", "fun": lambda w: w @ mu - m},
    ]
    r = optimize.minimize(
        lambda w: w @ S @ w,
        one / 3,
        bounds=[(0, None)] * 3 if long_only else None,
        constraints=cons,
        method="SLSQP",
        options={"ftol": 1e-15, "maxiter": 1000},
    )
    return r


table = {}
for m in (0.05, 0.06, 0.07, 0.075, 0.08, 0.09):
    w = frontier_w(m)
    r = num_frontier(m)
    table[m] = (w, math.sqrt(frontier_var(m)))
    assert np.allclose(r.x, w, atol=1e-6), (m, r.x, w)
    assert close(w @ S @ w, frontier_var(m), 1e-12)
    print(
        f"    target {m:.3f}: unconstrained weights {w.round(4)}, s.d. {math.sqrt(frontier_var(m)):.4f}"
    )
ok(
    "closed-form target-return weights = SLSQP at 5, 6, 7, 7.5, 8 and 9 percent; variance formula = w'Sw",
    True,
)
ok(
    "unconstrained frontier: 6 percent needs weights 0.3718, 0.2974, 0.3308 and s.d. 10.11 percent",
    np.allclose(table[0.06][0], [0.371783, 0.297426, 0.330791], atol=1e-6)
    and close(table[0.06][1], 0.101114, 1e-6),
)
# Target at which the unconstrained bond weight reaches zero: w_B(m) is linear in m.
wB = lambda m: frontier_w(m)[1]
m_star = optimize.brentq(wB, 0.06, 0.08)
ok(
    "unconstrained bond weight falls to zero at a 7.06 percent target and is negative above it (-0.2631 at 8)",
    close(m_star, 0.070612, 1e-6)
    and frontier_w(0.08)[1] < 0
    and close(frontier_w(0.08)[1], -0.263108, 1e-6),
    f"{m_star:.6f}",
)
lo75 = num_frontier(0.075, long_only=True)
w75 = lo75.x
# Long-only at 7.5 percent: B = 0 is binding. Check KKT: on the active set {E, P} the solution is the two-asset
# frontier point, and the multiplier on w_B >= 0 is non-negative.
wEP = np.array([(0.075 - 0.06) / (0.08 - 0.06), 0.0, 1 - (0.075 - 0.06) / (0.08 - 0.06)])
grad = 2 * S @ wEP
M = np.array([[1.0, mu[0]], [1.0, mu[2]]])
nu = np.linalg.solve(M, grad[[0, 2]])  # grad_i = nu0 + nu1 mu_i for the free assets
kkt_B = grad[1] - (nu[0] + nu[1] * mu[1])
ok(
    "long-only 7.5 percent: boundary solution 0.75 E, 0 B, 0.25 P (s.d. 15.49 percent); KKT multiplier on w_B > 0",
    np.allclose(w75, wEP, atol=1e-5)
    and kkt_B > 0
    and close(math.sqrt(wEP @ S @ wEP), 0.154871, 1e-6),
    f"multiplier {kkt_B:.6f}, unconstrained s.d. {table[0.075][1]:.4f}",
)
# Interior solutions (correction pass, 2026-10-18): where the unconstrained optimum already satisfies w >= 0, the
# long-only optimum is the same portfolio; the 7.5 percent target is where the constraint changes the answer.
interior = all(
    (frontier_w(m) > 1e-3).all()
    and np.allclose(num_frontier(m, long_only=True).x, frontier_w(m), atol=1e-5)
    for m in (0.05, 0.06)
)
ok(
    "5 and 6 percent: unconstrained weights strictly positive, so the long-only optimum is identical; "
    "7.5 percent differs (w_B = 0, s.d. 15.49 against 15.25)",
    interior
    and frontier_w(0.075)[1] < 0
    and math.sqrt(wEP @ S @ wEP) > math.sqrt(frontier_var(0.075)) + 1e-3,
)
lo8 = num_frontier(0.08, long_only=True)
ok("long-only 8 percent: only E is feasible (s.d. 18)", np.allclose(lo8.x, [1, 0, 0], atol=1e-6))
lo9 = num_frontier(0.09, long_only=True)
ok(
    "long-only 9 percent is infeasible: above the largest expected return; the optimiser reports failure",
    (not lo9.success) or abs(lo9.x @ mu - 0.09) > 1e-6 or (lo9.x < -1e-9).any(),
    f"success={lo9.success}, message={lo9.message}",
)
# Dominance: a point on the lower branch is dominated by the frontier point with the same s.d. above the GMV.
m_low = 0.03
s_low = math.sqrt(frontier_var(m_low))
m_up = 2 * mg - m_low  # same variance, mirror image about the GMV mean
ok(
    "3 percent lies on the inefficient branch: the 4.75 percent frontier portfolio has the same s.d. (6.74)",
    close(frontier_var(m_up), frontier_var(m_low), 1e-12)
    and close(m_up, 0.047476, 1e-6)
    and close(s_low, 0.067402, 1e-6),
    f"{m_up:.6f}, {s_low:.6f}",
)
ok(
    "bond fund alone: frontier s.d. at 3.5 percent is 5.99986 < 6.00; efficient mean at s.d. 6 is 4.2478 percent",
    math.sqrt(frontier_var(0.035)) < 0.06
    and close(math.sqrt(frontier_var(0.035)), 0.05999857, 1e-8)
    and close(mg + math.sqrt((0.06**2 - 1 / a_) * d_ / a_), 0.042478, 1e-6)
    and close(frontier_var(mg + math.sqrt((0.06**2 - 1 / a_) * d_ / a_)), 0.06**2, 1e-12),
)
# Singular covariance: two perfectly correlated assets; the inverse does not exist.
S_sing = np.outer([0.2, 0.1], [0.2, 0.1])
ok("a 2x2 covariance with correlation +1 is singular (rank 1)", np.linalg.matrix_rank(S_sing) == 1)
ok(
    "equal expected returns make D = 0: the frontier is a single point in mean",
    close(
        (one @ Si @ one) * (np.full(3, 0.05) @ Si @ np.full(3, 0.05))
        - (one @ Si @ np.full(3, 0.05)) ** 2,
        0.0,
        1e-9,
    ),
)
# Brute-force check that no long-only portfolio beats the frontier: grid over the simplex.
grid = [
    np.array([x, y, 1 - x - y])
    for x in np.linspace(0, 1, 201)
    for y in np.linspace(0, 1, 201)
    if x + y <= 1 + 1e-12
]
pts = np.array([(w @ mu, math.sqrt(max(w @ S @ w, 0.0))) for w in grid])
ok(
    "grid of 20,301 long-only portfolios: none lies left of the unconstrained frontier",
    all(s >= math.sqrt(frontier_var(m)) - 1e-12 for m, s in pts),
)

print("== part 4: risk-free asset, capital allocation line and optimal allocation")
rf = 0.03
z = Si @ (mu - rf)
wt = z / z.sum()
mt, st = wt @ mu, math.sqrt(wt @ S @ wt)
sharpe = (mt - rf) / st
ok("tangency exists on the upper branch: GMV mean 3.874 > rf 3.0", mg > rf)
res_t = optimize.minimize(
    lambda w: -(w @ mu - rf) / math.sqrt(w @ S @ w),
    one / 3,
    constraints=[{"type": "eq", "fun": lambda w: w.sum() - 1}],
    method="SLSQP",
    options={"ftol": 1e-15, "maxiter": 1000},
)
ok(
    "tangency Sigma^-1 (mu - rf 1) normalised = maximum-Sharpe SLSQP: 0.4374, 0.1745, 0.3881; mean 6.438, s.d. 11.547",
    np.allclose(res_t.x, wt, atol=1e-5)
    and np.allclose(wt, [0.437403, 0.174545, 0.388052], atol=1e-6)
    and close(mt, 0.064384, 1e-6)
    and close(st, 0.115473, 1e-6),
    f"Sharpe {sharpe:.6f}",
)
ok("Sharpe ratio of the tangency (slope of the CAL) 0.2978", close(sharpe, 0.297771, 1e-6))
ok(
    "the tangency is also on the minimum-variance frontier (variance formula at its mean)",
    close(st**2, frontier_var(mt), 1e-12),
)
for w_any in (wg, frontier_w(0.07), np.array([0.6, 0.2, 0.2])):
    s_any = math.sqrt(w_any @ S @ w_any)
    assert (w_any @ mu - rf) / s_any <= sharpe + 1e-12
ok("CALs through the GMV, the 7 percent frontier portfolio and a 60/20/20 mix are flatter", True)
ystar = {Aa: (mt - rf) / (Aa * st * st) for Aa in (2.0, 4.0, 8.0)}
print("    y* =", {k: round(v, 4) for k, v in ystar.items()})
ok(
    "optimal risky share y* = (E r_T - rf)/(A s_T^2): 1.2894 (borrow), 0.6447, 0.3223",
    close(ystar[2.0], 1.289357, 1e-6)
    and close(ystar[4.0], 0.644679, 1e-6)
    and close(ystar[8.0], 0.322339, 1e-6),
)
for Aa, y in ystar.items():
    yy = np.linspace(-0.5, 3, 35001)
    best = yy[np.argmax(rf + yy * (mt - rf) - 0.5 * Aa * (yy * st) ** 2)]
    assert abs(best - y) < 1e-4, (Aa, best, y)
ok("y* equals the grid maximiser of U(y) for A = 2, 4, 8", True)
pos4 = (rf + ystar[4.0] * (mt - rf), ystar[4.0] * st)
ok(
    "A = 4: 64.5 percent in T, 35.5 percent lent; mean 5.217, s.d. 7.444; U = 0.04108",
    close(pos4[0], 0.052167, 1e-6)
    and close(pos4[1], 0.074443, 1e-6)
    and close(U(pos4[0], pos4[1], 4.0), 0.041083, 1e-6),
    f"{pos4}",
)
pos2 = (rf + ystar[2.0] * (mt - rf), ystar[2.0] * st)
ok(
    "A = 2: 128.9 percent in T financed by borrowing 28.9 percent at 3; mean 7.433, s.d. 14.889",
    close(pos2[0], 0.074334, 1e-6) and close(pos2[1], 0.148886, 1e-6),
)
# A borrowing rate above the GMV mean has no upper-branch tangency: 1' Sigma^-1 (mu - r 1) = B - r A < 0.
z5 = Si @ (mu - 0.05)
w5 = z5 / z5.sum()
ok(
    "r = 5 percent > GMV mean 3.874: the normalised formula gives a lower-branch point (mean 1.88 percent)",
    z5.sum() < 0
    and close(z5.sum(), b_ - 0.05 * a_)
    and w5 @ mu < mg
    and close(w5 @ mu, 0.018839, 1e-6),
    f"sum {z5.sum():.4f}",
)
# Higher borrowing rate: 3.5 percent (lending stays at 3). The borrowing line is tangent at a riskier frontier
# portfolio, which in this unconstrained example shorts B.
rb = 0.035
zb = Si @ (mu - rb)
wb = zb / zb.sum()
mb, sb = wb @ mu, math.sqrt(wb @ S @ wb)
y_b = (mb - rb) / (2.0 * sb * sb)
print(
    f"    borrowing tangency {wb.round(4)}, mean {mb:.6f}, s.d. {sb:.6f}, y at rb for A=2: {y_b:.4f}"
)
ok(
    "borrowing at 3.5 percent: tangency 0.9508, -0.7869, 0.8361 (mean 9.87, s.d. 24.03); for A = 2, y = 0.55 < 1",
    np.allclose(wb, [0.950820, -0.786885, 0.836066], atol=1e-6)
    and close(mb, 0.098689, 1e-6)
    and close(sb, 0.240277, 1e-6)
    and close(y_b, 0.551577, 1e-6),
)


# With lending at 3 and borrowing at 3.5 percent, the A = 2 investor wants y > 1 on the lending line and y < 1
# on the borrowing line, so holds a frontier portfolio without riskless lending or borrowing: maximise
# mu_p - (A/2) s_p^2 along the frontier between the two tangency means.
def u_front(m):
    return m - 1.0 * frontier_var(m)


m_opt = optimize.minimize_scalar(
    lambda m: -u_front(m), bounds=(mt, mb), method="bounded", options={"xatol": 1e-12}
).x
ok(
    "A = 2 with 3.5 percent borrowing: frontier portfolio with mean 7.18 and s.d. 14.11, between the tangencies",
    mt < m_opt < mb
    and close(m_opt, b_ / a_ + d_ / (2.0 * a_), 1e-6)
    and close(m_opt, 0.071805, 1e-6)
    and close(math.sqrt(frontier_var(m_opt)), 0.141146, 1e-6),
    f"{m_opt:.6f}, weights {frontier_w(m_opt).round(4)}",
)
ok(
    "its utility 0.05188 beats lending-line and borrowing-line choices restricted to y <= 1 and y >= 1",
    u_front(m_opt)
    >= max(U(rf + y * (mt - rf), y * st, 2.0) for y in np.linspace(0, 1, 1001)) - 1e-12
    and u_front(m_opt)
    >= max(U(rb + y * (mb - rb), y * sb, 2.0) for y in np.linspace(1, 3, 2001)) - 1e-12
    and close(u_front(m_opt), 0.051884, 1e-6),
    f"{u_front(m_opt):.6f}",
)

print("== figure: mean-standard deviation diagram coordinates")
fig = Path("../../../compendium/portfolio-construction-risk/figures/mean-sd-frontier.tikz")
txt = fig.read_text()


def coords(tag):
    block = re.search(rf"% {tag}\n.*?coordinates \{{(.*?)\}}", txt, re.S).group(1)
    return np.array([[float(v) for v in p.split(",")] for p in re.findall(r"\(([^)]*)\)", block)])


upper = coords("efficient")
lower = coords("inefficient")
lo_front = coords("long-only")
ok(
    "figure: efficient and inefficient branches are (100 s, 100 m) of the closed-form frontier to 0.01",
    all(
        abs(100 * math.sqrt(frontier_var(m / 100)) - s) < 0.006
        for s, m in np.vstack([upper, lower])
    ),
)
lo_ok = True
for s, m in lo_front:
    r = num_frontier(m / 100, long_only=True)
    lo_ok &= abs(100 * math.sqrt(r.fun) - s) < 0.006
ok("figure: long-only frontier points match SLSQP with w >= 0 to 0.01", lo_ok)
ok(
    "figure: T, GMV, E, B, P, the A = 4 optimum (7.44, 5.22) and the CAL end (24, 10.147) as computed",
    all(
        s in txt
        for s in (
            "(11.55,6.44)",
            "(5.82,3.87)",
            "(18,8)",
            "(6,3.5)",
            "(12,6)",
            "(7.44,5.22)",
            "(24,10.147)",
        )
    )
    and close(3 + sharpe * 24, 10.147, 1e-3)
    and close(100 * pos4[1], 7.44, 0.005)
    and close(100 * pos4[0], 5.22, 0.005),
)

if fails:
    print("FAILED:", ", ".join(fails))
    sys.exit(1)
print("all checks passed")
