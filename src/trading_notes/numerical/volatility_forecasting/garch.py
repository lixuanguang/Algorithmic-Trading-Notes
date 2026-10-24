"""GARCH(1,1) variance forecasts and their RiskMetrics (EWMA) special case."""

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]


class GarchSeries(Record):
    """One simulated GARCH(1,1) series.

    Attributes:
        returns: R_t.
        variances: sigma2_t, the variance R_t was drawn with, known at t - 1.
    """

    returns: Floats
    variances: Floats


class Garch11(Record):
    """sigma2_{t+1} = omega + alpha R_t^2 + beta sigma2_t, with Gaussian shocks.

    Attributes:
        omega: The constant.
        alpha: The weight of the squared return.
        beta: The weight of the previous variance.
    """

    omega: float
    alpha: float
    beta: float

    @property
    def long_run(self) -> float:
        """Return the long-run variance omega / (1 - alpha - beta)."""
        return self.omega / (1 - self.alpha - self.beta)

    def k_step_forecast(self, s2_next: float, k: int) -> float:
        """Return E_t[sigma2_{t+k}] = sigma2 + (alpha + beta)^(k-1) (sigma2_{t+1} - sigma2)."""
        return self.long_run + (self.alpha + self.beta) ** (k - 1) * (s2_next - self.long_run)

    def cumulative_forecast(self, s2: float, h: int) -> float:
        """Return the forecast of sum R_t^2 over days t..t+h-1, given sigma2_t = s2."""
        lr = self.long_run
        return float(sum(lr + (self.alpha + self.beta) ** j * (s2 - lr) for j in range(h)))

    def monte_carlo_forecast(
        self, rng: np.random.Generator, s2_next: float, k: int, paths: int
    ) -> float:
        """Return the mean of sigma2_{t+k} over simulated paths started at sigma2_{t+1} = s2_next.

        Each of the k - 1 steps draws one vector of `paths` shocks; no closed form is used.
        """
        s2 = np.full(paths, s2_next)
        for _ in range(k - 1):
            R = np.sqrt(s2) * rng.standard_normal(paths)
            s2 = self.omega + self.alpha * R**2 + self.beta * s2
        return float(s2.mean())

    def simulate(self, rng: np.random.Generator, n: int) -> GarchSeries:
        """Simulate n days from sigma2_0 = sigma2, drawing one scalar shock per day in order."""
        R = np.empty(n)
        s2 = np.empty(n)
        s2[0] = self.long_run
        for t in range(n):
            R[t] = np.sqrt(s2[t]) * rng.standard_normal()
            if t + 1 < n:
                s2[t + 1] = self.omega + self.alpha * R[t] ** 2 + self.beta * s2[t]
        return GarchSeries(returns=R, variances=s2)


class Ewma(Record):
    """RiskMetrics: ew_{t+1} = decay ew_t + (1 - decay) R_t^2.

    Attributes:
        decay: lambda, 0.94 for daily data.
        weight: 1 - lambda, kept as its own constant so the recursion uses 0.06 exactly.
    """

    decay: float = 0.94
    weight: float = 0.06

    def variances(self, R: Floats, start: float) -> Floats:
        """Return the variances ew_t, from ew_0 = start, each known at t - 1."""
        n = len(R)
        ew = np.empty(n)
        ew[0] = start
        for t in range(n - 1):
            ew[t + 1] = self.decay * ew[t] + self.weight * R[t] ** 2
        return ew


def mse_ratio(model: Garch11, series: GarchSeries, ew: Floats, h: int, first: int) -> float:
    """Return MSE(EWMA) / MSE(GARCH) of the cumulative variance forecast over days t..t+h-1.

    Each forecast is made with the variances for day t, from day `first` to len - h - 1.
    """
    R, s2 = series.returns, series.variances
    idx = np.arange(first, len(R) - h)
    real = np.array([np.sum(R[t : t + h] ** 2) for t in idx])
    g = np.array([model.cumulative_forecast(s2[t], h) for t in idx])
    e = h * ew[idx]
    return float(np.mean((real - e) ** 2) / np.mean((real - g) ** 2))
