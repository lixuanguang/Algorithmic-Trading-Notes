"""Strategic asset allocation (2026-10-19): the worked numbers of meth:economic-balance-sheet-allocation,
def:allocation-approaches-risk, meth:asset-class-factor-specification, meth:asset-only-allocation-mvo,
meth:allocation-implementation-rebalancing, meth:allocation-robustness-liquidity-risk-budget,
meth:liability-relative-allocation, meth:goals-based-allocation-heuristics, meth:allocation-constraints-taxes-revision
and meth:tactical-shifts-behavioural-biases.

Reproduced from Portfolio Management in Practice, Volume 1 (CFA Institute Investment Series, 2020), chaps. 5-7: the
utility U = E(R) - 0.005 lambda sigma^2 (6% at 10%, lambda 2, 20% volatility; chap. 6, eq. 1, p. 213); reverse-
optimised expected returns 2.5% + beta x 4% (Exhibit 12, p. 232); the equal ratio of excess return to marginal
contribution to risk at the Sharpe-maximising mix (Exhibit 19, p. 244); minimum-expectation returns of goals-based
modules (Exhibit 36, p. 273) and the Smiths' required capital for two goals (pp. 274-275: 6,671 and 2,679 thousand,
which need unrounded rates of about 4.13% and 6.81%); after-tax returns 1.8% and 6% (chap. 7, eqs. 1-3, pp. 328-329).
Ang, Asset Management (2014), chap. 4, pp. 135-140: rebalancing is short volatility. Original: an economic balance sheet
with human capital and a glide path; asset-only, surplus and shortfall risk of one portfolio; unconstrained mean-
variance weights from reverse-optimised returns; input sensitivity; a constrained optimum; a two-period binomial in
which the rebalanced portfolio is a buy-and-hold portfolio short volatility; a corridor; Monte Carlo success rates
for a spending plan; the denominator effect on illiquid weights; risk budgets; surplus optimisation and a hedging/
return-seeking split; heuristics (120 minus age, 60/40, 1/N, risk parity); a size constraint; revising an allocation
after a funding change; and a tactical tilt judged by its information ratio.

Count convention: one check is one executed ok() call (a call inside a loop counts once per iteration).

Run: uv run --frozen --no-editable python saa-checks.py   (numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import math
import sys

# third party library imports
import numpy as np
import scipy
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


print("== part 1: the economic balance sheet")


def equity_weight_financial(fin, hc, target=0.45, hc_equity=0.30):
    """Equity share of financial assets so that total wealth (financial + human capital) is `target` equity."""
    return (target * (fin + hc) - hc_equity * hc) / fin


w35 = equity_weight_financial(400_000, 1_000_000)
w55 = equity_weight_financial(1_200_000, 300_000)
ok(
    "human capital 30% equity-like (PMiP p. 167): a 45% equity target for total wealth means 82.5% equities in the"
    " financial portfolio at 35 (400k financial, 1.0m human capital) and 48.75% at 55 (1.2m, 0.3m): a glide path",
    abs(w35 - 0.825) < 1e-12 and abs(w55 - 0.4875) < 1e-12 and w35 > w55,
)
w_risky_job = equity_weight_financial(400_000, 1_000_000, hc_equity=0.60)
ok(
    "if the client's earnings are equity-like (60%, e.g. in finance) the same target needs only 7.5% equities in the"
    " financial portfolio: the economic balance sheet changes the answer",
    abs(w_risky_job - 0.075) < 1e-12,
)

print("== part 2: asset-only, liability-relative and goals-based risk")
mu_p, sd_p = 0.065, 0.11
assets, liab, corr_al, sd_l, mu_l = 1.10, 1.00, 0.35, 0.10, 0.045
surplus_mu = (assets * mu_p - liab * mu_l) / assets
surplus_sd = (
    math.sqrt((assets * sd_p) ** 2 + (liab * sd_l) ** 2 - 2 * corr_al * assets * sd_p * liab * sd_l)
    / assets
)
p_short = norm.cdf((0.03 - mu_p) / (sd_p / math.sqrt(10)))
ok(
    "one portfolio (6.5%, 11% volatility), three risk measures: asset volatility 11%; surplus volatility 11.6% of"
    " assets against liabilities of 10% volatility with correlation 0.35 (funding 110%); and a 15.6% chance that the"
    " 10-year annualised return falls short of a 3% goal",
    abs(surplus_sd - 0.11561) < 1e-4
    and abs(p_short - 0.1572) < 1e-3
    and abs(surplus_mu - 0.024091) < 1e-5,
    f"surplus sd {surplus_sd:.4%}, shortfall {p_short:.4f}",
)

print("== part 3: asset classes, factors and the global market portfolio")
beta = {
    "UK large cap": 1.03,
    "UK mid cap": 1.11,
    "Japan equities": 0.98,
    "Global ex UK bonds": 0.39,
    "Cash": 0.0,
}
printed = {
    "UK large cap": 6.62,
    "UK mid cap": 6.92,
    "Japan equities": 6.43,
    "Global ex UK bonds": 4.05,
    "Cash": 2.50,
}
ok(
    "reverse optimisation (Exhibit 12): E[R] = 2.5% + beta x 4% reproduces the printed returns to within 0.02 point"
    " for these rows (others differ slightly because betas are rounded, as the text notes)",
    all(abs(2.5 + 4 * b - printed[k]) < 0.021 for k, b in beta.items()),
)
loadings = np.array(
    [[1.0, 0.0], [0.9, 0.4], [0.2, 0.0]]
)  # equity, credit and bond exposures to (growth, credit)
fvol = np.diag([0.16, 0.06]) ** 2
cov_f = loadings @ fvol @ loadings.T + np.diag([0.02, 0.03, 0.03]) ** 2
corr_ec = cov_f[0, 1] / math.sqrt(cov_f[0, 0] * cov_f[1, 1])
ok(
    "factor view: if high-yield credit loads 0.9 on the equity (growth) factor, its correlation with equities is"
    " 0.96: two 'asset classes' can be largely one risk",
    abs(corr_ec - 0.9587) < 1e-3,
    f"{corr_ec:.4f}",
)

print("== part 4: asset-only mean-variance allocation")
ok(
    "PMiP eq. (1): U = 10% - 0.005 x 2 x 20^2 = 6%, a certainty-equivalent return",
    close(10 - 0.005 * 2 * 20**2, 6.0, 1e-12),
)
vol = np.array([0.16, 0.18, 0.06, 0.01])
corr = np.array([[1, 0.75, 0.2, 0], [0.75, 1, 0.15, 0], [0.2, 0.15, 1, 0.1], [0, 0, 0.1, 1]])
cov = np.outer(vol, vol) * corr
w_mkt = np.array([0.45, 0.20, 0.30, 0.05])
lam_mkt = 3.0
pi = lam_mkt * cov @ w_mkt  # implied excess returns
w_back = np.linalg.solve(lam_mkt * cov, pi)
ok(
    "reverse optimisation round trip: implied excess returns pi = lambda Sigma w_mkt, fed back into the unconstrained"
    " optimiser, return exactly the market weights",
    np.allclose(w_back, w_mkt, atol=1e-12),
    " ".join(f"{x:.3%}" for x in pi),
)
pi_bumped = pi + np.array([0.0, 0.005, 0.0, 0.0])
w_bumped = np.linalg.solve(lam_mkt * cov, pi_bumped)
ok(
    "input sensitivity: raising one equity class's expected return by 0.5 point moves its unconstrained weight from"
    " 20% to 31.8% and cuts the other equity class from 45% to 35.1%: MVO amplifies small input changes",
    abs(w_bumped[1] - 0.318) < 1e-3 and abs(w_bumped[0] - 0.351) < 1e-3,
    " ".join(f"{x:.1%}" for x in w_bumped),
)


def mvo(mu, lam, cap=1.0):
    obj = lambda w: -(w @ mu - 0.5 * lam * w @ cov @ w)
    cons = [{"type": "eq", "fun": lambda w: w.sum() - 1}]
    r = minimize(obj, np.full(4, 0.25), bounds=[(0, cap)] * 4, constraints=cons, method="SLSQP")
    return r.x


w_lo, w_hi = mvo(pi + 0.02, 2.0), mvo(pi + 0.02, 8.0)
ok(
    "budget and no-short constraints: a less risk-averse investor (lambda 2) holds more equity than a more risk-averse"
    " one (lambda 8), and both portfolios are fully invested and long-only",
    w_lo[:2].sum() > w_hi[:2].sum() and close(w_lo.sum(), 1, 1e-6) and w_hi.min() > -1e-9,
    f"equity {w_lo[:2].sum():.1%} vs {w_hi[:2].sum():.1%}",
)

print("== part 5: implementation and rebalancing")
s0, up, down, rf = 1.0, 1.25, 0.80, 0.0
paths = {"uu": up * up, "ud": up * down, "du": down * up, "dd": down * down}


def rebalanced(path):
    w = 1.0
    for step in path:
        w = w * (0.5 * (up if step == "u" else down) + 0.5)
    return w


bh = {k: 0.5 * v + 0.5 for k, v in paths.items()}
rb = {k: rebalanced(k) for k in paths}
ok(
    "two periods, 50/50 stock and cash, stock up 25% or down 20%: rebalancing beats buy-and-hold when the stock"
    " reverses (1.0125 against 1.0) and lags after two moves in the same direction (1.2656 against 1.2813; 0.81 against"
    " 0.82): a concave, short-volatility payoff (Ang chap. 4)",
    rb["ud"] > bh["ud"]
    and rb["uu"] < bh["uu"]
    and rb["dd"] < bh["dd"]
    and abs(rb["ud"] - 1.0125) < 1e-12,
    " ".join(f"{k} {rb[k]:.4f}/{bh[k]:.4f}" for k in paths),
)
target, band = 0.60, 0.05
drift = 0.60 * 1.12 / (0.60 * 1.12 + 0.40 * 0.99)
ok(
    "a corridor of +-5 points around a 60% equity target: equities up 12% and bonds down 1% take the weight to 62.9%,"
    " inside the band, so no trade; a further 8% equity rise to 64.7% stays inside, 66%+ would trigger",
    target - band < drift < target + band
    and abs(drift - 0.6292) < 1e-4
    and 0.60 * 1.12 * 1.08 / (0.60 * 1.12 * 1.08 + 0.40 * 0.99) < 0.65,
)

print("== part 6: robustness, liquidity and risk budgets")
rng = np.random.default_rng(20261019)
n_paths, years = 20_000, 30
rets = rng.normal(0.055, 0.11, (n_paths, years))
wealth = np.full(n_paths, 1_000_000.0)
alive = np.ones(n_paths, bool)
for t in range(years):
    wealth = wealth * (1 + rets[:, t]) - 50_000 * 1.02**t
    alive &= wealth > 0
    wealth = np.maximum(wealth, 0)
ok(
    "Monte Carlo: 1m spending 50k a year rising with 2% inflation, 5.5% mean and 11% volatility: about 52% of 30-year"
    " paths never run out; a mean-return projection alone would suggest the plan works",
    abs(alive.mean() - 0.52) < 0.02,
    f"success {alive.mean():.3f}",
)
illiq0 = 0.20
illiq_after = illiq0 / (illiq0 + 0.80 * (1 - 0.30))
ok(
    "denominator effect: a 20% private-asset allocation becomes 26.3% after a 30% fall in public assets with private"
    " valuations unchanged, breaching a 25% cap without any purchase",
    abs(illiq_after - 0.2632) < 1e-4,
)
mu_ex = np.array([0.050, 0.055, 0.015, 0.0])
w_tan = np.linalg.solve(cov[:3, :3], mu_ex[:3])
w_tan = w_tan / w_tan.sum()
sd_tan = math.sqrt(w_tan @ cov[:3, :3] @ w_tan)
mctr = cov[:3, :3] @ w_tan / sd_tan
actr = w_tan * mctr
ok(
    "risk budget at the Sharpe-maximising mix: absolute contributions sum to portfolio volatility, and every asset has"
    " the same ratio of excess return to marginal contribution (the portfolio's Sharpe ratio), as in Exhibit 19",
    close(actr.sum(), sd_tan, 1e-12) and np.ptp(mu_ex[:3] / mctr) < 1e-12,
    f"ratio {mu_ex[0] / mctr[0]:.4f}",
)

print("== part 7: liability-relative allocation")
ex_r = np.array([0.065, 0.040, 0.050])  # equities, long liability-matching bonds, credit
vols = np.array([0.16, 0.10, 0.07])
c = np.array(
    [[1, 0.1, 0.5, 0.1], [0.1, 1, 0.6, 0.95], [0.5, 0.6, 1, 0.55], [0.1, 0.95, 0.55, 1]]
)  # last = liabilities
sd_all = np.append(vols, 0.10)
cov_all = np.outer(sd_all, sd_all) * c
A, L = 1.10, 1.00


def surplus_stats(w):
    x = np.append(A * w, -L)  # money exposures, liabilities short
    mu = (A * w @ ex_r - L * 0.040) / A
    sd = math.sqrt(x @ cov_all @ x) / A
    return mu, sd


w_eq_heavy, w_ldi = np.array([0.60, 0.20, 0.20]), np.array([0.25, 0.65, 0.10])
s_eq, s_ldi = surplus_stats(w_eq_heavy), surplus_stats(w_ldi)
ok(
    "surplus optimisation (funding 110%, liabilities like long bonds): a 60/20/20 asset-only mix has surplus volatility"
    " of 11.6% of assets; a 25/65/10 liability-matching mix cuts it to 5.3% while giving up 0.97 point of expected"
    " surplus return",
    abs(s_eq[1] - 0.1164) < 1e-3
    and abs(s_ldi[1] - 0.0532) < 1e-3
    and abs((s_eq[0] - s_ldi[0]) - 0.00975) < 1e-5,
    f"surplus sd {s_eq[1]:.4f} vs {s_ldi[1]:.4f}",
)
hedge = L / A
ok(
    "hedging/return-seeking: with assets 1.10 and liabilities 1.00, 90.9% goes to the liability-hedging portfolio and"
    " the 9.1% surplus to return-seeking assets; with a deficit (assets 0.95) the split is unavailable without"
    " contributions or leverage",
    abs(hedge - 0.9091) < 1e-4 and 0.95 < L,
)

print("== part 8: goals-based allocation and heuristics")
modules = {
    "A": (4.3, 2.7),
    "B": (5.5, 4.5),
    "C": (6.4, 6.0),
    "D": (7.2, 7.5),
    "E": (8.0, 10.0),
    "F": (8.7, 12.5),
}
printed_5y99 = {"A": 1.5, "B": 0.9, "C": 0.2, "D": -0.6, "E": -2.4, "F": -4.3}


def min_exp(mu, sd, years, prob):
    return mu - norm.ppf(prob) * sd / math.sqrt(years)


diffs = [abs(min_exp(*modules[k], 5, 0.99) - printed_5y99[k]) for k in modules]
ok(
    "Exhibit 36: the minimum-expectation return mu - z sigma / sqrt(T) reproduces the 5-year 99% row to within 0.1"
    " point (1.5, 0.9, 0.2, -0.6, -2.4, -4.3)",
    max(diffs) < 0.1,
    " ".join(f"{min_exp(*modules[k], 5, 0.99):.2f}" for k in modules),
)
best_5y95 = max(modules, key=lambda k: min_exp(*modules[k], 5, 0.95))
best_10y75 = max(modules, key=lambda k: min_exp(*modules[k], 10, 0.75))
ok(
    "module choice: for a 5-year need at 95% the best module is A (2.3%); for a 10-year wish at 75% it is F (6.0%)",
    best_5y95 == "A" and best_10y75 == "F" and abs(min_exp(*modules["F"], 10, 0.75) - 6.03) < 0.05,
)
g3, g4 = 10_000 / 1.041**10, 10_000 / 1.068**20
ok(
    "the Smiths: 10m in 10 years at 4.1% needs 6,691 thousand and 10m in 20 years at 6.8% needs 2,683 thousand; the"
    " printed 6,671 and 2,679 correspond to unrounded rates near 4.13% and 6.81%",
    abs(g3 - 6690.8) < 1
    and abs(g4 - 2682.7) < 1
    and abs((10_000 / 6_671) ** 0.1 - 1 - 0.0413) < 2e-4,
    f"{g3:.1f} {g4:.1f}",
)
w_rp = (1 / vol[:3]) / (1 / vol[:3]).sum()
ok(
    "heuristics: '120 minus age' gives 75% equities at 45; 60/40 is fixed; 1/N over three classes is 33.3% each; naive"
    " risk parity (inverse volatility over two equity classes and bonds) gives 22.0%, 19.5% and 58.5%",
    close(120 - 45, 75) and abs(w_rp[2] - 0.5854) < 1e-3,
    " ".join(f"{x:.1%}" for x in w_rp),
)

print("== part 9: constraints, taxes and revisions")
ok(
    "after-tax returns (PMiP eqs. 1-3): a 3% coupon at a 40% tax rate earns 1.8%; 8% taxed at 25% earns 6%; after-tax"
    " volatility is sigma(1 - t), so taxes shrink return and risk proportionally",
    close(0.03 * 0.6, 0.018, 1e-12) and close(0.08 * 0.75, 0.06, 1e-12),
)
small_fund, min_ticket, n_funds = 20e6, 5e6, 8
ok(
    "size constraint: a 20m foundation cannot build a diversified 8-fund private-equity programme with 5m minimum"
    " commitments (40m needed); a large fund faces the opposite problem of capacity in small markets",
    min_ticket * n_funds > small_fund,
)
w_before, w_after = np.array([0.60, 0.30, 0.10]), np.array([0.35, 0.55, 0.10])
ok(
    "revision: after a rise in funding from 95% to 120%, de-risking from 60% to 35% return-seeking assets lowers surplus"
    " volatility because the plan no longer needs return to close a deficit",
    surplus_stats(w_after)[1] < surplus_stats(w_before)[1],
)

print("== part 10: short-term shifts and behavioural biases")
tilt_alpha, tilt_te = 0.006, 0.02
ok(
    "a tactical tilt adding 0.6% a year with 2% tracking error has an information ratio of 0.30; over 5 years its"
    " t-statistic is only 0.67, so its skill cannot be confirmed quickly",
    close(tilt_alpha / tilt_te, 0.30, 1e-12) and abs(0.30 * math.sqrt(5) - 0.6708) < 1e-4,
)
ok(
    "loss aversion: with losses weighted 2.25 times gains, a 50/50 bet of +12/-10 feels negative (12 - 22.5 < 0)"
    " though its expected value is +1: framing returns as losses drives under-allocation to equities",
    0.5 * 12 - 0.5 * 2.25 * 10 < 0 < 0.5 * 12 - 0.5 * 10,
)


print("== part 10: client decisions and complete funding")
# Cedar: the covariance above belongs to the same four asset classes.
client_mu = np.array([0.07, 0.08, 0.035, 0.02])
client_stress = np.array([-0.30, -0.40, 0.05, 0.02])
# cov was reused later in this script; rebuild the declared four-asset input explicitly.
client_vol = np.array([0.16, 0.18, 0.06, 0.01])
client_corr = np.array([[1, 0.75, 0.2, 0], [0.75, 1, 0.15, 0], [0.2, 0.15, 1, 0.1], [0, 0, 0.1, 1]])
client_cov = np.outer(client_vol, client_vol) * client_corr
mixes = np.array(
    [[0.45, 0.2, 0.3, 0.05], [0.2, 0.05, 0.6, 0.15], [0.35, 0.1, 0.45, 0.1], [0.3, 0.15, 0.45, 0.1]]
)
means = mixes @ client_mu
vols = np.sqrt(np.einsum("ij,jk,ik->i", mixes, client_cov, mixes))
stresses = mixes @ client_stress
utilities = means - 2.5 * vols**2
feasible = (
    (means >= 0.05)
    & (vols <= 0.085)
    & (stresses >= -0.15)
    & (mixes[:, 3] >= 0.1)
    & (mixes.max(axis=1) <= 0.45)
)
ok(
    "Cedar alternatives satisfy or fail the stated constraints",
    np.array_equal(feasible, [False, False, True, True]),
)
ok(
    "recommended candidate has higher specified utility than the other feasible mix",
    utilities[3] > utilities[2],
)
# Dated dollar ledger, independently sum dollar asset gains then deduct spending.
amounts = mixes[3] * 10_000_000
expected_close = sum(amounts * (1 + client_mu)) - 300_000
stress_close = sum(amounts * (1 + client_stress)) - 300_000
ok(
    "Cedar dollar ledger, liquidity and stress outcomes",
    close(expected_close, 10_207_500, 1e-6)
    and close(stress_close, 8_445_000, 1e-6)
    and amounts[3] >= 3 * 300_000,
)
# Normal-model fifth percentile of the recommended mix: closed form, and independently the
# empirical quantile of simulated multivariate-normal asset returns (2026-10-20 correction: -8.1%, not -8.2%).
q05 = means[3] + norm.ppf(0.05) * vols[3]
sim = np.random.default_rng(20261020).multivariate_normal(client_mu, client_cov, 400_000) @ mixes[3]
ok(
    "Cedar normal-model fifth percentile is about -8.1%",
    round(q05 * 100, 1) == -8.1 and abs(np.quantile(sim, 0.05) - q05) < 0.0005,
    f"closed form {q05:.4%}, simulated {np.quantile(sim, 0.05):.4%}",
)
for i in range(4):
    print(
        f"Cedar {i}: mean {means[i]:.6%}, volatility {vols[i]:.6%}, stress {stresses[i]:.6%}, utility {utilities[i]:.6%}"
    )
# Lins: lognormal single-payment budgets, using direct distribution CDF as a check.
modules = np.array([[0, 0, 1], [0.4, 0.6, 0], [0.8, 0.2, 0]])
log_mu = np.array([0.02, 0.04, 0.055])
log_sd = np.array([0, 0.07, 0.13])
goals = [(250_000.0, 5, 0.95), (900_000.0, 15, 0.80)]
capital, choices = [], []
for amount, horizon, success in goals:
    costs = amount * np.exp(-log_mu * horizon + norm.ppf(success) * log_sd * math.sqrt(horizon))
    choice = int(np.argmin(costs))
    choices.append(choice)
    capital.append(costs[choice])
    for j in range(3):
        terminal_quantile = costs[j] * math.exp(
            log_mu[j] * horizon - norm.ppf(success) * log_sd[j] * math.sqrt(horizon)
        )
        probability = (
            1.0
            if j == 0
            else norm.sf(
                (math.log(amount / costs[j]) - log_mu[j] * horizon)
                / (log_sd[j] * math.sqrt(horizon))
            )
        )
        ok(
            f"goal {horizon} years module {j}: wealth quantile and independent CDF",
            close(terminal_quantile, amount, 1e-6) and probability >= success - 1e-10,
        )
ok("lowest funding costs select cash for education and growth for home", choices == [0, 2])
reserve = 100_000.0
surplus = 1_000_000 - reserve - sum(capital)
assets_by_goal = np.array([capital[i] * modules[j] for i, j in enumerate(choices)])
aggregate = assets_by_goal.sum(axis=0) + np.array([0, 0, reserve + surplus])
ok(
    "Lins total funding reconciles to aggregate asset balances",
    close(aggregate.sum(), 1_000_000, 1e-6)
    and np.allclose(aggregate, [482_025.6193409, 120_506.4048352, 397_467.9758239], atol=0.001),
)
heuristic_cost = [
    a * math.exp(-0.0475 * t + norm.ppf(p) * 0.10 * math.sqrt(t)) for a, t, p in goals
]
ok(
    "same-client 60/40 budgets are more expensive but feasible",
    sum(heuristic_cost) + reserve <= 1_000_000 and sum(heuristic_cost) > sum(capital),
)
education_probability_6040 = norm.sf(
    (math.log(250_000 / capital[0]) - 0.0475 * 5) / (0.10 * math.sqrt(5))
)
ok(
    "60/40 applied to cheaper education capital fails 95% success",
    education_probability_6040 < 0.95,
)
remaining = 900_000 - reserve - capital[0]
revised_home = remaining * math.exp(0.055 * 15 - norm.ppf(0.80) * 0.13 * math.sqrt(15))
ok(
    "infeasible 900,000 wealth case reduces the flexible goal explicitly",
    remaining < capital[1] and close((capital[1] - remaining), 28_741.3786851, 0.001),
)
print(
    f"Lins budgets {capital}, surplus {surplus:.6f}, aggregate {aggregate}, 60/40 total {sum(heuristic_cost) + reserve:.6f}, reduced home {revised_home:.6f}"
)

print()
if fails:
    print(f"{len(fails)} check(s) failed: {fails}")
    sys.exit(1)
print("all checks passed")
