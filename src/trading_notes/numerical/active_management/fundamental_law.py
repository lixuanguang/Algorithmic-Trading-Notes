"""The fundamental law of active management."""

import math

from trading_notes.records import Record


class FundamentalLaw(Record):
    """An active strategy's skill, breadth and implementation efficiency.

    Attributes:
        ic: Information coefficient, the correlation of forecasts with outcomes.
        breadth: Independent bets a year.
        transfer: Transfer coefficient, 1 for an unconstrained portfolio.
    """

    ic: float
    breadth: float
    transfer: float = 1.0

    @property
    def information_ratio(self) -> float:
        """Return IR = TC x IC x sqrt(BR)."""
        return self.transfer * self.ic * math.sqrt(self.breadth)
