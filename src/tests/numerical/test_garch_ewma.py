"""Tests of the GARCH/EWMA example's forecast timing and draw order.

The example's checks run in test_checks.py. These pin down the k - 1 exponent, which day each
variance belongs to, the forecast window and the order in which the one stream is consumed, on
short series.

Run: make test (uv run --frozen --no-editable pytest)
"""

import contextlib
import io
import unittest
from collections.abc import Mapping
from unittest import mock

import numpy as np

from trading_notes.numerical.report import CheckReport
from trading_notes.numerical.volatility_forecasting import garch_ewma_checks as ge
from trading_notes.numerical.volatility_forecasting.garch import (
    Ewma,
    Garch11,
    GarchSeries,
    mse_ratio,
)


class KStepForecast(unittest.TestCase):
    """The analytical forecast and the Monte Carlo reference are separate routes."""

    def test_exponent_is_k_minus_1(self) -> None:
        """One step ahead is sigma2_{t+1} itself; the gap then decays by alpha + beta a step."""
        s2_next = 4 * ge.MODEL.long_run
        self.assertEqual(ge.MODEL.k_step_forecast(s2_next, 1), s2_next)
        gap = ge.MODEL.k_step_forecast(s2_next, 3) - ge.MODEL.long_run
        self.assertAlmostEqual(
            gap, (ge.MODEL.alpha + ge.MODEL.beta) ** 2 * 3 * ge.MODEL.long_run, places=18
        )

    def test_monte_carlo_draws_k_minus_1_vectors(self) -> None:
        """A k-step forecast draws k - 1 shock vectors and does not use the closed form."""
        rng = np.random.default_rng(5)
        with mock.patch.object(Garch11, "k_step_forecast", side_effect=AssertionError):
            self.assertEqual(ge.MODEL.monte_carlo_forecast(rng, 0.5, 1, 7), 0.5)
            ge.MODEL.monte_carlo_forecast(rng, 0.5, 4, 7)
        replay = np.random.default_rng(5)
        for _ in range(3):
            replay.standard_normal(7)
        self.assertEqual(rng.bit_generator.state, replay.bit_generator.state)


class SeriesTiming(unittest.TestCase):
    """sigma2_t and ew_t are the variances for day t, known at t - 1."""

    def test_garch_recurrence_and_scalar_draws(self) -> None:
        """R_t uses sigma2_t; sigma2_{t+1} uses R_t; one scalar draw per day, in order."""
        series = ge.MODEL.simulate(np.random.default_rng(8), 30)
        replay = np.random.default_rng(8)
        z = np.array([replay.standard_normal() for _ in range(30)])
        R, s2 = series.returns, series.variances
        self.assertEqual(s2[0], ge.MODEL.long_run)
        np.testing.assert_array_equal(R, np.sqrt(s2) * z)
        np.testing.assert_array_equal(
            s2[1:], ge.MODEL.omega + ge.MODEL.alpha * R[:-1] ** 2 + ge.MODEL.beta * s2[:-1]
        )

    def test_ewma_recurrence(self) -> None:
        """ew_0 = sigma2 and ew_{t+1} = 0.94 ew_t + 0.06 R_t^2; the last return is unused."""
        R = np.array([0.01, -0.02, 0.03, 0.5])
        ew = Ewma().variances(R, ge.MODEL.long_run)
        self.assertEqual(ew[0], ge.MODEL.long_run)
        self.assertEqual(ew[1], 0.94 * ge.MODEL.long_run + 0.06 * 0.01**2)
        self.assertEqual(ew[3], 0.94 * ew[2] + 0.06 * 0.03**2)

    def test_forecast_window(self) -> None:
        """Day t's forecasts cover R_t..R_{t+h-1}, for t from FIRST_FORECAST to n - h - 1."""
        rng = np.random.default_rng(9)
        n, h = ge.FIRST_FORECAST + 12, 3
        series = GarchSeries(returns=rng.normal(0, 0.01, n), variances=rng.uniform(1e-5, 2e-4, n))
        ew = rng.uniform(1e-5, 2e-4, n)
        real, garch, ewma = [], [], []
        for t in range(ge.FIRST_FORECAST, n - h):
            real.append(sum(series.returns[t + j] ** 2 for j in range(h)))
            garch.append(
                sum(
                    ge.MODEL.long_run
                    + (ge.MODEL.alpha + ge.MODEL.beta) ** j
                    * (series.variances[t] - ge.MODEL.long_run)
                    for j in range(h)
                )
            )
            ewma.append(h * ew[t])
        want = np.mean((np.array(real) - ewma) ** 2) / np.mean((np.array(real) - garch) ** 2)
        self.assertAlmostEqual(
            mse_ratio(ge.MODEL, series, ew, h, ge.FIRST_FORECAST), float(want), places=12
        )


class SeriesStarted(Exception):
    """Raised by a stand-in to stop a check once its series simulation is reached."""


class Stream(unittest.TestCase):
    """The second experiment continues the first's stream rather than reseeding."""

    def test_series_follows_the_monte_carlo_vectors(self) -> None:
        """Nine vectors of PATHS shocks precede the series' scalar draws."""
        drawn: list[Mapping[str, object]] = []

        def series_at(model: Garch11, rng: np.random.Generator, n: int) -> GarchSeries:
            drawn.append(rng.bit_generator.state)
            raise SeriesStarted

        report = CheckReport()
        rng = np.random.default_rng(ge.SEED)
        with (
            mock.patch.object(Garch11, "simulate", series_at),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            ge.check_k_step(report, rng)
            with self.assertRaises(SeriesStarted):
                ge.check_ewma_against_garch(report, rng)
        replay = np.random.default_rng(ge.SEED)
        for _ in range(ge.K - 1):
            replay.standard_normal(ge.PATHS)
        self.assertEqual(drawn, [replay.bit_generator.state])


if __name__ == "__main__":
    unittest.main()
