"""Value at risk and expected shortfall of discrete and historical-simulation loss distributions."""

import math
from collections.abc import Sequence

from trading_notes.numerical.records import Record


class DiscreteLoss(Record):
    """A discrete loss distribution.

    Attributes:
        atoms: (loss, probability) pairs; the probabilities sum to one.
    """

    atoms: Sequence[tuple[float, float]]

    def var(self, c: float) -> float:
        """Return the lower c-quantile of the loss.

        The cumulative probability is compared with c less 1e-15, so that rounding in the
        running sum cannot skip the atom at which it reaches c.
        """
        cum = 0.0
        for x, p in sorted(self.atoms):
            cum += p
            if cum >= c - 1e-15:
                return x
        return max(x for x, _ in self.atoms)

    def expected_shortfall(self, c: float) -> float:
        """Return ES_c by the fractional-tail-mass form (Acerbi and Tasche, 2001, for losses).

        With tail probability alpha = 1 - c, ES_c = (E[L 1{L > VaR_c}] + VaR_c (P(L <= VaR_c) -
        c)) / alpha, which weights the atom at VaR so that the tail always carries probability
        exactly alpha.
        """
        a = 1 - c
        v = self.var(c)
        above = sum(x * p for x, p in self.atoms if x > v)
        at_or_below = sum(p for x, p in self.atoms if x <= v)
        return (above + v * (at_or_below - c)) / a

    def tail_conditional_expectation(self, c: float, strict: bool = True) -> float:
        """Return E[L | L > VaR_c], or E[L | L >= VaR_c] when not strict."""
        v = self.var(c)
        sel = [(x, p) for x, p in self.atoms if (x > v if strict else x >= v)]
        return sum(x * p for x, p in sel) / sum(p for _, p in sel)


def historical_expected_shortfall(sample: Sequence[float], c: float) -> float:
    """Return the historical-simulation ES_c of a sample of losses.

    The average of the worst n alpha losses, the last one fractionally weighted. A whole or
    fractional part within 1e-12 of an integer is treated as that integer, so that n alpha
    computed in floating point keeps its intended count: 1000 * (1 - 0.99) is
    10.000000000000009.
    """
    xs = sorted(sample, reverse=True)
    k = len(xs) * (1 - c)
    whole = math.floor(k + 1e-12)
    frac = k - whole
    tail = sum(xs[:whole]) + (frac * xs[whole] if frac > 1e-12 else 0.0)
    return tail / k
