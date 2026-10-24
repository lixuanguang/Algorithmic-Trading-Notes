"""Currency exposure of foreign holdings, minimum-variance and cross hedges, and FX options."""

import math

from scipy.stats import norm

from trading_notes.records import Record


class CurrencyExposure(Record):
    """A foreign holding's local-currency and currency risk.

    Attributes:
        local_vol: Volatility of the foreign-currency return.
        fx_vol: Volatility of the currency return.
        correlation: Their correlation.
    """

    local_vol: float
    fx_vol: float
    correlation: float

    def domestic_vol(self, h: float = 0.0) -> float:
        """Approximate the domestic-currency volatility with hedge ratio h (share hedged)."""
        s_fc, s_fx, rho = self.local_vol, self.fx_vol, self.correlation
        e = 1 - h
        return math.sqrt(s_fc**2 + (e * s_fx) ** 2 + 2 * e * s_fc * s_fx * rho)

    def min_variance_hedge(self) -> float:
        """Return the minimum-variance hedge ratio 1 + rho s_fc / s_fx."""
        return 1 + self.correlation * self.local_vol / self.fx_vol


class CrossHedge(Record):
    """Hedging one currency with forwards on a correlated proxy currency.

    Attributes:
        exposure_vol: Volatility of the exposure's currency.
        proxy_vol: Volatility of the proxy currency.
        correlation: Their correlation.
    """

    exposure_vol: float
    proxy_vol: float
    correlation: float

    def ratio(self) -> float:
        """Return the value hedge ratio rho s_exposure / s_proxy."""
        return self.correlation * self.exposure_vol / self.proxy_vol

    def residual_vol(self) -> float:
        """Return the volatility left unhedged, s_exposure sqrt(1 - rho^2)."""
        return self.exposure_vol * math.sqrt(1 - self.correlation**2)


class GarmanKohlhagen(Record):
    """European FX options on a spot rate quoted in domestic currency per foreign unit.

    Attributes:
        spot: S0.
        maturity: T in years.
        domestic_rate: r_d, continuously compounded.
        foreign_rate: r_f, continuously compounded.
        volatility: sigma.
    """

    spot: float
    maturity: float
    domestic_rate: float
    foreign_rate: float
    volatility: float

    def _d(self, k: float) -> tuple[float, float]:
        s, t, vol = self.spot, self.maturity, self.volatility
        d1 = (math.log(s / k) + (self.domestic_rate - self.foreign_rate + 0.5 * vol**2) * t) / (
            vol * math.sqrt(t)
        )
        return d1, d1 - vol * math.sqrt(t)

    def call(self, k: float) -> float:
        """Return the call struck at k."""
        s, t, rd, rf = self.spot, self.maturity, self.domestic_rate, self.foreign_rate
        d1, d2 = self._d(k)
        return float(s * math.exp(-rf * t) * norm.cdf(d1) - k * math.exp(-rd * t) * norm.cdf(d2))

    def put(self, k: float) -> float:
        """Return the put struck at k."""
        s, t, rd, rf = self.spot, self.maturity, self.domestic_rate, self.foreign_rate
        d1, d2 = self._d(k)
        return float(k * math.exp(-rd * t) * norm.cdf(-d2) - s * math.exp(-rf * t) * norm.cdf(-d1))
