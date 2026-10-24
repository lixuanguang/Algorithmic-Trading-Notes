"""Tests of the drawdown-resampling example's measures, resamplers, stream and report.

The example's full run is tested in test_checks.py. These pin down the log drawdown from an
initial zero peak, the AR(1) burn-in, the bootstraps' wrap-around and restart draws, the order in
which the one stream is consumed, the two conditions and the failure-only report, with small
inputs or prepared results.

Run: make test (uv run --frozen --no-editable pytest)
"""

import contextlib
import io
import math
import unittest
from unittest import mock

import numpy as np

from trading_notes.numerical.backtest_evaluation import drawdown_resampling_checks as dd
from trading_notes.numerical.backtest_evaluation.drawdown_bootstrap import (
    DrawdownComparison,
    DrawdownExperiment,
    StationaryBootstrap,
    max_drawdown,
    shuffle_bootstrap,
)

MODEL = dd.EXPERIMENT.returns


class MaxDrawdown(unittest.TestCase):
    """Drawdowns are falls of log wealth from a running peak that starts at 0."""

    def test_initial_peak_and_log_units(self) -> None:
        """A first-month loss of 10% is a drawdown of -log(0.9); a later fall is measured too."""
        one = max_drawdown(np.array([-0.1]))
        self.assertIs(type(one), np.float64)
        self.assertAlmostEqual(float(one), -math.log(0.9), places=15)
        self.assertAlmostEqual(
            float(max_drawdown(np.array([0.1, -0.05, 0.02]))), -math.log(0.95), places=15
        )
        self.assertEqual(float(max_drawdown(np.array([0.1, 0.2]))), 0.0)

    def test_last_axis_of_a_batch(self) -> None:
        """Each row is measured on its own, into a float64 array with one value per row."""
        got = max_drawdown(np.array([[-0.1, 0.0], [0.0, 0.0]]))
        self.assertIsInstance(got, np.ndarray)
        assert isinstance(got, np.ndarray)
        self.assertEqual((got.shape, got.dtype), ((2,), np.float64))
        self.assertAlmostEqual(float(got[0]), -math.log(0.9), places=15)
        self.assertEqual(float(got[1]), 0.0)


class Paths(unittest.TestCase):
    """AR(1) paths keep T months after a burn-in of BURN_IN."""

    def test_burn_in_and_initialisation(self) -> None:
        """r_0 = mean + e_0, the recursion runs through the burn-in and only the last are kept."""
        m = MODEL
        paths = m.simulate(np.random.default_rng(2), 2)
        e = np.random.default_rng(2).normal(0, m.sd, (2, m.periods + m.burn_in))
        r = np.empty_like(e)
        r[:, 0] = m.mean + e[:, 0]
        for t in range(1, m.periods + m.burn_in):
            r[:, t] = m.mean + m.phi * (r[:, t - 1] - m.mean) + e[:, t]
        self.assertEqual(paths.shape, (2, m.periods))
        np.testing.assert_array_equal(paths, r[:, m.burn_in :])


class Bootstraps(unittest.TestCase):
    """Shuffles are permutations; blocks wrap around and restart with probability 1/L."""

    def test_shuffles_are_permutations_in_order(self) -> None:
        """B permutations, drawn one after another."""
        x = np.arange(5.0)
        got = shuffle_bootstrap(np.random.default_rng(3), x, 4)
        replay = np.random.default_rng(3)
        np.testing.assert_array_equal(got, np.array([replay.permutation(x) for _ in range(4)]))

    def test_long_blocks_wrap_around(self) -> None:
        """With no restarts a sample is x read circularly from its uniform start.

        Each sample draws its start, then one uniform after every observation, the last
        included.
        """
        x = np.arange(7.0)
        rng = np.random.default_rng(4)
        got = StationaryBootstrap(mean_block=10**12).resample(rng, x, 3)
        replay = np.random.default_rng(4)
        for row in got:
            start = replay.integers(7)
            np.testing.assert_array_equal(row, np.roll(x, -start))
            for _ in range(7):
                replay.random()
        self.assertEqual(rng.bit_generator.state, replay.bit_generator.state)

    def test_unit_blocks_restart_after_each_observation(self) -> None:
        """With L = 1 every uniform restarts the block, at a fresh uniform index."""
        x = np.arange(7.0)
        rng = np.random.default_rng(5)
        got = StationaryBootstrap(mean_block=1).resample(rng, x, 2)
        replay = np.random.default_rng(5)
        for row in got:
            starts = [replay.integers(7)]
            for _ in range(7):
                replay.random()
                starts.append(replay.integers(7))
            np.testing.assert_array_equal(row, x[starts[:-1]])
        self.assertEqual(rng.bit_generator.state, replay.bit_generator.state)


class Stream(unittest.TestCase):
    """Reference paths first; then each sample path, its shuffles and its blocks, in turn."""

    def test_draw_order(self) -> None:
        """A reduced run consumes the stream as the replay does, step for step."""
        small = dd.EXPERIMENT.model_copy(
            update={"reference_paths": 5, "sample_paths": 2, "replications": 3}
        )
        rng = np.random.default_rng(dd.SEED)
        run = small.run(rng)
        replay = np.random.default_rng(dd.SEED)
        ref = np.quantile(max_drawdown(MODEL.simulate(replay, 5)), 0.95)
        q_sh, q_st = [], []
        for _ in range(2):
            x = MODEL.simulate(replay, 1)[0]
            q_sh.append(np.quantile(max_drawdown(shuffle_bootstrap(replay, x, 3)), 0.95))
            q_st.append(np.quantile(max_drawdown(small.blocks.resample(replay, x, 3)), 0.95))
        want = DrawdownComparison(
            reference=float(ref),
            shuffle=float(np.median(q_sh)),
            stationary=float(np.median(q_st)),
        )
        self.assertEqual(run, want)
        self.assertEqual(rng.bit_generator.state, replay.bit_generator.state)


class Conditions(unittest.TestCase):
    """Shuffling must understate by more than 15%; blocks must be strictly closer."""

    def test_edges_and_order(self) -> None:
        """At exactly 85% or equal distances a condition fails; failures keep their order."""
        compare = DrawdownComparison
        self.assertEqual(
            dd.failed_conditions(compare(reference=1.0, shuffle=0.5, stationary=0.9)), []
        )
        self.assertEqual(
            dd.failed_conditions(compare(reference=1.0, shuffle=0.85, stationary=0.9)),
            ["shuffle does not understate"],
        )
        self.assertEqual(
            dd.failed_conditions(compare(reference=1.0, shuffle=0.5, stationary=1.5)),
            ["blocks not closer than shuffle"],
        )
        self.assertEqual(
            dd.failed_conditions(compare(reference=1.0, shuffle=1.0, stationary=1.0)),
            ["shuffle does not understate", "blocks not closer than shuffle"],
        )


class Report(unittest.TestCase):
    """Prepared results: the summaries, then BAD lines only for failures."""

    def run_with(self, run: DrawdownComparison) -> tuple[int, str]:
        """Return main's status and output with the experiment answered by run."""
        out = io.StringIO()
        with (
            mock.patch.object(DrawdownExperiment, "run", return_value=run),
            contextlib.redirect_stdout(out),
        ):
            status = dd.main()
        return status, out.getvalue()

    def test_passing_and_failing_output(self) -> None:
        """A pass ends with the explanatory ok line; failures print only BAD lines."""
        summaries = (
            "reference 95th percentile of max drawdown (log units): 1.000\n"
            "median bootstrap 95th percentile: shuffle {:.3f}, "
            "stationary-type blocks (L=12) {:.3f}\n"
        )
        self.assertEqual(
            self.run_with(DrawdownComparison(reference=1.0, shuffle=0.5, stationary=0.9)),
            (
                0,
                summaries.format(0.5, 0.9) + "ok  shuffling understates the drawdown tail under "
                "positive autocorrelation; blocks come closer\nall checks passed\n",
            ),
        )
        self.assertEqual(
            self.run_with(DrawdownComparison(reference=1.0, shuffle=1.0, stationary=1.0)),
            (
                1,
                summaries.format(1.0, 1.0)
                + "BAD shuffle does not understate\nBAD blocks not closer than shuffle\n",
            ),
        )


if __name__ == "__main__":
    unittest.main()
