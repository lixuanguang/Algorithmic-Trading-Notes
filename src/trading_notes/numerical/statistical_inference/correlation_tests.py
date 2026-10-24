"""Tests of correlation and independence: Pearson's t-test, Spearman's rho and chi-square."""

import math

import numpy as np
from numpy.typing import NDArray
from scipy import stats

from trading_notes.records import Record

type Floats = NDArray[np.float64]


class CorrelationTTest(Record):
    """The t-test of zero correlation on n pairs: t = r sqrt(n - 2) / sqrt(1 - r^2), n - 2 df.

    Attributes:
        pairs: n, the number of pairs.
    """

    pairs: int

    def statistic(self, r: float) -> float:
        """Return t for the sample correlation r."""
        return r * math.sqrt(self.pairs - 2) / math.sqrt(1 - r * r)

    def p_value(self, r: float) -> float:
        """Return the two-sided p-value for the sample correlation r."""
        return float(2 * stats.t.sf(abs(self.statistic(r)), self.pairs - 2))

    def critical_r(self, alpha: float = 0.05) -> float:
        """Return the two-sided critical value of r at level alpha."""
        tc = stats.t.ppf(1 - alpha / 2, self.pairs - 2)
        return float(tc / math.sqrt(tc * tc + self.pairs - 2))


def midranks(x: Floats) -> Floats:
    """Return the ranks of x, ties sharing their average rank."""
    return stats.rankdata(x, method="average")


def spearman(x: Floats, y: Floats) -> float:
    """Return Spearman's correlation as Pearson's on midranks."""
    return float(np.corrcoef(midranks(x), midranks(y))[0, 1])


def spearman_shortcut(x: Floats, y: Floats) -> float:
    """Return the shortcut 1 - 6 sum d^2 / (n(n^2 - 1)), exact only without ties."""
    d = midranks(x) - midranks(y)
    n = len(x)
    return 1 - 6 * float(np.sum(d * d)) / (n * (n * n - 1))


class ContingencyTable(Record):
    """Observed counts of a two-way table, for Pearson's chi-square test of independence.

    Attributes:
        counts: Rows of observed counts.
    """

    counts: tuple[tuple[int, ...], ...]

    def expected(self) -> Floats:
        """Return the counts expected under independence: row total x column total / total."""
        o = np.asarray(self.counts, dtype=float)
        expected: Floats = np.outer(o.sum(axis=1), o.sum(axis=0)) / o.sum()
        return expected

    def statistic(self) -> float:
        """Return Pearson's chi-square statistic, without continuity correction."""
        o = np.asarray(self.counts, dtype=float)
        e = self.expected()
        return float(np.sum((o - e) ** 2 / e))

    @property
    def dof(self) -> int:
        """Return the degrees of freedom, (rows - 1)(columns - 1)."""
        return (len(self.counts) - 1) * (len(self.counts[0]) - 1)

    def p_value(self) -> float:
        """Return the upper-tail chi-square p-value of the statistic."""
        return float(stats.chi2.sf(self.statistic(), self.dof))
