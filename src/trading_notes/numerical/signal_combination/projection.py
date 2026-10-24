"""Best linear projection against conditional expectation for a signal with zero linear IC."""

import itertools

import numpy as np
from numpy.typing import NDArray

from trading_notes.records import Record

type Floats = NDArray[np.float64]


class NonlinearSample(Record):
    """A signal and a return that depends on it only through g^2.

    Attributes:
        g: The signal, draws of N(0, 1).
        r: The return g^2 - 1 + s e, with e independent N(0, 1) draws.
    """

    g: Floats
    r: Floats

    def projection_slope(self) -> float:
        """Return the linear projection slope Cov(r, g) / Var(g).

        The covariance is np.cov's (divisor N - 1) and the variance np.var's (divisor N); at
        N = 2,000,000 the mismatch changes the slope by a factor 1 + 5e-7.
        """
        return float(np.cov(self.r, self.g)[0, 1] / np.var(self.g))


class ZeroIcModel(Record):
    """The model r = g^2 - 1 + s e, g and e independent N(0, 1): zero IC, full information.

    Attributes:
        noise: The standard deviation s of the noise term.
    """

    noise: float

    def simulate(self, rng: np.random.Generator, n: int) -> NonlinearSample:
        """Draw all n signals, then all n noise terms, and form the returns."""
        g = rng.standard_normal(n)
        # The data-generating model, written out; conditional_mean is the claim checked against it.
        r = g**2 - 1 + self.noise * rng.standard_normal(n)
        return NonlinearSample(g=g, r=r)

    def conditional_mean(self, g: Floats) -> Floats:
        """Return E[r | g] = g^2 - 1."""
        return g**2 - 1

    def explained_share(self) -> float:
        """Return the share of Var(r) explained by E[r | g]: Var(g^2) / (Var(g^2) + s^2).

        For g ~ N(0, 1), Var(g^2) = 2, so the share is 2 / (2 + s^2), independent of simulation.
        """
        return 2 / (2 + self.noise**2)


def correlation(x: Floats, y: Floats) -> float:
    """Return the sample correlation of x and y."""
    return float(np.corrcoef(x, y)[0, 1])


def largest_bin_gap(g: Floats, r: Floats, slope: float) -> float:
    """Return the largest |mean(r) - slope mean(g)| over eight bins of g of width 0.5.

    Each bin [lo, hi) includes its lower edge and excludes its upper one; observations below
    -2 or at or above 2 fall in no bin.
    """
    worst = 0.0
    for lo, hi in itertools.pairwise(np.linspace(-2, 2, 9)):
        m = (g >= lo) & (g < hi)
        worst = max(worst, float(abs(r[m].mean() - slope * g[m].mean())))
    return worst
