"""Annual bond cash flows on a zero curve: prices, durations, key-rate exposures and horizons."""

from collections.abc import Sequence
from typing import cast

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.records import Record

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

    def price(self, cfs: Sequence[float], times: Sequence[int], **kw: float) -> float:
        """Return the price of cash flows on the curve, shifted or twisted by kw."""
        return sum(c / (1 + self.zero(t, **kw)) ** t for c, t in zip(cfs, times, strict=True))

    def modified_duration(
        self, cfs: Sequence[float], times: Sequence[int], h: float = 1e-4, **kw: float
    ) -> float:
        """Return the modified duration by central parallel shifts of the curve."""
        p0 = self.price(cfs, times, **kw)
        rest = {k: v for k, v in kw.items() if k != "shift"}
        return (
            self.price(cfs, times, shift=-h, **rest) - self.price(cfs, times, shift=h, **rest)
        ) / (2 * p0 * h)

    def pv_bumped(self, cf: Floats, bumps: Floats) -> np.float64:
        """Return the PV of annual cash flows (years 1-10) with each zero rate bumped."""
        return cast(
            np.float64,
            sum(cf[k] / (1 + self.zero(k + 1) + bumps[k]) ** (k + 1) for k in range(10)),
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


def bond(coupon: float, mat: int) -> tuple[list[float], list[int]]:
    """Return the annual cash flows per 100 face and their times of a coupon bond."""
    times = list(range(1, mat + 1))
    cfs = [100 * coupon] * mat
    cfs[-1] += 100
    return cfs, times


def horizon_value(
    cfs: Sequence[float], times: Sequence[int], y_after: float, horizon: int, twist: float = 0.0
) -> float:
    """Return the value at the horizon of reinvested coupons and the remaining cash flows sold.

    The curve is flat at y_after (annual), with an optional twist: reinvestment at y_after - twist,
    discounting at y_after + twist.
    """
    total = 0.0
    for c_, t_ in zip(cfs, times, strict=True):
        if t_ <= horizon:
            total += c_ * (1 + y_after - twist) ** (horizon - t_)
        else:
            total += c_ / (1 + y_after + twist) ** (t_ - horizon)
    return total


def mac(cfs: Sequence[float], times: Sequence[int], y: float) -> float:
    """Return the Macaulay duration at a flat annual yield y."""
    pv = [c_ / (1 + y) ** t_ for c_, t_ in zip(cfs, times, strict=True)]
    return sum(t_ * v for t_, v in zip(times, pv, strict=True)) / sum(pv)
