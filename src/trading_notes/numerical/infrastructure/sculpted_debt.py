"""Project debt sculpted to a target debt service cover ratio, and its loan-life cover ratio."""

import numpy as np
from numpy.typing import NDArray

from trading_notes.records import Record

type Floats = NDArray[np.float64]


class SculptedDebt(Record):
    """Senior debt whose service is the cash available for it divided by a target DSCR.

    Attributes:
        available_cash: Cash flow available for debt service in each operating year.
        tenor: The loan's operating years.
        rate: Its annual interest rate.
        target_dscr: The target debt service cover ratio.
    """

    available_cash: Floats
    tenor: int
    rate: float
    target_dscr: float

    def debt_service(self) -> Floats:
        """Return each year's debt service, CFADS / target DSCR, over the tenor."""
        ds: Floats = self.available_cash[: self.tenor] / self.target_dscr
        return ds

    def discount_factors(self) -> Floats:
        """Return the compounding factors (1 + rate)^t, t = 1..tenor."""
        return np.asarray((1 + self.rate) ** np.arange(1, self.tenor + 1), dtype=np.float64)

    def opening_balance(self) -> float:
        """Return the debt the sculpted service repays: its present value at the rate."""
        return float(np.sum(self.debt_service() / self.discount_factors()))

    def schedule(self) -> tuple[list[tuple[float, float, float]], float]:
        """Return each year's (opening balance, interest, principal) and the closing balance."""
        bal = self.opening_balance()
        rows: list[tuple[float, float, float]] = []
        for service in self.debt_service():
            interest = self.rate * bal
            principal = service - interest
            rows.append((bal, interest, principal))
            bal -= principal
        return rows, bal

    def llcr(self, year: int, balance: float) -> float:
        """Return PV(CFADS over the remaining loan life) / balance at the start of a year."""
        remaining = self.tenor - year
        pv = np.sum(
            self.available_cash[year : self.tenor] / (1 + self.rate) ** np.arange(1, remaining + 1)
        )
        return float(pv) / balance
