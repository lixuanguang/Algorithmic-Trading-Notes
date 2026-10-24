"""A linear commitment model of a private-markets programme and scenario portfolio returns."""

from collections.abc import Mapping

import numpy as np
from numpy.typing import NDArray

from trading_notes.records import Record

type Floats = NDArray[np.float64]


def scenario_return(weights: Mapping[str, float], scenario: Mapping[str, float]) -> float:
    """Return a portfolio's return in a scenario of asset returns, both keyed by asset."""
    return sum(w * scenario[k] for k, w in weights.items())


class CommitmentModel(Record):
    """A Takahashi-Alexander-type linear model of a unit commitment made every period.

    The state is (NAV I, uncalled commitments K); each period
    I' = R (1 - delta) I + lambda1 K + lambda0 and K' = (1 - lambda1) K + 1 - lambda0.

    Attributes:
        new_call: lambda0, the share of a new commitment called at once.
        uncalled_call: lambda1, the share of uncalled commitments called each period.
        distribution: delta, the share of NAV distributed each period.
        gross_return: R, one plus the return earned on NAV each period.
    """

    new_call: float
    uncalled_call: float
    distribution: float
    gross_return: float

    @property
    def transition(self) -> Floats:
        """Return the 2 x 2 matrix A of x' = A x + b, x = (I, K)."""
        R, delta, lam1 = self.gross_return, self.distribution, self.uncalled_call
        return np.array([[R * (1 - delta), lam1], [0.0, 1 - lam1]])

    @property
    def inflow(self) -> Floats:
        """Return the vector b of x' = A x + b: the unit commitment's called and uncalled parts."""
        return np.array([self.new_call, 1 - self.new_call])

    def steady_state(self) -> Floats:
        """Return the steady state (I, K) = (identity - A)^-1 b."""
        return np.asarray(np.linalg.solve(np.eye(2) - self.transition, self.inflow), np.float64)
