"""The Taylor rule, the carry of curve positions per unit of DV01 and an annual-pay bond."""

import numpy as np

from trading_notes.records import Record


class TaylorRule(Record):
    """Taylor's (1993) rule r = p + 0.5 y + 0.5 (p - 2) + 2, in percent.

    Attributes:
        neutral_real: The equilibrium real rate.
        target: The inflation target.
        gap_weight: The weight on the output gap.
        inflation_weight: The weight on inflation above target.
    """

    neutral_real: float = 2.0
    target: float = 2.0
    gap_weight: float = 0.5
    inflation_weight: float = 0.5

    def rate(self, p: float, y: float) -> float:
        """Return the policy rate for inflation p and output gap y."""
        return (
            p + self.gap_weight * y + self.inflation_weight * (p - self.target) + self.neutral_real
        )

    def gliner_printed(self, p: float, y: float) -> float:
        """Return Gliner's printed second form, with 1/(2y) for the output term."""
        return p + 1 / (2 * y) + self.inflation_weight * (p - self.target) + self.neutral_real


class CurveLeg(Record):
    """A bond position financed at repo, in percent and years of duration.

    Attributes:
        yield_: The bond's yield.
        duration: Its duration.
    """

    yield_: float
    duration: float

    def carry_per_dv01(self, repo: float) -> float:
        """Return the annual carry per unit of DV01: (yield - repo) / duration."""
        return (self.yield_ - repo) / self.duration


class AnnualBond(Record):
    """A bond paying an annual coupon per 100 face, priced from a flat annual yield.

    Attributes:
        coupon: The annual coupon per 100 face.
        years: Its maturity.
    """

    coupon: float
    years: int

    def price(self, y: float) -> float:
        """Return the price at yield y."""
        times = np.arange(1, self.years + 1)
        cf = np.full(self.years, self.coupon)
        cf[-1] += 100
        value: float = np.sum(cf / (1 + y) ** times)
        return value

    def modified_duration(self, y: float, h: float = 1e-4) -> float:
        """Return -P'(y) / P by a central difference of step h."""
        return -(self.price(y + h) - self.price(y - h)) / (2 * h) / self.price(y)

    def convexity(self, y: float, h: float = 1e-4) -> float:
        """Return P''(y) / P by a central second difference of step h."""
        p0 = self.price(y)
        return (self.price(y + h) - 2 * p0 + self.price(y - h)) / h**2 / p0
