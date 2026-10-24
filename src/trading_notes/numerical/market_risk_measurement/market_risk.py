"""Normal expected shortfall and the parametric VaR of a book with its Euler decomposition."""

import math

import numpy as np
from numpy.typing import NDArray
from scipy.stats import norm

from trading_notes.records import Record

type Floats = NDArray[np.float64]


def normal_expected_shortfall(sigma: float, x: float = 0.99) -> float:
    """Return the expected shortfall at confidence x of a zero-mean normal with s.d. sigma."""
    y = norm.ppf(x)
    return sigma * math.exp(-(y**2) / 2) / (math.sqrt(2 * math.pi) * (1 - x))


class ParametricVaR(Record):
    """Zero-mean normal one-day VaR of money positions under a return covariance matrix.

    Attributes:
        cov: Covariance matrix of the assets' one-day returns.
        confidence: VaR confidence level.
    """

    cov: Floats
    confidence: float = 0.99

    def var(self, positions: Floats) -> float:
        """Return z_c sqrt(x' Sigma x) for money positions x."""
        return norm.ppf(self.confidence) * math.sqrt(positions @ self.cov @ positions)

    def marginal(self, positions: Floats) -> Floats:
        """Return the marginal VaR of each position, dVaR/dx_i."""
        sd = math.sqrt(positions @ self.cov @ positions)
        marginal: Floats = (self.cov @ positions) / sd * norm.ppf(self.confidence)
        return marginal

    def components(self, positions: Floats) -> Floats:
        """Return the Euler component VaRs x_i dVaR/dx_i, which sum to the VaR."""
        components: Floats = positions * self.marginal(positions)
        return components
