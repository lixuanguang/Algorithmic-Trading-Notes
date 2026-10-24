"""The backwardation test's contract identity, holding periods, report timing and outputs."""

import csv
import datetime as dt
import hashlib
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Final

from trading_notes.numerical.commodity_curves.nymex_contracts import (
    ContractCalendar,
    available_week,
)
from trading_notes.numerical.report import CheckReport
from trading_notes.numerical.repository import repository_root

# The test's outputs, below the repository root, and its first run kept beside them.
FOLDER: Final = Path("notes/artefacts/commodity-storage-curves")
D = dt.date


def synthetic_calendar() -> list[dt.date]:
    """Return the weekdays from 2 January 2024 for 130 days, less three NYMEX holidays.

    Martin Luther King Day, Presidents Day and Good Friday (29 March) are closed.
    """
    cal = [D(2024, 1, 2) + dt.timedelta(days=k) for k in range(130)]
    return [
        x
        for x in cal
        if x.weekday() < 5 and x not in {D(2024, 1, 15), D(2024, 2, 19), D(2024, 3, 29)}
    ]


def check_contract_identity(report: CheckReport) -> list[dt.date]:
    """1. NYMEX expiries and nearby contracts on the synthetic 2024 calendar; return it."""
    print("== 1. contract identity on a synthetic 2024 calendar")
    cal = synthetic_calendar()
    wti = ContractCalendar(market="WTI", days=tuple(cal))
    ng = ContractCalendar(market="NG", days=tuple(cal))
    report.same("CLJ24 last trading day", wti.expiry(2024, 4), D(2024, 3, 20))
    report.same("CLK24 last trading day", wti.expiry(2024, 5), D(2024, 4, 22))
    report.same("NGJ24 last trading day", ng.expiry(2024, 4), D(2024, 3, 26))
    report.same("WTI C2 on 28 March 2024", wti.delivery(D(2024, 3, 28), 2), (2024, 6))
    report.same("WTI C1 on 5 April 2024", wti.delivery(D(2024, 4, 5), 1), (2024, 5))
    report.same(
        "v1 pairing (28 Mar C2, 5 Apr C1) is not the same contract",
        wti.same_contract(D(2024, 3, 28), 2, D(2024, 4, 5), 1),
        False,
    )
    report.same(
        "29 Feb C2 is 28 Mar C1 (WTI)",
        wti.same_contract(D(2024, 2, 29), 2, D(2024, 3, 28), 1),
        True,
    )
    return cal


def check_holding_periods(report: CheckReport, cal: list[dt.date]) -> None:
    """2. A calendar ending on 5 April has no complete April, so 28 March has no next month-end."""
    print("== 2. complete holding periods")
    short = ContractCalendar(market="WTI", days=tuple(x for x in cal if x <= D(2024, 4, 5)))
    report.same(
        "month-ends of a calendar ending 5 April",
        short.complete_month_ends()[-2:],
        [D(2024, 2, 29), D(2024, 3, 28)],
    )


def check_report_availability(report: CheckReport) -> None:
    """3. The weekly stocks report usable at each settlement, holiday weeks included."""
    print("== 3. report availability")
    F = D(2024, 3, 8)  # a Friday week-ending date
    weeks = [F - dt.timedelta(days=7 * k) for k in range(3, -1, -1)]
    report.same(
        "gas, Wednesday F+5",
        available_week("NG", weeks, F + dt.timedelta(days=5)),
        F - dt.timedelta(days=7),
    )
    report.same(
        "gas, Thursday F+6",
        available_week("NG", weeks, F + dt.timedelta(days=6)),
        F - dt.timedelta(days=7),
    )
    report.same("gas, Friday F+7", available_week("NG", weeks, F + dt.timedelta(days=7)), F)
    report.same("crude, Thursday F+6", available_week("WTI", weeks, F + dt.timedelta(days=6)), F)
    X = D(2025, 12, 19)
    wx = [X - dt.timedelta(days=7 * k) for k in range(3, -1, -1)]
    report.same(
        "crude, Christmas week, Wednesday 31 Dec 2025 (F+12)",
        available_week("WTI", wx, D(2025, 12, 31)),
        X,
    )
    report.same(
        "crude, Christmas week, Monday 29 Dec 2025 (F+10)",
        available_week("WTI", wx, D(2025, 12, 29)),
        X - dt.timedelta(days=7),
    )


def check_outputs(report: CheckReport, root: Path) -> None:
    """4-6. The rerun's panel and results, and the first run's panel preserved."""
    print("== 4-6. rebuilt outputs")
    with (root / FOLDER / "backwardation_monthly.csv").open() as fh:
        rows = list(csv.DictReader(fh))
    ng_early = [r for r in rows if r["market"] == "NG" and r["month_end"] < "2015-01-01"]
    report.same("gas price-only months before 2015 present", len(ng_early) > 200, True)
    report.same("...with no inventory deviation", all(r["inv_dev"] == "" for r in ng_early), True)
    report.same(
        "no month-end pair reaches into April 2024",
        max(r["next_month_end"] for r in rows) < "2024-04-01",
        True,
    )
    res = (root / FOLDER / "backwardation_results.txt").read_text()
    ng_part = res.split("== NG")[1]
    report.same(
        "gas out-of-sample test reported",
        "P OOS (price-only, from month 121): R^2" in ng_part,
        True,
    )
    report.same('no "dropped" wording', "dropped" in res, False)
    report.same('"retained" wording', "retained in every estimate" in res, True)
    report.same(
        "executable return differs from settlement return somewhere",
        any(r["r_exec_next_day"] != r["r_next_settle"] for r in rows if r["r_exec_next_day"]),
        True,
    )
    v1 = (root / FOLDER / "superseded-first-run" / "backwardation_monthly.csv").read_bytes()
    report.same(
        "v1 panel preserved (SHA-256 prefix)", hashlib.sha256(v1).hexdigest()[:8], "6953ecd1"
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Check the backwardation test's rerun against the findings on its first run.

    Each check targets one finding, on a synthetic trading calendar or on the rebuilt outputs:

    1. Contract identity: NYMEX expiries on a synthetic 2024 calendar (Good Friday, 29 March,
       closed): CL April 2024 (CLJ24) 20 March, CL May (CLK24) 22 April, NG April (NGJ24)
       26 March; 28 March's C2 (June WTI) is not 5 April's C1 (May WTI), the pairing the first
       run used.
    2. Complete holding periods: a calendar ending on 5 April has no complete April, so
       28 March has no next month-end.
    3. Report availability: a gas report for the week ending Friday F is not usable on
       Wednesday F+5 (the first run's five-day rule admitted it) or Thursday F+6, and is on
       Friday F+7; crude is usable on F+6; Christmas weeks wait 11 days.
    4. Samples: the rebuilt panel has gas months before 2015 (price-only) with no inventory
       value, and the results report a gas out-of-sample test.
    5. Wording: the results say months are retained, not "dropped".
    6. Execution: the panel's executable return differs from the settlement-to-settlement
       return, and the first run's outputs are kept unchanged in superseded-first-run/.

    The contract rules are those trading_notes.numerical.commodity_curves.nymex_contracts
    gives backwardation_test.py.

    Args:
        argv: Command-line arguments: `--root DIR`, the repository root that holds the outputs
            (default: the working directory).

    Returns:
        The exit status, 0 or 1.
    """
    root = repository_root(__doc__ or "", argv)
    report = CheckReport()
    cal = check_contract_identity(report)
    check_holding_periods(report, cal)
    check_report_availability(report)
    check_outputs(report, root)
    if report.failures:
        print("\nFAILED:", report.failures)
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
