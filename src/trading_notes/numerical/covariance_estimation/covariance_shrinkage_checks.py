"""Oracle linear shrinkage of the sample covariance, simulated with a known population."""

import sys
from typing import Final

from trading_notes.numerical.covariance_estimation.oracle_shrinkage import (
    OracleShrinkage,
    ShrinkageExperiment,
)

EXPERIMENT: Final = ShrinkageExperiment(assets=100, observations=120, samples=300, seed=2020)


def failed_conditions(run: OracleShrinkage) -> list[str]:
    """Return the names of the three conditions that fail, in order.

    The identity is accepted within 2% of delta^2; the two improvements must be strict.
    """
    fails = []
    if abs(run.alpha2 + run.beta2 - run.delta2) > 0.02 * run.delta2:
        fails.append("identity")
    if not run.loss_oracle < run.beta2:
        fails.append("Frobenius")
    if not run.var_oracle < run.var_sample:
        fails.append("GMV variance")
    return fails


def main() -> int:
    """Run the simulation, print its estimates and any failures; return 0, or 1 on failure.

    Own simulation behind meth:portfolio-covariance-estimation. Ledoit and Wolf's review (UZH WP
    323, version of February 2020, eqs. (2.4)-(2.7), pp. 5-6) gives the oracle linear shrinkage
    Sigma* = gamma* mu I + (1 - gamma*) S, gamma* = beta^2 / delta^2, mu = <Sigma, I>, with the
    scaled Frobenius norm ||A||^2 = Tr(A'A)/N, beta^2 = E||S - Sigma||^2, delta^2 =
    E||S - mu I||^2 = alpha^2 + beta^2. With the population known, so that the oracle is
    computable (N = 100 assets, T = 120 i.i.d. normal observations, a one-factor covariance):
    (1) the identity alpha^2 + beta^2 = delta^2 holds by simulation; (2) the oracle has lower
    Frobenius loss than S; (3) the global minimum-variance portfolio built from Sigma* has a lower
    true variance than the one built from S. Synthetic data only; the paper's feasible estimator
    is not reproduced. Only failed conditions are reported, each as a BAD line.
    """
    run = EXPERIMENT.run()
    print(
        f"alpha^2 + beta^2 = {run.alpha2 + run.beta2:.6f}, delta^2 = {run.delta2:.6f}; "
        f"oracle intensity gamma* = {run.gamma:.3f}"
    )
    print(f"Frobenius loss: sample {run.beta2:.6f}, oracle shrinkage {run.loss_oracle:.6f}")
    print(
        f"true variance of GMV portfolio: from S {run.var_sample:.6f}, "
        f"from Sigma* {run.var_oracle:.6f}, true optimum {run.var_true:.6f}"
    )
    fails = failed_conditions(run)
    for f in fails:
        print("BAD", f)
    if fails:
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
