"""Ledoit and Wolf's shrinkage toward constant correlation, and the Marchenko-Pastur noise band."""

from typing import Self

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]


class ShrunkCovariance(Record):
    """A sample covariance shrunk toward the constant-correlation target.

    Attributes:
        shrunk: delta F + (1 - delta) S.
        sample: S, the sample covariance with divisor T.
        intensity: delta = max(0, min(kappa / T, 1)), kappa = (pi - rho) / gamma.
    """

    shrunk: Floats
    sample: Floats
    intensity: float

    @classmethod
    def fit(cls, Y: Floats) -> Self:
        """Return the estimate of Ledoit and Wolf (2003, App. A-B, eqs. (3)-(5)), as printed.

        Args:
            Y: A T x N sample of returns.
        """
        T, N = Y.shape
        X = Y - Y.mean(0)
        S = X.T @ X / T
        s = np.sqrt(np.diag(S))
        R = S / np.outer(s, s)
        rbar = (R.sum() - N) / (N * (N - 1))
        F = rbar * np.outer(s, s)
        np.fill_diagonal(F, np.diag(S))
        Z = X[:, :, None] * X[:, None, :] - S  # T x N x N
        pi_mat = (Z**2).mean(0)
        pi = pi_mat.sum()
        D = X**2 - np.diag(S)  # T x N
        th_ii = np.einsum("ti,tij->ij", D, Z) / T  # theta_{ii,ij}
        th_jj = np.einsum("tj,tij->ij", D, Z) / T  # theta_{jj,ij}
        off = (rbar / 2) * (
            np.sqrt(np.outer(1 / s**2, s**2)) * th_ii + np.sqrt(np.outer(s**2, 1 / s**2)) * th_jj
        )
        np.fill_diagonal(off, 0)
        rho = np.trace(pi_mat) + off.sum()
        gamma = ((F - S) ** 2).sum()
        delta = max(0.0, min((pi - rho) / gamma / T, 1.0))
        return cls(shrunk=delta * F + (1 - delta) * S, sample=S, intensity=delta)


class NoiseBand(Record):
    """The Marchenko-Pastur support of correlation eigenvalues of T x N unit-variance noise.

    Attributes:
        assets: N.
        observations: T.
    """

    assets: int
    observations: int

    @property
    def lower(self) -> float:
        """Return (1 - Q^-1/2)^2, Q = T / N."""
        return float((1 - (self.observations / self.assets) ** -0.5) ** 2)

    @property
    def upper(self) -> float:
        """Return (1 + Q^-1/2)^2, Q = T / N."""
        return float((1 + (self.observations / self.assets) ** -0.5) ** 2)
