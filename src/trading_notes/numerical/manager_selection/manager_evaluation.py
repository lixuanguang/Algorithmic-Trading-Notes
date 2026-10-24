"""Performance-fee schedules, returns-based style analysis and shrunk information ratios."""

from collections.abc import Callable, Sequence

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import minimize

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]


class AsymmetricFee(Record):
    """A base fee plus a share of positive excess return, capped, in percent of assets.

    Attributes:
        base: Fee charged whatever the return.
        share: Share of eligible excess return paid.
        cap: Maximum fee in a year.
        high_water_mark: Whether earlier shortfalls must be recovered before a share is paid.
    """

    base: float = 0.25
    share: float = 0.20
    cap: float = 1.25
    high_water_mark: bool = True

    def fees(self, excess: Sequence[float]) -> list[float]:
        """Return each year's fee for the yearly excess returns."""
        fees, deficit = [], 0.0
        for x in excess:
            if self.high_water_mark:
                eligible = max(0.0, x - deficit)
                deficit = max(0.0, deficit - x)
            else:
                eligible = max(0.0, x)
            fees.append(min(self.cap, self.base + self.share * eligible))
        return fees


class FulcrumFee(Record):
    """A symmetric fee, base plus a share of excess return, between a floor and a cap.

    Attributes:
        base: Fee at zero excess return.
        share: Share of excess return, positive or negative.
        floor: Minimum fee.
        cap: Maximum fee.
    """

    base: float = 0.50
    share: float = 0.10
    floor: float = 0.10
    cap: float = 0.90

    def fees(self, excess: Sequence[float]) -> list[float]:
        """Return each year's fee for the yearly excess returns."""
        return [min(self.cap, max(self.floor, self.base + self.share * x)) for x in excess]


class StyleFit(Record):
    """The parts of an SLSQP style fit that the checks read.

    Attributes:
        x: The style weights found.
        fun: The objective at x.
        success: Whether the optimiser reported success.
    """

    x: Floats
    fun: float
    success: bool


def style_fit(objective: Callable[[Floats], float], n_styles: int = 5) -> StyleFit:
    """Minimise an objective over long-only style weights that sum to one, from equal weights."""

    def budget(wv: Floats) -> float:
        gap: float = wv.sum() - 1
        return gap

    r = minimize(
        objective,
        np.full(n_styles, 1 / n_styles),
        method="SLSQP",
        bounds=[(0, 1)] * n_styles,
        constraints=[{"type": "eq", "fun": budget}],
        options={"ftol": 1e-15, "maxiter": 1000},
    )
    return StyleFit(x=r.x, fun=r.fun, success=r.success)


def shrunk_information_ratio(ir: float, years: float, tau: float) -> float:
    """Return the posterior mean of a true IR: prior N(0, tau^2), estimate ~ N(true, 1/years)."""
    return ir * tau**2 / (tau**2 + 1 / years)
