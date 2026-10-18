"""Market risk measurement and limits (2026-10-19): the worked numbers of meth:portfolio-var-methods-decomposition,
meth:sensitivity-scenario-risk-measures and meth:market-risk-limits-capital.

Reproduced from Hull, Risk Management and Financial Institutions, 6th ed. (2023): the model-building VaR of $10m
Microsoft and $5m AT&T (one-day 99% VaR 512,300; ten-day 1,620,100; ten-day ES 1,856,100; diversification benefit
219,000; sec. 13.1), changing the confidence level (VaR 1.5m -> 2.12m, ES 2m -> 2.58m) and aggregating ES (60 and 100
at correlation 0.4 -> 135.6) (sec. 11.6-11.8), RAROC of 20% and 22% (sec. 28.6), and 97.5% ES = 2.338 sigma against 99%
VaR = 2.326 sigma (sec. 27.1). From Managing Investment Portfolios (2007), chap. 9: the FX and fixed-income desks'
returns on capital (20% and 12.5%) under the same VaR budget. Original, synthetic data (fixed seed): a 100m two-asset
portfolio with Student-t returns for parametric, historical and Monte Carlo VaR and ES, Euler component, marginal and
incremental VaR, and a backtest count; equity, bond and option sensitivities against full revaluation; historical,
hypothetical and reverse stress scenarios; limits, surplus at risk and relative VaR.

Count convention: one check is one executed ok() call (a call inside a loop counts once per iteration).

Run: uv run python market-risk-checks.py   (numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import math
import sys

# third party library imports
import numpy as np
import scipy
from scipy.optimize import brentq
from scipy.stats import norm

print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
fails = []


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


Z99 = 2.326  # Hull rounds N^{-1}(0.99) to 2.326 in the worked examples


def es_normal(sigma, x=0.99):
    y = norm.ppf(x)
    return sigma * math.exp(-(y**2) / 2) / (math.sqrt(2 * math.pi) * (1 - x))


print("== part 1: VaR and ES by the model-building approach (RMFI 6th ed., chaps. 11 and 13)")
s_msft, s_t = 10e6 * 0.02, 5e6 * 0.01
s_port = math.sqrt(s_msft**2 + s_t**2 + 2 * 0.3 * s_msft * s_t)
ok(
    "one-day sd 220,227; one-day 99% VaR 512,300; ten-day 1,620,100 (Microsoft 10m at 2%/day, AT&T 5m at 1%, rho 0.3)",
    abs(s_port - 220_227) < 1
    and abs(Z99 * s_port - 512_300) < 100
    and abs(Z99 * s_port * math.sqrt(10) - 1_620_100) < 300,
    f"{Z99 * s_port:,.0f} {Z99 * s_port * math.sqrt(10):,.0f}",
)
ok(
    "ten-day 99% ES 1,856,100 (sigma x phi(z)/0.01 x sqrt 10)",
    abs(es_normal(s_port * math.sqrt(10)) - 1_856_100) < 500,
    f"{es_normal(s_port * math.sqrt(10)):,.0f}",
)
v_m, v_t = Z99 * s_msft * math.sqrt(10), Z99 * s_t * math.sqrt(10)
ok(
    "ten-day VaRs 1,471,300 and 367,800 alone; diversification benefit 1,471,300 + 367,800 - 1,620,100 = 219,000",
    abs(v_m - 1_471_300) < 300
    and abs(v_t - 367_800) < 100
    and abs(v_m + v_t - Z99 * s_port * math.sqrt(10) - 219_000) < 400,
)
ok(
    "RMFI sec. 11.6: 95% VaR 1.5m -> 99% VaR 2.12m under normality; 95% ES 2m -> 99% ES 2.58m",
    abs(1.5 * norm.ppf(0.99) / norm.ppf(0.95) - 2.12) < 5e-3
    and abs(
        2
        * 0.05
        / 0.01
        * math.exp(-(norm.ppf(0.99) - norm.ppf(0.95)) * (norm.ppf(0.99) + norm.ppf(0.95)) / 2)
        - 2.58
    )
    < 5e-3,
)
ok(
    "RMFI sec. 11.8: aggregating ESs of 60 and 100 with correlation 0.4 gives 135.6",
    abs(math.sqrt(60**2 + 100**2 + 2 * 0.4 * 60 * 100) - 135.6) < 0.05,
)

print("== part 2: parametric, historical and Monte Carlo VaR and ES on a synthetic 100m portfolio")
rng = np.random.default_rng(20261019)
n, nu = 1000, 4
vols = np.array([0.012, 0.004])
corr = np.array([[1.0, -0.2], [-0.2, 1.0]])
L = np.linalg.cholesky(corr)
z = rng.standard_normal((n, 2)) @ L.T
w = rng.chisquare(nu, size=(n, 1)) / nu
rets = z / np.sqrt(w) * vols * math.sqrt((nu - 2) / nu)  # Student-t with the target volatilities
pos = np.array([60e6, 40e6])
pnl = rets @ pos
cov = np.cov(rets, rowvar=False)
sd_p = math.sqrt(pos @ cov @ pos)
var_par = norm.ppf(0.99) * sd_p - pnl.mean()
es_par = es_normal(sd_p) - pnl.mean()
srt = np.sort(-pnl)[::-1]  # losses, largest first
var_hs = np.quantile(-pnl, 0.99, method="higher")
es_hs = srt[: int(0.01 * n)].mean()
sim_n = 200_000
zs = rng.standard_normal((sim_n, 2)) @ np.linalg.cholesky(cov).T
pnl_mc = zs @ pos
var_mc = np.quantile(-pnl_mc, 0.99)
ok(
    "Monte Carlo with the sample covariance (normal) reproduces parametric VaR within 1.5%",
    abs(var_mc / var_par - 1) < 0.015,
    f"par {var_par:,.0f}, MC {var_mc:,.0f}",
)
ok(
    "with Student-t (4 df) returns the historical 99% VaR and ES exceed the normal ones: fat tails are missed by the"
    " parametric method",
    var_hs > var_par and es_hs > es_par,
    f"HS VaR {var_hs:,.0f} ES {es_hs:,.0f}; normal VaR {var_par:,.0f} ES {es_par:,.0f}",
)
wt = rng.chisquare(nu, size=(sim_n, 1)) / nu
pnl_t = (
    rng.standard_normal((sim_n, 2)) @ L.T / np.sqrt(wt) * vols * math.sqrt((nu - 2) / nu)
) @ pos
ok(
    "Monte Carlo from the true Student-t model agrees with historical VaR within 15% (sampling error of 1,000 days)",
    abs(np.quantile(-pnl_t, 0.99) / var_hs - 1) < 0.15,
    f"{np.quantile(-pnl_t, 0.99):,.0f}",
)
# Euler decomposition under the parametric model
marg = (cov @ pos) / sd_p * norm.ppf(0.99)
comp = pos * marg
ok(
    "component VaRs (Euler) sum to the parametric VaR (zero-mean form)",
    close(comp.sum(), norm.ppf(0.99) * sd_p, 1e-6),
    f"equity {comp[0]:,.0f}, bonds {comp[1]:,.0f}",
)
var_eq_only = norm.ppf(0.99) * math.sqrt(pos[0] ** 2 * cov[0, 0])
incr_bonds = norm.ppf(0.99) * sd_p - var_eq_only
ok(
    "the 40m bond book has a component VaR near zero (+11,899) but an incremental VaR of -28,794: removing it would"
    " raise VaR. Component approximates incremental only for small positions",
    abs(comp[1] - 11_899) < 1 and abs(incr_bonds + 28_794) < 1,
    f"component {comp[1]:,.0f}, incremental {incr_bonds:,.0f}",
)
small = np.array([60e6, 1e6])
sd_s = math.sqrt(small @ cov @ small)
comp_s = small[1] * (cov @ small)[1] / sd_s * norm.ppf(0.99)
incr_s = norm.ppf(0.99) * sd_s - var_eq_only
ok(
    "with a 1m bond position instead, component and incremental VaR agree within 5%",
    abs(comp_s - incr_s) < 0.05 * abs(incr_s),
    f"component {comp_s:,.0f}, incremental {incr_s:,.0f}",
)
bump = 1e5
bumped = pos + np.array([bump, 0.0])
var_bumped = norm.ppf(0.99) * math.sqrt(bumped @ cov @ bumped)
ok(
    "marginal VaR by a 100,000 bump of equities matches the analytic marginal VaR",
    abs((var_bumped - norm.ppf(0.99) * sd_p) / bump - marg[0]) < 1e-4,
)
viol = np.sum(
    -pnl[250:]
    > np.array([np.quantile(-pnl[i - 250 : i], 0.99, method="higher") for i in range(250, n)])
)
ok(
    "rolling 250-day historical VaR has 750 out-of-sample days and an expected 7.5 violations; the count is reported",
    0 <= viol <= 25,
    f"{viol} violations",
)

print("== part 3: sensitivity and scenario measures against VaR")
beta, eq_pos = 1.1, 60e6
ok(
    "equity: beta 1.1 on 60m loses 6.6m for a 10% index fall",
    close(beta * eq_pos * 0.10, 6.6e6, 1e-6),
)
bond_pos, dur, cvx = 40e6, 6.5, 60.0
dp = bond_pos * (-dur * 0.01 + 0.5 * cvx * 0.01**2)
ok(
    "bonds: duration 6.5, convexity 60 on 40m: +100 bp loses 2.48m (duration 2.60m less convexity 0.12m); PVBP 26,000",
    abs(dp + 2.48e6) < 1 and close(bond_pos * dur * 1e-4, 26_000, 1e-6),
)


def bs(s, k, t, r, sig, kind="c"):
    d1 = (math.log(s / k) + (r + sig**2 / 2) * t) / (sig * math.sqrt(t))
    d2 = d1 - sig * math.sqrt(t)
    if kind == "c":
        return s * norm.cdf(d1) - k * math.exp(-r * t) * norm.cdf(d2)
    return k * math.exp(-r * t) * norm.cdf(-d2) - s * norm.cdf(-d1)


# options book: short 10,000 index puts (multiplier 100) struck 95 on index 100, 3 months, 20% vol, 4%
S, K, T, r, sig, qty = 100.0, 95.0, 0.25, 0.04, 0.20, -10_000 * 100
v0 = qty * bs(S, K, T, r, sig, "p")
h = 0.01
delta = qty * (bs(S + h, K, T, r, sig, "p") - bs(S - h, K, T, r, sig, "p")) / (2 * h)
gamma = (
    qty
    * (bs(S + h, K, T, r, sig, "p") - 2 * bs(S, K, T, r, sig, "p") + bs(S - h, K, T, r, sig, "p"))
    / h**2
)
vega = qty * (bs(S, K, T, r, sig + 1e-4, "p") - bs(S, K, T, r, sig - 1e-4, "p")) / 2e-4
grid = {}
for ds, dv in ((-2.0, 0.0), (-10.0, 0.10), (-25.0, 0.25)):
    full = qty * bs(S + ds, K, T, r, sig + dv, "p") - v0
    approx = delta * ds + 0.5 * gamma * ds**2 + vega * dv
    grid[(ds, dv)] = (full, approx, (full - approx) / full)
ok(
    "short 1m puts: the delta-gamma-vega approximation is within 1% for a 2-point fall, understates the loss by 7%"
    " for a 10-point fall with volatility up 10 points (cross terms omitted), and overstates it by 7% at 25 points",
    abs(grid[(-2.0, 0.0)][2]) < 0.01
    and abs(grid[(-10.0, 0.10)][2] - 0.069) < 0.002
    and abs(grid[(-25.0, 0.25)][2] + 0.071) < 0.002,
    f"(-10, +10vol) full {grid[(-10.0, 0.10)][0] / 1e6:.3f}m vs approx {grid[(-10.0, 0.10)][1] / 1e6:.3f}m",
)
# scenarios on the whole book (equity 60m beta 1.1, bonds 40m, the put book)
scen = {
    "historical 2008-style": (-0.35, -0.0100, 0.30),
    "rates shock": (-0.05, 0.0150, 0.05),
    "hypothetical crash": (-0.20, -0.0050, 0.25),
}
res = {}
for name, (eq, dy, dvol) in scen.items():
    eq_pnl = beta * eq_pos * eq
    bd_pnl = bond_pos * (-dur * dy + 0.5 * cvx * dy**2)
    opt_pnl = qty * bs(S * (1 + eq), K, T, r, sig + dvol, "p") - v0
    res[name] = eq_pnl + bd_pnl + opt_pnl
ok(
    "the 2008-style scenario loses far more than the 99% one-day VaR: VaR says nothing about such tails",
    -res["historical 2008-style"] > 5 * var_par,
    f"{res['historical 2008-style'] / 1e6:.1f}m vs VaR {var_par / 1e6:.2f}m",
)


def total_loss(eq):
    return -(
        beta * eq_pos * eq + qty * bs(S * (1 + eq), K, T, r, sig + max(-eq, 0) * 1.0, "p") - v0
    )


eq_break = brentq(lambda e: total_loss(e) - 20e6, -0.5, 0.0)
ok(
    "reverse stress test: the index fall (with volatility rising one point per point of fall) that loses 20m is 14.95%",
    abs(eq_break + 0.1495) < 5e-4,
    f"{eq_break:.4f}",
)

print("== part 4: limits, risk budgets, capital allocation and institution-specific measures")
ok(
    "MIP: FX desk 100m capital, VaR 5m, profit 20m (20%); fixed-income desk 200m, VaR 5m, profit 25m (12.5%)",
    close(20 / 100, 0.20) and close(25 / 200, 0.125),
)
ok(
    "with weak correlation the combined VaR is 7m, 70% of the 10m sum: risk budgets are not additive",
    close(7 / 10, 0.70),
)
ok(
    "RMFI Example: economic capital 4 per 100 of loans, expected profit 0.80 -> RAROC 20%; adding 2% on capital -> 22%",
    close(0.80 / 4, 0.20) and close((0.80 + 0.02 * 4) / 4, 0.22),
)
ok(
    "RMFI sec. 27.1: under normality 97.5% ES = 2.338 sigma and 99% VaR = 2.326 sigma",
    abs(es_normal(1.0, 0.975) - 2.338) < 5e-4 and abs(norm.ppf(0.99) - 2.326) < 5e-4,
)
nu_t = 4
xs = np.sort(rng.standard_t(nu_t, 2_000_000) * math.sqrt((nu_t - 2) / nu_t))
t_var99 = xs[int(0.99 * len(xs))]
t_es975 = xs[int(0.975 * len(xs)) :].mean()
ok(
    "for a unit-variance Student-t (4 df) the 97.5% ES (2.83) exceeds the 99% VaR (2.66), unlike the normal case:"
    " heavier tails separate the two",
    abs(t_es975 - 2.83) < 0.02 and abs(t_var99 - 2.66) < 0.02 and t_es975 > t_var99 + 0.1,
    f"ES {t_es975:.3f}, VaR {t_var99:.3f}",
)
# pension surplus at risk: assets 1,000 duration 8, liabilities 900 duration 14, rate vol 1% a year
a, la, da, dl, sig_y = 1000.0, 900.0, 8.0, 14.0, 0.01
surplus_dv = a * da - la * dl
sar = norm.ppf(0.95) * abs(surplus_dv) * sig_y
ok(
    "surplus at risk: assets 1,000 (duration 8) against liabilities 900 (duration 14) lose 46 of surplus per 1% fall in"
    " rates; 95% one-year SaR from rates alone is 75.7",
    close(surplus_dv * 0.01, -46.0, 1e-9) and abs(sar - 75.66) < 0.01,
    f"{sar:.2f}",
)
ok(
    "a 3% tracking error is a 95% one-year relative VaR of 4.93% of assets for an active manager",
    abs(norm.ppf(0.95) * 0.03 - 0.0493) < 5e-5,
)
daily_stop = 2.0
hit_rate = np.mean(-pnl > daily_stop * 1e6)
ok(
    "a 2m daily stop-loss is 1.15 times the normal 99% VaR, yet the fat-tailed history breaches it on 1.1% of days"
    " (about 2.8 days a year) against the 0.36% normality implies",
    abs(daily_stop * 1e6 / var_par - 1.15) < 0.01
    and abs(hit_rate - 0.011) < 0.0015
    and hit_rate > 1 - norm.cdf(daily_stop * 1e6 / sd_p),
    f"{hit_rate:.4f} vs normal {1 - norm.cdf(daily_stop * 1e6 / sd_p):.4f}",
)

print()
if fails:
    print(f"{len(fails)} check(s) failed: {fails}")
    sys.exit(1)
print("all checks passed")
