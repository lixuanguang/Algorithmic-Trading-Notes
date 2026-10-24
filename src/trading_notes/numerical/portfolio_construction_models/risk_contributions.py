"""Portfolio volatility, risk contributions and the equal-risk-contribution portfolio."""

import math
from collections.abc import Sequence
from typing import Self

import numpy as np
from numpy.typing import NDArray

from trading_notes.records import Record

type Floats = NDArray[np.float64]


class CovarianceModel(Record):
    """An asset covariance matrix and the portfolio risk quantities it implies.

    Weight vectors have one entry per asset; none of the methods changes its arguments.

    Attributes:
        sigma: Covariance matrix, n x n.
    """

    sigma: Floats

    @classmethod
    def from_volatilities(cls, vols: Sequence[float], correlations: Floats) -> Self:
        """Return the model with covariance D C D for volatilities D and correlation matrix C."""
        v = np.array(vols)
        return cls(sigma=np.outer(v, v) * correlations)

    def volatility(self, w: Floats) -> float:
        """Return the portfolio volatility sqrt(w' Sigma w)."""
        return float(np.sqrt(w @ self.sigma @ w))

    def risk_contributions(self, w: Floats) -> Floats:
        """Return each asset's contribution w_i (Sigma w)_i / sigma(w); they sum to sigma(w)."""
        contributions: Floats = w * (self.sigma @ w) / self.volatility(w)
        return contributions

    def variance_shares(self, w: Floats) -> Floats:
        """Return each asset's share w_i (Sigma w)_i / w' Sigma w of the portfolio variance."""
        shares: Floats = w * (self.sigma @ w) / (w @ self.sigma @ w)
        return shares

    def betas(self, w: Floats) -> Floats:
        """Return each asset's beta (Sigma w)_i / w' Sigma w against the portfolio."""
        betas: Floats = (self.sigma @ w) / (w @ self.sigma @ w)
        return betas

    def sharpe(self, w: Floats, excess: Floats) -> float:
        """Return the Sharpe ratio w' excess / sqrt(w' Sigma w)."""
        return float(w @ excess / math.sqrt(w @ self.sigma @ w))

    def tangency(self, excess: Floats) -> Floats:
        """Return the maximum-Sharpe weights Sigma^-1 excess, normalised to sum to one."""
        w = np.linalg.solve(self.sigma, excess)
        return np.asarray(w / w.sum(), dtype=np.float64)

    def equal_risk_contribution(self, iters: int = 20000) -> Floats:
        """Return the long-only ERC weights by a fixed-point iteration on y_i = 1 / (Sigma y)_i.

        Each step is the geometric move y <- sqrt(y / (Sigma y)); the weights are y normalised.
        """
        y: Floats = np.ones(len(self.sigma))
        for _ in range(iters):
            y = np.sqrt(y / (self.sigma @ y))
        weights: Floats = y / y.sum()
        return weights

    def long_only_minimum_variance(self, iters: int = 200000, lr: float = 0.5) -> Floats:
        """Return the long-only minimum-variance weights by projected gradient descent.

        Args:
            iters: Number of gradient steps, each followed by a projection onto the simplex.
            lr: Step size.
        """
        n = len(self.sigma)
        x = np.ones(n) / n
        for _ in range(iters):
            x = project_to_simplex(x - lr * (self.sigma @ x))
        return x


def inverse_volatility(vols: Floats) -> Floats:
    """Return weights proportional to 1 / volatility, summing to one."""
    weights: Floats = (1 / vols) / (1 / vols).sum()
    return weights


def project_to_simplex(x: Floats) -> Floats:
    """Return the Euclidean projection of x onto the simplex {w >= 0, sum w = 1}, as a new array."""
    n = len(x)
    u = np.sort(x)[::-1]
    css = np.cumsum(u)
    rho = np.nonzero(u * np.arange(1, n + 1) > (css - 1))[0][-1]
    projected: Floats = np.maximum(x - (css[rho] - 1) / (rho + 1), 0)
    return projected
