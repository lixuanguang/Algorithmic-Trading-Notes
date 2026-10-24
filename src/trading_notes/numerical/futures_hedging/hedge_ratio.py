"""Minimum-variance hedge ratios: analytic moments, simulated changes and sample estimates."""

import numpy as np
from numpy.typing import NDArray

from trading_notes.records import Record

type Floats = NDArray[np.float64]


class HedgeSample(Record):
    """Paired spot and futures changes; the hedged change is V(h) = dS - h dF.

    So h > 0 is a short futures position against a long exposure and h < 0 a long one.

    Attributes:
        spot_changes: dS.
        futures_changes: dF, of the same length.
    """

    spot_changes: Floats
    futures_changes: Floats

    def variance(self, h: float) -> float:
        """Return the sample Var(dS - h dF), np.var's default (ddof 0)."""
        return float(np.var(self.spot_changes - h * self.futures_changes))

    def cov_var_ratio(self) -> float:
        """Return Cov(dS, dF) / Var(dF), np.cov's default (ddof 1) over Var with ddof 1."""
        dS, dF = self.spot_changes, self.futures_changes
        return float(np.cov(dS, dF)[0, 1] / dF.var(ddof=1))

    def grid_minimiser(self) -> float:
        """Return the h of 3001 points in [-1.5, 1.5] with the least sample Var(dS - h dF).

        The variance is np.var's default (ddof 0); no closed form is used, and the search
        stops at the grid's ends rather than extrapolating.
        """
        dS, dF = self.spot_changes, self.futures_changes
        grid = np.linspace(-1.5, 1.5, 3001)
        return float(grid[np.argmin([np.var(dS - h * dF) for h in grid])])


class HedgeMoments(Record):
    """Spot and futures changes with given volatilities and correlation, hedged as dS - h dF.

    Attributes:
        spot_vol: sS.
        futures_vol: sF.
        correlation: rho.
    """

    spot_vol: float
    futures_vol: float
    correlation: float

    def optimal_ratio(self) -> float:
        """Return the minimum-variance ratio h* = rho sS / sF."""
        return self.correlation * self.spot_vol / self.futures_vol

    def variance(self, h: float) -> float:
        """Return Var(dS - h dF) = sS^2 - 2 h rho sS sF + h^2 sF^2."""
        s_s, s_f = self.spot_vol, self.futures_vol
        return s_s**2 - 2 * h * self.correlation * s_s * s_f + h**2 * s_f**2

    def simulate(self, rng: np.random.Generator, draws: int) -> HedgeSample:
        """Return draws correlated changes from two standard normal vectors, the first for dF."""
        rho = self.correlation
        z1, z2 = rng.standard_normal(draws), rng.standard_normal(draws)
        dF = self.futures_vol * z1
        dS = self.spot_vol * (rho * z1 + np.sqrt(1 - rho**2) * z2)
        return HedgeSample(spot_changes=dS, futures_changes=dF)
