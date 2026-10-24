"""Tests of the labelled table's boundaries and the scoring-rule forecast records."""

# The examples' full runs are tested in test_checks.py. These pin down the shift and first-valid
# boundaries of the table, and the scoring rules against hand-computed values, the quadrature
# reference and their scalar and array return types.

import math
import unittest

import numpy as np
from scipy import stats

from trading_notes.numerical.return_predictability.labelled_table import LabelledTable, lagged
from trading_notes.numerical.return_predictability.scoring_rules import (
    CentralInterval,
    NormalForecast,
    QuantileForecast,
    crps_quadrature,
)

NAN = math.nan


class Shifts(unittest.TestCase):
    """lagged(x, k) is pandas' shift(k) for k >= 0 and rejects negative lags."""

    def test_zero_lag_is_an_unchanged_copy(self) -> None:
        """K = 0 returns equal values in a new array."""
        x = np.array([1.0, 2.0, NAN, 4.0])
        out = lagged(x, 0)
        np.testing.assert_array_equal(out, x)
        self.assertIsNot(out, x)
        out[0] = 9.0
        self.assertEqual(x[0], 1.0)

    def test_lags_inside_and_beyond_the_length(self) -> None:
        """K = 1 and 3 shift; k = 4 and 10 on four rows give all NaN; empty stays empty."""
        x = np.array([1.0, 2.0, 3.0, 4.0])
        np.testing.assert_array_equal(lagged(x), [NAN, 1.0, 2.0, 3.0])
        np.testing.assert_array_equal(lagged(x, 3), [NAN, NAN, NAN, 1.0])
        for k in (4, 10):
            out = lagged(x, k)
            self.assertEqual(out.shape, (4,))
            self.assertTrue(np.isnan(out).all())
        self.assertEqual(lagged(np.array([], dtype=np.float64), 2).shape, (0,))

    def test_negative_lag_is_rejected(self) -> None:
        """A lead is not a lag."""
        with self.assertRaises(ValueError):
            lagged(np.array([1.0, 2.0]), -1)


class FirstValid(unittest.TestCase):
    """The first label with a value, None when the column has none."""

    table = LabelledTable(
        labels=np.array([1990, 1991, 1992], dtype=np.int64),
        columns={"a": np.array([NAN, 2.0, 3.0]), "b": np.array([NAN, NAN, NAN])},
    )

    def test_first_label_with_a_value(self) -> None:
        """Column a starts in 1991."""
        self.assertEqual(self.table.first_valid("a"), 1991)

    def test_all_missing_and_empty_columns_give_none(self) -> None:
        """An all-NaN column and a table without rows have no first valid label."""
        self.assertIsNone(self.table.first_valid("b"))
        empty = LabelledTable(
            labels=np.array([], dtype=np.int64), columns={"a": np.array([], dtype=np.float64)}
        )
        self.assertIsNone(empty.first_valid("a"))

    def test_unknown_column_raises(self) -> None:
        """A column the table lacks is a KeyError, not a missing value."""
        with self.assertRaises(KeyError):
            self.table.first_valid("c")


class NormalScores(unittest.TestCase):
    """Log score and CRPS of N(mean, sd^2) against hand values and the quadrature reference."""

    def test_standard_normal_at_its_mean(self) -> None:
        """-log f(0) = log(2 pi)/2 and CRPS(0) = (sqrt 2 - 1)/sqrt(pi) for N(0, 1)."""
        forecast = NormalForecast(mean=0.0, sd=1.0)
        self.assertAlmostEqual(forecast.log_score(0.0), 0.5 * math.log(2 * math.pi), places=15)
        self.assertAlmostEqual(
            forecast.crps(0.0), (math.sqrt(2) - 1) / math.sqrt(math.pi), places=15
        )

    def test_crps_matches_the_threshold_integral(self) -> None:
        """The closed form equals the quadrature of a separately written normal CDF."""
        forecast = NormalForecast(mean=5.0, sd=20.0)
        for x in (5.0, -15.0, -40.0):
            reference = crps_quadrature(lambda u: float(stats.norm.cdf((u - 5.0) / 20.0)), x)
            self.assertAlmostEqual(forecast.crps(x), reference, delta=1e-7)

    def test_scalar_and_array_contracts(self) -> None:
        """Scalars give float; arrays give float64 arrays of the outcome's shape, elementwise."""
        scalar = NormalForecast(mean=1.0, sd=2.0)
        self.assertIs(type(scalar.crps(0.5)), float)
        self.assertIs(type(scalar.log_score(0.5)), float)
        means, sds, xs = np.array([1.0, 0.0]), np.array([2.0, 1.0]), np.array([0.5, 0.0])
        vector = NormalForecast(mean=means, sd=sds)
        for score in (vector.crps(xs), vector.log_score(xs)):
            self.assertIsInstance(score, np.ndarray)
            self.assertEqual((score.dtype, score.shape), (np.float64, (2,)))
        np.testing.assert_array_equal(
            vector.crps(xs),
            [
                NormalForecast(mean=float(m), sd=float(s)).crps(float(x))
                for m, s, x in zip(means, sds, xs, strict=True)
            ],
        )


class IntervalAndQuantileScores(unittest.TestCase):
    """Interval and quantile scores against hand values, and their decomposition."""

    def test_hand_values(self) -> None:
        """[-1, 1] at alpha 0.1: 2 inside, 2 + 20 x 1 at x = 2; quantile score 0.75."""
        interval = CentralInterval(lower=-1.0, upper=1.0, alpha=0.1)
        self.assertEqual(interval.score(0.0), 2.0)
        self.assertAlmostEqual(interval.score(2.0), 22.0, places=12)
        self.assertAlmostEqual(interval.score(-3.0), 42.0, places=12)
        self.assertEqual(QuantileForecast(value=1.0, level=0.25).score(0.0), 0.75)

    def test_normal_interval_and_quantile_decomposition(self) -> None:
        """N(5, 10^2)'s 90% interval is 5 -/+ 10 z_0.95; it scores 2/alpha x its quantile scores."""
        interval = NormalForecast(mean=5.0, sd=10.0).central_interval(0.1)
        z = 1.6448536269514722
        self.assertAlmostEqual(interval.lower, 5 - 10 * z, places=12)
        self.assertAlmostEqual(interval.upper, 5 + 10 * z, places=12)
        lower, upper = interval.quantiles()
        for x in (-40.0, 5.0, 30.0):
            self.assertAlmostEqual(
                interval.score(x), (2 / 0.1) * (lower.score(x) + upper.score(x)), places=12
            )

    def test_array_intervals_score_elementwise(self) -> None:
        """Array bounds and outcomes give a float64 array, one score per element."""
        interval = CentralInterval(
            lower=np.array([-1.0, 0.0]), upper=np.array([1.0, 2.0]), alpha=0.05
        )
        score = interval.score(np.array([0.0, 3.0]))
        self.assertEqual(score.dtype, np.float64)
        np.testing.assert_allclose(score, [2.0, 2.0 + 40.0], rtol=1e-15)


if __name__ == "__main__":
    unittest.main()
