"""Covariance of asynchronously observed prices: refresh-time sampling and Hayashi-Yoshida."""

from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray

from trading_notes.records import Record

type Floats = NDArray[np.float64]


def refresh_times(times: Sequence[Floats]) -> Floats:
    """Return the refresh times of several observation series, each sorted ascending.

    Barndorff-Nielsen, Hansen, Lunde and Shephard's Definition 1: each refresh time is the first
    time by which every series has traded since the previous one.
    """
    out: list[float] = []
    cur = -np.inf
    while True:
        nxt = []
        for t in times:
            k = np.searchsorted(t, cur, side="right")
            if k >= len(t):
                return np.array(out)
            nxt.append(t[k])
        cur = max(nxt)
        out.append(cur)


class ObservedPrices(Record):
    """A price observed at irregular times, with its known value at time 0.

    Attributes:
        times: The observation times, ascending, shape (n,).
        values: The value at time 0, then the value at each observation, shape (n + 1,).
    """

    times: Floats
    values: Floats

    def previous_tick(self, at: Floats) -> Floats:
        """Return the last observed value at or before each time in `at`."""
        value: Floats = self.values[np.searchsorted(self.times, at, side="right")]
        return value

    def hayashi_yoshida(self, other: ObservedPrices) -> float:
        """Return the sum of r1_i r2_j over all pairs of observation intervals that overlap."""
        a0, a1, r1 = np.r_[0.0, self.times[:-1]], self.times, np.diff(self.values)
        b0, b1, r2 = np.r_[0.0, other.times[:-1]], other.times, np.diff(other.values)
        tot, j = 0.0, 0
        for i in range(len(r1)):
            while j < len(r2) and b1[j] <= a0[i]:
                j += 1
            k = j
            while k < len(r2) and b0[k] < a1[i]:
                tot += r1[i] * r2[k]
                k += 1
        return tot
