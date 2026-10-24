"""Tests of the linear-projection example's references, conventions and stream.

The example's full run is tested in test_checks.py. These pin down the analytical variance
share, the slope's mixed covariance and variance divisors, the half-open bins of the
joint-normal check, and the order in which the one generator is drawn, with small inputs.

Run: make test (uv run --frozen --no-editable pytest)
"""

import contextlib
import io
import unittest
from collections.abc import Mapping
from unittest import mock

import numpy as np

from trading_notes.numerical import linear_projection as lp
from trading_notes.numerical.report import CheckReport

# The midpoints of the eight bins of width 0.5 between -2 and 2.
MIDPOINTS = np.arange(-1.75, 2.0, 0.5)


class References(unittest.TestCase):
    """The conditional mean and its explained share are stated, not estimated."""

    def test_explained_share_is_analytical(self) -> None:
        """2 / (2 + s^2): two thirds at s = 1, all of it without noise."""
        self.assertEqual(lp.explained_share(1.0), 2 / 3)
        self.assertEqual(lp.explained_share(0.0), 1.0)

    def test_conditional_mean(self) -> None:
        """E[r | g] = g^2 - 1."""
        np.testing.assert_array_equal(
            lp.conditional_mean(np.array([-2.0, 0.0, 1.0])), [3.0, -1.0, 0.0]
        )


class Slope(unittest.TestCase):
    """The slope divides np.cov's covariance (N - 1) by np.var's variance (N)."""

    def test_mixed_divisors_are_kept(self) -> None:
        """For r = g on three points the slope is 3/2, not the projection's exact 1."""
        g = np.array([0.0, 1.0, 2.0])
        self.assertEqual(lp.projection_slope(lp.NonlinearSample(g, g.copy())), 1.5)


class Bins(unittest.TestCase):
    """Eight bins [lo, hi) from -2 to 2; points outside them are ignored."""

    def test_on_the_line_gives_no_gap(self) -> None:
        """One point on r = RHO g in each bin gives a zero gap."""
        self.assertEqual(lp.largest_bin_gap(MIDPOINTS, lp.RHO * MIDPOINTS), 0.0)

    def test_outer_edges(self) -> None:
        """-2 falls in the first bin; 2 and beyond, or below -2, fall in none."""
        g = np.r_[MIDPOINTS, 2.0, 2.5, -2.5]
        r = np.r_[lp.RHO * MIDPOINTS, 100.0, 100.0, 100.0]
        self.assertEqual(lp.largest_bin_gap(g, r), 0.0)
        g = np.r_[MIDPOINTS, -2.0]
        r = np.r_[lp.RHO * MIDPOINTS, lp.RHO * -2.0 + 1.0]
        self.assertAlmostEqual(lp.largest_bin_gap(g, r), 0.5, places=15)

    def test_inner_edge_belongs_to_the_upper_bin(self) -> None:
        """A signal of 0 joins [0, 0.5): it leaves the gap of 1 in [-0.5, 0) undiluted."""
        r = lp.RHO * MIDPOINTS
        r[3] += 1.0  # the midpoint of [-0.5, 0)
        self.assertAlmostEqual(lp.largest_bin_gap(MIDPOINTS, r), 1.0, places=15)
        g0, r0 = np.r_[MIDPOINTS, 0.0], np.r_[r, 0.0]
        self.assertAlmostEqual(lp.largest_bin_gap(g0, r0), 1.0, places=15)
        # In [-0.5, 0) the extra point on the line would have halved that bin's gap.
        below = np.r_[MIDPOINTS, -1e-12], np.r_[r, lp.RHO * -1e-12]
        self.assertAlmostEqual(lp.largest_bin_gap(*below), 0.5, places=12)


class Stream(unittest.TestCase):
    """All signals, then all noise, then the joint-normal sample, on one generator."""

    def test_nonlinear_sample_draw_order(self) -> None:
        """The signal takes the first N normals and the noise the next N."""
        with mock.patch.object(lp, "N", 6):
            rng = np.random.default_rng(lp.SEED)
            sample = lp.simulate_nonlinear(rng)
        replay = np.random.default_rng(lp.SEED)
        g = replay.standard_normal(6)
        e = replay.standard_normal(6)
        np.testing.assert_array_equal(sample.g, g)
        np.testing.assert_array_equal(sample.r, g**2 - 1 + lp.S * e)
        self.assertEqual(rng.bit_generator.state, replay.bit_generator.state)

    def test_joint_normal_sample_continues_the_stream(self) -> None:
        """The joint-normal check gets the generator after the first 2N draws."""
        seen: list[Mapping[str, object]] = []

        def record(report: CheckReport, rng: np.random.Generator) -> None:
            seen.append(rng.bit_generator.state)

        with (
            mock.patch.object(lp, "N", 6),
            mock.patch.object(lp, "check_joint_normality", record),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            lp.main()
        replay = np.random.default_rng(lp.SEED)
        replay.standard_normal(12)
        self.assertEqual(seen, [replay.bit_generator.state])


if __name__ == "__main__":
    unittest.main()
