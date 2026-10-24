"""A single-price auction, pro-rata allocation and the outcome of posting against crossing."""

from fractions import Fraction
from typing import Self

from trading_notes.records import Record

type BuyOrder = tuple[str, int, Fraction | None]
type SellOrder = tuple[str, int, Fraction]


class SinglePriceAuction(Record):
    """A call auction of limit and market orders at one clearing price.

    Attributes:
        buys: (trader, quantity, limit price, None for a market order).
        sells: (trader, quantity, limit price).
    """

    buys: tuple[BuyOrder, ...]
    sells: tuple[SellOrder, ...]

    def prices(self) -> list[Fraction]:
        """Return the distinct limit prices in increasing order."""
        return sorted({p for *_, p in self.buys + self.sells if p is not None})

    def demand(self, p: Fraction) -> int:
        """Return the buy quantity at price p: market orders and limits at or above p."""
        return sum(q for _, q, lim in self.buys if lim is None or lim >= p)

    def supply(self, p: Fraction) -> int:
        """Return the sell quantity at price p: limits at or below p."""
        return sum(q for _, q, lim in self.sells if lim <= p)


class ProRataAllocation(Record):
    """An incoming order allocated pro rata across resting orders.

    Attributes:
        executable: The quantity that trades, capped by eligible resting liquidity.
        exact: Each resting order's exact proportional share.
        floors: The shares rounded down.
        rounding: What the floors leave of the executable quantity, for a venue rule.
        residual: The incoming quantity beyond the resting liquidity, unexecuted.
    """

    executable: int
    exact: list[Fraction]
    floors: list[int]
    rounding: int
    residual: int

    @classmethod
    def of(cls, quantity: int, resting: list[int]) -> Self:
        """Return the allocation of an incoming quantity against resting order sizes."""
        E = min(quantity, sum(resting))
        exact = [Fraction(E * q, sum(resting)) for q in resting]
        floors = [int(x) for x in exact]
        rounding = E - sum(floors)
        residual = quantity - E
        assert all(f <= q for f, q in zip(floors, resting, strict=True)), (
            "no order fills beyond its size"
        )
        assert sum(floors) + rounding + residual == quantity, "quantity conserved"
        assert sum(floors) + rounding <= sum(resting), "capacity respected"
        return cls(executable=E, exact=exact, floors=floors, rounding=rounding, residual=residual)


class PostingOutcome(Record):
    """Buying one unit by a horizon, by crossing now or by posting at the bid.

    Both routes end long one unit marked at the same terminal price, so the gain of posting
    is the spread saved when filled and ask0 less the chase price when missed. Values keep
    the type of the prices: prices in integer ticks give integer outcomes.

    Attributes:
        cross: Marked value of crossing at the ask now.
        post: Marked value of posting: the bid if filled, else the chase price at the horizon.
        gain: post - cross.
    """

    cross: int | float
    post: int | float
    gain: int | float

    @classmethod
    def of(
        cls,
        ask0: int | float,
        bid0: int | float,
        filled: bool,
        chase_price: int | float | None,
        mark: int | float,
    ) -> Self:
        """Return the outcomes for the quotes now, the fill, the chase price and the mark.

        Raises:
            ValueError: If the order is missed and no chase price is given.
        """
        cross = mark - ask0
        if filled:
            post = mark - bid0
        elif chase_price is None:
            raise ValueError("a missed order needs a chase price")
        else:
            post = mark - chase_price
        return cls(cross=cross, post=post, gain=post - cross)
