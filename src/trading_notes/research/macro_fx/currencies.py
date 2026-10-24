"""The nine dollar exchange rates of the FX tests and their FRED spot, CPI and rate series."""

import math
from collections.abc import Mapping
from pathlib import Path
from typing import Final

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.newey_west import Month
from trading_notes.records import Record
from trading_notes.research.fred import monthly_values

type Floats = NDArray[np.float64]

US_CPI: Final = "CPIAUCNS"
US_RATE: Final = "IR3TIB01USM156N"


class Currency(Record):
    """A currency's FRED series.

    Attributes:
        spot: The H.10/G.5 spot series (monthly averages of noon buying rates).
        foreign_per_usd: Whether the spot series quotes foreign currency per dollar.
        cpi: The CPI series.
        quarterly: Whether the CPI is quarterly.
        rate: The three-month interbank rate (IR3TIB01) series.
    """

    spot: str
    foreign_per_usd: bool
    cpi: str
    quarterly: bool
    rate: str

    def log_usd_per_unit(self, folder: Path) -> dict[Month, float]:
        """Return the log spot rate in dollars per unit of the currency, by month."""
        return {
            t: (-math.log(v) if self.foreign_per_usd else math.log(v))
            for t, v in monthly_values(folder / f"{self.spot}.csv").items()
        }


CURRENCIES: Final = {
    "JPY": Currency(
        spot="EXJPUS",
        foreign_per_usd=True,
        cpi="JPNCPIALLMINMEI",
        quarterly=False,
        rate="IR3TIB01JPM156N",
    ),
    "GBP": Currency(
        spot="EXUSUK",
        foreign_per_usd=False,
        cpi="GBRCPIALLMINMEI",
        quarterly=False,
        rate="IR3TIB01GBM156N",
    ),
    "CHF": Currency(
        spot="EXSZUS",
        foreign_per_usd=True,
        cpi="CHECPIALLMINMEI",
        quarterly=False,
        rate="IR3TIB01CHM156N",
    ),
    "CAD": Currency(
        spot="EXCAUS",
        foreign_per_usd=True,
        cpi="CANCPIALLMINMEI",
        quarterly=False,
        rate="IR3TIB01CAM156N",
    ),
    "AUD": Currency(
        spot="EXUSAL",
        foreign_per_usd=False,
        cpi="AUSCPIALLQINMEI",
        quarterly=True,
        rate="IR3TIB01AUM156N",
    ),
    "NZD": Currency(
        spot="EXUSNZ",
        foreign_per_usd=False,
        cpi="NZLCPIALLQINMEI",
        quarterly=True,
        rate="IR3TIB01NZM156N",
    ),
    "SEK": Currency(
        spot="EXSDUS",
        foreign_per_usd=True,
        cpi="SWECPIALLMINMEI",
        quarterly=False,
        rate="IR3TIB01SEM156N",
    ),
    "NOK": Currency(
        spot="EXNOUS",
        foreign_per_usd=True,
        cpi="NORCPIALLMINMEI",
        quarterly=False,
        rate="IR3TIB01NOM156N",
    ),
    "DKK": Currency(
        spot="EXDNUS",
        foreign_per_usd=True,
        cpi="DNKCPIALLMINMEI",
        quarterly=False,
        rate="IR3TIB01DKM156N",
    ),
}


class RandomWalkComparison(Record):
    """Forecasts of a change in the log spot rate against the random walk's forecast of zero.

    Attributes:
        actual: The realised changes.
        forecast: The model's forecasts of them.
    """

    actual: Floats
    forecast: Floats

    @property
    def sse(self) -> float:
        """Return the model's sum of squared forecast errors."""
        return float(((self.actual - self.forecast) ** 2).sum())

    @property
    def sse_random_walk(self) -> float:
        """Return the random walk's sum of squared forecast errors."""
        return float((self.actual**2).sum())

    @property
    def r2(self) -> float:
        """Return the out-of-sample R^2 against the random walk."""
        return 1 - self.sse / self.sse_random_walk

    @property
    def clark_west(self) -> Floats:
        """Return the Clark-West adjusted loss differentials, one per forecast."""
        a, f = self.actual, self.forecast
        return a**2 - ((a - f) ** 2 - f**2)


def turnover(new: Mapping[str, float], old: Mapping[str, float]) -> float:
    """Return the sum of absolute weight changes from the old portfolio to the new one."""
    return sum(abs(new.get(c, 0) - old.get(c, 0)) for c in set(new) | set(old))
