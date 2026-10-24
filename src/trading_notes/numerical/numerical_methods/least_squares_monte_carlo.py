"""Longstaff-Schwartz least-squares Monte Carlo for a put exercisable on a set of dates."""

from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray

from trading_notes.records import Record

type Floats = NDArray[np.float64]
type Basis = Callable[[Floats], Floats]


def quadratic_basis(s: Floats) -> Floats:
    """Return the regressors 1, S, S^2."""
    return np.column_stack([np.ones_like(s), s, s**2])


class LongstaffSchwartz(Record):
    """Exercise policy by regressing continuation values of in-the-money paths on a basis.

    Paths are rows of prices on the exercise dates dt, 2 dt, ...; the last date is maturity.

    Attributes:
        strike: K.
        rate: Continuously compounded discount rate.
        dt: Time between exercise dates.
        basis: Maps prices to the regressors of the continuation value.
    """

    strike: float
    rate: float
    dt: float
    basis: Basis

    def fit(self, paths: Floats) -> tuple[Floats, dict[int, Floats]]:
        """Return each path's discounted cash flow and the policy fitted on the same paths.

        Returns:
            The cash flows, and the regression coefficients by date index.
        """
        return self._backward(paths, None)

    def value(self, paths: Floats, policy: dict[int, Floats]) -> Floats:
        """Return each path's discounted cash flow under a policy fitted elsewhere."""
        return self._backward(paths, policy)[0]

    def _backward(
        self, paths: Floats, policy: dict[int, Floats] | None
    ) -> tuple[Floats, dict[int, Floats]]:
        """Walk back from maturity, fitting (policy None) or applying the regressions."""
        strike, rate, dt = self.strike, self.rate, self.dt
        n_paths, n_dates = paths.shape
        cash = np.maximum(strike - paths[:, -1], 0.0)
        when = np.full(n_paths, n_dates - 1)
        fitted = {}
        for t in range(n_dates - 2, -1, -1):
            itm = strike - paths[:, t] > 0
            if not itm.any():
                continue
            X = self.basis(paths[itm, t])
            y = cash[itm] * np.exp(-rate * dt * (when[itm] - t))
            beta = np.linalg.lstsq(X, y, rcond=None)[0] if policy is None else policy[t]
            fitted[t] = beta
            ex_now = strike - paths[itm, t] >= X @ beta
            idx = np.where(itm)[0][ex_now]
            cash[idx], when[idx] = strike - paths[idx, t], t
        return cash * np.exp(-rate * dt * (when + 1)), fitted
