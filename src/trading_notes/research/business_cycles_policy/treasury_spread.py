"""The 10-year less 3-month and 2-year Treasury par-yield spreads, as monthly averages."""

import csv
import datetime as dt
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Final, Self

from trading_notes.records import Record
from trading_notes.research.business_cycles_policy.monthly_spreads import (
    DailyRows,
    Row,
    SpreadArguments,
)

DAILY: Final = "ust-daily-3m-2y-10y.csv"
MONTHLY: Final = "ust-10y3m-monthly.csv"


class ParYieldFiles(Record):
    """Treasury's daily par yields at 3 months, 2 years and 10 years, from the yearly CSVs.

    Attributes:
        rows: (ISO date, 3-month, 2-year, 10-year) as text, blank where not reported, sorted.
    """

    rows: list[tuple[str, str, str, str]]

    @classmethod
    def read(cls, raw_dir: Path) -> Self:
        """Read every y*.csv file of a folder."""
        rows = []
        for path in sorted(raw_dir.glob("y*.csv")):
            with path.open() as f:
                for r in csv.DictReader(f):
                    d = dt.datetime.strptime(r["Date"], "%m/%d/%Y").date()
                    rows.append(
                        (d.isoformat(), r.get("3 Mo", ""), r.get("2 Yr", ""), r.get("10 Yr", ""))
                    )
        return cls(rows=sorted(rows))

    def write_daily(self, daily: Path) -> int:
        """Write the daily extract; return its rows."""
        with daily.open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["date", "cmt_3m", "cmt_2y", "cmt_10y"])
            w.writerows(self.rows)
        return len(self.rows)


def mean_spread(rows: Sequence[Row], short: str) -> float:
    """Return the mean of the 10-year yield less the `short` column's over the rows."""
    return sum(float(r["cmt_10y"]) - float(r[short]) for r in rows) / len(rows)


def monthly(daily: Path, out: Path) -> tuple[int, str, str]:
    """Write the monthly mean spreads; return the months and the date range.

    A day missing the 3-month or 10-year yield is skipped; the 10y-2y mean uses the days
    with a 2-year yield.
    """
    rows = DailyRows.read(daily)
    values: dict[str, list[str | int]] = {}
    for mo, rs in rows.months(lambda r: bool(r["cmt_3m"] and r["cmt_10y"])).items():
        s2 = mean_spread([r for r in rs if r["cmt_2y"]], "cmt_2y")
        values[mo] = [f"{mean_spread(rs, 'cmt_3m'):.4f}", f"{s2:.4f}", len(rs)]
    header = ["month", "spread_10y_3m_cmt", "spread_10y_2y_cmt", "days", "complete"]
    return rows.write_monthly(out, header, values)


def main(argv: Sequence[str] | None = None) -> int:
    """Rebuild ust-10y3m-monthly.csv, after the daily extract when a raw folder is given.

    Source: U.S. Treasury, Daily Treasury Par Yield Curve Rates, one CSV per year 2006-2026,
    retrieved 2026-10-16. These constant-maturity par yields are a proxy for, not the same
    series as, Estrella and Trubin's bond-equivalent 3-month bill rate (H.15).

    Returns:
        0.
    """
    parser = SpreadArguments.parser(__doc__ or "")
    parser.add_argument("--extract", type=Path, default=None, help="folder of yearly CSVs")
    args = SpreadArguments.parse(parser, argv)
    daily = args.daily(DAILY, lambda raw, path: ParYieldFiles.read(raw).write_daily(path))
    print("months, first day, last day:", monthly(daily, args.output_folder / MONTHLY))
    return 0


if __name__ == "__main__":
    sys.exit(main())
