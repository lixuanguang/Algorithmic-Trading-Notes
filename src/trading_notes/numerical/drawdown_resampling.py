"""Own synthetic check behind meth:backtest-evaluation-diagnostics (drawdowns).

Source verification (2026-10-17). Claim checked: shuffling single returns (Narang's remedy)
destroys the serial dependence that drives drawdown depth, so with positively autocorrelated
returns it understates drawdown risk, while resampling blocks of random (geometric) length keeps
short-range dependence. This is an illustration on an AR(1) model chosen here, not a reading:
Politis and Romano's stationary bootstrap paper was not obtained, and the resampler below is the
commonly described form (block starts uniform, lengths geometric with mean L, wrapping around
the sample).
Design: monthly returns r_t = 0.005 + 0.3 (r_{t-1} - 0.005) + e_t, e_t ~ N(0, 0.04^2), T = 120.
The model's own distribution of the maximum drawdown is the reference; for 200 independent
sample paths each method's bootstrap 95th percentile is compared with the reference 95th
percentile. Only failed conditions are reported, each as a BAD line.
Run: uv run --frozen --no-editable python -m trading_notes.numerical.drawdown_resampling
(numpy; about 5 s). Exits non-zero on failure.
"""

# standard library imports
import sys
from dataclasses import dataclass
from typing import Final

# third party library imports
import numpy as np
from numpy.typing import NDArray

SEED: Final = 1710
T: Final = 120  # months per path
PHI: Final = 0.3  # AR(1) coefficient
MU: Final = 0.005  # mean monthly return
SD: Final = 0.04  # innovation standard deviation
BURN_IN: Final = 50  # months simulated and discarded before each path
REFERENCE_PATHS: Final = 20000
SAMPLE_PATHS: Final = 200
REPLICATIONS: Final = 400  # bootstrap samples per sample path
BLOCK: Final = 12  # mean block length L of the stationary-type bootstrap


@dataclass(frozen=True)
class DrawdownComparison:
    """95th percentiles of the maximum drawdown, in log units.

    Attributes:
        reference: The model's own, over REFERENCE_PATHS paths.
        shuffle: Median over sample paths of the shuffled bootstrap's.
        stationary: Median over sample paths of the stationary-type block bootstrap's.
    """

    reference: float
    shuffle: float
    stationary: float


def ar1(rng: np.random.Generator, n_paths: int) -> NDArray[np.float64]:
    """Return n_paths AR(1) return paths, n_paths x T, after BURN_IN discarded months.

    Each path starts at r_0 = MU + e_0; all innovations are drawn at once, path by path.
    """
    e = rng.normal(0, SD, (n_paths, T + BURN_IN))
    r = np.empty_like(e)
    r[:, 0] = MU + e[:, 0]
    for t in range(1, T + BURN_IN):
        r[:, t] = MU + PHI * (r[:, t - 1] - MU) + e[:, t]
    return r[:, BURN_IN:]


def max_dd(r: NDArray[np.float64]) -> NDArray[np.float64]:
    """Return the maximum drawdown of log wealth along the last axis.

    Log wealth starts at 0, which counts as the first peak, so an initial loss is a drawdown.

    Args:
        r: Simple returns, (..., n).

    Returns:
        The largest fall from a running peak, in log units, shape (...).
    """
    w = np.cumsum(np.log1p(r), axis=-1)
    peak = np.maximum.accumulate(
        np.concatenate([np.zeros((*w.shape[:-1], 1)), w], axis=-1), axis=-1
    )[..., 1:]
    drawdowns: NDArray[np.float64] = np.max(peak - w, axis=-1)
    return drawdowns


def shuffle_boot(rng: np.random.Generator, x: NDArray[np.float64], B: int) -> NDArray[np.float64]:
    """Return B random permutations of x, B x len(x)."""
    return np.array([rng.permutation(x) for _ in range(B)])


def stationary_boot(
    rng: np.random.Generator, x: NDArray[np.float64], B: int, L: int = BLOCK
) -> NDArray[np.float64]:
    """Return B stationary-type block bootstrap samples of x, B x len(x).

    Each sample starts at a uniform index. After each observation one uniform draw decides,
    with probability 1/L, whether a new block starts at a fresh uniform index; otherwise the
    next index follows, wrapping around the end of x.
    """
    n = len(x)
    out = np.empty((B, n))
    for b in range(B):
        i, k = rng.integers(n), 0
        while k < n:
            out[b, k] = x[i % n]
            k += 1
            i = rng.integers(n) if rng.random() < 1 / L else i + 1
    return out


def simulate(rng: np.random.Generator) -> DrawdownComparison:
    """Run the comparison on one stream.

    The generator draws the reference paths, then for each sample path in turn the path itself,
    its shuffled samples and its block samples.
    """
    ref = np.quantile(max_dd(ar1(rng, REFERENCE_PATHS)), 0.95)
    q_sh, q_st = [], []
    for _ in range(SAMPLE_PATHS):
        x = ar1(rng, 1)[0]
        q_sh.append(np.quantile(max_dd(shuffle_boot(rng, x, REPLICATIONS)), 0.95))
        q_st.append(np.quantile(max_dd(stationary_boot(rng, x, REPLICATIONS)), 0.95))
    return DrawdownComparison(float(ref), float(np.median(q_sh)), float(np.median(q_st)))


def failed_conditions(run: DrawdownComparison) -> list[str]:
    """Return the names of the two conditions that fail, in order.

    Shuffling must understate the reference by more than 15%, and blocks must come closer to it.
    """
    fails = []
    if not run.shuffle < 0.85 * run.reference:
        fails.append("shuffle does not understate")
    if not abs(run.stationary - run.reference) < abs(run.shuffle - run.reference):
        fails.append("blocks not closer than shuffle")
    return fails


def main() -> int:
    """Run the comparison, print it and any failures; return 0, or 1 on failure."""
    run = simulate(np.random.default_rng(SEED))
    print(f"reference 95th percentile of max drawdown (log units): {run.reference:.3f}")
    print(
        f"median bootstrap 95th percentile: shuffle {run.shuffle:.3f}, "
        f"stationary-type blocks (L=12) {run.stationary:.3f}"
    )
    fails = failed_conditions(run)
    for f in fails:
        print("BAD", f)
    if fails:
        return 1
    print(
        "ok  shuffling understates the drawdown tail under positive autocorrelation; "
        "blocks come closer\nall checks passed"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
