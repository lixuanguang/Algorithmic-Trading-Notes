"""Proper scoring rules for normal, interval and quantile forecasts, and a quadrature CRPS."""

from collections.abc import Callable
from typing import overload

import numpy as np
from numpy.typing import NDArray
from scipy import integrate, stats

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]


@overload
def _shaped(x: float, value: float | Floats) -> float: ...
@overload
def _shaped(x: Floats, value: float | Floats) -> Floats: ...
def _shaped(x: float | Floats, value: float | Floats) -> float | Floats:
    """Return value as a float for a scalar outcome x, else as a float array of x's shape."""
    if isinstance(x, np.ndarray):
        return np.asarray(value, dtype=np.float64)
    return float(value)


class QuantileForecast[T: (float, Floats)](Record):
    """A forecast of the tau-quantile of the outcome; arrays score elementwise.

    Attributes:
        value: The forecast quantile r.
        level: tau, in (0, 1).
    """

    value: T
    level: float

    def score(self, x: T) -> T:
        """Return the quantile score (1{x <= r} - tau)(r - x) at the outcome x."""
        r, tau = self.value, self.level
        return _shaped(x, ((x <= r) - tau) * (r - x))


class CentralInterval[T: (float, Floats)](Record):
    """A central (1 - alpha) prediction interval [lower, upper]; arrays score elementwise.

    Attributes:
        lower: The alpha/2 quantile.
        upper: The 1 - alpha/2 quantile.
        alpha: The nominal miss rate.
    """

    lower: T
    upper: T
    alpha: float

    def score(self, x: T) -> T:
        """Return the interval score of Gneiting and Raftery's eq. (43) at the outcome x."""
        lo, hi, alpha = self.lower, self.upper, self.alpha
        return _shaped(
            x, (hi - lo) + (2 / alpha) * (lo - x) * (x < lo) + (2 / alpha) * (x - hi) * (x > hi)
        )

    def quantiles(self) -> tuple[QuantileForecast[T], QuantileForecast[T]]:
        """Return the two quantile forecasts whose scores, times 2/alpha, sum to this score."""
        return (
            QuantileForecast(value=self.lower, level=self.alpha / 2),
            QuantileForecast(value=self.upper, level=1 - self.alpha / 2),
        )


class NormalForecast[T: (float, Floats)](Record):
    """The predictive distribution N(mean, sd^2); arrays hold one forecast per element.

    Attributes:
        mean: The forecast mean.
        sd: The forecast standard deviation, positive.
    """

    mean: T
    sd: T

    def log_score(self, x: T) -> T:
        """Return the log score -log f(x)."""
        return _shaped(x, -stats.norm.logpdf(x, self.mean, self.sd))

    def crps(self, x: T) -> T:
        """Return the closed-form continuous ranked probability score at x."""
        z = (x - self.mean) / self.sd
        return _shaped(
            x,
            self.sd
            * (z * (2 * stats.norm.cdf(z) - 1) + 2 * stats.norm.pdf(z) - 1 / np.sqrt(np.pi)),
        )

    def central_interval(self, alpha: float) -> CentralInterval[T]:
        """Return the central (1 - alpha) interval mean -/+ sd z_{1 - alpha/2}."""
        return CentralInterval(
            lower=_shaped(self.mean, self.mean + self.sd * stats.norm.ppf(alpha / 2)),
            upper=_shaped(self.mean, self.mean + self.sd * stats.norm.ppf(1 - alpha / 2)),
            alpha=alpha,
        )


def crps_quadrature(cdf: Callable[[float], float], x: float) -> float:
    """Return the CRPS as the threshold integral of (F(u) - 1{u >= x})^2 (Gneiting-Raftery (20)).

    An independent reference for any closed form: it sees only the cumulative distribution.
    """
    left = integrate.quad(lambda u: cdf(u) ** 2, -np.inf, x, epsabs=1e-12, epsrel=1e-12, limit=200)[
        0
    ]
    right = integrate.quad(
        lambda u: (1 - cdf(u)) ** 2, x, np.inf, epsabs=1e-12, epsrel=1e-12, limit=200
    )[0]
    return left + right
