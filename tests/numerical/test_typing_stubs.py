"""Tests that the local statsmodels and pandas stubs describe what the pinned libraries return.

typings/ types only the calls the numerical checks make, and mypy trusts it without looking at
the libraries. These make each of those calls on float64 arrays, as the checks do, and compare
the runtime type with the declared one, so that a library upgrade that changes a result's type
(an ndarray becoming a pandas object, say) fails here rather than passing mypy unnoticed.

Run: make test (uv run --frozen --no-editable pytest)
"""

# standard library imports
import unittest

# third party library imports
import numpy as np
import pandas as pd
import statsmodels
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from statsmodels.tsa.stattools import adfuller


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

    def test_adfuller_tuple(self) -> None:
        """Without autolag or a result object, adfuller returns the declared five-tuple."""
        walk = np.cumsum(np.random.default_rng(3).normal(size=200))
        result = adfuller(walk, maxlag=1, regression="c", autolag=None, result_object=False)
        self.assertEqual([type(value) for value in result], [float, float, int, int, dict])
        self.assertTrue(all(type(v) is np.float64 for v in result[4].values()))


if __name__ == "__main__":
    unittest.main()
