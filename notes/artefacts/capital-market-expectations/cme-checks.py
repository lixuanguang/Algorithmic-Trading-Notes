"""Capital market expectations (2026-10-19): the worked numbers of meth:cme-framework-forecasting,
meth:growth-shocks-long-run-expectations, meth:cycle-policy-curve-expectations, meth:asset-class-return-forecasts,
meth:fx-volatility-forecasts and ex:global-portfolio-macro-rebalancing.

Reproduced from Portfolio Management in Practice, Volume 1 (CFA Institute Investment Series, 2020), chaps. 3-4:
the regime example (Example 7, p. 65: expansions of 39 months, contractions of 20, +2%/-2% a month, long-run 8% a
year); long-run equity returns and growth (Example 5, pp. 55-56: baseline 6.75%, P/E effect 51.3% cumulative, -1.71% a
year over 30 years); yield-to-maturity forecasts with rising yields (Example 1, pp. 97-98: -1.09%, 2.71%, 3.44%);
Grinold-Kroner (Example 4, pp. 109-110: 9.5%, long run 7.25%; P/E from 16 to 20 at 4.56%, 2.26%, 0.75% a year over 5,
10, 30 years); Singer-Terhaar for German equities and bonds (p. 114: 3.57/1.05, 5.95/1.75, 3.93/1.16, 6.93%/4.16%);
smoothing (eq. 16, p. 135: lambda 0.8 gives 9 times the variance); and the ARCH update (eq. 17, p. 137: 2.0833% and
1.9849%). Original: sampling error of a historical mean; the three types of growth shock; a Markov regime forecast
computed exactly; the real-estate return equation; a shrinkage covariance estimate against the sample estimate on
simulated data; an exchange-rate forecast combining PPP, UIP and current-account views; and a global reweighting
whose quantified views raise the expected return per unit of risk.

Count convention: one check is one executed ok() call (a call inside a loop counts once per iteration).

Run: uv run python cme-checks.py   (numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import math
import sys

# third party library imports
import numpy as np
import scipy

print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
fails = []


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


print("== part 1: framework and forecasting challenges")
sigma, years = 0.16, 60
ok(
    "a historical mean from 60 years of 16%-volatility returns has a standard error of 2.07 points: a 95% interval of"
    " about +-4 points around the estimate",
    abs(sigma / math.sqrt(years) - 0.02066) < 1e-5,
)
lam = 0.8
ok(
    "smoothing (PMiP eq. 16): with R_t = (1 - lambda) r_t + lambda R_{t-1} and lambda = 0.8, true variance is (1 + 0.8)/"
    "(1 - 0.8) = 9 times observed, so true volatility is 3 times the appraisal-based figure",
    close((1 + lam) / (1 - lam), 9.0, 1e-12),
)
rng = np.random.default_rng(20261019)
true_r = rng.normal(0.0, 0.10, 200_000)
obs = np.empty_like(true_r)
obs[0] = true_r[0]
for t in range(1, len(true_r)):
    obs[t] = (1 - lam) * true_r[t] + lam * obs[t - 1]
ok(
    "simulated: smoothing the true series with lambda 0.8 cuts its measured variance to 1/9 (within 3%)",
    abs(np.var(true_r) / np.var(obs) / 9 - 1) < 0.03,
    f"ratio {np.var(true_r) / np.var(obs):.3f}",
)

print("== part 2: growth trends and exogenous shocks in long-run expectations")
base = 0.009 + 0.015 + 0.021 + 0.0225
ok(
    "Example 5: labour input 0.9%, productivity 1.5%, inflation 2.1%, dividend yield 2.25% give a 6.75% baseline;"
    " a P/E adding 0.95% for 54 years leaves 51.3% (1.67 times) above fair value, -1.71% a year if unwound over 30"
    " years and -10.26% over 5 (to -3.51%)",
    close(base, 0.0675, 1e-12)
    and close(54 * 0.0095, 0.513, 1e-9)
    and abs(math.exp(0.513) - 1.67) < 0.005
    and abs(0.513 / 30 - 0.0171) < 1e-4
    and close(base - 0.513 / 5, -0.0351, 1e-9),
)
g, t10 = 0.02, 10
type1 = 0.95 * (1 + g) ** t10
type2 = (1 + 0.015) ** t10
type3 = 0.95 * (1 + 0.015) ** t10
ok(
    "shocks over 10 years from a 2% trend: a 5% level loss (type 1) leaves output at 1.158; a growth cut to 1.5% (type"
    " 2) at 1.161 and widening; both (type 3) at 1.103 against 1.219 without the shock",
    abs(type1 - 1.1580) < 1e-3 and abs(type2 - 1.1605) < 1e-3 and abs(type3 - 1.1025) < 1e-3,
)

print("== part 3: the cycle, policy and the yield curve")
p_ee, p_cc = 1 - 1 / 39, 1 - 1 / 20  # monthly persistence: expected durations 39 and 20 months
P = np.array([[p_ee, 1 - p_ee], [1 - p_cc, p_cc]])
mu = np.array([0.02, -0.02])
stationary = np.linalg.lstsq(
    np.vstack([P.T - np.eye(2), np.ones(2)]), np.array([0.0, 0.0, 1.0]), rcond=None
)[0]
ok(
    "Example 7: expected spells of 39 and 20 months put the economy in expansion 66.1% of the time; the unconditional"
    " return is 0.645% a month, about 8% a year (the text rounds to two-thirds and 0.67%)",
    abs(stationary[0] - 39 / 59) < 1e-12 and abs(stationary @ mu - 0.006441) < 1e-6,
)


def horizon_return(months, start=1):
    state = np.eye(2)[start]
    total = 0.0
    for _ in range(months):
        total += state @ mu
        state = state @ P
    return total


r3, r12, r60, r120 = (horizon_return(m) for m in (3, 12, 60, 120))
ok(
    "starting in contraction, the exact chain gives -5.4% over 3 months, -13.6% over 1 year, 0.8% a year over 5 years"
    " and 4.2% a year over 10: the longer the horizon, the closer to the unconditional mean; the text's judgemental"
    " -6%, -18%, 4.8% and ~8% have the same shape but converge faster than the chain implies",
    abs(r3 + 0.0542) < 5e-4
    and abs(r12 + 0.1362) < 5e-4
    and abs(r60 / 5 - 0.0080) < 5e-4
    and abs(r120 / 10 - 0.0423) < 5e-4
    and r3 / 3 < r12 / 12 < r60 / 60 < r120 / 120 < stationary @ mu,
    f"{r3:.4f} {r12:.4f} {r60 / 5:.4f} {r120 / 10:.4f}",
)
trade_share, elasticity, shock = 0.25, 0.8, -0.04
ok(
    "cross-economy linkage: if exports to a partner are 25% of GDP and respond with elasticity 0.8 to its 4% fall in"
    " demand, the exporter's GDP falls by 0.8% before second-round effects",
    close(trade_share * elasticity * shock, -0.008, 1e-12),
)

print("== part 4: fixed income, equities and real estate")
dur, ytm, dy = 4.84, 0.0325, 0.02
loss = dur * dy
r2 = ytm + (-loss + 0.010) / 2
r5 = ytm + (-loss + 0.010 + 0.060) / 5
r7 = ytm + (-loss + 0.010 + 0.060 + 0.040) / 7
ok(
    "Example 1: modified duration 4.84, YTM 3.25%, yields +200 bp over two years: about -1.09% a year over 2 years,"
    " 2.71% over 5 and 3.44% over 7; Macaulay duration is 5.0",
    abs(r2 + 0.0109) < 5e-5
    and abs(r5 - 0.0271) < 5e-5
    and abs(r7 - 0.0344) < 5e-5
    and abs(dur * (1 + ytm) - 5.0) < 0.005,
)
ok(
    "building blocks: short default-free rate 2.0% + term premium 1.0% + credit premium 1.2% + liquidity premium 0.3% ="
    " 4.5% for an investment-grade corporate bond fund",
    close(0.020 + 0.010 + 0.012 + 0.003, 0.045, 1e-12),
)
gk = 0.0225 + (0.06 - (-0.01)) + 0.0025
ok(
    "Example 4 (Grinold-Kroner): 2.25% yield + (6% earnings growth + 1% net buybacks) + 0.25% P/E expansion = 9.5%; the"
    " sustainable long-run figure is 7.25% (yield + nominal GDP growth)",
    close(gk, 0.095, 1e-12) and close(0.0225 + 0.05, 0.0725, 1e-12),
)
pe_rates = {n: (20 / 16) ** (1 / n) - 1 for n in (5, 10, 30)}
ok(
    "a P/E reverting from 16 to 20 implies 4.56% a year over 5 years, 2.26% over 10 and 0.75% over 30: horizon-specific"
    " growth rates must not be extrapolated",
    abs(pe_rates[5] - 0.0456) < 5e-5
    and abs(pe_rates[10] - 0.0226) < 5e-5
    and abs(pe_rates[30] - 0.0075) < 5e-5,
)
sr_g = 0.30
rp_g = {"equity": 0.70 * 0.17 * sr_g, "bond": 0.50 * 0.07 * sr_g}
rp_s = {"equity": 0.17 * 0.35, "bond": 0.07 * 0.25}
rp = {k: 0.85 * rp_g[k] + 0.15 * rp_s[k] for k in rp_g}
ok(
    "Singer-Terhaar (German assets): integrated premia 3.57% and 1.05%, segmented 5.95% and 1.75%, at 85% integration"
    " 3.93% and 1.16%; with a 3% risk-free rate, 6.93% and 4.16%",
    round(rp_g["equity"], 4) == 0.0357
    and round(rp_g["bond"], 4) == 0.0105
    and round(rp["equity"], 4) == 0.0393
    and round(rp["bond"], 4) == 0.0116
    and round(0.03 + rp["equity"], 4) == 0.0693
    and round(0.03 + rp["bond"], 4) == 0.0416,
)
ok(
    "real estate (eq. 8): cap rate 5.0% + NOI growth 2.5% - expected 0.3%/year rise in the cap rate gives about 7.2%",
    close(0.05 + 0.025 - 0.003, 0.072, 1e-12),
)

print("== part 5: exchange rates and volatility")
gam, alpha_, beta_ = 0.000002, 0.9, 0.08
var_prev = 0.0004
var_t = gam + alpha_ * var_prev + beta_ * 0.03**2
var_alt = gam + alpha_ * var_prev + beta_ * 0.02**2
ok(
    "ARCH (eq. 17): gamma 0.000002, persistence 0.9, shock weight 0.08; long-run variance 0.0001 (1% a day); from"
    " 0.0004 a 3% surprise gives 2.0833% and a 2% surprise 1.9849%",
    close(gam / (1 - alpha_ - beta_), 0.0001, 1e-15)
    and abs(math.sqrt(var_t) - 0.020833) < 1e-6
    and abs(math.sqrt(var_alt) - 0.019849) < 1e-6,
)
n_assets, n_obs = 10, 60
true_corr = 0.5
true_cov = (np.full((n_assets, n_assets), true_corr) + (1 - true_corr) * np.eye(n_assets)) * 0.04
err_sample, err_shrunk = [], []
for _ in range(300):
    x = rng.multivariate_normal(np.zeros(n_assets), true_cov, n_obs)
    s = np.cov(x, rowvar=False)
    vols = np.sqrt(np.diag(s))
    rbar = (s / np.outer(vols, vols))[~np.eye(n_assets, dtype=bool)].mean()
    target = rbar * np.outer(vols, vols)
    np.fill_diagonal(target, np.diag(s))
    shrunk = 0.5 * s + 0.5 * target
    err_sample.append(np.sum((s - true_cov) ** 2))
    err_shrunk.append(np.sum((shrunk - true_cov) ** 2))
ok(
    "shrinkage: with 10 assets and 60 observations, averaging the sample covariance with a constant-correlation target"
    " (weight 0.5) cuts the mean squared estimation error versus the true matrix",
    np.mean(err_shrunk) < np.mean(err_sample),
    f"MSE ratio {np.mean(err_shrunk) / np.mean(err_sample):.3f}",
)
ppp_view = 0.02 - 0.035  # inflation 2% at home, 3.5% abroad: foreign currency falls 1.5%/yr (d/f)
uip_view = 0.04 - 0.055  # interest differential implies the same direction
ca_view = -0.01  # widening foreign deficit: extra 1% pressure
ok(
    "an exchange-rate view combining relative PPP (-1.5% a year for the foreign currency), the interest differential"
    " (-1.5%) and a current-account adjustment (-1%) gives -2.5% if the first two are treated as one anchor, not -4%:"
    " the two parity views share the inflation differential",
    close(ppp_view, uip_view, 1e-12)
    and close(0.5 * (ppp_view + uip_view) + ca_view, -0.025, 1e-12),
)

print("== part 6: reweighting a global portfolio on macro views")
er = np.array(
    [0.075, 0.055, 0.035, 0.040]
)  # equity A (near trough), equity B (near peak), bonds A, bonds B
vol = np.array([0.18, 0.16, 0.06, 0.05])
corr = np.array(
    [[1, 0.7, -0.1, 0.0], [0.7, 1, 0.0, -0.1], [-0.1, 0.0, 1, 0.6], [0.0, -0.1, 0.6, 1]]
)
cov = np.outer(vol, vol) * corr
w0 = np.array([0.30, 0.30, 0.20, 0.20])
w1 = np.array([0.38, 0.24, 0.18, 0.20])  # equities from B to A, a little less bond A
sr = lambda w: (w @ er - 0.02) / math.sqrt(w @ cov @ w)
ok(
    "macro views (A near its trough: higher expected equity return; B near its peak) moving 8 points of equity from B to"
    " A and 2 points out of A bonds raise expected return from 5.40% to 5.60% and the ratio of excess return to risk",
    abs(w0 @ er - 0.0540) < 1e-12
    and abs(w1 @ er - 0.0560) < 1e-12
    and sr(w1) > sr(w0)
    and close(w1.sum(), 1.0),
    f"Sharpe {sr(w0):.3f} -> {sr(w1):.3f}",
)

print()
if fails:
    print(f"{len(fails)} check(s) failed: {fails}")
    sys.exit(1)
print("all checks passed")
