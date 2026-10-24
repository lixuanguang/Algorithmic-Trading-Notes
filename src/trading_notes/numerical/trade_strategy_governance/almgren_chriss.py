"""Discrete Almgren-Chriss optimal liquidation: the schedule, its expected cost and variance."""

import math

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]


class ExecutionSchedule(Record):
    """An optimal liquidation schedule.

    Attributes:
        expected_cost: E, the expected implementation shortfall.
        variance: V, its variance.
        holdings: The shares still held at each of the n + 1 times.
    """

    expected_cost: float
    variance: float
    holdings: Floats


class AlmgrenChriss(Record):
    """The sale of X shares over T in n equal periods with linear temporary and permanent impact.

    Attributes:
        shares: X.
        horizon: T.
        periods: n.
        sigma: Volatility of the price per unit time.
        eta: Temporary impact coefficient.
        epsilon: Fixed cost per share (half the spread plus fees).
        gamma: Permanent impact coefficient.
    """

    shares: float
    horizon: float
    periods: int
    sigma: float
    eta: float
    epsilon: float
    gamma: float

    def schedule(self, risk_aversion: float) -> ExecutionSchedule:
        """Return the optimal schedule for a risk aversion lambda; lambda = 0 trades linearly."""
        X, T, n, lam = self.shares, self.horizon, self.periods, risk_aversion
        tau = T / n
        eta_t = self.eta * (1 - self.gamma * tau / (2 * self.eta))
        kt = math.sqrt(lam * self.sigma**2 / eta_t) if lam > 0 else 0.0
        kappa = math.acosh(1 + 0.5 * kt**2 * tau**2) / tau if lam > 0 else 0.0
        t = np.arange(n + 1) * tau
        if lam > 0:
            x = X * np.sinh(kappa * (T - t)) / np.sinh(kappa * T)
        else:
            x = X * (1 - t / T)
        trades = -np.diff(x)
        E = 0.5 * self.gamma * X**2 + self.epsilon * X + (eta_t / tau) * np.sum(trades**2)
        V = self.sigma**2 * tau * np.sum(x[1:] ** 2)
        return ExecutionSchedule(expected_cost=float(E), variance=float(V), holdings=x)
