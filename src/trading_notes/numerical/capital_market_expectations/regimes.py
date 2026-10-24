"""A two-state Markov regime chain's returns, and the ARCH(1) variance update."""

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]


class RegimeChain(Record):
    """A monthly Markov chain of expansion (state 0) and contraction (state 1).

    Attributes:
        transitions: The monthly transition matrix, rows summing to one.
        returns: Each state's monthly log return.
    """

    transitions: Floats
    returns: Floats

    def stationary(self) -> Floats:
        """Return the stationary distribution, solving pi (P - I) = 0 with sum(pi) = 1."""
        P = self.transitions
        n = len(P)
        pi: Floats = np.linalg.lstsq(
            np.vstack([P.T - np.eye(n), np.ones(n)]), np.r_[np.zeros(n), 1.0], rcond=None
        )[0]
        return pi

    def horizon_return(self, months: int, start: int = 1) -> float:
        """Return the expected cumulative log return over `months`, starting in state `start`.

        The first month earns the starting state's return; the chain moves after each month.
        """
        state = np.eye(len(self.transitions))[start]
        total = 0.0
        for _ in range(months):
            total += state @ self.returns
            state = state @ self.transitions
        return total

    def expected_wealth(self, months: int, start: int = 1) -> float:
        """Return E[exp(cumulative log return)] over `months` from `start`, by matrix products."""
        D = np.diag(np.exp(self.returns))
        P = self.transitions
        n = len(P)
        return float(np.eye(n)[start] @ D @ np.linalg.matrix_power(P @ D, months - 1) @ np.ones(n))


class ArchVariance(Record):
    """sigma^2_t = gamma + alpha sigma^2_{t-1} + beta eps^2_{t-1} (PMiP eq. 17).

    Attributes:
        gamma: The constant.
        persistence: alpha, the weight on the previous variance.
        shock: beta, the weight on the squared surprise.
    """

    gamma: float
    persistence: float
    shock: float

    def long_run(self) -> float:
        """Return gamma / (1 - alpha - beta)."""
        return self.gamma / (1 - self.persistence - self.shock)

    def update(self, previous: float, surprise: float) -> float:
        """Return the next variance after a surprise."""
        return self.gamma + self.persistence * previous + self.shock * surprise**2
