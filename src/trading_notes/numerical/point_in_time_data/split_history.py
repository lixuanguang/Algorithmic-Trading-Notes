"""An append-only bitemporal history of a stock's split factors."""

import datetime as dt
from collections.abc import Iterable
from typing import Final

from trading_notes.records import Record

INF: Final = dt.date(9999, 12, 31)  # end of an open range: still current
NO_SPLIT: Final = 1.0  # the factor where no row matches


class SplitRow(Record):
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
    """The append-only bitemporal split history of one stock, after Fowler's actual/record time.

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
                    SplitRow(
                        record_from=r.record_from,
                        record_to=closed,
                        actual_from=r.actual_from,
                        actual_to=r.actual_to,
                        split_factor=r.split_factor,
                    )
                )
                if r.actual_from < actual_from:
                    new.append(
                        SplitRow(
                            record_from=record_date,
                            record_to=INF,
                            actual_from=r.actual_from,
                            actual_to=actual_from - dt.timedelta(days=1),
                            split_factor=r.split_factor,
                        )
                    )
            else:
                new.append(r)
        new.append(
            SplitRow(
                record_from=record_date,
                record_to=INF,
                actual_from=actual_from,
                actual_to=INF,
                split_factor=factor,
            )
        )
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
