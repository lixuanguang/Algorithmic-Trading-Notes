"""Tests of the fee schedules and the style-analysis solver boundary."""

import unittest

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.manager_selection.manager_evaluation import (
    AsymmetricFee,
    FulcrumFee,
    shrunk_information_ratio,
    style_fit,
)


class FeeSchedules(unittest.TestCase):
    """Fees for excess returns of +4, -3 and +5 percent, worked by hand."""

    def test_high_water_mark_defers_the_share(self) -> None:
        """After a -3 year, only the 2 points above the mark earn the 20 percent share."""
        np.testing.assert_allclose(AsymmetricFee().fees([4.0, -3.0, 5.0]), [1.05, 0.25, 0.65])
        np.testing.assert_allclose(
            AsymmetricFee(high_water_mark=False).fees([4.0, -3.0, 5.0]), [1.05, 0.25, 1.25]
        )

    def test_fulcrum_fee_is_symmetric_within_its_floor_and_cap(self) -> None:
        """Base 0.50 plus 0.10 per point, kept between 0.10 and 0.90."""
        np.testing.assert_allclose(FulcrumFee().fees([4.0, -3.0, 5.0, -6.0]), [0.9, 0.2, 0.9, 0.1])

    def test_shrinkage_toward_zero(self) -> None:
        """A longer record shrinks less; a zero prior spread shrinks to zero."""
        short, long_ = shrunk_information_ratio(1.0, 1, 0.5), shrunk_information_ratio(1.0, 9, 0.5)
        self.assertLess(short, long_)
        self.assertLess(long_, 1.0)
        self.assertEqual(shrunk_information_ratio(1.0, 9, 0.0), 0.0)


class StyleFitBoundary(unittest.TestCase):
    """SLSQP over long-only weights that sum to one."""

    def test_interior_minimiser(self) -> None:
        """A target inside the simplex is recovered, with a float objective and success."""
        target = np.array([0.1, 0.2, 0.3, 0.25, 0.15])

        def distance(w: NDArray[np.float64]) -> float:
            return float(((w - target) ** 2).sum())

        fit = style_fit(distance)
        self.assertIs(type(fit.fun), float)
        self.assertIs(fit.success, True)
        self.assertEqual((fit.x.dtype, fit.x.shape), (np.dtype(np.float64), (5,)))
        np.testing.assert_allclose(fit.x, target, atol=1e-8)

    def test_bounds_bind(self) -> None:
        """A target outside the simplex lands on its face: nonnegative weights summing to one."""
        target = np.array([0.6, 0.6, -0.2, 0.0, 0.0])

        def distance(w: NDArray[np.float64]) -> float:
            return float(((w - target) ** 2).sum())

        fit = style_fit(distance)
        self.assertAlmostEqual(float(fit.x.sum()), 1.0, places=9)
        self.assertGreaterEqual(float(fit.x.min()), -1e-9)
        np.testing.assert_allclose(fit.x, [0.5, 0.5, 0.0, 0.0, 0.0], atol=1e-7)


if __name__ == "__main__":
    unittest.main()
