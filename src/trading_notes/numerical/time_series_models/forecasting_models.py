"""Autoregressive and ARCH(1) models, and tests of forecasts and coefficient stability."""

import math
from typing import Self

import numpy as np
import statsmodels.api as sm
from numpy.typing import NDArray
from scipy.optimize import minimize

from trading_notes.records import Record

type Floats = NDArray[np.float64]


class AutoRegression(Record):
    """An AR(p) model x_t = b0 + b1 x_{t-1} + ... + bp x_{t-p} + e_t, fitted by OLS.

    Attributes:
        order: p.
    """

    order: int

    def lags(self, x: Floats) -> Floats:
        """Return the regressors x_{t-1}, ..., x_{t-p} for t = p, ..., n - 1, one lag a column."""
        p = self.order
        return np.column_stack([x[p - j : len(x) - j] for j in range(1, p + 1)])

    def coefficients(self, x: Floats) -> Floats:
        """Return (b0, b1, ..., bp) fitted to the series x."""
        return sm.OLS(x[self.order :], sm.add_constant(self.lags(x))).fit().params

    def forecast_path(self, x: Floats, horizon: int) -> Floats:
        """Return the 1- to h-step forecasts from the end of x, by the recursion of the fit."""
        p = self.order
        b = self.coefficients(x)
        hist, out = list(x[-p:][::-1]), []
        for _ in range(horizon):
            f = b[0] + b[1:] @ np.array(hist[:p])
            out.append(f)
            hist.insert(0, f)
        return np.array(out)


def half_life(phi: float) -> float:
    """Return ln 0.5 / ln phi, the periods for a deviation from the mean to halve under AR(1)."""
    return float(np.log(0.5) / np.log(phi))


class Arch1(Record):
    """Conditional variance s2_t = omega + alpha e_{t-1}^2.

    Attributes:
        omega: The constant, positive.
        alpha: The ARCH coefficient, in [0, 1).
    """

    omega: float
    alpha: float

    @property
    def unconditional_variance(self) -> float:
        """Return omega / (1 - alpha)."""
        return self.omega / (1 - self.alpha)

    def next_variance(self, last_shock: float) -> float:
        """Return the one-step variance after the shock last_shock."""
        return self.omega + self.alpha * last_shock**2

    def variance_forecast(self, last_shock: float, h: int) -> float:
        """Return the h-step variance forecast, reverting to the unconditional at rate alpha."""
        uncond = self.unconditional_variance
        return uncond + self.alpha ** (h - 1) * (self.next_variance(last_shock) - uncond)

    @classmethod
    def fit(cls, shocks: Floats) -> Self:
        """Fit by Gaussian maximum likelihood with Nelder-Mead.

        The first period's variance is the sample variance of the shocks; parameters off the
        admissible region score 1e10. The search starts at half the sample variance and 0.3.
        """
        e = shocks
        n = len(e)

        def negative_log_likelihood(params: Floats) -> float:
            w, al = params
            if w <= 0 or al < 0 or al >= 1:
                return 1e10
            s2 = np.empty(n)
            s2[0] = e.var()
            s2[1:] = w + al * e[:-1] ** 2
            return float(0.5 * np.sum(np.log(s2) + e**2 / s2))

        res = minimize(
            negative_log_likelihood,
            x0=[e.var() * 0.5, 0.3],
            method="Nelder-Mead",
            options={"xatol": 1e-10, "fatol": 1e-12},
        )
        return cls(omega=float(res.x[0]), alpha=float(res.x[1]))


def chow_statistic(pooled_sse: float, split_sse: float, parameters: int, n: int) -> float:
    """Return the Chow F statistic of equal coefficients in two subsamples.

    Args:
        pooled_sse: SSE of the pooled regression.
        split_sse: Sum of the two subsample SSEs.
        parameters: Coefficients per regression, k.
        n: Observations in the pooled regression; F has (k, n - 2k) degrees of freedom.
    """
    return ((pooled_sse - split_sse) / parameters) / (split_sse / (n - 2 * parameters))


def diebold_mariano_t(loss_difference: Floats, maxlags: int) -> float:
    """Return the t statistic of a zero mean loss difference with a Newey-West variance."""
    fit = sm.OLS(loss_difference, np.ones_like(loss_difference)).fit(
        cov_type="HAC", cov_kwds={"maxlags": maxlags}
    )
    return float(fit.tvalues[0])


def compounded_change(path: Floats) -> float:
    """Return the cumulative change over a path of periodic rates, prod(1 + r) - 1."""
    return float(np.prod(1 + path) - 1)


def root_mean_square(errors: Floats) -> float:
    """Return sqrt(mean(errors^2))."""
    return math.sqrt(float(np.mean(errors**2)))
