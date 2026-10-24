"""Order-flow models: Hawkes processes, a latent spread on a tick grid, imbalance and sampling."""

import numpy as np
from numpy.typing import NDArray
from scipy import integrate, stats

from trading_notes.records import Record

type Floats = NDArray[np.float64]
type Ints = NDArray[np.int64]
# A best-quote state: bid price, bid size, ask price, ask size.
type QuoteState = tuple[float, int, float, int]


class ExponentialHawkes(Record):
    """A Hawkes process with intensity mu + sum_i alpha exp(-beta (t - t_i)).

    Attributes:
        mu: The baseline intensity.
        alpha: The jump of the intensity at each event.
        beta: The decay rate; alpha / beta is the branching ratio, below 1 for stationarity.
    """

    mu: float
    alpha: float
    beta: float

    def simulate(self, horizon: float, rng: np.random.Generator) -> Floats:
        """Return the event times in [0, horizon], by Ogata thinning."""
        t, excite = 0.0, 0.0
        ev: list[float] = []
        while True:
            lam_bar = self.mu + excite
            w = rng.exponential(1 / lam_bar)
            t_new = t + w
            excite *= np.exp(-self.beta * w)
            if t_new > horizon:
                return np.array(ev)
            if rng.uniform() * lam_bar <= self.mu + excite:
                ev.append(t_new)
                excite += self.alpha
            t = t_new

    def compensator_increments(self, events: Floats) -> Floats:
        """Return the compensator's increase between successive events.

        Under the model these time-rescaled durations are independent unit exponentials.
        """
        increments: list[float] = []
        excite_at = 0.0
        for i in range(1, len(events)):
            dt = events[i] - events[i - 1]
            excite_after = excite_at + self.alpha  # just after event i - 1
            increments.append(
                self.mu * dt + excite_after / self.beta * (1 - np.exp(-self.beta * dt))
            )
            excite_at = excite_after * np.exp(-self.beta * dt)
        return np.array(increments)


class RectifiedHawkes(Record):
    """A Hawkes process with intensity (mu + sum_i a exp(-beta (t - t_i)))^+, so a may be negative.

    Attributes:
        mu: The baseline intensity, which bounds the intensity when a < 0.
        a: The jump of the linear predictor at each event.
        beta: The decay rate.
    """

    mu: float
    a: float
    beta: float

    def simulate(self, horizon: float, rng: np.random.Generator) -> Floats:
        """Return the event times in [0, horizon], by thinning at the rate mu (valid for a < 0)."""
        t, ex = 0.0, 0.0
        ev: list[float] = []
        while True:
            w = rng.exponential(1 / self.mu)
            t += w
            ex *= np.exp(-self.beta * w)
            if t > horizon:
                return np.array(ev)
            if rng.uniform() * self.mu <= max(self.mu + ex, 0.0):
                ev.append(t)
                ex += self.a


class LatentSpread(Record):
    """A latent spread, gamma distributed in old ticks, observed after rounding to a tick grid.

    Attributes:
        shape: The gamma shape.
        mean: The mean latent spread in old ticks.
    """

    shape: float
    mean: float

    def pdf(self, x: float) -> float:
        """Return the density of the latent spread at x old ticks."""
        value: float = stats.gamma.pdf(x, a=self.shape, scale=self.mean / self.shape)
        return value

    def expected_observed(self, delta: float, kmax: int = 400) -> float:
        """Return the expected observed spread in old ticks on a grid of 1/delta old ticks.

        The spread rounds to the nearest grid point, with at least one tick.
        """
        tot = 0.0
        p1 = integrate.quad(self.pdf, 0, 1.5 / delta)[0]
        tot += (1 / delta) * p1
        for k in range(2, kmax):
            pk = integrate.quad(self.pdf, (k - 0.5) / delta, (k + 0.5) / delta)[0]
            tot += (k / delta) * pk
            if (k - 0.5) / delta > self.mean * 10:
                break
        return tot


def order_flow_imbalance(prev: QuoteState, cur: QuoteState) -> float:
    """Return the Cont-Kukanov-Stoikov order-flow imbalance between two best-quote states."""
    pb0, qb0, pa0, qa0 = prev
    pb1, qb1, pa1, qa1 = cur
    return (pb1 >= pb0) * qb1 - (pb1 <= pb0) * qb0 - (pa1 <= pa0) * qa1 + (pa1 >= pa0) * qa0


def previous_tick(path: Floats, observed: Ints, grid: Floats) -> Floats:
    """Return the values of a path observed at the times `observed`, sampled on a time grid.

    Each grid time takes the last observation at or before it (the first, before any).
    """
    idx = np.searchsorted(observed, grid, side="right") - 1
    value: Floats = path[observed[np.clip(idx, 0, len(observed) - 1)]]
    return value
