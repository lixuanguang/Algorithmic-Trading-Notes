"""Tests of the Black-Litterman and equal-risk-contribution examples' NumPy routines.

The examples' own checks run in test_checks.py. These pin down boundaries, the independence
of each reference calculation and the ownership of input and working arrays, with small or
short computations rather than the examples' full solver runs.

Run: make test (uv run --frozen --no-editable pytest)
"""

# standard library imports
import contextlib
import io
import math
import unittest
from unittest import mock

# third party library imports
import numpy as np
from numpy.typing import NDArray

# project library imports
from trading_notes.numerical import black_litterman as bl
from trading_notes.numerical import equal_risk_contribution as erc
from trading_notes.numerical import erc_sharpe
from trading_notes.numerical.report import CheckReport


def unchanged(arrays: list[NDArray[np.float64]]) -> list[NDArray[np.float64]]:
    """Return copies of arrays, to compare with them after a call."""
    return [a.copy() for a in arrays]


class BlackLitterman(unittest.TestCase):
    """The precision form and the conditioning reference stay separate routes."""

    def test_each_run_gets_new_inputs(self) -> None:
        """market() builds new arrays, so changing one run's inputs cannot reach the next."""
        first = bl.market()
        first.sigma[0, 0] = 99.0
        first.pi[:] = 0.0
        second = bl.market()
        self.assertNotEqual(second.sigma[0, 0], 99.0)
        self.assertTrue(np.all(second.pi > 0))

    def test_posterior_leaves_inputs_alone(self) -> None:
        """Neither route changes the market arrays or Omega."""
        m, omega = bl.market(), np.array([[bl.VIEW_VARIANCE]])
        before = unchanged([m.sigma, m.pi, m.p, m.q, omega])
        bl.posterior_mean(m, omega)
        bl.gaussian_conditioning(m, omega)
        for was, now in zip(before, [m.sigma, m.pi, m.p, m.q, omega], strict=True):
            np.testing.assert_array_equal(was, now)

    def test_precision_form_does_not_use_the_reference(self) -> None:
        """The posterior is computed with the conditioning reference unavailable."""
        with mock.patch.object(bl, "gaussian_conditioning", side_effect=AssertionError):
            e = bl.posterior_mean(bl.market(), np.array([[bl.VIEW_VARIANCE]]))
        self.assertEqual(e.shape, (3,))
        self.assertEqual(e.dtype, np.float64)

    def test_conditioning_check_uses_numpy_default_rtol(self) -> None:
        """The check keeps allclose's default rtol: a 1e-7 shift passes, a 1e-5 one fails."""
        posterior = bl.posterior_mean
        for shift, failures in ((1e-7, []), (1e-5, ["equals Gaussian conditioning"])):
            with self.subTest(shift=shift):

                def shifted(
                    m: bl.Market, omega: NDArray[np.float64], by: float = shift
                ) -> NDArray[np.float64]:
                    return posterior(m, omega) + by

                report = CheckReport()
                with contextlib.redirect_stdout(io.StringIO()):
                    with mock.patch.object(bl, "posterior_mean", shifted):
                        bl.check_posterior(report, bl.market())
                self.assertEqual(report.failures, failures)

    def test_view_limits(self) -> None:
        """A vague view leaves Pi; a certain view is met; the covariance is never changed."""
        m = bl.market()
        sigma = m.sigma.copy()
        vague = bl.posterior_mean(m, np.array([[bl.NO_VIEW_VARIANCE]]))
        certain = bl.posterior_mean(m, np.array([[bl.CERTAIN_VIEW_VARIANCE]]))
        np.testing.assert_allclose(vague, m.pi, rtol=0, atol=1e-9)
        self.assertAlmostEqual(float((m.p @ certain)[0]), float(m.q[0]), places=9)
        np.testing.assert_array_equal(m.sigma, sigma)


class EqualRiskContribution(unittest.TestCase):
    """The ERC iterations, the simplex projection and the minimum-variance descent."""

    def test_simplex_projection(self) -> None:
        """Points on the simplex stay; others move to the nearest point; the input is kept."""
        on = np.array([0.2, 0.3, 0.5])
        np.testing.assert_array_equal(erc.project_to_simplex(on), on)
        np.testing.assert_allclose(erc.project_to_simplex(np.array([2.0, 0.0])), [1.0, 0.0])
        np.testing.assert_allclose(
            erc.project_to_simplex(np.array([0.5, 0.5, -1.0])), [0.5, 0.5, 0]
        )
        x = np.array([0.6, 0.6, 0.6])
        projected = erc.project_to_simplex(x)
        np.testing.assert_allclose(projected, [1 / 3] * 3)
        self.assertIsNot(projected, x)
        np.testing.assert_array_equal(x, [0.6, 0.6, 0.6])

    def test_minvar_on_uncorrelated_assets(self) -> None:
        """Uncorrelated assets: minimum-variance weights are proportional to 1 / variance."""
        S = np.diag([0.01, 0.04])
        # The error shrinks by about 1 - lr * mean variance = 0.9875 a step: e^-50 here.
        weights = erc.minvar_long_only(S, iters=4000)
        np.testing.assert_allclose(weights, [0.8, 0.2], atol=1e-12)
        np.testing.assert_array_equal(S, np.diag([0.01, 0.04]))

    def test_minvar_corner_solution(self) -> None:
        """A dominated asset gets zero weight: the projection keeps the descent long-only."""
        S = np.array([[0.01, 0.015], [0.015, 0.04]])  # correlation 0.75 > vol ratio 0.5
        weights = erc.minvar_long_only(S, iters=2000)
        np.testing.assert_allclose(weights, [1.0, 0.0], atol=1e-12)

    def test_two_erc_iterations_agree_but_stay_separate(self) -> None:
        """Both fixed points equalise risk contributions; each keeps its own step."""
        vols = np.array(erc.VOLS)
        S = np.outer(vols, vols) * np.array(erc.UNEQUAL_CORRELATIONS)
        before = S.copy()
        multiplied, divided = erc.erc(S), erc_sharpe.erc(S)
        np.testing.assert_allclose(multiplied, divided, rtol=0, atol=1e-12)
        contributions, sigma = erc.rc(multiplied, S)
        self.assertLess(float(np.ptp(contributions)), 1e-10)
        self.assertAlmostEqual(float(contributions.sum()), sigma, places=12)
        self.assertIsInstance(sigma, float)
        self.assertIsNot(erc.erc, erc_sharpe.erc)
        np.testing.assert_array_equal(S, before)

    def test_erc_iteration_count_matters(self) -> None:
        """Three iterations are visibly short of the equal-contribution fixed point."""
        S = np.outer(erc.VOLS, erc.VOLS) * (np.full((4, 4), 0.3) + 0.7 * np.eye(4))
        contributions, _ = erc.rc(erc.erc(S, iters=3), S)
        self.assertGreater(float(np.ptp(contributions)), 1e-4)


class ErcSharpe(unittest.TestCase):
    """The Sharpe ratio, the long-only grid and the counterexample."""

    def test_grid_is_the_long_only_simplex_of_step_one_twentieth(self) -> None:
        """C(23, 3) = 1771 portfolios, each non-negative and fully invested, new on each call."""
        grid = erc_sharpe.long_only_grid()
        self.assertEqual(len(grid), math.comb(23, 3))
        self.assertTrue(all(w.min() >= 0 and math.isclose(w.sum(), 1.0) for w in grid))
        self.assertTrue(any(np.array_equal(w, [1.0, 0, 0, 0]) for w in grid))
        self.assertIsNot(erc_sharpe.long_only_grid()[0], grid[0])

    def test_sharpe_is_a_float_with_the_counterexample_values(self) -> None:
        """Equal weights on the negative pair give -sqrt(2); a single asset gives -1."""
        S, ex = np.eye(2), np.array([-1.0, -1.0])
        equal = erc_sharpe.sharpe(np.array([0.5, 0.5]), ex, S)
        self.assertIs(type(equal), float)
        self.assertAlmostEqual(equal, -math.sqrt(2), places=12)
        self.assertEqual(erc_sharpe.sharpe(np.array([1.0, 0.0]), ex, S), -1.0)

    def test_sharpe_ratio_cases_cover_each_sign(self) -> None:
        """The grid checks cover a positive, a zero and a negative common Sharpe ratio."""
        self.assertEqual(
            [math.copysign(1, s) if s else 0 for s in erc_sharpe.SHARPE_RATIOS], [1, 0, -1]
        )


if __name__ == "__main__":
    unittest.main()
