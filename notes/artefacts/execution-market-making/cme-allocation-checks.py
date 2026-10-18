"""source verification (2026-10-17): CME Globex allocation steps (Client Systems Wiki, "CME Globex Matching Algorithm Steps",
version 5, 2 June 2026), reproduced on the page's own examples.

1. Pro Rata: floor(q_i / sum(q) * M), allocated only if floor >= PR Min (= 2 in the example); 50-lot sell against
   5, 9, 57, 4, 28, 300 gives 0, 0, 7, 0, 3, 37 (47 lots), remaining 5, 9, 50, 4, 25, 263.
2. Leveling (algorithm K): one lot each to orders that took part in Pro Rata and got nothing, by working quantity then
   time; 3 lots left go to the 9, 5 and 4 lot orders.
3. Split: 49 lots at 100/0, 20/80, 40/60, 0/100 give FIFO 49, 10, 20, 0 (FIFO rounded up) and Pro Rata the rest.
4. FIFO examples: 50 against 5, 9, 57 ... leaves 21 on order 3; with order 2 a display order showing 10, 22.
Run: uv run python cme-allocation-checks.py   (standard library). Exits non-zero on failure.
"""

# standard library imports
import math
import sys

fails = []


def same(name, got, want):
    ok = got == want
    print(f"  {'ok ' if ok else 'BAD'} {name}: {got} (want {want})")
    if not ok:
        fails.append(name)


q = [5, 9, 57, 4, 28, 300]
M, prmin = 50, 2
raw = [math.floor(x / sum(q) * M) for x in q]
alloc = [a if a >= prmin else 0 for a in raw]
same("Pro Rata rounded down", raw, [0, 1, 7, 0, 3, 37])
same("Pro Rata allocated (PR Min 2)", alloc, [0, 0, 7, 0, 3, 37])
same("remaining after Pro Rata", [x - a for x, a in zip(q, alloc)], [5, 9, 50, 4, 25, 263])
left = M - sum(alloc)
same("lots left for Leveling", left, 3)
qual = sorted([i for i in range(6) if alloc[i] == 0], key=lambda i: (-q[i], i))
lev = [0] * 6
for i in qual[:left]:
    lev[i] = 1
same("Leveling order of qualifying orders (1-based)", [i + 1 for i in qual], [2, 1, 4])
same(
    "remaining after Leveling",
    [x - a - l for x, a, l in zip(q, alloc, lev)],
    [4, 8, 50, 3, 25, 263],
)
for pct, want in [(100, 49), (20, 10), (40, 20), (0, 0)]:
    f = math.ceil(49 * pct / 100)
    same(f"Split {pct}/{100 - pct}: FIFO, Pro Rata", (f, 49 - f), (want, 49 - want))


def fifo(qs, m):
    out = []
    for x in qs:
        take = min(x, m)
        out.append(x - take)
        m -= take
    return out


same("FIFO example 1, order 3 remaining", fifo(q, 50)[2], 21)
same(
    "FIFO example 2 (order 2 displays 10), order 3 remaining",
    fifo([5, 10, 57, 4, 28, 300], 50)[2],
    22,
)
if fails:
    print("\nFAILED:", fails)
    sys.exit(1)
print("\nall checks passed")
