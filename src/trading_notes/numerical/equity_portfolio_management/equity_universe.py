"""A synthetic equity universe with a factor risk model, and active-share and turnover measures."""

import math
from typing import Final, Self

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]
type Ints = NDArray[np.int64]

N: Final = 500  # stocks
S: Final = 10  # sectors


class Universe(Record):
    """The synthetic 500-stock universe and its factor risk model.

    Attributes:
        mcap: Market capitalisations (millions), lognormal.
        sector: Each stock's sector, 0 to S - 1.
        value: Each stock's value score (high = cheap).
        w_cap: Cap weights, the index.
        B: Factor loadings: market beta, the sector dummies and the value score.
        F: The annual factor covariance.
        idio: Idiosyncratic volatilities.
        cov: The model covariance of returns.
    """

    mcap: Floats
    sector: Ints
    value: Floats
    w_cap: Floats
    B: Floats
    F: Floats
    idio: Floats
    cov: Floats

    @classmethod
    def simulate(cls, rng: np.random.Generator) -> Self:
        """Draw the universe: capitalisations, sectors, value scores, betas and specific risk."""
        mcap = np.exp(rng.normal(9.0, 1.2, N))  # market capitalisations (millions), lognormal
        sector = rng.integers(0, S, N)
        value = rng.standard_normal(N)  # value score (high = cheap)
        w_cap = mcap / mcap.sum()
        # factor model (annual): market beta ~1, sector factors, value factor, idiosyncratic
        beta = 1 + 0.2 * rng.standard_normal(N)
        B = np.zeros((N, S + 2))
        B[:, 0] = beta
        B[np.arange(N), 1 + sector] = 1.0
        B[:, S + 1] = value
        F = np.diag([0.16**2] + [0.06**2] * S + [0.04**2])
        idio = (0.20 + 0.15 * rng.random(N)) * np.where(w_cap > np.quantile(w_cap, 0.8), 0.8, 1.0)
        cov = B @ F @ B.T + np.diag(idio**2)
        return cls(mcap=mcap, sector=sector, value=value, w_cap=w_cap, B=B, F=F, idio=idio, cov=cov)

    def tracking_error(self, w: Floats) -> float:
        """Return the model tracking error of weights w against the cap-weighted index."""
        a = w - self.w_cap
        return math.sqrt(a @ self.cov @ a)


def active_share(w: Floats, b: Floats) -> np.float64:
    """Return Active Share, half the sum of absolute weight differences from the benchmark b."""
    share: np.float64 = 0.5 * np.abs(w - b).sum()
    return share


def turnover_after(w: Floats, ret: Floats) -> np.float64:
    """Return the one-way turnover of trading weights w back after they drift with ret."""
    drift = w * (1 + ret)
    drift /= drift.sum()
    turnover: np.float64 = 0.5 * np.abs(drift - w).sum()
    return turnover
