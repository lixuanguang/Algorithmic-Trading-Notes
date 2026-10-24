"""Checks of the 13F, 13D and Form 4 filing deadlines on the U.S. business-day calendar."""

import datetime as dt
import sys

from trading_notes.numerical.report import CheckReport
from trading_notes.numerical.us_calendar import (
    add_business_days,
    federal_holidays,
    nth_weekday,
    rolled_forward,
)


def check_holidays(report: CheckReport) -> None:
    """Check the computed holidays that the deadlines below cross."""
    report.same("Thanksgiving 2026", nth_weekday(2026, 11, 3, 4), dt.date(2026, 11, 26))
    report.same(
        "Veterans Day 2026 is a Wednesday holiday",
        dt.date(2026, 11, 11) in federal_holidays(2026),
        True,
    )


def check_deadlines(report: CheckReport) -> None:
    """Check the 13F, Form 4 and 13D due dates of the Q3 2026 and November 2026 examples."""
    raw = dt.date(2026, 9, 30) + dt.timedelta(45)
    report.same("13F raw due date for Q3 2026", raw, dt.date(2026, 11, 14))
    report.same("13F raw due date is a Saturday", raw.weekday(), 5)
    report.same("13F due after roll (Rule 0-3)", rolled_forward(raw), dt.date(2026, 11, 16))
    report.same(
        "Form 4 for a trade on Fri 20 Nov 2026",
        add_business_days(dt.date(2026, 11, 20), 2),
        dt.date(2026, 11, 24),
    )
    report.same(
        "13D for an acquisition on Mon 23 Nov 2026",
        add_business_days(dt.date(2026, 11, 23), 5),
        dt.date(2026, 12, 1),
    )
    report.same(
        "Form 4 latest under deemed execution (3 + 2 business days) from Fri 20 Nov",
        add_business_days(dt.date(2026, 11, 20), 5),
        dt.date(2026, 11, 30),
    )


def main() -> int:
    """Run every check with a fresh report, print the summary and return the exit status (0 or 1).

    Deadline arithmetic of data:holdings-insider-filing-lags. 13F: 45 calendar days after
    quarter end (17 CFR 240.13f-1(a)(1)); 13D: five business days after the acquisition
    (240.13d-1(a)); Form 4: before the end of the second business day after execution
    (15 U.S.C. 78p(a)(2)(C)); a due date on a Saturday, Sunday or holiday moves to the next
    business day (240.0-3(a)). Business days exclude weekends and the federal holidays of
    5 U.S.C. 6103 with the observed-day rule.
    """
    report = CheckReport()
    check_holidays(report)
    check_deadlines(report)
    if report.failures:
        print("\nFAILED:", report.failures)
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
