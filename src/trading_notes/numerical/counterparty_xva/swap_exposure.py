"""Interest rate swaps valued path by path under Hull-White, for exposure simulation."""

import math

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.arbitrage_free_valuation.short_rate_models import (
    HullWhite,
    SvenssonCurve,
)
from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]


def par_rate(curve: SvenssonCurve, n: int) -> float:
    """Return the par swap rate of an annual n-year swap on the curve."""
    return (1 - curve.discount(n)) / sum(curve.discount(j) for j in range(1, n + 1))


class AnnualSwap(Record):
    """A single-curve annual swap, floating rate set in advance and paid in arrears.

    Attributes:
        fixed_rate: K.
        years: n, the final payment date.
        payer: Whether the holder pays fixed.
        notional: The notional.
    """

    fixed_rate: float
    years: int
    payer: bool
    notional: float

    def value(self, model: HullWhite, t: float, x: Floats, last_reset_bond: Floats) -> Floats:
        """Return the ex-coupon value at t on each path.

        Args:
            model: The short-rate model.
            t: The valuation date.
            x: The model factor on each path.
            last_reset_bond: P(k, k + 1) on each path, set at the last reset k = floor(t).
        """
        n = self.years
        if t >= n:
            return np.zeros_like(x)
        k = math.floor(t)  # last reset at k (k = 0 uses today's curve)
        nxt = model.bond(t, k + 1, x)
        floating = nxt / last_reset_bond - model.bond(t, n, x)
        fixed = self.fixed_rate * sum(model.bond(t, j, x) for j in range(k + 1, n + 1))
        return self.notional * (floating - fixed) * (1 if self.payer else -1)
