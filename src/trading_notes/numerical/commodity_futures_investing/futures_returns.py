"""Collateralised futures positions rolled at expiry, rebalanced indexes and commodity swaps."""

from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray

from trading_notes.records import Record

type Floats = NDArray[np.float64]


class RolledPosition(Record):
    """A fully collateralised position in the 3-month contract, rolled at each expiry.

    Each contract is bought at S(1 + basis) and converges to the spot at expiry; the
    collateral earns a quarter of the annual bill yield each quarter.

    Attributes:
        basis: The futures price's premium (negative in backwardation) over spot at purchase.
        collateral_rate: The annual T-bill yield on the collateral.
    """

    basis: float
    collateral_rate: float

    def index_values(self, spot_path: Sequence[float]) -> tuple[float, float]:
        """Return the total-return and the excess-return index values after the spot path."""
        value = 1.0
        excess = 1.0
        for q in range(len(spot_path) - 1):
            f_buy = spot_path[q] * (1 + self.basis)
            f_sell = spot_path[q + 1]  # converges to spot at expiry
            r_fut = f_sell / f_buy - 1
            excess *= 1 + r_fut
            value *= 1 + r_fut + self.collateral_rate / 4
        return value, excess


class TwoCommodityIndex(Record):
    """An index of two commodities, held or rebalanced to fixed weights each period.

    Attributes:
        first: The first commodity's returns per period.
        second: The second commodity's returns per period.
    """

    first: Floats
    second: Floats

    def rebalanced(self, w: float) -> float:
        """Return the index return with weight w on the first commodity reset each period."""
        return float(np.prod(1 + w * self.first + (1 - w) * self.second)) - 1

    def buy_and_hold(self, w: float) -> float:
        """Return the return of holding weight w in the first commodity without rebalancing."""
        return float(w * np.prod(1 + self.first) + (1 - w) * np.prod(1 + self.second)) - 1


class CommoditySwap(Record):
    """A fixed-for-floating commodity swap settled annually.

    Attributes:
        fixed: The fixed price per unit.
        volume: The units settled each year.
    """

    fixed: float
    volume: float

    def value(self, forwards: Floats, discount_factors: Floats) -> float:
        """Return the value to the fixed payer: sum of discounted (F_t - fixed) x volume."""
        return float(np.sum((forwards - self.fixed) * self.volume * discount_factors))
