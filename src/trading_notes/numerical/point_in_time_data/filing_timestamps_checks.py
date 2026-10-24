"""Checks of EDGAR deemed filing dates, recorded availability and its lower bound."""

import datetime as dt
import sys

from trading_notes.numerical.point_in_time_data.edgar_filings import FilingRecord
from trading_notes.numerical.report import CheckReport
from trading_notes.numerical.us_calendar import add_business_days


def check_filing_dates(report: CheckReport) -> None:
    """Check deemed filing dates around both cutoffs and Thanksgiving."""
    report.same(
        "10-K starting 18:00 on Thu 19 Nov 2026 is filed Fri 20 Nov",
        FilingRecord(form="10-K", accepted=dt.datetime(2026, 11, 19, 18, 0)).filing_date(),
        dt.date(2026, 11, 20),
    )
    report.same(
        "Form 4 starting 21:30 on Thu 19 Nov 2026 is filed the same day",
        FilingRecord(form="4", accepted=dt.datetime(2026, 11, 19, 21, 30)).filing_date(),
        dt.date(2026, 11, 19),
    )
    report.same(
        "SC 13D/A starting 22:01 on Wed 25 Nov 2026 is filed Fri 27 Nov (Thanksgiving)",
        FilingRecord(form="SC 13D/A", accepted=dt.datetime(2026, 11, 25, 22, 1)).filing_date(),
        dt.date(2026, 11, 27),
    )
    report.same(
        "13F-HR starting 17:31 on Mon 16 Nov 2026 is filed Tue 17 Nov",
        FilingRecord(form="13F-HR", accepted=dt.datetime(2026, 11, 16, 17, 31)).filing_date(),
        dt.date(2026, 11, 17),
    )


def check_confidential_release(report: CheckReport) -> None:
    """Check a 13F filed after the cutoff and its later confidential-treatment amendment."""
    # A record carries every timestamp separately; the amendment and the later release are
    # separate records.
    orig = FilingRecord(
        form="13F-HR", accepted=dt.datetime(2026, 11, 16, 17, 31), period=dt.date(2026, 9, 30)
    )
    # positions omitted under confidential treatment, later released
    conf = FilingRecord(
        form="13F-HR/A",
        accepted=dt.datetime(2027, 9, 14, 9, 5),
        period=dt.date(2026, 9, 30),
        first_observed=dt.datetime(2027, 9, 14, 9, 40),
    )
    report.same(
        "original filing date differs from its acceptance date",
        orig.filing_date() != orig.accepted.date(),
        True,
    )
    report.same(
        "original without a recorded time: availability unknown, not midnight",
        orig.available_at(),
        None,
    )
    report.same(
        "original lower bound: 06:00 on the next business day",
        orig.not_before(),
        dt.datetime(2026, 11, 17, 6, 0),
    )
    report.same(
        "the old midnight fallback is before the lower bound (look-ahead)",
        dt.datetime.combine(add_business_days(orig.accepted.date(), 1), dt.time(0, 0))
        < orig.not_before(),
        True,
    )
    released = conf.available_at()
    report.same(
        "released positions available at their own first-observed time",
        released,
        dt.datetime(2027, 9, 14, 9, 40),
    )
    report.same(
        "the release does not back-date the original period",
        conf.period == orig.period and released is not None and released > orig.not_before(),
        True,
    )


def check_holiday_cutoff(report: CheckReport) -> None:
    """Check a 10-Q begun after the cutoff on the eve of Thanksgiving, with no recorded times."""
    # After the cutoff before a holiday: a 10-Q begun 18:10 on Wed 25 Nov 2026 has filing date
    # and lower bound Fri 27 Nov 06:00.
    tenq = FilingRecord(form="10-Q", accepted=dt.datetime(2026, 11, 25, 18, 10))
    report.same(
        "10-Q after cutoff before Thanksgiving: filing date Fri 27 Nov",
        tenq.filing_date(),
        dt.date(2026, 11, 27),
    )
    report.same(
        "10-Q after cutoff before Thanksgiving: not before Fri 27 Nov 06:00",
        tenq.not_before(),
        dt.datetime(2026, 11, 27, 6, 0),
    )
    report.same("10-Q without recorded times stays unknown", tenq.available_at(), None)


def check_late_forms(report: CheckReport) -> None:
    """Check a Form 4 and a Schedule 13D/A accepted between the two cutoffs."""
    # Form 4 after 5:30 is on the page's same-day list: the lower bound is acceptance, and
    # availability still needs a record.
    f4 = FilingRecord(
        form="4",
        accepted=dt.datetime(2026, 11, 19, 21, 30),
        disseminated=dt.datetime(2026, 11, 19, 21, 31),
    )
    report.same("Form 4 at 21:30: lower bound is acceptance", f4.not_before(), f4.accepted)
    report.same(
        "Form 4 at 21:30: recorded dissemination is used",
        f4.available_at(),
        dt.datetime(2026, 11, 19, 21, 31),
    )
    # Schedule 13D/A after 5:30: filed the same day under 232.13(a)(4), but not on the page's
    # same-day dissemination list.
    d13 = FilingRecord(form="SC 13D/A", accepted=dt.datetime(2026, 11, 19, 19, 0))
    report.same(
        "SC 13D/A at 19:00: filed the same day",
        d13.filing_date(),
        dt.date(2026, 11, 19),
    )
    report.same("SC 13D/A at 19:00: lower bound is acceptance only", d13.not_before(), d13.accepted)


def check_observation_error(report: CheckReport) -> None:
    """Check that a first observation recorded before the lower bound is detectable."""
    # A recorded first observation earlier than the lower bound would be a data error, flagged
    # rather than used.
    bad = FilingRecord(
        form="10-K",
        accepted=dt.datetime(2026, 11, 19, 18, 0),
        first_observed=dt.datetime(2026, 11, 19, 23, 0),
    )
    seen = bad.available_at()
    report.same(
        "first-observed before the lower bound is flagged",
        seen is not None and seen < bad.not_before(),
        True,
    )


def main() -> int:
    """Run every check with a fresh report, print the summary and return the exit status (0 or 1).

    Separate timestamps of an EDGAR filing, behind data:holdings-insider-filing-lags: the
    deemed filing date (17 CFR 232.13(a)(2) and (a)(4), eCFR text for 15 October 2026),
    the recorded availability and a lower bound on it from EDGAR's page "Determine the Status
    of My Filing" (dated June 4, 2024, last reviewed Oct. 31, 2024; read from the Wayback
    Machine capture of 5 October 2026). Synthetic records only; no SEC data are used.
    """
    report = CheckReport()
    check_filing_dates(report)
    check_confidential_release(report)
    check_holiday_cutoff(report)
    check_late_forms(report)
    check_observation_error(report)
    if report.failures:
        print("\nFAILED:", report.failures)
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
