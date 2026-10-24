"""Estrella and Trubin's spread from the Federal Reserve's H.15 release, as monthly averages."""

import csv
import sys
import xml.etree.ElementTree as ET
from collections.abc import Sequence
from pathlib import Path
from typing import Final, Self

from trading_notes.records import Record
from trading_notes.research.business_cycles_policy.monthly_spreads import (
    DailyRows,
    SpreadArguments,
)

DAILY: Final = "h15-daily-3m-10y.csv"
MONTHLY: Final = "h15-spread-monthly.csv"
SERIES: Final = {"RIFSGFSM03_N.B": "tb3m_discount", "RIFLGFCY10_N.B": "cmt_10y"}
FIRST_DATE: Final = "1962-01-01"  # the 10-year series begins in 1962


class H15Release(Record):
    """The 3-month bill (secondary market, discount basis) and 10-year CMT observations.

    Attributes:
        series: Each column's observations with status "A", value text by ISO date.
    """

    series: dict[str, dict[str, str]]

    @classmethod
    def parse(cls, xml_path: Path) -> Self:
        """Read the two series from the H.15 SDMX XML."""
        data: dict[str, dict[str, str]] = {v: {} for v in SERIES.values()}
        cur: str | None = None
        for ev, el in ET.iterparse(xml_path, events=("start", "end")):
            tag = el.tag.split("}")[-1]
            if ev == "start" and tag == "Series":
                cur = SERIES.get(el.get("SERIES_NAME") or "")
            elif ev == "end" and tag == "Obs":
                period, value = el.get("TIME_PERIOD"), el.get("OBS_VALUE")
                if cur and el.get("OBS_STATUS") == "A" and period is not None and value is not None:
                    data[cur][period] = value
                el.clear()
            elif ev == "end" and tag == "Series":
                cur = None
        return cls(series=data)

    def write_daily(self, daily: Path) -> int:
        """Write the dates with both series, from 1962, as the daily extract; return its rows."""
        bill, cmt = self.series["tb3m_discount"], self.series["cmt_10y"]
        dates = sorted(d for d in set(bill) & set(cmt) if d >= FIRST_DATE)
        with daily.open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["date", "tb3m_discount", "cmt_10y"])
            for d in dates:
                w.writerow([d, bill[d], cmt[d]])
        return len(dates)


def bond_equivalent(d: float) -> float:
    """Return the bond-equivalent yield of a 3-month bill at discount yield d, in points."""
    return 100 * (365 * d / 100) / (360 - 91 * d / 100)


def monthly(daily: Path, out: Path) -> tuple[int, str, str]:
    """Write the monthly averages of the daily spread; return the months and the date range.

    The daily spread is the 10-year CMT less the bill's bond-equivalent yield.
    """
    rows = DailyRows.read(daily)
    values: dict[str, list[str | int]] = {}
    for mo, rs in rows.months().items():
        v = [float(r["cmt_10y"]) - bond_equivalent(float(r["tb3m_discount"])) for r in rs]
        values[mo] = [f"{sum(v) / len(v):.4f}", len(v)]
    return rows.write_monthly(out, ["month", "spread_10y_3m_be", "days", "complete"], values)


def main(argv: Sequence[str] | None = None) -> int:
    """Rebuild h15-spread-monthly.csv, after the daily extract when an XML file is given.

    Source: Board of Governors, H.15 Selected Interest Rates, the full data package (SDMX
    XML) retrieved 2026-10-16; series RIFSGFSM03_N.B (3-month bill) and RIFLGFCY10_N.B
    (10-year CMT). Transformation as in Estrella and Trubin (2006), n. 4: bond-equivalent =
    100 (365 d/100) / (360 - 91 d/100), d the discount yield in points; daily spread =
    10-year CMT less the bond-equivalent bill; monthly average of business days.

    Returns:
        0.
    """
    parser = SpreadArguments.parser(__doc__ or "")
    parser.add_argument("--extract", type=Path, default=None, help="the H.15 SDMX XML file")
    args = SpreadArguments.parse(parser, argv)
    daily = args.daily(DAILY, lambda xml, path: H15Release.parse(xml).write_daily(path))
    print("months, first day, last day:", monthly(daily, args.output_folder / MONTHLY))
    return 0


if __name__ == "__main__":
    sys.exit(main())
