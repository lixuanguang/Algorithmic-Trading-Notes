"""Tests of the liquidity-spiral price response and the margin-spiral checks' failure paths."""

# The example's full run is tested in test_checks.py. These pin down the closed form against the
# loop series computed separately, and show that a wrong closed form or a dampening loss loop
# fails the checks.

import contextlib
import io
import unittest
from unittest import mock

from trading_notes.numerical.crowding_contagion import margin_spiral_checks as spiral_checks
from trading_notes.numerical.crowding_contagion.liquidity_spiral import LiquiditySpiral
from trading_notes.numerical.report import CheckReport

SPIRAL = spiral_checks.SPIRAL


class PriceResponse(unittest.TestCase):
    """The loop series is summed independently of the closed form it is checked against."""

    def test_series_and_closed_form_agree(self) -> None:
        """K = 1 with l = 0.5: both give 2; the example's loops are 0.2 (margin) and 0.3 (loss)."""
        self.assertEqual(SPIRAL.k, 1.0)
        self.assertEqual(SPIRAL.response(0.5), 2.0)
        self.assertAlmostEqual(SPIRAL.series_response(0.5, 200), 2.0, places=12)
        self.assertEqual((SPIRAL.margin_loop, SPIRAL.loss_loop), (0.2, 0.3))

    def test_wrong_closed_form_fails_the_series_check(self) -> None:
        """A closed form off by 1e-9 no longer matches the series."""

        def wrong(spiral: LiquiditySpiral, ell: float) -> float:
            return 1 / (spiral.k - ell) + 1e-9

        report = CheckReport()
        with contextlib.redirect_stdout(io.StringIO()):
            with mock.patch.object(LiquiditySpiral, "response", wrong):
                spiral_checks.check_series(report)
        self.assertEqual(report.failures, ["series = closed form (2.000000 vs 2.000000)"])

    def test_negative_loss_loop_is_not_super_additive(self) -> None:
        """With x0 < 0 the loss loop dampens, and the joint extra falls below the sum."""
        dampened = SPIRAL.model_copy(update={"loss_position": -0.3})
        report = CheckReport()
        with contextlib.redirect_stdout(io.StringIO()):
            with mock.patch.object(spiral_checks, "SPIRAL", dampened):
                spiral_checks.check_amplification(report)
        self.assertEqual(
            report.failures,
            [
                "loss spiral amplifies: 0.7692 > 1.0000",
                "joint extra -0.0909 > sum of separate extras 0.0192",
            ],
        )


if __name__ == "__main__":
    unittest.main()
