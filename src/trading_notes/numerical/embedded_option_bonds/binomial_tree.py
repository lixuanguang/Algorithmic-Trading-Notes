"""The lognormal binomial short-rate tree of the Handbook (chap. 36): calibration and valuation."""

import math
from collections.abc import Callable, Sequence
from typing import Final

import numpy as np
from scipy.optimize import brentq

from trading_notes.records import Record

SIG: Final = 0.10  # the Handbook's volatility


class LognormalTree(Record):
    """A lognormal tree of one-period rates, one-half probability per branch.

    Attributes:
        lows: The lowest rate of each period 0..n-1; lows[0] is the root rate.
        sigma: The volatility; node i of a period has rate low * exp(2 sigma i).
    """

    lows: tuple[float, ...]
    sigma: float = SIG

    @classmethod
    def calibrate(cls, par: Sequence[float], sigma: float = SIG) -> LognormalTree:
        """Return the tree whose lowest rates reprice each annual par bond at 100.

        Args:
            par: The par yields of maturities 1..n, as decimals.
            sigma: The volatility of the tree.
        """
        lows = [par[0]]
        for k in range(1, len(par)):
            c = 100 * par[k]

            def price_gap(low: float, c: float = c, k: int = k) -> float:
                return cls(lows=(*lows, low), sigma=sigma).value([c] * (k + 1)) - 100

            lows.append(brentq(price_gap, 1e-6, 0.5))
        return cls(lows=tuple(lows), sigma=sigma)

    def rate(self, t: int, i: int) -> float:
        """Return the rate at period t, node i (i = the number of up moves)."""
        return self.lows[t] * math.exp(2 * self.sigma * i)

    def value(
        self,
        cfs: Sequence[float],
        spread: float = 0.0,
        call: float | None = None,
        put: float | None = None,
        exercise_from: int = 1,
        coupon_fn: Callable[[int, float], float] | None = None,
        face: float = 100.0,
    ) -> float:
        """Return the root value of a bond by backward induction, per 100 of face.

        Args:
            cfs: The fixed coupon paid at the end of each period t = 0..n-1.
            spread: A constant spread (OAS) added to every node rate when discounting.
            call: The call price, applied from period `exercise_from` on, after the coupon due.
            put: The put price, applied like the call price.
            exercise_from: The first period at which the options can be exercised.
            coupon_fn: coupon_fn(t, r) replaces cfs with a coupon set from the node rate r at
                the start of period t and paid in arrears.
            face: The redemption value.
        """
        n = len(self.lows)
        v = np.full(n + 1, face)  # values at maturity, before the final coupon is added
        for t in range(n - 1, -1, -1):
            new = np.empty(t + 1)
            for i in range(t + 1):
                r = self.rate(t, i) + spread
                c = coupon_fn(t, r - spread) if coupon_fn else cfs[t]
                cont = 0.5 * ((v[i + 1] + c) + (v[i] + c)) / (1 + r)
                if t >= exercise_from:
                    if call is not None:
                        cont = min(cont, call)
                    if put is not None:
                        cont = max(cont, put)
                new[i] = cont
            v = new
        return float(v[0])
