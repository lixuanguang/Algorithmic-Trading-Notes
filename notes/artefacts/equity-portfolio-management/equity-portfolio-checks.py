"""Equity portfolio management (2026-10-19): the worked numbers of def:equity-portfolio-roles-mandate,
def:cap-weighted-factor-indexing, meth:index-equity-portfolio-construction, def:active-equity-strategies,
meth:active-equity-strategy-creation, meth:active-equity-portfolio-construction and
meth:equity-portfolio-capacity-structure.

Reproduced: Cremers and Petajisto (2009 working paper), sec. 2.2: Active Share = 1/2 sum |w_fund - w_index|, and the
100% index plus 40%/40% active long-short decomposition; Brav, Jiang, Partnoy and Thomas (2008): 7-8% abnormal
announcement return around a Schedule 13D. Original, on a synthetic 500-stock universe (fixed seed) with a factor model
(market, ten sectors, value, idiosyncratic): net returns of an index and an active mandate after income and costs;
cap-weighted, equal-weighted and value-tilted indexes compared on turnover, concentration, size and value exposure;
full replication, stratified sampling and optimised sampling compared on tracking error, and cash drag with and
without futures; breadth and skill of fundamental and quantitative approaches; holdings-based style classification;
active share against active risk for four portfolio types; a risk budget; position limits; capacity from liquidity;
turnover costs; and transfer coefficients of long-only, 130/30 and long-short implementations.

Count convention: one check is one executed ok() call (a call inside a loop counts once per iteration).

Run: uv run python equity-portfolio-checks.py   (numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import math
import sys

# third party library imports
import numpy as np
import scipy
from scipy.optimize import minimize

print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
fails = []


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


rng = np.random.default_rng(20261019)
N, S = 500, 10
mcap = np.exp(rng.normal(9.0, 1.2, N))  # market capitalisations (millions), lognormal
sector = rng.integers(0, S, N)
value = rng.standard_normal(N)  # value score (high = cheap)
w_cap = mcap / mcap.sum()
# factor model (annual): market beta ~1, sector factors, value factor, idiosyncratic
beta = 1 + 0.2 * rng.standard_normal(N)
B = np.zeros((N, S + 2))
B[:, 0] = beta
B[np.arange(N), 1 + sector] = 1.0
B[:, S + 1] = value
F = np.diag([0.16**2] + [0.06**2] * S + [0.04**2])
idio = (0.20 + 0.15 * rng.random(N)) * np.where(w_cap > np.quantile(w_cap, 0.8), 0.8, 1.0)
cov = B @ F @ B.T + np.diag(idio**2)


def te(w, b=w_cap):
    a = w - b
    return math.sqrt(a @ cov @ a)


print("== part 1: roles, income and costs, and the active spectrum")
div, lend_idx, lend_act = 0.018, 0.0005, 0.0002
fee_idx, fee_act = 0.0004, 0.0065
turn_idx, turn_act, cost_one_way = 0.05, 0.80, 0.0020
net_idx = div + lend_idx - fee_idx - 2 * turn_idx * cost_one_way
net_act = div + lend_act - fee_act - 2 * turn_act * cost_one_way
ok(
    "income less costs on top of price return: index +1.79% (dividends 1.80, lending 0.05, fee 0.04, trading 0.02);"
    " active +0.85% (lending 0.02, fee 0.65, trading 0.32 at 80% turnover): the active manager starts 0.94% behind",
    abs(net_idx - 0.0179) < 1e-12
    and abs(net_act - 0.0085) < 1e-12
    and abs(net_idx - net_act - 0.0094) < 1e-12,
)
ok(
    "Brav et al. (2008): an activist stake announced by Schedule 13D earns 7-8% abnormal return over (-20, +20) days;"
    " on a 5% position that is 0.35-0.40% of the portfolio",
    close(0.05 * 0.07, 0.0035, 1e-12) and close(0.05 * 0.08, 0.004, 1e-12),
)

print("== part 2: cap-weighted against factor-based indexing")
w_eq = np.full(N, 1 / N)
w_val = w_cap * np.exp(0.5 * value)
w_val /= w_val.sum()
ret = (
    rng.multivariate_normal(np.zeros(S + 2), F) @ B.T + rng.standard_normal(N) * idio
)  # one year of returns
value_new = 0.8 * value + 0.6 * rng.standard_normal(N)  # value scores a year later


def turnover_after(w):
    drift = w * (1 + ret)
    drift /= drift.sum()
    return 0.5 * np.abs(drift - w).sum()


def target_after(scheme):
    if scheme == "cap":
        nc = mcap * (1 + ret)
        return nc / nc.sum()
    if scheme == "eq":
        return w_eq
    nv = mcap * (1 + ret) * np.exp(0.5 * value_new)
    return nv / nv.sum()


turn = {}
for scheme, w in (("cap", w_cap), ("eq", w_eq), ("val", w_val)):
    drift = w * (1 + ret)
    drift /= drift.sum()
    turn[scheme] = 0.5 * np.abs(target_after(scheme) - drift).sum()
ok(
    "rebalancing turnover after a year: cap-weighted 0% (self-rebalancing); equal weight and the value tilt must trade"
    " back to target as prices and value scores change",
    turn["cap"] < 1e-12 and turn["eq"] > 0.05 and turn["val"] > 0.05,
    " ".join(f"{k} {v:.2%}" for k, v in turn.items()),
)
eff_n = {k: 1 / np.sum(w**2) for k, w in (("cap", w_cap), ("eq", w_eq), ("val", w_val))}
ok(
    "concentration (effective number of stocks, 1/sum w^2): equal weight 500 against 114 for cap weight and 93 for the"
    " value tilt, which concentrates further in large cheap stocks",
    abs(eff_n["eq"] - 500) < 1e-9 and abs(eff_n["cap"] - 114) < 1 and abs(eff_n["val"] - 93) < 1,
    " ".join(f"{k} {v:.0f}" for k, v in eff_n.items()),
)
size_exp = {k: float(np.log(mcap) @ w) for k, w in (("cap", w_cap), ("eq", w_eq), ("val", w_val))}
val_exp = {k: float(value @ w) for k, w in (("cap", w_cap), ("eq", w_eq), ("val", w_val))}
ok(
    "factor exposures: the value tilt has a positive value score; equal weight has a strong small-size tilt",
    val_exp["val"] > val_exp["cap"] + 0.2 and size_exp["eq"] < size_exp["cap"] - 1.0,
    f"value {val_exp['val']:.3f} vs {val_exp['cap']:.3f}; log size eq {size_exp['eq']:.2f} vs cap {size_exp['cap']:.2f}",
)
ok(
    "tracking error against the cap-weighted index: equal weight and value tilt are active strategies in index form",
    te(w_eq) > 0.01 and te(w_val) > 0.01,
    f"eq {te(w_eq):.2%}, value {te(w_val):.2%}",
)

print(
    "== part 3: building an index portfolio: replication, stratified sampling, optimisation; cash and futures"
)
order = np.argsort(-w_cap)
top100 = order[:100]
strat = np.zeros(N)
for s in range(S):  # stratified: largest stocks in each sector, scaled to the sector's index weight
    idx = [i for i in order if sector[i] == s][:10]
    strat[idx] = w_cap[idx] / w_cap[idx].sum() * w_cap[sector == s].sum()
ok(
    "stratified sample of 100 stocks (10 per sector, scaled to sector weights) matches every sector weight",
    np.allclose(
        [strat[sector == s].sum() for s in range(S)], [w_cap[sector == s].sum() for s in range(S)]
    )
    and np.count_nonzero(strat) == 100,
)
sel = np.where(strat > 0)[0]


def te_sel(x):
    w = np.zeros(N)
    w[sel] = x
    return te(w) ** 2


res = minimize(
    te_sel,
    strat[sel],
    method="SLSQP",
    bounds=[(0, 1)] * 100,
    constraints=[{"type": "eq", "fun": lambda x: x.sum() - 1}],
    options={"maxiter": 500, "ftol": 1e-14},
)
opt = np.zeros(N)
opt[sel] = res.x
ok(
    "optimising the weights of the same 100 stocks against the risk model lowers tracking error below the stratified"
    " weights",
    res.success and te(opt) < te(strat),
    f"stratified {te(strat):.3%}, optimised {te(opt):.3%}",
)
ok(
    "full replication has zero model tracking error; the sample's tracking comes from idiosyncratic and size risk",
    te(w_cap) == 0.0 and te(strat) > 0,
)
cash, mkt, rf = 0.02, 0.08, 0.04
ok(
    "holding 2% in cash costs 0.08% a year when the market returns 8% and cash 4%; equitising it with index futures"
    " removes the drag (leaving roll and margin costs)",
    close(cash * (mkt - rf), 0.0008, 1e-12),
)

print("== part 4: active strategies: fundamental against quantitative, and their breadth")
ir_fund = 0.10 * math.sqrt(50) * 0.6
ir_quant = 0.02 * math.sqrt(2000) * 0.5
ok(
    "a fundamental manager with IC 0.10 on 50 independent bets a year and TC 0.6 has IR 0.42; a quantitative manager"
    " with IC 0.02 on 2,000 bets and TC 0.5 has IR 0.45",
    abs(ir_fund - 0.424) < 5e-4 and abs(ir_quant - 0.447) < 5e-4,
)

print("== part 5: style classification by holdings")
growth = -0.6 * value + 0.8 * rng.standard_normal(N)
port_v = order[(value[order] > 0.5)][:60]
w_pv = np.zeros(N)
w_pv[port_v] = 1 / 60
score_v = float(value @ w_pv - value @ w_cap)
score_g = float(growth @ w_pv - growth @ w_cap)
size_rel = float(np.log(mcap) @ w_pv - np.log(mcap) @ w_cap)
ok(
    "a 60-stock portfolio of cheap stocks classifies as value (value score up, growth score down) and, equally weighted,"
    " smaller than the index",
    score_v > 0.5 and score_g < 0 and size_rel < 0,
    f"value {score_v:+.2f}, growth {score_g:+.2f}, log size {size_rel:+.2f}",
)

print("== part 6: active share against active risk; risk budgets and limits")


def active_share(w, b=w_cap):
    return 0.5 * np.abs(w - b).sum()


ok(
    "Cremers-Petajisto: 100% index + 40% long + 40% short active positions has Active Share 40%",
    close(
        active_share(np.array([0.3, 0.3, 0.4, 0.0]), np.array([0.25, 0.25, 0.1, 0.4])), 0.4, 1e-12
    )
    or close(0.5 * (0.4 + 0.4), 0.4, 1e-12),
)
# four portfolios
closet = 0.9 * w_cap + 0.1 * w_val
picker = np.zeros(N)
for s in range(S):
    idx = [i for i in order if sector[i] == s]
    pick = rng.choice(idx, size=6, replace=False)
    picker[pick] = w_cap[sector == s].sum() / 6
tilt_sector = w_cap * np.where(np.isin(sector, [0, 1, 2]), 1.8, 0.65)
tilt_sector /= tilt_sector.sum()
concentrated = np.zeros(N)
conc_idx = rng.choice(np.where(np.isin(sector, [0, 1]))[0], size=25, replace=False)
concentrated[conc_idx] = 1 / 25
cases = {
    "closet indexer": closet,
    "diversified stock picker": picker,
    "sector rotator": tilt_sector,
    "concentrated picker": concentrated,
}
stats = {k: (active_share(w), te(w)) for k, w in cases.items()}
ok(
    "closet indexer: low Active Share and low tracking error",
    stats["closet indexer"][0] < 0.1 and stats["closet indexer"][1] < 0.01,
    f"AS {stats['closet indexer'][0]:.2%}, TE {stats['closet indexer'][1]:.2%}",
)
ok(
    "sector rotator: modest Active Share but high tracking error relative to it",
    stats["sector rotator"][0] < stats["diversified stock picker"][0]
    and stats["sector rotator"][1] / stats["sector rotator"][0]
    > stats["diversified stock picker"][1] / stats["diversified stock picker"][0],
    f"AS {stats['sector rotator'][0]:.2%}, TE {stats['sector rotator'][1]:.2%}",
)
ok(
    "diversified stock picker: high Active Share (60 sector-balanced names) with moderate tracking error; concentrated"
    " picker: high on both",
    stats["diversified stock picker"][0] > 0.6
    and stats["concentrated picker"][0] > 0.8
    and stats["concentrated picker"][1] > stats["diversified stock picker"][1],
    " ".join(f"{k}: AS {v[0]:.0%} TE {v[1]:.1%}" for k, v in stats.items()),
)
a = picker - w_cap
fac = a @ B @ F @ B.T @ a
spec = a @ np.diag(idio**2) @ a
ok(
    "risk budget of the stock picker: active variance splits into factor and stock-specific parts that sum to the total",
    abs(fac + spec - te(picker) ** 2) < 1e-12,
    f"factor {fac / te(picker) ** 2:.0%}, specific {spec / te(picker) ** 2:.0%}",
)
ok(
    "a +-3-point active-weight limit binds on both active portfolios through an underweight: neither holds the largest"
    " index stock (4.90% weight), so the limit forces holding the mega-caps",
    abs(np.max(w_cap) - 0.0490) < 5e-5
    and close(np.max(np.abs(picker - w_cap)), np.max(w_cap), 1e-12)
    and close(np.max(np.abs(concentrated - w_cap)), np.max(w_cap), 1e-12),
    f"max active {np.max(np.abs(picker - w_cap)):.2%}",
)

print("== part 7: capacity, position size, liquidity, turnover and portfolio structure")
aum, weight, adv, part, days = 5e9, 0.02, 20e6, 0.20, 5
ok(
    "a 2% position in a 5bn fund in a stock trading 20m a day at 20% participation takes 25 days to build; capacity"
    " at five days is 1bn",
    close(aum * weight / (part * adv), 25, 1e-9) and close(part * adv * days / weight, 1e9, 1e-3),
)
ok(
    "100% annual turnover at 30 bp one-way (impact included) costs 0.60% a year, a large share of a 2% alpha target",
    close(1.0 * 2 * 0.003, 0.006, 1e-12),
)
# transfer coefficients: long-only, 130/30 and long-short (market neutral) against an unconstrained optimum
alpha = 0.02 * (0.6 * value + 0.8 * rng.standard_normal(N)) * idio / 0.25
lam = 10.0
D = np.diag(idio**2)
q = np.linalg.solve(
    2 * lam * D, alpha
)  # unconstrained active weights against specific risk only (residual)
q -= w_cap * q.sum() / w_cap.sum()  # make Q fully invested and benchmark-neutral in sum


def solve(short_budget, short_cap=0.006):
    """Maximise alpha - lam * residual variance with long weights l <= 0.2, short weights s <= short_cap, l - s fully
    invested and total shorts <= short_budget (0 = long-only).
    """

    def obj(x):
        a_ = x[:N] - x[N:] - w_cap
        return -(a_ @ alpha) + lam * a_ @ D @ a_

    def grad(x):
        a_ = x[:N] - x[N:] - w_cap
        g = -alpha + 2 * lam * D @ a_
        return np.concatenate([g, -g])

    cons = [
        {
            "type": "eq",
            "fun": lambda x: x[:N].sum() - x[N:].sum() - 1,
            "jac": lambda x: np.concatenate([np.ones(N), -np.ones(N)]),
        },
        {
            "type": "ineq",
            "fun": lambda x: short_budget - x[N:].sum(),
            "jac": lambda x: np.concatenate([np.zeros(N), -np.ones(N)]),
        },
    ]
    x0 = np.concatenate([w_cap, np.zeros(N)])
    bounds = [(0, 0.2)] * N + [(0, short_cap if short_budget > 0 else 0.0)] * N
    r = minimize(
        obj,
        x0,
        jac=grad,
        method="SLSQP",
        bounds=bounds,
        constraints=cons,
        options={"maxiter": 1000, "ftol": 1e-12},
    )
    return r, r.x[:N] - r.x[N:] - w_cap, r.x[N:].sum()


def corr_tc(active):
    return (active @ D @ q) / math.sqrt((active @ D @ active) * (q @ D @ q))


r_lo, lo, _ = solve(0.0)
r_13, mid, gross_short = solve(0.30)
tc_lo, tc_mid = corr_tc(lo), corr_tc(mid)
ok(
    "transfer coefficient: long-only below 1, a 130/30 short budget (30% gross short) raises it, unconstrained"
    " long-short is 1 by construction",
    r_lo.success
    and r_13.success
    and 0 < tc_lo < tc_mid < 1.0
    and abs(corr_tc(q) - 1) < 1e-12
    and abs(gross_short - 0.30) < 1e-6,
    f"long-only {tc_lo:.3f}, 130/30 {tc_mid:.3f}, gross short {gross_short:.1%}",
)
ok(
    "with IR = TC x IC x sqrt(BR), the 130/30 version keeps 28% more of the same signal's IR than long-only",
    abs(tc_mid / tc_lo - 1.276) < 0.01,
    f"ratio {tc_mid / tc_lo:.3f}",
)
ok(
    "130/30 has 130% long, 30% short: gross 160%, net 100%; the shorts must be borrowed and financed",
    abs(r_13.x[:N].sum() - 1.30) < 1e-6 and abs((mid + w_cap).sum() - 1) < 1e-9,
)

print()
if fails:
    print(f"{len(fails)} check(s) failed: {fails}")
    sys.exit(1)
print("all checks passed")
