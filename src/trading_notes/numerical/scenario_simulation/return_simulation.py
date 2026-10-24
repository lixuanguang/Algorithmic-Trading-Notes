"""Multi-year wealth from bootstrapped history or from a fitted normal model of asset returns."""

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]


def compounded_wealth(returns: Floats) -> Floats:
    """Return the wealth per 1 invested over each path of periodic returns, paths x periods."""
    wealth: Floats = np.prod(1 + returns, axis=1)
    return wealth


class NormalReturns(Record):
    """Asset returns mean + L z, where L L' is the covariance and z is standard normal.

    Reusing the same z across models gives common random numbers, so the difference between two
    models' outcomes is a sensitivity, not simulation noise.

    Attributes:
        mean: Mean return of each asset per period.
        covariance: Covariance of the assets' returns per period.
    """

    mean: Floats
    covariance: Floats

    def simulate(self, z: Floats) -> Floats:
        """Return returns for standard normal shocks z of shape (..., assets)."""
        returns: Floats = self.mean + z @ np.linalg.cholesky(self.covariance).T
        return returns
