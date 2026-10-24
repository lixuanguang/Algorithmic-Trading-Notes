"""Geometric Brownian motion: its exact solution, moments, Euler scheme and discounted payoffs."""

import math

import numpy as np
from numpy.typing import NDArray
from scipy import stats

from trading_notes.records import Record

type Floats = NDArray[np.float64]


class GeometricBrownianMotion(Record):
    """dS = drift S dt + vol S dW, started at spot.

    Attributes:
        spot: S_0.
        drift: The drift m, annual.
        vol: sigma, annual.
    """

    spot: float
    drift: float
    vol: float

    def terminal(self, horizon: float, w: Floats) -> Floats:
        """Return the exact S_T = S_0 exp((m - sigma^2/2) T + sigma W_T) for each value of W_T."""
        st: Floats = self.spot * np.exp((self.drift - self.vol**2 / 2) * horizon + self.vol * w)
        return st

    def euler_terminal(self, horizon: float, dw: Floats) -> Floats:
        """Return S_T by Euler steps over [0, T], one column of Brownian increments per step."""
        s = np.full(dw.shape[0], self.spot)
        h = horizon / dw.shape[1]
        for k in range(dw.shape[1]):
            s = s * (1 + self.drift * h + self.vol * dw[:, k])
        return s

    def mean(self, horizon: float) -> float:
        """Return E[S_T] = S_0 e^(m T)."""
        return self.spot * math.exp(self.drift * horizon)

    def median(self, horizon: float) -> float:
        """Return the median S_0 e^((m - sigma^2/2) T)."""
        return self.spot * math.exp((self.drift - self.vol**2 / 2) * horizon)

    def second_moment(self, horizon: float) -> float:
        """Return E[S_T^2] = S_0^2 e^((2 m + sigma^2) T), by Ito's lemma on S^2."""
        return self.spot**2 * math.exp((2 * self.drift + self.vol**2) * horizon)

    def discounted_call_expectation(self, strike: float, rate: float, tau: float) -> float:
        """Return e^(-r tau) E[(S_tau - K)^+] under this drift.

        By Feynman-Kac it solves V_t + sigma^2 S^2 V_SS / 2 + m S V_S - r V = 0; it is a price
        only when the drift is the risk-free rate.
        """
        s, sg = self.spot, self.vol
        a1 = (math.log(s / strike) + (self.drift + sg**2 / 2) * tau) / (sg * math.sqrt(tau))
        a2 = a1 - sg * math.sqrt(tau)
        return math.exp(-rate * tau) * (
            s * math.exp(self.drift * tau) * stats.norm.cdf(a1) - strike * stats.norm.cdf(a2)
        )
