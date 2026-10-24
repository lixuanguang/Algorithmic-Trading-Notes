"""Statement-linked cash flows: one year's statements derived several ways must agree."""

import sys
from collections.abc import Sequence
from typing import Final

from trading_notes.numerical.cash_flow_analysis.statement_linkage import (
    BalanceSheet,
    CashFlows,
    Disposal,
    IncomeStatement,
    Movements,
    StatementLinkage,
    cash_tax_roll_forward,
)
from trading_notes.numerical.report import CheckReport

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
LINKAGE: Final = StatementLinkage(
    income=INCOME,
    opening=OPENING,
    closing=CLOSING,
    opening_cash=OPENING_CASH,
    disposal=DISPOSAL,
    dividends_paid=DIVIDENDS_PAID,
)


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
    m = LINKAGE.movements
    capex, tax_paid = m.capex, m.tax_paid
    report.ok("capital expenditure from the PP&E cost roll-forward", capex == 200, str(capex))
    report.ok("tax paid = expense + decrease in tax payable", tax_paid == 45, str(tax_paid))
    return m


def check_indirect_from_operating_profit(report: CheckReport, m: Movements) -> CashFlows:
    """Derive the statement by the indirect method from operating profit (IFRS 18 amendments).

    Returns:
        The three sections and the closing cash they imply, starting from the opening cash.
    """
    print("== indirect method from operating profit (IFRS 18 amendments)")
    operating_profit = INCOME.operating_profit
    flows = LINKAGE.cash_flows
    cfo, cfi, cff, close_cash = flows.cfo, flows.cfi, flows.cff, flows.close_cash
    report.ok("operating profit", operating_profit == 180, str(operating_profit))
    report.ok("operating cash flow", cfo == 197, str(cfo))
    report.ok("investing cash flow", cfi == -120, str(cfi))
    report.ok("financing cash flow", cff == -30, str(cff))
    report.ok("closing cash", close_cash == 97, str(close_cash))
    return flows


def check_balance_sheets(report: CheckReport, close_cash: int) -> None:
    """Check that the closing balance sheet balances with the derived closing cash."""
    print("== balance sheets balance (retained earnings as the residual at the start)")
    profit = INCOME.profit
    re_open = OPENING.assets(OPENING_CASH) - OPENING.liabilities() - OPENING.share_capital
    re_close = re_open + profit - DIVIDENDS_PAID
    report.ok("profit", profit == 120, str(profit))
    report.ok(
        "closing balance sheet balances with the derived cash",
        CLOSING.assets(close_cash) == CLOSING.liabilities() + CLOSING.share_capital + re_close,
        f"{CLOSING.assets(close_cash)} = {CLOSING.liabilities()} + {CLOSING.share_capital} +"
        f" {re_close}",
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


# An independent ledger of tax events, not the roll-forward formula itself.
def cash_tax_from_ledger(events: Sequence[tuple[str, int]]) -> int:
    """Tax paid = sum of cash settlements recorded directly in the ledger."""
    return sum(amount for kind, amount in events if kind == "payment")


def check_cash_tax(report: CheckReport) -> None:
    """Check the current-tax roll-forward against the ledger, and where expense less dDTL fails."""
    print(
        "== cash tax: current-tax roll-forward against deferred-tax balance changes (IAS 12 paras."
        " 12, 58, 61A, 62(a))"
    )
    # Case A: current tax 30 in profit or loss, deferred tax 0 there; payable 5 at both dates; a
    # property revaluation of 40 in OCI at a 25 percent rate adds a deferred tax liability of 10
    # through OCI. The entity paid 30.
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
        "expense - dPayable - dDTL gives 20, not 30",
        naive == 20,
        str(naive),
    )

    # Case B: deferred tax wholly in profit or loss. Expense 30 = current 20 + deferred 10; payable
    # unchanged at 0.
    events_b = [("payment", 20)]
    report.ok("ledger: tax paid 20", cash_tax_from_ledger(events_b) == 20)
    report.ok("roll-forward from current tax gives 20", cash_tax_roll_forward(0, 20, 0, 0) == 20)
    report.ok("expense less the profit-or-loss deferred tax agrees here", 30 - 10 - 0 == 20)

    # Case C: current tax charged in OCI is still paid in cash. Current tax 30 in profit or loss and
    # 4 in OCI (for example on a realised hedge gain taxed now), payable 0 -> 6.
    events_c = [("payment", 28)]
    report.ok("ledger: tax paid 28", cash_tax_from_ledger(events_c) == 28)
    report.ok(
        "roll-forward includes current tax recognised in OCI",
        cash_tax_roll_forward(0, 30, 4, 6) == 28,
    )


def main() -> int:
    """Run every check with a fresh report and return the exit status (0 or 1).

    A synthetic distributor's income statement and opening and closing balance sheets are rolled
    forward account by account; the cash-flow statement is derived by the indirect method from
    operating profit (IAS 7 paras. 18(b) and 20 as amended by IFRS 18), from profit (IAS 7 para. 20
    before IFRS 18) with interest paid operating or financing, by the direct method line by line
    (para. 19(b)), and under US GAAP (ASC 230-10-45-15(a), -16(b), -17(c)-(d), as reprinted in ASU
    2016-15); each must agree with the change in cash. Cash tax comes from a current-tax
    roll-forward, checked against an independent ledger of tax payments, with tax charged in OCI
    (IAS 12 paras. 12, 58, 61A, 62(a)). Inputs are invented; all amounts are integer currency units.
    """
    report = CheckReport()
    movements = check_roll_forwards(report)
    flows = check_indirect_from_operating_profit(report, movements)
    check_balance_sheets(report, flows.close_cash)
    check_indirect_from_profit(report, movements, flows)
    check_direct_method(report, movements, flows)
    check_us_gaap(report, movements, flows)
    check_interpretation(report, movements, flows)
    check_cash_tax(report)
    return report.summarise()


if __name__ == "__main__":
    sys.exit(main())
