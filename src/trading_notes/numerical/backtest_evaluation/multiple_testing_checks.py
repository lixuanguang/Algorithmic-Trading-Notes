"""Familywise error and power of four multiple-testing procedures on dependent statistics."""

import sys
from collections.abc import Mapping
from typing import Final

import numpy as np
from scipy.stats import norm

from trading_notes.numerical.backtest_evaluation.familywise_tests import (
    FamilywiseTests,
    NormalTestStatistics,
    Tally,
)

SEED: Final = 31
K: Final = 20  # hypotheses
RHO: Final = 0.8  # correlation of every pair of test statistics
ALPHA: Final = 0.05
FALSE_NULLS: Final = 5  # the first FALSE_NULLS hypotheses, with mean 3.0; the rest are true
CALIBRATION_DRAWS: Final = 200000  # null vectors behind the max quantiles
TRIALS: Final = 4000
METHODS: Final = ("Bonferroni", "Holm", "single-step max", "StepM")
TESTS: Final = FamilywiseTests(alpha=ALPHA)


def model() -> NormalTestStatistics:
    """Return the example's statistics: FALSE_NULLS means of 3.0, then zeros, equicorrelated."""
    theta = np.concatenate([np.full(FALSE_NULLS, 3.0), np.zeros(K - FALSE_NULLS)])
    return NormalTestStatistics.equicorrelated(theta, RHO)


def simulate(rng: np.random.Generator) -> dict[str, Tally]:
    """Calibrate the cutoffs, then run the trials, on one stream.

    The generator draws the CALIBRATION_DRAWS null vectors first, then one vector per trial.
    """
    m = model()
    cutoffs = TESTS.max_cutoffs(m.draw_nulls(rng, CALIBRATION_DRAWS))
    tallies = {method: Tally(false_nulls=FALSE_NULLS) for method in METHODS}
    for _ in range(TRIALS):
        w = m.draw(rng)
        p = 1 - norm.cdf(w)
        tallies["Bonferroni"].add(TESTS.bonferroni(p))
        tallies["Holm"].add(TESTS.holm(p))
        tallies["single-step max"].add(cutoffs.single_step(w))
        tallies["StepM"].add(cutoffs.stepm(w))
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

    Romano and Wolf (UPF working paper 712, October 2003, secs. 2.3-3, pp. 7-11) state that
    Bonferroni and Holm control the familywise error rate (FWE) but are conservative because
    they ignore dependence, that a single-step max-type method (White's Reality Check, modified)
    controls the FWE with power gained from the joint distribution, and that the stepwise
    version (StepM) controls the FWE while rejecting at least as many hypotheses. Checked here
    on K = 20 jointly normal, equicorrelated (rho = 0.8) test statistics with known covariance
    (so the max quantiles are simulated exactly rather than bootstrapped), 5 false nulls with
    mean 3.0 and 15 true nulls with mean 0, alpha 5%. Each method's FWE and share of false nulls
    rejected are printed; only failed conditions are reported, each as a BAD line.

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
