"""The Federal Reserve Board's FEDS curve tables and the New York Fed's ACM workbook."""

import csv
import datetime as dt
import math
from pathlib import Path
from typing import Self

from trading_notes.numerical.newey_west import Month
from trading_notes.records import Record
from trading_notes.research.spreadsheets import xls_rows


class FedsTable(Record):
    """A FEDS CSV table: the header row starting with "Date" and the rows after it.

    Attributes:
        head: The column names.
        body: The data rows, as text.
    """

    head: list[str]
    body: list[list[str]]

    @classmethod
    def read(cls, path: Path) -> Self:
        """Read the table below the file's notes."""
        with path.open() as f:
            rows = list(csv.reader(f))
        i = next(k for k, r in enumerate(rows) if r and r[0] == "Date")
        return cls(head=rows[i], body=rows[i + 1 :])

    def column(self, name: str) -> int:
        """Return a column's index."""
        return self.head.index(name)


def number(x: str) -> float | None:
    """Return a table cell as a number, None for text or NaN."""
    try:
        v = float(x)
    except ValueError:
        return None
    return None if math.isnan(v) else v


class AcmEstimates(Record):
    """The 'ACM Monthly' sheet: end-of-month ACM yields and term premia, in percent.

    Attributes:
        head: The column names; the first is the date.
        rows: The rows, the date as DD-Mon-YYYY text.
    """

    head: list[str]
    rows: list[list[str | float]]

    @classmethod
    def read(cls, path: Path) -> Self:
        """Read the monthly sheet of ACMTermPremium.xls."""
        rows = xls_rows(path, "ACM Monthly")
        return cls(head=[str(h) for h in rows[0]], rows=rows[1:])

    def dates(self) -> list[str]:
        """Return each row's date text."""
        return [str(r[0]) for r in self.rows]

    def values(self, name: str) -> list[float]:
        """Return a column's values in row order.

        Raises:
            ValueError: If a cell is not a number.
        """
        k = self.head.index(name)
        out = []
        for r in self.rows:
            v = r[k]
            if isinstance(v, str):
                raise ValueError(f"{name}: not a number: {v!r}")
            out.append(v)
        return out

    def by_month(self, name: str) -> dict[Month, float]:
        """Return a column keyed by calendar month."""
        out = {}
        for d, v in zip(self.dates(), self.values(name), strict=True):
            x = dt.datetime.strptime(d, "%d-%b-%Y")
            out[(x.year, x.month)] = v
        return out
