"""EDGAR filing records: deemed filing dates, recorded availability and its lower bound."""

import datetime as dt
from typing import Final

from trading_notes.numerical.us_calendar import add_business_days, is_business_day
from trading_notes.records import Record

# Forms deemed filed the same day up to 22:00 under 17 CFR 232.13(a)(4), with their amendments.
LATE_FORMS: Final = frozenset({"3", "4", "5", "144", "SC 13D", "SC 13G", "SC 14N"})
# The forms that EDGAR's "Determine the Status of My Filing" page lists for same-day
# dissemination after 17:30, with their amendments; its MEF and POS 462B forms are omitted.
SAME_DAY_DISSEMINATION: Final = frozenset({"3", "4", "5", "144"})
CUTOFF: Final = dt.time(17, 30)
LATE_CUTOFF: Final = dt.time(22, 0)


class FilingRecord(Record):
    """The timestamps a panel records for one filing, each kept separately.

    An amendment or a later release is a record of its own. Times are naive datetimes on
    Eastern time, as EDGAR states them; business days are weekdays other than federal
    holidays (232.12).

    Attributes:
        form: EDGAR form type, `/A` marking an amendment (for example "13F-HR/A").
        accepted: Acceptance time, taken as the start of the direct transmission.
        period: Period of report, when recorded.
        disseminated: Recorded dissemination time, or None if none was recorded.
        first_observed: Recorded time the filing was first seen, or None if none was recorded.
    """

    form: str
    accepted: dt.datetime
    period: dt.date | None = None
    disseminated: dt.datetime | None = None
    first_observed: dt.datetime | None = None

    @property
    def base_form(self) -> str:
        """Return the form type without an amendment suffix: "SC 13D/A" gives "SC 13D"."""
        return self.form.split("/")[0]

    def filing_date(self) -> dt.date:
        """Return the deemed filing date under 17 CFR 232.13(a)(2) and (a)(4).

        A transmission starting on a non-business day is filed the next business day. On a
        business day, one starting at or before the cutoff (22:00 for `LATE_FORMS` and their
        amendments, else 17:30) is filed that day, a later one the next business day. The
        filing date can therefore differ from the calendar date of acceptance, and neither
        is the time the filing was public.
        """
        d = self.accepted.date()
        if not is_business_day(d):
            return add_business_days(d, 1)
        cutoff = LATE_CUTOFF if self.base_form in LATE_FORMS else CUTOFF
        return d if self.accepted.time() <= cutoff else add_business_days(d, 1)

    def available_at(self) -> dt.datetime | None:
        """Return the recorded availability, or None when no time was recorded.

        Dissemination takes precedence over first observation. None means unknown: the
        filing does not enter a decision-time panel on this record alone, and no other
        timestamp stands in for it.
        """
        if self.disseminated is not None:
            return self.disseminated
        return self.first_observed

    def not_before(self) -> dt.datetime:
        """Return a lower bound on public availability; never a substitute for available_at.

        The acceptance time, except for an acceptance after 17:30 of a form on neither the
        same-day dissemination list nor `LATE_FORMS`: such a submission receives a filing date
        of 06:00 on the next business day and is not disseminated before then (EDGAR's page,
        dated June 4, 2024). Using a filing before this bound is certain look-ahead; using it
        after the bound is not thereby safe, since no source bounds dissemination from above.
        Schedules 13D, 13G and 14N are filed the same day up to 22:00 but are not on the
        dissemination list, so their bound is the acceptance time only.
        """
        acc, base = self.accepted, self.base_form
        if acc.time() > CUTOFF and base not in SAME_DAY_DISSEMINATION and base not in LATE_FORMS:
            return dt.datetime.combine(add_business_days(acc.date(), 1), dt.time(6, 0))
        return acc
