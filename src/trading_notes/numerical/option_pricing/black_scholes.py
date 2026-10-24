"""Black-Scholes-Merton values and Greeks of European options on a dividend-paying asset."""

import math
from typing import Literal, Self

from scipy.stats import norm

from trading_notes.records import Record

type OptionKind = Literal["call", "put"]


class BlackScholes(Record):
    """A European option under Black-Scholes-Merton with a continuous dividend yield.

    Attributes:
        spot: Underlying price.
        strike: Strike price.
        maturity: Time to expiry in years.
        rate: Continuously compounded risk-free rate.
        vol: Annual volatility.
        dividend_yield: Continuous yield q; for Black's model on a forward it equals `rate`.
    """

    spot: float
    strike: float
    maturity: float
    rate: float
    vol: float
    dividend_yield: float = 0.0

    @classmethod
    def on_forward(
        cls, forward: float, strike: float, maturity: float, rate: float, vol: float
    ) -> Self:
        """Return Black's model of an option on a forward or futures price, discounted at rate."""
        return cls(
            spot=forward, strike=strike, maturity=maturity, rate=rate, vol=vol, dividend_yield=rate
        )

    @property
    def d1(self) -> float:
        """Return d1 = (ln(S/K) + (r - q + sigma^2/2) T) / (sigma sqrt(T))."""
        return (
            math.log(self.spot / self.strike)
            + (self.rate - self.dividend_yield + self.vol**2 / 2) * self.maturity
        ) / (self.vol * math.sqrt(self.maturity))

    @property
    def d2(self) -> float:
        """Return d2 = d1 - sigma sqrt(T)."""
        return self.d1 - self.vol * math.sqrt(self.maturity)

    def call(self) -> float:
        """Return the call value."""
        return self.spot * math.exp(-self.dividend_yield * self.maturity) * norm.cdf(
            self.d1
        ) - self.strike * math.exp(-self.rate * self.maturity) * norm.cdf(self.d2)

    def put(self) -> float:
        """Return the put value."""
        return self.strike * math.exp(-self.rate * self.maturity) * norm.cdf(
            -self.d2
        ) - self.spot * math.exp(-self.dividend_yield * self.maturity) * norm.cdf(-self.d1)

    def price(self, kind: OptionKind) -> float:
        """Return the value of a call or a put."""
        return self.call() if kind == "call" else self.put()

    def call_delta(self) -> float:
        """Return the call's spot delta, e^(-qT) N(d1)."""
        return math.exp(-self.dividend_yield * self.maturity) * norm.cdf(self.d1)

    def put_delta(self) -> float:
        """Return the put's spot delta, e^(-qT) (N(d1) - 1)."""
        return math.exp(-self.dividend_yield * self.maturity) * (norm.cdf(self.d1) - 1)

    def gamma(self) -> float:
        """Return the gamma of a call or a put."""
        return (
            math.exp(-self.dividend_yield * self.maturity)
            * norm.pdf(self.d1)
            / (self.spot * self.vol * math.sqrt(self.maturity))
        )
