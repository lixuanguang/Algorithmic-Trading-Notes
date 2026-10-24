"""GIPS return calculations: Modified Dietz returns and a composite membership rule."""

import math
from collections.abc import Sequence

from trading_notes.numerical.records import Record


def mod_dietz(bmv: float, emv: float, flows: Sequence[tuple[float, float]]) -> float:
    """Return the Modified Dietz return.

    Args:
        bmv: Beginning market value.
        emv: Ending market value.
        flows: Each external flow as (amount, weight = fraction of the period remaining).
    """
    return (emv - bmv - sum(f for f, _ in flows)) / (bmv + sum(f * wt for f, wt in flows))


class MembershipRule(Record):
    """One portfolio's dates under the invented composite policy, in fractional months.

    Attributes:
        start: When it was funded; 0 if held all year.
        end: When it was terminated, if it was.
        sig_flow_month: The month of a client-directed flow of 25% or more, if any.
        mandate_change: When the client changed its mandate, if it did.
        nondiscretionary: Whether it is non-discretionary.
    """

    start: float
    end: float | None = None
    sig_flow_month: int | None = None
    mandate_change: float | None = None
    nondiscretionary: bool = False

    def member(self, m: int) -> bool:
        """Return whether the portfolio is in the composite in month m (1 to 12)."""
        if self.nondiscretionary:
            return False
        if self.start != 0 and m < math.floor(self.start) + 1:  # first full month after funding
            return False
        if self.end is not None and m >= math.floor(self.end):
            return False
        if self.sig_flow_month is not None and m in (self.sig_flow_month, self.sig_flow_month + 1):
            return False
        return not (self.mandate_change is not None and m >= math.floor(self.mandate_change) + 1)
