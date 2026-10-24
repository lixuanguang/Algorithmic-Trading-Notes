"""Own Monte Carlo behind meth:multiple-testing-control.

Source verification (2026-10-17). Romano and Wolf (UPF working paper 712, October 2003, secs.
2.3-3, pp. 7-11) state that Bonferroni and Holm control the familywise error rate (FWE) but are
conservative because they ignore dependence, that a single-step max-type method (White's
Reality Check, modified) controls the FWE with power gained from the joint distribution, and
that the stepwise version (StepM) controls the FWE while rejecting at least as many hypotheses.
Checked here on K = 20 jointly normal, equicorrelated (rho = 0.8) test statistics with known
covariance (so the max quantiles are simulated exactly rather than bootstrapped), 5 false nulls
with mean 3.0 and 15 true nulls with mean 0, alpha 5%. Each method's FWE and share of false
nulls rejected are printed; only failed conditions are reported, each as a BAD line.
Run: uv run --frozen --no-editable python -m trading_notes.numerical.multiple_testing
(numpy, scipy; about 1 s). Exits non-zero on failure.
"""

import sys
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Final

import numpy as np
from numpy.typing import NDArray
from scipy.stats import norm

SEED: Final = 31
K: Final = 20  # hypotheses
RHO: Final = 0.8  # correlation of every pair of test statistics
ALPHA: Final = 0.05
FALSE_NULLS: Final = 5  # the first FALSE_NULLS hypotheses, with mean 3.0; the rest are true
CALIBRATION_DRAWS: Final = 200000  # null vectors behind the max quantiles
TRIALS: Final = 4000
METHODS: Final = ("Bonferroni", "Holm", "single-step max", "StepM")


@dataclass(frozen=True)
class Model:
    """The test statistics' distribution: w = theta + L z, z ~ N(0, I_K).

    Attributes:
        theta: The means, FALSE_NULLS of 3.0 followed by zeros.
        chol: L, the Cholesky factor of the equicorrelated covariance.
    """

    theta: NDArray[np.float64]
    chol: NDArray[np.float64]


@dataclass
class Tally:
    """One method's counts over the trials.

    Attributes:
        familywise: Trials with at least one true null rejected.
        true_rejections: False nulls rejected, summed over trials.
    """

    familywise: int = 0
    true_rejections: int = 0

    def add(self, rejected: NDArray[np.bool_]) -> None:
        """Count one trial's rejections, hypotheses in model order."""
        self.familywise += bool(rejected[FALSE_NULLS:].any())
        self.true_rejections += int(rejected[:FALSE_NULLS].sum())


def model() -> Model:
    """Return the example's means and covariance factor."""
    theta = np.concatenate([np.full(FALSE_NULLS, 3.0), np.zeros(K - FALSE_NULLS)])
    C = RHO * np.ones((K, K)) + (1 - RHO) * np.eye(K)
    # The factor is already float64; asarray, which copies nothing, states the dtype that
    # NumPy's stubs leave open.
    return Model(theta, np.asarray(np.linalg.cholesky(C), dtype=np.float64))


def max_cutoffs(null_draws: NDArray[np.float64]) -> dict[int, float]:
    """Return the (1 - ALPHA) quantile of the maximum of n null statistics, for n = 1..K.

    Each is calibrated on the first n columns. With equicorrelated statistics the quantile
    depends only on how many are left, so it is keyed by that count, not by which ones.
    """
    return {
        n: float(np.quantile(null_draws[:, np.arange(n)].max(axis=1), 1 - ALPHA))
        for n in range(1, K + 1)
    }


def bonferroni(p: NDArray[np.float64]) -> NDArray[np.bool_]:
    """Reject each hypothesis with p < ALPHA / K."""
    return p < ALPHA / K


def holm(p: NDArray[np.float64]) -> NDArray[np.bool_]:
    """Step down through the p-values from the smallest, rejecting while p < ALPHA / (K - j).

    The order is np.argsort's default, and the first p-value that fails stops the procedure.
    """
    rejected = np.zeros(K, bool)
    for j, k in enumerate(np.argsort(p)):
        if p[k] < ALPHA / (K - j):
            rejected[k] = True
        else:
            break
    return rejected


def single_step_max(w: NDArray[np.float64], cutoffs: Mapping[int, float]) -> NDArray[np.bool_]:
    """Reject each hypothesis whose statistic exceeds the cutoff for the maximum of all K."""
    return w > cutoffs[K]


def stepm(w: NDArray[np.float64], cutoffs: Mapping[int, float]) -> NDArray[np.bool_]:
    """Romano and Wolf's StepM with known cutoffs.

    Each step rejects the statistics above the cutoff for the number not yet rejected, and
    stops when a step rejects nothing or none are left.
    """
    rejected = np.zeros(K, bool)
    while True:
        left = np.where(~rejected)[0]
        if len(left) == 0:
            break
        new = left[w[left] > cutoffs[len(left)]]
        if len(new) == 0:
            break
        rejected[new] = True
    return rejected


def simulate(rng: np.random.Generator) -> dict[str, Tally]:
    """Calibrate the cutoffs, then run the trials, on one stream.

    The generator draws the CALIBRATION_DRAWS null vectors first, then one vector per trial.
    """
    m = model()
    cutoffs = max_cutoffs(rng.standard_normal((CALIBRATION_DRAWS, K)) @ m.chol.T)
    tallies = {method: Tally() for method in METHODS}
    for _ in range(TRIALS):
        w = m.theta + m.chol @ rng.standard_normal(K)
        p = 1 - norm.cdf(w)
        tallies["Bonferroni"].add(bonferroni(p))
        tallies["Holm"].add(holm(p))
        tallies["single-step max"].add(single_step_max(w, cutoffs))
        tallies["StepM"].add(stepm(w, cutoffs))
    return tallies


def fwe(tally: Tally) -> float:
    """Return the share of trials with a familywise error."""
    return tally.familywise / TRIALS


def failed_conditions(tallies: Mapping[str, Tally]) -> list[str]:
    """Return the failed conditions, in order: four FWE checks, then two power comparisons.

    A method's FWE fails above ALPHA plus three binomial standard errors at 5%. Power is
    compared by the count of false nulls rejected.
    """
    se = np.sqrt(0.05 * 0.95 / TRIALS)
    fails = [f"{m} FWE above alpha" for m, tally in tallies.items() if fwe(tally) > ALPHA + 3 * se]
    pw = {m: tally.true_rejections for m, tally in tallies.items()}
    if not (
        pw["StepM"] >= pw["single-step max"] >= pw["Bonferroni"] and pw["Holm"] >= pw["Bonferroni"]
    ):
        fails.append("power ordering")
    if not pw["single-step max"] > pw["Holm"]:
        fails.append("dependence-aware method not more powerful than Holm at rho 0.8")
    return fails


def main() -> int:
    """Run the Monte Carlo and print each method, then any failures.

    Returns:
        The exit status, 0 or 1.
    """
    tallies = simulate(np.random.default_rng(SEED))
    for m, tally in tallies.items():
        power = tally.true_rejections / TRIALS / FALSE_NULLS
        print(f"  {m:16s}: FWE {fwe(tally):.3f}  share of false nulls rejected {power:.3f}")
    fails = failed_conditions(tallies)
    for f in fails:
        print("BAD", f)
    if fails:
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
