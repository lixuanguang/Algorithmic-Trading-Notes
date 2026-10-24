"""A whole-fund (European) distribution waterfall, and a buyout fund's deals marked over time."""

import numpy as np
from numpy.typing import NDArray

from trading_notes.records import Record

type Floats = NDArray[np.float64]


class EuropeanWaterfall(Record):
    """Return of contributions with a compounding preferred return, full catch-up, then a split.

    Attributes:
        hurdle: The preferred return.
        carry: The GP's share of profit.
    """

    hurdle: float = 0.08
    carry: float = 0.2

    def distribute(self, calls_t: Floats, proc_t: Floats) -> tuple[Floats, Floats]:
        """Return the LP's and the GP's distributions by date.

        (1) Return of contributions with the preferred return compounding; (2) 100% catch-up
        until the GP has its share of profit; (3) the remaining split.
        """
        hurdle, carry = self.hurdle, self.carry
        n = len(proc_t)
        lp, gp = np.zeros(n), np.zeros(n)
        owed = 0.0
        for t in range(n):
            owed = owed * (1 + hurdle) + calls_t[t]
            cash = proc_t[t]
            a = min(cash, owed)
            lp[t] += a
            owed -= a
            cash -= a
            if cash > 0:
                contrib = calls_t[: t + 1].sum()
                need = max(
                    0.0, (carry * (lp.sum() - contrib) - (1 - carry) * gp.sum()) / (1 - carry)
                )
                b = min(cash, need)
                gp[t] += b
                cash -= b
                lp[t] += (1 - carry) * cash
                gp[t] += carry * cash
        return lp, gp


class DealBook(Record):
    """A fund's deals, each held from the year bought to the year sold, flows at year ends.

    Attributes:
        deals: deal -> (cost, year bought, year sold, exit value).
    """

    deals: dict[str, tuple[float, int, int, float]]

    def held_cost(self, t: int) -> float:
        """Return the cost of the deals held after the exits of year t."""
        return sum(c for c, ti, te, _ in self.deals.values() if ti <= t < te)

    def mark(self, t: int) -> float:
        """Return the gross NAV after the year-t exits.

        Winners are held at cost for a year, then marked geometrically from cost to exit value;
        a write-off is held at cost when bought, then at half of cost until written off.
        """
        v = 0.0
        for c, ti, te, x in self.deals.values():
            if ti <= t < te:
                if x > 0:
                    v += c if t <= ti + 1 else c * (x / c) ** ((t - ti - 1) / (te - ti - 1))
                else:
                    v += c if t == ti else 0.5 * c
        return v
