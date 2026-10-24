"""A client's retirement funding plan and the after-tax statistics of candidate asset mixes."""

import math
from collections.abc import Sequence
from typing import Literal

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import OptimizeResult, minimize
from scipy.stats import norm

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]
type LossMeasure = Literal["q5", "q5_at"]

Z5 = norm.ppf(0.05)


class RetirementPlan(Record):
    """Real after-tax savings into a pool until retirement, then spending from it.

    Attributes:
        pool: The long-term pool today.
        savings: Real savings a year, at the end of each saving year.
        saving_years: Years until retirement.
        spending: Real spending a year from retirement, at the start of each year.
        drawing_years: Years of spending.
        gains_tax: (year, real amount) of tax paid from the pool at the end of early years.
    """

    pool: float
    savings: float
    saving_years: int
    spending: float
    drawing_years: int
    gains_tax: tuple[tuple[int, float], ...]

    def value_at_retirement(
        self,
        r: float,
        savings: float | None = None,
        years: int | None = None,
        with_gains_tax: bool = True,
    ) -> float:
        """Return the pool's real value at retirement at the real return r.

        Args:
            r: Real after-tax return a year.
            savings: Savings a year instead of the plan's.
            years: Saving years instead of the plan's.
            with_gains_tax: Whether the gains-tax payments are deducted.
        """
        savings = self.savings if savings is None else savings
        years = self.saving_years if years is None else years
        v = self.pool * (1 + r) ** years + savings * ((1 + r) ** years - 1) / r
        if with_gains_tax:
            v -= sum(x * (1 + r) ** (years - k) for k, x in self.gains_tax)
        return v

    def spending_need(
        self, r: float, spend: float | None = None, years: int | None = None
    ) -> float:
        """Return the value at retirement of the spending, an annuity due, at the real return r."""
        spend = self.spending if spend is None else spend
        years = self.drawing_years if years is None else years
        return spend * (1 - (1 + r) ** -years) / r * (1 + r)


class MixStats(Record):
    """Pre- and after-tax real return statistics of an asset mix, in percent.

    Attributes:
        mean: Pre-tax mean.
        sd: Pre-tax standard deviation.
        q5: Pre-tax one-year 5th percentile, normal.
        mean_at: After-tax mean.
        sd_at: After-tax standard deviation.
        geo_at: After-tax geometric mean, approximated as mean - sd^2 / 2.
        q5_at: After-tax 5th percentile.
    """

    mean: float
    sd: float
    q5: float
    mean_at: float
    sd_at: float
    geo_at: float
    q5_at: float

    def loss(self, measure: LossMeasure) -> float:
        """Return the pre-tax or after-tax 5th percentile."""
        return self.q5 if measure == "q5" else self.q5_at


class TaxedReturns(Record):
    """Real returns taxed each year on the nominal return as earned, losses fully offset.

    With nominal return (1 + r)(1 + pi) - 1 taxed at t, the after-tax real return is exactly
    (1 - t) r - t pi / (1 + pi), so its mean and s.d. follow linearly from the pre-tax ones.

    Attributes:
        tax: Tax rate t on each year's nominal return.
        inflation: Inflation pi.
    """

    tax: float
    inflation: float

    @property
    def drag(self) -> float:
        """Return the tax on the inflation part of the nominal return, in percent."""
        return 100 * self.tax * self.inflation / (1 + self.inflation)

    def stats(self, w: Floats, mu: Floats, V: Floats) -> MixStats:
        """Return the statistics of weights w given pre-tax means mu and covariance V (percent)."""
        m, s = np.float64(w @ mu), math.sqrt(w @ V @ w)
        m_at, s_at = (1 - self.tax) * m - self.drag, (1 - self.tax) * s
        return MixStats(
            mean=m,
            sd=s,
            q5=m + Z5 * s,
            mean_at=m_at,
            sd_at=s_at,
            geo_at=m_at - s_at * s_at / 200,  # geometric approximation, percent units
            q5_at=m_at + Z5 * s_at,
        )

    def best_within_limit(
        self,
        measure: LossMeasure,
        loss_limit: float,
        starts: Sequence[Floats],
        mu: Floats,
        V: Floats,
    ) -> tuple[Floats, MixStats]:
        """Return the long-only mix with the highest after-tax geometric return within a loss limit.

        SLSQP is started from each of `starts`; the best result is kept.

        Args:
            measure: The 5th percentile that the limit applies to.
            loss_limit: The worst acceptable 5th percentile, in percent.
            starts: Starting weights.
            mu: The pre-tax means of the asset classes.
            V: Their covariance matrix, in percent squared.
        """

        def slack(w: Floats) -> float:
            return self.stats(w, mu, V).loss(measure) - loss_limit

        def neg_geo(w: Floats) -> float:
            return -self.stats(w, mu, V).geo_at

        def budget(w: Floats) -> float:
            gap: float = w.sum() - 1
            return gap

        best: OptimizeResult[np.float64] | None = None
        for x0 in starts:
            r = minimize(
                neg_geo,
                x0,
                method="SLSQP",
                bounds=[(0, 1)] * len(x0),
                constraints=[
                    {"type": "eq", "fun": budget},
                    {"type": "ineq", "fun": slack},
                ],
                options={"ftol": 1e-14, "maxiter": 500},
            )
            if best is None or r.fun < best.fun:
                best = r
        assert best is not None
        x_best = np.asarray(best.x, dtype=np.float64)
        return x_best, self.stats(x_best, mu, V)
