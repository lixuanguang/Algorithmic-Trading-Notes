"""Sampling theory of the Sharpe ratio: standard errors, annualisation and deflation."""

import math
from typing import Final

import numpy as np
from numpy.typing import NDArray
from scipy.stats import norm

from trading_notes.records import Record

type Floats = NDArray[np.float64]

EULER_GAMMA: Final = 0.5772156649015329  # Euler-Mascheroni


def sample_sharpe_ratios(returns: Floats) -> Floats:
    """Return the Sharpe ratio along the last axis, with the population (ddof 0) deviation.

    Args:
        returns: Excess returns, (..., T).

    Returns:
        One ratio per series, shape (...).
    """
    ratios: Floats = returns.mean(axis=-1) / returns.std(axis=-1, ddof=0)
    return ratios


def ar1_annualisation_factor(q: int, rho: float) -> float:
    """Return Lo's eta(q) for AR(1) returns, the closed form of his eq. (22).

    SR(q) = eta(q) SR(1) when returns are summed over q periods. For positive q the form is
    defined at rho = 0, where its correction term vanishes and it is sqrt(q).
    """
    if rho == 0:
        return math.sqrt(q)
    return math.sqrt(q) * math.pow(
        1 + 2 * rho / (1 - rho) * (1 - (1 - rho**q) / (q * (1 - rho))), -0.5
    )


def expected_maximum_sharpe(trials: int, variance: float) -> float:
    """Return the expected maximum Sharpe ratio of independent trials (Bailey and Lopez de Prado).

    Their eq. (2): sqrt(V) ((1 - gamma) z(1 - 1/N) + gamma z(1 - 1/(N e))), with Euler's gamma.

    Args:
        trials: N, the number of trials.
        variance: V, the variance of the trials' Sharpe ratios, in the units of the ratio.
    """
    return math.sqrt(variance) * (
        (1 - EULER_GAMMA) * norm.ppf(1 - 1 / trials)
        + EULER_GAMMA * norm.ppf(1 - 1 / (trials * math.e))
    )


class SharpeEstimate(Record):
    """A Sharpe ratio estimated from IID returns, in per-observation units.

    Attributes:
        ratio: The estimate SR.
        observations: T, the number of returns behind it.
        skewness: g3 of the returns.
        kurtosis: g4 of the returns, not excess; 3 for normal returns.
    """

    ratio: float
    observations: int
    skewness: float = 0.0
    kurtosis: float = 3.0

    def asymptotic_variance(self) -> float:
        """Return V = 1 - g3 SR + (g4 - 1) / 4 SR^2, the limit of T Var(SR_hat).

        It needs a finite fourth moment unless SR = 0, and reduces to 1 + SR^2/2 for normal
        moments.
        """
        sr = self.ratio
        return 1 - self.skewness * sr + (self.kurtosis - 1) / 4 * sr * sr

    def normal_standard_error(self) -> float:
        """Return Lo's IID standard error sqrt((1 + SR^2/2) / T), his eq. (9)."""
        return math.sqrt((1 + 0.5 * self.ratio * self.ratio) / self.observations)

    def deflated(self, trials: int, trial_variance: float) -> float:
        """Return the deflated Sharpe ratio, Bailey and Lopez de Prado's eq. (1).

        The probability that the true ratio exceeds the expected maximum of `trials`
        independent trials whose ratios have variance `trial_variance`.
        """
        benchmark = expected_maximum_sharpe(trials, trial_variance)
        return float(
            norm.cdf(
                (self.ratio - benchmark)
                * math.sqrt(self.observations - 1)
                / math.sqrt(self.asymptotic_variance())
            )
        )
