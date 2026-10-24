"""A SOFR floating-rate note: business-day schedule, compounded-in-arrears coupons and price."""

from collections.abc import Callable, Iterable
from datetime import date, timedelta
from itertools import pairwise

from trading_notes.numerical.records import Record
from trading_notes.numerical.us_calendar import last_weekday, nth_weekday


def federal_reserve_holidays(y: int) -> set[date]:
    """Return the weekday Federal Reserve holidays of a year by rule.

    Sunday holidays move to Monday; Saturday holidays are not observed.
    """
    fixed = [date(y, 1, 1), date(y, 6, 19), date(y, 7, 4), date(y, 11, 11), date(y, 12, 25)]
    fixed = [d0 + timedelta(1) if d0.weekday() == 6 else d0 for d0 in fixed]
    rules = [
        nth_weekday(y, 1, 0, 3),  # Martin Luther King Jr. Day
        nth_weekday(y, 2, 0, 3),  # Washington's Birthday
        last_weekday(y, 5, 0),  # Memorial Day
        nth_weekday(y, 9, 0, 1),  # Labor Day
        nth_weekday(y, 10, 0, 2),  # Columbus Day
        nth_weekday(y, 11, 3, 4),  # Thanksgiving
    ]
    return {d0 for d0 in fixed + rules if d0.weekday() < 5}


class BusinessCalendar(Record):
    """Weekdays other than a set of holidays.

    Attributes:
        holidays: The holidays.
    """

    holidays: frozenset[date]

    @classmethod
    def federal_reserve(cls, years: Iterable[int]) -> BusinessCalendar:
        """Return the calendar of the Federal Reserve holidays of the given years."""
        return cls(holidays=frozenset(set().union(*(federal_reserve_holidays(y) for y in years))))

    def is_business_day(self, d0: date) -> bool:
        """Return whether d0 is a business day."""
        return d0.weekday() < 5 and d0 not in self.holidays

    def modified_following(self, d0: date) -> date:
        """Return the next business day, or the previous one if the next is in another month."""
        d1 = d0
        while not self.is_business_day(d1):
            d1 += timedelta(1)
        if d1.month != d0.month:
            d1 = d0
            while not self.is_business_day(d1):
                d1 -= timedelta(1)
        return d1

    def next_business_day(self, d0: date) -> date:
        """Return the first business day after d0."""
        nxt = d0 + timedelta(1)
        while not self.is_business_day(nxt):
            nxt += timedelta(1)
        return nxt

    def period_growth(
        self, start: date, end: date, rate_of: Callable[[date], float]
    ) -> tuple[float, int]:
        """Return (1 + r_i n_i/360) over business days start <= i < end, and the day count."""
        g, n_sum, d0 = 1.0, 0, start
        while d0 < end:
            nxt = d0 + timedelta(1)
            while nxt < end and not self.is_business_day(nxt):
                nxt += timedelta(1)
            n_i = (nxt - d0).days
            g *= 1 + rate_of(d0) * n_i / 360
            n_sum += n_i
            d0 = nxt
        return g, n_sum


class CompoundedPeriod(Record):
    """A coupon period with SOFR compounded in arrears over its business days.

    Attributes:
        start: The period start.
        end: The period end.
        days: Calendar days in the period.
        growth: The product of (1 + r_i n_i/360) over the period.
        weights: The sum of the day weights n_i.
    """

    start: date
    end: date
    days: int
    growth: float
    weights: int


class SofrFloatingRateNote(Record):
    """A SOFR floater paying compounded SOFR plus a quoted margin, act/360.

    Each period is discounted at its projected compounded growth plus the discount margin, simple
    act/360, so the note is at par on a reset date when the discount margin equals the quoted
    margin.

    Attributes:
        periods: The coupon periods, in order.
        quoted_margin: The margin over compounded SOFR.
    """

    periods: tuple[CompoundedPeriod, ...]
    quoted_margin: float

    @classmethod
    def on_schedule(
        cls,
        calendar: BusinessCalendar,
        schedule: list[date],
        rate_of: Callable[[date], float],
        quoted_margin: float,
    ) -> SofrFloatingRateNote:
        """Return the note whose periods run between consecutive schedule dates."""
        periods = []
        for a, b in pairwise(schedule):
            g, n_sum = calendar.period_growth(a, b, rate_of)
            periods.append(
                CompoundedPeriod(start=a, end=b, days=(b - a).days, growth=g, weights=n_sum)
            )
        return cls(periods=tuple(periods), quoted_margin=quoted_margin)

    def price(self, dm: float, qm: float | None = None) -> float:
        """Return the price per 100 at discount margin dm, at quoted margin qm if given."""
        qm = self.quoted_margin if qm is None else qm
        pv, dfac = 0.0, 1.0
        for k, p in enumerate(self.periods):
            dfac /= p.growth + dm * p.days / 360
            cpn = 100 * (p.growth - 1 + qm * p.days / 360)
            pv += (cpn + (100 if k == len(self.periods) - 1 else 0)) * dfac
        return pv
