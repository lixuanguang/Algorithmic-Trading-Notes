"""Tests of the time-value bisection contract and the cash-flow stream's NPV and IRR."""

# The worked examples' full run is tested in test_checks.py. These pin down the bracket contract,
# exact roots, the n-halving midpoint, and the stream's values against hand sums.

import unittest

from trading_notes.numerical.time_value.cash_flows import CashFlowStream, GrowingDividend, bisect


class Bisection(unittest.TestCase):
    """Bad brackets raise; exact roots return as they are; otherwise n halvings."""

    def test_rejects_bad_brackets(self) -> None:
        """Bad brackets raise ValueError with their own message, before any iteration."""
        with self.assertRaisesRegex(ValueError, r"^bracket needs lo < hi$"):
            bisect(lambda x: x, 1.0, 1.0)
        with self.assertRaisesRegex(ValueError, r"^ends of the bracket have the same sign$"):
            bisect(lambda x: x, 1.0, 2.0)

    def test_returns_exact_roots_and_midpoints(self) -> None:
        """Exact roots at an end or a midpoint return as they are; otherwise n halvings."""
        self.assertEqual(bisect(lambda x: x - 0.5, 0.0, 1.0), 0.5)
        self.assertEqual(bisect(lambda x: x, 0.0, 1.0), 0.0)
        self.assertEqual(bisect(lambda x: x - 0.3, 0.0, 1.0, n=0), 0.5)
        self.assertEqual(bisect(lambda x: x - 0.3, 0.0, 1.0, n=1), 0.25)


class Streams(unittest.TestCase):
    """NPV, its slope and the IRR of dated flows from t = 0."""

    def test_npv_and_slope_by_hand(self) -> None:
        """-100 now and 121 in two years: NPV 0 at 10%, slope -2 x 121 / 1.1^3."""
        stream = CashFlowStream(flows=(-100, 0, 121))
        self.assertAlmostEqual(stream.npv(0.10), 0.0, places=12)
        self.assertEqual(stream.npv(0.0), 21.0)
        self.assertAlmostEqual(stream.npv_slope(0.10), -2 * 121 / 1.1**3, places=12)
        self.assertAlmostEqual(stream.irr(0.0, 1.0), 0.10, places=12)

    def test_irr_inherits_the_bracket_contract(self) -> None:
        """A bracket without a sign change raises instead of returning a rate."""
        with self.assertRaises(ValueError):
            CashFlowStream(flows=(-100, 50, 40)).irr(0.0, 1.0)

    def test_growing_dividend_value(self) -> None:
        """D0 2, g 4%, r 9%: 2.08 / 0.05 = 41.6."""
        self.assertAlmostEqual(GrowingDividend(d0=2.0, g=0.04, r=0.09).value(), 41.6, places=12)


if __name__ == "__main__":
    unittest.main()
