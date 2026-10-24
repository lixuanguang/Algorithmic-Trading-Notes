"""CME Globex allocation steps: Pro Rata with a minimum, Leveling, Split and FIFO."""

import math
from collections.abc import Sequence

from trading_notes.numerical.records import Record


def split_fifo(m: int, pct: int) -> int:
    """Return the FIFO part of a Split allocation of m lots at pct percent, rounded up."""
    return math.ceil(m * pct / 100)


class RestingOrders(Record):
    """The resting quantities at one price that an incoming order is allocated against.

    Attributes:
        quantities: The working quantity of each order in time priority, so a lower index is
            an earlier order.
    """

    quantities: tuple[int, ...]

    def pro_rata_shares(self, incoming: int) -> list[int]:
        """Return each order's Pro Rata share floor(q_i / sum(q) * M), before the minimum."""
        q = self.quantities
        return [math.floor(x / sum(q) * incoming) for x in q]

    def pro_rata(self, incoming: int, minimum: int) -> list[int]:
        """Return the Pro Rata allocation: a share below the minimum (PR Min) is not allocated."""
        return [a if a >= minimum else 0 for a in self.pro_rata_shares(incoming)]

    def leveling_order(self, alloc: Sequence[int]) -> list[int]:
        """Return the 0-based orders that qualify for Leveling, in Leveling order.

        An order qualifies when it took part in Pro Rata and got nothing; larger working
        quantity comes first, then earlier time (lower index).
        """
        q = self.quantities
        return sorted([i for i in range(len(q)) if alloc[i] == 0], key=lambda i: (-q[i], i))

    def leveling(self, alloc: Sequence[int], left: int) -> list[int]:
        """Return the Leveling lots: one each to the first `left` qualifying orders."""
        lev = [0] * len(self.quantities)
        for i in self.leveling_order(alloc)[:left]:
            lev[i] = 1
        return lev

    def fifo(self, incoming: int) -> list[int]:
        """Return each order's remaining quantity after FIFO allocation in time order."""
        out: list[int] = []
        for x in self.quantities:
            take = min(x, incoming)
            out.append(x - take)
            incoming -= take
        return out
