"""Multiple regression: formulation, fit, misspecification and extensions."""

import sys
from collections.abc import Sequence
from typing import Final

import numpy as np
import statsmodels
import statsmodels.api as sm
from numpy.typing import NDArray
from statsmodels.regression.linear_model import RegressionResults
from statsmodels.stats.diagnostic import het_breuschpagan, het_white
from statsmodels.stats.outliers_influence import OLSInfluence, variance_inflation_factor
from statsmodels.stats.stattools import durbin_watson

from trading_notes.numerical.multiple_regression.least_squares import (
    LeastSquares,
    ar1_ols_variance_ratio,
    newton_logit,
)
from trading_notes.numerical.portfolio_choice.history import DATA, AssetClassHistory
from trading_notes.numerical.report import CheckReport, print_versions
from trading_notes.numerical.repository import repository_root
from trading_notes.numerical.tolerance import close
from trading_notes.records import Record

type Floats = NDArray[np.float64]

T_CRIT: Final = 1.985251  # the 97.5% t quantile on 95 degrees of freedom


class BaaRegression(Record):
    """Baa corporate bond excess returns on Treasury and S&P 500 excess returns, 1928-2025.

    Excess returns are over 3-month bills, in decimals.

    Attributes:
        history: The annual asset-class returns.
    """

    history: AssetClassHistory

    def excess(self, name: str) -> Floats:
        """Return one series' annual return over the 3-month bill."""
        excess: Floats = self.history.series[name] - self.history.series["tbill_3m"]
        return excess

    @property
    def years(self) -> NDArray[np.int_]:
        """Return the calendar years."""
        return self.history.years

    @property
    def y(self) -> Floats:
        """Return the Baa excess return."""
        return self.excess("baa_corp")

    @property
    def x_bond(self) -> Floats:
        """Return the 10-year Treasury excess return."""
        return self.excess("tbond_10y")

    @property
    def x_stock(self) -> Floats:
        """Return the S&P 500 excess return."""
        return self.excess("sp500")

    @property
    def design(self) -> Floats:
        """Return the design: a constant, the bond and the stock excess returns."""
        return np.column_stack([np.ones(len(self.y)), self.x_bond, self.x_stock])


def check_formulation(report: CheckReport, data: BaaRegression) -> RegressionResults:
    """Part 1: the regression, its residuals and omitted-variable bias.

    Returns:
        The statsmodels fit of the two-factor regression, which later parts reuse.
    """
    print("== part 1: formulating the regression")
    y, X, n = data.y, data.design, len(data.y)
    ls = LeastSquares(design=X, response=y)
    b = ls.coefficients()
    fit = sm.OLS(y, X).fit()
    report.ok(
        "98 years; normal equations and statsmodels agree: intercept 1.18%, bond beta 0.660, stock"
        " beta 0.163",
        n == 98
        and np.allclose(b, fit.params, atol=1e-12)
        and [round(v, 4) for v in b] == [0.0118, 0.6599, 0.1632],
    )
    b_bond_only = sm.OLS(y, X[:, :2]).fit().params[1]
    b_stock_only = sm.OLS(y, X[:, [0, 2]]).fit().params[1]
    rho = np.corrcoef(data.x_bond, data.x_stock)[0, 1]
    report.ok(
        "the regressors are nearly uncorrelated (0.044), so the simple-regression slopes (0.678,"
        " 0.174) are close to the partial ones",
        bool(
            round(rho, 3) == 0.044
            and round(b_bond_only, 3) == 0.678
            and round(b_stock_only, 3) == 0.174
        ),
    )
    resid, fitted = ls.residuals(), ls.fitted()
    report.ok(
        "residuals are orthogonal to the fitted values and to each regressor (a property of least"
        " squares, so a residual plot tests shape, not mean)",
        bool(abs(resid @ fitted) < 1e-10 and np.allclose(X.T @ resid, 0, atol=1e-10)),
    )
    order = np.argsort(-np.abs(resid))[:3]
    worst = data.years[order]
    report.ok(
        "largest residuals: 2009 (+21.9%), 1932 (+17.8%) and 1934 (+12.5%), all rebounds after"
        " credit crises that the two factors do not capture",
        list(worst) == [2009, 1932, 1934]
        and [round(v, 3) for v in resid[order]] == [0.219, 0.178, 0.125],
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
    report.ok(
        "omitted-variable bias (simulated, corr 0.6): the short regression's slope equals b1 + b2 x"
        " delta exactly in sample: 0.422 + 0.797 x 0.556 = 0.865, against a true partial effect of"
        " 0.5",
        close(short_sim, full_sim[1] + full_sim[2] * delta, 1e-10) and round(short_sim, 3) == 0.865,
        f"short {short_sim:.3f}, full {full_sim[1]:.3f}, delta {delta:.3f}",
    )
    return fit


def check_fit_and_tests(report: CheckReport, data: BaaRegression, fit: RegressionResults) -> None:
    """Part 2: goodness of fit, ANOVA, nested and partial tests, and a prediction interval."""
    print("== part 2: goodness of fit, ANOVA, joint tests and prediction")
    y, X, n = data.y, data.design, len(data.y)
    ls = LeastSquares(design=X, response=y)
    r2, adj, F, see = ls.r_squared, ls.adjusted_r_squared, ls.f_statistic, ls.standard_error
    report.ok(
        "ANOVA: R2 0.597, adjusted 0.589, F 70.4 on (2, 95), standard error of estimate 5.06%;"
        " matches statsmodels",
        round(r2, 3) == 0.597
        and round(adj, 3) == 0.589
        and round(F, 1) == 70.4
        and round(see, 4) == 0.0506
        and close(F, fit.fvalue, 1e-8)
        and close(adj, fit.rsquared_adj, 1e-12),
    )
    report.ok(
        "coefficient t statistics: bond 9.80, stock 6.26, intercept 2.10 (p 0.038)",
        bool(
            [round(v, 2) for v in fit.tvalues] == [2.10, 9.80, 6.26]
            and round(fit.pvalues[0], 3) == 0.038
        ),
    )
    # Nested test: do real estate and gold add anything?
    X_big = np.column_stack([X, data.excess("real_estate"), data.excess("gold")])
    big = sm.OLS(y, X_big).fit()
    F_nest = ((ls.sse - big.ssr) / 2) / (big.ssr / (n - 5))
    f_sm, p_sm, _ = big.compare_f_test(fit)
    report.ok(
        "general linear F test: adding real-estate and gold excess returns gives F 0.40 (p 0.67);"
        " the reduced model stands",
        bool(close(F_nest, f_sm, 1e-9) and round(F_nest, 2) == 0.40 and round(p_sm, 2) == 0.67),
    )
    sse_no_stock = sm.OLS(y, X[:, :2]).fit().ssr
    partial_r2 = (sse_no_stock - ls.sse) / sse_no_stock
    report.ok(
        "partial R2 of the stock factor given the bond factor: 29.2% of the variation left after"
        " the bond factor",
        round(partial_r2, 3) == 0.292,
    )
    x0 = np.array([1.0, 0.05, -0.20])
    pred = fit.get_prediction(x0.reshape(1, -1)).summary_frame(alpha=0.05)
    se_mean, se_new = ls.mean_prediction_se(x0), ls.new_prediction_se(x0)
    lower, upper = pred["obs_ci_lower"].iloc[0], pred["obs_ci_upper"].iloc[0]
    b = ls.coefficients()
    report.ok(
        "prediction for a year with bond excess +5% and stock excess -20%: Baa excess +1.2%; 95%"
        " interval for the year -9.0% to +11.4% (by hand and by statsmodels)",
        bool(
            round(float(x0 @ b), 3) == 0.012
            and close(pred["mean_se"].iloc[0], se_mean, 1e-12)
            and abs(lower - (x0 @ b - T_CRIT * se_new)) < 1e-5
            and [round(lower, 3), round(upper, 3)] == [-0.090, 0.114]
        ),
    )


def check_misspecification(
    report: CheckReport, data: BaaRegression, fit: RegressionResults
) -> None:
    """Part 3: heteroskedasticity, serial correlation, multicollinearity and units."""
    print("== part 3: misspecification - heteroskedasticity, serial correlation, multicollinearity")
    y, X, n = data.y, data.design, len(data.y)
    resid = LeastSquares(design=X, response=y).residuals()
    bp = het_breuschpagan(resid, X)
    wh = het_white(resid, X)
    report.ok(
        "Breusch-Pagan LM 0.88 (p 0.65) finds no variance linked linearly to the regressors;"
        " White's test, with squares and the cross-product, gives 13.7 (p 0.017)",
        bool(
            round(bp[0], 2) == 0.88
            and round(bp[1], 2) == 0.65
            and round(wh[0], 1) == 13.7
            and round(wh[1], 3) == 0.017
        ),
    )
    hc1 = fit.get_robustcov_results("HC1").bse
    nw = fit.get_robustcov_results("HAC", maxlags=2).bse
    report.ok(
        "robust standard errors: bond 0.067 (OLS) -> 0.085 (White HC1) -> 0.104 (Newey-West, 2"
        " lags); stock 0.026 -> 0.030 -> 0.032; both slopes stay significant",
        bool(
            [round(v, 3) for v in (fit.bse[1], hc1[1], nw[1])] == [0.067, 0.085, 0.104]
            and [round(v, 3) for v in (fit.bse[2], hc1[2], nw[2])] == [0.026, 0.030, 0.032]
            and fit.params[1] / nw[1] > 6
            and fit.params[2] / nw[2] > 5
        ),
    )
    dw = durbin_watson(resid)
    r1 = np.corrcoef(resid[1:], resid[:-1])[0, 1]
    report.ok(
        "Durbin-Watson 1.88, about 2(1 - r1) with first-order residual autocorrelation 0.05: no"
        " serial correlation",
        bool(round(dw, 2) == 1.88 and round(r1, 2) == 0.05 and abs(dw - 2 * (1 - r1)) < 0.05),
    )
    rho = np.corrcoef(data.x_bond, data.x_stock)[0, 1]
    vif = [variance_inflation_factor(X, i) for i in (1, 2)]
    report.ok(
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
    report.ok(
        "simulated collinearity (corr 0.95): VIF 12.3; the slope's standard error is 3.5 times that"
        " of a one-regressor fit (about the square root of the VIF), yet the joint F test is"
        " overwhelming",
        bool(
            round(vif_w, 1) == 12.3
            and round(fw.bse[1] / f_one.bse[1], 1) == 3.5
            and fw.f_pvalue < 1e-20
        ),
        f"VIF {vif_w:.1f}, SE ratio {fw.bse[1] / f_one.bse[1]:.2f}, t {fw.tvalues[1]:.2f},"
        f" {fw.tvalues[2]:.2f}",
    )
    # The direction of the bias in the usual OLS standard error under serially correlated errors
    # depends on the design: exactly, and by a seeded simulation of AR(1) errors.
    trend10 = np.arange(1, 11, dtype=np.float64)
    alt10 = np.asarray((-1.0) ** np.arange(1, 11), dtype=np.float64)
    ratios = {
        (nm, r_): ar1_ols_variance_ratio(xv, r_)
        for nm, xv in (("trend", trend10), ("alternating", alt10))
        for r_ in (0.5, -0.5)
    }
    report.ok(
        "ten observations, intercept, AR(1) errors: true / expected usual slope variance is 2.75"
        " (trend, rho 0.5), 0.41 (trend, -0.5), 0.43 (alternating, 0.5) and 2.96 (alternating,"
        " -0.5) - positive autocorrelation overstates the usual standard error for the alternating"
        " regressor",
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
    report.ok(
        "simulation (20,000 draws, rho 0.5, alternating regressor): the slope's sampling variance"
        " is below the average usual estimate, ratio within 0.02 of the exact 0.43",
        bool(abs(np.var(sims_b) / np.mean(sims_v) - ratios[("alternating", 0.5)]) < 0.02),
        f"{np.var(sims_b) / np.mean(sims_v):.4f}",
    )
    X_pct = np.column_stack([np.ones(n), data.x_bond, 100 * data.x_stock])
    fit_pct = sm.OLS(y, X_pct).fit()
    report.ok(
        "units: the stock excess return in percentage points divides its slope and standard error"
        " by 100; t, R2 and fitted values are unchanged",
        close(fit_pct.params[2] * 100, fit.params[2], 1e-12)
        and close(fit_pct.bse[2] * 100, fit.bse[2], 1e-12)
        and close(fit_pct.tvalues[2], fit.tvalues[2], 1e-9)
        and close(fit_pct.rsquared, fit.rsquared, 1e-12)
        and np.allclose(fit_pct.fittedvalues, fit.fittedvalues, atol=1e-12),
    )


def check_extensions(report: CheckReport, data: BaaRegression, fit: RegressionResults) -> None:
    """Part 4: influential observations, dummy variables and logistic regression."""
    print("== part 4: influential observations, dummy variables and logistic regression")
    y, X, n, yr = data.y, data.design, len(data.y), data.years
    inf = OLSInfluence(fit)
    lev = LeastSquares(design=X, response=y).leverage()
    report.ok(
        "leverage from the hat matrix equals statsmodels' and averages p/n = 3/98",
        np.allclose(lev, inf.hat_matrix_diag, atol=1e-12) and close(lev.mean(), 3 / n, 1e-12),
    )
    flag = yr[lev > 3 * 3 / n]
    report.ok(
        "leverage above 3p/n = 0.092 flags 1931 (0.094), 2008 (0.125) and 2022 (0.109), years with"
        " extreme regressor values; 2022 is the year stocks and Treasuries fell together",
        flag.tolist() == [1931, 2008, 2022]
        and [round(v, 3) for v in lev[lev > 9 / n]] == [0.094, 0.125, 0.109],
        f"{sorted(flag.tolist())}",
    )
    sdr = inf.resid_studentized_external
    cook = inf.cooks_distance[0]
    i09 = int(np.where(yr == 2009)[0][0])
    report.ok(
        "2009 is an outlier in y (studentized deleted residual 4.95) but not influential by Cook's"
        " rule (D = 0.33 < 0.5); no year has D above 0.5",
        bool(round(sdr[i09], 2) == 4.95 and round(cook[i09], 2) == 0.33 and cook.max() < 0.5),
    )
    keep = yr != 2009
    fit_x09 = sm.OLS(y[keep], X[keep]).fit()
    report.ok(
        "dropping 2009 moves the bond beta from 0.660 to 0.713 and the stock beta from 0.163 to"
        " 0.152",
        bool(round(fit_x09.params[1], 3) == 0.713 and round(fit_x09.params[2], 3) == 0.152),
    )
    post = (yr >= 1980).astype(float)
    fd = sm.OLS(y, np.column_stack([X, post, data.x_stock * post])).fit()
    report.ok(
        "dummy variables: a post-1980 intercept shift of 0.12 points (p 0.91) and slope shift on"
        " stocks of 0.065 (p 0.25): no evidence the relation changed",
        bool(
            round(fd.params[3], 4) == 0.0012
            and round(fd.pvalues[3], 2) == 0.91
            and round(fd.params[4], 3) == 0.065
            and round(fd.pvalues[4], 2) == 0.25
        ),
    )
    series = data.history.series
    under = ((series["baa_corp"] - series["tbond_10y"]) < 0).astype(float)
    Xl = np.column_stack([np.ones(n), data.x_stock])
    lg = sm.Logit(under, Xl).fit(disp=0)
    beta = newton_logit(Xl, under)
    probs = [1 / (1 + np.exp(-(beta[0] + beta[1] * v))) for v in (-0.20, 0.0, 0.20)]
    report.ok(
        "logistic regression of 'Baa underperforms Treasuries' (31 of 98 years) on the stock"
        " excess return: -0.486 - 5.01 x; Newton-Raphson equals statsmodels; probability 62.6%"
        " after a -20% stock year, 38.1% at 0, 18.4% at +20%; odds fall by 39% per 10 points of"
        " stock return",
        bool(
            int(under.sum()) == 31
            and np.allclose(beta, lg.params, atol=1e-8)
            and [round(v, 3) for v in beta] == [-0.486, -5.013]
            and [round(p, 3) for p in probs] == [0.626, 0.381, 0.184]
            and round(1 - np.exp(beta[1] * 0.10), 2) == 0.39
        ),
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Read the history from the repository root, then run the four parts with one report.

    The worked numbers of meth:multiple-regression-formulation,
    meth:multiple-regression-fit-tests, meth:regression-misspecification and
    meth:regression-extensions. Data: annual US returns 1928-2025 (Damodaran's histretSP
    workbook, January 2026). The investment problem: how much of the Baa corporate bond excess
    return over bills is explained by Treasury duration (10-year Treasury excess return) and by
    equity-like credit risk (S&P 500 excess return)? Simulated designs (fixed seeds) illustrate
    omitted-variable bias and multicollinearity, which the real data do not show because the two
    regressors are nearly uncorrelated.

    Independent routes: coefficients from the normal equations against statsmodels OLS; the
    ANOVA F and R-squared from sums of squares against statsmodels; the nested F from restricted
    and unrestricted SSE against statsmodels' compare_f_test; the omitted-variable identity
    b_short = b1 + b2 * delta checked exactly in sample; leverage from the hat matrix against
    statsmodels' influence measures; the logistic fit by Newton-Raphson against statsmodels
    Logit. One check is one executed ok() call (a call inside a loop counts once per iteration).

    Args:
        argv: Command-line arguments: `--root DIR`, the repository root that holds the data
            (default: the working directory).

    Returns:
        The exit status, 0 or 1.
    """
    root = repository_root(__doc__ or "", argv)
    print_versions(np, statsmodels)
    data = BaaRegression(history=AssetClassHistory.read(root / DATA))
    report = CheckReport()
    fit = check_formulation(report, data)
    check_fit_and_tests(report, data, fit)
    check_misspecification(report, data, fit)
    check_extensions(report, data, fit)
    print(f"\n{report.count} checks executed")
    if report.failures:
        print("FAILED:", report.failures)
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
