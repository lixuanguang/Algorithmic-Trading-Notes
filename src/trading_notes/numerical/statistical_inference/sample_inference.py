"""Inference from samples: the t interval for a mean, and weighted historical VaR and ES."""

import math
from typing import Self

import numpy as np
from numpy.typing import NDArray
from scipy import stats

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]


class MeanEstimate(Record):
    """The sample mean of n observations, with its standard error, for normal IID data.

    Attributes:
        n: The number of observations.
        mean: The sample mean.
        sd: The sample standard deviation (divide by n - 1).
    """

    n: int
    mean: float
    sd: float

    @classmethod
    def of(cls, x: Floats) -> Self:
        """Return the estimate from a sample."""
        return cls(n=len(x), mean=float(x.mean()), sd=float(x.std(ddof=1)))

    @property
    def standard_error(self) -> float:
        """Return s / sqrt(n)."""
        return self.sd / math.sqrt(self.n)

    def t_quantile(self, level: float = 0.95) -> float:
        """Return the two-sided t quantile with n - 1 degrees of freedom."""
        return float(stats.t.ppf(1 - (1 - level) / 2, self.n - 1))

    def t_interval(self, level: float = 0.95) -> tuple[float, float]:
        """Return the exact t interval for the mean at the given confidence level."""
        tq, se = self.t_quantile(level), self.standard_error
        return self.mean - tq * se, self.mean + tq * se


class WeightedScenarioLosses(Record):
    """Scenario losses with probability weights, as in weighted historical simulation.

    Attributes:
        losses: One loss per scenario.
        weights: The scenarios' probabilities, summing to one.
    """

    losses: Floats
    weights: Floats

    def var_es(self, c: float) -> tuple[float, float]:
        """Return the lower c-quantile of the loss and the exact-tail-mass ES at c.

        Acerbi and Tasche, Definitions 2.2 and 2.6: tied losses are merged, and the tail mass
        1 - c is filled from the largest loss down, the last level fractionally. A cumulative
        mass within 1e-12 of the tail is treated as reaching it, so that weights summed in
        floating point keep their intended count.
        """
        p = 1 - c
        levels, inv = np.unique(-self.losses, return_inverse=True)
        levels = -levels  # distinct losses, largest first
        w = np.bincount(inv, weights=self.weights)
        cum = np.cumsum(w)
        k = int(np.argmax(cum > p + 1e-12))
        above = cum[k - 1] if k else 0.0
        return float(levels[k]), float((np.dot(w[:k], levels[:k]) + (p - above) * levels[k]) / p)

    def es_by_quantile_integral(self, c: float, grid: int = 200_000) -> float:
        """Return ES as the average of VaR_u over u in (c, 1), by a midpoint rule."""
        u = c + (np.arange(grid) + 0.5) * (1 - c) / grid
        order = np.argsort(self.losses)
        srt = self.losses[order]
        cdf = np.cumsum(self.weights[order])
        idx = np.searchsorted(cdf, u - 1e-12, side="left")
        return float(srt[np.minimum(idx, len(srt) - 1)].mean())


class ProportionEstimate(Record):
    """A proportion estimated from k successes in n independent trials.

    Attributes:
        successes: k.
        trials: n.
    """

    successes: int
    trials: int

    def _z(self, confidence: float) -> float:
        return float(stats.norm.ppf(0.5 + confidence / 2))

    def wald_interval(self, confidence: float = 0.95) -> tuple[float, float]:
        """Return the normal (Wald) interval p +/- z sqrt(p (1 - p) / n)."""
        n, z = self.trials, self._z(confidence)
        p = self.successes / n
        h = z * np.sqrt(p * (1 - p) / n)
        return float(p - h), float(p + h)

    def wilson_interval(self, confidence: float = 0.95) -> tuple[float, float]:
        """Return Wilson's score interval, which stays inside [0, 1] and covers better near 0."""
        n, z = self.trials, self._z(confidence)
        p = self.successes / n
        c = (p + z**2 / (2 * n)) / (1 + z**2 / n)
        h = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / (1 + z**2 / n)
        return float(c - h), float(c + h)


class SkillTest(Record):
    """A one-sided normal test that a manager's mean excess return is positive.

    Attributes:
        skill: The true mean excess return a year.
        sd: Its standard deviation a year, in the same units.
        confidence: One minus the test's size.
    """

    skill: float
    sd: float
    confidence: float = 0.95

    def power(self, years: float) -> float:
        """Return the probability of rejecting no skill after the given years."""
        z = stats.norm.ppf(self.confidence)
        tail: float = stats.norm.cdf(z - self.skill * np.sqrt(years) / self.sd)
        return 1 - tail

    def years_needed(self, power: float) -> float:
        """Return ((z_c + z_p) sd / skill)^2, the years for the test to reach the given power."""
        z_c, z_p = stats.norm.ppf(self.confidence), stats.norm.ppf(power)
        return float(((z_c + z_p) * self.sd / self.skill) ** 2)
