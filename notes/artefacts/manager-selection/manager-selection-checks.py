"""Manager selection (2026-10-18): the worked numbers of meth:manager-due-diligence,
meth:vehicle-contract-fee-analysis and ex:manager-selection-case.

Part 1 computes three-year fees under an invented mandate (average assets 100 million each year, excess returns
gross of fees +4, -3 and +5 percent): an ad valorem fee, an asymmetric performance fee with a cumulative high-water
mark and a cap, and a fulcrum (symmetric) fee with a floor and a cap, then the expected incentive fee paid to a
manager with no skill. Part 1 also applies a high-water mark to Ang's NAV path 100, 120, 110, 145 (Asset Management,
2014, p. 582). Part 2 evaluates a manager-continuation rule as a filter, using Bailey, Richards and Tierney's three
manager types (+2, 0 and -1 percent a year; MIP 3rd ed., p. 781) with an assumed 5 percent tracking error and normal
returns. Part 3 is a returns-based style analysis (Sharpe 1992) on 36 invented months: weights minimise the variance
of the tracking difference, cross-checked by a centred quadratic form, the KKT conditions and shift invariance. Part 4
shrinks two invented track records' information ratios toward zero under a normal prior and shows how the ranking
depends on the assumed prior spread.

No random draws. Run: uv run --frozen --no-editable python manager-selection-checks.py   (numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import math
import sys

# third party library imports
import numpy as np
import scipy
from scipy.integrate import quad
from scipy.optimize import minimize
from scipy.stats import norm

print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
fails = []


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


print("== part 1: fee schedules (percent of average assets; excess returns gross of fees)")
excess = [4.0, -3.0, 5.0]
ad_valorem = [0.50] * 3


def asymmetric(xs, base=0.25, share=0.20, cap=1.25, hwm=True):
    fees, deficit = [], 0.0
    for x in xs:
        if hwm:
            eligible = max(0.0, x - deficit)
            deficit = max(0.0, deficit - x)
        else:
            eligible = max(0.0, x)
        fees.append(min(cap, base + share * eligible))
    return fees


def fulcrum(xs, base=0.50, share=0.10, floor=0.10, cap=0.90):
    return [min(cap, max(floor, base + share * x)) for x in xs]


fa = asymmetric(excess)
fa_nohwm = asymmetric(excess, hwm=False)
ff = fulcrum(excess)
print(f"    asymmetric with HWM {fa}, without HWM {fa_nohwm}, fulcrum {ff}")
ok(
    "asymmetric with HWM: 1.05, 0.25, 0.65 (year 3 pays only on the 2 points above the high-water mark)",
    np.allclose(fa, [1.05, 0.25, 0.65]),
)
ok(
    "without the HWM year 3 would pay 1.25 (the cap binds exactly)",
    np.allclose(fa_nohwm, [1.05, 0.25, 1.25]),
)
ok("fulcrum: 0.90 (capped), 0.20, 0.90 (capped)", np.allclose(ff, [0.90, 0.20, 0.90]))
ok(
    "three-year totals: ad valorem 1.50, asymmetric 1.95, fulcrum 2.00 points of assets",
    close(sum(ad_valorem), 1.5) and close(sum(fa), 1.95) and close(sum(ff), 2.00),
)
ok(
    "in currency on 100 million a year: 1.50, 1.95 and 2.00 million",
    close(sum(fa) * 100 / 100, 1.95),
)
ok(
    "share of the 6.0 points of cumulative excess paid away: 25%, 32.5%, 33.3%",
    close(sum(ad_valorem) / 6, 0.25)
    and close(sum(fa) / 6, 0.325)
    and abs(sum(ff) / 6 - 0.3333) < 1e-4,
)
# Expected fee for a manager with no skill: excess ~ N(0, 5^2), one year, no high-water mark carried in.
sig = 5.0
e_incentive_uncapped = 0.20 * sig / math.sqrt(2 * math.pi)
e_asym = quad(lambda x: min(1.25, 0.25 + 0.20 * max(0.0, x)) * norm.pdf(x, 0, sig), -60, 60)[0]
e_fulc = quad(lambda x: min(0.90, max(0.10, 0.50 + 0.10 * x)) * norm.pdf(x, 0, sig), -60, 60)[0]
ok(
    "zero-skill manager: expected uncapped incentive 0.20 x 5/sqrt(2 pi) = 0.399 points a year",
    abs(e_incentive_uncapped - 0.39894) < 1e-5,
)
ok(
    "expected asymmetric fee 0.566 (0.649 before the cap) against a base of 0.25; the fulcrum fee expects exactly its 0.50",
    abs(e_asym - 0.56563) < 1e-5 and abs(e_fulc - 0.50) < 1e-9,
)
navs = [100.0, 120.0, 110.0, 145.0]
hw, inc = navs[0], []
for v in navs[1:]:
    inc.append(0.20 * max(0.0, v - hw))
    hw = max(hw, v)
ok(
    "Ang's NAV path: incentive 4.0 at time 2, nothing at time 3 (below 120), 5.0 at time 4 on 145 - 120",
    np.allclose(inc, [4.0, 0.0, 5.0]),
)

print("== part 2: a continuation rule as a statistical filter")
types = {
    "positive": (2.0, 0.4),
    "zero": (0.0, 0.4),
    "negative": (-1.0, 0.2),
}  # value added, prior share
te, yrs = 5.0, 5
for cut in (0.0, 1.645):
    keep = {k: 1 - norm.cdf(cut - (va / te) * math.sqrt(yrs)) for k, (va, _) in types.items()}
    kept = sum(types[k][1] * keep[k] for k in types)
    va_kept = sum(types[k][1] * keep[k] * types[k][0] for k in types) / kept
    type1 = (types["zero"][1] * keep["zero"] + types["negative"][1] * keep["negative"]) / (
        types["zero"][1] + types["negative"][1]
    )
    type2 = 1 - keep["positive"]
    print(
        f"    keep if 5-year t > {cut}: keep probs {dict((k, round(v, 4)) for k, v in keep.items())}, kept value added {va_kept:.4f}, type I {type1:.4f}, type II {type2:.4f}"
    )
    if cut == 0.0:
        ok(
            "keep-if-ahead rule: keeps 81.4% of positive, 50% of zero, 32.7% of negative managers; Type II 18.6%",
            abs(keep["positive"] - 0.8145) < 1e-4
            and close(keep["zero"], 0.5)
            and abs(keep["negative"] - 0.3274) < 1e-4,
        )
        va0 = va_kept
    else:
        ok(
            "5% significance rule: keeps only 22.6% of positive managers (Type II 77.4%) but cuts Type I to 3.9%",
            abs(keep["positive"] - 0.22645) < 1e-5 and abs(type1 - 0.0394) < 1e-4,
        )
        ok(
            "the stricter rule raises the expected value added of those kept (1.55 against 0.99 points) but keeps far fewer",
            va_kept > va0 and abs(va_kept - 1.5542) < 1e-4 and abs(va0 - 0.9913) < 1e-4,
        )
ok(
    "pool expectation before any filter: 0.4 x 2 + 0.4 x 0 + 0.2 x (-1) = 0.6 points (Bailey et al.)",
    close(sum(v * p for v, p in types.values()), 0.6),
)

print("== part 3: returns-based style analysis on 36 invented months")
t = np.arange(36)
mkt = 0.8 + 3.0 * np.sin(0.7 * t)
lg = mkt + 1.2 * np.sin(1.3 * t + 0.5)
lv = mkt - 1.0 * np.sin(1.3 * t + 0.5) + 0.4 * np.cos(0.4 * t)
sg = 1.3 * mkt + 1.5 * np.cos(0.9 * t)
sv = 1.1 * mkt - 0.8 * np.cos(0.9 * t) + 0.9 * np.sin(2.1 * t)
cash = np.full(36, 0.3)
X = np.column_stack([lg, lv, sg, sv, cash])
sel = 0.35 * np.sin(
    2.9 * t + 1.0
)  # selection return: mean ~0, uncorrelated by construction with slow styles
true_w = np.array([0.0, 0.55, 0.0, 0.30, 0.15])
fund = X @ true_w + sel
ols = np.linalg.lstsq(np.column_stack([np.ones(36), X[:, :4]]), fund, rcond=None)[0]
cons = [{"type": "eq", "fun": lambda wv: wv.sum() - 1}]


def style_fit(objective):
    r = minimize(
        objective,
        np.full(5, 0.2),
        method="SLSQP",
        bounds=[(0, 1)] * 5,
        constraints=cons,
        options={"ftol": 1e-15, "maxiter": 1000},
    )
    return r


# Sharpe (1992): minimise the variance of the tracking difference fund - X w, not its mean or mean square.
res = style_fit(lambda wv: (fund - X @ wv).var())
w_hat = res.x
track = fund - X @ w_hat
r2 = 1 - track.var() / fund.var()
print(
    f"    style weights {np.round(100 * w_hat, 4)} percent, residual variance {track.var():.8f}, R^2 {r2:.4f}; "
    f"unconstrained slopes {np.round(ols[1:], 3)}"
)
ok(
    "constrained style weights are nonnegative and sum to one",
    res.success and np.all(w_hat >= -1e-9) and abs(w_hat.sum() - 1) < 1e-9,
)
ok(
    "weights 1.37, 56.60, 0, 27.13 and 14.90 percent; residual variance 0.05587; R^2 0.986",
    np.allclose(100 * w_hat, [1.3745, 56.6014, 0.0, 27.1260, 14.8981], atol=2e-4)
    and abs(track.var() - 0.05586964) < 1e-8
    and abs(r2 - 0.98568) < 1e-5,
)
# Independent formulation: the same objective written as a quadratic form in centred data,
# w'Qw - 2c'w + const with Q = cov(X), c = cov(X, fund) (divisor n).
Xc, fc = X - X.mean(axis=0), fund - fund.mean()
Q, c = Xc.T @ Xc / 36, Xc.T @ fc / 36
res_q = style_fit(lambda wv: wv @ Q @ wv - 2 * c @ wv + fc @ fc / 36)
ok(
    "the centred quadratic form gives the same weights and the same minimum",
    np.allclose(res_q.x, w_hat, atol=1e-6)
    and abs(res_q.fun - track.var()) < 1e-10
    and abs(res_q.fun - (fund - X @ res_q.x).var()) < 1e-12,
)
# Optimality certificate (KKT) for this convex problem: with gradient g = 2(Qw - c), every weight held at a positive
# level has the same g_i (the multiplier of the budget constraint) and every weight at zero has g_i at least as large.
g = 2 * (Q @ w_hat - c)
held = w_hat > 1e-6
lam = g[held].mean()
ok(
    "KKT conditions hold: equal gradients on held styles, larger on the excluded small-growth style",
    np.ptp(g[held]) < 1e-6 and np.all(g[~held] >= lam - 1e-9),
    f"multiplier {lam:.6f}, small growth {g[2]:.6f}",
)
shift = 2.0
w_shift = style_fit(lambda wv: (fund + shift - X @ wv).var()).x
ok(
    "adding 2 points to every fund return leaves the weights unchanged (only the mean tracking difference moves)",
    np.allclose(w_shift, w_hat, atol=1e-6),
)
# The mean-square objective ((fund - X w)^2) is not Sharpe's: it penalises the mean difference, so its solution
# moves when a constant is added and its tracking variance is higher than the minimum.
res_ms = style_fit(lambda wv: ((fund - X @ wv) ** 2).mean())
res_ms_shift = style_fit(lambda wv: ((fund + shift - X @ wv) ** 2).mean())
ok(
    "by contrast the mean-square objective is not shift-invariant and does not minimise tracking variance",
    not np.allclose(res_ms.x, res_ms_shift.x, atol=1e-3)
    and (fund - X @ res_ms.x).var() > track.var() + 1e-6,
)
ok(
    "style recovered within 3 points of the 0/55/0/30/15 construction (consistent, not proof of the objective)",
    np.allclose(w_hat, true_w, atol=0.03),
)
ok("style explains over 98% of return variance; 1 - R^2 is attributed to selection", r2 > 0.98)
ok(
    "mean tracking difference 0.0096 stays near the built-in selection mean 0.0091",
    abs(track.mean() - sel.mean()) < 0.001,
)

print("== part 4: shrinking information ratios toward zero")
cands = {"X": (0.62, 9), "Y": (1.10, 3)}  # sampling se of an annual IR estimate ~ 1/sqrt(years)


def posterior_ir(ir, n, tau):
    """Posterior mean of the true IR under a normal prior N(0, tau^2) and estimate ~ N(true, 1/n)."""
    return ir * tau**2 / (tau**2 + 1 / n)


tstat = {k: ir * math.sqrt(n) for k, (ir, n) in cands.items()}
for tau in (0.30, 0.50):
    print(
        f"    prior sd {tau}: "
        + ", ".join(f"{k} {posterior_ir(ir, n, tau):.5f}" for k, (ir, n) in cands.items())
    )
ok(
    "raw IR ranks Y first (1.10 against 0.62); t-statistics are close (1.905 against 1.860)",
    abs(tstat["Y"] - 1.9053) < 1e-4 and abs(tstat["X"] - 1.86) < 1e-9,
)
px30, py30 = posterior_ir(0.62, 9, 0.30), posterior_ir(1.10, 3, 0.30)
px50, py50 = posterior_ir(0.62, 9, 0.50), posterior_ir(1.10, 3, 0.50)
ok(
    "prior sd 0.30: posterior means reverse the raw ranking, X 0.27746 against Y 0.23386",
    abs(px30 - 0.277459) < 1e-6 and abs(py30 - 0.233858) < 1e-6 and px30 > py30,
)
ok(
    "prior sd 0.50: the ranking flips back, X 0.42923 against Y 0.47143",
    abs(px50 - 0.429231) < 1e-6 and abs(py50 - 0.471429) < 1e-6 and py50 > px50,
)
# Crossover: 0.62/(tau^2 + 1/9) = 1.10/(tau^2 + 1/3), so tau^2 = (0.62/3 - 1.10/9)/(1.10 - 0.62).
tau_star = math.sqrt((0.62 / 3 - 1.10 / 9) / (1.10 - 0.62))
ok(
    "the posterior ranking changes at a prior sd of 0.419; X ranks first only below it",
    abs(tau_star - 0.41944) < 1e-5
    and abs(posterior_ir(0.62, 9, tau_star) - posterior_ir(1.10, 3, tau_star)) < 1e-12
    and posterior_ir(0.62, 9, 0.41) > posterior_ir(1.10, 3, 0.41)
    and posterior_ir(0.62, 9, 0.43) < posterior_ir(1.10, 3, 0.43),
)

print()
if fails:
    print(f"{len(fails)} check(s) failed: {fails}")
    sys.exit(1)
print("all checks passed")
