"""Getmansky-Lo-Makarov smoothing of reported hedge-fund returns."""

from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]


class ReturnSmoothing(Record):
    """Reported returns as a weighted average of current and lagged true returns.

    Attributes:
        theta: Weights on the true returns of lags 0, 1, ...; they sum to one.
    """

    theta: Sequence[float]

    @property
    def volatility_ratio(self) -> float:
        """Return reported over true volatility, sqrt(sum theta_k^2), for i.i.d. true returns."""
        return float(np.sqrt(np.sum(np.array(self.theta) ** 2)))

    @property
    def autocorrelation(self) -> float:
        """Return the first-order autocorrelation of reported returns."""
        theta = np.array(self.theta)
        lagged = theta[0] * theta[1]
        for k in range(1, len(theta) - 1):
            lagged = lagged + theta[k] * theta[k + 1]
        return float(lagged) / float(np.sum(theta**2))

    def report(self, true: Floats) -> Floats:
        """Return the reported series of the true returns; it is len(theta) - 1 shorter."""
        theta, q = self.theta, len(self.theta)
        n = len(true)
        reported: Floats = theta[0] * true[q - 1 :]
        for k in range(1, q):
            reported = reported + theta[k] * true[q - 1 - k : n - k]
        return reported
