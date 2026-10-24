"""Risk-adjusted and downside performance measures, drawdowns and Carino linking factors."""

import math

import numpy as np
from numpy.typing import NDArray
from scipy.stats import norm

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]


class MarketLine(Record):
    """The risk-free rate and the benchmark return of a single-index model, in percent a year.

    Attributes:
        rf: Risk-free rate.
        benchmark: Benchmark return.
    """

    rf: float
    benchmark: float

    def alpha_treynor(self, r: float, beta: float) -> tuple[float, float]:
        """Return Jensen's alpha and the Treynor ratio of a return r with beta; inf at beta 0."""
        alpha = r - self.rf - beta * (self.benchmark - self.rf)
        return alpha, (math.inf if beta == 0 else (r - self.rf) / beta)


class Drawdown(Record):
    """The largest peak-to-trough fall of cumulative wealth.

    Attributes:
        depth: The fall as a fraction of the peak, negative.
        peak: Month index of the peak (0 is the start, before the first return).
        trough: Month index of the trough.
        recovery: First month at or above the peak again, or None if never.
    """

    depth: float
    peak: int
    trough: int
    recovery: int | None


def downside_deviation(x: Floats, mar: float) -> float:
    """Return the downside deviation of x about mar, dividing by all n observations."""
    return math.sqrt((np.minimum(x - mar, 0.0) ** 2).mean())


def sortino_annual(x: Floats, mar: float) -> float:
    """Return the annualised Sortino ratio of monthly returns x; inf with no shortfall."""
    d = downside_deviation(x, mar)
    return math.inf if d == 0 else 12 * (x.mean() - mar) / (math.sqrt(12) * d)


def normal_downside_ratio(z: float) -> float:
    """Return the normal downside deviation over sigma, for a target z sigmas from the mean."""
    return math.sqrt((1 + z * z) * norm.cdf(z) + z * norm.pdf(z))


def max_drawdown(x: Floats) -> Drawdown:
    """Return the maximum drawdown of monthly returns x, in percent."""
    w = np.concatenate([[1.0], np.cumprod(1 + x / 100)])
    peak = np.maximum.accumulate(w)
    d = w / peak - 1
    trough = int(d.argmin())
    pk = int(w[: trough + 1].argmax())
    rec = next((k for k in range(trough, len(w)) if w[k] >= w[pk]), None)
    return Drawdown(depth=d.min(), peak=pk, trough=trough, recovery=rec)


def carino_k(rr: float, bb: float) -> float:
    """Return the Carino factor (ln(1 + R) - ln(1 + B)) / (R - B), 1 / (1 + R) when R = B."""
    return (math.log(1 + rr) - math.log(1 + bb)) / (rr - bb) if rr != bb else 1 / (1 + rr)
