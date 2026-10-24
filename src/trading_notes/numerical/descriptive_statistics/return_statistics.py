"""Summary statistics of a return sample by the formulas of the return-statistics entries."""

import math
from collections.abc import Sequence

from trading_notes.records import Record


class ReturnSample(Record):
    """A sample of returns, with location, dispersion and shape statistics computed from it.

    Population statistics divide by N, sample statistics by N - 1; the returns may be in
    percent or decimals, and every statistic keeps their units (squared for variances).

    Attributes:
        values: The returns, in time order.
    """

    values: tuple[float, ...]

    @property
    def n(self) -> int:
        """Return N, the number of returns."""
        return len(self.values)

    def mean(self) -> float:
        """Return the arithmetic mean."""
        return sum(self.values) / self.n

    def median(self) -> float:
        """Return the middle ordered value, or the average of the two middle ones."""
        srt = sorted(self.values)
        mid = self.n // 2
        return srt[mid] if self.n % 2 else (srt[mid - 1] + srt[mid]) / 2

    def central_moment(self, k: int) -> float:
        """Return the k-th central moment with an N denominator."""
        m = self.mean()
        return sum((x - m) ** k for x in self.values) / self.n

    def population_variance(self) -> float:
        """Return the variance with an N denominator."""
        m = self.mean()
        return sum((x - m) ** 2 for x in self.values) / self.n

    def sample_variance(self) -> float:
        """Return the variance with an N - 1 denominator."""
        m = self.mean()
        return sum((x - m) ** 2 for x in self.values) / (self.n - 1)

    def average_absolute_deviation(self) -> float:
        """Return the mean absolute deviation from the mean."""
        m = self.mean()
        return sum(abs(x - m) for x in self.values) / self.n

    def median_absolute_deviation(self) -> float:
        """Return the median of the absolute deviations from the median."""
        med = self.median()
        return ReturnSample(values=tuple(abs(x - med) for x in self.values)).median()

    def percentile(self, p: float) -> float:
        """Return the p-quantile by the p(N + 1) rule, interpolating and clamping at the ends."""
        y = sorted(self.values)
        h = p * (self.n + 1)
        k, d = int(h), h - int(h)
        if k == 0:
            return y[0]
        if k >= self.n:
            return y[-1]
        return y[k - 1] + d * (y[k] - y[k - 1])

    def semideviation(self, target: float, denominator: float) -> float:
        """Return the semi-deviation below target, dividing the squared shortfalls by denominator.

        Conventions differ: N, N - 1 and the number of shortfalls are all in use.
        """
        s = sum(min(v - target, 0) ** 2 for v in self.values)
        return math.sqrt(s / denominator)

    def skewness(self) -> float:
        """Return the moment-ratio skewness g1 = m3 / m2^1.5."""
        scale: float = self.central_moment(2) ** 1.5
        return self.central_moment(3) / scale

    def kurtosis(self) -> float:
        """Return the moment-ratio kurtosis m4 / m2^2; the excess kurtosis is this less 3."""
        return self.central_moment(4) / self.central_moment(2) ** 2

    def adjusted_skewness(self) -> float:
        """Return the bias-adjusted skewness G1 = sqrt(N (N - 1)) / (N - 2) g1."""
        n = self.n
        return math.sqrt(n * (n - 1)) / (n - 2) * self.skewness()

    def adjusted_excess_kurtosis(self) -> float:
        """Return the bias-adjusted excess kurtosis G2."""
        n = self.n
        return (n - 1) / ((n - 2) * (n - 3)) * ((n + 1) * (self.kurtosis() - 3) + 6)

    def coefficient_of_variation(self) -> float:
        """Return the sample standard deviation over the mean."""
        return math.sqrt(self.sample_variance()) / self.mean()


def population_covariance(a: Sequence[float], b: Sequence[float]) -> float:
    """Return the covariance of two equally long samples with an N denominator."""
    n = len(a)
    mean_a, mean_b = sum(a) / n, sum(b) / n
    return sum((x - mean_a) * (y - mean_b) for x, y in zip(a, b, strict=True)) / n
