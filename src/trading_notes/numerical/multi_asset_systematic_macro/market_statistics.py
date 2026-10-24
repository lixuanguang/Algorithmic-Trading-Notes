"""Extracts of BIS OTC derivatives notionals and UN population projections, read from CSV."""

import csv
from pathlib import Path
from typing import Self

from trading_notes.numerical.records import Record


class OtcNotionals(Record):
    """Notional outstanding by half-year, risk category and instrument, in USD trillions.

    Attributes:
        amounts: (period, risk, instrument) -> notional; risk "A" is all OTC derivatives and "D"
            interest-rate derivatives, instrument "A" all instruments.
    """

    amounts: dict[tuple[str, str, str], float]

    @classmethod
    def read(cls, path: Path) -> Self:
        """Read the extract, whose notionals are in USD millions."""
        with path.open() as fh:
            return cls(
                amounts={
                    (r["period"], r["risk"], r["instrument"]): float(r["notional_usd_millions"])
                    / 1e6
                    for r in csv.DictReader(fh)
                }
            )

    def __getitem__(self, key: tuple[str, str, str]) -> float:
        """Return the notional of (period, risk, instrument)."""
        return self.amounts[key]


class AgePopulations(Record):
    """Each country's 1 July populations aged 15-64 and 35-69, in thousands, by year.

    Attributes:
        years: country -> year -> (15-64, 35-69).
    """

    years: dict[str, dict[int, tuple[float, float]]]

    @classmethod
    def read(cls, path: Path) -> Self:
        """Read the extract of the UN World Population Prospects 2024, medium variant."""
        pop: dict[str, dict[int, tuple[float, float]]] = {}
        with path.open() as fh:
            for r in csv.DictReader(fh):
                pop.setdefault(r["country"], {})[int(r["year"])] = (
                    float(r["pop_15_64_thousands"]),
                    float(r["pop_35_69_thousands"]),
                )
        return cls(years=pop)

    def peak_year(self, country: str, group: int, last: int) -> int:
        """Return the year up to `last` with the largest population of group 0 (15-64) or 1."""
        ys = self.years[country]
        return max((y for y in ys if y <= last), key=lambda y: ys[y][group])
