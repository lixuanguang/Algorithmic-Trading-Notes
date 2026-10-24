"""Checks behind meth:purged-embargoed-cross-validation.

Source verification (2026-10-17): Lopez de Prado, AFML, chap. 7.

1. The three overlap conditions of p. 106 (t_j0 <= t_i0 <= t_j1, t_j0 <= t_i1 <= t_j1,
   t_i0 <= t_j0 <= t_j1 <= t_i1) are equivalent to the closed intervals [t_i0, t_i1] and
   [t_j0, t_j1] intersecting (exhaustive check on a grid).
2. Snippet 7.3's PurgedKFold.split, re-implemented with numpy from the printed code (p. 109),
   on a toy series of 20 labels each spanning 3 bars: the left training set is the
   observations whose label ends at or before the start of the test block (t1 <= t0); the
   right one starts at the first observation starting at or after the latest test label end,
   plus the embargo counted in observations (int(N * pctEmbargo)).
   Consequence, found here: a training label that ends exactly at the test block's first bar,
   or starts exactly at the last test label's end, is kept by the class but overlaps under the
   closed-interval rule of p. 106 (one shared bar).
Run: uv run --frozen --no-editable python -m trading_notes.numerical.purged_cv (numpy).
Exits non-zero on failure.
"""

import itertools
import sys
from collections.abc import Iterator
from typing import Final

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.report import CheckReport

type Indices = NDArray[np.intp]

N: Final = 20  # observations, one label starting at each bar
SPAN: Final = 3  # bars spanned by each label


def purged_kfold(
    start: Indices, end: Indices, n_splits: int, pct_embargo: float
) -> Iterator[tuple[Indices, Indices]]:
    """Yield (train, test) observation indices as the printed Snippet 7.3 computes them.

    Args:
        start: Each label's start bar, increasing (t1.index).
        end: Each label's end bar (t1.values).
        n_splits: The number of contiguous test blocks.
        pct_embargo: The embargo as a fraction of the observations, truncated to a count.
    """
    indices = np.arange(N)
    mbrg = int(N * pct_embargo)
    test_starts = [(i[0], i[-1] + 1) for i in np.array_split(np.arange(N), n_splits)]
    for i, j in test_starts:
        t0 = start[i]
        test_indices = indices[i:j]
        max_t1_idx = np.searchsorted(start, end[test_indices].max())  # side='left' as in pandas
        train_indices = np.searchsorted(start, start[end <= t0])
        if max_t1_idx < N:
            train_indices = np.concatenate((train_indices, indices[max_t1_idx + mbrg :]))
        yield train_indices, test_indices


def check_overlap_conditions(report: CheckReport) -> None:
    """1. The three conditions agree with closed-interval intersection on every grid case."""
    print("== 1. Overlap conditions against interval intersection")
    ok = True
    for ti0, ti1, tj0, tj1 in itertools.product(range(6), repeat=4):
        if ti0 > ti1 or tj0 > tj1:
            continue
        three = (tj0 <= ti0 <= tj1) or (tj0 <= ti1 <= tj1) or (ti0 <= tj0 <= tj1 <= ti1)
        inter = max(ti0, tj0) <= min(ti1, tj1)
        ok &= three == inter
    report.ok("three conditions == closed intervals intersect, all cases on 0..5", ok)


def check_purged_kfold(report: CheckReport) -> None:
    """2. The second fold's index sets, against the closed-interval purge."""
    print("\n== 2. PurgedKFold index sets (printed Snippet 7.3)")
    start = np.arange(N)  # t1.index: label start bar
    end = start + SPAN  # t1.values: label end bar
    folds = list(purged_kfold(start, end, 4, 0.1))
    tr, te = folds[1]  # test block 5..9, labels span 5..12
    report.ok("test block of fold 2 is observations 5-9", list(te) == [5, 6, 7, 8, 9])
    report.ok(
        "left training set = labels ending at or before bar 5 (observations 0-2)",
        list(tr[tr < 5]) == [0, 1, 2],
    )
    report.ok(
        "right training set starts at 12 + embargo 2 = observation 14",
        bool(tr[tr > 9].min() == 14),
    )
    closed = [
        i
        for i in range(N)
        if i not in te and all(max(start[i], start[j]) > min(end[i], end[j]) for j in te)
    ]
    report.ok(
        "closed-interval purge drops observations 2 (ends at bar 5) and 12 (starts at bar 12)"
        " and keeps 13",
        2 not in closed and 13 in closed and 12 not in closed,
    )
    kept_but_touching = [
        i for i in tr if any(max(start[i], start[j]) == min(end[i], end[j]) for j in te)
    ]
    report.ok(
        "class keeps observation 2, whose label touches the test block at one bar",
        kept_but_touching == [2],
    )
    tr0, _ = list(purged_kfold(start, end, 4, 0.0))[1]
    report.ok(
        "without embargo the right set starts at observation 12, which touches bar 12",
        bool(tr0[tr0 > 9].min() == 12),
    )


def main() -> int:
    """Run the two parts with one report.

    Returns:
        The exit status, 0 or 1.
    """
    report = CheckReport()
    check_overlap_conditions(report)
    check_purged_kfold(report)
    if report.failures:
        print("\nFAILED:", report.failures)
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
