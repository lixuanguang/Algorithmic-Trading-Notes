"""Tests of the bitemporal split history, EDGAR filing records and the business-day calendar."""

# The examples' full runs are tested in test_checks.py. These pin down the history's append-only
# rows and inclusive boundaries, the filing record's cutoffs, amendments and availability, and the
# federal-holiday calendar both filing examples use.

import datetime as dt
import unittest

from pydantic import ValidationError

from trading_notes.numerical.point_in_time_data.edgar_filings import FilingRecord
from trading_notes.numerical.point_in_time_data.split_history import INF, SplitHistory, SplitRow
from trading_notes.numerical.us_calendar import (
    add_business_days,
    federal_holidays,
    last_weekday,
    rolled_forward,
)

D = dt.date


def row(
    record_from: dt.date,
    record_to: dt.date,
    actual_from: dt.date,
    actual_to: dt.date,
    factor: float,
) -> SplitRow:
    """Return a split row from its two ranges and factor."""
    return SplitRow(
        record_from=record_from,
        record_to=record_to,
        actual_from=actual_from,
        actual_to=actual_to,
        split_factor=factor,
    )


def corrected_history() -> SplitHistory:
    """Return the example's history: a 2-for-1 split recorded on 3 March, corrected on 20 March."""
    history = SplitHistory([row(D(2000, 1, 1), INF, D(2000, 1, 1), INF, 1.0)])
    history.record(D(2026, 3, 3), D(2026, 3, 2), 2.0)
    history.record(D(2026, 3, 20), D(2026, 3, 2), 1.5)
    return history


class BitemporalHistory(unittest.TestCase):
    """A split history is append-only, inclusive at its boundaries and owned by one instance."""

    def test_correction_closes_and_appends_rows(self) -> None:
        """Both records leave every earlier row, closed or replaced, in lookup order."""
        self.assertEqual(
            corrected_history().rows,
            (
                row(D(2000, 1, 1), D(2026, 3, 2), D(2000, 1, 1), INF, 1.0),  # seed, closed
                row(D(2026, 3, 3), INF, D(2000, 1, 1), D(2026, 3, 1), 1.0),  # pre-split remainder
                row(D(2026, 3, 3), D(2026, 3, 19), D(2026, 3, 2), INF, 2.0),  # first entry, closed
                row(D(2026, 3, 20), INF, D(2026, 3, 2), INF, 1.5),  # correction
            ),
        )

    def test_boundaries_are_inclusive(self) -> None:
        """Record and actual ranges include both ends, the sentinel date included."""
        factor = corrected_history().factor_at
        self.assertEqual(factor(D(2026, 3, 5), D(2026, 3, 2)), 1.0)
        self.assertEqual(factor(D(2026, 3, 5), D(2026, 3, 3)), 2.0)
        self.assertEqual(factor(D(2026, 3, 5), D(2026, 3, 19)), 2.0)
        self.assertEqual(factor(D(2026, 3, 5), D(2026, 3, 20)), 1.5)
        self.assertEqual(factor(D(2026, 3, 1), D(2026, 10, 17)), 1.0)
        self.assertEqual(factor(D(2026, 3, 2), D(2026, 10, 17)), 1.5)
        self.assertEqual(factor(INF, INF), 1.5)

    def test_no_matching_row_gives_no_split(self) -> None:
        """Dates outside every row, or an empty history, give the factor 1.0."""
        self.assertEqual(SplitHistory().factor_at(D(2026, 3, 5), D(2026, 10, 17)), 1.0)
        self.assertEqual(corrected_history().factor_at(D(1999, 12, 31), D(2026, 10, 17)), 1.0)
        self.assertEqual(corrected_history().factor_at(D(2026, 3, 5), D(1999, 12, 31)), 1.0)

    def test_instances_do_not_share_history(self) -> None:
        """Recording into one history changes neither another nor the rows it started from."""
        seed = [row(D(2000, 1, 1), INF, D(2000, 1, 1), INF, 1.0)]
        first, second = SplitHistory(seed), SplitHistory(seed)
        first.record(D(2026, 3, 3), D(2026, 3, 2), 2.0)
        self.assertEqual(len(first.rows), 3)
        self.assertEqual(second.rows, tuple(seed))
        self.assertEqual(len(seed), 1)
        self.assertEqual(SplitHistory().rows, ())

    def test_rows_are_immutable_and_hashable(self) -> None:
        """A row cannot be changed in place, and equal rows hash alike."""
        seed = row(D(2000, 1, 1), INF, D(2000, 1, 1), INF, 1.0)
        with self.assertRaises(ValidationError):
            setattr(seed, "split_factor", 2.0)  # a write the type checker would reject
        self.assertEqual(hash(seed), hash(row(D(2000, 1, 1), INF, D(2000, 1, 1), INF, 1.0)))


class FilingRecords(unittest.TestCase):
    """Availability is recorded or unknown; the deemed filing date and lower bound stay apart."""

    def test_unknown_availability_stays_none(self) -> None:
        """Without recorded times availability is None, whatever else the record holds."""
        record = FilingRecord(
            form="10-K", accepted=dt.datetime(2026, 11, 19, 18, 0), period=D(2026, 9, 30)
        )
        self.assertIsNone(record.available_at())
        self.assertEqual(record.not_before(), dt.datetime(2026, 11, 20, 6, 0))

    def test_dissemination_takes_precedence(self) -> None:
        """A recorded dissemination wins even over an earlier first observation."""
        both = FilingRecord(
            form="10-K",
            accepted=dt.datetime(2026, 11, 19, 9, 0),
            disseminated=dt.datetime(2026, 11, 19, 9, 30),
            first_observed=dt.datetime(2026, 11, 19, 9, 10),
        )
        seen = both.model_copy(update={"disseminated": None})
        self.assertEqual(both.available_at(), dt.datetime(2026, 11, 19, 9, 30))
        self.assertEqual(seen.available_at(), dt.datetime(2026, 11, 19, 9, 10))

    def test_cutoffs_are_inclusive(self) -> None:
        """A start at 17:30 (22:00 for late forms) is filed that day; a second later is not."""

        def filed(form: str, start: dt.datetime) -> dt.date:
            return FilingRecord(form=form, accepted=start).filing_date()

        self.assertEqual(filed("10-K", dt.datetime(2026, 11, 19, 17, 30)), D(2026, 11, 19))
        self.assertEqual(filed("10-K", dt.datetime(2026, 11, 19, 17, 30, 1)), D(2026, 11, 20))
        self.assertEqual(filed("4/A", dt.datetime(2026, 11, 19, 22, 0)), D(2026, 11, 19))
        self.assertEqual(filed("4/A", dt.datetime(2026, 11, 19, 22, 0, 1)), D(2026, 11, 20))
        at_cutoff = FilingRecord(form="10-K", accepted=dt.datetime(2026, 11, 19, 17, 30))
        self.assertEqual(at_cutoff.not_before(), at_cutoff.accepted)
        late = FilingRecord(form="10-K", accepted=dt.datetime(2026, 11, 19, 17, 30, 1))
        self.assertEqual(late.not_before(), dt.datetime(2026, 11, 20, 6, 0))

    def test_amendments_follow_their_base_form(self) -> None:
        """An /A form takes its base form's cutoff and dissemination treatment."""
        f4a = FilingRecord(form="4/A", accepted=dt.datetime(2026, 11, 19, 19, 0))
        tenka = FilingRecord(form="10-K/A", accepted=dt.datetime(2026, 11, 19, 19, 0))
        self.assertEqual((f4a.base_form, tenka.base_form), ("4", "10-K"))
        self.assertEqual(f4a.not_before(), f4a.accepted)
        self.assertEqual(tenka.not_before(), dt.datetime(2026, 11, 20, 6, 0))

    def test_non_business_days(self) -> None:
        """A weekend start is filed the next business day; holidays are skipped."""
        weekend = FilingRecord(form="10-K", accepted=dt.datetime(2026, 11, 21, 9, 0))
        self.assertEqual(weekend.filing_date(), D(2026, 11, 23))
        christmas_eve = FilingRecord(form="10-K", accepted=dt.datetime(2026, 12, 24, 18, 0))
        self.assertEqual(christmas_eve.not_before(), dt.datetime(2026, 12, 28, 6, 0))


class BusinessDays(unittest.TestCase):
    """The computed federal-holiday calendar the deadline and filing examples share."""

    def test_observed_fixed_date_holidays(self) -> None:
        """A Saturday holiday is observed on Friday, a Sunday one on Monday."""
        self.assertIn(D(2026, 7, 3), federal_holidays(2026))
        self.assertNotIn(D(2026, 7, 4), federal_holidays(2026))
        self.assertIn(D(2027, 7, 5), federal_holidays(2027))
        self.assertIn(D(2027, 12, 24), federal_holidays(2027))
        self.assertEqual(len(federal_holidays(2026)), 11)

    def test_last_weekday_including_december(self) -> None:
        """The last Monday of May and of December (the year-end branch)."""
        self.assertEqual(last_weekday(2026, 5, 0), D(2026, 5, 25))
        self.assertEqual(last_weekday(2026, 12, 0), D(2026, 12, 28))

    def test_business_day_steps(self) -> None:
        """A business day rolls to itself; adding skips a holiday and counts from the next day."""
        self.assertEqual(rolled_forward(D(2026, 11, 16)), D(2026, 11, 16))
        self.assertEqual(rolled_forward(D(2026, 11, 14)), D(2026, 11, 16))
        self.assertEqual(add_business_days(D(2026, 11, 10), 1), D(2026, 11, 12))
        self.assertEqual(add_business_days(D(2026, 11, 10), 0), D(2026, 11, 10))


if __name__ == "__main__":
    unittest.main()
