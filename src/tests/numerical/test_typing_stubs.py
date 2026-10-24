"""Tests that the local statsmodels and pandas stubs describe what the pinned libraries return.

src/typings/ types only the calls the numerical checks make, and mypy trusts it without looking at
the libraries. These make each of those calls on float64 arrays, as the checks do, and compare
the runtime type with the declared one, so that a library upgrade that changes a result's type
(an ndarray becoming a pandas object, say) fails here rather than passing mypy unnoticed.

Run: make test (uv run --frozen --no-editable pytest)
"""

import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.diagnostic import acorr_ljungbox, het_arch, het_breuschpagan, het_white
from statsmodels.stats.outliers_influence import OLSInfluence, variance_inflation_factor
from statsmodels.stats.stattools import durbin_watson
from statsmodels.tools.sm_exceptions import InterpolationWarning
from statsmodels.tsa.adfvalues import mackinnoncrit
from statsmodels.tsa.stattools import acf, adfuller, coint, kpss


class StubbedTypes(unittest.TestCase):
    """Each stubbed call returns the type its stub declares."""

    def test_ols_on_arrays(self) -> None:
        """OLS fitted on arrays returns ndarrays and NumPy scalars, as the stubs say."""
        x = np.arange(10.0)
        y = 1 + 2 * x + np.random.default_rng(1).normal(size=10)
        X = sm.add_constant(x)
        self.assertIs(type(X), np.ndarray)
        fit = sm.OLS(y, X).fit()
        for array in (fit.params, fit.bse, fit.tvalues, fit.pvalues, fit.resid, fit.conf_int()):
            self.assertIs(type(array), np.ndarray)
            self.assertEqual(array.dtype, np.float64)
        for scalar in (fit.fvalue, fit.rsquared, fit.mse_resid):
            self.assertIs(type(scalar), np.float64)
        contrast = fit.f_test((np.array([[0.0, 1.0]]), np.array([2.0])))
        self.assertIsInstance(contrast.fvalue, float | np.ndarray)
        self.assertIsInstance(contrast.pvalue, np.float64 | np.ndarray)
        influence = fit.get_influence().resid_studentized_internal
        self.assertIs(type(influence), np.ndarray)
        frame = fit.get_prediction(np.array([[1.0, 4.0]])).summary_frame(alpha=0.05)
        self.assertIs(type(frame), pd.DataFrame)
        self.assertIs(type(frame[["mean_ci_lower", "obs_ci_upper"]]), pd.DataFrame)
        self.assertEqual(frame[["mean_ci_lower", "obs_ci_upper"]].values.dtype, np.float64)
        self.assertIsInstance(statsmodels.__version__, str)

    def test_formula_anova_and_frames(self) -> None:
        """anova_lm returns a frame whose columns are Series of NumPy float64 scalars."""
        x = np.arange(10.0)
        y = 1 + 2 * x + np.random.default_rng(2).normal(size=10)
        table = anova_lm(smf.ols("y ~ x", data=pd.DataFrame({"y": y, "x": x})).fit())
        self.assertIs(type(table), pd.DataFrame)
        self.assertIs(type(table["sum_sq"]), pd.Series)
        self.assertIs(type(table["sum_sq"].iloc[0]), np.float64)

    def test_read_csv_columns(self) -> None:
        """read_csv skips comments, iterates column names and converts columns to typed arrays."""
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "table.csv"
            path.write_text("# a comment\nlabel,x\n1,0.5\n2,\n")
            frame = pd.read_csv(path, comment="#")
        self.assertIs(type(frame), pd.DataFrame)
        self.assertEqual([type(c) for c in frame], [str, str])
        labels, x = frame["label"].to_numpy(dtype=np.int64), frame["x"].to_numpy(dtype=np.float64)
        self.assertEqual((type(labels), labels.dtype), (np.ndarray, np.int64))
        self.assertEqual((type(x), x.dtype), (np.ndarray, np.float64))
        self.assertTrue(np.isnan(x[1]))
        self.assertIsInstance(pd.__version__, str)

    def test_adfuller_tuple(self) -> None:
        """Without a result object, adfuller returns the declared five- or six-tuple."""
        walk = np.cumsum(np.random.default_rng(3).normal(size=200))
        result = adfuller(walk, maxlag=1, regression="c", autolag=None, result_object=False)
        self.assertEqual([type(value) for value in result], [float, float, int, int, dict])
        self.assertTrue(all(type(v) is np.float64 for v in result[4].values()))
        chosen = adfuller(walk, regression="c", autolag="AIC", result_object=False)
        self.assertEqual(
            [type(value) for value in chosen], [float, float, int, int, dict, np.float64]
        )

    def test_regression_extras_and_diagnostics(self) -> None:
        """The further OLS results, robust and HAC fits, diagnostics and Logit, as stubbed."""
        rng = np.random.default_rng(4)
        X = sm.add_constant(rng.normal(size=(60, 2)))
        y = X @ np.array([1.0, 2.0, 3.0]) + rng.normal(size=60)
        fit = sm.OLS(y, X).fit()
        restricted = sm.OLS(y, X[:, :2]).fit()
        for scalar in (fit.rsquared_adj, fit.f_pvalue, fit.ssr, fit.aic, fit.bic):
            self.assertIs(type(scalar), np.float64)
        self.assertIs(type(fit.fittedvalues), np.ndarray)
        self.assertEqual([type(v) for v in fit.compare_f_test(restricted)], [np.float64] * 3)
        for robust in (
            fit.get_robustcov_results("HC1"),
            fit.get_robustcov_results("HAC", maxlags=2),
            sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": 4}),
        ):
            self.assertIs(type(robust.bse), np.ndarray)
            self.assertIs(type(robust.tvalues), np.ndarray)
        for test in (het_breuschpagan(fit.resid, X), het_white(fit.resid, X)):
            self.assertEqual([type(v) for v in test], [np.float64] * 4)
        arch = het_arch(fit.resid, nlags=1, result_object=False)
        self.assertEqual([type(v) for v in arch], [np.float64, np.float64, float, float])
        influence = OLSInfluence(fit)
        for array in (
            influence.hat_matrix_diag,
            influence.resid_studentized_external,
            *influence.cooks_distance,
        ):
            self.assertIs(type(array), np.ndarray)
        self.assertIs(type(variance_inflation_factor(X, 1)), np.float64)
        self.assertIs(type(durbin_watson(fit.resid)), np.float64)
        logit = sm.Logit((y > 3).astype(float), X).fit(disp=0)
        self.assertIs(type(logit.params), np.ndarray)
        ljung_box = acorr_ljungbox(fit.resid, lags=[1, 2])
        self.assertIs(type(ljung_box), pd.DataFrame)
        self.assertIs(type(ljung_box["lb_pvalue"].iloc[0]), np.float64)
        frame = fit.get_prediction(np.array([[1.0, 0.1, 0.2]])).summary_frame(alpha=0.05)
        self.assertIs(type(frame["mean_se"].iloc[0]), np.float64)

    def test_time_series_tests(self) -> None:
        """KPSS, the ACF, the Engle-Granger test and MacKinnon's critical values, as stubbed."""
        rng = np.random.default_rng(5)
        walk = np.cumsum(rng.normal(size=200))
        with self.assertWarns(InterpolationWarning):
            result = kpss(walk, regression="c", nlags="auto", result_object=False)
        self.assertEqual([type(v) for v in result], [np.float64, np.float64, int, dict])
        correlations = acf(walk, nlags=4)
        self.assertEqual((type(correlations), correlations.dtype), (np.ndarray, np.float64))
        test = coint(walk, walk + rng.normal(size=200))
        self.assertEqual([type(v) for v in test], [float, float, np.ndarray])
        critical = mackinnoncrit(N=2, regression="c", nobs=199)
        self.assertEqual((type(critical), critical.dtype), (np.ndarray, np.float64))


if __name__ == "__main__":
    unittest.main()
