"""source verification (2026-10-17): deadline arithmetic behind data:holdings-insider-filing-lags.

13F: 45 calendar days after quarter end (17 CFR 240.13f-1(a)(1)); 13D: five business days after the acquisition
(240.13d-1(a)); Form 4: before the end of the second business day after execution (15 U.S.C. 78p(a)(2)(C));
a due date on a Saturday, Sunday or holiday moves to the next business day (240.0-3(a)).
Business days exclude weekends and U.S. federal holidays (5 U.S.C. 6103, observed-day rule), computed here.
Run: uv run --frozen --no-editable python -m trading_notes.numerical.filing_deadlines (standard library).
"""

# standard library imports
import datetime as dt
import sys

# project library imports
from trading_notes.numerical.report import CheckReport


def nth_weekday(y: int, m: int, wd: int, n: int) -> dt.date:
    """Return the n-th weekday wd (Monday 0 to Sunday 6) of month m of year y."""
    d = dt.date(y, m, 1)
    d += dt.timedelta((wd - d.weekday()) % 7)
    return d + dt.timedelta(7 * (n - 1))


def last_weekday(y: int, m: int, wd: int) -> dt.date:
    """Return the last weekday wd (Monday 0 to Sunday 6) of month m of year y."""
    d = dt.date(y, m + 1, 1) - dt.timedelta(1) if m < 12 else dt.date(y, 12, 31)
    return d - dt.timedelta((d.weekday() - wd) % 7)


def observed(d: dt.date) -> dt.date:
    """Return the observed day of a fixed-date holiday: Saturday to Friday, Sunday to Monday."""
    return (
        d - dt.timedelta(1) if d.weekday() == 5 else d + dt.timedelta(1) if d.weekday() == 6 else d
    )


def holidays(y: int) -> set[dt.date]:
    """Return the observed days of the eleven 5 U.S.C. 6103 holidays of year y."""
    return {
        observed(dt.date(y, 1, 1)),
        nth_weekday(y, 1, 0, 3),
        nth_weekday(y, 2, 0, 3),
        last_weekday(y, 5, 0),
        observed(dt.date(y, 6, 19)),
        observed(dt.date(y, 7, 4)),
        nth_weekday(y, 9, 0, 1),
        nth_weekday(y, 10, 0, 2),
        observed(dt.date(y, 11, 11)),
        nth_weekday(y, 11, 3, 4),
        observed(dt.date(y, 12, 25)),
    }


def is_bd(d: dt.date) -> bool:
    """Return whether d is a business day: a weekday that is not a holiday of its own year."""
    return d.weekday() < 5 and d not in holidays(d.year)


def roll(d: dt.date) -> dt.date:
    """Return d if it is a business day, else the next business day (Rule 0-3)."""
    while not is_bd(d):
        d += dt.timedelta(1)
    return d


def add_bd(d: dt.date, n: int) -> dt.date:
    """Return the n-th business day after d, for n >= 0; d itself is not counted."""
    while n:
        d += dt.timedelta(1)
        if is_bd(d):
            n -= 1
    return d


def check_holidays(report: CheckReport) -> None:
    """Check the computed holidays that the deadlines below cross."""
    report.same("Thanksgiving 2026", nth_weekday(2026, 11, 3, 4), dt.date(2026, 11, 26))
    report.same(
        "Veterans Day 2026 is a Wednesday holiday", dt.date(2026, 11, 11) in holidays(2026), True
    )


def check_deadlines(report: CheckReport) -> None:
    """Check the 13F, Form 4 and 13D due dates of the Q3 2026 and November 2026 examples."""
    raw = dt.date(2026, 9, 30) + dt.timedelta(45)
    report.same("13F raw due date for Q3 2026", raw, dt.date(2026, 11, 14))
    report.same("13F raw due date is a Saturday", raw.weekday(), 5)
    report.same("13F due after roll (Rule 0-3)", roll(raw), dt.date(2026, 11, 16))
    report.same(
        "Form 4 for a trade on Fri 20 Nov 2026",
        add_bd(dt.date(2026, 11, 20), 2),
        dt.date(2026, 11, 24),
    )
    report.same(
        "13D for an acquisition on Mon 23 Nov 2026",
        add_bd(dt.date(2026, 11, 23), 5),
        dt.date(2026, 12, 1),
    )
    report.same(
        "Form 4 latest under deemed execution (3 + 2 business days) from Fri 20 Nov",
        add_bd(dt.date(2026, 11, 20), 5),
        dt.date(2026, 11, 30),
    )


def main() -> int:
    """Run every check with a fresh report, print the summary and return the exit status (0 or 1)."""
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
