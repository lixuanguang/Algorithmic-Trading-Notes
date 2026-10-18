"""source verification (2026-10-17): an own, synthetic illustration behind meth:bitemporal-reference-tables.

A vendor first records a 2-for-1 split of stock XYZ effective 2026-03-02 (actual time) on 2026-03-03 (record
time), then corrects it on 2026-03-20 to a 3-for-2 split. Following Fowler's actual/record distinction, every row
carries an actual-time range and a record-time range, and record history is append-only. Checked:
1. the factor "as known on 2026-03-10" for 2026-03-05 is the first (wrong) one, as a backtest dated 2026-03-10 saw;
2. the factor "as known now" is the corrected one;
3. before the record date of the first entry, no split is known even for actual dates after the split;
4. the correction appends rows and closes record ranges; no earlier row is overwritten.
Synthetic data only. Run: uv run python bitemporal-check.py (standard library). Exits non-zero on failure.
"""

# standard library imports
import datetime as dt
import sys

D = dt.date
INF = D(9999, 12, 31)
rows = []  # (record_from, record_to, actual_from, actual_to, split_factor)


def record(record_date, actual_from, factor):
    """Append-only: close the open record range of rows overlapping actual_from onward, then append new rows."""
    global rows
    new = []
    for r in rows:
        rf, rt, af, at, f = r
        if rt == INF and at >= actual_from:
            new.append((rf, record_date - dt.timedelta(days=1), af, at, f))  # closed copy
            if af < actual_from:
                new.append((record_date, INF, af, actual_from - dt.timedelta(days=1), f))
        else:
            new.append(r)
    new.append((record_date, INF, actual_from, INF, factor))
    before = set(rows)
    rows = new
    return before


def factor_at(actual, known_on):
    for rf, rt, af, at, f in rows:
        if rf <= known_on <= rt and af <= actual <= at:
            return f
    return 1.0


rows.append((D(2000, 1, 1), INF, D(2000, 1, 1), INF, 1.0))
record(D(2026, 3, 3), D(2026, 3, 2), 2.0)
snapshot = [r for r in rows if r[1] != INF]
record(D(2026, 3, 20), D(2026, 3, 2), 1.5)
fails = []


def same(name, got, want):
    ok = got == want
    print(f"  {'ok ' if ok else 'BAD'} {name}: {got} (want {want})")
    if not ok:
        fails.append(name)


same("as known on 2026-03-10, factor for 2026-03-05", factor_at(D(2026, 3, 5), D(2026, 3, 10)), 2.0)
same("as known now, factor for 2026-03-05", factor_at(D(2026, 3, 5), D(2026, 10, 17)), 1.5)
same("as known on 2026-03-02, factor for 2026-03-05", factor_at(D(2026, 3, 5), D(2026, 3, 2)), 1.0)
same("closed rows survive the correction unchanged", all(r in rows for r in snapshot), True)
if fails:
    sys.exit(1)
print("all checks passed")
