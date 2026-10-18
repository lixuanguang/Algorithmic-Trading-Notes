"""CAPM, market model and factor models (2026-10-18): the worked examples of mech:systematic-risk-pricing,
mod:return-generating-models, mod:capm-sml, meth:capm-regression, meth:required-return-on-equity,
mod:multifactor-apt and def:factor-model-types.

Part 1 is a declared synthetic sample: twelve monthly total returns in percent, typed by hand, for a stock S,
a market index M and a one-month Treasury bill whose rate rises from 0.30 to 0.42 percent a month. The stock's
returns were built as r_f + 0.1 + 1.25 (R_M - r_f) + e with hand-chosen e summing to zero, rounded to one decimal;
the regression does not know this. Alpha and beta are estimated by the closed forms, by numpy least squares and by
statsmodels OLS.

Part 3 uses forward-looking inputs published for 1 October 2026: Damodaran's implied equity risk premium of
4.20 percent with the 5.29 percent US Treasury rate he paired with it (the 10-year par yield on 30 September 2026
in the Treasury's daily file), and an assumed beta. Parts 2, 4 and 5 use invented inputs.

No random draws. Run: uv run python asset-pricing-checks.py   (numpy, statsmodels). Exits 1 on failure.
"""

# standard library imports
import math
import re
import sys
from pathlib import Path

# third party library imports
import numpy as np
import statsmodels
import statsmodels.api as sm

print(
    f"Python {sys.version.split()[0]}, NumPy {np.__version__}, statsmodels {statsmodels.__version__}"
)
fails = []


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


print("== part 1: CAPM regression on twelve synthetic months (percent a month)")
rf = np.array([0.30, 0.31, 0.32, 0.33, 0.35, 0.36, 0.38, 0.39, 0.40, 0.41, 0.42, 0.42])
RM = np.array([2.1, -1.4, 3.0, 0.8, -2.6, 1.9, 4.2, -0.7, 1.1, -3.3, 2.5, 0.6])
RS = np.array([3.6, -3.3, 2.6, 2.8, -3.6, 0.5, 6.6, -0.2, -0.8, -3.0, 3.7, 1.6])
n = len(RS)
x, y = RM - rf, RS - rf
sxx = ((x - x.mean()) ** 2).sum()
sxy = ((x - x.mean()) * (y - y.mean())).sum()
beta = sxy / sxx
alpha = y.mean() - beta * x.mean()
X = np.column_stack([np.ones(n), x])
lstsq = np.linalg.lstsq(X, y, rcond=None)[0]
fit = sm.OLS(y, X).fit()
ok(
    "excess-return regression: beta = Sxy/Sxx = 1.2548, alpha = 0.1108 percent a month (closed form = lstsq = OLS)",
    np.allclose(lstsq, [alpha, beta])
    and np.allclose(fit.params, [alpha, beta])
    and close(beta, 1.254850, 1e-6)
    and close(alpha, 0.110752, 1e-6),
    f"alpha {alpha:.6f}, beta {beta:.6f}",
)
ok(
    "beta also = sample Cov(excess S, excess M) / Var(excess M), any common denominator",
    close(beta, np.cov(y, x, ddof=1)[0, 1] / np.var(x, ddof=1))
    and close(beta, np.cov(y, x, ddof=0)[0, 1] / np.var(x, ddof=0)),
)
resid = y - alpha - beta * x
s = math.sqrt((resid**2).sum() / (n - 2))
se_b = s / math.sqrt(sxx)
se_a = s * math.sqrt(1 / n + x.mean() ** 2 / sxx)
r2 = 1 - (resid**2).sum() / ((y - y.mean()) ** 2).sum()
ok(
    "standard errors by hand = OLS: se(beta) 0.1903, se(alpha) 0.4220; residual s.d. 1.447; R^2 0.813",
    np.allclose(fit.bse, [se_a, se_b])
    and close(se_b, 0.190267, 1e-6)
    and close(se_a, 0.422013, 1e-6)
    and close(s, 1.446842, 1e-6)
    and close(r2, fit.rsquared)
    and close(r2, 0.813073, 1e-6),
)
ci = fit.conf_int(0.05)
ok(
    "t(alpha) 0.26 with a 95 percent interval of -0.83 to 1.05; beta interval 0.83 to 1.68 (10 df)",
    close(fit.tvalues[0], 0.262437, 1e-5)
    and np.allclose(ci[0], [-0.829552, 1.051056], atol=1e-5)
    and np.allclose(ci[1], [0.830910, 1.678790], atol=1e-5),
)
ok(
    "annualised: 12 x alpha = 1.33 percent a year, with a 95 percent interval of -9.95 to 12.61 percent",
    close(12 * alpha, 1.329022, 1e-5)
    and np.allclose(12 * ci[0], [-9.954629, 12.612673], atol=1e-4),
)
# Systematic and residual parts of the sample variation: SST = beta^2 Sxx + SSE.
sst = ((y - y.mean()) ** 2).sum()
ok(
    "decomposition: total sum of squares = beta^2 Sxx + SSE; systematic share = R^2",
    close(sst, beta**2 * sxx + (resid**2).sum(), 1e-9) and close(beta**2 * sxx / sst, r2),
    f"systematic {beta**2 * sxx:.4f}, residual {(resid**2).sum():.4f}",
)
ok(
    "monthly s.d.: market excess 2.293, stock excess 3.191, residual 1.447 percent",
    close(np.std(x, ddof=1), 2.292780, 1e-6) and close(np.std(y, ddof=1), 3.190724, 1e-6),
)
# Raw-return (market model) regression.
Xr = np.column_stack([np.ones(n), RM])
a_raw, b_raw = np.linalg.lstsq(Xr, RS, rcond=None)[0]
ok(
    "raw-return regression: a = 0.0158, b = 1.2574, differing from alpha 0.1108 and beta 1.2548",
    close(a_raw, 0.015803, 1e-6) and close(b_raw, 1.257362, 1e-6),
)
ok(
    "a - alpha = -0.0949 is mostly (1 - beta) mean(r_f) = -0.0932; the remaining -0.0017 comes from the varying r_f",
    close(a_raw - alpha, -0.094949, 1e-6)
    and close((1 - beta) * rf.mean(), -0.093233, 1e-6)
    and close(a_raw - (alpha + (1 - beta) * rf.mean()), -0.001716, 1e-6),
    f"{alpha + (1 - beta) * rf.mean():.6f} against {a_raw:.6f}",
)
# With a constant risk-free rate the slopes coincide and a = alpha + (1 - beta) r_f exactly.
rf_c = np.full(n, rf.mean())
RS_c = RS - rf + rf_c
RM_c = RM - rf + rf_c
ac, bc = np.linalg.lstsq(np.column_stack([np.ones(n), RM_c]), RS_c, rcond=None)[0]
ae, be = np.linalg.lstsq(np.column_stack([np.ones(n), RM_c - rf_c]), RS_c - rf_c, rcond=None)[0]
ok(
    "constant r_f: raw and excess slopes are equal and a = alpha + (1 - beta) r_f exactly",
    close(bc, be, 1e-12) and close(ac, ae + (1 - be) * rf_c[0], 1e-12),
)
ok(
    "averages: stock 0.875, market 0.683, T-bill 0.366 percent a month",
    close(RS.mean(), 0.875)
    and close(RM.mean(), 0.683333, 1e-6)
    and close(rf.mean(), 0.365833, 1e-6),
)

ok(
    "single-index covariance for 500 assets: 1,001 parameters (500 betas, 500 residual variances, 1 market variance) against 125,250",
    500 * 501 // 2 == 125_250 and 2 * 500 + 1 == 1001,
)

print("== part 2: SML, CML and systematic risk (forward-looking inputs, percent a year)")
RF, ERP, SM = 5.29, 4.20, 16.0  # market s.d. 16 percent is an assumption of the example
sml = lambda b: RF + b * ERP
for b in (0.0, 0.6, 1.0, 1.25, 1.6):
    print(f"    beta {b:.2f}: required return {sml(b):.3f}")
ok(
    "SML: 5.29, 7.81, 9.49, 10.54, 12.01 for beta 0, 0.6, 1, 1.25, 1.6",
    np.allclose([sml(b) for b in (0, 0.6, 1, 1.25, 1.6)], [5.29, 7.81, 9.49, 10.54, 12.01]),
)
w_port = np.array([0.5, 0.3, 0.2])
b_port = w_port @ np.array([0.6, 1.0, 1.6])
ok(
    "portfolio beta is the weighted average 0.92; its SML return 9.154 = weighted SML returns",
    close(b_port, 0.92)
    and close(sml(b_port), w_port @ np.array([sml(0.6), sml(1.0), sml(1.6)]), 1e-12)
    and close(sml(b_port), 9.154, 1e-9),
)
forecast = 11.5
ok(
    "a 11.5 percent forecast for beta 1.25 plots 0.96 above the SML",
    close(forecast - sml(1.25), 0.96, 1e-9),
)
sd_asset = 30.0
sys_sd = 1.25 * SM
res_sd = math.sqrt(sd_asset**2 - sys_sd**2)
cml = lambda sdv: RF + ERP / SM * sdv
ok(
    "asset with s.d. 30 and beta 1.25 (market s.d. 16): systematic s.d. 20, residual 22.36; CML at 30 would be 13.165",
    close(sys_sd, 20.0) and close(res_sd, 22.360680, 1e-6) and close(cml(30.0), 13.165, 1e-9),
)
ok(
    "the CML portfolio with s.d. 20 has the same expected return as the asset (10.54): only systematic risk is priced",
    close(cml(sys_sd), sml(1.25), 1e-12),
)
ok(
    "correlation with the market implied: rho = beta s_M / s_i = 0.667; CML return = r_f + rho x slope x s_i",
    close(1.25 * SM / sd_asset, 2 / 3)
    and close(RF + (1.25 * SM / sd_asset) * ERP / SM * sd_asset, sml(1.25), 1e-12),
)
# Diversification of residual risk: equal weights over n assets with beta 1.25 and independent residuals.
for k in (1, 10, 100, 1000):
    port_sd = math.sqrt(sys_sd**2 + res_sd**2 / k)
    print(f"    {k:4d} such assets, equal weights: s.d. {port_sd:.2f}")
ok(
    "equal-weight portfolio s.d. 30.0, 21.21, 20.12, 20.01 for n = 1, 10, 100, 1000 -> 20 (systematic)",
    close(math.sqrt(sys_sd**2 + res_sd**2 / 10), 21.213203, 1e-6)
    and close(math.sqrt(sys_sd**2 + res_sd**2 / 100), 20.124612, 1e-6),
)

print("== part 3: required return on equity (inputs for 1 October 2026)")
beta_f = 1.15  # assumed forward-looking beta
ke = RF + beta_f * ERP
ok("k_e = 5.29 + 1.15 x 4.20 = 10.12 percent", close(ke, 10.12, 1e-12))
erp_range = (
    3.30,
    5.67,
)  # Damodaran's lowest and highest of five implied-premium variants on 1 October 2026
ok(
    "with the published range of implied premia 3.30 to 5.67: k_e from 9.085 to 11.810",
    close(RF + beta_f * erp_range[0], 9.085, 1e-9)
    and close(RF + beta_f * erp_range[1], 11.8105, 1e-9),
)
ok(
    "with the 1928-2025 arithmetic stock-T.bond premium of 7.03 instead: k_e 13.38 (a historical, not implied, premium)",
    close(RF + beta_f * 7.0323, 13.377, 1e-3),
)
# Historical-premium alternatives (correction pass, 2026-10-18). The 1928-2025 premium statistics are computed from
# the retained CSV by ../portfolio-risk-return/portfolio-choice-checks.py: arithmetic 7.0323 percent with standard
# error 2.1028 (years treated as independent), and geometric 10.02 - 4.53 = 5.4831 percent.
arith_p, se_p, geo_p = 7.032289, 2.102764, 5.483129
ok(
    "historical premium with the current 10-year yield: arithmetic 13.38, geometric 11.60; +/- 2 s.e. band 8.54 to 18.21",
    close(RF + beta_f * arith_p, 13.377133, 1e-5)
    and close(RF + beta_f * geo_p, 11.595598, 1e-5)
    and close(RF + beta_f * (arith_p - 2 * se_p), 8.540776, 1e-5)
    and close(RF + beta_f * (arith_p + 2 * se_p), 18.213489, 1e-5)
    and close(RF + beta_f * arith_p - (RF + beta_f * geo_p), 1.7815, 1e-3),
)
ok(
    "beta interval 0.83-1.68 from part 1 moves k_e from 8.78 to 12.34 at the 4.20 premium",
    close(RF + 0.83091 * ERP, 8.7798, 1e-3) and close(RF + 1.67879 * ERP, 12.3409, 1e-3),
)
ok(
    "the sample's average stock return, 0.875 x 12 = 10.50 percent a year, is a historical average, not a required return",
    close(12 * RS.mean(), 10.50, 1e-9),
)

print(
    "== part 4: APT, arbitrage and expected returns from factor sensitivities (invented, percent a year)"
)
lam0, lam = (
    4.0,
    np.array([3.0, 1.5]),
)  # zero-beta return and premia per unit sensitivity to factors 1, 2
Bm = np.array([[1.0, 0.5], [0.5, -0.5], [1.5, 1.0]])  # well-diversified portfolios A, B, C
E_abc = lam0 + Bm @ lam
ok("A, B, C priced by the APT: 7.75, 4.75, 10.00", np.allclose(E_abc, [7.75, 4.75, 10.0]))
sol = np.linalg.solve(np.column_stack([np.ones(3), Bm]), E_abc)
ok(
    "solving the three equations recovers lambda_0 = 4, lambda = (3, 1.5)",
    np.allclose(sol, [4.0, 3.0, 1.5]),
)
bD, ED = np.array([0.8, 0.2]), 7.5
fairD = lam0 + bD @ lam
ok(
    "D (b = 0.8, 0.2) should earn 6.70; quoted 7.50 is 0.80 too high",
    close(fairD, 6.7) and close(ED - fairD, 0.8, 1e-12),
)
wrep = np.linalg.solve(np.vstack([np.ones(3), Bm.T]), np.concatenate([[1.0], bD]))
ok(
    "replicating portfolio of A, B, C with D's sensitivities: weights 1.0, 0.2, -0.2 (sum 1), expected return 6.70",
    np.allclose(wrep, [1.0, 0.2, -0.2], atol=1e-12)
    and close(wrep @ E_abc, 6.7, 1e-12)
    and close(wrep.sum(), 1.0)
    and np.allclose(wrep @ Bm, bD),
)
size = 1_000_000.0
pos = np.concatenate([[size], -size * wrep])  # long D, short the replica
ok(
    "long 1,000,000 of D, short the replica: zero cost, zero factor exposure, sure profit 8,000 a year",
    close(pos.sum(), 0.0, 1e-6)
    and np.allclose(pos[0] * bD - (size * wrep) @ Bm, 0.0, atol=1e-6)
    and close((pos[0] * ED - size * wrep @ E_abc) / 100, 8000.0, 1e-6),
)
# If D is a single stock with residual s.d. 25 percent, the trade is not an arbitrage.
res = 25.0
ok(
    "with a single stock's 25 percent residual s.d. the same trade has expected profit 8,000 and s.d. 250,000",
    close(size * res / 100, 250000.0),
)
for k in (1, 100, 2500):
    print(
        f"    {k:5d} independent mispriced stocks (equal weights): residual s.d. {res / math.sqrt(k):.3f} percent"
    )
ok(
    "n independent mispriced stocks: residual s.d. 25/sqrt(n): 2.5 at n = 100, 0.5 at n = 2,500 -- small, not zero",
    close(res / math.sqrt(100), 2.5) and close(res / math.sqrt(2500), 0.5),
)
ok(
    "expected return of a stock with sensitivities (1.2, -0.4): 4 + 3.6 - 0.6 = 7.0; excess over lambda_0 3.0",
    close(lam0 + np.array([1.2, -0.4]) @ lam, 7.0) and close(np.array([1.2, -0.4]) @ lam, 3.0),
)

print("== part 5: multiple risk dimensions and factor-model output (invented)")
# Two portfolios with the same market sensitivity but opposite inflation sensitivity.
b_mkt, b_inf = np.array([1.0, 1.0]), np.array([0.5, -0.5])
shock_m, shock_i = (
    -2.0,
    1.0,
)  # a market factor return of -2 and an inflation surprise factor return of +1
moves = b_mkt * shock_m + b_inf * shock_i
ok(
    "same market beta, inflation sensitivity +0.5 vs -0.5: an inflation shock of +1 moves them -1.5 and -2.5",
    np.allclose(moves, [-1.5, -2.5]),
)
# Fundamental-factor attribution: exposures to market, size and value; monthly factor returns.
expo_p = np.array([1.0, -0.3, 0.6])
expo_b = np.array([1.0, 0.0, 0.1])
f_ret = np.array([2.0, -0.8, 1.2])
active = expo_p - expo_b
ok(
    "active exposures (0, -0.3, 0.5); factor contribution to active return 0.24 + 0.60 = 0.84 percent",
    np.allclose(active, [0, -0.3, 0.5]) and close(active @ f_ret, 0.84, 1e-12),
)
realised_active = 1.10
ok(
    "realised active return 1.10: specific (residual) part 0.26",
    close(realised_active - active @ f_ret, 0.26, 1e-12),
)
F_cov = np.array([[16.0, 2.0, -1.0], [2.0, 9.0, 0.5], [-1.0, 0.5, 6.25]])  # percent^2 a month
spec_var = 4.0
fac_var = expo_p @ F_cov @ expo_p
ok(
    "portfolio variance: factor part x'Fx = 16.48 plus specific 4.0; factor share 80.5 percent",
    close(fac_var, 16.48, 1e-9) and close(fac_var / (fac_var + spec_var), 0.8046875, 1e-9),
    f"{fac_var:.4f}",
)
contrib = expo_p * (F_cov @ expo_p)
ok(
    "factor contributions x_k (F x)_k sum to x'Fx: market 14.80, size 0.12, value 1.56",
    close(contrib.sum(), fac_var, 1e-12) and np.allclose(contrib, [14.8, 0.12, 1.56], atol=1e-9),
    f"{contrib}",
)

print("== figure: security market line coordinates")
fig = Path("../../../compendium/portfolio-construction-risk/figures/security-market-line.tikz")
txt = fig.read_text()
pts = {
    k: tuple(map(float, v.split(",")))
    for k, v in re.findall(r"% point (\w+)\n\s*\\fill \(([^)]*)\)", txt)
}
ok(
    "SML drawn from (0, 5.29) to (2, 13.69); points for beta 0.6, 1, 1.6 on it; the 11.5 forecast above it",
    "(0,5.29) -- (2,13.69)" in txt
    and close(sml(2.0), 13.69, 1e-9)
    and all(close(pts[k][1], sml(pts[k][0]), 1e-9) for k in ("low", "market", "high"))
    and close(pts["forecast"][1], 11.5)
    and pts["forecast"][1] > sml(pts["forecast"][0]),
    f"{pts}",
)

if fails:
    print("FAILED:", ", ".join(fails))
    sys.exit(1)
print("all checks passed")
