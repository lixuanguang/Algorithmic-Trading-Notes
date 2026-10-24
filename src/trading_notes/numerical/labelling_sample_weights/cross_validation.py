"""Purged and embargoed k-fold cross-validation of overlapping labels (AFML Snippet 7.3)."""

from collections.abc import Iterator

import numpy as np
from numpy.typing import NDArray

from trading_notes.records import Record

type Indices = NDArray[np.intp]


class LabelSpans(Record):
    """The bars spanned by each label, one label per observation.

    Attributes:
        start: Each label's start bar, increasing (t1.index).
        end: Each label's end bar (t1.values).
    """

    start: Indices
    end: Indices

    def purged_kfold(self, n_splits: int, pct_embargo: float) -> Iterator[tuple[Indices, Indices]]:
        """Yield (train, test) observation indices as the printed Snippet 7.3 computes them.

        Args:
            n_splits: The number of contiguous test blocks.
            pct_embargo: The embargo as a fraction of the observations, truncated to a count.
        """
        start, end = self.start, self.end
        n = len(start)
        indices = np.arange(n)
        mbrg = int(n * pct_embargo)
        test_starts = [(i[0], i[-1] + 1) for i in np.array_split(np.arange(n), n_splits)]
        for i, j in test_starts:
            t0 = start[i]
            test_indices = indices[i:j]
            max_t1_idx = np.searchsorted(start, end[test_indices].max())  # side='left' as pandas
            train_indices = np.searchsorted(start, start[end <= t0])
            if max_t1_idx < n:
                train_indices = np.concatenate((train_indices, indices[max_t1_idx + mbrg :]))
            yield train_indices, test_indices
