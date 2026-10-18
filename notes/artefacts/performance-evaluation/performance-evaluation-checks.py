"""Performance evaluation (2026-10-18): the worked examples of meth:risk-adjusted-performance-measures,
meth:downside-appraisal-measures, meth:return-attribution, meth:macro-attribution-owner-manager,
meth:benchmark-selection-quality and meth:manager-skill-evaluation.

Every return series and weight is invented and typed by hand (percent). Part 2 reproduces Bacon's Table 5.6 Sharpe
ratios (3rd ed., 2023, p. 159); part 8 reproduces Exhibits 12-19 and 12-20 of Bailey, Richards and Tierney
(Managing Investment Portfolios, 3rd ed., 2007, pp. 777-778), which assume normally distributed annual value added.
Conventions: downside deviation divides by all n observations (Bacon eq. 5.80); capture ratios are ratios of
arithmetic means over up or down benchmark months (Bacon eqs. 4.21-4.22); drawdown is peak to trough of
cumulative wealth; Carino linking follows Bacon eqs. 6.153-6.158; fixed-income attribution follows the weighted-
duration decomposition Bacon attributes to van Breukelen (eqs. 6.121-6.133) with returns approximated by income
minus duration times yield change.

No random draws. Run: uv run python performance-evaluation-checks.py   (numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import math
import sys

# third party library imports
import numpy as np
import scipy
from scipy.stats import binom, norm

print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
fails = []


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


print(
    "== part 1: Sharpe, Treynor, M-squared, Jensen's alpha and the appraisal ratio (annual, percent)"
)
rf, rB, sB = 3.0, 8.0, 15.0
funds = {"P": (9.5, 14.0, 0.90), "Q": (11.0, 22.0, 1.00)}
out = {}
for k, (r, s, beta) in funds.items():
    sharpe = (r - rf) / s
    treynor = (r - rf) / beta
    m2 = rf + sharpe * sB
    jensen = r - rf - beta * (rB - rf)
    resid = math.sqrt(
        s * s - beta * beta * sB * sB
    )  # single-index model: sigma^2 = beta^2 sigma_B^2 + sigma_e^2
    out[k] = (sharpe, treynor, m2, jensen, resid, jensen / resid)
    print(
        f"    {k}: SR {sharpe:.4f} TR {treynor:.4f} M2 {m2:.4f} alpha {jensen:.4f} sigma_e {resid:.4f} AR {jensen / resid:.4f}"
    )
srB = (rB - rf) / sB
ok(
    "benchmark: Sharpe 0.3333, Treynor 5.0, M2 8.0 = its own return",
    close(srB, 1 / 3) and close(rf + srB * sB, rB),
)
ok(
    "P: Sharpe 0.4643, Treynor 7.22, M2 9.96 (1.96 above the benchmark), alpha 2.00, AR 0.539",
    abs(out["P"][0] - 0.464286) < 1e-6
    and abs(out["P"][1] - 7.2222) < 1e-4
    and abs(out["P"][2] - 9.964286) < 1e-6
    and close(out["P"][3], 2.0)
    and abs(out["P"][5] - 0.53936) < 1e-5,
)
ok(
    "Q: Sharpe 0.3636, Treynor 8.0, M2 8.45, alpha 3.00, AR 0.186",
    abs(out["Q"][0] - 0.363636) < 1e-6
    and close(out["Q"][1], 8.0)
    and abs(out["Q"][2] - 8.454545) < 1e-6
    and close(out["Q"][3], 3.0)
    and abs(out["Q"][5] - 0.18641) < 1e-5,
)
ok(
    "rankings split: total-risk measures prefer P, beta-based measures prefer Q",
    out["P"][0] > out["Q"][0]
    and out["P"][2] > out["Q"][2]
    and out["Q"][1] > out["P"][1]
    and out["Q"][3] > out["P"][3],
)
ok(
    "M2 ranks exactly as Sharpe (it is a linear transform at fixed rf and sigma_B)",
    (out["P"][2] - out["Q"][2]) * (out["P"][0] - out["Q"][0]) > 0,
)
ok(
    "Jensen's alpha = beta x (Treynor - benchmark Treynor)",
    all(close(out[k][3], funds[k][2] * (out[k][1] - (rB - rf))) for k in funds),
)

print("== part 2: Bacon's Table 5.6")
ok(
    "Sharpe ratios 1.07, 1.53, 1.22 for (7.9, 5.5), (6.9, 3.2), (7.5, 4.5) with rf 2%",
    [round((r - 2) / s, 2) for r, s in [(7.9, 5.5), (6.9, 3.2), (7.5, 4.5)]] == [1.07, 1.53, 1.22],
)

print("== part 3: downside, capture and drawdown measures on 24 invented months")
P = np.array(
    [
        1.8,
        -0.6,
        2.4,
        -3.1,
        1.2,
        0.9,
        -1.5,
        2.8,
        0.4,
        -0.9,
        1.6,
        2.1,
        -2.4,
        0.7,
        1.9,
        -0.3,
        3.0,
        -4.2,
        -1.8,
        2.2,
        0.5,
        -1.2,
        1.4,
        0.8,
    ]
)
B = np.array(
    [
        2.0,
        -1.0,
        2.6,
        -3.8,
        1.0,
        1.1,
        -2.0,
        3.0,
        0.2,
        -1.4,
        1.8,
        2.3,
        -3.0,
        0.5,
        2.1,
        -0.6,
        3.2,
        -5.0,
        -2.2,
        2.0,
        0.6,
        -1.6,
        1.5,
        0.7,
    ]
)
MAR = 0.25  # minimum acceptable return, percent a month


def downside_dev(x, mar):
    return math.sqrt((np.minimum(x - mar, 0.0) ** 2).mean())


def sortino_annual(x, mar):
    d = downside_dev(x, mar)
    return math.inf if d == 0 else 12 * (x.mean() - mar) / (math.sqrt(12) * d)


dd = downside_dev(P, MAR)
srt = sortino_annual(P, MAR)
print(f"    mean {P.mean():.4f}, downside deviation {dd:.4f}, annual Sortino {srt:.4f}")
ok(
    "downside deviation counts every month in the denominator, with zeros above the MAR",
    close(dd, math.sqrt(sum(min(v - MAR, 0) ** 2 for v in P) / 24)),
)
ok(
    "a series never below the MAR has zero downside deviation and an undefined (infinite) Sortino",
    sortino_annual(np.array([0.5, 0.6, 0.9]), MAR) == math.inf,
)
up, dn = B > 0, B < 0
ucap = P[up].mean() / B[up].mean()
dcap = P[dn].mean() / B[dn].mean()
print(f"    up capture {ucap:.4f} ({up.sum()} months), down capture {dcap:.4f} ({dn.sum()} months)")
ok(
    "15 up and 9 down benchmark months; up capture 0.963, down capture 0.777",
    up.sum() == 15 and dn.sum() == 9 and abs(ucap - 0.96341) < 1e-5 and abs(dcap - 0.77670) < 1e-5,
)
ok(
    "capture ratio of upside to downside capture exceeds 1 (asymmetric participation)",
    ucap / dcap > 1,
)


def drawdowns(x):
    w = np.concatenate([[1.0], np.cumprod(1 + x / 100)])
    peak = np.maximum.accumulate(w)
    d = w / peak - 1
    trough = int(d.argmin())
    pk = int(w[: trough + 1].argmax())
    rec = next((k for k in range(trough, len(w)) if w[k] >= w[pk]), None)
    return d.min(), pk, trough, rec


mddP, pkP, trP, recP = drawdowns(P)
print(
    f"    max drawdown {mddP:.6f}, peak at end of month {pkP}, trough at end of month {trP}, recovery {recP}"
)
ok(
    "maximum drawdown -5.92% over months 18-19 ((1 - 0.042)(1 - 0.018) - 1)",
    abs(mddP - ((1 - 0.042) * (1 - 0.018) - 1)) < 1e-12 and (pkP, trP) == (17, 19),
)
ok("not recovered by month 24: recovery time is censored, not zero", recP is None)
w_path = np.concatenate([[1.0], np.cumprod(1 + P / 100)])
rec4 = next(t for t in range(4, 25) if w_path[t] >= w_path[3])
ok(
    "the -3.1% drawdown after month 3 recovers at month 8: duration 5 months from peak, 4 from trough",
    rec4 == 8 and w_path[7] < w_path[3] <= w_path[8],
)
Pq = np.array([np.prod(1 + P[i : i + 3] / 100) - 1 for i in range(0, 24, 3)]) * 100
ok("quarterly sampling of the same path shows a shallower drawdown", drawdowns(Pq)[0] > mddP)
ann = np.prod(1 + P / 100) ** (12 / 24) - 1
calmar = (100 * ann - 3.0) / abs(100 * mddP)
print(f"    annualised return {100 * ann:.4f}%, Calmar (rf 3%) {calmar:.4f}")

print("== part 4: Brinson attribution, one period and two")
w = np.array([0.40, 0.35, 0.25])
W = np.array([0.30, 0.40, 0.30])
r = np.array([6.0, 2.0, -1.0])
b = np.array([5.0, 3.0, -2.0])
Rp, Rb = w @ r, W @ b
A_bhb, S, I = (w - W) * b, W * (r - b), (w - W) * (r - b)
A_bf = (w - W) * (b - Rb)
ok("portfolio 2.85%, benchmark 2.10%, excess 0.75 points", close(Rp, 2.85) and close(Rb, 2.10))
ok(
    "BHB: allocation 0.45, selection 0.20, interaction 0.10, summing to 0.75",
    close(A_bhb.sum(), 0.45)
    and close(S.sum(), 0.20)
    and close(I.sum(), 0.10)
    and close(A_bhb.sum() + S.sum() + I.sum(), Rp - Rb),
)
ok(
    "Brinson-Fachler allocation by sector 0.29, -0.045, 0.205: same total 0.45, different signs and sizes",
    np.allclose(A_bf, [0.29, -0.045, 0.205]) and close(A_bf.sum(), A_bhb.sum()),
)
ok(
    "selection measured at portfolio weights, w(r - b) = 0.40, -0.35, 0.25, absorbs the interaction",
    np.allclose(w * (r - b), S + I),
)
w2 = np.array([0.38, 0.37, 0.25])
r2 = np.array([-2.0, 1.5, 3.0])
b2 = np.array([-3.0, 2.0, 2.5])
Rp2, Rb2 = w2 @ r2, W @ b2
Rtot = (1 + Rp / 100) * (1 + Rp2 / 100) - 1
Btot = (1 + Rb / 100) * (1 + Rb2 / 100) - 1
ok("period 2: 0.545% against 0.650% (excess -0.105)", close(Rp2, 0.545) and close(Rb2, 0.65))
ok(
    "the two arithmetic excesses sum to 0.6450 points, but the compounded excess is 0.6469",
    abs((Rp - Rb + Rp2 - Rb2) - 0.645) < 1e-12 and abs(100 * (Rtot - Btot) - 0.646883) < 1e-6,
)


def k(rr, bb):
    return (math.log(1 + rr) - math.log(1 + bb)) / (rr - bb) if rr != bb else 1 / (1 + rr)


K = k(Rtot, Btot)
k1, k2 = k(Rp / 100, Rb / 100), k(Rp2 / 100, Rb2 / 100)
effects1 = np.concatenate([A_bf, S, I])
A2, S2, I2 = (w2 - W) * (b2 - Rb2), W * (r2 - b2), (w2 - W) * (r2 - b2)
effects2 = np.concatenate([A2, S2, I2])
linked = (k1 * effects1 + k2 * effects2) / K
ok(
    "Carino-scaled effects sum exactly to the compounded excess",
    abs(linked.sum() - 100 * (Rtot - Btot)) < 1e-12,
)

print("== part 5: fixed-income attribution (weighted duration)")
wf, D, dy, c = (
    np.array([0.5, 0.5]),
    np.array([7.0, 5.0]),
    np.array([-0.20, -0.10]),
    np.array([0.30, 0.45]),
)
Wf, Db, dyb, cb = (
    np.array([0.6, 0.4]),
    np.array([6.0, 5.5]),
    np.array([-0.20, -0.05]),
    np.array([0.30, 0.42]),
)
ri, bi = c - D * dy, cb - Db * dyb
rP, rBf = wf @ ri, Wf @ bi
Dr, Dbb = wf @ D, Wf @ Db
Dbeta = Dr / Dbb
dyB = (Wf * Db * dyb).sum() / (Wf * Db).sum()
dur = (Dbeta - 1) * (Wf * Db * -dyb).sum()
alloc = (D * wf - Dbeta * Db * Wf) * (-dyb + dyB)
sel = D * wf * (-dy + dyb)
inc = wf @ c - Wf @ cb
print(
    f"    returns {ri} vs {bi}; P {rP:.4f} B {rBf:.4f}; duration {Dr} vs {Dbb}; effects dur {dur:.5f} alloc {alloc.sum():.5f} sel {sel.sum():.5f} income {inc:.5f}"
)
ok("portfolio 1.325%, benchmark 1.178%, excess 0.147", close(rP, 1.325) and close(rBf, 1.178))
ok(
    "duration 0.0286 + allocation -0.0336 + selection 0.1250 + income 0.0270 = 0.147",
    abs(dur - 0.028621) < 1e-6
    and abs(alloc.sum() + 0.033621) < 1e-6
    and close(sel.sum(), 0.125)
    and close(inc, 0.027)
    and close(dur + alloc.sum() + sel.sum() + inc, rP - rBf),
)
ok(
    "the Brinson-Fachler term sums to zero: sum(D w - Dbeta Db W) x dyB = 0",
    abs(((D * wf - Dbeta * Db * Wf) * dyB).sum()) < 1e-12,
)

print("== part 6: macro attribution, owner against managers (one month, no intra-month flows)")
V0 = 500.0  # millions
rf_m = 0.30
pol_cat = np.array([0.70, 0.30])  # equities, bonds
pol_mgr = [np.array([0.60, 0.40]), np.array([0.50, 0.50])]
cat_bench = np.array([2.40, 0.60])
mgr_bench = [np.array([2.90, 1.80]), np.array([0.70, 0.40])]
mgr_ret = [np.array([3.10, 1.50]), np.array([0.65, 0.55])]
act_w = [
    np.array([0.44, 0.28]),
    np.array([0.13, 0.15]),
]  # actual total-fund weights of the four managers
ok("actual weights sum to one", close(sum(x.sum() for x in act_w), 1.0))
lvl_rf = rf_m
lvl_cat = pol_cat @ cat_bench - rf_m
agg_bench = sum(pol_cat[i] * (pol_mgr[i] @ mgr_bench[i]) for i in range(2))
lvl_style = agg_bench - pol_cat @ cat_bench
agg_mgr = sum(pol_cat[i] * (pol_mgr[i] @ mgr_ret[i]) for i in range(2))
lvl_mgr = agg_mgr - agg_bench
actual = sum(act_w[i] @ mgr_ret[i] for i in range(2))
lvl_alloc = actual - agg_mgr
print(
    f"    rf {lvl_rf:.4f} category {lvl_cat:.4f} style/misfit {lvl_style:.4f} managers {lvl_mgr:.4f} allocation {lvl_alloc:.4f} total {actual:.4f}"
)
ok(
    "levels add to the fund's return",
    close(lvl_rf + lvl_cat + lvl_style + lvl_mgr + lvl_alloc, actual),
)
ok(
    "value metric: 500m x each level adds to the change in value",
    close(V0 * (lvl_rf + lvl_cat + lvl_style + lvl_mgr + lvl_alloc) / 100, V0 * actual / 100),
)

print("== part 7: benchmark quality statistics on 12 invented months")
M = np.array([1.5, -2.0, 3.0, 0.5, -1.0, 2.2, -0.8, 1.9, -2.5, 0.9, 1.4, -0.3])
Sty = np.array([0.4, -0.6, 0.2, 0.5, -0.3, 0.1, 0.6, -0.4, 0.3, -0.2, -0.5, 0.4])
Act = np.array([0.2, 0.1, -0.3, 0.3, 0.0, -0.2, 0.1, 0.2, -0.1, 0.3, -0.2, 0.1])
Bq = M + Sty
Pq2 = Bq + Act
E = Pq2 - M
beta_PB = np.cov(Pq2, Bq, ddof=1)[0, 1] / np.var(Bq, ddof=1)
rho_AS = np.corrcoef(Act, Sty)[0, 1]
rho_SE = np.corrcoef(Sty, E)[0, 1]
te_B, te_M = Act.std(ddof=1), E.std(ddof=1)
print(
    f"    beta(P on B) {beta_PB:.4f}, corr(A,S) {rho_AS:.4f}, corr(S,E) {rho_SE:.4f}, TE vs B {te_B:.4f}, vs M {te_M:.4f}"
)
ok(
    "good-benchmark signs: beta near 1, corr(A,S) near 0, corr(S,E) strongly positive, TE vs B < TE vs M",
    abs(beta_PB - 1) < 0.1 and abs(rho_AS) < 0.3 and rho_SE > 0.8 and te_B < te_M,
)
hold_p = {"a": 0.30, "b": 0.25, "c": 0.20, "d": 0.15, "x": 0.10}
hold_b = {"a": 0.20, "b": 0.20, "c": 0.25, "d": 0.10, "e": 0.25}
coverage = sum(v for n_, v in hold_p.items() if n_ in hold_b)
active = {n_: hold_p.get(n_, 0) - hold_b.get(n_, 0) for n_ in set(hold_p) | set(hold_b)}
ok("coverage ratio 90%: 10% of the portfolio is outside the benchmark", close(coverage, 0.90))
ok(
    "2 of 6 active positions negative (c and e); positive weight of active bets 0.30",
    sum(v < 0 for v in active.values()) == 2
    and close(sum(v for v in active.values() if v > 0), 0.30),
)

print("== part 8: skill against noise")
ir_grid = [0.20, 0.30, 0.40, 2 / 3, 0.80, 1.00]  # the exhibit's "0.67" column matches 2/3
years = [0.5, 1.0, 3.0, 5.0, 10.0, 20.0]
exhibit = [
    [55.63, 58.40, 61.14, 68.13, 71.42, 76.02],
    [57.93, 61.79, 65.54, 74.75, 78.81, 84.03],
    [63.81, 69.83, 75.58, 87.59, 91.71, 95.84],
    [67.26, 74.88, 81.45, 93.20, 96.32, 98.73],
    [73.65, 82.86, 89.70, 98.25, 99.43, 99.92],
    [81.70, 91.01, 96.32, 99.86, 99.98, 99.99],
]
model = [[100 * norm.cdf(ir * math.sqrt(T)) for ir in ir_grid] for T in years]
off = [
    (years[i], ir_grid[j])
    for i in range(6)
    for j in range(6)
    if abs(model[i][j] - exhibit[i][j]) > 0.011
]
print(f"    cells differing from Phi(IR sqrt(T)) by more than 0.01: {off}")
ok(
    "Exhibit 12-19 = Phi(IR sqrt(T)) in 33 of 36 cells; it prints 84.03 (IR 1.00, 1 year), 63.81 and 81.70 (IR 0.20, 3 and 20 years) for 84.13, 63.55 and 81.45",
    off == [(1.0, 1.0), (3.0, 0.20), (20.0, 0.20)]
    and abs(model[1][5] - 84.13) < 0.01
    and abs(model[2][0] - 63.55) < 0.01
    and abs(model[5][0] - 81.45) < 0.01,
)
p_under = 1 - norm.cdf(0.4 * math.sqrt(3))
printed_1220 = [6.10, 19.68, 28.59, 24.60, 13.90, 5.38, 1.45, 0.27, 0.03]
ok(
    "Exhibit 12-20 agrees with binomial(10, 0.2442) to within 0.05 points (6.08 for 6.10 at k = 0)",
    all(abs(100 * binom.pmf(kk, 10, p_under) - v) < 0.05 for kk, v in enumerate(printed_1220)),
)
power5 = norm.cdf(0.5 * math.sqrt(5) - norm.ppf(0.95))
yrs80 = ((norm.ppf(0.95) + norm.ppf(0.80)) / 0.5) ** 2
ok(
    "a true IR of 0.5 passes a 5% one-sided test in 5 years with probability 0.30; 80% power needs 24.7 years",
    abs(power5 - 0.2991) < 1e-3 and abs(yrs80 - 24.73) < 0.01,
)
t7 = 0.55 * math.sqrt(7)
ok(
    "an observed 7-year IR of 0.55 gives t = 1.455, one-sided p = 0.073: not significant at 5%",
    abs(t7 - 1.4552) < 1e-4 and abs(1 - norm.cdf(t7) - 0.0728) < 1e-3,
)

print()
if fails:
    print(f"{len(fails)} check(s) failed: {fails}")
    sys.exit(1)
print("all checks passed")
