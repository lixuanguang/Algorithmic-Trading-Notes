"""Raw SVI total-variance slices and the butterfly function of Gatheral and Jacquier."""

import math
from collections.abc import Callable

from trading_notes.records import Record

# A total-variance slice w(k) of log-moneyness k.
type Slice = Callable[[float], float]


class RawSVI(Record):
    """A raw SVI slice w(k) = a + b (rho (k - m) + sqrt((k - m)^2 + sigma^2)) (eq. 3.1).

    Attributes:
        a: Level.
        b: Slope of the wings.
        rho: Skew, between -1 and 1.
        m: Horizontal shift.
        sigma: Curvature at the minimum.
    """

    a: float
    b: float
    rho: float
    m: float
    sigma: float

    def __call__(self, k: float) -> float:
        """Return the total variance at log-moneyness k."""
        return self.a + self.b * (
            self.rho * (k - self.m) + math.sqrt((k - self.m) ** 2 + self.sigma * self.sigma)
        )


def butterfly(k: float, w: Slice, eps: float = 1e-4) -> float:
    """Return the butterfly function g(k) of eq. (2.1), with w' and w'' by central differences.

    A slice is free of butterfly arbitrage only if g >= 0 everywhere (Lemma 2.2).
    """
    W = w(k)
    W1 = (w(k + eps) - w(k - eps)) / (2 * eps)
    W2 = (w(k + eps) - 2 * W + w(k - eps)) / eps**2
    return (1 - k * W1 / (2 * W)) ** 2 - W1**2 / 4 * (1 / W + 0.25) + W2 / 2
