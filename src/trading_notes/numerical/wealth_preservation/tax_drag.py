"""Tax drag on accumulation, the location of bonds and stocks across accounts, wash sales."""

from collections.abc import Sequence

from trading_notes.numerical.records import Record


class TaxDrag(Record):
    """100 invested at a constant return for a number of years.

    Attributes:
        rate: The annual pre-tax return r.
        years: n.
    """

    rate: float
    years: int

    def accrual(self, t: float) -> float:
        """Return the value when the return is taxed each year at rate t."""
        return 100 * (1 + self.rate * (1 - t)) ** self.years

    def deferred(self, t: float) -> float:
        """Return the value when the gain is taxed once, at rate t, at the end."""
        return 100 * ((1 + self.rate) ** self.years * (1 - t) + t)


class AssetLocation(Record):
    """Bonds and stocks split between an IRA and a taxable account.

    Attributes:
        bonds: The bond holding.
        stocks: The stock holding.
        bond_yield: The bond yield, all interest.
        dividend_yield: The stocks' dividend yield on opening value.
        price_growth: The stocks' price growth on opening value.
    """

    bonds: float
    stocks: float
    bond_yield: float
    dividend_yield: float
    price_growth: float

    def stock_ledger(
        self, years: int, tax_div: float, tax_gain: float
    ) -> tuple[float, float, float]:
        """Return the stock account's value, basis and after-tax value on liquidation.

        Each year the price rises on the opening value, a dividend on the opening value is paid
        at year-end, tax on it is paid, and the rest is reinvested and added to basis.
        """
        value = basis = self.stocks
        for _ in range(years):
            div = self.dividend_yield * value
            net_div = div * (1 - tax_div)
            value += self.price_growth * value + net_div
            basis += net_div
        return value, basis, value - tax_gain * (value - basis)

    def after_tax(
        self,
        bonds_in_ira: bool,
        t_int: float,
        t_div: float,
        t_gain: float,
        years: int = 20,
        t_ira: float = 0.24,
    ) -> float:
        """Return after-tax wealth with bonds or stocks in the IRA (taxed at t_ira when drawn)."""
        if bonds_in_ira:
            ira = self.bonds * (1 + self.bond_yield) ** years
            tx_after = self.stock_ledger(years, t_div, t_gain)[2]
        else:
            ira = self.stock_ledger(years, 0.0, 0.0)[0]  # in the IRA: same dividend timing, untaxed
            # interest taxed yearly; basis equals value
            tx_after = self.bonds * (1 + self.bond_yield * (1 - t_int)) ** years
        return ira * (1 - t_ira) + tx_after


def wash_sale(sale_day: int, buy_days: Sequence[int]) -> bool:
    """Return whether s. 1091(a) disallows the loss: identical stock bought within 30 days."""
    return any(sale_day - 30 <= d <= sale_day + 30 for d in buy_days)
