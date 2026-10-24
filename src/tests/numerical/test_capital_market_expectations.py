"""Tests of the regime chain's timing convention.

The example's full run is tested in test_checks.py. These pin down that the first month's
return is the starting state's and the chain moves after each month, against hand recursion on
a prepared two-state chain.

Run: make test (uv run --frozen --no-editable pytest)
"""

import unittest

import numpy as np

from trading_notes.numerical.capital_market_expectations import horizon_return

P = np.array([[0.9, 0.1], [0.3, 0.7]])
MU = np.array([0.02, -0.04])


class HorizonReturn(unittest.TestCase):
    """Expected cumulative log return from a known starting state."""

    def test_first_month_is_the_starting_state(self) -> None:
        """One month from contraction earns mu[1]; from expansion, mu[0]."""
        self.assertEqual(horizon_return(P, MU, 1), MU[1])
        self.assertEqual(horizon_return(P, MU, 1, start=0), MU[0])

    def test_later_months_follow_the_chain(self) -> None:
        """Three months from contraction: mu1 + P[1] mu + P[1] P mu."""
        want = MU[1] + P[1] @ MU + P[1] @ P @ MU
        self.assertAlmostEqual(horizon_return(P, MU, 3), want, places=15)
        self.assertEqual(horizon_return(P, MU, 0), 0.0)


if __name__ == "__main__":
    unittest.main()
