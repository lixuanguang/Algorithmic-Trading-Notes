"""Fixed-rate bond prices, yields, duration, convexity and horizon returns, per 100 of par."""

from datetime import date
from typing import overload

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import brentq

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]


def days_30_360(d1: date, d2: date) -> int:
    """U.S. 30/360 (bond basis) day count between two dates."""
    a, b = min(d1.day, 30), d2.day
    if a == 30 and b == 31:
        b = 30
    return 360 * (d2.year - d1.year) + 30 * (d2.month - d1.month) + (b - a)


def price_periodic(
    c: float, y: float, n: int, freq: float = 2, w: float = 1.0, face: float = 100.0
) -> float:
    """Return the full (dirty) price per 100 of n coupons of c/freq, the first w periods away."""
    cpn = c / freq
    price: float = sum(
        (cpn + (face if k == n else 0.0)) / (1 + y / freq) ** (k - 1 + w) for k in range(1, n + 1)
    )
    return price


def ytm_from_price(p: float, c: float, n: int, freq: float = 2, w: float = 1.0) -> float:
    """Return the yield to maturity that prices n coupons of c/freq at p."""
    return brentq(lambda y: price_periodic(c, y, n, freq, w) - p, -0.5, 1.0)


def mac_duration(c: float, y: float, n: int, freq: float = 2, w: float = 1.0) -> float:
    """Return the Macaulay duration in years of n coupons of c/freq at yield y."""
    cp = c / freq
    pv = [(cp + (100 if k == n else 0)) / (1 + y / freq) ** (k - 1 + w) for k in range(1, n + 1)]
    t = [(k - 1 + w) / freq for k in range(1, n + 1)]
    mean_t: float = sum(ti * p for ti, p in zip(t, pv, strict=True)) / sum(pv)
    return mean_t


def convexity(c: float, y: float, n: int, freq: float = 2, w: float = 1.0) -> float:
    """Return the convexity measure of n coupons of c/freq at yield y."""
    cp = c / freq
    P0 = price_periodic(c, y, n, freq, w)
    tot = 0.0
    for k in range(1, n + 1):
        tt = k - 1 + w
        tot += (cp + (100 if k == n else 0)) * tt * (tt + 1) / (1 + y / freq) ** (tt + 2)
    return tot / (P0 * freq**2)


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


def horizon(
    y_new: float, years: int = 3, c: float = 5.0, n: int = 14, y_buy: float = 0.048
) -> HorizonReturn:
    """Return the horizon return of a bond bought at y_buy, the yield moving at once to y_new.

    Coupons are reinvested at y_new and the bond is sold at y_new after `years`.
    """
    p_buy = price_periodic(c, y_buy, n)
    m = 2 * years
    coupons = c / 2 * m
    fv_cpn = c / 2 * ((1 + y_new / 2) ** m - 1) / (y_new / 2)
    p_sell = price_periodic(c, y_new, n - m)
    p_sell_old = price_periodic(c, y_buy, n - m)  # sale price had the yield not moved (pull to par)
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


def horizon_return_frac(
    y_new: float, H: float, c: float = 5.0, n: int = 14, y_buy: float = 0.048
) -> float:
    """Return the annualised horizon return over H years, from the yield at which it is bought."""
    p_buy = price_periodic(c, y_buy, n)
    m = 2 * H  # fractional half-years allowed
    val = 0.0
    for k in range(1, n + 1):
        cf = c / 2 + (100 if k == n else 0)
        val += cf * (1 + y_new / 2) ** (m - k)
    ann: float = 2 * ((val / p_buy) ** (1 / m) - 1)
    return ann
