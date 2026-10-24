"""Tail estimation: the Hill estimator, generalised Pareto fits and peaks-over-threshold risk."""

import math
from typing import Self

import numpy as np
from numpy.typing import NDArray
from scipy import optimize, stats

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]


def hill_estimate(x: Floats, k: int) -> float:
    """Return H_k = (1/k) sum ln X_(n-i+1) - ln X_(n-k), the threshold the (k+1)-th largest."""
    top = np.sort(np.partition(x, -(k + 1))[-(k + 1) :])
    return float(np.mean(np.log(top[1:])) - math.log(top[0]))


def student_t_expected_shortfall(q: float, nu: int) -> float:
    """Return the expected shortfall of the standard Student t distribution at level q."""
    x = stats.t.ppf(q, nu)
    return float((nu + x**2) / (nu - 1) * stats.t.pdf(x, nu) / (1 - q))


def _negative_log_likelihood(xi: float, beta: float, y: Floats) -> float:
    if beta <= 0 or np.any(1 + xi * y / beta <= 0):
        return math.inf
    return len(y) * math.log(beta) + (1 + 1 / xi) * float(np.sum(np.log1p(xi * y / beta)))


def _score(xi: float, beta: float, y: Floats) -> Floats:
    z = 1 + xi * y / beta
    d_xi = float(np.sum(np.log(z) / xi**2 - (1 + 1 / xi) * (y / beta) / z))
    d_beta = float(-len(y) / beta + (1 + 1 / xi) * np.sum(xi * y / beta**2 / z))
    return np.array([d_xi, d_beta])


class GeneralisedPareto(Record):
    """The generalised Pareto distribution of excesses over a threshold.

    Attributes:
        shape: xi.
        scale: beta, positive.
    """

    shape: float
    scale: float

    def negative_log_likelihood(self, y: Floats) -> float:
        """Return the negative log-likelihood of the excesses y; infinite off the support."""
        return _negative_log_likelihood(self.shape, self.scale, y)

    def score(self, y: Floats) -> Floats:
        """Return the gradient of the log-likelihood in (xi, beta) (QRM eq. (7.14))."""
        return _score(self.shape, self.scale, y)

    @classmethod
    def fit(cls, y: Floats, start: tuple[float, float | None] = (0.2, None)) -> Self:
        """Fit by maximum likelihood: Nelder-Mead, polished by Newton steps on the score.

        Args:
            y: The excesses.
            start: Starting (xi, beta); a missing beta starts at the mean excess.
        """
        b0 = start[1] or float(np.mean(y))

        def objective(params: Floats) -> float:
            return _negative_log_likelihood(params[0], params[1], y)

        res = optimize.minimize(
            objective,
            x0=[start[0], b0],
            method="Nelder-Mead",
            options={"xatol": 1e-12, "fatol": 1e-12, "maxiter": 20_000},
        )
        p: Floats = res.x.copy()
        for _ in range(50):
            g = _score(p[0], p[1], y)
            h = 1e-6 * np.maximum(np.abs(p), 1e-3)
            H = np.empty((2, 2))
            for j in range(2):
                e = np.zeros(2)
                e[j] = h[j]
                pe, pm = p + e, p - e
                H[:, j] = (_score(pe[0], pe[1], y) - _score(pm[0], pm[1], y)) / (2 * h[j])
            step = np.linalg.solve(H, g)
            p = p - step
            if np.max(np.abs(step)) < 1e-14:
                break
        return cls(shape=float(p[0]), scale=float(p[1]))


class PeaksOverThreshold(Record):
    """Tail risk from a generalised Pareto fit to the excesses over a threshold.

    The formulas are Hull's RMFI eqs. (12.9)-(12.10) and QRM eqs. (7.18)-(7.19).

    Attributes:
        threshold: u.
        tail_fraction: The share of observations above u.
        excesses: The GPD of the excesses over u; its shape must be below 1 for a finite ES.
    """

    threshold: float
    tail_fraction: float
    excesses: GeneralisedPareto

    def var(self, q: float) -> float:
        """Return VaR at level q."""
        xi, beta = self.excesses.shape, self.excesses.scale
        var: float = self.threshold + beta / xi * (((1 - q) / self.tail_fraction) ** (-xi) - 1)
        return var

    def es(self, var: float) -> float:
        """Return the expected shortfall at the level whose VaR is var."""
        xi, beta = self.excesses.shape, self.excesses.scale
        es: float = (var + beta - xi * self.threshold) / (1 - xi)
        return es
