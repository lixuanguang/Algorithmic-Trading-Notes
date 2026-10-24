"""A funded FX carry position: borrow domestic, buy and invest foreign, convert back and repay."""

import math

from trading_notes.numerical.records import Record


class FundedCarry(Record):
    """Per unit of domestic currency borrowed, with simple interest on each currency's basis.

    Attributes:
        spot: S0, domestic per foreign.
        domestic_rate: i_d.
        foreign_rate: i_f.
        days: The holding period in days.
        domestic_basis: The domestic day-count denominator.
        foreign_basis: The foreign day-count denominator.
    """

    spot: float
    domestic_rate: float
    foreign_rate: float
    days: int
    domestic_basis: int = 360
    foreign_basis: int = 365

    @property
    def tau_d(self) -> float:
        """Return the domestic accrual fraction."""
        return self.days / self.domestic_basis

    @property
    def tau_f(self) -> float:
        """Return the foreign accrual fraction."""
        return self.days / self.foreign_basis

    def forward(self) -> float:
        """Return the covered-parity forward S0 (1 + i_d tau_d) / (1 + i_f tau_f)."""
        return (
            self.spot * (1 + self.domestic_rate * self.tau_d) / (1 + self.foreign_rate * self.tau_f)
        )

    def pnl(self, ST: float) -> float:
        """Return the arithmetic funded P&L if the spot ends at ST."""
        return ST / self.spot * (1 + self.foreign_rate * self.tau_f) - (
            1 + self.domestic_rate * self.tau_d
        )

    def log_excess(self, s: float) -> float:
        """Return the continuously compounded excess return after a currency move s."""
        return (
            math.log(1 + s)
            + math.log(1 + self.foreign_rate * self.tau_f)
            - math.log(1 + self.domestic_rate * self.tau_d)
        )
