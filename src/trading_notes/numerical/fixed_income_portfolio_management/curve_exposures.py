"""Annual bond cash flows on a zero curve: prices, durations, key-rate exposures and horizons."""

import numpy as np
from numpy.typing import NDArray

from trading_notes.records import Record

type Floats = NDArray[np.float64]


class AnnualZeroCurve(Record):
    """An annual-compounding zero curve, linear in maturity to a point and flat beyond.

    Attributes:
        level: The zero rate at t = 0.
        slope: The rise per year of maturity.
        flat_after: The maturity beyond which the curve is flat.
    """

    level: float
    slope: float
    flat_after: float

    def zero(self, t: float, shift: float = 0.0, twist: float = 0.0) -> float:
        """Return the zero rate at t years, optionally shifted and twisted.

        The twist moves the 1-year rate by -twist and the 10-year by +twist, linearly between.
        """
        base = self.level + self.slope * min(t, self.flat_after)
        tw = twist * (min(max(t, 1.0), 10.0) - 5.5) / 4.5
        return base + shift + tw

    def price(self, flows: CashFlows, **kw: float) -> float:
        """Return the price of cash flows on the curve, shifted or twisted by kw."""
        return sum(
            c / (1 + self.zero(t, **kw)) ** t
            for c, t in zip(flows.amounts, flows.times, strict=True)
        )

    def modified_duration(self, flows: CashFlows, h: float = 1e-4, **kw: float) -> float:
        """Return the modified duration by central parallel shifts of the curve."""
        p0 = self.price(flows, **kw)
        rest = {k: v for k, v in kw.items() if k != "shift"}
        return (self.price(flows, shift=-h, **rest) - self.price(flows, shift=h, **rest)) / (
            2 * p0 * h
        )

    def pv_bumped(self, cf: Floats, bumps: Floats) -> np.float64:
        """Return the PV of annual cash flows (years 1-10) with each zero rate bumped."""
        return np.float64(
            sum(cf[k] / (1 + self.zero(k + 1) + bumps[k]) ** (k + 1) for k in range(10))
        )

    def key_rates(self, cf: Floats, h: float = 1e-5) -> Floats:
        """Return key-rate durations to each annual zero rate, bumping one rate at a time."""
        v = self.pv_bumped(cf, np.zeros(10))
        eye = np.eye(10)
        return np.array(
            [
                -(self.pv_bumped(cf, h * eye[k]) - self.pv_bumped(cf, -h * eye[k])) / (2 * h * v)
                for k in range(10)
            ]
        )


class CashFlows(Record):
    """Payments at whole years.

    Attributes:
        amounts: The payments.
        times: Their times in years, one per payment.
    """

    amounts: list[float]
    times: list[int]

    @classmethod
    def annual_bond(cls, coupon: float, mat: int) -> CashFlows:
        """Return the annual cash flows per 100 face of a coupon bond maturing in mat years."""
        cfs = [100 * coupon] * mat
        cfs[-1] += 100
        return cls(amounts=cfs, times=list(range(1, mat + 1)))

    def horizon_value(self, y_after: float, horizon: int, twist: float = 0.0) -> float:
        """Return the value at the horizon of reinvested payments and the later ones sold.

        The curve is flat at y_after (annual), with an optional twist: reinvestment at
        y_after - twist, discounting at y_after + twist.
        """
        total = 0.0
        for c_, t_ in zip(self.amounts, self.times, strict=True):
            if t_ <= horizon:
                total += c_ * (1 + y_after - twist) ** (horizon - t_)
            else:
                total += c_ / (1 + y_after + twist) ** (t_ - horizon)
        return total

    def macaulay_duration(self, y: float) -> float:
        """Return the Macaulay duration at a flat annual yield y."""
        pv = [c_ / (1 + y) ** t_ for c_, t_ in zip(self.amounts, self.times, strict=True)]
        return sum(t_ * v for t_, v in zip(self.times, pv, strict=True)) / sum(pv)
