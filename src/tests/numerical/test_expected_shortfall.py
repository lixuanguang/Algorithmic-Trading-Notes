"""Tests of the expected-shortfall conventions and the example's own random sequence."""

import random
import unittest

from trading_notes.numerical.var_es_estimation import expected_shortfall_checks as es
from trading_notes.numerical.var_es_estimation.expected_shortfall import (
    DiscreteLoss,
    historical_expected_shortfall,
)

from .single_run import GlobalState, prime_global_random, restored_global_state

LOSS = es.TWO_ATOMS


class DiscreteLaw(unittest.TestCase):
    """VaR is the lower quantile, and ES weights the atom at VaR fractionally."""

    def test_var_is_the_lower_quantile(self) -> None:
        """At c = P(L <= l) the quantile is l itself; just above c it is the next atom."""
        self.assertEqual(LOSS.var(0.99), 0.0)
        self.assertEqual(LOSS.var(0.995), 0.0)
        self.assertEqual(LOSS.var(0.996), 100.0)
        # Probabilities that sum to less than c fall back to the largest loss.
        self.assertEqual(DiscreteLoss(atoms=[(0.0, 0.5), (1.0, 0.4)]).var(0.95), 1.0)

    def test_fractional_mass_and_integral_agree(self) -> None:
        """Both ES forms give 50 at 99%; the midpoint rule is exact here with an even n."""
        self.assertAlmostEqual(LOSS.expected_shortfall(0.99), 50.0, places=9)
        self.assertAlmostEqual(es.quantile_integral(LOSS, 0.99, n=1000), 50.0, places=9)
        self.assertAlmostEqual(LOSS.expected_shortfall(0.996), 100.0, places=9)

    def test_tail_conditional_expectations_differ_from_es(self) -> None:
        """With an atom at VaR, E[L | L > VaR] and E[L | L >= VaR] both miss ES."""
        self.assertEqual(LOSS.tail_conditional_expectation(0.99, strict=True), 100.0)
        self.assertAlmostEqual(
            LOSS.tail_conditional_expectation(0.99, strict=False), 0.5, places=12
        )
        self.assertEqual(
            LOSS.tail_conditional_expectation(0.99),
            LOSS.tail_conditional_expectation(0.99, strict=True),
        )


class HistoricalSimulation(unittest.TestCase):
    """The worst n*alpha losses, the last weighted by the fractional part."""

    def test_fractional_tail_observation(self) -> None:
        """2.5 tail observations average 40, 30 and half of 20 over 2.5."""
        sample = [40.0, 30.0, 20.0, 10.0] + [0.0] * 246
        self.assertAlmostEqual(historical_expected_shortfall(sample, 0.99), 32.0, places=9)

    def test_near_integer_count_is_whole(self) -> None:
        """1000 * (1 - 0.99) == 10.000000000000009, not 10.0, and still counts 10 losses."""
        self.assertGreater(1000 * (1 - 0.99), 10)
        sample = [100.0] * 5 + [0.0] * 995
        self.assertAlmostEqual(historical_expected_shortfall(sample, 0.99), 50.0, places=9)
        # The fractional part, 9e-15, is below the tolerance, so the eleventh loss, here
        # 0, gets no weight; the divisor stays the computed k.
        self.assertEqual(historical_expected_shortfall(sample, 0.99), 500.0 / (1000 * (1 - 0.99)))


class GaussianDraws(unittest.TestCase):
    """The draws are the original sequence, from a generator the example owns."""

    def test_draws_match_the_seeded_shared_sequence(self) -> None:
        """random.seed(7) then gauss(0, 1), as first written, gives the same draws."""
        with restored_global_state():
            random.seed(es.SEED)
            shared = [random.gauss(0, 1) for _ in range(1001)]
        self.assertEqual(es.normal_draws(1001), shared)
        self.assertEqual(es.DRAWS, 400000)

    def test_draws_ignore_and_keep_the_shared_generator(self) -> None:
        """Draws repeat whatever the shared state, which they leave as it was."""
        with restored_global_state():
            prime_global_random(3)
            before = GlobalState.now()
            first = es.normal_draws(11)
            self.assertEqual(GlobalState.now(), before)
            prime_global_random(4)
            self.assertEqual(es.normal_draws(11), first)


if __name__ == "__main__":
    unittest.main()
