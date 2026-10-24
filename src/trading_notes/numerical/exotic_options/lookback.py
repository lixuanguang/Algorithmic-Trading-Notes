"""Hull's closed forms for floating- and fixed-strike lookback options (OFOD, sec. 26.11)."""

import math

from scipy import stats

from trading_notes.numerical.records import Record

N = stats.norm.cdf


class FloatingPutTerms(Record):
    """Hull's floating-strike put with the intermediates his Example 26.2 prints.

    Attributes:
        value: The put value.
        b1: Hull's b_1.
        b2: Hull's b_2.
        b3: Hull's b_3.
        y2: Hull's Y_2.
    """

    value: float
    b1: float
    b2: float
    b3: float
    y2: float


class LookbackModel(Record):
    """Hull's lookback closed forms under GBM with constant rate, dividend yield and volatility.

    The floating formulas read Hull's T as the remaining time `tau` and S_min or S_max as the
    extreme recorded to date, so they also value seasoned contracts. All rates are annual and
    continuously compounded.

    Attributes:
        rate: Risk-free rate r.
        dividend: Dividend yield q; the formulas divide by r - q, so it must differ from r.
        vol: Volatility sigma.
    """

    rate: float
    dividend: float
    vol: float

    def floating_call(self, spot: float, minimum: float, tau: float) -> float:
        """Return c_fl on the minimum recorded to date, with tau years remaining."""
        r, q, sig = self.rate, self.dividend, self.vol
        st = sig * math.sqrt(tau)
        a1 = (math.log(spot / minimum) + (r - q + sig**2 / 2) * tau) / st
        a2 = a1 - st
        a3 = (math.log(spot / minimum) + (-r + q + sig**2 / 2) * tau) / st
        y1 = -2 * (r - q - sig**2 / 2) * math.log(spot / minimum) / sig**2
        w = sig**2 / (2 * (r - q))
        return float(
            spot * math.exp(-q * tau) * N(a1)
            - spot * math.exp(-q * tau) * w * N(-a1)
            - minimum * math.exp(-r * tau) * (N(a2) - w * math.exp(y1) * N(-a3))
        )

    def floating_put_terms(self, spot: float, maximum: float, tau: float) -> FloatingPutTerms:
        """Return p_fl on the maximum recorded to date, with its intermediates."""
        r, q, sig = self.rate, self.dividend, self.vol
        st = sig * math.sqrt(tau)
        b1 = (math.log(maximum / spot) + (-r + q + sig**2 / 2) * tau) / st
        b2 = b1 - st
        b3 = (math.log(maximum / spot) + (r - q - sig**2 / 2) * tau) / st
        y2 = 2 * (r - q - sig**2 / 2) * math.log(maximum / spot) / sig**2
        w = sig**2 / (2 * (r - q))
        value = (
            maximum * math.exp(-r * tau) * (N(b1) - w * math.exp(y2) * N(-b3))
            + spot * math.exp(-q * tau) * w * N(-b2)
            - spot * math.exp(-q * tau) * N(b2)
        )
        return FloatingPutTerms(value=float(value), b1=b1, b2=b2, b3=b3, y2=y2)

    def floating_put(self, spot: float, maximum: float, tau: float) -> float:
        """Return p_fl on the maximum recorded to date, with tau years remaining."""
        return self.floating_put_terms(spot, maximum, tau).value

    def fixed_call(self, spot: float, maximum: float, strike: float, tau: float) -> float:
        """Return c_fix = p*_fl + S e^{-q tau} - K e^{-r tau}, S*_max = max(S_max, K) (p. 625)."""
        return (
            self.floating_put(spot, max(maximum, strike), tau)
            + spot * math.exp(-self.dividend * tau)
            - strike * math.exp(-self.rate * tau)
        )

    def fixed_put(self, spot: float, minimum: float, strike: float, tau: float) -> float:
        """Return p_fix = c*_fl + K e^{-r tau} - S e^{-q tau}, S*_min = min(S_min, K) (p. 625)."""
        return (
            self.floating_call(spot, min(minimum, strike), tau)
            + strike * math.exp(-self.rate * tau)
            - spot * math.exp(-self.dividend * tau)
        )
