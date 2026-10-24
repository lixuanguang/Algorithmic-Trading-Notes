"""Market makers' inventory risk: infinite-horizon reservation prices and free entry."""

import math

from trading_notes.numerical.records import Record


class InfiniteHorizonQuoting(Record):
    """A market maker with CARA utility holding a frozen inventory forever (Avellaneda-Stoikov).

    The value of inventory q with cash x is v(x, q) = -exp(-gamma (x + q s)) / D(q), with
    D(q) = omega - gamma^2 sigma^2 q^2 / 2, finite only while D(q) > 0. The reservation prices
    make the agent indifferent to buying or selling one unit.

    Attributes:
        gamma: Risk aversion.
        sigma: Volatility of the mid price, per unit time.
        mid: The mid price s.
        omega: The discount rate of the value integral.
    """

    gamma: float
    sigma: float
    mid: float
    omega: float

    def denominator(self, q: float) -> float:
        """Return D(q) = omega - gamma^2 sigma^2 q^2 / 2."""
        return self.omega - 0.5 * (self.gamma**2 * self.sigma**2) * q**2

    def value(self, x: float, q: float) -> float:
        """Return the closed-form infinite-horizon value of cash x and inventory q."""
        return -math.exp(-self.gamma * (x + q * self.mid)) / self.denominator(q)

    def reservation_bid(self, q: float) -> float:
        """Return r_b = s + ln(D(q + 1)/D(q)) / gamma."""
        return self.mid + math.log(self.denominator(q + 1) / self.denominator(q)) / self.gamma

    def reservation_ask(self, q: float) -> float:
        """Return r_a = s + ln(D(q)/D(q - 1)) / gamma."""
        return self.mid + math.log(self.denominator(q) / self.denominator(q - 1)) / self.gamma


def grossman_miller_participants(a: float, c: float, var_p2: float, var_i: float) -> float:
    """Return 1 + M, the market makers plus the trader, under Grossman and Miller's free entry.

    Their eq. (19) with a zero mean imbalance fixes t = e^{2ac} - 1, so
    1 + M = a sqrt(Var(P2) Var(i)) / sqrt(e^{2ac} - 1).

    Args:
        a: Risk aversion.
        c: The cost of participating.
        var_p2: Variance of the date-2 price.
        var_i: Variance of the order imbalance.
    """
    return a * math.sqrt(var_p2 * var_i) / math.sqrt(math.exp(2 * a * c) - 1)
