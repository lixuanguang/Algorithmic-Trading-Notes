"""NYMEX crude and natural-gas contract months on a trading calendar, and EIA report timing."""

import bisect
import datetime as dt
from collections.abc import Sequence
from typing import Final, Literal

from trading_notes.numerical.records import Record

type Market = Literal["WTI", "NG"]
type Month = tuple[int, int]

# Days after the week-ending Friday at which the weekly stocks report is treated as public.
REPORT_LAG: Final[dict[Market, int]] = {"WTI": 6, "NG": 7}
# Business-day offsets of the natural-gas expiry under which contract identity is required;
# the data show an earlier roll before 1997.
IDENTITY_RULES: Final[dict[Market, tuple[int, ...]]] = {"WTI": (3,), "NG": (3, 5, 6)}


def _next_month(y: int, m: int) -> Month:
    return (y, m + 1) if m < 12 else (y + 1, 1)


class ContractCalendar(Record):
    """A market's futures contracts on the trading days of its data, in order.

    Attributes:
        market: WTI crude (NYMEX Rule 200102.F) or Henry Hub gas (Rule 220102.F).
        days: The trading days, sorted.
    """

    market: Market
    days: tuple[dt.date, ...]

    def business_day_before(self, x: dt.date | None, k: int) -> dt.date | None:
        """Return the k-th trading day strictly before x, or None before the calendar starts."""
        if x is None:
            return None
        i = bisect.bisect_left(self.days, x)
        return self.days[i - k] if i - k >= 0 else None

    def expiry(self, y: int, m: int, ng_days: int = 3) -> dt.date | None:
        """Return the last trading day of the contract for delivery month (y, m).

        Gas expires ng_days business days before the first day of the delivery month; crude
        three business days before the 25th of the month before, or before the business day
        preceding the 25th when the 25th is not one. None if the month is beyond the data.
        """
        cal = self.days
        if dt.date(y, m, 1) > cal[-1]:
            return None  # beyond the data calendar: not computable
        if self.market == "NG":
            return self.business_day_before(dt.date(y, m, 1), ng_days)
        py, pm = (y, m - 1) if m > 1 else (y - 1, 12)
        x = dt.date(py, pm, 25)
        if x in set(cal):
            return self.business_day_before(x, 3)
        return self.business_day_before(self.business_day_before(x, 1), 3)

    def delivery(self, d: dt.date, nth: int = 1, ng_days: int = 3) -> Month | None:
        """Return the delivery month of the nth nearby contract on trading date d.

        None when the front contract's expiry falls after the data end too close to d to know.
        """
        cal = self.days
        y, m = d.year, d.month
        while True:
            e = self.expiry(y, m, ng_days)
            if e is None and dt.date(y, m, 1) > cal[-1]:
                # expiry falls after the data end; it is certainly after d when its anchor date
                # (the 1st of the delivery month for NG, the 25th of the month before for WTI)
                # is more than ten days after d
                anchor = (
                    dt.date(y, m, 1)
                    if self.market == "NG"
                    else dt.date(y if m > 1 else y - 1, m - 1 if m > 1 else 12, 25)
                )
                if (anchor - d).days > 10:
                    break
                return None
            if e is not None and e >= d:
                break
            y, m = _next_month(y, m)
        for _ in range(nth - 1):
            y, m = _next_month(y, m)
        return (y, m)

    def same_contract(self, d0: dt.date, n0: int, d1: dt.date, n1: int) -> bool:
        """Return whether the n0th nearby on d0 is the n1th on d1 under every identity rule."""
        return all(
            self.delivery(d0, n0, k) == self.delivery(d1, n1, k)
            for k in IDENTITY_RULES[self.market]
        )

    def complete_month_ends(self) -> list[dt.date]:
        """Return the last trading day of each calendar month whose following month has data."""
        cal = self.days
        return [d for i, d in enumerate(cal[:-1]) if cal[i + 1].month != d.month]


def available_week(
    market: Market, stocks_dates: Sequence[dt.date], t: dt.date, extra: int | None = None
) -> dt.date | None:
    """Return the latest weekly observation (week ending Friday F) public at settlement on t.

    A week is usable from F + 6 days (crude) or F + 7 (gas), or F + 11 when 25 December or
    1 January falls in F+1..F+7; `extra` replaces the lag for a sensitivity.
    """
    i = bisect.bisect_right(stocks_dates, t)
    # the usable week is among the last few before t
    for F in reversed(stocks_dates[max(0, i - 4) : i]):
        if extra is not None:
            lag = extra
        else:
            lag = REPORT_LAG[market]
            if any(
                ((F + dt.timedelta(days=k)).month, (F + dt.timedelta(days=k)).day)
                in ((12, 25), (1, 1))
                for k in range(1, 8)
            ):
                lag = 11
        if F + dt.timedelta(days=lag) <= t:
            return F
    return None
