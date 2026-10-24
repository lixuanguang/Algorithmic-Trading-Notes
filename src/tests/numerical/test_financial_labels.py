"""Tests of the labelling, bar-sampling, ETF-trick and fractional-differencing classes."""

# The demonstrations' full runs are tested in test_checks.py. These pin down the guard for a time
# that no label uses (uniqueness 0 there, not 0/0), AFML's sequential-bootstrap example, the CUSUM
# filter's strict threshold, the barriers' touch order, the ETF trick's gross exposure and the two
# routes to the fractional-difference weights, against hand-computed values.

import unittest
import warnings

import numpy as np

from trading_notes.numerical.financial_data_structures.bar_sampling import (
    CusumFilter,
    ImbalanceBars,
    tick_rule,
)
from trading_notes.numerical.financial_data_structures.etf_trick import EtfTrickBasket
from trading_notes.numerical.fractional_differentiation.fractional_weights import (
    FractionalDifference,
)
from trading_notes.numerical.labelling_sample_weights.labels import (
    LabelIndicators,
    TimeDecay,
    TripleBarrier,
)


class Uniqueness(unittest.TestCase):
    """Concurrency per time and average uniqueness per label."""

    def test_unused_time_contributes_nothing(self) -> None:
        """Rows (1, 0), (0, 0), (1, 1): concurrency 1, 0, 2; uniqueness (1 + 1/2)/2 and 1/2."""
        labels = LabelIndicators.by_rule(
            [(0, 1), (2, 3)], [1, 2, 3], lambda a, b, t: float(t in (1, 3) and (a == 0 or t == 3))
        )
        np.testing.assert_array_equal(labels.matrix, [[1.0, 0.0], [0.0, 0.0], [1.0, 1.0]])
        with np.errstate(all="raise"):
            c, u = labels.concurrency(), labels.average_uniqueness()
        np.testing.assert_array_equal(c, [1.0, 0.0, 2.0])
        np.testing.assert_array_equal(u, [0.75, 0.5])

    def test_sequential_bootstrap_example(self) -> None:
        """AFML's spans {0:2, 2:3, 4:5}: after label 2 the probabilities are {5, 3, 6}/14."""
        labels = LabelIndicators.closed_spans([(0, 2), (2, 3), (4, 5)], 6)
        np.testing.assert_array_equal(labels.concurrency(), [1, 1, 2, 1, 1, 1])
        _, probabilities = labels.sequential_probabilities([1])
        np.testing.assert_allclose(probabilities, np.array([5, 3, 6]) / 14, rtol=1e-15)
        drawn = labels.sequential_bootstrap(3, np.random.default_rng(1))
        self.assertEqual(len(drawn), 3)
        self.assertTrue(all(0 <= d < 3 for d in drawn))
        self.assertEqual(labels.sample_uniqueness([0, 2]), 1.0)

    def test_time_decay_ends(self) -> None:
        """d(S) = 1 always; c = 1 means no decay; c < 0 zeroes the oldest share -c."""
        for c in (1.0, 0.5, 0.0, -0.5):
            a, b = TimeDecay(last=c).coefficients(2.0)
            self.assertAlmostEqual(a + b * 2.0, 1.0, places=15)
        self.assertEqual(TimeDecay(last=1.0).coefficients(2.0), (1.0, 0.0))
        a, b = TimeDecay(last=-0.5).coefficients(2.0)
        self.assertAlmostEqual(-a / b, 1.0, places=15)


class Barriers(unittest.TestCase):
    """The first barrier touched sets the label; the vertical barrier labels by sign or 0."""

    def test_touch_order_and_vertical_rules(self) -> None:
        """Up first, down first, and a flat path under both vertical rules."""
        barrier = TripleBarrier(profit_take=0.02, stop_loss=0.01)
        self.assertEqual(barrier.label(np.array([100, 101, 102.5, 99.0])), (1, 2))
        self.assertEqual(barrier.label(np.array([100, 99.4, 98.9, 103.0])), (-1, 2))
        flat = np.array([100, 100.5, 99.5, 100.0])
        self.assertEqual(barrier.label(flat), (0, 3))
        rising = np.array([100, 100.3, 100.6, 100.8])
        zero = barrier.model_copy(update={"label_vertical": "zero"})
        self.assertEqual((barrier.label(rising), zero.label(rising)), ((1, 3), (0, 3)))


class Bars(unittest.TestCase):
    """The tick rule carries signs forward; the CUSUM filter needs a move beyond h."""

    def test_tick_rule_carries_the_previous_sign(self) -> None:
        """Unchanged prices repeat the last sign, the first one taken from b0."""
        prices = np.array([10.00, 10.01, 10.01, 10.00, 10.00, 10.02])
        self.assertEqual(tick_rule(prices, b0=1).tolist(), [1, 1, -1, -1, 1])
        self.assertEqual(tick_rule(np.array([10, 10, 10.01]), b0=-1).tolist(), [-1, 1])

    def test_empty_results_keep_the_integer_dtype(self) -> None:
        """No price change and no closed bar give empty int64 arrays that index arrays."""
        values = np.arange(5.0)
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            signs = tick_rule(np.array([10.0]), b0=1)
            short = ImbalanceBars(e_t0=50.0).bar_ends(np.ones(60, dtype=np.int64), np.ones(60))
            rng = np.random.default_rng(3)
            side = np.where(rng.random(400) < 0.5, 1, -1)
            never = ImbalanceBars(e_t0=1e9).bar_ends(side, np.ones(400))
        for empty in (signs, short, never):
            self.assertEqual((empty.dtype, empty.shape), (np.int64, (0,)))
            self.assertEqual(values[empty].shape, (0,))
        self.assertEqual(tick_rule(np.array([1.0, 2.0]), b0=-1).dtype, np.int64)

    def test_one_sided_burn_in(self) -> None:
        """Tick bars accept a one-sided burn-in silently; volume runs bars reject it."""
        side = np.ones(300, dtype=np.int64)
        side[150:] = -1
        volume = np.ones(300)
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            ends = ImbalanceBars(e_t0=50.0).bar_ends(side, volume)
        self.assertEqual(ends.dtype, np.int64)
        with self.assertRaises(ValueError):
            ImbalanceBars(e_t0=50.0, kind="volume", runs=True).bar_ends(side, volume)
        with self.assertRaises(ValueError):
            ImbalanceBars(e_t0=50.0).bar_ends(side, volume[:-1])

    def test_cusum_threshold_is_strict(self) -> None:
        """A run of exactly h fires nothing; a run just beyond it fires once."""
        cusum = CusumFilter(threshold=0.5)
        self.assertEqual(cusum.events(np.array([0, 0.25, 0.5])), [])
        self.assertEqual(cusum.events(np.array([0, 0.25, 0.5001])), [2])


class EtfTrick(unittest.TestCase):
    """Holdings are sized at the next open, so gross exposure equals |K| at that open."""

    def test_gross_exposure_at_the_open(self) -> None:
        """Sum |h| o phi = |K| for positive opens; K < 0 flips every holding."""
        basket = EtfTrickBasket(weights=np.array([0.6, -0.4]))
        opens, phi = np.array([101.5, 49.2]), np.array([1.0, 1.0])
        for capital in (1.0, 0.3, -0.2):
            h = basket.holdings(capital, opens, phi)
            self.assertAlmostEqual(float((np.abs(h) * opens * phi).sum()), abs(capital), places=15)
        self.assertLess(basket.holdings(-0.2, opens, phi)[0], 0.0)


class FractionalWeights(unittest.TestCase):
    """The recurrence and the binomial series give the same weights."""

    def test_routes_agree_and_integer_orders_terminate(self) -> None:
        """D = 1 gives (1, -1, 0, ...); d = 0.4 agrees across routes to 1e-15."""
        np.testing.assert_array_equal(FractionalDifference(order=1.0).weights(4), [1, -1, 0, 0])
        fd = FractionalDifference(order=0.4)
        np.testing.assert_allclose(fd.weights(12), fd.binomial_weights(12), atol=1e-15)
        self.assertTrue(np.all(fd.weights(50)[1:] < 0))

    def test_fixed_width_of_integer_orders(self) -> None:
        """D = 0, 1 and 2 give the series, its first and its second difference."""
        series = np.array([1.0, 3.0, 6.0, 10.0])
        np.testing.assert_array_equal(FractionalDifference(order=0.0).fixed_width(series), series)
        out = FractionalDifference(order=1.0).fixed_width(series)
        np.testing.assert_array_equal(out, np.diff(series))
        out = FractionalDifference(order=2.0).fixed_width(series)
        np.testing.assert_array_equal(out, np.diff(series, 2))

    def test_fixed_width_of_a_fractional_order(self) -> None:
        """D = 0.5 at thr 0.2 keeps (1, -1/2): each output is x_t - x_{t-1}/2."""
        fd = FractionalDifference(order=0.5)
        self.assertEqual(fd.width(0.2), 2)
        series = np.array([2.0, 4.0, 8.0])
        np.testing.assert_array_equal(fd.fixed_width(series, thr=0.2), [3.0, 6.0])

    def test_unreached_cutoff_raises(self) -> None:
        """|w_k| for d = 0.4 stays above 1e-12 for 10^5 weights; thr > 1 drops even w_0."""
        fd = FractionalDifference(order=0.4)
        series = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        for thr in (1e-12, 0.0, -1.0, 1.5):
            with self.assertRaises(ValueError):
                fd.fixed_width(series, thr=thr)

    def test_short_history_gives_no_observations(self) -> None:
        """A series shorter than the window yields an empty float array, not zeros."""
        fd = FractionalDifference(order=0.4)
        width = fd.width(1e-4)
        out = fd.fixed_width(np.arange(float(width - 1)))
        self.assertEqual((out.dtype, out.shape), (np.float64, (0,)))
        self.assertEqual(fd.fixed_width(np.arange(float(width))).shape, (1,))


if __name__ == "__main__":
    unittest.main()
