"""The weights of the fractional difference (1 - B)^d and fixed-width differencing."""

import math

import numpy as np
from numpy.typing import NDArray

from trading_notes.records import Record

type Floats = NDArray[np.float64]


class FractionalDifference(Record):
    """The fractional difference of order d.

    Attributes:
        order: d.
    """

    order: float

    def weights(self, n: int) -> Floats:
        """Return the first n weights by the recurrence w_k = -w_{k-1} (d - k + 1) / k."""
        dd = self.order
        wv = [1.0]
        for k in range(1, n):
            wv.append(-wv[-1] * (dd - k + 1) / k)
        return np.array(wv)

    def binomial_weights(self, n: int) -> Floats:
        """Return the first n weights from the binomial series (-1)^k prod(d - i) / k!."""
        dd = self.order
        return np.array(
            [(-1) ** k * math.prod(dd - i for i in range(k)) / math.factorial(k) for k in range(n)]
        )

    def width(self, thr: float, max_width: int = 100_000) -> int:
        """Return how many weights fixed-width differencing keeps: those before the first below thr.

        Args:
            thr: The cutoff on |w_k|.
            max_width: How many weights to search.

        Raises:
            ValueError: If |w_0| = 1 is already below thr, or no weight among the first
                max_width falls below it (thr not positive, or too small for the decay at
                this order).
        """
        below = np.flatnonzero(np.abs(self.weights(max_width)) < thr)
        if below.size == 0:
            raise ValueError(
                f"no weight of order {self.order} falls below {thr} within {max_width} weights"
            )
        if below[0] == 0:
            raise ValueError(f"threshold {thr} exceeds the leading weight 1")
        return int(below[0])

    def fixed_width(self, series: Floats, thr: float = 1e-4, max_width: int = 100_000) -> Floats:
        """Return the series differenced with the weights down to the first one below thr.

        Output t applies the kept weights to the observations t, t - 1, ..., so the result
        starts at the first full window and is empty when the series is shorter than one.

        Args:
            series: The observations, oldest first.
            thr: The cutoff on |w_k|.
            max_width: How many weights to search for the cutoff.

        Raises:
            ValueError: If the cutoff is not reached (see width).
        """
        width = self.width(thr, max_width)
        wv = self.weights(width)
        return np.array(
            [wv @ series[t - np.arange(width)] for t in range(width - 1, len(series))],
            dtype=np.float64,
        )
