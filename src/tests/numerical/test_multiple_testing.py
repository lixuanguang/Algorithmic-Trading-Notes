"""Tests of the multiple-testing example's procedures, counts, cutoffs, stream and report.

The example's full run is tested in test_checks.py. These pin down the strict comparisons,
Holm's sorting and stopping, StepM's steps and stopping, how rejections are counted, the
cutoffs' calibration from the first n columns, the order in which the one stream is drawn,
and the six conditions with the failure-only report, with small inputs or prepared tallies.

Run: make test (uv run --frozen --no-editable pytest)
"""

import contextlib
import io
import unittest
from unittest import mock

import numpy as np
from numpy.typing import NDArray
from scipy.stats import norm

from trading_notes.numerical import multiple_testing as mt

K = mt.K
# Synthetic cutoffs, falling by 0.1 with each statistic left: 3.0 for all K, 2.9 for K - 1.
CUTOFFS = {n: 1.0 + 0.1 * n for n in range(1, K + 1)}


def rejected(*indices: int) -> NDArray[np.bool_]:
    """Return the decisions that reject exactly the given hypotheses."""
    out = np.zeros(K, bool)
    out[list(indices)] = True
    return out


class PValueProcedures(unittest.TestCase):
    """Bonferroni and Holm compare p-values strictly; Holm stops at its first acceptance."""

    def test_bonferroni_is_strict(self) -> None:
        """A p-value of exactly ALPHA / K is not rejected; anything smaller is."""
        p = np.full(K, 0.5)
        p[[0, 1]] = mt.ALPHA / K, np.nextafter(mt.ALPHA / K, 0)
        np.testing.assert_array_equal(mt.bonferroni(p), rejected(1))

    def test_holm_steps_down_from_the_smallest(self) -> None:
        """The j-th smallest p-value needs p < ALPHA / (K - j), whatever its position."""
        p = np.full(K, 0.5)
        p[[7, 3]] = 0.0024, 0.0026  # under 0.05/20 = 0.0025, then under 0.05/19 = 0.00263
        np.testing.assert_array_equal(mt.holm(p), rejected(7, 3))
        np.testing.assert_array_equal(mt.bonferroni(p), rejected(7))

    def test_holm_stops_at_the_first_acceptance(self) -> None:
        """A smallest p-value at 0.0025 is accepted, so 0.0026 is not tried at 0.05/19."""
        p = np.full(K, 0.5)
        p[[7, 3]] = mt.ALPHA / K, 0.0026
        np.testing.assert_array_equal(mt.holm(p), rejected())


class MaxProcedures(unittest.TestCase):
    """Single-step max uses the cutoff for all K; StepM recomputes it for those left."""

    def test_single_step_is_strict(self) -> None:
        """A statistic equal to the cutoff for K is not rejected."""
        w = np.zeros(K)
        w[[0, 1, 2]] = 3.0, 3.5, 2.95
        np.testing.assert_array_equal(mt.single_step_max(w, CUTOFFS), rejected(1))

    def test_stepm_steps_until_nothing_is_rejected(self) -> None:
        """3.5 > 3.0, then 2.95 > 2.9, then 2.85 > 2.8; 2.7 is not above 2.7, so it stops."""
        w = np.zeros(K)
        w[[4, 9, 2, 5]] = 3.5, 2.95, 2.85, 2.7
        np.testing.assert_array_equal(mt.stepm(w, CUTOFFS), rejected(4, 9, 2))

    def test_stepm_rejects_a_step_at_once(self) -> None:
        """Every statistic above a step's cutoff is rejected in that step, then none are left."""
        w = np.full(K, 10.0)
        np.testing.assert_array_equal(mt.stepm(w, CUTOFFS), np.ones(K, bool))


class Counting(unittest.TestCase):
    """A familywise error counts once a trial; false nulls rejected count each."""

    def test_tally(self) -> None:
        """Two true nulls rejected make one error; two false nulls rejected count two."""
        tally = mt.Tally()
        tally.add(rejected(0, 4, 5, 19))
        tally.add(rejected(1))
        self.assertEqual((tally.familywise, tally.true_rejections), (1, 3))
        self.assertEqual(mt.fwe(tally), 1 / mt.TRIALS)


class Cutoffs(unittest.TestCase):
    """The cutoff for n statistics comes from the maximum of the first n columns."""

    def test_first_n_columns(self) -> None:
        """Columns hold 0, 1, ..., K - 1 plus a small spread: cutoff n is the n-th column's."""
        spread = np.linspace(0.0, 0.1, 101)[:, None]
        draws = spread + np.arange(K, dtype=float)
        got = mt.max_cutoffs(draws)
        self.assertEqual(list(got), list(range(1, K + 1)))
        for n in (1, 2, K):
            self.assertAlmostEqual(got[n], n - 1 + 0.095, places=12)


class Stream(unittest.TestCase):
    """The calibration draws come first, then one vector per trial."""

    def test_draw_order(self) -> None:
        """A reduced run consumes the stream as the replay does, step for step."""
        rng = np.random.default_rng(mt.SEED)
        with mock.patch.object(mt, "CALIBRATION_DRAWS", 50), mock.patch.object(mt, "TRIALS", 3):
            got = mt.simulate(rng)
        replay = np.random.default_rng(mt.SEED)
        m = mt.model()
        cutoffs = mt.max_cutoffs(replay.standard_normal((50, K)) @ m.chol.T)
        want = {method: mt.Tally() for method in mt.METHODS}
        for _ in range(3):
            w = m.theta + m.chol @ replay.standard_normal(K)
            p = 1 - norm.cdf(w)
            want["Bonferroni"].add(mt.bonferroni(p))
            want["Holm"].add(mt.holm(p))
            want["single-step max"].add(mt.single_step_max(w, cutoffs))
            want["StepM"].add(mt.stepm(w, cutoffs))
        self.assertEqual(got, want)
        self.assertEqual(list(got), list(mt.METHODS))
        self.assertEqual(rng.bit_generator.state, replay.bit_generator.state)


def tallies(*counts: tuple[int, int]) -> dict[str, mt.Tally]:
    """Return prepared tallies, (familywise, true_rejections) for each method in order."""
    return {method: mt.Tally(*count) for method, count in zip(mt.METHODS, counts, strict=True)}


class Conditions(unittest.TestCase):
    """Four FWE limits, then the power ordering and the dependence comparison."""

    def test_fwe_limit_is_strict(self) -> None:
        """At most ALPHA plus three standard errors passes; the next trial fails it."""
        limit = mt.ALPHA + 3 * np.sqrt(0.05 * 0.95 / mt.TRIALS)
        at = int(limit * mt.TRIALS)
        ok = (10, 40), (10, 50), (at, 60), (10, 70)
        self.assertEqual(mt.failed_conditions(tallies(*ok)), [])
        over = (10, 40), (10, 50), (at + 1, 60), (at + 1, 70)
        self.assertEqual(
            mt.failed_conditions(tallies(*over)),
            ["single-step max FWE above alpha", "StepM FWE above alpha"],
        )

    def test_power_comparisons(self) -> None:
        """Ties pass the ordering but not single-step max over Holm; failures keep their order."""
        self.assertEqual(
            mt.failed_conditions(tallies((0, 50), (0, 50), (0, 50), (0, 50))),
            ["dependence-aware method not more powerful than Holm at rho 0.8"],
        )
        self.assertEqual(
            mt.failed_conditions(tallies((0, 50), (0, 40), (0, 60), (0, 55))),
            ["power ordering"],
        )


class Report(unittest.TestCase):
    """Prepared tallies: the method summaries, then BAD lines only for failures."""

    def run_with(self, prepared: dict[str, mt.Tally]) -> tuple[int, str]:
        """Return main's status and output with the simulation answered by prepared."""
        out = io.StringIO()
        with (
            mock.patch.object(mt, "simulate", return_value=prepared),
            contextlib.redirect_stdout(out),
        ):
            status = mt.main()
        return status, out.getvalue()

    def test_passing_and_failing_output(self) -> None:
        """FWE and the share of false nulls rejected, per method; then the verdict."""
        status, out = self.run_with(tallies((56, 11332), (68, 11625), (170, 14574), (185, 14737)))
        self.assertEqual(status, 0)
        self.assertEqual(
            out,
            "  Bonferroni      : FWE 0.014  share of false nulls rejected 0.567\n"
            "  Holm            : FWE 0.017  share of false nulls rejected 0.581\n"
            "  single-step max : FWE 0.043  share of false nulls rejected 0.729\n"
            "  StepM           : FWE 0.046  share of false nulls rejected 0.737\n"
            "all checks passed\n",
        )
        status, out = self.run_with(tallies((0, 120), (0, 120), (0, 120), (0, 120)))
        self.assertEqual(status, 1)
        self.assertTrue(
            out.endswith(
                "rejected 0.006\nBAD dependence-aware method not more powerful than Holm at "
                "rho 0.8\n"
            )
        )


if __name__ == "__main__":
    unittest.main()
