"""Tests that the packaged NYMEX contract helpers are the backwardation test's own, bit for bit.

trading_notes.numerical.commodity_curves.nymex_contracts holds the contract calendar and report
timing that energy_checks verifies, taken from
notes/artefacts/commodity-storage-curves/backwardation_test.py. That script, and
heating_oil_test.py, which patches its module globals, keep their own copies until they migrate.
These compare the two on expiries, nearby contracts, contract identity, month ends and the
usable stocks week, over a calendar with holidays, year ends and a data end, so that the copies
cannot drift apart unnoticed. The script is loaded without running it; it reads data only in
`main`.

Run: make test (uv run --frozen --no-editable pytest)
"""

import datetime as dt
import runpy
import unittest
from pathlib import Path
from typing import Final

from trading_notes.numerical.commodity_curves.nymex_contracts import (
    ContractCalendar,
    Market,
    available_week,
)

SCRIPT = (
    Path(__file__).resolve().parents[3]
    / "notes"
    / "artefacts"
    / "commodity-storage-curves"
    / "backwardation_test.py"
)
MARKETS: Final[tuple[Market, ...]] = ("WTI", "NG")
# Weekdays from November 1995 to early April 1998, less some exchange holidays (so that the
# 25th or the 1st is sometimes not a trading day).
HOLIDAYS: Final = {
    dt.date(1995, 12, 25),
    dt.date(1996, 1, 1),
    dt.date(1996, 11, 25),
    dt.date(1996, 12, 25),
    dt.date(1997, 1, 1),
    dt.date(1997, 4, 25),
    dt.date(1997, 7, 4),
    dt.date(1997, 12, 25),
    dt.date(1998, 1, 1),
}
DAYS: Final = tuple(
    d
    for d in (dt.date(1995, 11, 1) + dt.timedelta(days=k) for k in range(887))
    if d.weekday() < 5 and d not in HOLIDAYS
)


def legacy(name: str) -> object:
    """Return one helper of the backwardation script, loaded so that main() is not run."""
    namespace: dict[str, object] = runpy.run_path(str(SCRIPT), run_name="backwardation_test")
    return namespace[name]


class ContractMonths(unittest.TestCase):
    """Expiries, nearby delivery months and contract identity match the script's."""

    def test_expiry_every_month(self) -> None:
        """Every delivery month's last trading day, for both markets and each gas rule."""
        expiry = legacy("expiry")
        assert callable(expiry)
        for market in MARKETS:
            calendar = ContractCalendar(market=market, days=DAYS)
            for y in range(1995, 1999):
                for m in range(1, 13):
                    for ng_days in (3, 5, 6):
                        with self.subTest(market=market, y=y, m=m, ng_days=ng_days):
                            self.assertEqual(
                                calendar.expiry(y, m, ng_days),
                                expiry(market, list(DAYS), y, m, ng_days),
                            )

    def test_nearby_contracts_and_identity(self) -> None:
        """Nearby months on every third day up to the data end, and identity across a month."""
        delivery, same_contract = legacy("delivery"), legacy("same_contract")
        assert callable(delivery) and callable(same_contract)
        for market in MARKETS:
            calendar = ContractCalendar(market=market, days=DAYS)
            for i in range(0, len(DAYS), 3):
                d = DAYS[i]
                for nth in (1, 2, 4):
                    with self.subTest(market=market, d=d, nth=nth):
                        self.assertEqual(
                            calendar.delivery(d, nth), delivery(market, list(DAYS), d, nth)
                        )
                later = DAYS[min(i + 21, len(DAYS) - 1)]
                with self.subTest(market=market, d=d, later=later):
                    self.assertEqual(
                        calendar.same_contract(d, 2, later, 1),
                        same_contract(market, list(DAYS), d, 2, later, 1),
                    )

    def test_unknown_front_contract_near_the_data_end(self) -> None:
        """Data ending a week before the anchor date leave the front month unknown, as before."""
        delivery = legacy("delivery")
        assert callable(delivery)
        short = tuple(d for d in DAYS if d <= dt.date(1998, 3, 24))
        unknown = 0
        for market in MARKETS:
            calendar = ContractCalendar(market=market, days=short)
            for d in short[-15:]:
                with self.subTest(market=market, d=d):
                    got = calendar.delivery(d, 1)
                    self.assertEqual(got, delivery(market, list(short), d, 1))
                    unknown += got is None
        self.assertGreater(unknown, 0)

    def test_month_ends_and_trading_days_before(self) -> None:
        """Complete month ends and the k-th trading day before a date."""
        complete_month_ends, bd_before = legacy("complete_month_ends"), legacy("bd_before")
        assert callable(complete_month_ends) and callable(bd_before)
        calendar = ContractCalendar(market="WTI", days=DAYS)
        self.assertEqual(calendar.complete_month_ends(), complete_month_ends(list(DAYS)))
        for x in (None, DAYS[0], DAYS[1], dt.date(1996, 12, 25), DAYS[-1]):
            for k in (1, 3):
                with self.subTest(x=x, k=k):
                    self.assertEqual(
                        calendar.business_day_before(x, k), bd_before(list(DAYS), x, k)
                    )


class StocksWeek(unittest.TestCase):
    """The latest public stocks week matches the script's, holiday lags and overrides included."""

    def test_available_week(self) -> None:
        """Every day from November 1995 to March 1998, both markets, with and without `extra`."""
        script_week = legacy("available_week")
        assert callable(script_week)
        weeks = [dt.date(1995, 11, 3) + dt.timedelta(days=7 * k) for k in range(125)]
        for market in MARKETS:
            for k in range(0, 880):
                t = dt.date(1995, 11, 1) + dt.timedelta(days=k)
                for extra in (None, 4, 9):
                    with self.subTest(market=market, t=t, extra=extra):
                        self.assertEqual(
                            available_week(market, weeks, t, extra),
                            script_week(market, weeks, t, extra),
                        )


if __name__ == "__main__":
    unittest.main()
