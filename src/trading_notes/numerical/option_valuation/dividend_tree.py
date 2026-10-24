"""A binomial tree for options on a stock that pays known dollar dividends (Hull, sec. 21.3)."""

import math
from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]


class KnownDividendTree(Record):
    """A Cox-Ross-Rubinstein tree on S* = S - PV(dividends), dividends added back before ex-dates.

    Attributes:
        spot: The stock price.
        strike: The strike.
        rate: The continuously compounded rate.
        vol: The volatility of S*.
        maturity: The maturity in years.
        steps: The number of tree steps.
        dividends: Each dividend as (ex-dividend time, amount); those after maturity are ignored.
    """

    spot: float
    strike: float
    rate: float
    vol: float
    maturity: float
    steps: int
    dividends: Sequence[tuple[float, float]]

    def value(
        self, call: bool, american: bool = True, exercise_log: list[float] | None = None
    ) -> float:
        """Return the option value.

        Args:
            call: A call if true, else a put.
            american: Whether early exercise is allowed.
            exercise_log: If given, receives the time of each step at which some node exercises.
        """
        K, r, T, divs = self.strike, self.rate, self.maturity, self.dividends
        dt = T / self.steps
        pv0 = sum(D * math.exp(-r * t) for t, D in divs if t <= T)
        s_star0 = self.spot - pv0
        u = math.exp(self.vol * math.sqrt(dt))
        d = 1 / u
        p = (math.exp(r * dt) - d) / (u - d)
        disc = math.exp(-r * dt)

        def stock(i: int) -> Floats:
            t = i * dt
            pv = sum(D * math.exp(-r * (td - t)) for td, D in divs if t < td <= T)
            nodes: Floats = s_star0 * u ** np.arange(i, -1, -1) * d ** np.arange(0, i + 1) + pv
            return nodes

        def payoff(s: Floats) -> Floats:
            return np.maximum(s - K, 0) if call else np.maximum(K - s, 0)

        v = payoff(stock(self.steps))
        for i in range(self.steps - 1, -1, -1):
            v = disc * (p * v[:-1] + (1 - p) * v[1:])
            if american:
                ex = payoff(stock(i))
                if exercise_log is not None and np.any(ex > v):
                    exercise_log.append(i * dt)
                v = np.maximum(v, ex)
        return float(v[0])
