"""Population moments of asset and portfolio returns under discrete scenarios."""

import numpy as np
from numpy.typing import NDArray

from trading_notes.records import Record

type Floats = NDArray[np.float64]


class ScenarioModel(Record):
    """Asset returns in a finite set of states with known probabilities.

    Attributes:
        probabilities: Probability of each state; they sum to one.
        returns: Returns, one row per state and one column per asset.
    """

    probabilities: Floats
    returns: Floats

    @property
    def mean(self) -> Floats:
        """Return the expected return of each asset."""
        mean: Floats = self.probabilities @ self.returns
        return mean

    @property
    def covariance(self) -> Floats:
        """Return the population covariance matrix of the asset returns."""
        dev = self.returns - self.mean
        cov: Floats = (self.probabilities[:, None] * dev).T @ dev
        return cov


def equicorrelation(n: int, r: float) -> Floats:
    """Return the n x n correlation matrix with every off-diagonal entry equal to r."""
    C = np.full((n, n), r)
    np.fill_diagonal(C, 1.0)
    return C
