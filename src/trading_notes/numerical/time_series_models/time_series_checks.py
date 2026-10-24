"""Time-series models: trends, unit roots, autoregression, forecasts, ARCH and cointegration."""

import sys
import warnings
from collections.abc import Sequence
from typing import Final

import numpy as np
import statsmodels
import statsmodels.api as sm
from numpy.typing import NDArray
from scipy.stats import f as f_dist
from statsmodels.regression.linear_model import RegressionResults
from statsmodels.stats.diagnostic import acorr_ljungbox, het_arch
from statsmodels.stats.stattools import durbin_watson
from statsmodels.tools.sm_exceptions import InterpolationWarning
from statsmodels.tsa.adfvalues import mackinnoncrit
from statsmodels.tsa.stattools import acf, adfuller, coint, kpss

from trading_notes.numerical.portfolio_choice.history import DATA, AssetClassHistory
from trading_notes.numerical.report import CheckReport, print_versions
from trading_notes.numerical.repository import repository_root
from trading_notes.numerical.time_series_models.forecasting_models import (
    Arch1,
    AutoRegression,
    chow_statistic,
    compounded_change,
    diebold_mariano_t,
    half_life,
    root_mean_square,
)
from trading_notes.numerical.tolerance import close

type Floats = NDArray[np.float64]
type Ints = NDArray[np.int_]

AR1: Final = AutoRegression(order=1)
AR4: Final = AutoRegression(order=4)
H5: Final = 5  # years of the decision-horizon validation


def check_trends(report: CheckReport, infl: Floats) -> None:
    """Part 1: linear and log-linear trends of the price level, and their residuals."""
    print("== part 1: linear and log-linear trend models for the price level")
    cpi = np.asarray(np.cumprod(1 + infl), dtype=np.float64)
    T = len(infl)
    t = np.arange(1, T + 1, dtype=float)
    lin = sm.OLS(cpi, sm.add_constant(t)).fit()
    loglin = sm.OLS(np.log(cpi), sm.add_constant(t)).fit()
    slope_hand = np.cov(t, np.log(cpi), ddof=1)[0, 1] / np.var(t, ddof=1)
    report.ok(
        "the CPI index (1927 = 1) rises from 0.99 to 18.7 by 2025",
        bool(round(cpi[0], 2) == 0.99 and round(cpi[-1], 1) == 18.7),
    )
    report.ok(
        "linear trend: +0.177 index points a year, R2 0.896; log-linear trend: 0.0367 log points a"
        " year (3.73% compound), R2 0.975; slope by hand equals OLS",
        bool(
            round(lin.params[1], 3) == 0.177
            and round(lin.rsquared, 3) == 0.896
            and round(loglin.params[1], 4) == 0.0367
            and round(np.exp(loglin.params[1]) - 1, 4) == 0.0373
            and round(loglin.rsquared, 3) == 0.975
            and close(slope_hand, loglin.params[1], 1e-10)
        ),
    )
    report.ok(
        "both fail the residual check: Durbin-Watson 0.013 (linear) and 0.051 (log-linear), far"
        " below 2, so the residuals are persistent and a deterministic trend misdescribes the"
        " series",
        bool(
            round(durbin_watson(lin.resid), 3) == 0.013
            and round(durbin_watson(loglin.resid), 3) == 0.051
        ),
    )
    fc_2030 = np.exp(loglin.params[0] + loglin.params[1] * (T + 5))
    report.ok(
        "the log-linear trend puts 2025 at 21.8 against an actual 18.7, and 2030 at 26.2: a trend"
        " fitted through the 1930s deflation and the 1970s inflation starts its forecasts 17% away"
        " from where the series is",
        bool(
            round(fc_2030, 1) == 26.2
            and round(np.exp(loglin.fittedvalues[-1]), 1) == 21.8
            and round(np.exp(loglin.fittedvalues[-1]) / cpi[-1] - 1, 2) == 0.17
        ),
    )


def check_unit_roots(report: CheckReport, infl: Floats) -> None:
    """Part 2: random walks, ADF tests on the price level and inflation, and KPSS."""
    print("== part 2: covariance stationarity, random walks and unit roots")
    rng = np.random.default_rng(20261023)
    paths = np.cumsum(rng.standard_normal((5000, 100)), axis=1)
    v10, v100 = paths[:, 9].var(), paths[:, 99].var()
    report.ok(
        "a random walk's variance grows with time (about 10 at t = 10, 100 at t = 100): it is not"
        " covariance stationary",
        bool(9.0 < v10 < 11.0 and 90 < v100 < 110),
        f"{v10:.1f}, {v100:.1f}",
    )
    lc = np.log(np.cumprod(1 + infl))
    adf_level = adfuller(lc, regression="ct", autolag="AIC", result_object=False)
    adf_diff = adfuller(np.diff(lc), regression="c", autolag="AIC", result_object=False)
    adf_inf = adfuller(infl, regression="c", autolag="AIC", result_object=False)
    report.ok(
        "ADF on the log price level with a trend: statistic -2.50, p 0.33: a unit root is not"
        " rejected",
        round(adf_level[0], 2) == -2.50 and round(adf_level[1], 2) == 0.33,
    )
    report.ok(
        "ADF on inflation (lag chosen by AIC): -2.95, p 0.040; on the log difference: -2.55, p"
        " 0.105 - the verdict turns on the lag length and on a 5% line",
        round(adf_inf[0], 2) == -2.95
        and round(adf_inf[1], 3) == 0.040
        and round(adf_diff[0], 2) == -2.55
        and round(adf_diff[1], 3) == 0.105,
    )
    lag_p = [
        adfuller(infl, regression="c", maxlag=L, autolag=None, result_object=False)[1]
        for L in range(5)
    ]
    report.ok(
        "ADF on inflation by fixed lag 0-4: p 0.000, 0.000, 0.000, 0.012, 0.002 - rejected at"
        " every lag; the AIC choice of lag gives the weakest result",
        all(p < 0.05 for p in lag_p)
        and [round(p, 3) for p in lag_p] == [0.0, 0.0, 0.0, 0.012, 0.002],
        ", ".join(f"{p:.3f}" for p in lag_p),
    )
    df_reg = sm.OLS(np.diff(infl), sm.add_constant(infl[:-1])).fit()
    df_stat = adfuller(infl, regression="c", maxlag=0, autolag=None, result_object=False)[0]
    report.ok(
        "the Dickey-Fuller statistic with no augmentation is the t ratio of the lagged level in a"
        " regression of the change on it: -4.85, the same as statsmodels",
        close(df_reg.tvalues[1], df_stat, 1e-8) and round(df_reg.tvalues[1], 2) == -4.85,
    )
    # The statistic lies beyond KPSS's table, so its p-value is the table's bound (a lower bound
    # on the true p-value), which is what the check compares with 0.10.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", InterpolationWarning)
        kp = kpss(infl, regression="c", nlags="auto", result_object=False)
    report.ok(
        "KPSS (null: stationary) on inflation: 0.25, p above 0.10 - consistent with treating"
        " inflation as stationary and the price level as I(1)",
        bool(round(kp[0], 2) == 0.25 and kp[1] >= 0.10),
    )


def check_autoregression(report: CheckReport, infl: Floats) -> None:
    """Part 3: AR(1) mean reversion, residual checks, forecasts and a seasonal lag."""
    print("== part 3: autoregressive models, mean reversion, multi-step forecasts and seasonality")
    ar1 = sm.OLS(infl[1:], sm.add_constant(infl[:-1])).fit()
    b0, b1 = ar1.params
    mrl = b0 / (1 - b1)
    report.ok(
        "AR(1) on 1928-2025 inflation: 1.25% + 0.610 x last year's; mean-reverting level 3.22%;"
        " half-life ln 0.5 / ln 0.610 = 1.40 years",
        bool(
            round(b0, 4) == 0.0125
            and round(b1, 3) == 0.610
            and round(mrl, 4) == 0.0322
            and round(half_life(b1), 2) == 1.40
        ),
    )
    lb_p = acorr_ljungbox(ar1.resid, lags=[1, 2, 4])["lb_pvalue"]
    res_acf = acf(ar1.resid, nlags=4)[1:]
    report.ok(
        "residual autocorrelations at lags 1-4 are 0.07, -0.11, -0.31, 0.19 against 2/sqrt(97) ="
        " 0.20: lag 3 exceeds it, and Ljung-Box at 4 lags gives p 0.005 - the AR(1) leaves"
        " structure",
        bool(
            [round(v, 2) for v in res_acf] == [0.07, -0.11, -0.31, 0.19]
            and abs(res_acf[2]) > 2 / np.sqrt(97)
            and round(lb_p.iloc[2], 3) == 0.005
            and lb_p.iloc[0] > 0.4
        ),
        f"acf {np.round(res_acf, 3)}",
    )
    x_last = infl[-1]
    path_rec = []
    x = x_last
    for _ in range(3):
        x = b0 + b1 * x
        path_rec.append(x)
    path_closed = [mrl + b1**h * (x_last - mrl) for h in (1, 2, 3)]
    report.ok(
        "forecasts from 2025's 2.74%: 2.92%, 3.04%, 3.11% for 2026-2028, by the recursion and by"
        " mean + b1^h (x - mean)",
        np.allclose(path_rec, path_closed, atol=1e-12)
        and [round(v, 4) for v in path_rec] == [0.0292, 0.0304, 0.0311],
    )
    rng = np.random.default_rng(20261022)
    nq = 120
    q = np.zeros(nq)
    u = rng.standard_normal(nq) * 0.5
    for i in range(nq):
        q[i] = 1.0 + 0.2 * (q[i - 1] if i >= 1 else 0) + 0.6 * (q[i - 4] if i >= 4 else 0) + u[i]
    Yq = q[4:]
    r_ar1 = sm.OLS(Yq, sm.add_constant(q[3:-1])).fit()
    r_sea = sm.OLS(Yq, sm.add_constant(np.column_stack([q[3:-1], q[:-4]]))).fit()
    a1 = acf(r_ar1.resid, nlags=4)[1:]
    a2 = acf(r_sea.resid, nlags=4)[1:]
    report.ok(
        "simulated quarterly series with a seasonal lag: AR(1) residual autocorrelation at lag 4"
        " is 0.58 (limit 0.19); adding the lag-4 term removes it (all below 0.04) and recovers"
        " 0.59 for the seasonal coefficient",
        bool(
            round(a1[3], 2) == 0.58
            and np.all(np.abs(a2) < 0.04)
            and round(r_sea.params[2], 2) == 0.59
        ),
    )
    sb = r_sea.params
    fq1 = sb[0] + sb[1] * q[-1] + sb[2] * q[-4]
    fq2 = sb[0] + sb[1] * fq1 + sb[2] * q[-3]
    report.ok(
        "seasonal-lag forecasts: next quarter 1.193 + 0.164 x 4.94 + 0.589 x 5.35 = 5.16; the one"
        " after uses the first forecast and the observed value four quarters earlier: 4.38",
        bool(
            [round(v, 3) for v in sb] == [1.193, 0.164, 0.589]
            and [round(v, 2) for v in (q[-1], q[-4], q[-3])] == [4.94, 5.35, 3.97]
            and round(fq1, 2) == 5.16
            and round(fq2, 2) == 4.38
        ),
    )


def check_forecast_evaluation(report: CheckReport, infl: Floats, yr: Ints) -> Floats:
    """Part 4: in-sample against out-of-sample accuracy, and coefficient instability.

    Returns:
        The expanding-window AR(1) forecasts for 1990-2025, which part 7 compares.
    """
    print(
        "== part 4: forecast evaluation - in-sample against out-of-sample, and coefficient"
        " instability"
    )
    T = len(infl)
    train = yr <= 1989
    test_idx = np.where(~train)[0]
    actual = infl[test_idx]

    def fit_ar1(x: Floats) -> RegressionResults:
        return sm.OLS(x[1:], sm.add_constant(x[:-1])).fit()

    def rmse(f: Floats) -> float:
        return root_mean_square(actual - f)

    tr_fit = fit_ar1(infl[train])
    tb0, tb1 = tr_fit.params
    f_ar = tb0 + tb1 * infl[test_idx - 1]
    f_rw = infl[test_idx - 1]
    f_mean = np.full(len(test_idx), infl[train].mean())
    report.ok(
        "trained on 1928-1989 (AR coefficient 0.621), tested on 1990-2025: RMSE 1.46% for AR(1),"
        " 1.66% for the random walk, 1.60% for the training mean",
        round(tb1, 3) == 0.621
        and [round(rmse(f) * 100, 2) for f in (f_ar, f_rw, f_mean)] == [1.46, 1.66, 1.60],
    )
    ins = root_mean_square(tr_fit.resid)
    report.ok(
        "the in-sample RMSE (3.69%) is larger than the out-of-sample one only because 1928-1989"
        " was more volatile: RMSEs must be compared on the same test period",
        round(ins * 100, 2) == 3.69 and ins > rmse(f_ar),
    )
    f_exp = np.array(
        [(lambda b: b[0] + b[1] * infl[i - 1])(fit_ar1(infl[:i]).params) for i in test_idx]
    )
    report.ok(
        "re-estimating at every origin (expanding window, time-series cross-validation) gives"
        " RMSE 1.45%",
        round(rmse(f_exp) * 100, 2) == 1.45,
    )
    early, late = fit_ar1(infl[yr <= 1979]), fit_ar1(infl[yr >= 1980])
    p1, p2 = early.params[1], late.params[1]
    chow = chow_statistic(fit_ar1(infl).ssr, early.ssr + late.ssr, 2, T - 1)
    report.ok(
        "subsamples: AR coefficient 0.617 for 1928-1979 and 0.435 for 1980-2025; the Chow test of"
        " equal coefficients gives F 1.03 (p 0.36) - the persistence estimate moves, but the data"
        " cannot reject stability",
        round(p1, 3) == 0.617
        and round(p2, 3) == 0.435
        and round(chow, 2) == 1.03
        and round(1 - f_dist.cdf(chow, 2, T - 5), 2) == 0.36,
    )
    report.ok(
        "half-lives: 1.40 years at the full-sample 0.610 and 0.83 at the 1980-2025 0.435",
        round(half_life(p2), 2) == 0.83,
    )
    return f_exp


def check_arch(report: CheckReport, sp500: Floats) -> None:
    """Part 5: Engle's LM test, ARCH(1) estimation and variance forecasts."""
    print("== part 5: ARCH - testing for and forecasting conditional variance")
    rng = np.random.default_rng(20261020)
    na = 600
    a0, a1_true = 0.0002, 0.5
    e = np.zeros(na)
    z = rng.standard_normal(na)
    for i in range(na):
        s2 = a0 + a1_true * (e[i - 1] ** 2 if i > 0 else a0 / (1 - a1_true))
        e[i] = np.sqrt(s2) * z[i]
    aux = sm.OLS(e[1:] ** 2, sm.add_constant(e[:-1] ** 2)).fit()
    lm = (na - 1) * aux.rsquared
    lm_sm = het_arch(e, nlags=1, result_object=False)
    report.ok(
        "Engle's LM test on 600 simulated ARCH(1) shocks: (T - 1) R2 = 52.1 against"
        " chi-squared(1), p below 1e-12; statsmodels agrees",
        bool(close(lm, lm_sm[0], 1e-8) and round(lm, 1) == 52.1 and lm_sm[1] < 1e-12),
    )
    arch = Arch1.fit(e)
    w_hat, a_hat = arch.omega, arch.alpha
    report.ok(
        "estimates: OLS on squared shocks gives alpha 0.29, maximum likelihood 0.54, against the"
        " true 0.5 - OLS is inefficient (and biased in small samples) with fat-tailed squared"
        " shocks",
        bool(round(aux.params[1], 2) == 0.29 and round(a_hat, 2) == 0.54),
        f"MLE omega {w_hat:.6f}, alpha {a_hat:.3f}",
    )
    s2_next = arch.next_variance(e[-1])
    uncond = arch.unconditional_variance
    h_path = [arch.variance_forecast(e[-1], h) for h in (1, 2, 5)]
    report.ok(
        "variance forecasts revert to the unconditional w/(1 - a) at rate a per step",
        abs(h_path[2] - uncond) < abs(h_path[0] - uncond) and close(h_path[0], s2_next, 1e-15),
        f"next {s2_next:.6f}, h=5 {h_path[2]:.6f}, long run {uncond:.6f}",
    )
    report.ok(
        "with the last shock at -1.74%, next-period variance is 0.000379 (volatility 1.95%),"
        " rising to 0.000421 at two steps and 0.000462 at five towards the long-run 0.000469"
        " (2.17%)",
        bool(
            round(e[-1], 4) == -0.0174
            and [round(v, 6) for v in h_path] == [0.000379, 0.000421, 0.000462]
            and round(uncond, 6) == 0.000469
            and round(np.sqrt(s2_next), 4) == 0.0195
            and round(np.sqrt(uncond), 4) == 0.0217
        ),
    )
    arch_sp = het_arch(sp500 - sp500.mean(), nlags=1, result_object=False)
    report.ok(
        "on annual S&P 500 returns the LM test gives 2.22 (p 0.14): volatility clustering is a"
        " feature of daily and monthly data that annual data barely show",
        bool(round(arch_sp[0], 2) == 2.22 and round(arch_sp[1], 2) == 0.14),
    )


def check_cointegration(report: CheckReport) -> None:
    """Part 6: a cointegrated pair against a spurious regression of independent walks."""
    print("== part 6: cointegration and spurious regression")
    rng = np.random.default_rng(20261021)
    nc = 250
    xw = np.cumsum(rng.standard_normal(nc))
    yc = 2 + 0.8 * xw + rng.standard_normal(nc) * 0.8
    ww = np.cumsum(rng.standard_normal(nc))
    report.ok(
        "both simulated series are I(1): ADF on x does not reject a unit root (p 0.11)",
        adfuller(xw, result_object=False)[1] > 0.10,
    )
    spur = sm.OLS(ww, sm.add_constant(xw)).fit()
    report.ok(
        "spurious regression of an independent random walk on x: slope t 4.74 and R2 0.08, but"
        " Durbin-Watson 0.025",
        bool(
            round(spur.tvalues[1], 2) == 4.74
            and round(spur.rsquared, 2) == 0.08
            and round(durbin_watson(spur.resid), 3) == 0.025
        ),
    )
    eg = sm.OLS(yc, sm.add_constant(xw)).fit()
    t_eg = adfuller(eg.resid, regression="n", maxlag=0, autolag=None, result_object=False)[0]
    crit5 = mackinnoncrit(N=2, regression="c", nobs=nc - 1)[1]
    report.ok(
        "Engle-Granger: the cointegrating regression recovers slope 0.81; the residuals'"
        " Dickey-Fuller t is -16.0 against the Engle-Granger 5% critical value of about -3.36 (not"
        " the ordinary -2.88): cointegrated",
        bool(
            round(eg.params[1], 2) == 0.81
            and round(t_eg, 1) == -16.0
            and round(crit5, 2) == -3.36
            and t_eg < crit5
        ),
    )
    report.ok(
        "statsmodels' coint agrees: p below 1e-10 for the cointegrated pair, 0.84 for the spurious"
        " pair",
        coint(yc, xw)[1] < 1e-10 and round(coint(ww, xw)[1], 2) == 0.84,
    )


def information_criteria(x: Floats, p: int) -> tuple[float, float]:
    """Return the AIC and BIC of an AR(p) fitted to x after its first four values."""
    Xp = np.column_stack([x[4 - j : len(x) - j] for j in range(1, p + 1)])
    r = sm.OLS(x[4:], sm.add_constant(Xp)).fit()
    return float(r.aic), float(r.bic)


def check_model_selection(report: CheckReport, infl: Floats, yr: Ints, f_exp: Floats) -> None:
    """Part 7: AR order by AIC and BIC, out-of-sample and at the decision's horizon."""
    print("== part 7: choosing a model for inflation")
    T = len(infl)
    test_idx = np.where(yr > 1989)[0]
    actual = infl[test_idx]
    crit = {p: information_criteria(infl, p) for p in range(1, 5)}
    report.ok(
        "on a common sample, AIC and BIC both pick AR(4) (AIC -410.0, BIC -397.3) over AR(1)"
        " (-395.0, -389.9)",
        min(crit, key=lambda p: crit[p][0]) == 4
        and min(crit, key=lambda p: crit[p][1]) == 4
        and [round(v, 1) for v in crit[4]] == [-410.0, -397.3]
        and [round(v, 1) for v in crit[1]] == [-395.0, -389.9],
    )
    f_ar4 = []
    for i in test_idx:
        pr = AR4.coefficients(infl[:i])
        f_ar4.append(pr[0] + pr[1:] @ infl[i - 1 : i - 5 : -1])
    rmse_ar4 = root_mean_square(actual - np.array(f_ar4))
    rmse_ar1 = root_mean_square(actual - f_exp)
    report.ok(
        "one-year forecasts (expanding window, 1990-2025): AR(4) RMSE 1.60% against 1.45% for"
        " AR(1)",
        round(rmse_ar4 * 100, 2) == 1.60 and rmse_ar4 > rmse_ar1,
    )
    pre = AR4.coefficients(infl[yr <= 1989])
    post53 = AR4.coefficients(infl[(yr >= 1953) & (yr <= 1989)])
    s53 = infl[yr >= 1953]
    crit53 = {p: information_criteria(s53, p) for p in (1, 4)}
    report.ok(
        "the AR(4) lag-4 coefficient is 0.43 estimated to 1989 but 0.17 on 1953-1989; from 1953"
        " BIC prefers AR(1) (-345.3 against -339.6) and AIC barely separates them (-350.7 against"
        " -349.7): the full-sample preference depends on the pre-1953 years (consistent with, not"
        " proof of, a wartime and Depression effect)",
        bool(
            round(pre[4], 2) == 0.43
            and round(post53[4], 2) == 0.17
            and [round(v, 1) for v in crit53[1]] == [-349.7, -345.3]
            and [round(v, 1) for v in crit53[4]] == [-350.7, -339.6]
        ),
    )
    # Validation at the decision's horizon: cumulative inflation over the five years after each
    # origin. Every model is estimated on data to the origin only; origins 1990-2020 are common to
    # all models and have their five-year outcome observed by 2025. The 1990-2025 data have been
    # examined before, so this is model-selection validation, not a holdout.
    origins = [i for i in range(T) if 1990 <= yr[i] <= 2020]
    act5 = np.array([compounded_change(infl[i + 1 : i + 1 + H5]) for i in origins])
    fc5: dict[str, list[float]] = {"ar1": [], "mean": [], "ar4": [], "rw": [], "trend": []}
    for i in origins:
        xo = infl[: i + 1]
        fc5["ar1"].append(compounded_change(AR1.forecast_path(xo, H5)))
        fc5["ar4"].append(compounded_change(AR4.forecast_path(xo, H5)))
        fc5["mean"].append(compounded_change(np.repeat(xo.mean(), H5)))
        fc5["rw"].append(compounded_change(np.repeat(xo[-1], H5)))
        lp = np.log(np.cumprod(1 + xo))
        tt = np.arange(len(lp))
        slope_, icpt_ = np.polyfit(tt, lp, 1)
        fc5["trend"].append(float(np.exp(icpt_ + slope_ * (len(lp) - 1 + H5) - lp[-1]) - 1))
    err5 = {k_: act5 - np.array(v) for k_, v in fc5.items()}
    rmse5 = {k_: root_mean_square(e) * 100 for k_, e in err5.items()}
    report.ok(
        "31 common origins (1990-2020), five-year cumulative inflation: RMSE AR(1) 5.94, mean"
        " 6.12, AR(4) 7.27, random walk 7.56, trend 19.36 percentage points; mean errors -3.21,"
        " -4.10, -4.63, +0.60, -10.44",
        len(origins) == 31
        and [round(rmse5[k_], 2) for k_ in ("ar1", "mean", "ar4", "rw", "trend")]
        == [5.94, 6.12, 7.27, 7.56, 19.36]
        and [round(err5[k_].mean() * 100, 2) for k_ in ("ar1", "mean", "ar4", "rw", "trend")]
        == [-3.21, -4.10, -4.63, 0.60, -10.44],
        ", ".join(f"{k_} {rmse5[k_]:.3f} ({err5[k_].mean() * 100:+.3f})" for k_ in rmse5),
    )
    e1 = err5["ar1"]
    ac1 = np.corrcoef(e1[:-1], e1[1:])[0, 1]
    report.ok(
        "overlapping windows: AR(1)'s five-year errors autocorrelate at 0.76 at lag 1, so 31"
        " origins carry about 31 / 5 = 6 separate windows",
        round(ac1, 2) == 0.76,
    )

    def dm_t(a: str, b: str) -> float:
        return diebold_mariano_t(err5[a] ** 2 - err5[b] ** 2, maxlags=4)

    report.ok(
        "Diebold-Mariano with Newey-West (4 lags) on squared-error differences: AR(4) vs AR(1) t"
        " 2.61; AR(1) vs mean -0.40; AR(1) vs random walk -1.45 - only the AR(4) gap stands out,"
        " and with about six effective windows even that is indicative",
        [round(dm_t(*pair), 2) for pair in (("ar4", "ar1"), ("ar1", "mean"), ("ar1", "rw"))]
        == [2.61, -0.40, -1.45],
    )
    latest = AR1.forecast_path(infl, H5)
    report.ok(
        "AR(1) on 1928-2025 forecasts 16.4% cumulative for 2026-2030 from 2025's 2.7%; long-run"
        " mean 3.1% against a 1991-2025 average of 2.6%",
        bool(
            round(compounded_change(latest) * 100, 1) == 16.4
            and round(infl[-1] * 100, 1) == 2.7
            and round(infl.mean() * 100, 1) == 3.1
            and round(infl[yr >= 1991].mean() * 100, 1) == 2.6
        ),
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Read the history from the repository root, then run the seven parts with one report.

    The worked numbers of meth:trend-models, def:stationarity-unit-roots,
    meth:autoregressive-forecasting, meth:forecast-accuracy-evaluation,
    mod:arch-conditional-variance, meth:cointegration-testing and
    meth:time-series-model-selection. Data: annual US CPI-U inflation 1928-2025 (Damodaran's
    histretSP workbook, January 2026) and its cumulative price index (1927 = 1). Simulated
    series (fixed seeds) illustrate seasonality, ARCH effects, cointegration and spurious
    regression, where the true model must be known. Every evaluation is chronological: models
    are fitted on data up to an origin and judged on later data only.

    Independent routes: OLS by normal equations against statsmodels; the Dickey-Fuller statistic
    from a hand-run regression against statsmodels' adfuller with no augmentation; forecasts by
    the recursion against the closed-form mean-reverting path; Engle's LM statistic as
    (T - q) R^2 of the auxiliary regression against statsmodels' het_arch; the Engle-Granger
    residual test by hand against statsmodels' coint; the Chow statistic from pooled and
    subsample SSE. One check is one executed ok() call (a call inside a loop counts once per
    iteration).

    Args:
        argv: Command-line arguments: `--root DIR`, the repository root that holds the data
            (default: the working directory).

    Returns:
        The exit status, 0 or 1.
    """
    root = repository_root(__doc__ or "", argv)
    print_versions(np, statsmodels)
    history = AssetClassHistory.read(root / DATA)
    infl, yr = history.series["cpi_inflation"], history.years
    report = CheckReport()
    check_trends(report, infl)
    check_unit_roots(report, infl)
    check_autoregression(report, infl)
    f_exp = check_forecast_evaluation(report, infl, yr)
    check_arch(report, history.series["sp500"])
    check_cointegration(report)
    check_model_selection(report, infl, yr, f_exp)
    print(f"\n{report.count} checks executed")
    if report.failures:
        print("FAILED:", report.failures)
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
