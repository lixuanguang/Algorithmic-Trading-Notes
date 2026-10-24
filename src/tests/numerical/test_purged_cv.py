"""Tests of the printed Snippet 7.3 split's index conventions.

The example's full run is tested in test_checks.py. These pin down that the folds partition
the observations into contiguous test blocks that training never touches, and the purge and
embargo conventions on a label span other than the example's.

Run: make test (uv run --frozen --no-editable pytest)
"""

import unittest

import numpy as np

from trading_notes.numerical import purged_cv as pcv


class Folds(unittest.TestCase):
    """Contiguous test blocks that cover every observation once; training excludes them."""

    def test_partition(self) -> None:
        """With or without an embargo, the test blocks partition 0..N-1 in order."""
        start = np.arange(pcv.N)
        for pct in (0.0, 0.1):
            with self.subTest(pct=pct):
                folds = list(pcv.purged_kfold(start, start + pcv.SPAN, 4, pct))
                tests = np.concatenate([te for _, te in folds])
                np.testing.assert_array_equal(tests, start)
                for tr, te in folds:
                    self.assertFalse(np.isin(tr, te).any())


class Conventions(unittest.TestCase):
    """The left and right training sets.

    Left: labels ending at or before the test block's first bar. Right: from the first start at
    or after the latest test label end (side='left'), plus int(N * pct) observations.
    """

    def test_one_bar_labels(self) -> None:
        """Labels [i, i + 1]: fold 2 (test 5..9) trains on 0..4 and from 10 + embargo."""
        start = np.arange(pcv.N)
        tr, te = list(pcv.purged_kfold(start, start + 1, 4, 0.0))[1]
        np.testing.assert_array_equal(te, np.arange(5, 10))
        np.testing.assert_array_equal(tr, np.r_[0:5, 10:20])
        tr, _ = list(pcv.purged_kfold(start, start + 1, 4, 0.25))[1]
        np.testing.assert_array_equal(tr, np.r_[0:5, 15:20])  # embargo int(20 * 0.25) = 5

    def test_last_fold_has_no_right_set(self) -> None:
        """When the latest test label ends past the last start, nothing is appended."""
        start = np.arange(pcv.N)
        tr, te = list(pcv.purged_kfold(start, start + pcv.SPAN, 4, 0.1))[-1]
        np.testing.assert_array_equal(te, np.arange(15, 20))
        np.testing.assert_array_equal(tr, np.arange(0, 13))


if __name__ == "__main__":
    unittest.main()
