"""OLS with Newey-West standard errors, as the research workflows' inference uses it."""

from typing import Self

import numpy as np
from numpy.typing import NDArray

from trading_notes.records import Record

type Floats = NDArray[np.float64]


class NeweyWestOls(Record):
    """An OLS fit of y on a constant and the columns of X, with Bartlett-weighted HAC errors.

    Attributes:
        coefficients: The constant first, then one per column of X.
        t_stats: Each coefficient over its Newey-West standard error.
    """

    coefficients: Floats
    t_stats: Floats

    @classmethod
    def fit(cls, y: Floats, X: Floats, lags: int = 12) -> Self:
        """Return the fit, its long-run covariance over `lags` lags with weights 1 - L/(lags+1).

        Args:
            y: The outcomes, in time order.
            X: The regressors, one row per outcome (a vector for one regressor, or no columns).
            lags: The Bartlett truncation lag.
        """
        A = np.column_stack([np.ones(len(y)), X])
        b = np.asarray(np.linalg.lstsq(A, y, rcond=None)[0], dtype=np.float64)
        e = y - A @ b
        S = (A * e[:, None]).T @ (A * e[:, None])
        for L in range(1, lags + 1):
            w = 1 - L / (lags + 1)
            G = (A[L:] * e[L:, None]).T @ (A[:-L] * e[:-L, None])
            S += w * (G + G.T)
        AtAi = np.linalg.inv(A.T @ A)
        V = AtAi @ S @ AtAi
        return cls(coefficients=b, t_stats=np.asarray(b / np.sqrt(np.diag(V)), dtype=np.float64))
