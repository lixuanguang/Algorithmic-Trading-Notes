"""Harbour Tools plc: ledger, statements, ratios, forecasts, free cash flows and valuation."""

import functools
from collections import defaultdict
from collections.abc import Callable, Mapping
from typing import Final

from trading_notes.numerical.option_pricing.black_scholes import BlackScholes
from trading_notes.records import Record

type Line = Mapping[str, float]  # named line items of one year


class YearInputs(Record):
    """One year of Harbour's inputs (EUR millions); the ledger postings are driven by these."""

    accrued_wages_end: float
    capex: float
    db_contrib: float
    dep: float
    dev_amort: float
    dev_capex: float
    dividends: float
    exercise_cash: float
    inventory_end: float
    lease_payment: float
    loan_repay: float
    new_lease: float
    other_sga: float
    payables_end: float
    prod_labour: float
    purchases: float
    receivables_end: float
    remeasurement_loss: float
    research: float
    restructuring: float
    restructuring_paid: float
    revenue: float
    revolver_draw: float
    rou_dep: float
    sa_wages: float
    sbc: float
    service_cost: float
    tax_dep: float
    tax_payable_end: float
    disposal: tuple[float, float, float]


class Acquisition(Record):
    """An acquisition in EUR millions: price, revenue, EBITDA, goodwill, PP&E and intangibles."""

    price: float
    revenue: float
    ebitda: float
    goodwill: float
    ppe: float
    intangibles: float
    fraction_2026: float


class ForecastCase(Record):
    """Assumptions and financing of a forecast; the defaults are the base case.

    Attributes:
        price_infl: Price growth in each forecast year.
        vol_growth: Volume growth in each forecast year.
        var_cost_infl: Variable-cost inflation in each forecast year.
        fixed_infl: Fixed-cost inflation, every year.
        payout: Dividend payout ratio of profit.
        acquisition: An acquisition completed in 2026, if any.
        rcf_limit: Revolving facility limit.
        min_cash: Cash below which the revolver is drawn (and above which it is repaid).
        capex_rate: Capital expenditure as a share of revenue.
        lockup: Leverage above which the next dividend is suspended, if any.
        sga_rate: Selling and administrative cost as a share of organic revenue.
        lockup_pro_forma: Whether the 2026 lock-up test is pro forma for the acquisition.
    """

    price_infl: tuple[float, float, float] = (0.03, 0.025, 0.025)
    vol_growth: tuple[float, float, float] = (0.03, 0.03, 0.03)
    var_cost_infl: tuple[float, float, float] = (0.04, 0.03, 0.025)
    fixed_infl: float = 0.03
    payout: float = 0.40
    acquisition: Acquisition | None = None
    rcf_limit: float = 100.0
    min_cash: float = 40.0
    capex_rate: float = 0.085
    lockup: float | None = None
    sga_rate: float = 0.175
    lockup_pro_forma: bool = False


class YearForecast(Record):
    """One forecast year: flows, ratios, the balance sheet and the opening balance sheet.

    Balance sheets are by account, with credit balances and accumulated depreciation positive.
    """

    year: int
    revenue: float
    cogs: float
    op: float
    fin: float
    pbt: float
    tax: float
    current: float
    profit: float
    cfo: float
    cfi: float
    divs: float
    draw: float
    assets: float
    liab_eq: float
    ebitda: float
    cov_ebitda: float
    debt: float
    net_debt: float
    gross_margin: float
    interest_cover: float
    rcf: float
    liquidity: float
    interest_paid: float
    lease_int: float
    pens_int: float
    capex: float
    acq_cash: float
    organic: float
    vol: float
    price: float
    vcost: float
    lease_principal: float
    lease_new: float
    loan_repay: float
    sbc: float
    service: float
    dep: float
    dev_amort: float
    acq_amort: float
    dep_acq: float
    rou_dep: float
    iters: int
    balance_sheet: dict[str, float]
    opening: dict[str, float]

    def valuation_fcff(self) -> float:
        """Return a forecast year's valuation FCFF by the CFO route.

        CFO plus after-tax interest and pension financing, less capital spending, acquisitions,
        right-of-use additions and share-based expense.
        """
        pension_fin = 15.0 - self.service - TAX * self.pens_int
        return (
            self.cfo
            + self.interest_paid * (1 - TAX)
            + pension_fin
            - self.capex
            - self.acq_cash
            - self.lease_new
            - self.sbc
        )

    def nopat_route_fcff(self) -> float:
        """Return valuation FCFF by the NOPAT route: EBIT less cash taxes, D&A and investment."""
        o, c = self.opening, self.balance_sheet
        cash_tax = self.current - (c["tax_payable"] - o["tax_payable"])
        # All finance costs are deductible; their tax shield belongs to the WACC.
        op_tax = cash_tax + TAX * self.fin
        dwc = (
            (c["receivables"] - o["receivables"])
            + (c["inventory"] - o["inventory"])
            - (c["payables"] - o["payables"])
            - (c["accrued_wages"] - o["accrued_wages"])
            - (c["restructuring_prov"] - o["restructuring_prov"])
        )
        da = self.dep + self.rou_dep + self.dev_amort + self.acq_amort
        return self.op - op_tax + da - dwc - self.capex - self.acq_cash - self.lease_new


ASSETS: Final = [
    "cash",
    "receivables",
    "inventory",
    "ppe_gross",
    "acc_dep",
    "rou",
    "development",
    "goodwill",
]


LIABS: Final = [
    "payables",
    "accrued_wages",
    "tax_payable",
    "lease_liab",
    "term_loan",
    "revolver",
    "db_liab",
    "dtl",
    "restructuring_prov",
]


EQUITY: Final = ["share_capital", "sbp_reserve", "remeasurement_reserve", "retained"]


INCOME: Final = [
    "revenue",
    "other_income",
    "cogs",
    "sga",
    "rnd",
    "restructuring",
    "fin_loan",
    "fin_lease",
    "fin_pension",
    "current_tax",
    "deferred_tax",
]


OCI: Final = ["oci_remeasurement"]


class Ledger:
    """Double-entry ledger of Harbour's accounts: balances, income and OCI flows, and cash tags."""

    def __init__(self, opening: Line) -> None:
        """Start from the opening balances; income and OCI flows are closed to equity each year."""
        self.bal: defaultdict[str, float] = defaultdict(float)
        for k, v in opening.items():
            self.bal[k] = v
        # (activity, line) -> amount
        self.cash_tags: defaultdict[tuple[str, str], float] = defaultdict(float)
        # income and OCI accounts for the year
        self.flows: defaultdict[str, float] = defaultdict(float)

    def post(self, entries: list[tuple[str, float]], tag: tuple[str, str] | None = None) -> None:
        """Post balanced entries, tagging the cash leg by (activity, line).

        Args:
            entries: (account, debit-positive amount) pairs that sum to zero.
            tag: The cash posting's activity and line; required when cash is posted.

        Raises:
            AssertionError: If the entries do not balance or cash is posted untagged.
        """
        assert abs(sum(a for _, a in entries)) < 1e-9, entries
        for acct, amt in entries:
            if acct in INCOME or acct in OCI:
                self.flows[acct] += amt
            else:
                self.bal[acct] += amt
            if acct == "cash":
                assert tag is not None, entries
                self.cash_tags[tag] += amt

    def close_year(self) -> tuple[dict[str, float], dict[tuple[str, str], float], float]:
        """Close income to retained earnings and OCI to its reserve; return the year's flows."""
        flows = dict(self.flows)
        profit = -sum(flows.get(a, 0.0) for a in INCOME)
        self.bal["retained"] -= profit
        self.bal["remeasurement_reserve"] += flows.get("oci_remeasurement", 0.0)
        tags = dict(self.cash_tags)
        self.flows = defaultdict(float)
        self.cash_tags = defaultdict(float)
        return flows, tags, profit


OPENING_2023: Final = {  # balances at 31 December 2023; credits negative
    "cash": 60,
    "receivables": 150,
    "inventory": 180,
    "ppe_gross": 900,
    "acc_dep": -360,
    "rou": 80,
    "development": 40,
    "goodwill": 120,
    "payables": -110,
    "accrued_wages": -30,
    "tax_payable": -12,
    "lease_liab": -80,
    "term_loan": -300,
    "revolver": 0,
    "db_liab": -50,
    "dtl": -30,
    "restructuring_prov": 0,
    "share_capital": -200,
    "sbp_reserve": -10,
    "remeasurement_reserve": 15,
}


def opening_2023_balances() -> dict[str, int]:
    """Return the balances at 31 December 2023, with the equity residual as retained earnings."""
    return {**OPENING_2023, "retained": -sum(OPENING_2023.values())}


TAX: Final = 0.25


LEASE_RATE: Final = 0.05


LOAN_RATE: Final = 0.04


DB_RATE: Final = 0.04


def post_year(L: Ledger, p: YearInputs) -> tuple[float, float]:
    """Post one year of Harbour's transactions and return profit before tax and taxable profit."""
    b = L.bal
    # Sales on credit and collections.
    L.post([("receivables", p.revenue), ("revenue", -p.revenue)])
    collections = b["receivables"] - p.receivables_end
    L.post([("cash", collections), ("receivables", -collections)], ("op", "customers"))
    # Production: purchases on credit, production labour accrued, production depreciation, all
    # into inventory.
    L.post([("inventory", p.purchases), ("payables", -p.purchases)])
    L.post([("inventory", p.prod_labour), ("accrued_wages", -p.prod_labour)])
    L.post([("inventory", p.dep), ("acc_dep", -p.dep)])
    cogs = b["inventory"] - p.inventory_end
    L.post([("cogs", cogs), ("inventory", -cogs)])
    pay_sup = -(b["payables"]) + p.payables_end  # payables are negative balances
    L.post([("payables", pay_sup), ("cash", -pay_sup)], ("op", "suppliers"))
    # Selling and administration.
    L.post([("sga", p.sa_wages), ("accrued_wages", -p.sa_wages)])
    wages_paid = -(b["accrued_wages"]) + p.accrued_wages_end
    L.post([("accrued_wages", wages_paid), ("cash", -wages_paid)], ("op", "employees"))
    L.post([("sga", p.other_sga), ("cash", -p.other_sga)], ("op", "other_sga"))
    L.post([("sga", p.rou_dep), ("rou", -p.rou_dep)])
    L.post([("sga", p.sbc), ("sbp_reserve", -p.sbc)])
    # Pension: service cost in S&A, net interest in finance costs, remeasurement in OCI,
    # contributions in cash.
    net_interest = DB_RATE * -b["db_liab"]
    L.post([("sga", p.service_cost), ("db_liab", -p.service_cost)])
    L.post([("fin_pension", net_interest), ("db_liab", -net_interest)])
    L.post(
        [
            ("oci_remeasurement", p.remeasurement_loss),
            ("db_liab", -p.remeasurement_loss),
        ]
    )
    L.post(
        [("db_liab", p.db_contrib), ("cash", -p.db_contrib)],
        ("op", "pension_contrib"),
    )
    # Research and development: research expensed in cash, development capitalised
    # (investing), amortised.
    L.post([("rnd", p.research), ("cash", -p.research)], ("op", "research"))
    L.post(
        [("development", p.dev_capex), ("cash", -p.dev_capex)],
        ("inv", "development"),
    )
    L.post([("rnd", p.dev_amort), ("development", -p.dev_amort)])
    # Restructuring (2025 only): provision, partly paid.
    if p.restructuring:
        L.post(
            [
                ("restructuring", p.restructuring),
                ("restructuring_prov", -p.restructuring),
            ]
        )
        L.post(
            [
                ("restructuring_prov", p.restructuring_paid),
                ("cash", -p.restructuring_paid),
            ],
            ("op", "restructuring"),
        )
    # Property, plant and equipment: capital expenditure and a disposal with a gain.
    L.post([("ppe_gross", p.capex), ("cash", -p.capex)], ("inv", "capex"))
    cost, accd, proceeds = p.disposal
    L.post(
        [
            ("cash", proceeds),
            ("acc_dep", accd),
            ("ppe_gross", -cost),
            ("other_income", -(proceeds - cost + accd)),
        ],
        ("inv", "disposal"),
    )
    # Lease: interest accrues, payment reduces the liability; interest paid classified as
    # operating (IAS 7 choice).
    lease_int = LEASE_RATE * -b["lease_liab"]
    L.post([("fin_lease", lease_int), ("lease_liab", -lease_int)])
    L.post(
        [
            ("lease_liab", p.lease_payment - lease_int),
            ("cash", -(p.lease_payment - lease_int)),
        ],
        ("fin", "lease_principal"),
    )
    L.post([("lease_liab", lease_int), ("cash", -lease_int)], ("op", "interest_paid"))
    if p.new_lease:
        L.post([("rou", p.new_lease), ("lease_liab", -p.new_lease)])  # non-cash addition
    # Term loan: interest on the opening balance, paid; scheduled repayment.
    loan_int = LOAN_RATE * -b["term_loan"]
    L.post([("fin_loan", loan_int), ("cash", -loan_int)], ("op", "interest_paid"))
    L.post(
        [("term_loan", p.loan_repay), ("cash", -p.loan_repay)],
        ("fin", "loan_repay"),
    )
    # Share options exercised for cash.
    L.post(
        [("cash", p.exercise_cash), ("share_capital", -p.exercise_cash)],
        ("fin", "share_issue"),
    )
    # Taxes: taxable profit adjusts for the non-deductible share-based expense and accelerated
    # tax depreciation.
    pbt = -sum(L.flows[a] for a in INCOME if a not in ("current_tax", "deferred_tax"))
    taxable = pbt + p.sbc + p.restructuring - p.restructuring_paid - (p.tax_dep - p.dep)
    current = TAX * taxable
    deferred = TAX * (p.tax_dep - p.dep) - TAX * (p.restructuring - p.restructuring_paid)
    L.post([("current_tax", current), ("tax_payable", -current)])
    L.post([("deferred_tax", deferred), ("dtl", -deferred)])
    tax_paid = -(b["tax_payable"]) + p.tax_payable_end
    L.post([("tax_payable", tax_paid), ("cash", -tax_paid)], ("op", "tax_paid"))
    # Dividends declared and paid; a year-end revolver draw (no interest accrues in the year
    # of the draw).
    L.post([("retained", p.dividends), ("cash", -p.dividends)], ("fin", "dividends"))
    if p.revolver_draw:
        L.post(
            [("cash", p.revolver_draw), ("revolver", -p.revolver_draw)],
            ("fin", "revolver"),
        )
    return pbt, taxable


YEARS: Final = {
    2024: YearInputs(
        revenue=1000,
        receivables_end=165,
        purchases=450,
        prod_labour=150,
        dep=60,
        inventory_end=200,
        payables_end=-118,
        sa_wages=120,
        accrued_wages_end=-32,
        other_sga=60,
        rou_dep=20,
        sbc=8,
        service_cost=10,
        remeasurement_loss=6,
        db_contrib=14,
        research=25,
        dev_capex=20,
        dev_amort=10,
        restructuring=0,
        restructuring_paid=0,
        capex=95,
        disposal=(40, 30, 13),
        lease_payment=24,
        new_lease=0,
        loan_repay=25,
        exercise_cash=8,
        tax_dep=90,
        tax_payable_end=-14,
        dividends=30,
        revolver_draw=0,
    ),
    2025: YearInputs(
        revenue=1080,
        receivables_end=180,
        purchases=485,
        prod_labour=158,
        dep=66,
        inventory_end=212,
        payables_end=-124,
        sa_wages=126,
        accrued_wages_end=-33,
        other_sga=63,
        rou_dep=24,
        sbc=9,
        service_cost=11,
        remeasurement_loss=-4,
        db_contrib=15,
        research=26,
        dev_capex=22,
        dev_amort=12,
        restructuring=18,
        restructuring_paid=6,
        capex=105,
        disposal=(20, 16, 3),
        lease_payment=28,
        new_lease=30,
        loan_repay=25,
        exercise_cash=6,
        tax_dep=92,
        tax_payable_end=-15,
        dividends=32,
        revolver_draw=40,
    ),
}


def is_lines(f: dict[str, float]) -> dict[str, float]:
    """Return the income-statement lines of one year, from its flows."""
    rev = -f["revenue"]
    gp = rev - f["cogs"]
    op = gp - f["sga"] - f["rnd"] - f.get("restructuring", 0) - f["other_income"]
    fin = f["fin_loan"] + f["fin_lease"] + f["fin_pension"]
    tax = f["current_tax"] + f["deferred_tax"]
    return dict(
        revenue=rev,
        cogs=f["cogs"],
        gross=gp,
        sga=f["sga"],
        rnd=f["rnd"],
        restructuring=f.get("restructuring", 0),
        other_income=-f["other_income"],
        op=op,
        fin=fin,
        pbt=op - fin,
        tax=tax,
        profit=op - fin - tax,
        oci=-f.get("oci_remeasurement", 0),
    )


NEXT_PRINCIPAL: Final = {
    2024: (25, 28 - LEASE_RATE * 60),
    2025: (25, 28 - LEASE_RATE * 65),
}  # (term loan, lease)


def avg(f: Callable[[int], float], y: int) -> float:
    """Return the average of f over year y and the year before."""
    return (f(y) + f(y - 1)) / 2


LEGACY_DEV_LIFE: Final = (
    5  # the 31 Dec 2025 development balance of 60 is amortised straight-line over 2026-2030
)


DEV_LIFE: Final = (
    5  # each year's capitalised development is available for use on 1 January of the next year
)


ACQ_INTANGIBLE_LIFE: Final = 10


ACQ_PPE_LIFE: Final = 5  # acquired PP&E at fair value: straight-line from completion


def straight_line(
    cost: float, life: float, start: int, years: range, fraction_first: float = 1.0
) -> dict[int, float]:
    """Charge per calendar year for an asset in use from year `start`.

    The first year may be partial. The asset is charged once per period until its cost is
    exhausted, so the schedule never goes negative.
    """
    remaining = cost
    out: dict[int, float] = {}
    for y in years:
        if y < start or remaining <= 1e-12:
            out[y] = 0.0
            continue
        charge = min(remaining, cost / life * (fraction_first if y == start else 1.0))
        out[y] = charge
        remaining -= charge
    return out


class BalanceView(Record):
    """Balance-sheet aggregates of one year-end, EUR millions.

    Attributes:
        ca: Current assets: cash, receivables and inventory.
        ta: Total assets.
        cl: Current liabilities, with next year's loan and lease principal.
        debt: Term loan, revolver and lease liabilities.
        eq: Total equity.
        net_ppe: Net property, plant and equipment.
        nfo: Net financial obligations: debt plus the pension deficit less cash.
    """

    ca: float
    ta: float
    cl: float
    debt: float
    eq: float
    net_ppe: float
    nfo: float


class YearStatements(Record):
    """One reported year derived from the ledger, EUR millions.

    Attributes:
        flows: Income and OCI account flows, debit positive.
        tags: Cash postings by (activity, line).
        profit: Profit for the year from the ledger.
        pbt: Profit before tax.
        taxable: Taxable profit.
        opening: Balances at the start of the year, credits negative.
        closing: Balances at the end of the year, credits negative.
        income: Income-statement lines (see is_lines).
        cfo: Operating cash flow by the direct method.
        cfi: Investing cash flow.
        cff: Financing cash flow.
    """

    flows: dict[str, float]
    tags: dict[tuple[str, str], float]
    profit: float
    pbt: float
    taxable: float
    opening: dict[str, float]
    closing: dict[str, float]
    income: dict[str, float]
    cfo: float
    cfi: float
    cff: float


class Ratios(Record):
    """Harbour's ratio families of one year; averages use the year-end and prior year-end.

    Days measures use 365 days; RNOA, NFR and FLEV come from the operating and financing split
    with the statutory tax shield on finance costs.
    """

    gross_margin: float
    op_margin: float
    net_margin: float
    dso: float
    doh: float
    dpo: float
    fat: float
    tat: float
    current: float
    quick: float
    cash_ratio: float
    debt_equity: float
    net_debt_ebitda: float
    net_debt_adj_ebitda: float
    coverage: float
    ebitda: float
    roa: float
    roe: float
    lev: float
    tax_burden: float
    interest_burden: float
    ccc: float
    rnoa: float
    nfr: float
    flev: float
    nopat: float
    noa_avg: float


class CashFlow2025(Record):
    """Harbour's 2025 free cash flows, statutory and under the valuation conventions.

    The valuation conventions treat leases as debt (right-of-use additions are reinvestment),
    deduct share-based pay as an operating cost, and treat the pension deficit as a debt-like
    claim, so contributions above service cost and the tax shield on net interest are financing.

    Attributes:
        tags: The 2025 cash postings by (activity, line).
        interest_paid: Loan and lease interest paid.
        capex_net: Capital expenditure and development less disposal proceeds.
        fcff: Statutory FCFF: CFO plus after-tax interest less net investment.
        net_borrowing: Loan repayment, revolver draw and lease principal, as cash flows.
        fcfe: Statutory FCFE: CFO less net investment plus net borrowing.
        rou_additions: Right-of-use additions, non-cash.
        fcff_leases_as_debt: FCFF less the right-of-use additions.
        pension_financing: Contributions less service cost less the tax on net interest.
        valuation_fcff: FCFF under all three valuation conventions.
        valuation_fcfe: FCFE after share-based expense.
    """

    tags: dict[tuple[str, str], float]
    interest_paid: float
    capex_net: float
    fcff: float
    net_borrowing: float
    fcfe: float
    rou_additions: float
    fcff_leases_as_debt: float
    pension_financing: float
    valuation_fcff: float
    valuation_fcfe: float


def terminal_value(nopat_next: float, g: float, ronic: float, r: float) -> float:
    """Return the value-driver terminal value NOPAT_{T+1} (1 - g / RONIC) / (r - g)."""
    return nopat_next * (1 - g / ronic) / (r - g)


class HarbourValuation(Record):
    """Harbour's discounted-cash-flow value at 31 December 2025.

    End-of-year cash flows; the terminal value assumes steady growth g with return on new
    invested capital RONIC; claims are debt, leases and the after-tax pension deficit, and
    5m vested options at EUR 8 valued by Black-Scholes-Merton (3 years, volatility 30%, rate
    3%, yield 2.5%) at the value per share, a fixed point.

    Attributes:
        wacc: Discount rate, an input.
        growth: Steady-state growth after 2028.
        ronic: Return on new invested capital after 2028.
        fcff: Valuation FCFF of 2026-2028.
        nopat_2028: NOPAT of 2028, with share-based pay non-deductible.
        terminal_value: Value at the end of 2028.
        enterprise_value: Value of operations at 31 December 2025.
        claims: Non-equity claims by name.
        equity_before_options: Enterprise value plus cash less claims.
        shares: Shares outstanding, millions.
        options: Vested options outstanding, millions.
        option_value: Value of one option at the value per share.
        price: Value per share after the options.
    """

    wacc: float
    growth: float
    ronic: float
    fcff: list[float]
    nopat_2028: float
    terminal_value: float
    enterprise_value: float
    claims: dict[str, float]
    equity_before_options: float
    shares: float
    options: float
    option_value: float
    price: float


SHARES: Final = 100.75  # millions of shares outstanding
VESTED_OPTIONS: Final = 5.0  # millions of vested employee options
MARKET_PRICE: Final = 11.0  # EUR per share on the valuation date
GROSS_DEBT: Final = 355.0  # term loan, revolver and leases at the end of 2025


class VestedOptions(Record):
    """Employee options on Harbour shares, valued by Black-Scholes-Merton.

    Attributes:
        count: Options outstanding, millions.
        strike: Exercise price, EUR.
        maturity: Years to expiry.
        rate: Continuously compounded risk-free rate.
        vol: Volatility of the share.
        dividend_yield: Continuous dividend yield of the share.
    """

    count: float
    strike: float
    maturity: float
    rate: float
    vol: float
    dividend_yield: float

    def option(self, price: float) -> BlackScholes:
        """Return one option on a share worth `price`."""
        return BlackScholes(
            spot=price,
            strike=self.strike,
            maturity=self.maturity,
            rate=self.rate,
            vol=self.vol,
            dividend_yield=self.dividend_yield,
        )

    def claim(self, price: float) -> float:
        """Return the value of all the options on a share worth `price`."""
        return self.count * self.option(price).call()

    def price_per_share(self, equity_before_options: float, shares: float = SHARES) -> float:
        """Return the value per share after the options, valued at that same price.

        Iterates p = (equity before options - options at p) / shares to a fixed point.
        """
        price = equity_before_options / shares
        for _ in range(200):
            new_price = (equity_before_options - self.claim(price)) / shares
            if abs(new_price - price) < 1e-12:
                break
            price = new_price
        return price


# The 5m vested options at EUR 8: 3 years, volatility 30%, rate 3%, yield 2.5%.
OPTIONS: Final = VestedOptions(
    count=VESTED_OPTIONS, strike=8.0, maturity=3.0, rate=0.03, vol=0.30, dividend_yield=0.025
)


def market_cost_of_equity() -> float:
    """Return the cost of equity with beta 0.93 relevered at D/E = debt / (shares + options).

    The equity is valued at the market price: 3% risk-free rate and 5.5% equity premium.
    """
    equity = MARKET_PRICE * SHARES + OPTIONS.claim(MARKET_PRICE)
    return 0.03 + 0.93 * (1 + (1 - TAX) * GROSS_DEBT / equity) * 0.055


class HarbourCase:
    """Harbour Tools plc, a hypothetical IFRS reporter (EUR millions, 2024-2025).

    The statements are derived from a double-entry ledger of the 2024 and 2025 transactions;
    forecasts, cash flows and the valuation are computed on demand from them. Nothing is
    printed or checked here.
    """

    def __init__(self) -> None:
        """Post both years to the ledger and derive the statements, balances and ratios."""
        ledger = Ledger(opening_2023_balances())
        self.statements: dict[int, YearStatements] = {}
        prev = dict(ledger.bal)
        for y in (2024, 2025):
            pbt, taxable = post_year(ledger, YEARS[y])
            flows, tags, profit = ledger.close_year()
            self.statements[y] = YearStatements(
                flows=flows,
                tags=tags,
                profit=profit,
                pbt=pbt,
                taxable=taxable,
                opening=prev,
                closing=dict(ledger.bal),
                income=is_lines(flows),
                cfo=sum(v for (act, _), v in tags.items() if act == "op"),
                cfi=sum(v for (act, _), v in tags.items() if act == "inv"),
                cff=sum(v for (act, _), v in tags.items() if act == "fin"),
            )
            prev = dict(ledger.bal)
        self.balances: dict[int, dict[str, float]] = {
            2023: dict(opening_2023_balances()),
            2024: self.statements[2024].closing,
            2025: self.statements[2025].closing,
        }
        self.ratios: dict[int, Ratios] = {y: self._ratios(y) for y in (2024, 2025)}

    def balance_view(self, y: int) -> BalanceView:
        """Return the balance-sheet aggregates at the end of year y (2023 to 2025)."""
        b = self.balances[y]
        ca = b["cash"] + b["receivables"] + b["inventory"]
        ta = sum(b[a] for a in ASSETS)
        loan_cur, lease_cur = NEXT_PRINCIPAL.get(y, (25, 0))
        cl = (
            -(b["payables"] + b["accrued_wages"] + b["tax_payable"] + b["restructuring_prov"])
            + loan_cur
            + lease_cur
        )
        debt = -(b["term_loan"] + b["revolver"] + b["lease_liab"])
        eq = -sum(b[a] for a in EQUITY)
        return BalanceView(
            ca=ca,
            ta=ta,
            cl=cl,
            debt=debt,
            eq=eq,
            net_ppe=b["ppe_gross"] + b["acc_dep"],
            nfo=debt - b["db_liab"] - b["cash"],
        )

    def _ratios(self, y: int) -> Ratios:
        """Return year y's ratio families."""
        B, view = self.balances, self.balance_view
        i, v, p = self.statements[y].income, view(y), YEARS[y]
        ebitda = i["op"] + p.dep + p.rou_dep + p.dev_amort
        dso = 365 / (i["revenue"] / avg(lambda t: B[t]["receivables"], y))
        doh = 365 / (i["cogs"] / avg(lambda t: B[t]["inventory"], y))
        dpo = 365 / (p.purchases / avg(lambda t: -B[t]["payables"], y))
        # RNOA + FLEV x spread: operating tax = total tax + statutory tax shield on finance costs.
        nfe = i["fin"] * (1 - TAX)
        nopat = i["profit"] + nfe
        noa_avg = avg(lambda t: view(t).eq + view(t).nfo, y)
        nfo_avg = avg(lambda t: view(t).nfo, y)
        eq_avg = avg(lambda t: view(t).eq, y)
        return Ratios(
            gross_margin=i["gross"] / i["revenue"],
            op_margin=i["op"] / i["revenue"],
            net_margin=i["profit"] / i["revenue"],
            dso=dso,
            doh=doh,
            dpo=dpo,
            fat=i["revenue"] / avg(lambda t: view(t).net_ppe, y),
            tat=i["revenue"] / avg(lambda t: view(t).ta, y),
            current=v.ca / v.cl,
            quick=(B[y]["cash"] + B[y]["receivables"]) / v.cl,
            cash_ratio=B[y]["cash"] / v.cl,
            debt_equity=v.debt / v.eq,
            net_debt_ebitda=(v.debt - B[y]["cash"]) / ebitda,
            net_debt_adj_ebitda=(v.debt - B[y]["cash"]) / (ebitda + i["restructuring"]),
            coverage=i["op"] / i["fin"],
            ebitda=ebitda,
            roa=i["profit"] / avg(lambda t: view(t).ta, y),
            roe=i["profit"] / avg(lambda t: view(t).eq, y),
            lev=avg(lambda t: view(t).ta, y) / avg(lambda t: view(t).eq, y),
            tax_burden=i["profit"] / i["pbt"],
            interest_burden=i["pbt"] / i["op"],
            ccc=dso + doh - dpo,
            rnoa=nopat / noa_avg,
            nfr=nfe / nfo_avg,
            flev=nfo_avg / eq_avg,
            nopat=nopat,
            noa_avg=noa_avg,
        )

    @functools.cached_property
    def base(self) -> list[YearForecast]:
        """Return the base-case forecast of 2026-2028."""
        return self.forecast()

    @functools.cached_property
    def cash_flow_2025(self) -> CashFlow2025:
        """Return the 2025 free cash flows."""
        s25, p25 = self.statements[2025], YEARS[2025]
        t25 = s25.tags
        interest_paid = -t25[("op", "interest_paid")]
        capex_net = -(
            t25[("inv", "capex")] + t25[("inv", "development")] + t25[("inv", "disposal")]
        )
        fcff = s25.cfo + interest_paid * (1 - TAX) - capex_net
        net_borrowing = (
            t25[("fin", "loan_repay")] + t25[("fin", "revolver")] + t25[("fin", "lease_principal")]
        )
        fcfe = s25.cfo - capex_net + net_borrowing
        rou_add = p25.new_lease
        fcff_lease = fcff - rou_add
        pension_fin = p25.db_contrib - p25.service_cost - TAX * s25.flows["fin_pension"]
        return CashFlow2025(
            tags=t25,
            interest_paid=interest_paid,
            capex_net=capex_net,
            fcff=fcff,
            net_borrowing=net_borrowing,
            fcfe=fcfe,
            rou_additions=rou_add,
            fcff_leases_as_debt=fcff_lease,
            pension_financing=pension_fin,
            valuation_fcff=fcff_lease - p25.sbc + pension_fin,
            valuation_fcfe=fcfe - p25.sbc,
        )

    @functools.cached_property
    def valuation(self) -> HarbourValuation:
        """Return the valuation at 31 December 2025, at an 8% WACC."""
        wacc, g_ss, ronic_ss = 0.08, 0.025, 0.12
        base = self.base
        fcff = [f.valuation_fcff() for f in base]
        # NOPAT uses book taxes on EBIT with share-based pay non-deductible: EBIT - t(EBIT + SBC).
        nopat_2028 = base[2].op - TAX * (base[2].op + base[2].sbc)
        tv_2028 = terminal_value(nopat_2028 * (1 + g_ss), g_ss, ronic_ss, wacc)
        v_short = (
            sum(c / (1 + wacc) ** (t + 1) for t, c in enumerate(fcff)) + tv_2028 / (1 + wacc) ** 3
        )
        b25 = self.balances[2025]
        claims = dict(
            term_loan=-b25["term_loan"],
            rcf=-b25["revolver"],
            lease=-b25["lease_liab"],
            pension_after_tax=-b25["db_liab"] * (1 - TAX),
        )
        equity_pre_options = v_short + b25["cash"] - sum(claims.values())
        price_iv = OPTIONS.price_per_share(equity_pre_options)
        return HarbourValuation(
            wacc=wacc,
            growth=g_ss,
            ronic=ronic_ss,
            fcff=fcff,
            nopat_2028=nopat_2028,
            terminal_value=tv_2028,
            enterprise_value=v_short,
            claims=claims,
            equity_before_options=equity_pre_options,
            shares=SHARES,
            options=VESTED_OPTIONS,
            option_value=OPTIONS.option(price_iv).call(),
            price=price_iv,
        )

    def forecast(self, case: ForecastCase | None = None) -> list[YearForecast]:
        """Return yearly statements for the forecast years.

        Cash comes from the cash-flow statement; the revolver tops cash up to min_cash (and
        repays when cash is above it). Interest on the revolver uses the average balance, solved
        by iteration. The opening development balance, each later development vintage, acquired
        intangibles and acquired PP&E are separate assets with their own lives and
        available-for-use dates, each charged once. An acquisition completes part-way through
        2026 (acquisition.fraction_2026 of the year); its revenue, EBITDA, amortisation and
        depreciation start at completion, and covenant EBITDA adds the pre-completion part of the
        acquired business's EBITDA (pro forma), as facility agreements usually define it.

        Args:
            case: The assumptions; the base case if omitted.
        """
        if case is None:
            case = ForecastCase()
        price_infl, vol_growth, var_cost_infl = case.price_infl, case.vol_growth, case.var_cost_infl
        fixed_infl, payout, acquisition = case.fixed_infl, case.payout, case.acquisition
        rcf_limit, min_cash, capex_rate = case.rcf_limit, case.min_cash, case.capex_rate
        lockup, sga_rate, lockup_pro_forma = case.lockup, case.sga_rate, case.lockup_pro_forma
        B, R = self.balances, self.ratios
        o = dict(B[2025])
        o = {
            k: (v if (k in ASSETS and k != "acc_dep") else -v) for k, v in o.items()
        }  # credits and acc_dep positive
        o["acq_intangibles"] = 0.0
        vol, price, vcost, fixed = 100.0, 10.8, 4.8, 151.0
        out: list[YearForecast] = []
        years = range(2026, 2050)
        legacy_dev = straight_line(o["development"], LEGACY_DEV_LIFE, 2026, years)
        dev_vintages: dict[int, float] = {}  # year spent -> cost
        frac = acquisition.fraction_2026 if acquisition else 0.0
        acq_int = straight_line(
            acquisition.intangibles if acquisition else 0.0,
            ACQ_INTANGIBLE_LIFE,
            2026,
            years,
            frac,
        )
        acq_ppe_dep = straight_line(
            acquisition.ppe if acquisition else 0.0, ACQ_PPE_LIFE, 2026, years, frac
        )
        acq_ppe_in_gross = (
            0.0  # acquired PP&E is depreciated by its own schedule, not by the organic rate
        )
        prior_lev = (self.balance_view(2025).debt - B[2025]["cash"]) / R[2025].ebitda
        if (
            acquisition and lockup_pro_forma
        ):  # 2026 dividend tested on leverage pro forma for the acquisition
            prior_lev = (self.balance_view(2025).debt - B[2025]["cash"] + acquisition.price) / (
                R[2025].ebitda + acquisition.ebitda
            )
        for k in range(3):
            y = 2026 + k
            vol *= 1 + vol_growth[k]
            price *= 1 + price_infl[k]
            vcost *= 1 + var_cost_infl[k]
            fixed *= 1 + fixed_infl
            share = (frac if k == 0 else 1.0) if acquisition else 0.0
            acq_run_ebitda = acquisition.ebitda * 1.03**k if acquisition else 0.0
            acq_ebitda = acq_run_ebitda * share
            organic = vol * price
            acq_rev = acquisition.revenue * 1.03**k * share if acquisition else 0.0
            revenue = organic + acq_rev
            dep_organic = 0.069 * (o["ppe_gross"] - acq_ppe_in_gross)
            dep_acq = acq_ppe_dep[y]
            dep = dep_organic + dep_acq
            cogs = vol * vcost + fixed + dep_organic
            sga_cash = sga_rate * organic
            sbc = 9.0 * 1.05 ** (k + 1)
            service = 11.0 * 1.03 ** (k + 1)
            rou_dep = 24.0
            research = 0.024 * organic
            dev_amort = legacy_dev[y] + sum(
                straight_line(c, DEV_LIFE, sy + 1, years)[y] for sy, c in dev_vintages.items()
            )
            acq_amort = acq_int[y]
            op = (
                organic
                - cogs
                - sga_cash
                - sbc
                - service
                - rou_dep
                - research
                - dev_amort
                + acq_ebitda
                - acq_amort
                - dep_acq
            )
            lease_int = LEASE_RATE * o["lease_liab"]
            loan_int = LOAN_RATE * o["term_loan"]
            pens_int = DB_RATE * o["db_liab"]
            capex = (
                capex_rate * revenue
            )  # 8.5% of revenue, including the acquired business from completion
            dev_capex = 0.02 * organic
            receivables = (
                organic * 61 / 365
            )  # the acquired business is bought with its working capital settled
            inventory = (
                cogs * 111 / 365
            )  # full production cost, including absorbed depreciation (IAS 2 para. 12)
            payables = vol * vcost * 94 / 365
            accrued = 0.0306 * organic
            restr_paid = o["restructuring_prov"]
            loan_repay = min(25.0, o["term_loan"])
            lease_new, lease_pay = 25.0, 28.0
            acq_cash = acquisition.price if (acquisition and k == 0) else 0.0
            rev_draw, iters = 0.0, 0
            rcf_int = fin = pbt = current = deferred = tax = profit = tax_payable = 0.0
            cfo = cfi = divs = lease_principal = cash_pre = 0.0
            for iters in range(1, 200):
                rcf_avg = o["revolver"] + rev_draw / 2
                rcf_int = 0.06 * rcf_avg
                fin = lease_int + loan_int + pens_int + rcf_int
                pbt = op - fin
                current = TAX * (pbt + sbc - 20.0 - restr_paid)
                deferred = TAX * 20.0 + TAX * restr_paid
                tax = current + deferred
                profit = pbt - tax
                tax_payable = 0.8 * current
                cfo = (
                    profit
                    + dep
                    + rou_dep
                    + dev_amort
                    + acq_amort
                    + sbc
                    + deferred
                    + service
                    + pens_int
                    - 15.0
                    - (receivables - o["receivables"])
                    - (inventory - o["inventory"])
                    + (payables - o["payables"])
                    + (accrued - o["accrued_wages"])
                    + (tax_payable - o["tax_payable"])
                    - restr_paid
                )
                cfi = -capex - dev_capex - acq_cash
                divs = (0.0 if (lockup is not None and prior_lev > lockup) else payout) * profit
                lease_principal = lease_pay - lease_int
                cff_pre = -loan_repay - lease_principal - divs
                # Interest paid is inside CFO (profit after finance costs); the revolver
                # closes the gap to min_cash.
                cash_pre = o["cash"] + cfo + cfi + cff_pre
                new_draw = max(-o["revolver"], min_cash - cash_pre)
                if abs(new_draw - rev_draw) < 1e-12:
                    break
                rev_draw = new_draw
            c = dict(
                cash=cash_pre + rev_draw,
                receivables=receivables,
                inventory=inventory,
                ppe_gross=o["ppe_gross"] + capex,
                acc_dep=o["acc_dep"] + dep,
                rou=o["rou"] + lease_new - rou_dep,
                development=o["development"] + dev_capex - dev_amort,
                acq_intangibles=o["acq_intangibles"] - acq_amort,
                goodwill=o["goodwill"]
                + (acquisition.goodwill if (acquisition and k == 0) else 0.0),
                payables=payables,
                accrued_wages=accrued,
                tax_payable=tax_payable,
                lease_liab=o["lease_liab"] + lease_int - lease_pay + lease_new,
                term_loan=o["term_loan"] - loan_repay,
                revolver=o["revolver"] + rev_draw,
                db_liab=o["db_liab"] + service + pens_int - 15.0,
                dtl=o["dtl"] + deferred,
                restructuring_prov=0.0,
                share_capital=o["share_capital"],
                sbp_reserve=o["sbp_reserve"] + sbc,
                remeasurement_reserve=o["remeasurement_reserve"],
                retained=o["retained"] + profit - divs,
            )
            if acquisition and k == 0:
                # Acquired PP&E and intangibles arrive at completion at fair value (the
                # price less goodwill).
                c["ppe_gross"] += acquisition.ppe
                c["acq_intangibles"] += acquisition.intangibles
                acq_ppe_in_gross = acquisition.ppe
            dev_vintages[y] = dev_capex
            assets = (
                c["cash"]
                + c["receivables"]
                + c["inventory"]
                + c["ppe_gross"]
                - c["acc_dep"]
                + c["rou"]
                + c["development"]
                + c["acq_intangibles"]
                + c["goodwill"]
            )
            liab_eq = (
                sum(c[a] for a in LIABS)
                + c["share_capital"]
                + c["sbp_reserve"]
                + c["remeasurement_reserve"]
                + c["retained"]
            )
            ebitda = op + dep + rou_dep + dev_amort + acq_amort
            cov_ebitda = ebitda + (
                acq_run_ebitda - acq_ebitda
            )  # pro forma for a full year of the acquisition
            debt = c["term_loan"] + c["revolver"] + c["lease_liab"]
            out.append(
                YearForecast(
                    year=y,
                    revenue=revenue,
                    cogs=cogs,
                    op=op,
                    fin=fin,
                    pbt=pbt,
                    tax=tax,
                    current=current,
                    profit=profit,
                    cfo=cfo,
                    cfi=cfi,
                    divs=divs,
                    draw=rev_draw,
                    iters=iters,
                    assets=assets,
                    liab_eq=liab_eq,
                    balance_sheet=c,
                    opening=o,
                    ebitda=ebitda,
                    cov_ebitda=cov_ebitda,
                    debt=debt,
                    net_debt=debt - c["cash"],
                    gross_margin=(organic - cogs) / organic,
                    interest_cover=cov_ebitda / fin,
                    rcf=c["revolver"],
                    liquidity=c["cash"] + rcf_limit - c["revolver"],
                    interest_paid=lease_int + loan_int + rcf_int,
                    lease_int=lease_int,
                    pens_int=pens_int,
                    capex=capex + dev_capex,
                    acq_cash=acq_cash,
                    organic=organic,
                    vol=vol,
                    price=price,
                    vcost=vcost,
                    lease_principal=lease_principal,
                    lease_new=lease_new,
                    loan_repay=loan_repay,
                    sbc=sbc,
                    service=service,
                    dep=dep,
                    dev_amort=dev_amort,
                    acq_amort=acq_amort,
                    dep_acq=dep_acq,
                    rou_dep=rou_dep,
                )
            )
            prior_lev = (debt - c["cash"]) / cov_ebitda
            o = c
        return out
