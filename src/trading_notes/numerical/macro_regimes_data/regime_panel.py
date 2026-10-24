"""The quarterly panel of the recession-regime test: NBER windows and dollar-index vintages."""

import csv
from pathlib import Path
from typing import Self

from trading_notes.records import Record


def add_months(ym: str, k: int) -> str:
    """Return the month k calendar months after ym, both written YYYY-MM."""
    y, m = map(int, ym.split("-"))
    n = y * 12 + m - 1 + k
    return f"{n // 12}-{n % 12 + 1:02d}"


class RegimeQuarter(Record):
    """One quarterly window of the panel, named by the month of its real-time vintage.

    Attributes:
        vintage_month: The vintage month, YYYY-MM.
        nber_any_overlap: Whether any month of the window lies in an NBER recession.
        nber_all_months: Whether every month of the window does.
        usd_goods_only: Whether the goods-only dollar index has a change for the window.
        usd_goods_services: Whether the goods-and-services dollar index has one.
    """

    vintage_month: str
    nber_any_overlap: bool
    nber_all_months: bool
    usd_goods_only: bool
    usd_goods_services: bool


class RegimePanel(Record):
    """The panel's windows in vintage order.

    Attributes:
        quarters: The windows.
    """

    quarters: tuple[RegimeQuarter, ...]

    @classmethod
    def read(cls, path: Path) -> Self:
        """Read regime_quarters.csv; a blank dollar column means no change for that window."""
        with path.open() as fh:
            rows = list(csv.DictReader(fh))
        return cls(
            quarters=tuple(
                RegimeQuarter(
                    vintage_month=r["vintage_month"],
                    nber_any_overlap=r["nber_any_overlap"] == "1",
                    nber_all_months=r["nber_all_months"] == "1",
                    usd_goods_only=bool(r["usd_goods_only"]),
                    usd_goods_services=bool(r["usd_goods_services"]),
                )
                for r in rows
            )
        )

    def all_months_within_any(self) -> bool:
        """Return whether every all-months window is also an any-overlap window."""
        return all(q.nber_any_overlap for q in self.quarters if q.nber_all_months)

    def any_overlap_count(self) -> int:
        """Return the number of windows that overlap a recession."""
        return sum(q.nber_any_overlap for q in self.quarters)

    def all_months_count(self) -> int:
        """Return the number of windows that lie wholly in a recession."""
        return sum(q.nber_all_months for q in self.quarters)
