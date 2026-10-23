"""source verification (2026-10-17): checks behind meth:purged-embargoed-cross-validation (Lopez de Prado, AFML, chap. 7).

1. The three overlap conditions of p. 106 (t_j0 <= t_i0 <= t_j1, t_j0 <= t_i1 <= t_j1, t_i0 <= t_j0 <= t_j1 <= t_i1)
   are equivalent to the closed intervals [t_i0, t_i1] and [t_j0, t_j1] intersecting (exhaustive check on a grid).
2. Snippet 7.3's PurgedKFold.split, re-implemented with numpy from the printed code (p. 109), on a toy series of
   20 labels each spanning 3 bars: the left training set is the observations whose label ends at or before the start
   of the test block (t1 <= t0); the right one starts at the first observation starting at or after the latest test
   label end, plus the embargo counted in observations (int(N * pctEmbargo)).
   Consequence, found here: a training label that ends exactly at the test block's first bar, or starts exactly at the
   last test label's end, is kept by the class but overlaps under the closed-interval rule of p. 106 (one shared bar).
Run: uv run --frozen --no-editable python cv-checks.py   (numpy). Exits non-zero on failure.
"""

# standard library imports
import itertools
import sys

# third party library imports
import numpy as np

fails = []


def truth(name, cond):
    print(f"  {'ok ' if cond else 'BAD'} {name}")
    if not cond:
        fails.append(name)


print("== 1. Overlap conditions against interval intersection")
ok = True
for ti0, ti1, tj0, tj1 in itertools.product(range(6), repeat=4):
    if ti0 > ti1 or tj0 > tj1:
        continue
    three = (tj0 <= ti0 <= tj1) or (tj0 <= ti1 <= tj1) or (ti0 <= tj0 <= tj1 <= ti1)
    inter = max(ti0, tj0) <= min(ti1, tj1)
    ok &= three == inter
truth("three conditions == closed intervals intersect, all cases on 0..5", ok)

print("\n== 2. PurgedKFold index sets (printed Snippet 7.3)")
N, span = 20, 3
start = np.arange(N)  # t1.index: label start bar
end = start + span  # t1.values: label end bar


def purged_kfold(n_splits, pct_embargo):
    indices = np.arange(N)
    mbrg = int(N * pct_embargo)
    test_starts = [(i[0], i[-1] + 1) for i in np.array_split(np.arange(N), n_splits)]
    for i, j in test_starts:
        t0 = start[i]
        test_indices = indices[i:j]
        max_t1_idx = np.searchsorted(
            start, end[test_indices].max()
        )  # side='left' as in pandas default
        train_indices = np.searchsorted(start, start[end <= t0])
        if max_t1_idx < N:
            train_indices = np.concatenate((train_indices, indices[max_t1_idx + mbrg :]))
        yield train_indices, test_indices


folds = list(purged_kfold(4, 0.1))
tr, te = folds[1]  # test block 5..9, labels span 5..12
truth("test block of fold 2 is observations 5-9", list(te) == [5, 6, 7, 8, 9])
truth(
    "left training set = labels ending at or before bar 5 (observations 0-2)",
    list(tr[tr < 5]) == [0, 1, 2],
)
truth("right training set starts at 12 + embargo 2 = observation 14", tr[tr > 9].min() == 14)
closed = [
    i
    for i in range(N)
    if i not in te and all(max(start[i], start[j]) > min(end[i], end[j]) for j in te)
]
truth(
    "closed-interval purge drops observations 2 (ends at bar 5) and 12 (starts at bar 12) and keeps 13",
    2 not in closed and 13 in closed and 12 not in closed,
)
kept_but_touching = [
    i for i in tr if any(max(start[i], start[j]) == min(end[i], end[j]) for j in te)
]
truth(
    "class keeps observation 2, whose label touches the test block at one bar",
    kept_but_touching == [2],
)
tr0, _ = list(purged_kfold(4, 0.0))[1]
truth(
    "without embargo the right set starts at observation 12, which touches bar 12",
    tr0[tr0 > 9].min() == 12,
)

if fails:
    print("\nFAILED:", fails)
    sys.exit(1)
print("\nall checks passed")
