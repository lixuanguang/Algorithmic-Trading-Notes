"""Tests of the finite-difference operator's upwinding and the grid read-out.

The example's full run is tested in test_checks.py, which checks the upwinded node at one grid
size. These check, at several sizes and rate differentials, that every off-diagonal coefficient
is non-negative and that upwinding happens exactly where sigma^2 i < |r - q|.

Run: make test (uv run --frozen --no-editable pytest)
"""

# standard library imports
import unittest
from unittest import mock

# third party library imports
import numpy as np

# project library imports
from trading_notes.numerical import numerical_pricing as npr


class Coefficients(unittest.TestCase):
    """Central differences, upwinded near S = 0 when the drift dominates."""

    def test_off_diagonals_are_nonnegative(self) -> None:
        """a_i, c_i >= 0 on every interior node; upwinded nodes are those with sigma^2 i < r - q."""
        for r in (0.01, 0.05, 0.20):
            for M in (50, 150, 400):
                with self.subTest(r=r, M=M), mock.patch.object(npr, "R", r):
                    a, _, c, up = npr.coefficients(M)
                    i = np.arange(1, M)
                    self.assertTrue((a >= 0).all() and (c >= 0).all())
                    np.testing.assert_array_equal(up, npr.SG**2 * i < r)

    def test_value_at_reads_the_nearest_node(self) -> None:
        """S = 100 is node 50 of a 150-step grid on [0, 300]."""
        S = np.arange(151, dtype=np.float64) * 2.0
        V = np.arange(151, dtype=np.float64)
        self.assertEqual(npr.value_at(V, S), 50.0)


if __name__ == "__main__":
    unittest.main()
