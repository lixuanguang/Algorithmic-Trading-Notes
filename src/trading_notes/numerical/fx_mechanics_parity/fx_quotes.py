"""Two-way FX quotes, their inverses and crosses, money-market forwards and forward positions."""

from typing import Literal

from trading_notes.numerical.records import Record


class TwoWayQuote(Record):
    """A bid and an offer for one unit of the base currency in units of the price currency.

    Attributes:
        bid: The price at which the dealer buys the base currency.
        offer: The price at which the dealer sells it.
    """

    bid: float
    offer: float

    def inverted(self) -> TwoWayQuote:
        """Return the quote for the other currency as base: the new bid is 1 / old offer."""
        return TwoWayQuote(bid=1 / self.offer, offer=1 / self.bid)

    def times(self, other: TwoWayQuote) -> TwoWayQuote:
        """Return the cross A/C of this A/B and other B/C: bids multiply, offers multiply."""
        return TwoWayQuote(bid=self.bid * other.bid, offer=self.offer * other.offer)

    def divided_by(self, other: TwoWayQuote) -> TwoWayQuote:
        """Return the cross A/C of this A/B and other C/B: bid over offer, offer over bid."""
        return TwoWayQuote(bid=self.bid / other.offer, offer=self.offer / other.bid)


class MoneyMarketForward(Record):
    """A forward rate by covered interest parity with simple money-market interest.

    Attributes:
        spot: Price currency per unit of base currency.
        price_rate: The price currency's money-market rate.
        base_rate: The base currency's money-market rate.
        price_basis: The price currency's day-count denominator.
        base_basis: The base currency's day-count denominator.
    """

    spot: float
    price_rate: float
    base_rate: float
    price_basis: int = 360
    base_basis: int = 365

    def forward(self, days: int) -> float:
        """Return S (1 + r_price days / basis) / (1 + r_base days / basis)."""
        return (
            self.spot
            * (1 + self.price_rate * days / self.price_basis)
            / (1 + self.base_rate * days / self.base_basis)
        )


class ForwardPosition(Record):
    """An outstanding forward on the base currency, marked by an offsetting forward.

    Attributes:
        side: Whether the position is long or short the base currency.
        notional: Base-currency amount.
        rate: The contracted forward rate.
    """

    side: Literal["long", "short"]
    notional: float
    rate: float

    def settlement(self, offset: float) -> float:
        """Return the price-currency amount settled at maturity against an offsetting forward."""
        gap = offset - self.rate if self.side == "long" else self.rate - offset
        return gap * self.notional

    def mark_to_market(self, offset: float, rate: float, days: int) -> float:
        """Return the settlement discounted at a simple act/360 rate of the price currency."""
        return self.settlement(offset) / (1 + rate * days / 360)
