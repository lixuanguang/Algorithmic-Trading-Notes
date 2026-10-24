"""European option values by closed form and by quadrature, and daily-credited cash accounts."""

from math import erf, exp, log, pi, sqrt

from trading_notes.records import Record


def N(x: float) -> float:
    """Return the standard normal distribution function."""
    return 0.5 * (1 + erf(x / sqrt(2)))


class LognormalMarket(Record):
    """A stock under Black-Scholes dynamics with a continuous dividend yield.

    Attributes:
        spot: S0.
        rate: r, continuously compounded.
        dividend_yield: q, continuously compounded.
        volatility: sigma.
        maturity: T in years.
    """

    spot: float
    rate: float
    dividend_yield: float
    volatility: float
    maturity: float

    def black_scholes(self, strike: float) -> tuple[float, float]:
        """Return the Black-Scholes call and put values."""
        S, K, r, q = self.spot, strike, self.rate, self.dividend_yield
        s, T = self.volatility, self.maturity
        d1 = (log(S / K) + (r - q + 0.5 * s * s) * T) / (s * sqrt(T))
        d2 = d1 - s * sqrt(T)
        return (
            S * exp(-q * T) * N(d1) - K * exp(-r * T) * N(d2),
            K * exp(-r * T) * N(-d2) - S * exp(-q * T) * N(-d1),
        )

    def by_quadrature(
        self, strike: float, n: int = 200000, zmax: float = 10.0
    ) -> tuple[float, float]:
        """Return the call and put values by midpoint integration over the lognormal density.

        The integral runs over z ~ N(0, 1) on [-zmax, zmax] in n cells, with
        S_T = S exp((r - q - s^2/2) T + s sqrt(T) z); the closed form is not used.
        """
        S, K, r, q = self.spot, strike, self.rate, self.dividend_yield
        s, T = self.volatility, self.maturity
        h = 2 * zmax / n
        c = p = 0.0
        for i in range(n):
            z = -zmax + (i + 0.5) * h
            w = exp(-0.5 * z * z) / sqrt(2 * pi) * h
            ST = S * exp((r - q - 0.5 * s * s) * T + s * sqrt(T) * z)
            c += w * max(ST - K, 0.0)
            p += w * max(K - ST, 0.0)
        return exp(-r * T) * c, exp(-r * T) * p


class DailyAccount(Record):
    """A cash balance credited each day at a continuously compounded annual rate.

    Attributes:
        rate: The annual rate.
        days: The credits per year.
    """

    rate: float
    days: int = 365

    def balance(self, start: float, T: float) -> float:
        """Return the balance after T years of daily credits from start."""
        bal = start
        for _ in range(self.days):
            bal *= exp(self.rate * T / self.days)
        return bal
