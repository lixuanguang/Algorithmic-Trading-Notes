"""Tests of the NYMEX contract calendar and EIA report timing against the contract rules."""

# The calendar is weekdays from November 1995 to early April 1998 less some exchange holidays, so
# that the 25th or the 1st is sometimes not a trading day. Each expected date below is counted by
# hand from the contract rules: WTI (Rule 200102.F) three business days before the 25th of the
# month before delivery, or before the business day preceding it when the 25th is not one; Henry
# Hub (Rule 220102.F) ng_days business days before the delivery month; heating oil the last
# business day before it.

import datetime as dt
import itertools
import unittest
from typing import Final

from trading_notes.numerical.commodity_curves.nymex_contracts import (
    ContractCalendar,
    available_week,
)

D = dt.date
HOLIDAYS: Final = {
    D(1995, 12, 25),
    D(1996, 1, 1),
    D(1996, 11, 25),
    D(1996, 12, 25),
    D(1997, 1, 1),
    D(1997, 4, 25),
    D(1997, 7, 4),
    D(1997, 12, 25),
    D(1998, 1, 1),
}
DAYS: Final = tuple(
    d
    for d in (D(1995, 11, 1) + dt.timedelta(days=k) for k in range(887))
    if d.weekday() < 5 and d not in HOLIDAYS
)
WTI: Final = ContractCalendar(market="WTI", days=DAYS)
NG: Final = ContractCalendar(market="NG", days=DAYS)
HO: Final = ContractCalendar(market="HO", days=DAYS)
# Fridays ending each week from 3 November 1995.
WEEKS: Final = [D(1995, 11, 3) + dt.timedelta(days=7 * k) for k in range(125)]


class Expiries(unittest.TestCase):
    """Last trading days of single contracts under each market's rule."""

    def test_wti(self) -> None:
        """The 25th a trading day, a weekend, and a holiday, including at a year end."""
        self.assertEqual(WTI.expiry(1996, 2), D(1996, 1, 22))  # Thu 25 Jan
        self.assertEqual(WTI.expiry(1996, 9), D(1996, 8, 20))  # Sun 25 Aug -> Fri 23
        self.assertEqual(WTI.expiry(1996, 12), D(1996, 11, 19))  # holiday Mon 25 Nov -> Fri 22
        self.assertEqual(WTI.expiry(1997, 1), D(1996, 12, 19))  # holiday Wed 25 Dec -> Tue 24
        self.assertEqual(WTI.expiry(1997, 5), D(1997, 4, 21))  # holiday Fri 25 Apr -> Thu 24

    def test_natural_gas_offsets(self) -> None:
        """Three, five and six business days before the 1st, across a holiday."""
        self.assertEqual(NG.expiry(1996, 2), D(1996, 1, 29))
        self.assertEqual(NG.expiry(1996, 2, ng_days=5), D(1996, 1, 25))
        self.assertEqual(NG.expiry(1996, 2, ng_days=6), D(1996, 1, 24))
        self.assertEqual(NG.expiry(1997, 1), D(1996, 12, 27))  # 31, 30, then 27 (26 is a day)

    def test_heating_oil(self) -> None:
        """The last business day of the month before delivery; ng_days is ignored."""
        self.assertEqual(HO.expiry(1996, 2), D(1996, 1, 31))
        self.assertEqual(HO.expiry(1996, 12), D(1996, 11, 29))
        self.assertEqual(HO.expiry(1998, 1), D(1997, 12, 31))
        self.assertEqual(HO.expiry(1996, 2, ng_days=6), D(1996, 1, 31))

    def test_months_beyond_the_data_are_unknown(self) -> None:
        """A delivery month after the last trading day has no computable expiry."""
        for calendar in (WTI, NG, HO):
            with self.subTest(market=calendar.market):
                self.assertIsNone(calendar.expiry(1998, 6))


class NearbyContracts(unittest.TestCase):
    """Delivery months of the nth nearby contract, and contract identity across a roll."""

    def test_front_month_rolls_after_expiry(self) -> None:
        """On WTI's expiry day the front is still February; the day after it is March."""
        self.assertEqual(WTI.delivery(D(1996, 1, 22)), (1996, 2))
        self.assertEqual(WTI.delivery(D(1996, 1, 23)), (1996, 3))
        self.assertEqual(WTI.delivery(D(1996, 1, 23), nth=2), (1996, 4))
        self.assertEqual(HO.delivery(D(1996, 1, 31)), (1996, 2))
        self.assertEqual(HO.delivery(D(1996, 2, 1)), (1996, 3))

    def test_contract_identity(self) -> None:
        """Contract 2 on 19 January is contract 1 through March's expiry, 20 February."""
        self.assertTrue(WTI.same_contract(D(1996, 1, 19), 2, D(1996, 2, 20), 1))
        self.assertFalse(WTI.same_contract(D(1996, 1, 19), 2, D(1996, 2, 21), 1))

    def test_gas_identity_needs_every_offset(self) -> None:
        """On 25 January 1996 the front is February under three days but March under six."""
        self.assertTrue(NG.same_contract(D(1996, 1, 22), 1, D(1996, 1, 23), 1))
        self.assertEqual(NG.delivery(D(1996, 1, 25), ng_days=3), (1996, 2))
        self.assertFalse(NG.same_contract(D(1996, 1, 23), 1, D(1996, 1, 25), 1))

    def test_front_month_near_the_data_end(self) -> None:
        """Data ending a week before WTI's anchor date leave the front month unknown."""
        short = ContractCalendar(market="WTI", days=tuple(d for d in DAYS if d <= D(1998, 3, 24)))
        self.assertEqual(short.delivery(D(1998, 3, 2)), (1998, 4))
        self.assertIsNone(short.delivery(D(1998, 3, 24)))


class UnknownIdentity(unittest.TestCase):
    """Identity near the data end, on weekdays from 1 January to Friday 23 October 2026.

    November's WTI contract counts back from Sunday 25 October, after the data end, so its
    expiry is unknown and the front month is unknown within ten days of that date.
    """

    CALENDAR: Final = ContractCalendar(
        market="WTI",
        days=tuple(
            d for d in (D(2026, 1, 1) + dt.timedelta(days=k) for k in range(296)) if d.weekday() < 5
        ),
    )

    def test_both_unknown(self) -> None:
        """Two unknown front months are not the same contract."""
        cal = self.CALENDAR
        self.assertIsNone(cal.delivery(D(2026, 10, 16)))
        self.assertIsNone(cal.delivery(D(2026, 10, 23)))
        self.assertFalse(cal.same_contract(D(2026, 10, 16), 1, D(2026, 10, 23), 1))

    def test_one_unknown(self) -> None:
        """A known front month is not the same contract as an unknown one, in either order."""
        cal = self.CALENDAR
        self.assertEqual(cal.delivery(D(2026, 9, 30)), (2026, 11))
        self.assertFalse(cal.same_contract(D(2026, 9, 30), 1, D(2026, 10, 16), 1))
        self.assertFalse(cal.same_contract(D(2026, 10, 16), 1, D(2026, 9, 30), 1))

    def test_known_match_and_roll(self) -> None:
        """October is the front through its expiry on 22 September; November from the 23rd."""
        cal = self.CALENDAR
        self.assertTrue(cal.same_contract(D(2026, 9, 1), 1, D(2026, 9, 22), 1))
        self.assertTrue(cal.same_contract(D(2026, 9, 22), 2, D(2026, 9, 30), 1))
        self.assertFalse(cal.same_contract(D(2026, 9, 22), 1, D(2026, 9, 23), 1))


class Calendar(unittest.TestCase):
    """Month ends and trading days before a date."""

    def test_complete_month_ends(self) -> None:
        """The last trading day of every month that has a following month in the data."""
        ends = WTI.complete_month_ends()
        self.assertEqual(ends[:3], [D(1995, 11, 30), D(1995, 12, 29), D(1996, 1, 31)])
        self.assertEqual(ends[-1], D(1998, 3, 31))
        self.assertEqual(len(ends), 29)

    def test_business_day_before(self) -> None:
        """None before the calendar starts; a holiday is skipped."""
        self.assertIsNone(WTI.business_day_before(None, 1))
        self.assertIsNone(WTI.business_day_before(DAYS[0], 1))
        self.assertEqual(WTI.business_day_before(DAYS[1], 1), DAYS[0])
        self.assertEqual(WTI.business_day_before(D(1996, 12, 26), 1), D(1996, 12, 24))
        self.assertEqual(WTI.business_day_before(D(1996, 12, 27), 3), D(1996, 12, 23))


class StocksWeek(unittest.TestCase):
    """The latest public stocks week: six days for crude, seven for gas, 11 at Christmas."""

    def test_report_lags(self) -> None:
        """Week of 5 January 1996 is public on 11 January for crude and 12 for gas."""
        self.assertEqual(available_week("WTI", WEEKS, D(1996, 1, 11)), D(1996, 1, 5))
        self.assertEqual(available_week("HO", WEEKS, D(1996, 1, 11)), D(1996, 1, 5))
        self.assertEqual(available_week("NG", WEEKS, D(1996, 1, 11)), D(1995, 12, 29))
        self.assertEqual(available_week("NG", WEEKS, D(1996, 1, 12)), D(1996, 1, 5))

    def test_holiday_weeks_wait_eleven_days(self) -> None:
        """Weeks with 25 December or 1 January in the next seven days are public on F + 11."""
        self.assertEqual(available_week("WTI", WEEKS, D(1996, 1, 1)), D(1995, 12, 15))
        self.assertEqual(available_week("WTI", WEEKS, D(1996, 1, 2)), D(1995, 12, 22))
        self.assertEqual(available_week("WTI", WEEKS, D(1996, 1, 9)), D(1995, 12, 29))

    def test_lag_override(self) -> None:
        """The sensitivity's fixed lag replaces every rule, Christmas included."""
        self.assertEqual(available_week("WTI", WEEKS, D(1996, 1, 19), extra=14), D(1996, 1, 5))
        self.assertEqual(available_week("WTI", WEEKS, D(1996, 1, 18), extra=14), D(1995, 12, 29))


def days_before(x: dt.date | None, k: int) -> dt.date | None:
    """Return the k-th trading day strictly before x by scanning DAYS, or None."""
    if x is None:
        return None
    earlier = [d for d in DAYS if d < x]
    return earlier[-k] if len(earlier) >= k else None


def rule_expiry(market: str, y: int, m: int, ng_days: int) -> dt.date | None:
    """Return the last trading day for delivery month (y, m), read from the rule texts."""
    first = D(y, m, 1)
    if first > DAYS[-1]:
        return None
    if market == "NG":
        return days_before(first, ng_days)
    if market == "HO":
        return days_before(first, 1)
    the_25th = D(*previous_month(y, m), 25)
    return days_before(the_25th if the_25th in DAYS else days_before(the_25th, 1), 3)


def next_month(y: int, m: int) -> tuple[int, int]:
    """Return the month after (y, m)."""
    return (y + 1, 1) if m == 12 else (y, m + 1)


def rule_delivery(market: str, d: dt.date, nth: int, ng_days: int) -> tuple[int, int] | None:
    """Return the nth nearby delivery month on d: the first unexpired contract, then later ones.

    A contract that expired before the calendar starts is expired. One whose expiry lies beyond
    the data is unexpired when the date its rule counts back from (the 1st, or the 25th of the
    month before) is more than ten days after d, and unknown otherwise.
    """
    y, m = d.year, d.month
    while True:
        e = rule_expiry(market, y, m, ng_days)
        if e is None and D(y, m, 1) > DAYS[-1]:
            counted_from = D(y, m, 1) if market == "NG" else D(*previous_month(y, m), 25)
            if (counted_from - d).days <= 10:
                return None
            break
        if e is not None and e >= d:
            break
        y, m = next_month(y, m)
    for _ in range(nth - 1):
        y, m = next_month(y, m)
    return (y, m)


def previous_month(y: int, m: int) -> tuple[int, int]:
    """Return the month before (y, m)."""
    return (y - 1, 12) if m == 1 else (y, m - 1)


class AgainstTheRuleText(unittest.TestCase):
    """Every month and trading day agrees with a direct reading of each rule, by scanning."""

    def test_every_expiry(self) -> None:
        """Each delivery month from 1995 to 1998, each market and each gas offset."""
        for calendar in (WTI, NG, HO):
            for y in range(1995, 1999):
                for m in range(1, 13):
                    for ng_days in (3, 5, 6):
                        with self.subTest(market=calendar.market, y=y, m=m, ng_days=ng_days):
                            self.assertEqual(
                                calendar.expiry(y, m, ng_days),
                                rule_expiry(calendar.market, y, m, ng_days),
                            )

    def test_every_nearby_contract(self) -> None:
        """The first, second and fourth nearby on every trading day, to the data end."""
        for calendar in (WTI, NG, HO):
            for d in DAYS:
                for nth in (1, 2, 4):
                    with self.subTest(market=calendar.market, d=d, nth=nth):
                        self.assertEqual(
                            calendar.delivery(d, nth), rule_delivery(calendar.market, d, nth, 3)
                        )

    def test_every_month_end_and_stocks_week(self) -> None:
        """Month ends of the calendar, and the latest public week on every day, by scanning."""
        ends = [a for a, b in itertools.pairwise(DAYS) if b.month != a.month]
        self.assertEqual(WTI.complete_month_ends(), ends)
        for market in ("WTI", "NG", "HO"):
            lag = 7 if market == "NG" else 6
            for t in DAYS:
                holiday = [
                    F
                    for F in WEEKS
                    if any(
                        (F + dt.timedelta(days=k)).strftime("%m-%d") in ("12-25", "01-01")
                        for k in range(1, 8)
                    )
                ]
                public = [
                    F for F in WEEKS if F + dt.timedelta(days=11 if F in holiday else lag) <= t
                ]
                with self.subTest(market=market, t=t):
                    self.assertEqual(
                        available_week(market, WEEKS, t), max(public) if public else None
                    )


if __name__ == "__main__":
    unittest.main()
