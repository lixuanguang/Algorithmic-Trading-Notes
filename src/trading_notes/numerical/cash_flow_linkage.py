"""Coverage pilot (2026-10-18): the worked example of meth:statement-linked-cash-flows.

A synthetic distributor's income statement and opening and closing balance sheets are rolled forward account by
account; the cash-flow statement is then derived three ways and must agree with the change in the cash balance:
  indirect method from operating profit (IAS 7 paras 18(b) and 20 as amended by IFRS 18);
  indirect method from profit (IAS 7 para 20 before IFRS 18), with interest paid classified as operating, one of the
    options paragraph 33 allowed, and alternatively as financing;
  direct method by adjusting revenue and expenses for working-capital changes (IAS 7 para 19(b)), line by line,
    including a prepaid expense and an accrued expense (extension of 2026-10-18, cash-flow slice);
  US GAAP classification (ASC 230-10-45-15(a), -16(b), -17(c)-(d) as reprinted in ASU 2016-15): indirect method from
    net income (230-10-45-28), interest paid and tax paid operating, dividends paid financing.
  cash tax: a current-tax roll-forward checked against an independent ledger, with the OCI revaluation
    counterexample to the superseded deferred-tax formula (correction of 2026-10-18, second audit).
Inputs are invented; they illustrate the mechanics, not any company. All amounts are integer currency units.
Run: uv run --frozen --no-editable python -m trading_notes.numerical.cash_flow_linkage (standard library).
"""

# standard library imports
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Final

# project library imports
from trading_notes.numerical.report import CheckReport


@dataclass(frozen=True)
class IncomeStatement:
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


@dataclass(frozen=True)
class BalanceSheet:
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


@dataclass(frozen=True)
class Disposal:
    """The equipment sold in the year: its cost, accumulated depreciation and cash proceeds."""

    cost: int
    acc_dep: int
    proceeds: int


@dataclass(frozen=True)
class Movements:
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


@dataclass(frozen=True)
class CashFlows:
    """The IFRS 18 indirect-method sections and the closing cash balance they imply."""

    cfo: int
    cfi: int
    cff: int
    close_cash: int


# Income statement for the year.
INCOME: Final = IncomeStatement(
    revenue=1000,
    cogs=600,
    depreciation=50,
    gain_on_sale=10,
    insurance_expense=30,  # the operating expenses other than depreciation
    wages_expense=150,
    interest_expense=20,
    tax_expense=40,
)
# Opening and closing balance sheets (cash closing balance is solved, not assumed).
OPENING_CASH: Final = 50
OPENING: Final = BalanceSheet(
    receivables=120,
    inventory=200,
    prepaid=10,
    ppe_cost=800,
    acc_dep=300,
    payables=100,
    wages_payable=12,
    tax_payable=15,
    borrowings=300,
    share_capital=400,
)
CLOSING: Final = BalanceSheet(
    receivables=150,
    inventory=180,
    prepaid=16,
    ppe_cost=900,
    acc_dep=320,
    payables=130,
    wages_payable=20,
    tax_payable=10,
    borrowings=350,
    share_capital=400,
)
DISPOSAL: Final = Disposal(cost=100, acc_dep=30, proceeds=80)
DIVIDENDS_PAID: Final = 60


def assets(b: BalanceSheet, cash: int) -> int:
    """Return total assets of a balance sheet holding the given cash."""
    return cash + b.receivables + b.inventory + b.prepaid + b.ppe_cost - b.acc_dep


def liabilities(b: BalanceSheet) -> int:
    """Return total liabilities of a balance sheet."""
    return b.payables + b.wages_payable + b.tax_payable + b.borrowings


def check_roll_forwards(report: CheckReport) -> Movements:
    """Roll the fixed-asset and tax accounts forward and take the working-capital changes.

    Returns:
        Capital expenditure, tax and interest paid, and the working-capital changes.
    """
    print("== account roll-forwards")
    report.ok(
        "gain = proceeds - carrying amount",
        INCOME.gain_on_sale == DISPOSAL.proceeds - (DISPOSAL.cost - DISPOSAL.acc_dep),
    )
    report.ok(
        "accumulated depreciation rolls forward",
        OPENING.acc_dep + INCOME.depreciation - DISPOSAL.acc_dep == CLOSING.acc_dep,
    )
    capex = CLOSING.ppe_cost - OPENING.ppe_cost + DISPOSAL.cost
    report.ok("capital expenditure from the PP&E cost roll-forward", capex == 200, str(capex))
    tax_paid = INCOME.tax_expense + OPENING.tax_payable - CLOSING.tax_payable
    report.ok("tax paid = expense + decrease in tax payable", tax_paid == 45, str(tax_paid))
    return Movements(
        capex=capex,
        tax_paid=tax_paid,
        interest_paid=INCOME.interest_expense,  # no interest payable at either date
        d_rec=CLOSING.receivables - OPENING.receivables,
        d_inv=CLOSING.inventory - OPENING.inventory,
        d_pay=CLOSING.payables - OPENING.payables,
        d_prepaid=CLOSING.prepaid - OPENING.prepaid,
        d_wages=CLOSING.wages_payable - OPENING.wages_payable,
    )


def check_indirect_from_operating_profit(report: CheckReport, m: Movements) -> CashFlows:
    """Derive the statement by the indirect method from operating profit (IFRS 18 amendments).

    Returns:
        The three sections and the closing cash they imply, starting from the opening cash.
    """
    print("== indirect method from operating profit (IFRS 18 amendments)")
    operating_profit = INCOME.operating_profit
    cfo = (
        operating_profit
        + INCOME.depreciation
        - INCOME.gain_on_sale
        - m.d_rec
        - m.d_inv
        - m.d_prepaid
        + m.d_pay
        + m.d_wages
        - m.tax_paid
    )
    cfi = -m.capex + DISPOSAL.proceeds
    cff = (CLOSING.borrowings - OPENING.borrowings) - m.interest_paid - DIVIDENDS_PAID
    report.ok("operating profit", operating_profit == 180, str(operating_profit))
    report.ok("operating cash flow", cfo == 197, str(cfo))
    report.ok("investing cash flow", cfi == -120, str(cfi))
    report.ok("financing cash flow", cff == -30, str(cff))
    close_cash = OPENING_CASH + cfo + cfi + cff
    report.ok("closing cash", close_cash == 97, str(close_cash))
    return CashFlows(cfo=cfo, cfi=cfi, cff=cff, close_cash=close_cash)


def check_balance_sheets(report: CheckReport, close_cash: int) -> None:
    """Check that the closing balance sheet balances with the derived closing cash."""
    print("== balance sheets balance (retained earnings as the residual at the start)")
    profit = INCOME.profit
    re_open = assets(OPENING, OPENING_CASH) - liabilities(OPENING) - OPENING.share_capital
    re_close = re_open + profit - DIVIDENDS_PAID
    report.ok("profit", profit == 120, str(profit))
    report.ok(
        "closing balance sheet balances with the derived cash",
        assets(CLOSING, close_cash) == liabilities(CLOSING) + CLOSING.share_capital + re_close,
        f"{assets(CLOSING, close_cash)} = {liabilities(CLOSING)} + {CLOSING.share_capital} + {re_close}",
    )


def check_indirect_from_profit(report: CheckReport, m: Movements, flows: CashFlows) -> None:
    """Derive operating cash flow from profit (IAS 7 before IFRS 18) under both interest choices."""
    print("== indirect method from profit (IAS 7 before IFRS 18)")
    cfo_old_operating_interest = (
        INCOME.profit
        + INCOME.depreciation
        - INCOME.gain_on_sale
        - m.d_rec
        - m.d_inv
        - m.d_prepaid
        + m.d_pay
        + m.d_wages
        - (OPENING.tax_payable - CLOSING.tax_payable)
    )
    report.ok(
        "interest paid in operating: CFO",
        cfo_old_operating_interest == 177,
        str(cfo_old_operating_interest),
    )
    report.ok(
        "same net change in cash",
        cfo_old_operating_interest + flows.cfi + (flows.cff + m.interest_paid)
        == flows.close_cash - OPENING_CASH,
    )
    cfo_old_financing_interest = cfo_old_operating_interest + m.interest_paid
    report.ok(
        "interest paid in financing: CFO equals the IFRS 18 figure",
        cfo_old_financing_interest == flows.cfo,
    )


def check_direct_method(report: CheckReport, m: Movements, flows: CashFlows) -> None:
    """Derive operating cash flow line by line by adjusting the income statement."""
    print("== direct method by adjusting the income statement")
    from_customers = INCOME.revenue - m.d_rec
    purchases = INCOME.cogs + m.d_inv
    to_suppliers = purchases - m.d_pay
    insurance_paid = (
        INCOME.insurance_expense + m.d_prepaid
    )  # opening prepaid + expense - ... = expense + increase
    wages_paid = INCOME.wages_expense - m.d_wages  # expense less the increase in wages payable
    cfo_direct = from_customers - to_suppliers - insurance_paid - wages_paid - m.tax_paid
    report.ok("cash from customers", from_customers == 970, str(from_customers))
    report.ok("cash paid to suppliers", to_suppliers == 550, str(to_suppliers))
    report.ok(
        "insurance paid = closing prepaid + expense - opening prepaid",
        insurance_paid == CLOSING.prepaid + INCOME.insurance_expense - OPENING.prepaid == 36,
        str(insurance_paid),
    )
    report.ok(
        "wages paid = opening payable + expense - closing payable",
        wages_paid == OPENING.wages_payable + INCOME.wages_expense - CLOSING.wages_payable == 142,
        str(wages_paid),
    )
    report.ok("direct CFO equals indirect CFO", cfo_direct == flows.cfo, str(cfo_direct))
    report.ok(
        "accrual adjustments: expenses 180 against cash 178",
        INCOME.insurance_expense + INCOME.wages_expense - (insurance_paid + wages_paid) == 2,
    )


def check_us_gaap(report: CheckReport, m: Movements, flows: CashFlows) -> None:
    """Classify under ASC 230: interest and tax paid operating, dividends paid financing."""
    print("== US GAAP classification (ASC 230 as amended by ASU 2016-15)")
    cfo_us = (
        INCOME.profit
        + INCOME.depreciation
        - INCOME.gain_on_sale
        - m.d_rec
        - m.d_inv
        - m.d_prepaid
        + m.d_pay
        + m.d_wages
        - (OPENING.tax_payable - CLOSING.tax_payable)
    )  # from net income; interest paid stays operating
    cff_us = (CLOSING.borrowings - OPENING.borrowings) - DIVIDENDS_PAID
    report.ok("US GAAP CFO from net income", cfo_us == 177, str(cfo_us))
    report.ok("US GAAP CFF (dividends financing)", cff_us == -10, str(cff_us))
    report.ok(
        "same change in cash under each classification",
        cfo_us + flows.cfi + cff_us == flows.close_cash - OPENING_CASH,
    )
    report.ok(
        "IFRS 18 against US GAAP: interest paid moves 20 between sections",
        flows.cfo - cfo_us == m.interest_paid,
    )


def check_interpretation(report: CheckReport, m: Movements, flows: CashFlows) -> None:
    """Check the free-cash-flow and working-capital figures used in the interpretation."""
    print("== interpretation figures")
    report.ok(
        "operating cash flow less capital expenditure",
        flows.cfo - m.capex == -3,
        str(flows.cfo - m.capex),
    )
    report.ok(
        "net working-capital release",
        -m.d_rec - m.d_inv - m.d_prepaid + m.d_pay + m.d_wages == 22,
    )


# Correction of 2026-10-18 (second audit, sec. 9.2). An independent ledger of tax events, not the formula itself.
def cash_tax_from_ledger(events: Sequence[tuple[str, int]]) -> int:
    """Tax paid = sum of cash settlements recorded directly in the ledger."""
    return sum(amount for kind, amount in events if kind == "payment")


def cash_tax_roll_forward(
    open_payable: int, current_tax_pl: int, current_tax_oci_equity: int, close_payable: int
) -> int:
    """Return tax paid from the current-tax payable roll-forward, including tax charged in OCI or equity."""
    return open_payable + current_tax_pl + current_tax_oci_equity - close_payable


def check_cash_tax(report: CheckReport) -> None:
    """Check the current-tax roll-forward against the ledger, and the superseded formula's failure."""
    print(
        "== cash tax: current-tax roll-forward against deferred-tax balance changes (IAS 12 paras. 12, 58, 61A, 62(a))"
    )
    # Case A: current tax 30 in profit or loss, deferred tax 0 there; payable 5 at both dates; a property revaluation of
    # 40 in OCI at a 25 percent rate adds a deferred tax liability of 10 through OCI. The entity paid 30.
    events_a = [("payment", 5), ("payment", 25)]  # settles the opening 5, then 25 of this year's 30
    open_pay_a, close_pay_a = 5, 5
    report.ok("ledger: tax paid 30", cash_tax_from_ledger(events_a) == 30)
    report.ok(
        "roll-forward from current tax gives 30",
        cash_tax_roll_forward(open_pay_a, 30, 0, close_pay_a) == 30,
    )
    tax_expense_pl, d_dtl_total = (
        30,
        0.25 * 40,
    )  # the whole change in the deferred tax liability came through OCI
    naive = tax_expense_pl - (close_pay_a - open_pay_a) - d_dtl_total
    report.ok(
        "the superseded formula (expense - dPayable - dDTL) gives 20, not 30",
        naive == 20,
        str(naive),
    )

    # Case B: deferred tax wholly in profit or loss. Expense 30 = current 20 + deferred 10; payable unchanged at 0.
    events_b = [("payment", 20)]
    report.ok("ledger: tax paid 20", cash_tax_from_ledger(events_b) == 20)
    report.ok("roll-forward from current tax gives 20", cash_tax_roll_forward(0, 20, 0, 0) == 20)
    report.ok("expense less the profit-or-loss deferred tax agrees here", 30 - 10 - 0 == 20)

    # Case C: current tax charged in OCI is still paid in cash. Current tax 30 in profit or loss and 4 in OCI
    # (for example on a realised hedge gain taxed now), payable 0 -> 6.
    events_c = [("payment", 28)]
    report.ok("ledger: tax paid 28", cash_tax_from_ledger(events_c) == 28)
    report.ok(
        "roll-forward includes current tax recognised in OCI",
        cash_tax_roll_forward(0, 30, 4, 6) == 28,
    )


def main() -> int:
    """Run every check with a fresh report, print the summary and return the exit status (0 or 1)."""
    report = CheckReport()
    movements = check_roll_forwards(report)
    flows = check_indirect_from_operating_profit(report, movements)
    check_balance_sheets(report, flows.close_cash)
    check_indirect_from_profit(report, movements, flows)
    check_direct_method(report, movements, flows)
    check_us_gaap(report, movements, flows)
    check_interpretation(report, movements, flows)
    check_cash_tax(report)
    if report.failures:
        print("FAILED:", ", ".join(report.failures))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
