"""Forward rate agreements valued with a projection curve and a separate discounting curve."""

import math
from collections.abc import Callable

from trading_notes.records import Record

type DiscountCurve = Callable[[float], float]
"""Discount factor P(t) for a time t in years."""


def flat_curve(rate: float) -> DiscountCurve:
    """Return the discount factors exp(-rate t) of a flat continuously compounded rate."""
    return lambda t: math.exp(-rate * t)


class ForwardRateAgreement(Record):
    """An FRA on the index rate L fixed at T1 for the period to T2: receive N tau (L - K).

    The forward F of a projection curve is (P(T1)/P(T2) - 1) / tau. End settlement pays at T2
    and is worth N tau (F - K) P_d(T2) on the discounting curve P_d; start settlement pays the
    end amount discounted at the fixing itself, at T1, and is worth N tau (F - K) P_d(T1) /
    (1 + tau F) when F is substituted for L, which is exact only for a deterministic L or a
    single curve.

    Attributes:
        fixing: T1, in years.
        payment: T2, in years.
        fixed_rate: K.
        notional: N.
    """

    fixing: float
    payment: float
    fixed_rate: float
    notional: float

    @property
    def accrual(self) -> float:
        """Return tau = T2 - T1."""
        return self.payment - self.fixing

    def forward(self, projection: DiscountCurve) -> float:
        """Return the simple forward rate F for the period on the projection curve."""
        return (projection(self.fixing) / projection(self.payment) - 1) / self.accrual

    def end_settled_value(self, discount: DiscountCurve, projection: DiscountCurve) -> float:
        """Return N tau (F - K) P_d(T2)."""
        F = self.forward(projection)
        return self.notional * self.accrual * (F - self.fixed_rate) * discount(self.payment)

    def start_settled_value(self, discount: DiscountCurve, projection: DiscountCurve) -> float:
        """Return N tau (F - K) P_d(T1) / (1 + tau F), with F substituted for the fixing."""
        F, tau = self.forward(projection), self.accrual
        return self.notional * tau * (F - self.fixed_rate) * discount(self.fixing) / (1 + tau * F)
