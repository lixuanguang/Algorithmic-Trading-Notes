"""Venue market shares: the ex-fixing share, turnover concentration and share-estimator variance."""

import numpy as np
from numpy.typing import NDArray

from trading_notes.records import Record

type Floats = NDArray[np.float64]


class VenueShare(Record):
    """A venue's share of a stock's volume when part of the volume trades in fixings.

    Attributes:
        share: M, the venue's share of all volume.
        fixing_share: m, its share of the fixing volume.
        fixing_fraction: p, the fraction of volume traded in fixings.
    """

    share: float
    fixing_share: float
    fixing_fraction: float

    def ex_fixing(self) -> float:
        """Return the share of continuous volume, (M - m p)/(1 - p).

        Raises:
            ValueError: If p is not in [0, 1) or the shares are infeasible together.
        """
        M, m, p = self.share, self.fixing_share, self.fixing_fraction
        if not (0 <= p < 1 and 0 <= m <= 1 and m * p <= M <= m * p + (1 - p)):
            raise ValueError("shares must be feasible")
        return (M - m * p) / (1 - p)


class Turnover(Record):
    """Turnover across stocks, or volume across venues, whose concentration is measured.

    Attributes:
        values: The non-negative turnover of each unit.
    """

    values: Floats

    def gini(self) -> float:
        """Return the Gini coefficient from the Lorenz curve, G = 1 - 2 int L."""
        x = np.sort(np.asarray(self.values, float))
        L = np.concatenate([[0], np.cumsum(x) / x.sum()])
        u = np.linspace(0, 1, len(L))
        value: float = 1 - 2 * np.trapezoid(L, u)
        return value

    def gini_mean_difference(self) -> float:
        """Return the Gini coefficient as half the relative mean difference."""
        x = np.asarray(self.values, float)
        value: float = np.abs(x[:, None] - x[None, :]).sum() / (2 * len(x) ** 2 * x.mean())
        return value


class IndexShareDifference(Record):
    """A stock's estimated venue share against a fixed-weight index of estimated shares.

    Attributes:
        weights: The index weights w_j.
        variances: The sampling variance of each estimated share.
    """

    weights: Floats
    variances: Floats

    def variance(self, k: int, covariance: Floats | None = None) -> float:
        """Return Var(p_hat_k - sum_j w_j p_hat_j), shares independent unless covariance given."""
        a = -np.asarray(self.weights, float)
        a[k] += 1.0  # p_hat_k - sum_j w_j p_hat_j
        C = np.diag(self.variances) if covariance is None else np.asarray(covariance)
        return float(a @ C @ a)
