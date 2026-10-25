"""Inputs and statistics of the regime-row tests: rates, oil, real-time vintages, Welch and NW t."""

import argparse
import csv
import math
from collections.abc import Iterator, Sequence
from pathlib import Path
from typing import ClassVar, Final, Self

import numpy as np
from numpy.typing import NDArray

from trading_notes.data_folders import DataFolder
from trading_notes.numerical.newey_west import Month, add
from trading_notes.records import Record
from trading_notes.research.business_cycles_policy.h15_spread import DAILY
from trading_notes.research.business_cycles_policy.monthly_spreads import SpreadArguments
from trading_notes.research.fred import monthly_means
from trading_notes.research.regressions import NeweyWestOls
from trading_notes.research.spreadsheets import XlsxCell, eia_series, xlsx_rows
from trading_notes.research.workflow import WorkflowArguments

type Floats = NDArray[np.float64]

# Below the reading-materials root: FRED's GS10, EIA's Cushing WTI spot and the vintage files.
GS10: Final = Path("source-verification") / "empirical" / "fred" / "GS10.csv"
WTI_SPOT: Final = Path("empirical-extensions") / "empirical" / "EIA_RWTCm.xls"
QUARTERLY_CPI: Final = Path("derivatives-validation") / "empirical" / "cpiQvMd.xlsx"
MONTHLY_CPI: Final = Path("empirical-extensions") / "empirical" / "pcpiMvMd.xlsx"
# Below the repository root: the retained daily H.15 extract, owned by the spread workflow.
H15_DAILY: Final = SpreadArguments.folder.inputs / DAILY
MIDDLE_MONTHS: Final = (2, 5, 8, 11)


class MonthlyResponses(Record):
    """The monthly series the inflation and deflation rows' responses are built from.

    Attributes:
        gs10: FRED GS10, the 10-year Treasury yield, monthly average.
        tb3: The 3-month bill (H.15, discount basis), monthly average of business days.
        oil: EIA's Cushing WTI spot, monthly average.
    """

    gs10: dict[Month, float]
    tb3: dict[Month, float]
    oil: dict[Month, float]

    @classmethod
    def read(cls, materials: Path, h15_daily: Path) -> Self:
        """Read the series from the reading-materials folder and a daily H.15 extract."""
        tb3: dict[Month, list[float]] = {}
        with h15_daily.open() as f:
            for row in csv.DictReader(f):
                if row["tb3m_discount"] not in ("", "ND"):
                    y, m, _ = map(int, row["date"].split("-"))
                    tb3.setdefault((y, m), []).append(float(row["tb3m_discount"]))
        oil = {(d.year, d.month): v for d, v in eia_series(materials / WTI_SPOT).items()}
        return cls(
            gs10=monthly_means(materials / GS10),
            tb3={k: sum(v) / len(v) for k, v in tb3.items()},
            oil=oil,
        )

    def complete(self, months: Sequence[Month]) -> bool:
        """Return whether every series has every one of the months."""
        return all(k in src for k in months for src in (self.gs10, self.tb3, self.oil))

    def dy10(self, m: Month, m3: Month) -> float:
        """Return the change in GS10 from m to m3."""
        return self.gs10[m3] - self.gs10[m]

    def dslope(self, m: Month, m3: Month) -> float:
        """Return the change in GS10 less TB3 from m to m3."""
        return (self.gs10[m3] - self.tb3[m3]) - (self.gs10[m] - self.tb3[m])

    def oil_change(self, m: Month, m3: Month) -> float:
        """Return 100 ln(RWTC(m3) / RWTC(m))."""
        return 100 * math.log(self.oil[m3] / self.oil[m])


class RowArguments(WorkflowArguments):
    """The arguments of the inflation and deflation rows.

    Attributes:
        materials: The reading-materials root that holds the vintage, GS10 and oil files.
        h15_daily: A generated h15-daily-3m-10y.csv, or a run folder holding one, to read
            instead of the retained extract.
    """

    folder: ClassVar[DataFolder] = DataFolder(subsection="macro_regimes_data")
    materials: Path
    h15_daily: Path | None = None

    @classmethod
    def parser(cls, description: str) -> argparse.ArgumentParser:
        """Return a parser with the reading-materials root and the --h15-daily option."""
        parser = super().parser(description)
        parser.add_argument("materials", type=Path, help="the reading-materials root")
        parser.add_argument(
            "--h15-daily", type=Path, default=None, help="a generated daily extract or run folder"
        )
        return parser

    def responses(self) -> MonthlyResponses:
        """Return the monthly responses, reading the requested or the retained H.15 extract."""
        return MonthlyResponses.read(self.materials, self.upstream(self.h15_daily, H15_DAILY))


class RealTimeVintage(Record):
    """One vintage of a Philadelphia Fed Real-Time Data Set series (CPI or unemployment).

    Attributes:
        name: The vintage's column name, such as CPI26Q3, PCPI26M08 or RUC26Q3.
        month: The vintage month: the middle month of its quarter.
        levels: The series by observation month, as reported in the vintage.
    """

    name: str
    month: Month
    levels: dict[Month, float]

    @classmethod
    def read_all(cls, path: Path, sheet: str, prefix: str, quarterly: bool) -> Iterator[Self]:
        """Yield each middle-month vintage of a workbook, in column order.

        Args:
            path: The workbook.
            sheet: Its data sheet.
            prefix: The letters before the vintage's two-digit year.
            quarterly: True for quarterly vintages <prefix>yyQq, dated in the quarter's middle
                month; False for monthly vintages <prefix>yyMmm, of which only the middle
                months are kept.
        """
        rows = xlsx_rows(path, sheet)
        head, body = rows[0], rows[1:]
        months = [month_label(r[0]) for r in body]
        for j, name in enumerate(head[1:], start=1):
            if not isinstance(name, str):
                raise ValueError(f"{path.name}: column {j} has no vintage name")
            yy = int(name[len(prefix) : len(prefix) + 2])
            year = 1900 + yy if yy >= 60 else 2000 + yy
            if quarterly:
                mm = 3 * int(name[-1]) - 1
            else:
                mm = int(name[len(prefix) + 3 :])
                if mm not in MIDDLE_MONTHS:
                    continue
            p = {
                m: float(v)
                for m, row in zip(months, body, strict=True)
                if isinstance(v := row[j], (int, float))
            }
            if p:
                yield cls(name=name, month=(year, mm), levels=p)

    def inflation(self, t: Month) -> float:
        """Return pi(t) = 100 ln(P_t / P_{t-12}).

        Raises:
            KeyError: If the vintage lacks either month.
        """
        return 100 * math.log(self.levels[t] / self.levels[add(t, -12)])

    def classify(self) -> tuple[Month, float, float]:
        """Return the last reported month L, pi(L) and the acceleration pi(L) - pi(L - 12).

        Raises:
            KeyError: If a month inside the 25-month window is missing.
        """
        L = max(self.levels)
        return L, self.inflation(L), self.inflation(L) - self.inflation(add(L, -12))


def month_label(cell: XlsxCell) -> Month:
    """Return the month of a "YYYY:MM" label."""
    if not isinstance(cell, str):
        raise ValueError(f"not a YYYY:MM month label: {cell!r}")
    y, m = map(int, cell.split(":"))
    return (y, m)


def welch_t(a: Floats, b: Floats) -> float:
    """Return Welch's t statistic for the difference in means of a and b."""
    return float((a.mean() - b.mean()) / math.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b)))


def indicator_slope(y: Floats, d: Floats, lags: int = 4) -> tuple[float, float]:
    """Return the slope of y on a constant and the 0/1 indicator d, and its Newey-West t."""
    fit = NeweyWestOls.fit(y, d, lags)
    return float(fit.coefficients[1]), float(fit.t_stats[1])


def episodes(flags: Sequence[bool | int]) -> int:
    """Return the number of runs of consecutive flagged observations."""
    return sum(1 for i, f in enumerate(flags) if f and (i == 0 or not flags[i - 1]))
