"""A synthetic rating schedule and a firm's market-value WACC."""

from typing import Final

from trading_notes.records import Record


class RatingBand(Record):
    """One row of a synthetic rating schedule.

    Attributes:
        cover: The lowest interest cover that earns the rating.
        rating: The rating.
        spread: The spread over the risk-free rate at that rating.
    """

    cover: float
    rating: str
    spread: float


class RatingSchedule(Record):
    """A synthetic rating schedule: interest cover bands from the best rating down.

    Attributes:
        bands: The bands in descending order of their cover bound; the last catches all.
    """

    bands: tuple[RatingBand, ...]

    def rating(self, cover: float) -> tuple[str, float]:
        """Return the rating and spread of the first band whose cover bound is met.

        Raises:
            ValueError: If the cover is below every bound.
        """
        for band in self.bands:
            if cover >= band.cover:
                return band.rating, band.spread
        raise ValueError(f"interest cover {cover} is below every bound of the schedule")

    def cost_of_debt(self, rf: float, debt: float, ebit: float) -> tuple[float, str]:
        """Return the cost of debt and rating whose own interest charge still earns that rating.

        The best rating is found by scanning the bands from the best down; no debt borrows at
        the best rating.
        """
        best, worst = self.bands[0], self.bands[-1]
        if debt == 0:
            return rf + best.spread, best.rating
        for band in self.bands:
            if ebit / ((rf + band.spread) * debt) >= band.cover:
                return rf + band.spread, band.rating
        return rf + worst.spread, worst.rating


# Illustrative, calibrated so that Harbour's normalised cover maps to a 5.2% cost of debt at a
# 3% risk-free rate.
SCHEDULE: Final = RatingSchedule(
    bands=tuple(
        RatingBand(cover=cover, rating=rating, spread=spread)
        for cover, rating, spread in (
            (12.5, "AAA", 0.007),
            (9.5, "AA", 0.009),
            (8.0, "A+", 0.012),
            (7.0, "A", 0.015),
            (6.5, "A-", 0.018),
            (5.5, "BBB", 0.022),
            (4.5, "BB+", 0.030),
            (3.5, "BB", 0.038),
            (3.0, "B+", 0.048),
            (2.5, "B", 0.060),
            (2.0, "B-", 0.075),
            (1.5, "CCC", 0.095),
            (1.0, "CC", 0.120),
            (0.5, "C", 0.150),
            (-1e9, "D", 0.180),
        )
    )
)


def levered_beta(beta_u: float, debt_to_equity: float, tax: float) -> float:
    """Return Hamada's levered beta beta_u (1 + (1 - t) D/E)."""
    return beta_u * (1 + (1 - tax) * debt_to_equity)


class CapitalStructure(Record):
    """A firm's claims at market value and its CAPM cost of capital.

    Attributes:
        rf: Risk-free rate.
        erp: Equity risk premium.
        beta_u: Unlevered (asset) beta.
        kd_pre: Pre-tax cost of debt.
        tax: Corporate tax rate.
        debt: Debt claims at market value.
        equity: Equity claims at market value, including options on the equity.
    """

    rf: float
    erp: float
    beta_u: float
    kd_pre: float
    tax: float
    debt: float
    equity: float

    @property
    def debt_to_equity(self) -> float:
        """Return D/E."""
        return self.debt / self.equity

    @property
    def beta_l(self) -> float:
        """Return the levered equity beta."""
        return levered_beta(self.beta_u, self.debt_to_equity, self.tax)

    @property
    def ke(self) -> float:
        """Return the CAPM cost of equity rf + beta_l erp."""
        return self.rf + self.beta_l * self.erp

    @property
    def kd(self) -> float:
        """Return the after-tax cost of debt."""
        return self.kd_pre * (1 - self.tax)

    @property
    def w_e(self) -> float:
        """Return the equity weight E / (E + D)."""
        return self.equity / (self.equity + self.debt)

    @property
    def w_d(self) -> float:
        """Return the debt weight D / (E + D)."""
        return self.debt / (self.equity + self.debt)

    @property
    def wacc(self) -> float:
        """Return the weighted average cost of capital w_e ke + w_d kd."""
        return self.w_e * self.ke + self.w_d * self.kd

    def wacc_at(self, debt_ratio: float, ebit: float) -> tuple[float, float]:
        """Return the WACC and pre-tax cost of debt if the firm's value were D/V = debt_ratio.

        Firm value is held at E + D; beta relevers to the new D/E and the cost of debt comes
        from the synthetic rating that the new interest charge earns on ebit.
        """
        value = self.equity + self.debt
        D = debt_ratio * value
        E = value - D
        kd_try, _ = SCHEDULE.cost_of_debt(self.rf, D, ebit)
        b = self.beta_u * (1 + (1 - self.tax) * D / E)  # (1 - t) D / E, in this order
        return E / value * (self.rf + b * self.erp) + D / value * kd_try * (1 - self.tax), kd_try
