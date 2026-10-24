"""Fixed-rate bond prices, yields, duration, convexity and horizon returns, per 100 of par."""

from datetime import date
from typing import overload

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import brentq

from trading_notes.records import Record

type Floats = NDArray[np.float64]


def days_30_360(d1: date, d2: date) -> int:
    """U.S. 30/360 (bond basis) day count between two dates."""
    a, b = min(d1.day, 30), d2.day
    if a == 30 and b == 31:
        b = 30
    return 360 * (d2.year - d1.year) + 30 * (d2.month - d1.month) + (b - a)


class FixedRateBond(Record):
    """A bullet bond paying coupon/freq each period, valued at a periodically compounded yield.

    Attributes:
        coupon: The annual coupon per 100 of par.
        periods: The coupons left, the last paid with the face value.
        freq: Coupons per year.
        first: Periods to the first coupon, a fraction of a period between coupon dates.
        face: The redemption amount.
    """

    coupon: float
    periods: int
    freq: float = 2
    first: float = 1.0
    face: float = 100.0

    def cash_flow(self, k: int) -> float:
        """Return the k-th payment (k = 1, ..., periods): the coupon, with the face value last."""
        return self.coupon / self.freq + (self.face if k == self.periods else 0.0)

    def price(self, y: float) -> float:
        """Return the full (dirty) price at yield y."""
        price: float = sum(
            self.cash_flow(k) / (1 + y / self.freq) ** (k - 1 + self.first)
            for k in range(1, self.periods + 1)
        )
        return price

    def yield_at(self, p: float) -> float:
        """Return the yield to maturity at which the full price is p."""
        return brentq(lambda y: self.price(y) - p, -0.5, 1.0)

    def macaulay_duration(self, y: float) -> float:
        """Return the Macaulay duration in years at yield y."""
        ks = range(1, self.periods + 1)
        pv = [self.cash_flow(k) / (1 + y / self.freq) ** (k - 1 + self.first) for k in ks]
        t = [(k - 1 + self.first) / self.freq for k in ks]
        mean_t: float = sum(ti * p for ti, p in zip(t, pv, strict=True)) / sum(pv)
        return mean_t

    def convexity(self, y: float) -> float:
        """Return the convexity measure at yield y."""
        tot = 0.0
        for k in range(1, self.periods + 1):
            tt = k - 1 + self.first
            tot += self.cash_flow(k) * tt * (tt + 1) / (1 + y / self.freq) ** (tt + 2)
        return tot / (self.price(y) * self.freq**2)

    def remaining(self, periods_passed: int) -> FixedRateBond:
        """Return the same bond after periods_passed whole coupon periods."""
        return self.model_copy(update={"periods": self.periods - periods_passed})

    def horizon_return(self, y_buy: float, y_new: float, years: int) -> HorizonReturn:
        """Return the sources of return of a semiannual bond bought at y_buy, held for years.

        The yield moves at once to y_new; coupons are reinvested at y_new and the bond is sold
        at y_new.
        """
        p_buy = self.price(y_buy)
        m = 2 * years
        coupons = self.coupon / 2 * m
        fv_cpn = self.coupon / 2 * ((1 + y_new / 2) ** m - 1) / (y_new / 2)
        later = self.remaining(m)
        p_sell = later.price(y_new)
        p_sell_old = later.price(y_buy)  # sale price had the yield not moved (pull to par)
        total = fv_cpn + p_sell
        ann = 2 * ((total / p_buy) ** (1 / m) - 1)
        return HorizonReturn(
            coupons=coupons,
            int_on_int=fv_cpn - coupons,
            pull_to_par=p_sell_old - p_buy,
            rate_effect=p_sell - p_sell_old,
            total=total - p_buy,
            ann=ann,
        )

    def annualised_horizon_return(self, y_buy: float, y_new: float, H: float) -> float:
        """Return the annualised return over H years (fractional half-years allowed).

        The bond is bought at y_buy, the yield moves at once to y_new, and every payment is
        carried to the horizon at y_new.
        """
        p_buy = self.price(y_buy)
        m = 2 * H
        val = 0.0
        for k in range(1, self.periods + 1):
            val += self.cash_flow(k) * (1 + y_new / 2) ** (m - k)
        ann: float = 2 * ((val / p_buy) ** (1 / m) - 1)
        return ann


class LinearZeroCurve(Record):
    """A government zero curve a + b t, semiannually compounded.

    Attributes:
        a: The zero rate at t = 0.
        b: The slope per year of maturity.
    """

    a: float
    b: float

    @overload
    def zero(self, t: float) -> float: ...
    @overload
    def zero(self, t: Floats) -> Floats: ...
    def zero(self, t: float | Floats) -> float | Floats:
        """Return the zero rate at t years."""
        return self.a + self.b * t

    def par_yield(self, T: float) -> float:
        """Return the par yield of a semiannual bond to maturity T."""
        k = np.arange(1, round(2 * T) + 1) / 2
        dfs = (1 + self.zero(k) / 2) ** (-2 * k)
        par: float = 2 * (1 - dfs[-1]) / dfs.sum()
        return par


class IndexedFloater(Record):
    """A semiannual floater paying a flat reference rate plus a quoted margin (Handbook Ex. 4-7).

    Attributes:
        reference: The reference rate, assumed unchanged.
        quoted_margin: The margin over the reference rate in the coupon.
        periods: Semiannual periods to maturity.
    """

    reference: float
    quoted_margin: float
    periods: int

    def price(self, dm: float) -> float:
        """Return the price per 100, discounting at the reference rate plus discount margin dm."""
        n = self.periods
        cf = 100 * (self.reference + self.quoted_margin) / 2
        return sum(
            (cf + (100 if k == n else 0)) / (1 + (self.reference + dm) / 2) ** k
            for k in range(1, n + 1)
        )


class HorizonReturn(Record):
    """The sources of a bond's return over a horizon, per 100 of par.

    Attributes:
        coupons: The coupons received.
        int_on_int: Interest on reinvested coupons.
        pull_to_par: The price change had the yield not moved.
        rate_effect: The price change from the yield move.
        total: The total gain.
        ann: The annualised (bond-equivalent) return.
    """

    coupons: float
    int_on_int: float
    pull_to_par: float
    rate_effect: float
    total: float
    ann: float
