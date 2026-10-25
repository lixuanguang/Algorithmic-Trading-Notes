"""The status of the post-2005 inversion outcomes: whose windows ended, and with what dating lag."""

import csv
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import ClassVar, Final, Self

from trading_notes.data_folders import DataFolder
from trading_notes.numerical.newey_west import Month, add, mdiff
from trading_notes.records import Record
from trading_notes.research.business_cycles_policy.h15_spread import MONTHLY
from trading_notes.research.workflow import WorkflowArguments

ASOF_LAST_COMPLETE: Final = (2026, 9)
FIRST_MONTH: Final = (2022, 11)
# NBER peak months and the months their dates were announced (announcements page, 2026-10-17).
ANNOUNCED: Final = {
    (1980, 1): (1980, 6),
    (1981, 7): (1982, 1),
    (1990, 7): (1991, 4),
    (2001, 3): (2001, 11),
    (2007, 12): (2008, 12),
    (2020, 2): (2020, 6),
}
EXPECTED_NEGATIVE: Final = 27


def months_text(xs: Sequence[Month]) -> str:
    """Return months as comma-separated YYYY-MM, or "none"."""
    return ", ".join(f"{a}-{b:02d}" for a, b in xs) if xs else "none"


class Inversions(Record):
    """The negative complete months of the bond-equivalent 10y-3m spread from FIRST_MONTH.

    Attributes:
        months: The months, in order.
        max_lag: The longest NBER peak announcement lag, in months.
    """

    months: list[Month]
    max_lag: int

    @classmethod
    def read(cls, monthly: Path, max_lag: int) -> Self:
        """Read the negative complete months of h15-spread-monthly.csv."""
        neg: list[Month] = []
        with monthly.open() as f:
            for r in csv.DictReader(f):
                y, m = map(int, r["month"].split("-"))
                if (
                    r["complete"] == "yes"
                    and float(r["spread_10y_3m_be"]) < 0
                    and (y, m) >= FIRST_MONTH
                ):
                    neg.append((y, m))
        return cls(months=neg, max_lag=max_lag)

    def dated_by_now(self, t: Month) -> bool:
        """Return whether a peak at t + 11 would have been announced within the longest lag."""
        return mdiff(ASOF_LAST_COMPLETE, t) >= 11 + self.max_lag

    def windows(self) -> tuple[list[Month], list[Month], list[Month]]:
        """Return the months passing (1) and (2), passing (1) only, and failing (1)."""
        beyond: list[Month] = []
        within: list[Month] = []
        still_open: list[Month] = []
        for t in self.months:
            done = mdiff(ASOF_LAST_COMPLETE, t) >= 12
            (beyond if done and self.dated_by_now(t) else within if done else still_open).append(t)
        return beyond, within, still_open

    def episodes(self) -> list[list[Month]]:
        """Return the runs of consecutive negative months."""
        runs: list[list[Month]] = []
        for t in self.months:
            if runs and t == add(runs[-1][-1], 1):
                runs[-1].append(t)
            else:
                runs.append([t])
        return runs

    def report(self) -> bool:
        """Print each month's and episode's window status; return whether all 27 are complete."""
        neg = self.months
        print(
            f"negative complete months from 2022-11: {len(neg)} ({neg[0][0]}-{neg[0][1]:02d} .."
            f" {neg[-1][0]}-{neg[-1][1]:02d})"
        )
        beyond, within, still_open = self.windows()
        print(
            f"(1) window complete and (2) beyond the longest past lag: {len(beyond)} months"
            f" ({months_text(beyond[:1])} .. {months_text(beyond[-1:])})"
        )
        print(
            f"(1) window complete, (2) still within the longest past lag: {len(within)} months:"
            f" {months_text(within)}"
        )
        print(f"window not yet complete: {len(still_open)} months: {months_text(still_open)}")
        for e in self.episodes():
            last = e[-1]
            status = "beyond" if self.dated_by_now(last) else "within"
            end = add(last, 12)
            print(
                f"episode {e[0][0]}-{e[0][1]:02d} .. {last[0]}-{last[1]:02d} ({len(e)} months):"
                f" window to {end[0]}-{end[1]:02d} complete; dating {status} the longest past lag"
            )
        return len(neg) == EXPECTED_NEGATIVE and not still_open


class Arguments(WorkflowArguments):
    """The inversion-horizons check's arguments.

    Attributes:
        spreads: A generated h15-spread-monthly.csv, or a run folder holding one, to read
            instead of the retained file.
    """

    folder: ClassVar[DataFolder] = DataFolder(subsection="business_cycles_policy")
    spreads: Path | None = None


def main(argv: Sequence[str] | None = None) -> int:
    """Print each negative month's window status and exit 1 unless all 27 windows are complete.

    For each negative complete month t of the bond-equivalent 10y-3m spread from November 2022
    (no NBER peak is dated after February 2020), the month rule asks whether a recession began
    in t + 1..t + 12. Two questions: (1) has month t + 12 ended by the last complete month,
    September 2026; (2) would a peak at t + 11 have been announced by then if NBER's lag were
    no longer than the longest in its list (12 months)? A month passing both is a miss beyond
    the longest past lag; one passing (1) only remains open to dating within past lags.

    Returns:
        0 when there are 27 negative months, all with complete windows; otherwise 1.
    """
    parser = Arguments.parser(__doc__ or "")
    parser.add_argument(
        "--spreads", type=Path, default=None, help="a generated monthly spread file or run folder"
    )
    args = Arguments.parse(parser, argv)
    spreads = args.upstream(args.spreads, args.folder.results / MONTHLY)
    lags = {p: mdiff(a, p) for p, a in ANNOUNCED.items()}
    print(
        "NBER peak announcement lags (months): "
        + ", ".join(f"{p[0]}-{p[1]:02d}: {lag}" for p, lag in lags.items())
        + f"; max {max(lags.values())}"
    )
    if not Inversions.read(spreads, max(lags.values())).report():
        print("FAILED: expected 27 negative months, all windows complete")
        return 1
    print("checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
