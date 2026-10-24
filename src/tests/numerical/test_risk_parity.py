"""Tests of the risk-parity example's variance shares, inputs and comparisons."""

import contextlib
import io
import unittest
from unittest import mock

import numpy as np

from trading_notes.numerical.portfolio_construction_models import risk_parity_checks as rp
from trading_notes.numerical.report import CheckReport


class VarianceShares(unittest.TestCase):
    """Shares w_i (Sigma w)_i / w' Sigma w sum to one and leave their inputs alone."""

    def test_shares_sum_to_one_and_inputs_are_unchanged(self) -> None:
        """The 60/40 shares are about 93/7 and sum to one; w and Sigma are not modified."""
        w, model = np.array([0.6, 0.4]), rp.stock_bond_model()
        S = model.sigma
        w0, S0 = w.copy(), S.copy()
        shares = model.variance_shares(w)
        self.assertEqual(shares.dtype, np.float64)
        self.assertAlmostEqual(float(shares.sum()), 1.0, places=15)
        self.assertEqual(round(shares[0] * 100), 93)
        np.testing.assert_array_equal(w, w0)
        np.testing.assert_array_equal(S, S0)

    def test_each_call_builds_a_new_covariance(self) -> None:
        """Changing one covariance matrix cannot reach the next run's."""
        first = rp.stock_bond_model().sigma
        first[0, 0] = 99.0
        second = rp.stock_bond_model().sigma
        self.assertEqual(second[0, 0], rp.STOCK_VOL**2)
        self.assertEqual(second[0, 1], second[1, 0])


class Comparisons(unittest.TestCase):
    """Each check keeps its rounding and tolerance."""

    def failures(self, check: str, **constants: object) -> list[str]:
        """Return the failures of one check run with some module constants replaced."""
        report = CheckReport()
        with contextlib.ExitStack() as stack:
            for name, value in constants.items():
                stack.enter_context(mock.patch.object(rp, name, value))
            stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
            getattr(rp, check)(report)
        return report.failures

    def test_rounded_percentages(self) -> None:
        """Equal volatilities give 50/50 shares and weights, which fail both rounded checks."""
        self.assertEqual(self.failures("check_sixty_forty"), [])
        self.assertEqual(self.failures("check_two_asset_erc"), [])
        self.assertEqual(
            self.failures("check_sixty_forty", BOND_VOL=0.151),
            ["60/40: stocks carry about 93% of variance"],
        )
        self.assertEqual(
            self.failures("check_two_asset_erc", BOND_VOL=0.151),
            ["two-asset ERC weights about 23/77 with equal contributions"],
        )

    def test_inverse_volatility_rounds_before_comparing(self) -> None:
        """Weights within half a percentage point of 48/24/16/12 pass; equal ones fail."""
        self.assertEqual(self.failures("check_inverse_volatility"), [])
        self.assertEqual(
            self.failures("check_inverse_volatility", MRT_VOLS=(0.101, 0.2, 0.3, 0.4)), []
        )
        self.assertEqual(
            self.failures("check_inverse_volatility", MRT_VOLS=(0.25, 0.25, 0.25, 0.25)),
            ["MRT sec. 4.1: 48/24/16/12"],
        )


if __name__ == "__main__":
    unittest.main()
