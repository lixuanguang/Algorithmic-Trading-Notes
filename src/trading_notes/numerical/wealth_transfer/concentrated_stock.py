"""Hedging a concentrated stock position: collars, variable prepaid forwards and exchange funds."""

import math

from scipy import stats

from trading_notes.numerical.records import Record


class StockOptions(Record):
    """BSM options on a non-dividend-paying stock.

    Attributes:
        spot: S0.
        rate: r, continuously compounded.
        volatility: sigma.
        maturity: T in years.
    """

    spot: float
    rate: float
    volatility: float
    maturity: float

    def call(self, K: float) -> float:
        """Return the BSM call struck at K."""
        S0, R, SIG, T = self.spot, self.rate, self.volatility, self.maturity
        d1 = (math.log(S0 / K) + (R + SIG**2 / 2) * T) / (SIG * math.sqrt(T))
        return float(
            S0 * stats.norm.cdf(d1) - K * math.exp(-R * T) * stats.norm.cdf(d1 - SIG * math.sqrt(T))
        )

    def put(self, K: float) -> float:
        """Return the put struck at K by put-call parity."""
        return self.call(K) - self.spot + K * math.exp(-self.rate * self.maturity)

    def put_direct(self, K: float) -> float:
        """Return the put struck at K from the BSM put formula, independently of parity."""
        S0, R, SIG, T = self.spot, self.rate, self.volatility, self.maturity
        d1 = (math.log(S0 / K) + (R + SIG**2 / 2) * T) / (SIG * math.sqrt(T))
        return float(
            K * math.exp(-R * T) * stats.norm.cdf(-d1 + SIG * math.sqrt(T))
            - S0 * stats.norm.cdf(-d1)
        )

    def zero_cost_call_strike(self, put_strike: float) -> float:
        """Return the call strike whose call is worth the put, by 200 bisections on [S0, 3 S0]."""
        lo, hi = self.spot, 3 * self.spot
        target = self.put(put_strike)
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            lo, hi = (mid, hi) if self.call(mid) > target else (lo, mid)
        return 0.5 * (lo + hi)


class PrepaidForward(Record):
    """A variable prepaid forward on terms patterned on Rev. Rul. 2003-7.

    All N shares are delivered below the floor F, shares worth N F between F and the cap C, and
    N F / C shares above C.

    Attributes:
        shares: N.
        floor: F.
        cap: C.
    """

    shares: int
    floor: float
    cap: float

    def delivered(self, ST: float) -> float:
        """Return the value delivered at a terminal price ST."""
        N, F, C = self.shares, self.floor, self.cap
        return N * ST if ST < F else (N * F if ST <= C else N * F / C * ST)

    def delivered_by_options(self, ST: float) -> float:
        """Return the delivered value as N (S_T - (S_T - F)^+ + (F/C)(S_T - C)^+)."""
        N, F, C = self.shares, self.floor, self.cap
        return N * (ST - max(ST - F, 0) + F / C * max(ST - C, 0))

    def retained_by_options(self, ST: float) -> float:
        """Return the retained value as N ((S_T - F)^+ - (F/C)(S_T - C)^+)."""
        N, F, C = self.shares, self.floor, self.cap
        return N * (max(ST - F, 0) - F / C * max(ST - C, 0))

    def advance(self, options: StockOptions) -> float:
        """Return the BSM present value of the delivery, S0 - c(F) + (F/C) c(C) a share."""
        F, C = self.floor, self.cap
        return self.shares * (options.spot - options.call(F) + F / C * options.call(C))

    def advance_as_loan_and_collar(self, options: StockOptions) -> float:
        """Return the same advance as F e^{-rT} - p(F) + (F/C) c(C) a share."""
        F, C = self.floor, self.cap
        disc = math.exp(-options.rate * options.maturity)
        return self.shares * (F * disc - options.put(F) + F / C * options.call(C))


class ExchangeFund(Record):
    """Selling a low-basis holding against contributing it to an exchange fund.

    Attributes:
        value: The holding's market value.
        basis: Its tax basis.
        tax: The tax rate on gains.
        growth: The annual return of both the reinvested proceeds and the fund.
        years: The holding period.
    """

    value: float
    basis: float
    tax: float
    growth: float
    years: int

    def sale(self) -> tuple[float, float, float]:
        """Return the proceeds after tax, their value at the end and the final after-tax value."""
        inv = self.value - self.tax * (self.value - self.basis)
        end = inv * (1 + self.growth) ** self.years
        return inv, end, end - self.tax * (end - inv)

    def fund(self, fee: float = 0.0) -> tuple[float, float]:
        """Return the fund's end value after an annual fee, and its final after-tax value."""
        end = self.value * (1 + self.growth - fee) ** self.years
        return end, end - self.tax * (end - self.basis)

    def break_even_fee(self) -> float:
        """Return the annual fee at which the fund's final value equals the sale's, by bisection."""
        final_sale = self.sale()[2]
        lo, hi = 0.0, self.growth
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            lo, hi = (mid, hi) if self.fund(mid)[1] > final_sale else (lo, mid)
        return 0.5 * (lo + hi)
