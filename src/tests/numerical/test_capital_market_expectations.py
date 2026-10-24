"""Tests of the regime chain's timing convention, stationary law and the ARCH update."""

# The example's full run is tested in test_checks.py. These pin down that the first month's return
# is the starting state's and the chain moves after each month, against hand recursion on a
# prepared two-state chain.

import unittest

import numpy as np

from trading_notes.numerical.capital_market_expectations.regimes import ArchVariance, RegimeChain

P = np.array([[0.9, 0.1], [0.3, 0.7]])
MU = np.array([0.02, -0.04])
CHAIN = RegimeChain(transitions=P, returns=MU)


class HorizonReturn(unittest.TestCase):
    """Expected cumulative log return from a known starting state."""

    def test_first_month_is_the_starting_state(self) -> None:
        """One month from contraction earns mu[1]; from expansion, mu[0]."""
        self.assertEqual(CHAIN.horizon_return(1), MU[1])
        self.assertEqual(CHAIN.horizon_return(1, start=0), MU[0])

    def test_later_months_follow_the_chain(self) -> None:
        """Three months from contraction: mu1 + P[1] mu + P[1] P mu."""
        want = MU[1] + P[1] @ MU + P[1] @ P @ MU
        self.assertAlmostEqual(CHAIN.horizon_return(3), want, places=15)
        self.assertEqual(CHAIN.horizon_return(0), 0.0)

    def test_stationary_distribution_and_wealth(self) -> None:
        """Pi P = pi with pi = (0.75, 0.25); one month's expected wealth is e^{mu[start]}."""
        np.testing.assert_allclose(CHAIN.stationary(), [0.75, 0.25], rtol=1e-12)
        self.assertAlmostEqual(CHAIN.expected_wealth(1), float(np.exp(MU[1])), places=15)
        two = np.exp(MU[1]) * (P[1] @ np.exp(MU))
        self.assertAlmostEqual(CHAIN.expected_wealth(2), float(two), places=15)


class Arch(unittest.TestCase):
    """The ARCH(1) update and its long-run variance."""

    def test_fixed_point(self) -> None:
        """Starting at the long-run variance with a surprise of its square root stays there."""
        arch = ArchVariance(gamma=0.000002, persistence=0.9, shock=0.08)
        lr = arch.long_run()
        self.assertAlmostEqual(arch.update(lr, lr**0.5), lr, places=18)


if __name__ == "__main__":
    unittest.main()
