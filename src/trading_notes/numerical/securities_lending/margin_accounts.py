"""Long margin purchases and short sales: equity ratios and the prices that trigger a call."""

from datetime import date

from trading_notes.records import Record


def act360(start: date, end: date) -> float:
    """Return the actual/360 year fraction from start to end."""
    return (end - start).days / 360


class LongMargin(Record):
    """A long margin position: shares bought partly with a broker loan.

    Attributes:
        shares: N.
        loan: The loan balance L at the date, after interest and any credits.
    """

    shares: float
    loan: float

    def equity_ratio(self, price: float) -> float:
        """Return (N P - L) / (N P), equity over market value at price P."""
        return (self.shares * price - self.loan) / (self.shares * price)

    def call_price(self, maintenance: float) -> float:
        """Return the price at which the equity ratio falls to the maintenance margin."""
        return self.loan / (self.shares * (1 - maintenance))


class ShortMargin(Record):
    """A short sale: the proceeds and the margin deposit held as a credit balance.

    Attributes:
        shares: N.
        credit: The credit balance K at the date, after rebates, fees and dividends owed.
    """

    shares: float
    credit: float

    def equity_ratio(self, price: float) -> float:
        """Return (K - N P) / (N P), equity over the market value of the shares owed."""
        return (self.credit - self.shares * price) / (self.shares * price)

    def call_price(self, maintenance: float) -> float:
        """Return the price at which the equity ratio falls to the maintenance margin."""
        return self.credit / (self.shares * (1 + maintenance))
