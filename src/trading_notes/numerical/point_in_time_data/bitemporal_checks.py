"""Checks of a bitemporal split history queried as known on several record dates."""

import datetime as dt
import sys

from trading_notes.numerical.point_in_time_data.split_history import INF, SplitHistory, SplitRow
from trading_notes.numerical.report import CheckReport


def check_split_correction(report: CheckReport) -> None:
    """Checks 1-4: record the split, correct it, and query it as known on several dates."""
    history = SplitHistory(
        [
            SplitRow(
                record_from=dt.date(2000, 1, 1),
                record_to=INF,
                actual_from=dt.date(2000, 1, 1),
                actual_to=INF,
                split_factor=1.0,
            )
        ]
    )
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

    Synthetic illustration of meth:bitemporal-reference-tables. A vendor first records a
    2-for-1 split of stock XYZ effective 2026-03-02 (actual time) on 2026-03-03 (record time),
    then corrects it on 2026-03-20 to a 3-for-2 split. Checked: the factor as known on
    2026-03-10 for 2026-03-05 is the first (wrong) one, as a backtest dated then saw; as known
    now it is the corrected one; before the first record date no split is known even for
    actual dates after it; the correction appends rows and closes record ranges without
    overwriting any. A failure prints no summary: the BAD lines are the whole report.
    """
    report = CheckReport()
    check_split_correction(report)
    if report.failures:
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
