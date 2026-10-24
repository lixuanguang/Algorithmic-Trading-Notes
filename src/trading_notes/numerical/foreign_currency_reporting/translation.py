"""A foreign operation's balance sheet in its functional currency, for translation."""

from trading_notes.records import Record


class ForeignBalanceSheet(Record):
    """A balance sheet in the operation's functional currency.

    Attributes:
        cash: Cash.
        receivables: Receivables.
        inventory: Inventory.
        ppe: Property, plant and equipment.
        payables: Payables.
        debt: Debt.
        capital: Share capital.
    """

    cash: float
    receivables: float
    inventory: float
    ppe: float
    payables: float
    debt: float
    capital: float

    def net_monetary(self) -> float:
        """Return the net monetary position: cash and receivables less payables and debt."""
        return self.cash + self.receivables - self.payables - self.debt

    def net_assets(self) -> float:
        """Return the net assets: the balance-sheet items less payables and debt."""
        return self.cash + self.receivables + self.inventory + self.ppe - self.payables - self.debt
