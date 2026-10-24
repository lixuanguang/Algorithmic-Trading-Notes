"""Tests of the label-span indicator and uniqueness helpers.

The demonstration's full run is tested in test_checks.py. These pin down the guard for a time
that no label uses (uniqueness 0 there, not 0/0) against hand-computed values.

Run: make test (uv run --frozen --no-editable pytest)
"""

# standard library imports
import unittest

# third party library imports
import numpy as np

# project library imports
from trading_notes.numerical import financial_labels as fl


class Uniqueness(unittest.TestCase):
    """Concurrency per time and average uniqueness per label."""

    def test_unused_time_contributes_nothing(self) -> None:
        """Rows (1, 0), (0, 0), (1, 1): concurrency 1, 0, 2; uniqueness (1 + 1/2)/2 and 1/2."""
        m = fl.ind_matrix(
            [(0, 1), (2, 3)], [1, 2, 3], lambda a, b, t: float(t in (1, 3) and (a == 0 or t == 3))
        )
        np.testing.assert_array_equal(m, [[1.0, 0.0], [0.0, 0.0], [1.0, 1.0]])
        with np.errstate(all="raise"):
            c, u = fl.avg_u(m)
        np.testing.assert_array_equal(c, [1.0, 0.0, 2.0])
        np.testing.assert_array_equal(u, [0.75, 0.5])


if __name__ == "__main__":
    unittest.main()
