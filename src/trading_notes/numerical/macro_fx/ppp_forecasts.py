"""Relative-PPP forecasts of exchange-rate changes: price levels known in time, expanding OLS."""

from collections.abc import Mapping

import numpy as np

from trading_notes.numerical.newey_west import Month, add, mdiff
from trading_notes.numerical.records import Record


class StaleDataRule(Record):
    """Which CPI observation is known at a forecast origin, and how old it may be.

    Attributes:
        monthly_lag: A monthly CPI is known with this publication lag, and nothing older is used.
        min_age: A quarterly CPI is known once its quarter ended at least this many months ago.
        max_age: ... and is used only while its quarter ended at most this many months ago.
    """

    monthly_lag: int = 2
    min_age: int = 4
    max_age: int = 6

    def known_price(
        self, cpi: Mapping[Month, float], t: Month, quarterly: bool
    ) -> tuple[float, int] | None:
        """Return the price level known at t and the age in months of its last month, or None.

        Quarterly series are dated at the quarter's first month; the quarter ends two months
        later.
        """
        if not quarterly:
            k = add(t, -self.monthly_lag)
            return (cpi[k], self.monthly_lag) if k in cpi else None
        cands = [k for k in cpi if mdiff(t, add(k, 2)) >= self.min_age]
        if not cands:
            return None
        k = max(cands)
        age = mdiff(t, add(k, 2))
        return (cpi[k], age) if age <= self.max_age else None


class ExpandingForecast(Record):
    """Forecasts of the h-month change in the log spot rate from expanding OLS on a predictor.

    At each origin t only pairs whose outcome month t' + h <= t enter the fit.

    Attributes:
        horizon: h, in months.
        start: The first forecast origin.
        min_train: The fewest training pairs a forecast needs.
    """

    horizon: int
    start: Month
    min_train: int = 60

    def forecasts(
        self, spot: Mapping[Month, float], z: Mapping[Month, float | None]
    ) -> tuple[
        list[tuple[Month, float, float]], list[Month], dict[Month, float], dict[Month, float]
    ]:
        """Return the forecasts as (t, forecast, actual), the usable origins, X and Y.

        Args:
            spot: The log spot rate by month.
            z: The predictor by month, None where it is not eligible.
        """
        h = self.horizon
        ts = [t for t in sorted(z) if z[t] is not None and add(t, h) in spot]
        X = {t: float(v) for t in ts if (v := z[t]) is not None}
        Y = {t: spot[add(t, h)] - spot[t] for t in ts}
        out = []
        for j, t in enumerate(ts):
            if t < self.start:
                continue
            tr = [k for k in ts[:j] if add(k, h) <= t]  # only outcomes known at t
            if len(tr) < self.min_train:
                continue
            A = np.column_stack([np.ones(len(tr)), [X[k] for k in tr]])
            b = np.linalg.lstsq(A, np.array([Y[k] for k in tr]), rcond=None)[0]
            out.append((t, float(b[0] + b[1] * X[t]), Y[t]))
        return out, ts, X, Y
