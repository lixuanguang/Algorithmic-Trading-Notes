"""Growing perpetuities, Gordon multiples and a two-state consumption economy's pricing kernel."""

import math

import numpy as np
from numpy.typing import NDArray

from trading_notes.records import Record

type Floats = NDArray[np.float64]


def gordon(d1: float, r: float, g: float) -> float:
    """Return the value of a perpetuity paying d1 next, growing at g, discounted at r."""
    return d1 / (r - g)


class GordonMultiple(Record):
    """The trailing P/E of a constant-growth stock with a fixed payout ratio.

    Attributes:
        payout: Dividends as a share of earnings.
        growth: Nominal growth of earnings and dividends.
    """

    payout: float
    growth: float

    def trailing_pe(self, required: float) -> float:
        """Return payout (1 + g) / (r - g) for a required nominal return r."""
        return self.payout * (1 + self.growth) / (required - self.growth)


class ConsumptionEconomy(Record):
    """A power-utility investor in an economy with a few consumption-growth states.

    Attributes:
        delta: The rate of time preference.
        gamma: Relative risk aversion.
        growth: Gross consumption growth in each state.
        probabilities: Each state's probability.
    """

    delta: float
    gamma: float
    growth: Floats
    probabilities: Floats

    def real_rate(self, mean_growth: float, vol: float) -> float:
        """Return Cochrane's log real rate delta + gamma E[g] - gamma^2 var(g) / 2 (eq. (1.7))."""
        return self.delta + self.gamma * mean_growth - 0.5 * self.gamma**2 * vol**2

    def kernel(self) -> Floats:
        """Return the stochastic discount factor e^{-delta} g^{-gamma} in each state."""
        m: Floats = math.exp(-self.delta) * self.growth ** (-self.gamma)
        return m

    def risk_free(self) -> float:
        """Return the gross risk-free return 1 / E[m]."""
        return float(1 / (self.probabilities @ self.kernel()))

    def price(self, payoff: Floats) -> float:
        """Return E[m x payoff]."""
        return float(self.probabilities @ (self.kernel() * payoff))

    def expected_excess(self, payoff: Floats) -> float:
        """Return the expected gross return less the gross risk-free return."""
        return float(self.probabilities @ payoff) / self.price(payoff) - self.risk_free()

    def covariance_premium(self, payoff: Floats) -> float:
        """Return -R_f Cov(m, R), the premium that the pricing kernel implies for the payoff."""
        m, p = self.kernel(), self.probabilities
        return float(-self.risk_free() * (p @ ((m - p @ m) * (payoff / self.price(payoff)))))
