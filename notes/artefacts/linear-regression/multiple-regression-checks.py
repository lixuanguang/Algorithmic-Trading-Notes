"""Multiple regression: formulation, fit, misspecification and extensions (2026-10-20).

Worked numbers of meth:multiple-regression-formulation, meth:multiple-regression-fit-tests,
meth:regression-misspecification and meth:regression-extensions.

Data: annual US returns 1928-2025 from notes/artefacts/portfolio-risk-return/us-asset-class-returns-1928-2025.csv
(Damodaran's histretSP workbook, January 2026). The investment problem: how much of the Baa corporate bond excess
return over bills is explained by Treasury duration (10-year Treasury excess return) and by equity-like credit risk
(S&P 500 excess return)? Simulated designs (seeds fixed before the run and not changed) illustrate omitted-variable
bias and multicollinearity, which the real data do not show because the two regressors are nearly uncorrelated.

Independent routes: coefficients from the normal equations against statsmodels OLS; the ANOVA F and R-squared from
sums of squares against statsmodels; the nested F from restricted and unrestricted SSE against statsmodels'
compare_f_test; the omitted-variable identity b_short = b1 + b2 * delta checked exactly in sample; leverage from the
hat matrix against statsmodels' influence measures; the logistic fit by hand-coded Newton-Raphson against
statsmodels Logit.

Count convention: one check is one executed ok() call (a call inside a loop counts once per iteration).

Run: uv run --frozen --no-editable python multiple-regression-checks.py   (numpy, pandas, statsmodels). Exits 1 on failure.
"""

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan, het_white
from statsmodels.stats.outliers_influence import OLSInfluence, variance_inflation_factor
from statsmodels.stats.stattools import durbin_watson

warnings.filterwarnings("ignore")
print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, statsmodels {sm.__version__}")
fails = []
n_checks = 0


def ok(name, cond, detail=""):
    global n_checks
    n_checks += 1
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


root = Path(__file__).resolve().parents[1]
d = pd.read_csv(
    root / "portfolio-risk-return" / "us-asset-class-returns-1928-2025.csv", comment="#"
)
y = (d.baa_corp - d.tbill_3m).to_numpy()
x_bond = (d.tbond_10y - d.tbill_3m).to_numpy()
x_stock = (d.sp500 - d.tbill_3m).to_numpy()
n = len(y)
X = np.column_stack([np.ones(n), x_bond, x_stock])
k = 2

# ---------------------------------------------------------------------------------------------
print("== part 1: formulating the regression")
b = np.linalg.solve(X.T @ X, X.T @ y)
fit = sm.OLS(y, X).fit()
ok(
    "98 years; normal equations and statsmodels agree: intercept 1.18%, bond beta 0.660, stock beta 0.163",
    n == 98
    and np.allclose(b, fit.params, atol=1e-12)
    and [round(v, 4) for v in b] == [0.0118, 0.6599, 0.1632],
)
b_bond_only = sm.OLS(y, X[:, :2]).fit().params[1]
b_stock_only = sm.OLS(y, X[:, [0, 2]]).fit().params[1]
rho = np.corrcoef(x_bond, x_stock)[0, 1]
ok(
    "the regressors are nearly uncorrelated (0.044), so the simple-regression slopes (0.678, 0.174) are close to "
    "the partial ones",
    round(rho, 3) == 0.044 and round(b_bond_only, 3) == 0.678 and round(b_stock_only, 3) == 0.174,
)
resid = y - X @ b
fitted = X @ b
ok(
    "residuals are orthogonal to the fitted values and to each regressor (a property of least squares, so a "
    "residual plot tests shape, not mean)",
    abs(resid @ fitted) < 1e-10 and np.allclose(X.T @ resid, 0, atol=1e-10),
)
yr = d.year.to_numpy()
worst = yr[np.argsort(-np.abs(resid))[:3]]
ok(
    "largest residuals: 2009 (+21.9%), 1932 (+17.8%) and 1934 (+12.5%), all rebounds after credit crises "
    "that the two factors do not capture",
    list(worst) == [2009, 1932, 1934]
    and [round(v, 3) for v in resid[np.argsort(-np.abs(resid))[:3]]] == [0.219, 0.178, 0.125],
    f"{worst}",
)
# Omitted-variable bias in a simulated design with correlated regressors.
rng = np.random.default_rng(20261020)
m_sim = 400
z1 = rng.standard_normal(m_sim)
z2 = 0.6 * z1 + 0.8 * rng.standard_normal(m_sim)
y_sim = 1.0 + 0.5 * z1 + 0.8 * z2 + rng.standard_normal(m_sim)
full_sim = sm.OLS(y_sim, sm.add_constant(np.column_stack([z1, z2]))).fit().params
short_sim = sm.OLS(y_sim, sm.add_constant(z1)).fit().params[1]
delta = sm.OLS(z2, sm.add_constant(z1)).fit().params[1]
ok(
    "omitted-variable bias (simulated, corr 0.6): the short regression's slope equals b1 + b2 x delta exactly in "
    "sample: 0.422 + 0.797 x 0.556 = 0.865, against a true partial effect of 0.5",
    close(short_sim, full_sim[1] + full_sim[2] * delta, 1e-10) and round(short_sim, 3) == 0.865,
    f"short {short_sim:.3f}, full {full_sim[1]:.3f}, delta {delta:.3f}",
)

# ---------------------------------------------------------------------------------------------
print("== part 2: goodness of fit, ANOVA, joint tests and prediction")
sst = ((y - y.mean()) ** 2).sum()
sse = (resid**2).sum()
ssr = sst - sse
r2 = ssr / sst
adj = 1 - (1 - r2) * (n - 1) / (n - k - 1)
F = (ssr / k) / (sse / (n - k - 1))
see = np.sqrt(sse / (n - k - 1))
ok(
    "ANOVA: R2 0.597, adjusted 0.589, F 70.4 on (2, 95), standard error of estimate 5.06%; matches statsmodels",
    round(r2, 3) == 0.597
    and round(adj, 3) == 0.589
    and round(F, 1) == 70.4
    and round(see, 4) == 0.0506
    and close(F, fit.fvalue, 1e-8)
    and close(adj, fit.rsquared_adj, 1e-12),
)
ok(
    "coefficient t statistics: bond 9.80, stock 6.26, intercept 2.10 (p 0.038)",
    [round(v, 2) for v in fit.tvalues] == [2.10, 9.80, 6.26] and round(fit.pvalues[0], 3) == 0.038,
)
# Nested test: do real estate and gold add anything?
X_big = np.column_stack(
    [X, (d.real_estate - d.tbill_3m).to_numpy(), (d.gold - d.tbill_3m).to_numpy()]
)
big = sm.OLS(y, X_big).fit()
F_nest = ((sse - big.ssr) / 2) / (big.ssr / (n - 5))
f_sm, p_sm, _ = big.compare_f_test(fit)
ok(
    "general linear F test: adding real-estate and gold excess returns gives F 0.40 (p 0.67); the reduced model stands",
    close(F_nest, f_sm, 1e-9) and round(F_nest, 2) == 0.40 and round(p_sm, 2) == 0.67,
)
sse_no_stock = sm.OLS(y, X[:, :2]).fit().ssr
partial_r2 = (sse_no_stock - sse) / sse_no_stock
ok(
    "partial R2 of the stock factor given the bond factor: 29.2% of the variation left after the bond factor",
    round(partial_r2, 3) == 0.292,
)
x0 = np.array([1.0, 0.05, -0.20])
pred = fit.get_prediction(x0.reshape(1, -1)).summary_frame(alpha=0.05)
xtx_inv = np.linalg.inv(X.T @ X)
se_mean = see * np.sqrt(x0 @ xtx_inv @ x0)
se_new = see * np.sqrt(1 + x0 @ xtx_inv @ x0)
tcrit = 1.985251
ok(
    "prediction for a year with bond excess +5% and stock excess -20%: Baa excess +1.2%; 95% interval for the "
    "year -9.0% to +11.4% (by hand and by statsmodels)",
    round(float(x0 @ b), 3) == 0.012
    and close(pred.mean_se.iloc[0], se_mean, 1e-12)
    and abs(pred.obs_ci_lower.iloc[0] - (x0 @ b - tcrit * se_new)) < 1e-5
    and [round(pred.obs_ci_lower.iloc[0], 3), round(pred.obs_ci_upper.iloc[0], 3)]
    == [-0.090, 0.114],
)

# ---------------------------------------------------------------------------------------------
print("== part 3: misspecification - heteroskedasticity, serial correlation, multicollinearity")
bp = het_breuschpagan(resid, X)
wh = het_white(resid, X)
ok(
    "Breusch-Pagan LM 0.88 (p 0.65) finds no variance linked linearly to the regressors; White's test, with "
    "squares and the cross-product, gives 13.7 (p 0.017)",
    round(bp[0], 2) == 0.88
    and round(bp[1], 2) == 0.65
    and round(wh[0], 1) == 13.7
    and round(wh[1], 3) == 0.017,
)
hc1 = fit.get_robustcov_results("HC1").bse
nw = fit.get_robustcov_results("HAC", maxlags=2).bse
ok(
    "robust standard errors: bond 0.067 (OLS) -> 0.085 (White HC1) -> 0.104 (Newey-West, 2 lags); stock "
    "0.026 -> 0.030 -> 0.032; both slopes stay significant",
    [round(v, 3) for v in (fit.bse[1], hc1[1], nw[1])] == [0.067, 0.085, 0.104]
    and [round(v, 3) for v in (fit.bse[2], hc1[2], nw[2])] == [0.026, 0.030, 0.032]
    and fit.params[1] / nw[1] > 6
    and fit.params[2] / nw[2] > 5,
)
dw = durbin_watson(resid)
r1 = np.corrcoef(resid[1:], resid[:-1])[0, 1]
ok(
    "Durbin-Watson 1.88, about 2(1 - r1) with first-order residual autocorrelation 0.05: no serial correlation",
    round(dw, 2) == 1.88 and round(r1, 2) == 0.05 and abs(dw - 2 * (1 - r1)) < 0.05,
)
vif = [variance_inflation_factor(X, i) for i in (1, 2)]
ok(
    "VIFs 1.002: no multicollinearity (VIF = 1/(1 - R2_j) with R2_j = 0.044^2)",
    all(round(v, 3) == 1.002 for v in vif) and close(vif[0], 1 / (1 - rho**2), 1e-9),
)
rng = np.random.default_rng(20261021)
w1 = rng.standard_normal(200)
w2 = 0.95 * w1 + np.sqrt(1 - 0.95**2) * rng.standard_normal(200)
yw = 1 + 0.5 * w1 + 0.5 * w2 + rng.standard_normal(200)
Xw = sm.add_constant(np.column_stack([w1, w2]))
fw = sm.OLS(yw, Xw).fit()
vif_w = variance_inflation_factor(Xw, 1)
f_one = sm.OLS(yw, sm.add_constant(w1)).fit()
ok(
    "simulated collinearity (corr 0.95): VIF 12.3; the slope's standard error is 3.5 times that of a "
    "one-regressor fit (about the square root of the VIF), yet the joint F test is overwhelming",
    round(vif_w, 1) == 12.3 and round(fw.bse[1] / f_one.bse[1], 1) == 3.5 and fw.f_pvalue < 1e-20,
    f"VIF {vif_w:.1f}, SE ratio {fw.bse[1] / f_one.bse[1]:.2f}, t {fw.tvalues[1]:.2f}, {fw.tvalues[2]:.2f}",
)


# Added 2026-10-20 (audit): the direction of the bias in the usual OLS standard error under serially correlated errors
# depends on the design. Exact: Var(b | X) = (X'X)^-1 X' Omega X (X'X)^-1 against E(s^2) (X'X)^-1, with
# E(s^2) = tr(M Omega) / (n - k). Independent route: a seeded simulation of AR(1) errors.
def ar1_variance_ratio(x, rho_e):
    m = len(x)
    Xd = np.column_stack([np.ones(m), x])
    idx = np.arange(m)
    om = rho_e ** np.abs(idx[:, None] - idx[None, :]) / (1 - rho_e**2)
    xtxi = np.linalg.inv(Xd.T @ Xd)
    true_var = (xtxi @ Xd.T @ om @ Xd @ xtxi)[1, 1]
    resid_maker = np.eye(m) - Xd @ xtxi @ Xd.T
    usual = np.trace(resid_maker @ om) / (m - 2) * xtxi[1, 1]
    return true_var / usual


trend10 = np.arange(1, 11, dtype=float)
alt10 = (-1.0) ** np.arange(1, 11)
ratios = {
    (nm, r_): ar1_variance_ratio(xv, r_)
    for nm, xv in (("trend", trend10), ("alternating", alt10))
    for r_ in (0.5, -0.5)
}
ok(
    "ten observations, intercept, AR(1) errors: true / expected usual slope variance is 2.75 (trend, rho 0.5), "
    "0.41 (trend, -0.5), 0.43 (alternating, 0.5) and 2.96 (alternating, -0.5) - positive autocorrelation "
    "overstates the usual standard error for the alternating regressor",
    [
        round(ratios[k_], 2)
        for k_ in (("trend", 0.5), ("trend", -0.5), ("alternating", 0.5), ("alternating", -0.5))
    ]
    == [2.75, 0.41, 0.43, 2.96]
    and ratios[("alternating", 0.5)] < 1 < ratios[("trend", 0.5)],
    ", ".join(f"{k_} {v:.3f}" for k_, v in ratios.items()),
)
rng_ar = np.random.default_rng(20261020)
Xa = np.column_stack([np.ones(10), alt10])
sims_b, sims_v = [], []
for _ in range(20000):
    e = np.empty(10)
    e[0] = rng_ar.standard_normal() / np.sqrt(1 - 0.25)
    for t_ in range(1, 10):
        e[t_] = 0.5 * e[t_ - 1] + rng_ar.standard_normal()
    fa = np.linalg.lstsq(Xa, e, rcond=None)
    sims_b.append(fa[0][1])
    sims_v.append(fa[1][0] / 8 * np.linalg.inv(Xa.T @ Xa)[1, 1])
ok(
    "simulation (20,000 draws, rho 0.5, alternating regressor): the slope's sampling variance is below the average "
    "usual estimate, ratio within 0.02 of the exact 0.43",
    abs(np.var(sims_b) / np.mean(sims_v) - ratios[("alternating", 0.5)]) < 0.02,
    f"{np.var(sims_b) / np.mean(sims_v):.4f}",
)
X_pct = np.column_stack([np.ones(n), x_bond, 100 * x_stock])
fit_pct = sm.OLS(y, X_pct).fit()
ok(
    "units: the stock excess return in percentage points divides its slope and standard error by 100; t, R2 and "
    "fitted values are unchanged",
    close(fit_pct.params[2] * 100, fit.params[2], 1e-12)
    and close(fit_pct.bse[2] * 100, fit.bse[2], 1e-12)
    and close(fit_pct.tvalues[2], fit.tvalues[2], 1e-9)
    and close(fit_pct.rsquared, fit.rsquared, 1e-12)
    and np.allclose(fit_pct.fittedvalues, fit.fittedvalues, atol=1e-12),
)

# ---------------------------------------------------------------------------------------------
print("== part 4: influential observations, dummy variables and logistic regression")
inf = OLSInfluence(fit)
H = X @ xtx_inv @ X.T
lev = np.diag(H)
ok(
    "leverage from the hat matrix equals statsmodels' and averages p/n = 3/98",
    np.allclose(lev, inf.hat_matrix_diag, atol=1e-12) and close(lev.mean(), 3 / n, 1e-12),
)
flag = yr[lev > 3 * 3 / n]
ok(
    "leverage above 3p/n = 0.092 flags 1931 (0.094), 2008 (0.125) and 2022 (0.109), years with extreme "
    "regressor values; 2022 is the year stocks and Treasuries fell together",
    flag.tolist() == [1931, 2008, 2022]
    and [round(v, 3) for v in lev[lev > 9 / n]] == [0.094, 0.125, 0.109],
    f"{sorted(flag.tolist())}",
)
sdr = inf.resid_studentized_external
cook = inf.cooks_distance[0]
i09 = int(np.where(yr == 2009)[0][0])
ok(
    "2009 is an outlier in y (studentized deleted residual 4.95) but not influential by Cook's rule "
    "(D = 0.33 < 0.5); no year has D above 0.5",
    round(sdr[i09], 2) == 4.95 and round(cook[i09], 2) == 0.33 and cook.max() < 0.5,
)
keep = yr != 2009
fit_x09 = sm.OLS(y[keep], X[keep]).fit()
ok(
    "dropping 2009 moves the bond beta from 0.660 to 0.713 and the stock beta from 0.163 to 0.152",
    round(fit_x09.params[1], 3) == 0.713 and round(fit_x09.params[2], 3) == 0.152,
)
post = (yr >= 1980).astype(float)
Xd = np.column_stack([X, post, x_stock * post])
fd = sm.OLS(y, Xd).fit()
ok(
    "dummy variables: a post-1980 intercept shift of 0.12 points (p 0.91) and slope shift on stocks of 0.065 "
    "(p 0.25): no evidence the relation changed",
    round(fd.params[3], 4) == 0.0012
    and round(fd.pvalues[3], 2) == 0.91
    and round(fd.params[4], 3) == 0.065
    and round(fd.pvalues[4], 2) == 0.25,
)
under = ((d.baa_corp - d.tbond_10y) < 0).astype(float).to_numpy()
Xl = np.column_stack([np.ones(n), x_stock])
lg = sm.Logit(under, Xl).fit(disp=0)
beta = np.zeros(2)
for _ in range(50):
    p_hat = 1 / (1 + np.exp(-Xl @ beta))
    W = p_hat * (1 - p_hat)
    beta = beta + np.linalg.solve(Xl.T @ (Xl * W[:, None]), Xl.T @ (under - p_hat))
probs = [1 / (1 + np.exp(-(beta[0] + beta[1] * v))) for v in (-0.20, 0.0, 0.20)]
ok(
    "logistic regression of 'Baa underperforms Treasuries' (31 of 98 years) on the stock excess return: "
    "-0.486 - 5.01 x; Newton-Raphson equals statsmodels; probability 62.6% after a -20% stock year, 38.1% at 0, "
    "18.4% at +20%; odds fall by 39% per 10 points of stock return",
    int(under.sum()) == 31
    and np.allclose(beta, lg.params, atol=1e-8)
    and [round(v, 3) for v in beta] == [-0.486, -5.013]
    and [round(p, 3) for p in probs] == [0.626, 0.381, 0.184]
    and round(1 - np.exp(beta[1] * 0.10), 2) == 0.39,
)

print(f"\n{n_checks} checks executed")
if fails:
    print("FAILED:", fails)
    sys.exit(1)
print("all checks passed")
