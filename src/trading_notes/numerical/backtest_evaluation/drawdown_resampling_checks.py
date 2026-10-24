"""Shuffled against block-bootstrap estimates of the drawdown tail of autocorrelated returns."""

import sys
from typing import Final

import numpy as np

from trading_notes.numerical.backtest_evaluation.drawdown_bootstrap import (
    Ar1Returns,
    DrawdownComparison,
    DrawdownExperiment,
    StationaryBootstrap,
)

SEED: Final = 1710
EXPERIMENT: Final = DrawdownExperiment(
    returns=Ar1Returns(mean=0.005, phi=0.3, sd=0.04, periods=120, burn_in=50),
    reference_paths=20000,
    sample_paths=200,
    replications=400,
    blocks=StationaryBootstrap(mean_block=12),
)


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
    """Run the comparison, print it and any failures; return 0, or 1 on failure.

    The claim checked: shuffling single returns (Narang's remedy) destroys the serial
    dependence that drives drawdown depth, so with positively autocorrelated returns it
    understates drawdown risk, while resampling blocks of random (geometric) length keeps
    short-range dependence. This is an illustration on an AR(1) model chosen here, not a
    reading: Politis and Romano's stationary bootstrap paper was not obtained, and the resampler
    is the commonly described form (block starts uniform, lengths geometric with mean L,
    wrapping around the sample).

    Monthly returns r_t = 0.005 + 0.3 (r_{t-1} - 0.005) + e_t, e_t ~ N(0, 0.04^2), T = 120. The
    model's own distribution of the maximum drawdown is the reference; for 200 independent
    sample paths each method's bootstrap 95th percentile is compared with the reference 95th
    percentile. Only failed conditions are reported, each as a BAD line.
    """
    run = EXPERIMENT.run(np.random.default_rng(SEED))
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
