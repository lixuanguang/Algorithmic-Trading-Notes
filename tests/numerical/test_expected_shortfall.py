"""Tests of the expected-shortfall example's conventions and its own random sequence.

The example's checks run in test_checks.py. These pin down the lower-quantile convention, the
fractional tail mass, the two tail conditional expectations, the historical-simulation rounding
tolerance and the Gaussian draws, on small inputs.

Run: make test (uv run --frozen --no-editable pytest)
"""

# standard library imports
import random
import unittest

# project library imports
from tests.numerical.test_checks import GlobalState, prime_global_random, restored_global_state
from trading_notes.numerical import expected_shortfall as es

ATOMS = es.AUDIT_ATOMS


class DiscreteLaw(unittest.TestCase):
    """VaR is the lower quantile, and ES weights the atom at VaR fractionally."""

    def test_var_is_the_lower_quantile(self) -> None:
        """At c = P(L <= l) the quantile is l itself; just above c it is the next atom."""
        self.assertEqual(es.var_discrete(ATOMS, 0.99), 0.0)
        self.assertEqual(es.var_discrete(ATOMS, 0.995), 0.0)
        self.assertEqual(es.var_discrete(ATOMS, 0.996), 100.0)
        # Probabilities that sum to less than c fall back to the largest loss.
        self.assertEqual(es.var_discrete([(0.0, 0.5), (1.0, 0.4)], 0.95), 1.0)

    def test_fractional_mass_and_integral_agree(self) -> None:
        """Both ES forms give 50 at 99%; the midpoint rule is exact here with an even n."""
        self.assertAlmostEqual(es.es_fractional(ATOMS, 0.99), 50.0, places=9)
        self.assertAlmostEqual(es.es_integral(ATOMS, 0.99, n=1000), 50.0, places=9)
        self.assertAlmostEqual(es.es_fractional(ATOMS, 0.996), 100.0, places=9)

    def test_tail_conditional_expectations_differ_from_es(self) -> None:
        """With an atom at VaR, E[L | L > VaR] and E[L | L >= VaR] both miss ES."""
        self.assertEqual(es.tce(ATOMS, 0.99, strict=True), 100.0)
        self.assertAlmostEqual(es.tce(ATOMS, 0.99, strict=False), 0.5, places=12)
        self.assertEqual(es.tce(ATOMS, 0.99), es.tce(ATOMS, 0.99, strict=True))


class HistoricalSimulation(unittest.TestCase):
    """The worst n*alpha losses, the last weighted by the fractional part."""

    def test_fractional_tail_observation(self) -> None:
        """2.5 tail observations average 40, 30 and half of 20 over 2.5."""
        sample = [40.0, 30.0, 20.0, 10.0] + [0.0] * 246
        self.assertAlmostEqual(es.es_hs(sample, 0.99), 32.0, places=9)

    def test_near_integer_count_is_whole(self) -> None:
        """1000 * (1 - 0.99) == 10.000000000000009, not 10.0, and still counts 10 losses."""
        self.assertGreater(1000 * (1 - 0.99), 10)
        sample = [100.0] * 5 + [0.0] * 995
        self.assertAlmostEqual(es.es_hs(sample, 0.99), 50.0, places=9)
        # The fractional part, 9e-15, is below the tolerance, so the eleventh loss, here
        # 0, gets no weight; the divisor stays the computed k.
        self.assertEqual(es.es_hs(sample, 0.99), 500.0 / (1000 * (1 - 0.99)))


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
