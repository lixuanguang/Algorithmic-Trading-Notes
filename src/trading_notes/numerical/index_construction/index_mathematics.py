"""Index levels, divisors, total returns and bond index returns (S&P DJI and Bloomberg rules)."""

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]


class PriceWeightedIndex(Record):
    """A price-weighted index: level = sum of prices / divisor.

    Attributes:
        divisor: The divisor.
    """

    divisor: float

    @classmethod
    def based(cls, prices: Floats, level: float) -> PriceWeightedIndex:
        """Return the index whose divisor puts these prices at the given level.

        S&P DJI eq. (6): after a split or a constituent change the divisor is reset this way,
        so the level is unchanged by the change.
        """
        return cls(divisor=float(prices.sum() / level))

    def level(self, prices: Floats) -> float:
        """Return the index level at these prices."""
        return float(prices.sum() / self.divisor)


class CapWeightedIndex(Record):
    """A float-adjusted capitalisation-weighted index: level = market value / divisor.

    Attributes:
        shares: Float-adjusted shares q of each constituent.
        divisor: The divisor.
    """

    shares: Floats
    divisor: float

    @classmethod
    def based(cls, prices: Floats, shares: Floats, level: float) -> CapWeightedIndex:
        """Return the index whose divisor puts these prices at the given base level."""
        return cls(shares=shares, divisor=float((prices * shares).sum() / level))

    def market_value(self, prices: Floats) -> float:
        """Return the index market value sum p_i q_i."""
        return float((prices * self.shares).sum())

    def level(self, prices: Floats) -> float:
        """Return the index level at these prices."""
        return self.market_value(prices) / self.divisor

    def weights(self, prices: Floats) -> Floats:
        """Return each constituent's share p_i q_i / MV of the market value."""
        w: Floats = prices * self.shares / self.market_value(prices)
        return w

    def after_issue(self, shares: Floats, added_value: float, level: float) -> CapWeightedIndex:
        """Return the index with new shares and the divisor raised by eq. (7), D + CMV / level."""
        return CapWeightedIndex(shares=shares, divisor=self.divisor + added_value / level)

    def rescaled_divisor(self, new_value: float, old_value: float) -> float:
        """Return the divisor of eq. (6), D x new market value / old market value."""
        return self.divisor * new_value / old_value

    def dividend_points(self, dividends: Floats) -> float:
        """Return the index dividend points sum d_i q_i / D on the ex-date."""
        return float((dividends * self.shares).sum() / self.divisor)

    def equal_weight_factors(self, prices: Floats) -> Floats:
        """Return S&P DJI's additional weight factors Z / (N p_i q_i), Z the market value."""
        fav = prices * self.shares
        awf: Floats = fav.sum() / (len(fav) * fav)
        return awf


def one_way_turnover(before: Floats, after: Floats) -> float:
    """Return half the sum of absolute weight changes."""
    return float(np.abs(before - after).sum() / 2)


class BondIndexMonth(Record):
    """One month of a bond index's returns universe, prices per 100 par (Bloomberg rules).

    Returns are measured on the beginning dirty value; weights are the beginning market values.

    Attributes:
        par: Par outstanding of each bond.
        clean0: Clean prices at the start.
        accrued0: Accrued interest at the start.
        clean1: Clean prices at the end.
        accrued1: Accrued interest at the end.
        coupon_paid: Coupons paid during the month.
    """

    par: Floats
    clean0: Floats
    accrued0: Floats
    clean1: Floats
    accrued1: Floats
    coupon_paid: Floats

    @property
    def dirty0(self) -> Floats:
        """Return the beginning dirty prices."""
        d: Floats = self.clean0 + self.accrued0
        return d

    def price_returns(self) -> Floats:
        """Return each bond's price return (clean1 - clean0) / dirty0."""
        r: Floats = (self.clean1 - self.clean0) / self.dirty0
        return r

    def coupon_returns(self) -> Floats:
        """Return each bond's coupon return (accrued1 - accrued0 + coupon) / dirty0."""
        r: Floats = (self.accrued1 - self.accrued0 + self.coupon_paid) / self.dirty0
        return r

    def total_returns(self) -> Floats:
        """Return each bond's price plus coupon return."""
        r: Floats = self.price_returns() + self.coupon_returns()
        return r

    def market_values(self) -> Floats:
        """Return the beginning market values par x dirty0 / 100."""
        mv: Floats = self.par * self.dirty0 / 100
        return mv

    def index_return(self) -> float:
        """Return the market-value-weighted total return of the month."""
        mv0 = self.market_values()
        return float((mv0 / mv0.sum() * self.total_returns()).sum())
