"""source verification (2026-10-17): an own, synthetic illustration behind meth:bitemporal-reference-tables.

A vendor first records a 2-for-1 split of stock XYZ effective 2026-03-02 (actual time) on 2026-03-03 (record
time), then corrects it on 2026-03-20 to a 3-for-2 split. Following Fowler's actual/record distinction, every row
carries an actual-time range and a record-time range, and record history is append-only. Checked:
1. the factor "as known on 2026-03-10" for 2026-03-05 is the first (wrong) one, as a backtest dated 2026-03-10 saw;
2. the factor "as known now" is the corrected one;
3. before the record date of the first entry, no split is known even for actual dates after the split;
4. the correction appends rows and closes record ranges; no earlier row is overwritten.
Synthetic data only. Run: uv run --frozen --no-editable python -m trading_notes.numerical.bitemporal (standard library).
"""

import datetime as dt
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Final

from trading_notes.numerical.report import CheckReport

INF: Final = dt.date(9999, 12, 31)  # end of an open range: still current
NO_SPLIT: Final = 1.0  # the factor where no row matches


@dataclass(frozen=True)
class SplitRow:
    """One bitemporal row: a split factor over an actual-time and a record-time range.

    Both ranges are dates, inclusive at both ends; `INF` ends an open range.

    Attributes:
        record_from: First date on which the vendor's records held this row.
        record_to: Last date on which they held it.
        actual_from: First date on which the factor applies in the world.
        actual_to: Last date on which it applies.
        split_factor: The cumulative split factor.
    """

    record_from: dt.date
    record_to: dt.date
    actual_from: dt.date
    actual_to: dt.date
    split_factor: float


class SplitHistory:
    """The append-only bitemporal split history of one stock.

    Each instance owns its rows; `record` adds to them and no row is ever changed in place.
    """

    def __init__(self, rows: Iterable[SplitRow] = ()) -> None:
        """Start a history from initial rows, in lookup order (copied, not shared)."""
        self._rows: list[SplitRow] = list(rows)

    @property
    def rows(self) -> tuple[SplitRow, ...]:
        """Return every row, closed and open, in lookup order."""
        return tuple(self._rows)

    def record(self, record_date: dt.date, actual_from: dt.date, factor: float) -> None:
        """Record on record_date that factor applies from actual_from onward.

        Append-only: each open row whose actual range reaches actual_from is replaced by a copy
        whose record range closes the day before record_date, followed, if its actual range
        starts before actual_from, by an open copy that ends the day before actual_from. Closed
        rows and open rows ending before actual_from are kept as they are; the new open row
        is appended last. Mutates this history only.

        Args:
            record_date: Date the vendor recorded the fact; the new rows' record ranges start here.
            actual_from: First actual date the factor applies to; it applies to `INF`.
            factor: The split factor recorded.
        """
        new: list[SplitRow] = []
        for r in self._rows:
            if r.record_to == INF and r.actual_to >= actual_from:
                closed = record_date - dt.timedelta(days=1)  # closed copy
                new.append(
                    SplitRow(r.record_from, closed, r.actual_from, r.actual_to, r.split_factor)
                )
                if r.actual_from < actual_from:
                    new.append(
                        SplitRow(
                            record_date,
                            INF,
                            r.actual_from,
                            actual_from - dt.timedelta(days=1),
                            r.split_factor,
                        )
                    )
            else:
                new.append(r)
        new.append(SplitRow(record_date, INF, actual_from, INF, factor))
        self._rows = new

    def factor_at(self, actual: dt.date, known_on: dt.date) -> float:
        """Return the factor for actual date `actual` as the records stood on `known_on`.

        Args:
            actual: The date in the world whose factor is wanted.
            known_on: The record date: which version of the records to read.

        Returns:
            The factor of the first row whose ranges both contain the dates (inclusive), or
            `NO_SPLIT` (1.0) when none does.
        """
        for r in self._rows:
            if r.record_from <= known_on <= r.record_to and r.actual_from <= actual <= r.actual_to:
                return r.split_factor
        return NO_SPLIT


def check_split_correction(report: CheckReport) -> None:
    """Checks 1-4: record the split, correct it, and query it as known on several dates."""
    history = SplitHistory([SplitRow(dt.date(2000, 1, 1), INF, dt.date(2000, 1, 1), INF, 1.0)])
    history.record(dt.date(2026, 3, 3), dt.date(2026, 3, 2), 2.0)
    snapshot = [r for r in history.rows if r.record_to != INF]
    history.record(dt.date(2026, 3, 20), dt.date(2026, 3, 2), 1.5)
    report.same(
        "as known on 2026-03-10, factor for 2026-03-05",
        history.factor_at(dt.date(2026, 3, 5), dt.date(2026, 3, 10)),
        2.0,
    )
    report.same(
        "as known now, factor for 2026-03-05",
        history.factor_at(dt.date(2026, 3, 5), dt.date(2026, 10, 17)),
        1.5,
    )
    report.same(
        "as known on 2026-03-02, factor for 2026-03-05",
        history.factor_at(dt.date(2026, 3, 5), dt.date(2026, 3, 2)),
        1.0,
    )
    report.same(
        "closed rows survive the correction unchanged",
        all(r in history.rows for r in snapshot),
        True,
    )


def main() -> int:
    """Run the checks with a fresh report and return the exit status (0 or 1).

    A failure prints no summary: the BAD lines are the whole report, as in the original script.
    """
    report = CheckReport()
    check_split_correction(report)
    if report.failures:
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
