"""Vasicek's one-factor Gaussian model of defaults, and the Basel IRB corporate risk weight."""

import math

import numpy as np
from numpy.typing import NDArray
from scipy import stats

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]


class VasicekFactorModel(Record):
    """Defaults of names whose latent variables load sqrt(rho) on one standard normal factor M.

    Attributes:
        pd: Each name's unconditional default probability to the horizon.
        rho: The copula correlation.
    """

    pd: float
    rho: float

    def conditional_pd[M: (float, Floats)](self, factor: M) -> M:
        """Return the default probability given the factor (Hull eq. 24.9, RMFI eq. 9.13)."""
        value: M = stats.norm.cdf(
            (stats.norm.ppf(self.pd) - np.sqrt(self.rho) * factor) / np.sqrt(1 - self.rho)
        )
        return value

    def worst_case_default_rate(self, confidence: float) -> float:
        """Return the default rate not exceeded with the given confidence (Hull RMFI eq. 19.1)."""
        return float(
            stats.norm.cdf(
                (stats.norm.ppf(self.pd) + np.sqrt(self.rho) * stats.norm.ppf(confidence))
                / np.sqrt(1 - self.rho)
            )
        )


class IrbCapital(Record):
    """The Basel IRB capital of a corporate exposure (CRE31.5).

    Attributes:
        correlation: R, interpolated between 0.12 and 0.24 by the PD.
        maturity_adjustment: b.
        conditional_pd: The default probability at the 99.9% factor quantile.
        capital: K, per unit of exposure at default.
        risk_weight: 12.5 K.
    """

    correlation: float
    maturity_adjustment: float
    conditional_pd: float
    capital: float
    risk_weight: float


def irb_corporate(pd: float, lgd: float, maturity: float = 2.5) -> IrbCapital:
    """Return CRE31.5's correlation, maturity adjustment, capital and risk weight."""
    N, G = stats.norm.cdf, stats.norm.ppf
    w = (1 - math.exp(-50 * pd)) / (1 - math.exp(-50))
    R = 0.12 * w + 0.24 * (1 - w)
    b = (0.11852 - 0.05478 * math.log(pd)) ** 2
    cond = N(G(pd) / math.sqrt(1 - R) + math.sqrt(R / (1 - R)) * G(0.999))
    K = (lgd * cond - pd * lgd) * (1 + (maturity - 2.5) * b) / (1 - 1.5 * b)
    return IrbCapital(
        correlation=R,
        maturity_adjustment=b,
        conditional_pd=float(cond),
        capital=float(K),
        risk_weight=float(12.5 * K),
    )
