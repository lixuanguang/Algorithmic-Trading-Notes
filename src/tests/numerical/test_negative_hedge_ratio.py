"""Tests of the negative-hedge-ratio demonstration's sign convention and three calculations."""

# The demonstration asserts nothing; its runs are tested in test_checks.py. These pin down the
# hedged-change convention V(h) = dS - h dF, the draw order and the variance conventions of each
# calculation, on small inputs.

import unittest
from unittest import mock

import numpy as np

from trading_notes.numerical.futures_hedging.hedge_ratio import HedgeMoments, HedgeSample
from trading_notes.numerical.futures_hedging.negative_hedge_ratio_checks import MOMENTS


class AnalyticVariance(unittest.TestCase):
    """With rho < 0 the minimum-variance hedge is a long futures position, h < 0."""

    def test_signs(self) -> None:
        """h* = rho sS / sF = -0.6 removes rho^2 of the variance; the short h = +0.6 adds it."""
        hstar = MOMENTS.optimal_ratio()
        self.assertEqual(hstar, -0.6)
        self.assertAlmostEqual(MOMENTS.variance(hstar), 1 - 0.6**2, places=15)
        self.assertEqual(MOMENTS.variance(0.0), 1.0)
        self.assertAlmostEqual(MOMENTS.variance(0.6), 1 + 2 * 0.36 + 0.36, places=15)
        self.assertLess(MOMENTS.variance(-0.5), MOMENTS.variance(0.0))


class Simulation(unittest.TestCase):
    """dF comes from the first normal vector, dS from both; the estimates stay separate."""

    def test_draw_order(self) -> None:
        """Two standard normal vectors are drawn in turn; the first drives dF."""
        sample = MOMENTS.simulate(np.random.default_rng(3), 8)
        replay = np.random.default_rng(3)
        z1, z2 = replay.standard_normal(8), replay.standard_normal(8)
        np.testing.assert_array_equal(sample.futures_changes, 1.0 * z1)
        np.testing.assert_array_equal(
            sample.spot_changes, 1.0 * (-0.6 * z1 + np.sqrt(1 - 0.6**2) * z2)
        )

    def test_cov_var_ratio_uses_ddof_1_throughout(self) -> None:
        """np.cov's default and Var with ddof 1 cancel to the OLS slope; ddof 0 would not."""
        dF = np.array([0.0, 1.0, 2.0, 4.0])
        dS = np.array([1.0, -1.0, 0.0, -3.0])
        sample = HedgeSample(spot_changes=dS, futures_changes=dF)
        x, y = dF - dF.mean(), dS - dS.mean()
        self.assertAlmostEqual(sample.cov_var_ratio(), (x @ y) / (x @ x), places=15)
        self.assertNotAlmostEqual(
            sample.cov_var_ratio(), float(np.cov(dS, dF)[0, 1] / dF.var()), places=3
        )

    def test_grid_search_is_empirical(self) -> None:
        """An exact linear relation is found on the grid with no closed form available."""
        dF = np.array([1.0, -2.0, 0.5, 3.0])
        sample = HedgeSample(spot_changes=-0.25 * dF, futures_changes=dF)
        with (
            mock.patch.object(HedgeMoments, "variance", side_effect=AssertionError),
            mock.patch.object(HedgeSample, "cov_var_ratio", side_effect=AssertionError),
        ):
            self.assertAlmostEqual(sample.grid_minimiser(), -0.25, places=12)
        # Beyond the grid's end the search stops at -1.5 rather than extrapolating.
        steep = HedgeSample(spot_changes=-2.0 * dF, futures_changes=dF)
        self.assertEqual(steep.grid_minimiser(), -1.5)


if __name__ == "__main__":
    unittest.main()
