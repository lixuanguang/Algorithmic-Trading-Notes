"""Uniswap v2 constant-product pools and v3 concentrated-liquidity positions."""

import math

from trading_notes.records import Record


class ConstantProductPool(Record):
    """A v2 pool with reserves x of X and y of Y, x y = k before fees.

    Attributes:
        x: The reserve of X.
        y: The reserve of Y.
        fee: The share of each input retained for liquidity providers (0.003 for 30 bp).
    """

    x: float
    y: float
    fee: float = 0.003

    @property
    def price(self) -> float:
        """Return the pool price y / x of X in units of Y."""
        return self.y / self.x

    def swap_output(self, dx: float) -> float:
        """Return the Y paid for dx of X: y g dx / (x + g dx), g = 1 - fee."""
        g = 1 - self.fee
        return self.y * g * dx / (self.x + g * dx)

    def after_swap(self, dx: float) -> ConstantProductPool:
        """Return the pool after dx of X is sold into it, the fee left in the reserves."""
        return self.model_copy(update={"x": self.x + dx, "y": self.y - self.swap_output(dx)})

    def arbitraged(self, p: float) -> ConstantProductPool:
        """Return the fee-free reserves at the same k once arbitrage moves the price to p."""
        k = self.x * self.y
        return self.model_copy(update={"x": math.sqrt(k / p), "y": math.sqrt(k * p)})


class ConcentratedPosition(Record):
    """A v3 position of liquidity L on the price range [p_a, p_b].

    Attributes:
        liquidity: L.
        lower: p_a.
        upper: p_b.
    """

    liquidity: float
    lower: float
    upper: float

    def reserves(self, p: float) -> tuple[float, float]:
        """Return the real reserves (x, y) at a price p inside the range."""
        L = self.liquidity
        return (
            L * (1 / math.sqrt(p) - 1 / math.sqrt(self.upper)),
            L * (math.sqrt(p) - math.sqrt(self.lower)),
        )

    def all_x(self) -> float:
        """Return the X held below p_a, where the position holds no Y."""
        return self.liquidity * (1 / math.sqrt(self.lower) - 1 / math.sqrt(self.upper))

    def all_y(self) -> float:
        """Return the Y held above p_b, where the position holds no X."""
        return self.liquidity * (math.sqrt(self.upper) - math.sqrt(self.lower))
