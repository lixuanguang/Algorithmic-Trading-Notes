"""Familywise error control: Bonferroni, Holm, a single-step max test and the StepM method."""

from typing import Self

import numpy as np
from numpy.typing import NDArray

from trading_notes.records import MutableRecord, Record

type Floats = NDArray[np.float64]
type Flags = NDArray[np.bool_]


class NormalTestStatistics(Record):
    """Jointly normal test statistics w = theta + L z, z ~ N(0, I).

    Attributes:
        means: theta, one mean per hypothesis; a true null has mean 0.
        chol: L, the Cholesky factor of their covariance.
    """

    means: Floats
    chol: Floats

    @classmethod
    def equicorrelated(cls, means: Floats, rho: float) -> Self:
        """Return unit-variance statistics whose every pair has correlation rho."""
        k = len(means)
        C = rho * np.ones((k, k)) + (1 - rho) * np.eye(k)
        # The factor is already float64; asarray, which copies nothing, states the dtype that
        # NumPy's stubs leave open.
        return cls(means=means, chol=np.asarray(np.linalg.cholesky(C), dtype=np.float64))

    def draw_nulls(self, rng: np.random.Generator, n: int) -> Floats:
        """Return n draws of the statistics with every mean set to zero, n x K."""
        draws: Floats = rng.standard_normal((n, len(self.means))) @ self.chol.T
        return draws

    def draw(self, rng: np.random.Generator) -> Floats:
        """Return one draw of the statistics."""
        sample: Floats = self.means + self.chol @ rng.standard_normal(len(self.means))
        return sample


class MaxCutoffs(Record):
    """Calibrated cutoffs of max-type tests, which use the statistics' joint distribution.

    Attributes:
        by_count: The (1 - alpha) quantile of the maximum of n null statistics, keyed by n.
    """

    by_count: dict[int, float]

    def single_step(self, w: Floats) -> Flags:
        """Reject each hypothesis whose statistic exceeds the cutoff for the maximum of all K."""
        return w > self.by_count[len(w)]

    def stepm(self, w: Floats) -> Flags:
        """Romano and Wolf's StepM with known cutoffs.

        Each step rejects the statistics above the cutoff for the number not yet rejected, and
        stops when a step rejects nothing or none are left.
        """
        rejected = np.zeros(len(w), bool)
        while True:
            left = np.where(~rejected)[0]
            if len(left) == 0:
                break
            new = left[w[left] > self.by_count[len(left)]]
            if len(new) == 0:
                break
            rejected[new] = True
        return rejected


class FamilywiseTests(Record):
    """Procedures that control the familywise error rate at level alpha.

    Attributes:
        alpha: The familywise level.
    """

    alpha: float

    def max_cutoffs(self, null_draws: Floats) -> MaxCutoffs:
        """Return the (1 - alpha) quantile of the maximum of n null statistics, for n = 1..K.

        Each is calibrated on the first n columns. With equicorrelated statistics the quantile
        depends only on how many are left, so it is keyed by that count, not by which ones.
        """
        k = null_draws.shape[1]
        return MaxCutoffs(
            by_count={
                n: float(np.quantile(null_draws[:, np.arange(n)].max(axis=1), 1 - self.alpha))
                for n in range(1, k + 1)
            }
        )

    def bonferroni(self, p: Floats) -> Flags:
        """Reject each hypothesis with p < alpha / K."""
        return p < self.alpha / len(p)

    def holm(self, p: Floats) -> Flags:
        """Step down from the smallest p-value, rejecting while p < alpha / (K - j).

        The order is np.argsort's default, and the first p-value that fails stops the procedure.
        """
        k = len(p)
        rejected = np.zeros(k, bool)
        for j, i in enumerate(np.argsort(p)):
            if p[i] < self.alpha / (k - j):
                rejected[i] = True
            else:
                break
        return rejected


class Tally(MutableRecord):
    """One procedure's counts over trials whose first `false_nulls` hypotheses are false.

    Attributes:
        false_nulls: How many leading hypotheses are false.
        familywise: Trials with at least one true null rejected.
        true_rejections: False nulls rejected, summed over trials.
    """

    false_nulls: int
    familywise: int = 0
    true_rejections: int = 0

    def add(self, rejected: Flags) -> None:
        """Count one trial's rejections, hypotheses in model order."""
        self.familywise += bool(rejected[self.false_nulls :].any())
        self.true_rejections += int(rejected[: self.false_nulls].sum())
