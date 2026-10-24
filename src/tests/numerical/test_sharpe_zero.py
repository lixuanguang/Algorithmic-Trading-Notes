"""Tests of the Sharpe-zero example's chunked estimator, samplers and stream."""

# The example's checks run in test_checks.py. These pin down the chunk shapes and order, the ddof
# 0 standard deviation, the two samplers' laws and that both checks draw from one stream, with
# small samples.

import contextlib
import io
import math
import unittest
from unittest import mock

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.backtest_evaluation import sharpe_zero_checks as sz


class RootTSharpe(unittest.TestCase):
    """reps // chunk draws of chunk x T, in order; the remainder of reps is not drawn."""

    def test_chunks_shapes_and_order(self) -> None:
        """Each draw is (chunk, T); results follow the draws; 260 reps of 250 draw one chunk."""
        shapes: list[tuple[int, int]] = []

        def counting(size: tuple[int, int]) -> NDArray[np.float64]:
            shapes.append(size)
            # Row r of draw d has mean d + r and population standard deviation 1.
            d = len(shapes)
            base = np.arange(size[0], dtype=np.float64)[:, None] + d
            rows: NDArray[np.float64] = base + np.tile([-1.0, 1.0], (size[0], size[1] // 2))
            return rows

        z = sz.root_t_sr(counting, 4, 6, chunk=3)
        self.assertEqual(shapes, [(3, 4), (3, 4)])
        np.testing.assert_allclose(z, 2 * np.array([1, 2, 3, 2, 3, 4]), rtol=1e-15)
        shapes.clear()
        self.assertEqual(len(sz.root_t_sr(counting, 2, 260)), 250)
        self.assertEqual(shapes, [(250, 2)])

    def test_population_standard_deviation_and_true_sr(self) -> None:
        """Rows (1, 3) have mean 2 and ddof-0 deviation 1, so SR_hat = 2; sr_true is subtracted."""

        def fixed(size: tuple[int, int]) -> NDArray[np.float64]:
            return np.tile([1.0, 3.0], (size[0], 1))

        self.assertEqual(sz.root_t_sr(fixed, 2, 1, chunk=1).tolist(), [math.sqrt(2) * 2])
        self.assertEqual(
            sz.root_t_sr(fixed, 2, 1, sr_true=0.5, chunk=1).tolist(), [math.sqrt(2) * 1.5]
        )


class Samplers(unittest.TestCase):
    """Centred Student-t3, and the three-point law with mean shift."""

    def test_student_t3_is_the_generators_draw(self) -> None:
        """The sampler returns standard_t(3, size) from the generator it was given."""
        draw = sz.student_t3(np.random.default_rng(4))
        got = draw((2, 5))
        np.testing.assert_array_equal(got, np.random.default_rng(4).standard_t(3, (2, 5)))
        self.assertEqual(got.dtype, np.float64)

    def test_three_point_law_moments_and_shift(self) -> None:
        """Values -sqrt(3), 0, sqrt(3) with 1/6, 2/3, 1/6: variance 1, kurtosis 3; then shifted."""
        vals, probs = np.array(sz.THREE_POINT_VALUES), np.array(sz.THREE_POINT_PROBABILITIES)
        self.assertAlmostEqual(float(probs @ vals), 0.0, places=15)
        self.assertAlmostEqual(float(probs @ vals**2), 1.0, places=15)
        self.assertAlmostEqual(float(probs @ vals**4), 3.0, places=14)
        got = sz.shifted_three_point(np.random.default_rng(6), 0.5)((40, 3))
        replay = np.random.default_rng(6)
        np.testing.assert_array_equal(got, vals[replay.choice(3, size=(40, 3), p=probs)] + 0.5)
        self.assertEqual(
            set(np.round(got - 0.5, 12).ravel()), {-1.732050807569, 0.0, 1.732050807569}
        )


class Stream(unittest.TestCase):
    """main draws the Student-t samples, then the three-point samples, from one generator."""

    def test_one_seed_31_stream(self) -> None:
        """With each estimate reduced to one small draw, main's draws are one stream in order."""
        drawn: list[NDArray[np.float64]] = []

        def one_draw(
            draw: sz.Sampler, T: int, reps: int, sr_true: float = 0.0, chunk: int = 250
        ) -> NDArray[np.float64]:
            drawn.append(draw((2, 3)))
            return np.zeros(4)

        with (
            mock.patch.object(sz, "root_t_sr", one_draw),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            self.assertEqual(sz.main(), 1)
        replay = np.random.default_rng(sz.SEED)
        np.testing.assert_array_equal(drawn[0], replay.standard_t(3, (2, 3)))
        vals, probs = np.array(sz.THREE_POINT_VALUES), np.array(sz.THREE_POINT_PROBABILITIES)
        np.testing.assert_array_equal(drawn[1], vals[replay.choice(3, size=(2, 3), p=probs)] + 0.5)


if __name__ == "__main__":
    unittest.main()
