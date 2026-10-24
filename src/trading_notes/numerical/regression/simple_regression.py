"""Simple linear regression by its closed forms: estimates, sums of squares, tests and intervals."""

import math

import numpy as np
from numpy.typing import NDArray
from scipy import stats

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]


class SimpleRegression(Record):
    """The least-squares line y = b0 + b1 x and its classical inference with n - 2 d.f.

    Attributes:
        x: The regressor.
        y: The response.
    """

    x: Floats
    y: Floats

    @property
    def n(self) -> int:
        """Return the number of observations."""
        return len(self.x)

    @property
    def x_mean(self) -> float:
        """Return the mean of x."""
        return float(self.x.mean())

    @property
    def y_mean(self) -> float:
        """Return the mean of y."""
        return float(self.y.mean())

    @property
    def sxx(self) -> float:
        """Return the sum of squared deviations of x from its mean."""
        return float(((self.x - self.x_mean) ** 2).sum())

    @property
    def sxy(self) -> float:
        """Return the sum of cross-products of the deviations of x and y."""
        return float(((self.x - self.x_mean) * (self.y - self.y_mean)).sum())

    @property
    def slope(self) -> float:
        """Return b1 = Sxy / Sxx."""
        return self.sxy / self.sxx

    @property
    def intercept(self) -> float:
        """Return b0 = mean(y) - b1 mean(x)."""
        return self.y_mean - self.slope * self.x_mean

    def predict(self, x: float) -> float:
        """Return the fitted value b0 + b1 x."""
        return self.intercept + self.slope * x

    def fitted(self) -> Floats:
        """Return the fitted values at the sample's x."""
        fit: Floats = self.intercept + self.slope * self.x
        return fit

    def residuals(self) -> Floats:
        """Return y less the fitted values."""
        e: Floats = self.y - self.fitted()
        return e

    @property
    def sse(self) -> float:
        """Return the residual sum of squares."""
        return float((self.residuals() ** 2).sum())

    @property
    def ssr(self) -> float:
        """Return the regression sum of squares."""
        return float(((self.fitted() - self.y_mean) ** 2).sum())

    @property
    def sst(self) -> float:
        """Return the total sum of squares."""
        return float(((self.y - self.y_mean) ** 2).sum())

    @property
    def standard_error(self) -> float:
        """Return the standard error of estimate s = sqrt(SSE / (n - 2))."""
        return math.sqrt(self.sse / (self.n - 2))

    @property
    def r_squared(self) -> float:
        """Return R^2 = SSR / SST."""
        return self.ssr / self.sst

    @property
    def slope_se(self) -> float:
        """Return se(b1) = s / sqrt(Sxx)."""
        return self.standard_error / math.sqrt(self.sxx)

    @property
    def intercept_se(self) -> float:
        """Return se(b0) = s sqrt(1/n + mean(x)^2 / Sxx)."""
        return self.standard_error * math.sqrt(1 / self.n + self.x_mean**2 / self.sxx)

    def slope_t(self, null: float = 0.0) -> float:
        """Return the t statistic of the slope against the null value."""
        return (self.slope - null) / self.slope_se

    def two_sided_p(self, t: float) -> float:
        """Return the two-sided p-value of a t statistic on n - 2 d.f."""
        return float(2 * stats.t.sf(abs(t), self.n - 2))

    def f_statistic(self) -> float:
        """Return the ANOVA F = MSR / MSE on (1, n - 2) d.f."""
        return (self.ssr / 1) / (self.sse / (self.n - 2))

    def mean_response_se(self, x: float) -> float:
        """Return the standard error of the fitted mean at x."""
        return self.standard_error * math.sqrt(1 / self.n + (x - self.x_mean) ** 2 / self.sxx)

    def prediction_se(self, x: float) -> float:
        """Return the standard error of a new observation's prediction at x."""
        return self.standard_error * math.sqrt(1 + 1 / self.n + (x - self.x_mean) ** 2 / self.sxx)
