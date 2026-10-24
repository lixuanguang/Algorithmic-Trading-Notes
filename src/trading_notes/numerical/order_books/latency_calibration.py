"""The value of low latency for limit orders, after Moallemi and Saglam's calibration."""

import math

from trading_notes.records import Record


class LatencyCalibration(Record):
    """A stock's half-spread and daily price volatility, in dollars, and its trading day.

    Attributes:
        half_spread: delta, the half bid-ask spread.
        daily_vol: sigma, the standard deviation of the price change over a trading day.
        day_seconds: The length of the trading day in seconds.
    """

    half_spread: float
    daily_vol: float
    day_seconds: float

    def latency_sd(self, ms: float) -> float:
        """Return the price standard deviation over a latency of ms milliseconds."""
        return self.daily_vol * math.sqrt(ms / 1000 / self.day_seconds)

    def premium_reduction(self, sd: float) -> float:
        """Return eq. (13)'s premium reduction sqrt(log(delta^2 / (2 pi sd^2))), in sd units."""
        return math.sqrt(math.log(self.half_spread**2 / (2 * math.pi * sd**2)))

    def latency_cost(self, sd: float) -> float:
        """Return Corollary 1's latency cost as a fraction of the cost of immediacy."""
        return sd / self.half_spread * self.premium_reduction(sd)
