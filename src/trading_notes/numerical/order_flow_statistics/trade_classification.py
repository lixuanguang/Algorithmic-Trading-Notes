"""Trade-signing rules on exact decimal prices: the tick test, Lee-Ready, EMO and CLNV."""

from collections.abc import Sequence
from decimal import Decimal
from typing import Annotated

from pydantic import Strict

from trading_notes.records import Record

# Prices stay Decimal: a float price would be rejected rather than converted, so the midpoint
# and 30% bands are compared exactly.
type Price = Annotated[Decimal, Strict()]


def tick_test(price: Decimal, prior: Sequence[Decimal]) -> int:
    """Return +1 if price is above the last different earlier price, -1 if below, 0 if none.

    This is the sign of the last non-zero price change, so a zero tick takes the sign of the
    change before it.
    """
    for q in reversed(prior):
        if q != price:
            return 1 if price > q else -1
    return 0


class Quote(Record):
    """The prevailing bid and ask against which a trade is signed (+1 buy, -1 sell, 0 none).

    Each rule falls back to the tick test on the earlier trade prices, oldest first.

    Attributes:
        bid: The best bid.
        ask: The best ask.
    """

    bid: Price
    ask: Price

    @property
    def mid(self) -> Decimal:
        """Return the exact midpoint (bid + ask) / 2."""
        return (self.bid + self.ask) / 2

    def lee_ready(self, price: Decimal, prior: Sequence[Decimal]) -> int:
        """Return the Lee-Ready sign: the quote rule against the midpoint, then the tick test."""
        if price > self.mid:
            return 1
        if price < self.mid:
            return -1
        return tick_test(price, prior)

    def emo(self, price: Decimal, prior: Sequence[Decimal]) -> int:
        """Return the Ellis-Michaely-O'Hara sign: at the ask or the bid, else the tick test."""
        if price == self.ask:
            return 1
        if price == self.bid:
            return -1
        return tick_test(price, prior)

    def clnv(self, price: Decimal, prior: Sequence[Decimal]) -> int:
        """Return the Chakrabarty-Li-Nguyen-Van Ness sign: within 30% of the spread of a quote."""
        bid, ask = self.bid, self.ask
        spread = ask - bid
        if ask - Decimal("0.3") * spread <= price <= ask:
            return 1
        if bid <= price <= bid + Decimal("0.3") * spread:
            return -1
        return tick_test(price, prior)
