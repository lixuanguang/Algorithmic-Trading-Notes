"""Fixed cash flows priced off a continuously compounded zero curve, with their yield."""

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import brentq

from trading_notes.records import Record

type Floats = NDArray[np.float64]


class CashFlows(Record):
    """Amounts paid at fixed times, in years.

    Attributes:
        amounts: The cash flows.
        times: Their payment times, in years.
    """

    amounts: Floats
    times: Floats

    def price(self, zero_rates: Floats) -> np.float64:
        """Return the value discounted at the continuous zero rate of each payment time."""
        return np.sum(self.amounts * np.exp(-zero_rates * self.times))

    def yield_to_maturity(self, zero_rates: Floats) -> float:
        """Return the single continuous rate that reprices the flows, bracketed in [-1, 1]."""
        target = self.price(zero_rates)

        def gap(y: float) -> np.float64:
            return np.sum(self.amounts * np.exp(-y * self.times)) - target

        return brentq(gap, -1, 1)

    def price_derivative(self, rates: Floats | float) -> np.float64:
        """Return dB/dr for a parallel shift of the given rates, -sum t c e^(-r t)."""
        return -np.sum(self.times * self.amounts * np.exp(-rates * self.times))
