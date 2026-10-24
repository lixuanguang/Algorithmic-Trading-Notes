"""Kelly growth rates of a constant-fraction strategy, in continuous time and for discrete bets."""

import math

import numpy as np

from trading_notes.numerical.records import Record


class ContinuousKelly(Record):
    """A risky asset following geometric Brownian motion beside cash earning a constant rate.

    A constant fraction f of wealth is held in the asset; there are no costs or leverage limits.

    Attributes:
        mu: Expected return of the asset, a year.
        rate: Risk-free rate, a year.
        sigma: Volatility of the asset, a year.
    """

    mu: float
    rate: float
    sigma: float

    @property
    def kelly_fraction(self) -> float:
        """Return the growth-optimal fraction f* = (mu - r) / sigma^2."""
        return (self.mu - self.rate) / self.sigma**2

    def growth(self, f: float) -> float:
        """Return the continuous log growth rate of wealth, r + f(mu - r) - f^2 sigma^2 / 2."""
        return self.rate + f * (self.mu - self.rate) - 0.5 * f**2 * self.sigma**2

    def gross_step(self, f: float, step: float, z: float) -> float:
        """Return one rebalancing step's gross wealth factor at the standard normal draw z.

        Args:
            f: Fraction held in the asset, restored at the start of the step.
            step: Length of the step in years.
            z: The step's standard normal shock.
        """
        return (1 - f) * math.exp(self.rate * step) + f * math.exp(
            (self.mu - self.sigma**2 / 2) * step + self.sigma * math.sqrt(step) * z
        )

    def ruin_threshold(self, f: float, step: float) -> float:
        """Return the draw z at or below which one step's gross factor is nonpositive.

        Only defined for a levered fraction f > 1, where wealth can be lost within a step.
        """
        return (
            math.log((f - 1) * math.exp(self.rate * step) / f)
            - (self.mu - self.sigma**2 / 2) * step
        ) / (self.sigma * math.sqrt(step))

    def rebalanced_growth(self, f: float, step: float, nodes: int = 80) -> float:
        """Return the expected log growth a year with the fraction 0 <= f <= 1 restored each step.

        The expectation over the step's lognormal return is approximated by Gauss-Hermite
        quadrature with `nodes` nodes.
        """
        z, w = np.polynomial.hermite_e.hermegauss(nodes)
        w = w / w.sum()
        gross = (1 - f) * math.exp(self.rate * step) + f * np.exp(
            (self.mu - self.sigma**2 / 2) * step + self.sigma * math.sqrt(step) * z
        )
        return float(np.sum(w * np.log(gross))) / step


class DiscreteBet(Record):
    """A repeated bet that wins b per unit staked with probability p and otherwise loses the stake.

    Attributes:
        p: Probability of a win.
        b: Net odds received on a win.
    """

    p: float
    b: float

    @property
    def kelly_fraction(self) -> float:
        """Return the growth-optimal fraction p - q / b."""
        return self.p - (1 - self.p) / self.b

    def growth(self, f: float) -> float:
        """Return the expected log growth of staking the fraction f of wealth on each bet."""
        return self.p * math.log(1 + self.b * f) + (1 - self.p) * math.log(1 - f)
