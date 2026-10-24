"""Linking the income statement, balance sheets and cash-flow statement through the accounts."""

from trading_notes.numerical.records import Record


class IncomeStatement(Record):
    """The year's income statement.

    Attributes:
        revenue: Sales.
        cogs: Cost of goods sold.
        depreciation: Depreciation charge.
        gain_on_sale: Gain on the disposal of equipment.
        insurance_expense: Insurance, an operating expense paid in advance.
        wages_expense: Wages, an operating expense paid in arrears.
        interest_expense: Interest; none is payable at either date.
        tax_expense: Current tax in profit or loss.
    """

    revenue: int
    cogs: int
    depreciation: int
    gain_on_sale: int
    insurance_expense: int
    wages_expense: int
    interest_expense: int
    tax_expense: int

    @property
    def operating_profit(self) -> int:
        """Return profit before interest and tax."""
        return (
            self.revenue
            - self.cogs
            - self.insurance_expense
            - self.wages_expense
            - self.depreciation
            + self.gain_on_sale
        )

    @property
    def profit(self) -> int:
        """Return profit after interest and tax."""
        return self.operating_profit - self.interest_expense - self.tax_expense


class BalanceSheet(Record):
    """Balances at one date other than cash, which is passed separately.

    The closing cash balance is solved from the cash-flow statement, not assumed, and
    retained earnings are the residual.
    """

    receivables: int
    inventory: int
    prepaid: int
    ppe_cost: int
    acc_dep: int
    payables: int
    wages_payable: int
    tax_payable: int
    borrowings: int
    share_capital: int

    def assets(self, cash: int) -> int:
        """Return total assets with the given cash."""
        return (
            cash + self.receivables + self.inventory + self.prepaid + self.ppe_cost - self.acc_dep
        )

    def liabilities(self) -> int:
        """Return total liabilities."""
        return self.payables + self.wages_payable + self.tax_payable + self.borrowings


class Disposal(Record):
    """The equipment sold in the year: its cost, accumulated depreciation and cash proceeds."""

    cost: int
    acc_dep: int
    proceeds: int


class Movements(Record):
    """Cash amounts and working-capital changes derived from the account roll-forwards.

    Each `d_` field is the closing less the opening balance of that account.
    """

    capex: int
    tax_paid: int
    interest_paid: int
    d_rec: int
    d_inv: int
    d_pay: int
    d_prepaid: int
    d_wages: int


class CashFlows(Record):
    """The IFRS 18 indirect-method sections and the closing cash balance they imply."""

    cfo: int
    cfi: int
    cff: int
    close_cash: int


def cash_tax_roll_forward(
    open_payable: int, current_tax_pl: int, current_tax_oci_equity: int, close_payable: int
) -> int:
    """Return tax paid from the current-tax payable roll-forward.

    Current tax charged in OCI or equity is paid in cash like current tax in profit or loss.
    """
    return open_payable + current_tax_pl + current_tax_oci_equity - close_payable


class StatementLinkage(Record):
    """One year's income statement and balance sheets, linked through the accounts.

    The closing cash balance is solved from the cash-flow statement, not assumed.

    Attributes:
        income: The year's income statement.
        opening: Opening balances other than cash.
        closing: Closing balances other than cash.
        opening_cash: Opening cash.
        disposal: The equipment sold in the year.
        dividends_paid: Dividends paid in cash.
    """

    income: IncomeStatement
    opening: BalanceSheet
    closing: BalanceSheet
    opening_cash: int
    disposal: Disposal
    dividends_paid: int

    @property
    def movements(self) -> Movements:
        """Return capital expenditure, tax and interest paid and the working-capital changes.

        Capital expenditure comes from the PP&E cost roll-forward and tax paid from the tax
        payable; no interest is payable at either date.
        """
        o, c, i = self.opening, self.closing, self.income
        return Movements(
            capex=c.ppe_cost - o.ppe_cost + self.disposal.cost,
            tax_paid=i.tax_expense + o.tax_payable - c.tax_payable,
            interest_paid=i.interest_expense,
            d_rec=c.receivables - o.receivables,
            d_inv=c.inventory - o.inventory,
            d_pay=c.payables - o.payables,
            d_prepaid=c.prepaid - o.prepaid,
            d_wages=c.wages_payable - o.wages_payable,
        )

    @property
    def cash_flows(self) -> CashFlows:
        """Return the indirect-method statement from operating profit (IFRS 18 amendments)."""
        m, i = self.movements, self.income
        cfo = (
            i.operating_profit
            + i.depreciation
            - i.gain_on_sale
            - m.d_rec
            - m.d_inv
            - m.d_prepaid
            + m.d_pay
            + m.d_wages
            - m.tax_paid
        )
        cfi = -m.capex + self.disposal.proceeds
        cff = (
            (self.closing.borrowings - self.opening.borrowings)
            - m.interest_paid
            - self.dividends_paid
        )
        return CashFlows(cfo=cfo, cfi=cfi, cff=cff, close_cash=self.opening_cash + cfo + cfi + cff)
