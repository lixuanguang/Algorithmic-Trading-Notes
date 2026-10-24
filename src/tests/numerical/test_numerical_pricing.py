"""Tests of the finite-difference operator's upwinding and the grid read-out."""

# The example's full run is tested in test_checks.py, which checks the upwinded node at one grid
# size. These check, at several sizes and rate differentials, that every off-diagonal coefficient
# is non-negative and that upwinding happens exactly where sigma^2 i < |r - q|.

import unittest

import numpy as np

from trading_notes.numerical.numerical_methods.numerical_pricing_checks import GRID, PUT
from trading_notes.numerical.numerical_methods.put_pricing import FiniteDifferenceGrid, GridValues


class Coefficients(unittest.TestCase):
    """Central differences, upwinded near S = 0 when the drift dominates."""

    def test_off_diagonals_are_nonnegative(self) -> None:
        """a_i, c_i >= 0 on every interior node; upwinded nodes are those with sigma^2 i < r - q."""
        for r in (0.01, 0.05, 0.20):
            grid = FiniteDifferenceGrid(option=PUT.model_copy(update={"rate": r}), s_max=GRID.s_max)
            for M in (50, 150, 400):
                with self.subTest(r=r, M=M):
                    a, _, c, up = grid.coefficients(M)
                    i = np.arange(1, M)
                    self.assertTrue((a >= 0).all() and (c >= 0).all())
                    np.testing.assert_array_equal(up, PUT.vol**2 * i < r)

    def test_value_at_reads_the_nearest_node(self) -> None:
        """S = 100 is node 50 of a 150-step grid on [0, 300]."""
        values = GridValues(
            values=np.arange(151, dtype=np.float64), prices=np.arange(151, dtype=np.float64) * 2.0
        )
        self.assertEqual(values.at(100.0), 50.0)


if __name__ == "__main__":
    unittest.main()
