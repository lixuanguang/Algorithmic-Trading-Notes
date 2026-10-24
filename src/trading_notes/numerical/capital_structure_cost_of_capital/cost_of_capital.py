"""Discounting helpers, a synthetic rating schedule and a firm's market-value WACC."""

from collections.abc import Sequence
from typing import Final

from trading_notes.numerical.records import Record

# Interest cover lower bound -> (rating, spread): illustrative, calibrated so that Harbour's
# normalised cover maps to a 5.2% cost of debt at a 3% risk-free rate.
SPREADS: Final = (
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


def npv(rate: float, flows: Sequence[float]) -> float:
    """Return the present value of flows at times 0, 1, 2, ... discounted at rate."""
    return sum(c / (1 + rate) ** t for t, c in enumerate(flows))


def annuity(r: float, n: int) -> float:
    """Return the present value of 1 a period for n periods at rate r, paid in arrears."""
    return (1 - (1 + r) ** -n) / r


def synthetic_rating(cover: float) -> tuple[str, float]:
    """Return the rating and spread of the first schedule row whose cover bound is met."""
    for lo, rating, spread in SPREADS:
        if cover >= lo:
            return rating, spread
    raise ValueError(f"interest cover {cover} is below every bound of the schedule")


def rated_cost_of_debt(rf: float, debt: float, ebit: float) -> tuple[float, str]:
    """Return the cost of debt and rating whose own interest charge still earns that rating.

    The best rating is found by scanning the discrete schedule from AAA down; no debt
    borrows at the AAA rate.
    """
    if debt == 0:
        return rf + SPREADS[0][2], SPREADS[0][1]
    for lo, rating, spread in SPREADS:
        if ebit / ((rf + spread) * debt) >= lo:
            return rf + spread, rating
    return rf + SPREADS[-1][2], SPREADS[-1][1]


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
        kd_try, _ = rated_cost_of_debt(self.rf, D, ebit)
        b = self.beta_u * (1 + (1 - self.tax) * D / E)  # (1 - t) D / E, in this order
        return E / value * (self.rf + b * self.erp) + D / value * kd_try * (1 - self.tax), kd_try
