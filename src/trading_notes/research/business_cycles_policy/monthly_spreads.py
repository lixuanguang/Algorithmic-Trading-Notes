"""Monthly averages of daily Treasury spreads, with the month-coverage checks both sources share."""

import csv
import datetime as dt
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import ClassVar, Final, Self

from trading_notes.records import Record
from trading_notes.research.workflow import WorkflowArguments

# The daily data were retrieved on 2026-10-16: a month containing both the last observation
# and the retrieval date is incomplete.
RETRIEVED: Final = dt.date(2026, 10, 16)

type Row = dict[str, str]


class DailyRows(Record):
    """A daily extract's rows, as text keyed by column name.

    Attributes:
        rows: The rows in file order.
    """

    rows: list[Row]

    @classmethod
    def read(cls, path: Path) -> Self:
        """Read a daily extract and check that its dates are unique and increasing.

        Raises:
            ValueError: If a date repeats or the dates are out of order.
        """
        with path.open() as f:
            rows = list(csv.DictReader(f))
        dates = [r["date"] for r in rows]
        if len(dates) != len(set(dates)):
            raise ValueError("duplicate dates")
        if dates != sorted(dates):
            raise ValueError("dates not increasing")
        return cls(rows=rows)

    @property
    def first_date(self) -> str:
        """Return the first date."""
        return self.rows[0]["date"]

    @property
    def last_date(self) -> str:
        """Return the last date."""
        return self.rows[-1]["date"]

    def months(self, usable: Callable[[Row], bool] | None = None) -> dict[str, list[Row]]:
        """Return the usable rows (all when `usable` is None) by YYYY-MM month, in order.

        Raises:
            ValueError: If a month between the first and the last has no usable row.
        """
        by: dict[str, list[Row]] = {}
        for r in self.rows:
            if usable is None or usable(r):
                by.setdefault(r["date"][:7], []).append(r)
        found = sorted(by)
        y, m = map(int, found[0].split("-"))
        expected = []
        while f"{y:04d}-{m:02d}" <= found[-1]:
            expected.append(f"{y:04d}-{m:02d}")
            y, m = (y + 1, 1) if m == 12 else (y, m + 1)
        if found != expected:
            raise ValueError("gap in months")
        return {mo: by[mo] for mo in found}

    def complete(self, month: str) -> bool:
        """Return whether a YYYY-MM month is complete: not both the last observed and retrieved."""
        last = dt.date.fromisoformat(self.last_date).strftime("%Y-%m")
        return not (month == last and month == RETRIEVED.strftime("%Y-%m"))

    def write_monthly(
        self, out: Path, header: Sequence[str], values: Mapping[str, Sequence[str | int]]
    ) -> tuple[int, str, str]:
        """Write each month's values and whether it is complete; return the months and dates.

        Args:
            out: The monthly CSV.
            header: Its columns, the month first and the completeness flag last.
            values: The other columns' values, by month in order.
        """
        with out.open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(header)
            for mo, v in values.items():
                w.writerow([mo, *v, "yes" if self.complete(mo) else "no"])
        return len(values), self.first_date, self.last_date


class SpreadArguments(WorkflowArguments):
    """A monthly spread's arguments.

    Attributes:
        extract: The raw source to rebuild the daily extract from, or None to use the committed
            one.
    """

    folder: ClassVar[str] = "multi-asset-systematic-macro"
    extract: Path | None = None

    def daily(self, name: str, write: Callable[[Path, Path], int]) -> Path:
        """Return the daily extract to read, after rebuilding it from --extract if given.

        Args:
            name: The extract's file name.
            write: Writes the extract from the raw source to a path; returns its rows.
        """
        if self.extract is None:
            return self.artefacts / name
        daily = self.output_folder / name
        print("daily rows:", write(self.extract, daily))
        return daily
