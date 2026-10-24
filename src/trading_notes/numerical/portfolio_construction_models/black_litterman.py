"""The Black-Litterman posterior mean of expected returns given equilibrium returns and views."""

from collections.abc import Sequence
from typing import Self

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]


class BlackLitterman(Record):
    """A market with equilibrium returns and linear views on expected returns.

    E[R] ~ N(pi, tau Sigma) a priori; the views say P E[R] = Q + eps, eps ~ N(0, Omega).

    Attributes:
        sigma: Covariance matrix Sigma of returns, n x n.
        pi: Equilibrium excess returns, length n.
        p: View matrix P, k x n.
        q: View returns Q, length k.
        tau: Scale of the uncertainty of E[R] relative to Sigma.
    """

    sigma: Floats
    pi: Floats
    p: Floats
    q: Floats
    tau: float

    @classmethod
    def from_market_weights(
        cls,
        sigma: Floats,
        weights: Sequence[float],
        risk_aversion: float,
        p: Floats,
        view_excess: Floats,
        tau: float,
    ) -> Self:
        """Return the model with pi = delta Sigma w and views stated relative to pi.

        Args:
            sigma: Covariance matrix, n x n.
            weights: Market-capitalisation weights, length n.
            risk_aversion: delta.
            p: View matrix, k x n.
            view_excess: How far each view's return lies above its equilibrium value P pi.
            tau: Scale of the prior uncertainty.
        """
        pi = risk_aversion * sigma @ np.array(weights)
        return cls(sigma=sigma, pi=pi, p=p, q=p @ pi + view_excess, tau=tau)

    def posterior_mean(self, omega: Floats) -> Floats:
        """Return the posterior mean in the precision form of Black and Litterman (1991).

        Ebar = [(tau Sigma)^-1 + P' Omega^-1 P]^-1 [(tau Sigma)^-1 pi + P' Omega^-1 Q].

        Args:
            omega: View covariance Omega, k x k.
        """
        a = np.linalg.inv(self.tau * self.sigma) + self.p.T @ np.linalg.inv(omega) @ self.p
        b = (
            np.linalg.inv(self.tau * self.sigma) @ self.pi
            + self.p.T @ np.linalg.inv(omega) @ self.q
        )
        return np.asarray(np.linalg.solve(a, b), dtype=np.float64)
