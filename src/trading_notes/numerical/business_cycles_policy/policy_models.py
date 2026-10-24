"""Fiscal multipliers, public-debt dynamics and the welfare effects of a large importer's tariff."""

from scipy.optimize import brentq

from trading_notes.records import Record


class KeynesianCross(Record):
    """Output demanded when consumption is a fixed share of disposable income.

    Attributes:
        mpc: c, the marginal propensity to consume.
        tax_rate: t, the net tax rate on income.
    """

    mpc: float
    tax_rate: float

    def multiplier(self) -> float:
        """Return 1 / (1 - c (1 - t))."""
        return 1 / (1 - self.mpc * (1 - self.tax_rate))

    def multiplier_by_rounds(self, rounds: int) -> float:
        """Return the sum of the first spending rounds (c (1 - t))^k, k = 0..rounds - 1."""
        return float(sum((self.mpc * (1 - self.tax_rate)) ** k for k in range(rounds)))

    def output_with_lump_sum_tax(
        self, autonomous: float, investment: float, spending: float, tax: float
    ) -> float:
        """Return Y solving Y = C0 + c (Y - T) + I + G with a lump-sum tax T."""
        return (autonomous + investment + spending - self.mpc * tax) / (1 - self.mpc)


class PublicDebt(Record):
    """The debt-to-GDP ratio under a nominal interest rate and nominal growth.

    Attributes:
        rate: r, the interest rate on the debt.
        growth: g, nominal GDP growth.
    """

    rate: float
    growth: float

    def next_ratio(self, d: float, pb: float) -> float:
        """Return next year's debt ratio d (1 + r) / (1 + g) - pb, pb the primary balance."""
        return d * (1 + self.rate) / (1 + self.growth) - pb

    def stabilising_balance(self, d: float) -> float:
        """Return the primary balance d (r - g) / (1 + g) that holds the ratio at d."""
        return d * (self.rate - self.growth) / (1 + self.growth)


def large_tariff(tau: float) -> tuple[float, float, float]:
    """Return the world price, imports and home welfare of a large importer under a tariff tau.

    Home demand is D = 100 - P, home supply S = P and foreign export supply X = P_w - 20, at the
    world price P_w; welfare is consumer and producer surplus plus tariff revenue.
    """
    pw_ = brentq(lambda p: (100 - (p + tau)) - (p + tau) - (p - 20), 0, 100)
    pd = pw_ + tau
    imports = (100 - pd) - pd
    cs = 0.5 * (100 - pd) ** 2
    ps = 0.5 * pd**2
    return pw_, imports, cs + ps + tau * imports
