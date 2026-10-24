"""ETF quotes from the basket, premium disclosures, leveraged compounding and holding costs."""

from collections.abc import Iterable

import numpy as np
from numpy.typing import NDArray

from trading_notes.records import Record

type Floats = NDArray[np.float64]


class BasketQuote(Record):
    """A market maker's ETF quote built from the basket and the costs of creating or redeeming.

    Attributes:
        basket_bid: The basket's bid per ETF share.
        basket_ask: The basket's ask per ETF share.
        creation_fee: The creation or redemption fee per share.
        slippage: Execution slippage per share.
        financing: Financing cost per share over the holding period.
    """

    basket_bid: float
    basket_ask: float
    creation_fee: float
    slippage: float
    financing: float

    def quote(self, netted: float = 0.0) -> tuple[float, float]:
        """Return (bid, ask) when a share `netted` of flow nets out, sparing fee and financing."""
        kept = 1 - netted
        costs_fee, costs_financing = self.creation_fee * kept, self.financing * kept
        return (
            self.basket_bid - costs_fee - self.slippage - costs_financing,
            self.basket_ask + costs_fee + self.slippage + costs_financing,
        )


def longest_run_above(premiums: Iterable[float], threshold: float) -> int:
    """Return the longest run of consecutive days with |premium| above the threshold."""
    run, longest = 0, 0
    for p in premiums:
        run = run + 1 if abs(p) > threshold else 0
        longest = max(longest, run)
    return longest


class LeveragedFund(Record):
    """A fund that delivers a multiple of the index's daily return.

    Attributes:
        leverage: The daily multiple, 2 for a 2x fund.
    """

    leverage: float

    def levels(self, returns: Iterable[float], start: float) -> tuple[float, float]:
        """Return the index and fund levels after compounding the daily returns from start."""
        level_i = level_e = start
        for r in returns:
            level_i *= 1 + r
            level_e *= 1 + self.leverage * r
        return level_i, level_e


class HoldingCosts(Record):
    """The costs of owning a fund, each as a fraction of the amount invested.

    Attributes:
        expense: The annual expense ratio.
        round_trip_spread: The bid-ask spread paid on entry and exit together.
        commission: The commission on each trade.
        premium_paid: A premium to NAV paid on entry.
    """

    expense: float
    round_trip_spread: float
    commission: float
    premium_paid: float = 0.0

    def total(self, years: float) -> float:
        """Return the total cost of holding for `years`."""
        return (
            self.expense * years + self.round_trip_spread + 2 * self.commission + self.premium_paid
        )
