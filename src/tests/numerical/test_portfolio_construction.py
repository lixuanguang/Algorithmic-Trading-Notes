"""Tests of the Black-Litterman model, the covariance model and the ERC-Sharpe example."""

import contextlib
import io
import math
import unittest
from unittest import mock

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.portfolio_construction_models import black_litterman_checks as bl
from trading_notes.numerical.portfolio_construction_models import erc_sharpe_checks as erc_sharpe
from trading_notes.numerical.portfolio_construction_models.black_litterman import BlackLitterman
from trading_notes.numerical.portfolio_construction_models.equal_risk_contribution_checks import (
    UNEQUAL_CORRELATIONS,
    VOLS,
)
from trading_notes.numerical.portfolio_construction_models.risk_contributions import (
    CovarianceModel,
    long_only_minimum_variance,
    project_to_simplex,
)
from trading_notes.numerical.report import CheckReport


def unchanged(arrays: list[NDArray[np.float64]]) -> list[NDArray[np.float64]]:
    """Return copies of arrays, to compare with them after a call."""
    return [a.copy() for a in arrays]


class BlackLittermanPosterior(unittest.TestCase):
    """The precision form and the conditioning reference stay separate routes."""

    def test_each_run_gets_new_inputs(self) -> None:
        """example() builds new arrays, so changing one run's inputs cannot reach the next."""
        first = bl.example()
        first.sigma[0, 0] = 99.0
        first.pi[:] = 0.0
        second = bl.example()
        self.assertNotEqual(second.sigma[0, 0], 99.0)
        self.assertTrue(np.all(second.pi > 0))

    def test_posterior_leaves_inputs_alone(self) -> None:
        """Neither route changes the market arrays or Omega."""
        m, omega = bl.example(), np.array([[bl.VIEW_VARIANCE]])
        before = unchanged([m.sigma, m.pi, m.p, m.q, omega])
        m.posterior_mean(omega)
        bl.gaussian_conditioning(m, omega)
        for was, now in zip(before, [m.sigma, m.pi, m.p, m.q, omega], strict=True):
            np.testing.assert_array_equal(was, now)

    def test_precision_form_does_not_use_the_reference(self) -> None:
        """The posterior is computed with the conditioning reference unavailable."""
        with mock.patch.object(bl, "gaussian_conditioning", side_effect=AssertionError):
            e = bl.example().posterior_mean(np.array([[bl.VIEW_VARIANCE]]))
        self.assertEqual(e.shape, (3,))
        self.assertEqual(e.dtype, np.float64)

    def test_conditioning_check_uses_numpy_default_rtol(self) -> None:
        """The check keeps allclose's default rtol: a 1e-7 shift passes, a 1e-5 one fails."""
        posterior = BlackLitterman.posterior_mean
        for shift, failures in ((1e-7, []), (1e-5, ["equals Gaussian conditioning"])):
            with self.subTest(shift=shift):

                def shifted(
                    m: BlackLitterman, omega: NDArray[np.float64], by: float = shift
                ) -> NDArray[np.float64]:
                    return posterior(m, omega) + by

                report = CheckReport()
                with contextlib.redirect_stdout(io.StringIO()):
                    with mock.patch.object(BlackLitterman, "posterior_mean", shifted):
                        bl.check_posterior(report, bl.example())
                self.assertEqual(report.failures, failures)

    def test_view_limits(self) -> None:
        """A vague view leaves Pi; a certain view is met; the covariance is never changed."""
        m = bl.example()
        sigma = m.sigma.copy()
        vague = m.posterior_mean(np.array([[bl.NO_VIEW_VARIANCE]]))
        certain = m.posterior_mean(np.array([[bl.CERTAIN_VIEW_VARIANCE]]))
        np.testing.assert_allclose(vague, m.pi, rtol=0, atol=1e-9)
        self.assertAlmostEqual(float((m.p @ certain)[0]), float(m.q[0]), places=9)
        np.testing.assert_array_equal(m.sigma, sigma)


class EqualRiskContribution(unittest.TestCase):
    """The ERC iteration, the simplex projection and the minimum-variance descent."""

    def test_simplex_projection(self) -> None:
        """Points on the simplex stay; others move to the nearest point; the input is kept."""
        on = np.array([0.2, 0.3, 0.5])
        np.testing.assert_array_equal(project_to_simplex(on), on)
        np.testing.assert_allclose(project_to_simplex(np.array([2.0, 0.0])), [1.0, 0.0])
        np.testing.assert_allclose(project_to_simplex(np.array([0.5, 0.5, -1.0])), [0.5, 0.5, 0])
        x = np.array([0.6, 0.6, 0.6])
        projected = project_to_simplex(x)
        np.testing.assert_allclose(projected, [1 / 3] * 3)
        self.assertIsNot(projected, x)
        np.testing.assert_array_equal(x, [0.6, 0.6, 0.6])

    def test_minvar_on_uncorrelated_assets(self) -> None:
        """Uncorrelated assets: minimum-variance weights are proportional to 1 / variance."""
        S = np.diag([0.01, 0.04])
        # The error shrinks by about 1 - lr * mean variance = 0.9875 a step: e^-50 here.
        weights = long_only_minimum_variance(S, iters=4000)
        np.testing.assert_allclose(weights, [0.8, 0.2], atol=1e-12)
        np.testing.assert_array_equal(S, np.diag([0.01, 0.04]))

    def test_minvar_corner_solution(self) -> None:
        """A dominated asset gets zero weight: the projection keeps the descent long-only."""
        S = np.array([[0.01, 0.015], [0.015, 0.04]])  # correlation 0.75 > vol ratio 0.5
        weights = long_only_minimum_variance(S, iters=2000)
        np.testing.assert_allclose(weights, [1.0, 0.0], atol=1e-12)

    def test_erc_equalises_contributions_and_keeps_inputs(self) -> None:
        """The fixed point equalises risk contributions, which sum to sigma; S is unchanged."""
        model = CovarianceModel.from_volatilities(VOLS, np.array(UNEQUAL_CORRELATIONS))
        before = model.sigma.copy()
        weights = model.equal_risk_contribution()
        contributions, sigma = model.risk_contributions(weights), model.volatility(weights)
        self.assertLess(float(np.ptp(contributions)), 1e-10)
        self.assertAlmostEqual(float(contributions.sum()), sigma, places=12)
        self.assertIsInstance(sigma, float)
        np.testing.assert_array_equal(model.sigma, before)

    def test_erc_iteration_count_matters(self) -> None:
        """Three iterations are visibly short of the equal-contribution fixed point."""
        model = CovarianceModel.from_volatilities(VOLS, np.full((4, 4), 0.3) + 0.7 * np.eye(4))
        weights = model.equal_risk_contribution(iters=3)
        self.assertGreater(float(np.ptp(model.risk_contributions(weights))), 1e-4)


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
        model, ex = CovarianceModel(sigma=np.eye(2)), np.array([-1.0, -1.0])
        equal = model.sharpe(np.array([0.5, 0.5]), ex)
        self.assertIs(type(equal), float)
        self.assertAlmostEqual(equal, -math.sqrt(2), places=12)
        self.assertEqual(model.sharpe(np.array([1.0, 0.0]), ex), -1.0)

    def test_sharpe_ratio_cases_cover_each_sign(self) -> None:
        """The grid checks cover a positive, a zero and a negative common Sharpe ratio."""
        self.assertEqual(
            [math.copysign(1, s) if s else 0 for s in erc_sharpe.SHARPE_RATIOS], [1, 0, -1]
        )


if __name__ == "__main__":
    unittest.main()
