"""Liquidity and capacity: sweeping a book, thinned Poisson arrivals and a single-server queue."""

import collections
from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]


class SweepCost(Record):
    """The cost of a market order that sweeps the book, measured from the midpoint.

    Attributes:
        total: Total cost in currency, fees included.
        average: Average cost per share.
        marginal: Cost per share of the last share.
    """

    total: float
    average: float
    marginal: float


class AskBook(Record):
    """The ask side of a limit order book.

    Attributes:
        levels: (price, size) of each level, best first.
    """

    levels: tuple[tuple[float, int], ...]

    def sweep(self, q: int, mid: float, fee: float = 0.0) -> SweepCost:
        """Return the cost of buying q shares by sweeping the levels, with a fixed fee per order.

        Raises:
            ValueError: If the book holds fewer than q shares.
        """
        left, total, last = q, 0.0, float("nan")
        for price, size in self.levels:
            take = min(left, size)
            if take > 0:
                total += take * (price - mid)
                last = price - mid
                left -= take
            if left == 0:
                break
        if left > 0:
            raise ValueError(f"{q} shares exceed the book")
        total += fee
        return SweepCost(total=total, average=total / q, marginal=last)


def thinned_arrivals(
    rng: np.random.Generator, rate: Callable[[Floats], Floats], rate_max: float, horizon: float
) -> Floats:
    """Return the arrival times of a Poisson process with rate(t) <= rate_max on [0, horizon).

    Thinning is exact for any rate below the bound, a piecewise-constant one included: draw a
    homogeneous process at rate_max and keep each point with probability rate(t) / rate_max.
    """
    n = rng.poisson(rate_max * horizon)
    cand = np.sort(rng.uniform(0.0, horizon, n))
    keep = rng.uniform(0.0, 1.0, n) < rate(cand) / rate_max
    return cand[keep]


class ExponentialServer(Record):
    """One server with exponential service times, serving messages first in, first out.

    Attributes:
        service_rate: mu, messages per second.
    """

    service_rate: float

    def waits(self, rng: np.random.Generator, arrivals: Floats) -> tuple[Floats, Floats]:
        """Return each message's wait in queue W and service time S; time in system is W + S."""
        S = rng.exponential(1.0 / self.service_rate, arrivals.size)
        W = np.empty(arrivals.size)
        w, prev = 0.0, arrivals[0]
        for i, a in enumerate(arrivals):
            if i:
                w = max(0.0, w + S[i - 1] - (a - prev))
            W[i] = w
            prev = a
        return W, S

    def rejected_share(self, rng: np.random.Generator, arrivals: Floats, room: int) -> float:
        """Return the share of arrivals turned away because the system already holds `room`."""
        S = rng.exponential(1.0 / self.service_rate, arrivals.size)
        rejected = 0
        departures: collections.deque[float] = collections.deque()
        for a, s in zip(arrivals, S, strict=True):
            while departures and departures[0] <= a:
                departures.popleft()
            if len(departures) >= room:
                rejected += 1
                continue
            start = max(a, departures[-1] if departures else a)
            departures.append(start + s)
        return rejected / arrivals.size
