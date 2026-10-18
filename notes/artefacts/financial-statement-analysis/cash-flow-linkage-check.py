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
Inputs are invented; they illustrate the mechanics, not any company.
Run: uv run python cash-flow-linkage-check.py   (standard library). Exits 1 on failure.
"""

# standard library imports
import sys

fails = []


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


# Income statement for the year.
revenue, cogs, depreciation, gain_on_sale = 1000, 600, 50, 10
insurance_expense, wages_expense = 30, 150  # the operating expenses other than depreciation
interest_expense, tax_expense = 20, 40
operating_profit = revenue - cogs - insurance_expense - wages_expense - depreciation + gain_on_sale
profit = operating_profit - interest_expense - tax_expense

# Opening and closing balance sheets (cash closing balance is solved, not assumed).
open_ = dict(
    cash=50,
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
close = dict(
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
sold_cost, sold_acc_dep, sale_proceeds, dividends_paid = 100, 30, 80, 60

print("== account roll-forwards")
ok("gain = proceeds - carrying amount", gain_on_sale == sale_proceeds - (sold_cost - sold_acc_dep))
ok(
    "accumulated depreciation rolls forward",
    open_["acc_dep"] + depreciation - sold_acc_dep == close["acc_dep"],
)
capex = close["ppe_cost"] - open_["ppe_cost"] + sold_cost
ok("capital expenditure from the PP&E cost roll-forward", capex == 200, str(capex))
tax_paid = tax_expense + open_["tax_payable"] - close["tax_payable"]
ok("tax paid = expense + decrease in tax payable", tax_paid == 45, str(tax_paid))
interest_paid = interest_expense  # no interest payable at either date
d_rec = close["receivables"] - open_["receivables"]
d_inv = close["inventory"] - open_["inventory"]
d_pay = close["payables"] - open_["payables"]
d_prepaid = close["prepaid"] - open_["prepaid"]
d_wages = close["wages_payable"] - open_["wages_payable"]

print("== indirect method from operating profit (IFRS 18 amendments)")
cfo = (
    operating_profit
    + depreciation
    - gain_on_sale
    - d_rec
    - d_inv
    - d_prepaid
    + d_pay
    + d_wages
    - tax_paid
)
cfi = -capex + sale_proceeds
cff = (close["borrowings"] - open_["borrowings"]) - interest_paid - dividends_paid
ok("operating profit", operating_profit == 180, str(operating_profit))
ok("operating cash flow", cfo == 197, str(cfo))
ok("investing cash flow", cfi == -120, str(cfi))
ok("financing cash flow", cff == -30, str(cff))
close_cash = open_["cash"] + cfo + cfi + cff
ok("closing cash", close_cash == 97, str(close_cash))

print("== balance sheets balance (retained earnings as the residual at the start)")


def assets(b, cash):
    return cash + b["receivables"] + b["inventory"] + b["prepaid"] + b["ppe_cost"] - b["acc_dep"]


def liabilities(b):
    return b["payables"] + b["wages_payable"] + b["tax_payable"] + b["borrowings"]


re_open = assets(open_, open_["cash"]) - liabilities(open_) - open_["share_capital"]
re_close = re_open + profit - dividends_paid
ok("profit", profit == 120, str(profit))
ok(
    "closing balance sheet balances with the derived cash",
    assets(close, close_cash) == liabilities(close) + close["share_capital"] + re_close,
    f"{assets(close, close_cash)} = {liabilities(close)} + {close['share_capital']} + {re_close}",
)

print("== indirect method from profit (IAS 7 before IFRS 18)")
cfo_old_operating_interest = (
    profit
    + depreciation
    - gain_on_sale
    - d_rec
    - d_inv
    - d_prepaid
    + d_pay
    + d_wages
    - (open_["tax_payable"] - close["tax_payable"])
)
ok(
    "interest paid in operating: CFO",
    cfo_old_operating_interest == 177,
    str(cfo_old_operating_interest),
)
ok(
    "same net change in cash",
    cfo_old_operating_interest + cfi + (cff + interest_paid) == close_cash - open_["cash"],
)
cfo_old_financing_interest = cfo_old_operating_interest + interest_paid
ok("interest paid in financing: CFO equals the IFRS 18 figure", cfo_old_financing_interest == cfo)

print("== direct method by adjusting the income statement")
from_customers = revenue - d_rec
purchases = cogs + d_inv
to_suppliers = purchases - d_pay
insurance_paid = (
    insurance_expense + d_prepaid
)  # opening prepaid + expense - ... = expense + increase
wages_paid = wages_expense - d_wages  # expense less the increase in wages payable
cfo_direct = from_customers - to_suppliers - insurance_paid - wages_paid - tax_paid
ok("cash from customers", from_customers == 970, str(from_customers))
ok("cash paid to suppliers", to_suppliers == 550, str(to_suppliers))
ok(
    "insurance paid = closing prepaid + expense - opening prepaid",
    insurance_paid == close["prepaid"] + insurance_expense - open_["prepaid"] == 36,
    str(insurance_paid),
)
ok(
    "wages paid = opening payable + expense - closing payable",
    wages_paid == open_["wages_payable"] + wages_expense - close["wages_payable"] == 142,
    str(wages_paid),
)
ok("direct CFO equals indirect CFO", cfo_direct == cfo, str(cfo_direct))
ok(
    "accrual adjustments: expenses 180 against cash 178",
    insurance_expense + wages_expense - (insurance_paid + wages_paid) == 2,
)

print("== US GAAP classification (ASC 230 as amended by ASU 2016-15)")
cfo_us = (
    profit
    + depreciation
    - gain_on_sale
    - d_rec
    - d_inv
    - d_prepaid
    + d_pay
    + d_wages
    - (open_["tax_payable"] - close["tax_payable"])
)  # from net income; interest paid stays operating
cff_us = (close["borrowings"] - open_["borrowings"]) - dividends_paid
ok("US GAAP CFO from net income", cfo_us == 177, str(cfo_us))
ok("US GAAP CFF (dividends financing)", cff_us == -10, str(cff_us))
ok(
    "same change in cash under each classification",
    cfo_us + cfi + cff_us == close_cash - open_["cash"],
)
ok(
    "IFRS 18 against US GAAP: interest paid moves 20 between sections",
    cfo - cfo_us == interest_paid,
)

print("== interpretation figures")
ok("operating cash flow less capital expenditure", cfo - capex == -3, str(cfo - capex))
ok("net working-capital release", -d_rec - d_inv - d_prepaid + d_pay + d_wages == 22)

print(
    "== cash tax: current-tax roll-forward against deferred-tax balance changes (IAS 12 paras. 12, 58, 61A, 62(a))"
)


# Correction of 2026-10-18 (second audit, sec. 9.2). An independent ledger of tax events, not the formula itself.
def cash_tax_from_ledger(events):
    """Tax paid = sum of cash settlements recorded directly in the ledger."""
    return sum(amount for kind, amount in events if kind == "payment")


def cash_tax_roll_forward(open_payable, current_tax_pl, current_tax_oci_equity, close_payable):
    return open_payable + current_tax_pl + current_tax_oci_equity - close_payable


# Case A: current tax 30 in profit or loss, deferred tax 0 there; payable 5 at both dates; a property revaluation of
# 40 in OCI at a 25 percent rate adds a deferred tax liability of 10 through OCI. The entity paid 30.
events_a = [("payment", 5), ("payment", 25)]  # settles the opening 5, then 25 of this year's 30
open_pay_a, close_pay_a = 5, 5
ok("ledger: tax paid 30", cash_tax_from_ledger(events_a) == 30)
ok(
    "roll-forward from current tax gives 30",
    cash_tax_roll_forward(open_pay_a, 30, 0, close_pay_a) == 30,
)
tax_expense_pl, d_dtl_total = (
    30,
    0.25 * 40,
)  # the whole change in the deferred tax liability came through OCI
naive = tax_expense_pl - (close_pay_a - open_pay_a) - d_dtl_total
ok("the superseded formula (expense - dPayable - dDTL) gives 20, not 30", naive == 20, str(naive))

# Case B: deferred tax wholly in profit or loss. Expense 30 = current 20 + deferred 10; payable unchanged at 0.
events_b = [("payment", 20)]
ok("ledger: tax paid 20", cash_tax_from_ledger(events_b) == 20)
ok("roll-forward from current tax gives 20", cash_tax_roll_forward(0, 20, 0, 0) == 20)
ok("expense less the profit-or-loss deferred tax agrees here", 30 - 10 - 0 == 20)

# Case C: current tax charged in OCI is still paid in cash. Current tax 30 in profit or loss and 4 in OCI
# (for example on a realised hedge gain taxed now), payable 0 -> 6.
events_c = [("payment", 28)]
ok("ledger: tax paid 28", cash_tax_from_ledger(events_c) == 28)
ok("roll-forward includes current tax recognised in OCI", cash_tax_roll_forward(0, 30, 4, 6) == 28)

if fails:
    print("FAILED:", ", ".join(fails))
    sys.exit(1)
print("all checks passed")
