"""source verification (2026-10-17) (audit repair): the separate timestamps of an EDGAR filing, behind data:holdings-insider-filing-lags.

Rule checked (17 CFR 232.13(a)(2) and (a)(4), eCFR text for 15 October 2026; business days per 232.12): a direct
transmission commencing by 5:30 p.m. Eastern on a business day is deemed filed that day, later ones the next business
day; Forms 3, 4, 5, 144, Schedules 13D, 13G and 14N (and their amendments) are deemed filed the same day up to 10 p.m.
So the official filing date can differ from the calendar date of acceptance, and neither is the time the filing was
public or the time a user first saw it.

Corrected 2026-10-17 (empirical extensions (2026-10-17)). The first version's fallback, "the start of the next business day after the
acceptance time", was not conservative: EDGAR's page "Determine the Status of My Filing" (dated June 4, 2024, last
reviewed Oct. 31, 2024; read from the Wayback Machine capture of 5 October 2026 because sec.gov refused the script)
says most submissions that begin transmission after 5:30 p.m. "will receive a filing date of 6:00 a.m. ET the next
business day and will not be disseminated by EDGAR until the next business day". So such a filing cannot be public at
00:00, and the page gives no time on that day by which it will be. No text read bounds dissemination from above.
The panel therefore keeps two quantities:
  available_at(rec)   = recorded dissemination time, else recorded first-observed time, else None (unknown: the
                        filing does not enter a decision-time panel on this record alone);
  not_before(rec)     = a lower bound only (acceptance time; for an after-cutoff submission whose form is not on the
                        page's same-day list, 06:00 on the next business day). Using a filing before this bound is
                        certain look-ahead; using it after the bound is not thereby safe.
Schedules 13D, 13G and 14N are deemed filed the same day up to 10 p.m. under 232.13(a)(4), but the page's same-day
dissemination list (3, 4, 5, 144 and their amendments, and MEF/POS 462B forms) does not include them; their lower
bound is therefore the acceptance time only.
Synthetic records only; no SEC data are used.
Run: uv run --frozen --no-editable python -m trading_notes.numerical.filing_timestamps (standard library).

All times are naive datetimes on Eastern time, as EDGAR states them.
"""

import datetime as dt
import sys
from dataclasses import dataclass
from typing import Final

from trading_notes.numerical.report import CheckReport

LATE_FORMS: Final = frozenset({"3", "4", "5", "144", "SC 13D", "SC 13G", "SC 14N"})
HOLIDAYS_2026: Final = frozenset(
    {
        dt.date(2026, 11, 11),
        dt.date(2026, 11, 26),
        dt.date(2026, 12, 25),
    }
)  # 5 U.S.C. 6103, Nov-Dec 2026
SAME_DAY_DISSEMINATION: Final = frozenset(
    {
        "3",
        "4",
        "5",
        "144",
    }
)  # page list, with /A amendments; MEF and POS 462B forms omitted here
CUTOFF: Final = dt.time(17, 30)
LATE_CUTOFF: Final = dt.time(22, 0)


@dataclass(frozen=True)
class FilingRecord:
    """The timestamps a panel records for one filing, each kept separately.

    An amendment or a later release is a record of its own. Times are naive Eastern.

    Attributes:
        form: EDGAR form type, `/A` marking an amendment (for example "13F-HR/A").
        accepted: Acceptance time.
        period: Period of report, when recorded.
        disseminated: Recorded dissemination time, or None if none was recorded.
        first_observed: Recorded time the filing was first seen, or None if none was recorded.
    """

    form: str
    accepted: dt.datetime
    period: dt.date | None = None
    disseminated: dt.datetime | None = None
    first_observed: dt.datetime | None = None


def base_form(form: str) -> str:
    """Return the form type without an amendment suffix: "SC 13D/A" gives "SC 13D"."""
    return form.split("/")[0]


def business_day(d: dt.date) -> bool:
    """Return whether d is a weekday outside `HOLIDAYS_2026` (holidays outside Nov-Dec 2026 are not known)."""
    return d.weekday() < 5 and d not in HOLIDAYS_2026


def next_business_day(d: dt.date) -> dt.date:
    """Return the first business day strictly after d."""
    d += dt.timedelta(days=1)
    while not business_day(d):
        d += dt.timedelta(days=1)
    return d


def filing_date(form: str, start_et: dt.datetime) -> dt.date:
    """Deemed filing date for a direct transmission commencing at start_et (Eastern, naive).

    A start on a non-business day is filed the next business day. On a business day, a start
    at or before the cutoff (22:00 for `LATE_FORMS` and their amendments, else 17:30) is filed
    that day, a later one the next business day.
    """
    d = start_et.date()
    if not business_day(d):
        return next_business_day(d)
    cutoff = LATE_CUTOFF if base_form(form) in LATE_FORMS else CUTOFF
    return d if start_et.time() <= cutoff else next_business_day(d)


def available_at(rec: FilingRecord) -> dt.datetime | None:
    """Recorded availability, or None when no dissemination or first-observed time was recorded.

    Dissemination takes precedence over first observation. None means unknown: no other
    timestamp stands in for it.
    """
    if rec.disseminated is not None:
        return rec.disseminated
    return rec.first_observed


def not_before(rec: FilingRecord) -> dt.datetime:
    """Lower bound on public availability; never a substitute for available_at.

    The acceptance time, except for an acceptance after 17:30 of a form on neither the
    same-day dissemination list nor `LATE_FORMS`: then 06:00 on the next business day.
    """
    acc = rec.accepted
    base = base_form(rec.form)
    if acc.time() > CUTOFF and base not in SAME_DAY_DISSEMINATION and base not in LATE_FORMS:
        return dt.datetime.combine(next_business_day(acc.date()), dt.time(6, 0))
    return acc


def check_filing_dates(report: CheckReport) -> None:
    """Check deemed filing dates around both cutoffs and Thanksgiving."""
    report.same(
        "10-K starting 18:00 on Thu 19 Nov 2026 is filed Fri 20 Nov",
        filing_date("10-K", dt.datetime(2026, 11, 19, 18, 0)),
        dt.date(2026, 11, 20),
    )
    report.same(
        "Form 4 starting 21:30 on Thu 19 Nov 2026 is filed the same day",
        filing_date("4", dt.datetime(2026, 11, 19, 21, 30)),
        dt.date(2026, 11, 19),
    )
    report.same(
        "SC 13D/A starting 22:01 on Wed 25 Nov 2026 is filed Fri 27 Nov (Thanksgiving)",
        filing_date("SC 13D/A", dt.datetime(2026, 11, 25, 22, 1)),
        dt.date(2026, 11, 27),
    )
    report.same(
        "13F-HR starting 17:31 on Mon 16 Nov 2026 is filed Tue 17 Nov",
        filing_date("13F-HR", dt.datetime(2026, 11, 16, 17, 31)),
        dt.date(2026, 11, 17),
    )


def check_confidential_release(report: CheckReport) -> None:
    """Check a 13F filed after the cutoff and its later confidential-treatment amendment."""
    # a record carries every timestamp separately; the amendment and the later release are separate records
    orig = FilingRecord("13F-HR", dt.datetime(2026, 11, 16, 17, 31), period=dt.date(2026, 9, 30))
    # positions omitted under confidential treatment, later released
    conf = FilingRecord(
        "13F-HR/A",
        dt.datetime(2027, 9, 14, 9, 5),
        period=dt.date(2026, 9, 30),
        first_observed=dt.datetime(2027, 9, 14, 9, 40),
    )
    report.same(
        "original filing date differs from its acceptance date",
        filing_date(orig.form, orig.accepted) != orig.accepted.date(),
        True,
    )
    report.same(
        "original without a recorded time: availability unknown, not midnight",
        available_at(orig),
        None,
    )
    report.same(
        "original lower bound: 06:00 on the next business day",
        not_before(orig),
        dt.datetime(2026, 11, 17, 6, 0),
    )
    report.same(
        "the old midnight fallback is before the lower bound (look-ahead)",
        dt.datetime.combine(next_business_day(orig.accepted.date()), dt.time(0, 0))
        < not_before(orig),
        True,
    )
    released = available_at(conf)
    report.same(
        "released positions available at their own first-observed time",
        released,
        dt.datetime(2027, 9, 14, 9, 40),
    )
    report.same(
        "the release does not back-date the original period",
        conf.period == orig.period and released is not None and released > not_before(orig),
        True,
    )


def check_holiday_cutoff(report: CheckReport) -> None:
    """Check a 10-Q begun after the cutoff on the eve of Thanksgiving, with no recorded times."""
    # after the cutoff before a holiday: 10-Q begun 18:10 on Wed 25 Nov 2026 -> filing date and lower bound Fri 27 Nov 06:00
    tenq = FilingRecord("10-Q", dt.datetime(2026, 11, 25, 18, 10))
    report.same(
        "10-Q after cutoff before Thanksgiving: filing date Fri 27 Nov",
        filing_date("10-Q", tenq.accepted),
        dt.date(2026, 11, 27),
    )
    report.same(
        "10-Q after cutoff before Thanksgiving: not before Fri 27 Nov 06:00",
        not_before(tenq),
        dt.datetime(2026, 11, 27, 6, 0),
    )
    report.same("10-Q without recorded times stays unknown", available_at(tenq), None)


def check_late_forms(report: CheckReport) -> None:
    """Check a Form 4 and a Schedule 13D/A accepted between the two cutoffs."""
    # Form 4 after 5:30 is on the page's same-day list: lower bound is acceptance, availability still needs a record
    f4 = FilingRecord(
        "4", dt.datetime(2026, 11, 19, 21, 30), disseminated=dt.datetime(2026, 11, 19, 21, 31)
    )
    report.same("Form 4 at 21:30: lower bound is acceptance", not_before(f4), f4.accepted)
    report.same(
        "Form 4 at 21:30: recorded dissemination is used",
        available_at(f4),
        dt.datetime(2026, 11, 19, 21, 31),
    )
    # Schedule 13D/A after 5:30: filed same day under 232.13(a)(4); the page does not list it for same-day dissemination
    d13 = FilingRecord("SC 13D/A", dt.datetime(2026, 11, 19, 19, 0))
    report.same(
        "SC 13D/A at 19:00: filed the same day",
        filing_date(d13.form, d13.accepted),
        dt.date(2026, 11, 19),
    )
    report.same("SC 13D/A at 19:00: lower bound is acceptance only", not_before(d13), d13.accepted)


def check_observation_error(report: CheckReport) -> None:
    """Check that a first observation recorded before the lower bound is detectable."""
    # a recorded first observation earlier than the lower bound would be a data error, flagged rather than used
    bad = FilingRecord(
        "10-K", dt.datetime(2026, 11, 19, 18, 0), first_observed=dt.datetime(2026, 11, 19, 23, 0)
    )
    seen = available_at(bad)
    report.same(
        "first-observed before the lower bound is flagged",
        seen is not None and seen < not_before(bad),
        True,
    )


def main() -> int:
    """Run every check with a fresh report, print the summary and return the exit status (0 or 1)."""
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
