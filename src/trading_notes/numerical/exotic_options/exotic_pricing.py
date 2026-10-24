"""Closed forms for digital, barrier and geometric Asian options under Black-Scholes-Merton."""

import math

from scipy.stats import norm

from trading_notes.numerical.option_pricing.black_scholes import BlackScholes
from trading_notes.records import Record


class ExoticPricer(Record):
    """Exotic option values under GBM with a constant rate, dividend yield and volatility.

    Methods that take `vol` use the pricer's volatility when it is None.

    Attributes:
        rate: Continuously compounded risk-free rate.
        dividend_yield: Continuous dividend yield q.
        vol: Volatility.
    """

    rate: float
    dividend_yield: float
    vol: float

    def option(self, S: float, k: float, tau: float, vol: float | None = None) -> BlackScholes:
        """Return the vanilla option with spot S, strike k and time tau."""
        v = self.vol if vol is None else vol
        return BlackScholes(
            spot=S,
            strike=k,
            maturity=tau,
            rate=self.rate,
            vol=v,
            dividend_yield=self.dividend_yield,
        )

    def call(self, S: float, k: float, tau: float, vol: float | None = None) -> float:
        """Return the Black-Scholes value of a European call."""
        return self.option(S, k, tau, vol).call()

    def cash_digital(self, S: float, k: float, tau: float) -> float:
        """Return the value of a cash-or-nothing call paying 1 if S exceeds k at expiry."""
        return math.exp(-self.rate * tau) * norm.cdf(self.option(S, k, tau).d2)

    def asset_digital(self, S: float, k: float, tau: float) -> float:
        """Return the value of an asset-or-nothing call paying S if S exceeds k at expiry."""
        return S * math.exp(-self.dividend_yield * tau) * norm.cdf(self.option(S, k, tau).d1)

    def cash_digital_delta(self, S: float, k: float, tau: float) -> float:
        """Return the delta of the cash-or-nothing call."""
        d2 = self.option(S, k, tau).d2
        return math.exp(-self.rate * tau) * norm.pdf(d2) / (S * self.vol * math.sqrt(tau))

    def down_in_call(
        self, S: float, k: float, h: float, tau: float, vol: float | None = None
    ) -> float:
        """Return the down-and-in call with barrier h <= k, continuously monitored (Hull 26.9)."""
        v = self.vol if vol is None else vol
        r, q = self.rate, self.dividend_yield
        lm = (r - q + v**2 / 2) / v**2
        y = math.log(h**2 / (S * k)) / (v * math.sqrt(tau)) + lm * v * math.sqrt(tau)
        p1: float = (h / S) ** (2 * lm)
        p2: float = (h / S) ** (2 * lm - 2)
        return S * math.exp(-q * tau) * p1 * norm.cdf(y) - k * math.exp(-r * tau) * p2 * norm.cdf(
            y - v * math.sqrt(tau)
        )

    def down_out_call(
        self, S: float, k: float, h: float, tau: float, vol: float | None = None
    ) -> float:
        """Return the down-and-out call: the vanilla call less the down-and-in call."""
        return self.call(S, k, tau, vol) - self.down_in_call(S, k, h, tau, vol)

    def up_out_call(
        self, S: float, k: float, h: float, tau: float, vol: float | None = None
    ) -> float:
        """Return the up-and-out call with barrier h > k: the call less the up-and-in call."""
        v = self.vol if vol is None else vol
        r, q, N = self.rate, self.dividend_yield, norm.cdf
        lm = (r - q + v**2 / 2) / v**2
        sq = v * math.sqrt(tau)
        y = math.log(h**2 / (S * k)) / sq + lm * sq
        x1 = math.log(S / h) / sq + lm * sq
        y1 = math.log(h / S) / sq + lm * sq
        p1: float = (h / S) ** (2 * lm)
        p2: float = (h / S) ** (2 * lm - 2)
        c_ui = (
            S * N(x1) * math.exp(-q * tau)
            - k * math.exp(-r * tau) * N(x1 - sq)
            - S * math.exp(-q * tau) * p1 * (N(-y) - N(-y1))
            + k * math.exp(-r * tau) * p2 * (N(-y + sq) - N(-y1 + sq))
        )
        return self.call(S, k, tau, v) - c_ui

    def geometric_asian_call(self, mu: float, var: float, k: float, tau: float) -> float:
        """Return a call on a lognormal average with log mean mu and log variance var."""
        d2 = (mu - math.log(k)) / math.sqrt(var)
        d1 = d2 + math.sqrt(var)
        return math.exp(-self.rate * tau) * (
            math.exp(mu + var / 2) * norm.cdf(d1) - k * norm.cdf(d2)
        )

    def discrete_geometric_asian_call(self, nn: int, S: float, k: float, tau: float) -> float:
        """Return the geometric Asian call averaging over nn equally spaced dates after today."""
        r, q, sg = self.rate, self.dividend_yield, self.vol
        return self.geometric_asian_call(
            math.log(S) + (r - q - sg**2 / 2) * tau * (nn + 1) / (2 * nn),
            sg**2 * tau * (nn + 1) * (2 * nn + 1) / (6 * nn**2),
            k,
            tau,
        )
