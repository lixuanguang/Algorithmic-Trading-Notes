"""Least squares by the normal equations, its variance under AR(1) errors, and a logistic fit."""

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]


class LeastSquares(Record):
    """Ordinary least squares of a response on a design whose first column is a constant.

    Attributes:
        design: X, observations by (1 + k) regressors.
        response: y.
    """

    design: Floats
    response: Floats

    @property
    def n(self) -> int:
        """Return the number of observations."""
        return len(self.response)

    @property
    def k(self) -> int:
        """Return the number of slope regressors, excluding the constant."""
        return int(self.design.shape[1]) - 1

    def coefficients(self) -> Floats:
        """Return b solving the normal equations X'X b = X'y."""
        X, y = self.design, self.response
        return np.asarray(np.linalg.solve(X.T @ X, X.T @ y), dtype=np.float64)

    def fitted(self) -> Floats:
        """Return Xb."""
        fit: Floats = self.design @ self.coefficients()
        return fit

    def residuals(self) -> Floats:
        """Return y - Xb."""
        e: Floats = self.response - self.design @ self.coefficients()
        return e

    @property
    def sst(self) -> float:
        """Return the total sum of squares about the mean of y."""
        return float(((self.response - self.response.mean()) ** 2).sum())

    @property
    def sse(self) -> float:
        """Return the residual sum of squares."""
        return float((self.residuals() ** 2).sum())

    @property
    def r_squared(self) -> float:
        """Return R^2 = (SST - SSE) / SST."""
        return (self.sst - self.sse) / self.sst

    @property
    def adjusted_r_squared(self) -> float:
        """Return 1 - (1 - R^2)(n - 1)/(n - k - 1)."""
        return 1 - (1 - self.r_squared) * (self.n - 1) / (self.n - self.k - 1)

    @property
    def f_statistic(self) -> float:
        """Return the ANOVA F = (SSR / k) / (SSE / (n - k - 1))."""
        return ((self.sst - self.sse) / self.k) / (self.sse / (self.n - self.k - 1))

    @property
    def standard_error(self) -> float:
        """Return the standard error of estimate sqrt(SSE / (n - k - 1))."""
        return float(np.sqrt(self.sse / (self.n - self.k - 1)))

    def inverse_cross_product(self) -> Floats:
        """Return (X'X)^-1."""
        return np.asarray(np.linalg.inv(self.design.T @ self.design), dtype=np.float64)

    def leverage(self) -> Floats:
        """Return the diagonal of the hat matrix X (X'X)^-1 X'."""
        X = self.design
        hat: Floats = X @ self.inverse_cross_product() @ X.T
        return np.diag(hat)

    def mean_prediction_se(self, x0: Floats) -> float:
        """Return the standard error of the fitted mean at the regressor row x0."""
        return float(self.standard_error * np.sqrt(x0 @ self.inverse_cross_product() @ x0))

    def new_prediction_se(self, x0: Floats) -> float:
        """Return the standard error of a new observation's prediction at x0."""
        return float(self.standard_error * np.sqrt(1 + x0 @ self.inverse_cross_product() @ x0))


def ar1_ols_variance_ratio(x: Floats, rho: float) -> float:
    """Return the true over the expected usual variance of the OLS slope, with AR(1) errors.

    The regression has an intercept and the regressor x. With error covariance Omega,
    Var(b | X) = (X'X)^-1 X' Omega X (X'X)^-1, while the usual estimate has expectation
    E(s^2) (X'X)^-1 with E(s^2) = tr(M Omega) / (n - 2), M the residual maker. Errors have unit
    innovation variance, so Omega_ij = rho^|i - j| / (1 - rho^2).
    """
    m = len(x)
    Xd = np.column_stack([np.ones(m), x])
    idx = np.arange(m)
    om = rho ** np.abs(idx[:, None] - idx[None, :]) / (1 - rho**2)
    xtxi = np.linalg.inv(Xd.T @ Xd)
    true_var = (xtxi @ Xd.T @ om @ Xd @ xtxi)[1, 1]
    resid_maker = np.eye(m) - Xd @ xtxi @ Xd.T
    usual = np.trace(resid_maker @ om) / (m - 2) * xtxi[1, 1]
    return float(true_var / usual)


def newton_logit(X: Floats, y: Floats, iterations: int = 50) -> Floats:
    """Return the logistic regression coefficients by Newton-Raphson from zero.

    Args:
        X: The design, with a constant column.
        y: Outcomes, 0 or 1.
        iterations: Newton steps taken; each solves the weighted normal equations.
    """
    beta = np.zeros(X.shape[1])
    for _ in range(iterations):
        p_hat = 1 / (1 + np.exp(-X @ beta))
        W = p_hat * (1 - p_hat)
        beta = beta + np.linalg.solve(X.T @ (X * W[:, None]), X.T @ (y - p_hat))
    return beta
