"""Tests of the oracle-shrinkage simulation: its generator, its conditions and its report."""

# The example's own run is tested in test_checks.py. These pin down the generator's draw order,
# the three conditions and the failure-only report, the last with stated estimates instead of a
# new simulation.

import contextlib
import io
import unittest
from unittest import mock

import numpy as np

from trading_notes.numerical.covariance_estimation import covariance_shrinkage_checks as cs
from trading_notes.numerical.covariance_estimation.oracle_shrinkage import (
    OracleShrinkage,
    ShrinkageExperiment,
    frob,
    gmv_var,
)

# Estimates that meet all three conditions.
PASSING = OracleShrinkage(
    alpha2=0.2, beta2=0.01, delta2=0.21, gamma=0.01 / 0.21, loss_oracle=0.009,
    var_sample=0.02, var_oracle=0.01, var_true=0.005,
)  # fmt: skip


class Simulation(unittest.TestCase):
    """Each run makes its own generator and draws the population before the samples."""

    def test_population_is_drawn_first(self) -> None:
        """Loadings then variances from default_rng(2020) give the run's alpha^2 exactly."""
        rng = np.random.default_rng(2020)
        beta = rng.normal(1.0, 0.3, cs.EXPERIMENT.assets)
        Sigma = 0.04 * np.outer(beta, beta) + np.diag(rng.uniform(0.01, 0.09, cs.EXPERIMENT.assets))
        mu = np.trace(Sigma) / cs.EXPERIMENT.assets
        run = cs.EXPERIMENT.run()
        self.assertEqual(run.alpha2, frob(Sigma - mu * np.eye(cs.EXPERIMENT.assets)))
        self.assertEqual(run, cs.EXPERIMENT.run())
        self.assertEqual(
            (
                cs.EXPERIMENT.assets,
                cs.EXPERIMENT.observations,
                cs.EXPERIMENT.samples,
                cs.EXPERIMENT.seed,
            ),
            (100, 120, 300, 2020),
        )

    def test_scaled_frobenius_norm_and_gmv_variance(self) -> None:
        """||I||^2 = Tr(I)/N = 1, and equal uncorrelated unit variances give GMV variance 1/N."""
        identity = np.eye(cs.EXPERIMENT.assets)
        self.assertEqual(frob(identity), 1.0)
        self.assertAlmostEqual(gmv_var(2 * identity, identity), 1 / cs.EXPERIMENT.assets, places=15)


class Conditions(unittest.TestCase):
    """The identity holds within 2%; both improvements must be strict."""

    def test_all_hold(self) -> None:
        """Estimates that meet every condition fail none."""
        self.assertEqual(cs.failed_conditions(PASSING), [])

    def test_identity_tolerance_is_two_percent_inclusive(self) -> None:
        """A gap of exactly 2% of delta^2 passes; a larger one fails."""
        # Exact in binary: the gap 51 - 50 equals 0.02 * 50, which rounds to 1.0.
        edge = PASSING.model_copy(update={"alpha2": 50.0, "beta2": 1.0, "delta2": 50.0})
        self.assertEqual(0.02 * edge.delta2, 1.0)
        self.assertEqual(cs.failed_conditions(edge), [])
        self.assertEqual(
            cs.failed_conditions(edge.model_copy(update={"beta2": 1.001})), ["identity"]
        )

    def test_ties_fail_in_order(self) -> None:
        """Equal losses and equal variances fail, reported in the conditions' order."""
        tied = PASSING.model_copy(
            update={"alpha2": 0.0, "loss_oracle": PASSING.beta2, "var_oracle": 0.02}
        )
        self.assertEqual(cs.failed_conditions(tied), ["identity", "Frobenius", "GMV variance"])


class Report(unittest.TestCase):
    """Only failed conditions are printed, after the estimates."""

    def test_failures_only_and_exit_status(self) -> None:
        """A failing run prints its three summaries, then one BAD line per failure."""
        failing = PASSING.model_copy(update={"var_oracle": 0.03})
        out = io.StringIO()
        with mock.patch.object(ShrinkageExperiment, "run", return_value=failing):
            with contextlib.redirect_stdout(out):
                status = cs.main()
        self.assertEqual(status, 1)
        self.assertEqual(
            out.getvalue(),
            "alpha^2 + beta^2 = 0.210000, delta^2 = 0.210000; oracle intensity gamma* = 0.048\n"
            "Frobenius loss: sample 0.010000, oracle shrinkage 0.009000\n"
            "true variance of GMV portfolio: from S 0.020000, from Sigma* 0.030000, "
            "true optimum 0.005000\n"
            "BAD GMV variance\n",
        )


if __name__ == "__main__":
    unittest.main()
