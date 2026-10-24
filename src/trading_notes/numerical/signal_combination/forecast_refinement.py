"""Refined forecasts: information coefficients and regression weights of correlated forecasts."""

import numpy as np
from numpy.typing import NDArray

from trading_notes.records import Record

type Floats = NDArray[np.float64]


class ForecastSet(Record):
    """Raw forecasts g of a return r, described by their second moments.

    Attributes:
        volatility: Std(r).
        covariance: Cov(g), one row and column per forecast.
        return_covariance: Cov(r, g_i) for each forecast.
    """

    volatility: float
    covariance: Floats
    return_covariance: Floats

    def ic(self, i: int) -> float:
        """Return forecast i's information coefficient Cov(r, g_i) / (Std r Std g_i)."""
        return float(self.return_covariance[i] / (self.volatility * np.sqrt(self.covariance[i, i])))

    def weights(self) -> Floats:
        """Return the regression weights Cov(g)^-1 Cov(r, g) of the refined forecast."""
        return np.asarray(
            np.linalg.solve(self.covariance, self.return_covariance), dtype=np.float64
        )

    def combined_ic(self) -> float:
        """Return the IC of the combined forecast, sqrt(c' Sigma^-1 c) / Std(r)."""
        return float(np.sqrt(self.return_covariance @ self.weights()) / self.volatility)
