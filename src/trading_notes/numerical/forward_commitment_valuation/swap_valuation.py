"""A semiannual bond coupon calendar and the legs of an equity swap against an overnight rate."""

import datetime

import numpy as np
from numpy.typing import NDArray

from trading_notes.records import Record

type Floats = NDArray[np.float64]


def next_business_day(d: datetime.date) -> datetime.date:
    """Return d, or the Monday after it when it falls on a weekend; no holidays are modelled."""
    while d.weekday() >= 5:
        d += datetime.timedelta(days=1)
    return d


class SemiannualCoupons(Record):
    """Coupon dates stepped back six months from maturity, not from the dates entered.

    A coupon date on a weekend is paid the next business day (31 CFR 356.30(a)).

    Attributes:
        maturity: The final coupon date, whose day of month every coupon date keeps.
    """

    maturity: datetime.date

    def dates_from(self, first_needed: datetime.date) -> list[datetime.date]:
        """Return the coupon dates from the last one on or before first_needed, in order."""
        dates: list[datetime.date] = []
        y, m = self.maturity.year, self.maturity.month
        while True:
            d = datetime.date(y, m, self.maturity.day)
            if d < first_needed:
                return sorted([*dates, d])
            dates.append(d)
            m -= 6
            if m <= 0:
                m, y = m + 12, y - 1

    def payment_date(self, coupon: datetime.date) -> datetime.date:
        """Return the date the coupon is paid."""
        return next_business_day(coupon)


class EquitySwap(Record):
    """An equity-for-overnight-rate swap between resets, valued by replication.

    The next equity payment N(E_next / E_reset - 1) is worth N(E_t / E_reset - P(t, T_next)),
    and the next compounded-overnight payment N(A_t - P(t, T_next)), where A_t is the growth
    since the reset. At a payment date P = 1 and the PV is the payment itself; just after a
    reset the next equity payment is worth N(1 - P), not zero.

    Attributes:
        notional: N, in currency units.
    """

    notional: float

    def next_equity_payment(self, e_rel: float, discount: float) -> float:
        """Return the PV of the next equity payment for E_t / E_reset and P(t, T_next)."""
        return self.notional * (e_rel - discount)

    def legs(self, e_rel: float, a_on: float, dfs: Floats) -> tuple[float, float]:
        """Return the equity and overnight floating legs from the payment discount factors.

        Args:
            e_rel: E_t / E_reset.
            a_on: Compounded overnight growth since the reset.
            dfs: P(t, T_k) for the remaining payment dates, the next one first.
        """
        later = sum(dfs[k - 1] - dfs[k] for k in range(1, len(dfs)))
        return self.notional * ((e_rel - dfs[0]) + later), self.notional * ((a_on - dfs[0]) + later)
