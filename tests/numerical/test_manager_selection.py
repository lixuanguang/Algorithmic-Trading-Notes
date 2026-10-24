"""Tests of the style-analysis solver boundary.

The example's full run is tested in test_checks.py. These pin down what style_fit returns from
SciPy's dynamic result: the weights as a float64 vector on the simplex, the objective at them
and the success flag, on objectives with known minimisers.

Run: make test (uv run --frozen --no-editable pytest)
"""

# standard library imports
import unittest

# third party library imports
import numpy as np
from numpy.typing import NDArray

# project library imports
from trading_notes.numerical import manager_selection as ms


class StyleFitBoundary(unittest.TestCase):
    """SLSQP over long-only weights that sum to one."""

    def test_interior_minimiser(self) -> None:
        """A target inside the simplex is recovered, with a float objective and success."""
        target = np.array([0.1, 0.2, 0.3, 0.25, 0.15])

        def distance(w: NDArray[np.float64]) -> float:
            return float(((w - target) ** 2).sum())

        fit = ms.style_fit(distance)
        self.assertIs(type(fit.fun), float)
        self.assertIs(fit.success, True)
        self.assertEqual((fit.x.dtype, fit.x.shape), (np.dtype(np.float64), (5,)))
        np.testing.assert_allclose(fit.x, target, atol=1e-8)

    def test_bounds_bind(self) -> None:
        """A target outside the simplex lands on its face: nonnegative weights summing to one."""
        target = np.array([0.6, 0.6, -0.2, 0.0, 0.0])

        def distance(w: NDArray[np.float64]) -> float:
            return float(((w - target) ** 2).sum())

        fit = ms.style_fit(distance)
        self.assertAlmostEqual(float(fit.x.sum()), 1.0, places=9)
        self.assertGreaterEqual(float(fit.x.min()), -1e-9)
        np.testing.assert_allclose(fit.x, [0.5, 0.5, 0.0, 0.0, 0.0], atol=1e-7)
        self.assertEqual(ms.budget(np.array([0.5, 0.5, 0.0, 0.0, 0.0])), 0.0)


if __name__ == "__main__":
    unittest.main()
