"""Maximum drawdowns of AR(1) returns against their shuffled and block-bootstrap resamples."""

import numpy as np
from numpy.typing import NDArray

from trading_notes.records import Record

type Floats = NDArray[np.float64]


def max_drawdown(r: Floats) -> np.float64 | Floats:
    """Return the maximum drawdown of log wealth along the last axis.

    Log wealth starts at 0, which counts as the first peak, so an initial loss is a drawdown.

    Args:
        r: Simple returns, (..., n).

    Returns:
        The largest fall from a running peak, in log units, shape (...): a NumPy scalar for
        one path of shape (n,), an array for a batch of paths.
    """
    w = np.cumsum(np.log1p(r), axis=-1)
    peak = np.maximum.accumulate(
        np.concatenate([np.zeros((*w.shape[:-1], 1)), w], axis=-1), axis=-1
    )[..., 1:]
    # NumPy's stubs leave a reduction along an axis untyped; reducing the last axis of a
    # one-dimensional array gives a scalar and of a batch an array, as the tests confirm.
    drawdowns: np.float64 | Floats = np.max(peak - w, axis=-1)
    return drawdowns


def shuffle_bootstrap(rng: np.random.Generator, x: Floats, samples: int) -> Floats:
    """Return `samples` random permutations of x, samples x len(x), drawn one after another."""
    return np.array([rng.permutation(x) for _ in range(samples)])


class Ar1Returns(Record):
    """Returns r_t = mean + phi (r_{t-1} - mean) + e_t with e_t ~ N(0, sd^2), from r_0 = mean + e_0.

    Attributes:
        mean: Mean return per period.
        phi: AR(1) coefficient.
        sd: Innovation standard deviation.
        periods: Periods kept per path.
        burn_in: Periods simulated and discarded before each path.
    """

    mean: float
    phi: float
    sd: float
    periods: int
    burn_in: int

    def simulate(self, rng: np.random.Generator, n_paths: int) -> Floats:
        """Return n_paths paths, n_paths x periods; all innovations are drawn at once."""
        n = self.periods + self.burn_in
        e = rng.normal(0, self.sd, (n_paths, n))
        r = np.empty_like(e)
        r[:, 0] = self.mean + e[:, 0]
        for t in range(1, n):
            r[:, t] = self.mean + self.phi * (r[:, t - 1] - self.mean) + e[:, t]
        return r[:, self.burn_in :]


class StationaryBootstrap(Record):
    """A stationary-type block bootstrap: uniform block starts, geometric lengths, wrapping around.

    Attributes:
        mean_block: L, the mean block length.
    """

    mean_block: float

    def resample(self, rng: np.random.Generator, x: Floats, samples: int) -> Floats:
        """Return `samples` resamples of x, samples x len(x).

        Each sample starts at a uniform index. After each observation one uniform draw decides,
        with probability 1/L, whether a new block starts at a fresh uniform index; otherwise the
        next index follows, wrapping around the end of x.
        """
        n = len(x)
        out = np.empty((samples, n))
        for b in range(samples):
            i, k = rng.integers(n), 0
            while k < n:
                out[b, k] = x[i % n]
                k += 1
                i = rng.integers(n) if rng.random() < 1 / self.mean_block else i + 1
        return out


class DrawdownComparison(Record):
    """95th percentiles of the maximum drawdown, in log units.

    Attributes:
        reference: The model's own, over the reference paths.
        shuffle: Median over sample paths of the shuffled bootstrap's.
        stationary: Median over sample paths of the stationary-type block bootstrap's.
    """

    reference: float
    shuffle: float
    stationary: float


class DrawdownExperiment(Record):
    """The model's own drawdown tail against each bootstrap's estimate from single paths.

    Attributes:
        returns: The return model.
        reference_paths: Paths behind the reference percentile.
        sample_paths: Independent sample paths, each bootstrapped on its own.
        replications: Bootstrap samples per sample path.
        blocks: The block bootstrap.
    """

    returns: Ar1Returns
    reference_paths: int
    sample_paths: int
    replications: int
    blocks: StationaryBootstrap

    def run(self, rng: np.random.Generator) -> DrawdownComparison:
        """Run the comparison on one stream.

        The generator draws the reference paths, then for each sample path in turn the path
        itself, its shuffled samples and its block samples.
        """
        ref = np.quantile(max_drawdown(self.returns.simulate(rng, self.reference_paths)), 0.95)
        q_sh, q_st = [], []
        for _ in range(self.sample_paths):
            x = self.returns.simulate(rng, 1)[0]
            shuffled = shuffle_bootstrap(rng, x, self.replications)
            q_sh.append(np.quantile(max_drawdown(shuffled), 0.95))
            blocks = self.blocks.resample(rng, x, self.replications)
            q_st.append(np.quantile(max_drawdown(blocks), 0.95))
        return DrawdownComparison(
            reference=float(ref),
            shuffle=float(np.median(q_sh)),
            stationary=float(np.median(q_st)),
        )
