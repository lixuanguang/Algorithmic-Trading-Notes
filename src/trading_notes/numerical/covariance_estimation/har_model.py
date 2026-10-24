"""Corsi's heterogeneous autoregressive model of realised variance (HAR-RV)."""

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]


class HarModel(Record):
    """HAR-RV: daily, weekly (5-day) and monthly (22-day) averages of realised variance.

    Attributes:
        daily: b_d.
        weekly: b_w.
        monthly: b_m.
    """

    daily: float
    weekly: float
    monthly: float

    def forecast(self, rv: Floats, t: int) -> float:
        """Return b_d RV_t + b_w mean(RV_{t-4..t}) + b_m mean(RV_{t-21..t})."""
        return float(
            self.daily * rv[t]
            + self.weekly * rv[t - 4 : t + 1].mean()
            + self.monthly * rv[t - 21 : t + 1].mean()
        )

    def ar_coefficients(self) -> Floats:
        """Return the AR(22) coefficients the HAR restricts to three steps, lag 1 first."""
        bd, bw, bm = self.daily, self.weekly, self.monthly
        return np.array([bd + bw / 5 + bm / 22] + [bw / 5 + bm / 22] * 4 + [bm / 22] * 17)
