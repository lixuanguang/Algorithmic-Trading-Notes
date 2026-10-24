"""Tests of the rate-model, rate-tree and order-flow domain classes behind several examples."""

# The examples' own checks run in test_checks.py. These pin down boundaries and return contracts
# that the examples do not reach: principal components of few maturities, scalar against array
# discount factors, the two independent binomial trees and the exact decimal trade-signing rules.

import unittest
from decimal import Decimal

import numpy as np
from pydantic import ValidationError

from trading_notes.numerical.arbitrage_free_valuation.short_rate_models import (
    GSW_CURVE,
    HullWhite,
)
from trading_notes.numerical.counterparty_xva.tree_cva import DefaultRisk, ShortRateTree
from trading_notes.numerical.default_correlation.tranche_pricing import tranche_payoff
from trading_notes.numerical.embedded_option_bonds.binomial_tree import LognormalTree
from trading_notes.numerical.order_flow_statistics.covariance_estimators import (
    ObservedPrices,
    refresh_times,
)
from trading_notes.numerical.order_flow_statistics.trade_classification import Quote
from trading_notes.numerical.term_structure_returns.curve_bootstrap import PrincipalComponents

TWO_MATURITIES = np.array([[0.01, 0.02], [-0.01, 0.01], [0.03, -0.02], [0.02, 0.04]])
PAR = (0.035, 0.042, 0.047, 0.052)


class PrincipalComponentCounts(unittest.TestCase):
    """The default signs every available component; explicit counts are bounded."""

    def test_two_maturities_default_matches_explicit_two(self) -> None:
        """A two-column matrix works by default, as with signed=2, and signs both components."""
        default = PrincipalComponents.of(TWO_MATURITIES)
        explicit = PrincipalComponents.of(TWO_MATURITIES, signed=2)
        np.testing.assert_array_equal(default.loadings, explicit.loadings)
        np.testing.assert_array_equal(default.variances, explicit.variances)
        self.assertEqual(default.loadings.shape, (2, 2))
        self.assertTrue(all(default.loadings[:, k].sum() >= 0 for k in range(2)))
        self.assertTrue(np.all(np.diff(default.variances) <= 0))

    def test_signing_flips_signs_only(self) -> None:
        """signed=0 leaves eigh's signs; either way the components agree up to sign."""
        raw = PrincipalComponents.of(TWO_MATURITIES, signed=0)
        signed = PrincipalComponents.of(TWO_MATURITIES)
        np.testing.assert_array_equal(np.abs(raw.loadings), np.abs(signed.loadings))
        np.testing.assert_array_equal(raw.variances, signed.variances)

    def test_more_maturities_keep_the_leading_three(self) -> None:
        """With five maturities the leading three loadings equal those of signed=3."""
        rng = np.random.default_rng(7)
        changes = rng.standard_normal((40, 5)) @ rng.standard_normal((5, 5))
        default, three = PrincipalComponents.of(changes), PrincipalComponents.of(changes, signed=3)
        np.testing.assert_array_equal(default.loadings[:, :3], three.loadings[:, :3])
        np.testing.assert_array_equal(np.abs(default.loadings), np.abs(three.loadings))

    def test_single_maturity(self) -> None:
        """One column gives one component holding all the variance."""
        pcs = PrincipalComponents.of(TWO_MATURITIES[:, :1])
        self.assertEqual(pcs.loadings.tolist(), [[1.0]])
        self.assertEqual(pcs.shares().tolist(), [1.0])

    def test_invalid_counts_and_shapes_raise(self) -> None:
        """Counts outside 0..maturities and non-matrix or single-row input raise ValueError."""
        for signed in (-1, 3):
            with self.subTest(signed=signed), self.assertRaisesRegex(ValueError, r"0\.\.2"):
                PrincipalComponents.of(TWO_MATURITIES, signed=signed)
        for bad in (TWO_MATURITIES[0], TWO_MATURITIES[:1], np.zeros((3, 0))):
            with self.subTest(shape=bad.shape), self.assertRaises(ValueError):
                PrincipalComponents.of(bad)


class HullWhiteDiscount(unittest.TestCase):
    """path_discount returns a float for a scalar integral and an array for an array."""

    model = HullWhite(curve=GSW_CURVE, a=0.1, sigma=0.01)

    def test_scalar_and_array_values_and_types(self) -> None:
        """Each array element equals the scalar result for that integral, bit for bit."""
        t = 1.5
        scalar = self.model.path_discount(t, 0.0)
        self.assertIs(type(scalar), float)
        self.assertAlmostEqual(
            scalar, GSW_CURVE.discount(t) * np.exp(-0.5 * self.model.var_int(t)), places=15
        )
        integrals = np.array([-0.01, 0.0, 0.02])
        vector = self.model.path_discount(t, integrals)
        self.assertIsInstance(vector, np.ndarray)
        self.assertEqual((vector.shape, vector.dtype), ((3,), np.float64))
        self.assertEqual(vector.tolist(), [self.model.path_discount(t, x) for x in integrals])
        self.assertIs(type(self.model.path_discount(t, np.float64(0.0))), float)

    def test_tranche_payoff_types(self) -> None:
        """A scalar loss gives a float, an array an array of its shape, with equal values."""
        self.assertIs(type(tranche_payoff(0.05, 0.03, 0.07)), float)
        self.assertEqual(tranche_payoff(0.05, 0.03, 0.07), np.clip(0.05, 0.03, 0.07) - 0.03)
        losses = np.array([0.0, 0.05, 0.2])
        payoff = tranche_payoff(losses, 0.03, 0.07)
        self.assertIsInstance(payoff, np.ndarray)
        self.assertEqual(payoff.tolist(), [tranche_payoff(float(x), 0.03, 0.07) for x in losses])


class RateTrees(unittest.TestCase):
    """The embedded-option lattice and the CVA tree: calibration, values and default risk."""

    def test_lognormal_tree_reprices_par_bonds(self) -> None:
        """Each truncated calibrated tree prices its par bond at 100; the value is a float."""
        tree = LognormalTree.calibrate(PAR)
        self.assertEqual(len(tree.lows), 4)
        for k in range(4):
            value = LognormalTree(lows=tree.lows[: k + 1]).value([100 * PAR[k]] * (k + 1))
            self.assertIs(type(value), float)
            self.assertAlmostEqual(value, 100.0, places=9)
        self.assertAlmostEqual(tree.rate(3, 2) / tree.rate(3, 1), np.exp(0.2), places=14)

    def test_options_bound_the_straight_value(self) -> None:
        """A call caps and a put floors the straight bond's value on the same tree."""
        tree = LognormalTree.calibrate(PAR)
        straight = tree.value([6.5] * 4)
        self.assertLess(tree.value([6.5] * 4, call=100.0), straight)
        self.assertGreater(tree.value([6.5] * 4, put=100.0), straight)

    def test_cva_tree_routes_agree(self) -> None:
        """Node-weighted and pathwise bond CVA agree; without hazard every CVA is zero."""
        tree = ShortRateTree.calibrate(PAR, 0.10)
        risk = DefaultRisk(hazard=(0.015,) * 4, recovery=0.4)
        self.assertEqual(tree.periods, 4)
        self.assertAlmostEqual(tree.bond_cva(5.0, risk), tree.bond_path_cva(5.0, risk), places=10)
        safe = DefaultRisk(hazard=(0.0,) * 4, recovery=0.4)
        self.assertEqual(
            (tree.bond_cva(5.0, safe), tree.swap_cva(PAR[-1], safe), tree.floater_cva(0.0, safe)),
            (0.0, 0.0, 0.0),
        )
        self.assertEqual(risk.survival(2), [1.0, np.exp(-0.015), np.exp(-0.03)])

    def test_state_prices_reprice_zero_coupon_bonds(self) -> None:
        """The state prices of each date sum to that date's discount factor on the tree."""
        tree = ShortRateTree.calibrate(PAR, 0.10)
        ad = tree.state_prices()
        self.assertEqual([len(a) for a in ad], [1, 2, 3, 4, 5])
        self.assertAlmostEqual(float(ad[1].sum()), 1 / (1 + PAR[0]), places=15)


class TradeSigning(unittest.TestCase):
    """The quote rules compare exact decimals and reject float prices."""

    def test_midpoint_is_exact(self) -> None:
        """A trade at the half-tick midpoint falls to the tick test instead of the quote rule."""
        quote = Quote(bid=Decimal("10.00"), ask=Decimal("10.01"))
        self.assertEqual(quote.mid, Decimal("10.005"))
        self.assertEqual(quote.lee_ready(Decimal("10.005"), [Decimal("10.01")]), -1)
        self.assertEqual(quote.lee_ready(Decimal("10.005"), []), 0)

    def test_rules_differ_inside_the_spread(self) -> None:
        """Inside a 10-cent spread after a downtick the three rules disagree as documented."""
        quote = Quote(bid=Decimal("10.00"), ask=Decimal("10.10"))
        prior = [Decimal("10.09")]
        signs = [
            (quote.lee_ready(p, prior), quote.emo(p, prior), quote.clnv(p, prior))
            for p in (Decimal("10.08"), Decimal("10.06"), Decimal("10.03"))
        ]
        self.assertEqual(signs, [(1, -1, 1), (1, -1, -1), (-1, -1, -1)])

    def test_float_quotes_are_rejected(self) -> None:
        """A float bid is rejected rather than converted to an inexact Decimal."""
        with self.assertRaises(ValidationError):
            Quote.model_validate({"bid": 10.0, "ask": Decimal("10.01")})


class AsynchronousCovariance(unittest.TestCase):
    """Previous-tick sampling and Hayashi-Yoshida on hand-checkable series."""

    def test_previous_tick_and_refresh_times(self) -> None:
        """Values hold until the next observation; refresh times wait for every series."""
        prices = ObservedPrices(times=np.array([1.0, 4.0]), values=np.array([0.0, 2.0, 5.0]))
        at = np.array([0.5, 1.0, 3.9, 4.0, 9.0])
        self.assertEqual(prices.previous_tick(at).tolist(), [0.0, 2.0, 2.0, 5.0, 5.0])
        times = [np.array([1.0, 4.0, 5.0, 9.0]), np.array([2.0, 3.0, 7.0, 8.0])]
        self.assertEqual(refresh_times(times).tolist(), [2.0, 4.0, 7.0, 9.0])

    def test_hayashi_yoshida_of_overlapping_intervals(self) -> None:
        """Only overlapping return intervals contribute, and the estimator is symmetric."""
        first = ObservedPrices(times=np.array([1.0, 2.0]), values=np.array([0.0, 1.0, 3.0]))
        second = ObservedPrices(times=np.array([1.5]), values=np.array([0.0, 4.0]))
        # (0, 1] and (1, 2] both overlap (0, 1.5]: 1 * 4 + 2 * 4.
        self.assertEqual(first.hayashi_yoshida(second), 12.0)
        self.assertEqual(second.hayashi_yoshida(first), 12.0)


if __name__ == "__main__":
    unittest.main()
