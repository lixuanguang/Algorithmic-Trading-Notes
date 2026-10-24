"""source verification (2026-10-17): CME Globex allocation steps (Client Systems Wiki, "CME Globex Matching Algorithm Steps", version 5, 2 June 2026), reproduced on the page's own examples.

1. Pro Rata: floor(q_i / sum(q) * M), allocated only if floor >= PR Min (= 2 in the example); 50-lot sell against
   5, 9, 57, 4, 28, 300 gives 0, 0, 7, 0, 3, 37 (47 lots), remaining 5, 9, 50, 4, 25, 263.
2. Leveling (algorithm K): one lot each to orders that took part in Pro Rata and got nothing, by working quantity then
   time; 3 lots left go to the 9, 5 and 4 lot orders.
3. Split: 49 lots at 100/0, 20/80, 40/60, 0/100 give FIFO 49, 10, 20, 0 (FIFO rounded up) and Pro Rata the rest.
4. FIFO examples: 50 against 5, 9, 57 ... leaves 21 on order 3; with order 2 a display order showing 10, 22.
The expected allocations are the page's printed results, not recomputed here.
Run: uv run --frozen --no-editable python -m trading_notes.numerical.cme_allocation   (standard library).
Exits non-zero on failure.
"""

import math
import sys
from collections.abc import Sequence
from typing import Final

from trading_notes.numerical.report import CheckReport

# Resting quantities in time priority, the incoming sell, and the Pro Rata minimum.
QUANTITIES: Final = (5, 9, 57, 4, 28, 300)
INCOMING: Final = 50
PR_MIN: Final = 2
# Incoming quantity of the Split examples.
SPLIT_INCOMING: Final = 49


def pro_rata(q: Sequence[int], m: int) -> list[int]:
    """Return each order's Pro Rata share floor(q_i / sum(q) * M), before the minimum."""
    return [math.floor(x / sum(q) * m) for x in q]


def apply_minimum(raw: Sequence[int], prmin: int) -> list[int]:
    """Return the Pro Rata allocation: a share below PR Min is not allocated."""
    return [a if a >= prmin else 0 for a in raw]


def leveling_order(q: Sequence[int], alloc: Sequence[int]) -> list[int]:
    """Return the 0-based orders that qualify for Leveling, in Leveling order.

    An order qualifies when it took part in Pro Rata and got nothing; larger working quantity
    comes first, then earlier time (lower index).
    """
    return sorted([i for i in range(len(q)) if alloc[i] == 0], key=lambda i: (-q[i], i))


def leveling(q: Sequence[int], alloc: Sequence[int], left: int) -> list[int]:
    """Return the Leveling lots: one each to the first `left` qualifying orders."""
    lev = [0] * len(q)
    for i in leveling_order(q, alloc)[:left]:
        lev[i] = 1
    return lev


def split_fifo(m: int, pct: int) -> int:
    """Return the FIFO part of a Split allocation of m lots at pct percent, rounded up."""
    return math.ceil(m * pct / 100)


def fifo(qs: Sequence[int], m: int) -> list[int]:
    """Return each order's remaining quantity after FIFO allocation of m lots in time order."""
    out: list[int] = []
    for x in qs:
        take = min(x, m)
        out.append(x - take)
        m -= take
    return out


def check_pro_rata(report: CheckReport) -> list[int]:
    """Check step 1, Pro Rata with the minimum, and return the allocation."""
    q = QUANTITIES
    raw = pro_rata(q, INCOMING)
    alloc = apply_minimum(raw, PR_MIN)
    report.same("Pro Rata rounded down", raw, [0, 1, 7, 0, 3, 37])
    report.same("Pro Rata allocated (PR Min 2)", alloc, [0, 0, 7, 0, 3, 37])
    report.same(
        "remaining after Pro Rata", [x - a for x, a in zip(q, alloc)], [5, 9, 50, 4, 25, 263]
    )
    return alloc


def check_leveling(report: CheckReport, alloc: Sequence[int]) -> None:
    """Check step 2, Leveling of the lots Pro Rata left, after the given allocation."""
    q = QUANTITIES
    left = INCOMING - sum(alloc)
    report.same("lots left for Leveling", left, 3)
    lev = leveling(q, alloc, left)
    report.same(
        "Leveling order of qualifying orders (1-based)",
        [i + 1 for i in leveling_order(q, alloc)],
        [2, 1, 4],
    )
    report.same(
        "remaining after Leveling",
        [x - a - lv for x, a, lv in zip(q, alloc, lev)],
        [4, 8, 50, 3, 25, 263],
    )


def check_split(report: CheckReport) -> None:
    """Check step 3, the FIFO and Pro Rata parts of the Split examples."""
    for pct, want in [(100, 49), (20, 10), (40, 20), (0, 0)]:
        f = split_fifo(SPLIT_INCOMING, pct)
        report.same(
            f"Split {pct}/{100 - pct}: FIFO, Pro Rata",
            (f, SPLIT_INCOMING - f),
            (want, SPLIT_INCOMING - want),
        )


def check_fifo(report: CheckReport) -> None:
    """Check step 4, the two FIFO examples."""
    report.same("FIFO example 1, order 3 remaining", fifo(QUANTITIES, INCOMING)[2], 21)
    report.same(
        "FIFO example 2 (order 2 displays 10), order 3 remaining",
        fifo([5, 10, 57, 4, 28, 300], INCOMING)[2],
        22,
    )


def main() -> int:
    """Run every check with a fresh report, print the summary and return the exit status (0 or 1)."""
    report = CheckReport()
    alloc = check_pro_rata(report)
    check_leveling(report, alloc)
    check_split(report)
    check_fifo(report)
    if report.failures:
        print("\nFAILED:", report.failures)
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
