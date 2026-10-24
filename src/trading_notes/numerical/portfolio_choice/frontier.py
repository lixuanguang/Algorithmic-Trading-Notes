"""Mean-variance utility, the minimum-variance frontier and tangency portfolios."""

import math

import numpy as np
from numpy.typing import NDArray

from trading_notes.records import Record

type Floats = NDArray[np.float64]


def mean_variance_utility(mean: float, sd: float, risk_aversion: float) -> float:
    """Return U = E(r) - A sd^2 / 2, with returns in decimals."""
    return mean - 0.5 * risk_aversion * sd * sd


class MeanVarianceFrontier(Record):
    """The unconstrained minimum-variance frontier of risky assets (Merton, 1972).

    With A = 1'S^-1 1, B = 1'S^-1 mu, C = mu'S^-1 mu and D = AC - B^2 > 0, the frontier
    variance at mean m is (A m^2 - 2 B m + C) / D.

    Attributes:
        mu: Expected returns, decimals.
        cov: Covariance matrix S, positive definite.
    """

    mu: Floats
    cov: Floats

    @property
    def inverse(self) -> Floats:
        """Return S^-1."""
        return np.asarray(np.linalg.inv(self.cov), dtype=np.float64)

    @property
    def constants(self) -> tuple[float, float, float, float]:
        """Return (A, B, C, D)."""
        one, Si = np.ones(len(self.mu)), self.inverse
        a, b, c = float(one @ Si @ one), float(one @ Si @ self.mu), float(self.mu @ Si @ self.mu)
        return a, b, c, a * c - b**2

    def global_minimum_variance(self) -> Floats:
        """Return the weights S^-1 1 / A of the global minimum-variance portfolio."""
        a = self.constants[0]
        weights: Floats = self.inverse @ np.ones(len(self.mu)) / a
        return weights

    def weights(self, m: float) -> Floats:
        """Return the frontier weights at the target mean m (short sales allowed)."""
        a, b, c, d = self.constants
        lam, gam = (c - b * m) / d, (a * m - b) / d
        weights: Floats = self.inverse @ (lam * np.ones(len(self.mu)) + gam * self.mu)
        return weights

    def variance(self, m: float) -> float:
        """Return the frontier variance at the target mean m."""
        a, b, c, d = self.constants
        return (a * m * m - 2 * b * m + c) / d

    def tangency(self, rf: float) -> Floats:
        """Return S^-1 (mu - rf 1), normalised to sum to one.

        This is the maximum-Sharpe portfolio only when rf is below the GMV mean; otherwise the
        normalisation lands on the lower branch.
        """
        z = self.inverse @ (self.mu - rf)
        weights: Floats = z / z.sum()
        return weights

    def mean(self, w: Floats) -> float:
        """Return the portfolio mean w'mu."""
        return float(w @ self.mu)

    def sd(self, w: Floats) -> float:
        """Return the portfolio standard deviation sqrt(w'S w)."""
        return math.sqrt(w @ self.cov @ w)

    def sharpe(self, w: Floats, rf: float) -> float:
        """Return (w'mu - rf) / sqrt(w'S w)."""
        return float((w @ self.mu - rf) / math.sqrt(w @ self.cov @ w))
