"""Original accounting cases, 19 October 2026; units stated in the printed entries.

One check is one executed ok() call, including each loop iteration. These checks
reconcile transaction cash ledgers, accounting equations, tax/equity movements,
share counts and forecast financing. They are not tests of source correctness.
Run: uv run python notes/artefacts/statement-accounting/statement-accounting-checks.py
"""

# standard library imports

# third party library imports
import numpy as np

checks = 0


def ok(name, condition):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(name)
    print(f"ok {checks}: {name}")


def close(a, b, tol=1e-8):
    return abs(a - b) < tol


# Meridian: USD millions. Interest and taxes paid are operating cash flows.
opening = dict(
    cash=100.0,
    ar=120.0,
    inventory=180.0,
    ppe=400.0,
    ap=100.0,
    accrual=40.0,
    debt=250.0,
    equity=410.0,
)
actual = dict(
    cash=87.5,
    ar=150.0,
    inventory=200.0,
    ppe=430.0,
    ap=120.0,
    accrual=45.0,
    debt=220.0,
    equity=482.5,
)
forecast = dict(
    cash=96.05,
    ar=165.0,
    inventory=220.0,
    ppe=465.0,
    ap=132.0,
    accrual=49.5,
    debt=200.0,
    equity=564.55,
)
for label, bs in [("2025", opening), ("2026", actual), ("2027", forecast)]:
    assets = sum(bs[k] for k in ("cash", "ar", "inventory", "ppe"))
    liabilities_equity = sum(bs[k] for k in ("ap", "accrual", "debt", "equity"))
    ok(f"{label}: assets equal liabilities plus equity", close(assets, liabilities_equity))

for label, start, end, sales, cogs, sga, depreciation, interest, capex, principal, dividend in [
    ("2026", opening, actual, 1000.0, 600.0, 180.0, 50.0, 20.0, 80.0, 30.0, 40.0),
    ("2027", actual, forecast, 1100.0, 660.0, 198.0, 55.0, 17.6, 90.0, 20.0, 45.0),
]:
    ebit = sales - cogs - sga - depreciation
    tax = (ebit - interest) * 0.25
    ni = ebit - interest - tax
    change = lambda key: end[key] - start[key]
    receipts = sales - change("ar")
    purchases = cogs + change("inventory")
    suppliers = purchases - change("ap")
    staff = sga - change("accrual")
    cfo_direct = receipts - suppliers - staff - interest - tax
    cfo_indirect = (
        ni + depreciation - change("ar") - change("inventory") + change("ap") + change("accrual")
    )
    ok(f"{label}: direct payments ledger equals indirect CFO", close(cfo_direct, cfo_indirect))
    ok(
        f"{label}: cash roll-forward has no balancing plug",
        close(start["cash"] + cfo_direct - capex - principal - dividend, end["cash"]),
    )
    ok(f"{label}: PPE ledger", close(start["ppe"] + capex - depreciation, end["ppe"]))
    ok(f"{label}: equity ledger", close(start["equity"] + ni - dividend, end["equity"]))
    ok(f"{label}: debt ledger", close(start["debt"] - principal, end["debt"]))
    print(
        label,
        dict(
            ebit=ebit,
            tax=tax,
            ni=ni,
            receipts=receipts,
            suppliers=suppliers,
            sga_paid=staff,
            cfo=cfo_direct,
        ),
    )

cfo, ni, capex, interest, net_borrowing = 137.5, 112.5, 80.0, 20.0, -30.0
fcff = cfo + interest * 0.75 - capex
fcff_operating = 170 * 0.75 + 50 - 25 - 80
fcfe = cfo - capex + net_borrowing
ok(
    "FCFF reconciles independent EBIT and operating-capital route",
    close(fcff, fcff_operating) and close(fcff, 72.5),
)
ok(
    "FCFE bridges to FCFF and distributions",
    close(fcfe, fcff - 15 - 30) and close(fcfe - 40, actual["cash"] - opening["cash"]),
)
# IFRS interest-financing presentation: addback cannot be counted twice.
ok("cash-flow classification invariance of FCFF", close((cfo + 20) - 20 * 0.25 - capex, fcff))

# Transaction-price allocation: delivered device and future support.
contract, device_ssp, support_ssp = 120.0, 100.0, 50.0
revenue = contract * device_ssp / (device_ssp + support_ssp)
liability = contract - revenue
ok(
    "customer cash reconciles delivered revenue and contract liability",
    close(revenue, 80) and close(liability, 40) and close(revenue + liability, contract),
)
ok("one support year releases half the two-year obligation", close(revenue + liability / 2, 100))
# Capitalized development starts amortizing next year; tax deducted immediately.
ok("development capitalization changes asset, DTL and equity coherently", close(90, 22.5 + 67.5))
ok("development moves cash classification but not total cash", close((-120 + 90) + (-90), -120))
# EPS sequential inclusion and exclusions.
basic = 110 / 50
options = 10 - 10 * 6 / 10
option_eps = 110 / (50 + options)
converted = (110 + 6) / (50 + options + 5)
preferred_increment = 10 / 4
ok("EPS weighted shares from half-year issuance", close(40 * 0.5 + 60 * 0.5, 50))
ok("treasury stock ledger", close(options, 4) and close(option_eps, 2.037037037037037))
ok(
    "if-converted bond dilutes in sequential order",
    6 / 5 < option_eps and close(converted, 116 / 59),
)
ok(
    "convertible preferred is antidilutive after prior inclusions",
    preferred_increment > converted and (116 + 10) / (59 + 4) > converted,
)
ok("loss-period instruments are excluded", -30 / 54 > -30 / 50 and (-30 + 6) / 55 > -30 / 50)
ok(
    "share split halves both basic and diluted EPS without changing income",
    close(110 / 100, basic / 2) and close(116 / 118, converted / 2),
)

# Cost-flow ledgers: periodic methods; all purchases precede the sale.
for prices in ([10.0, 14.0], [14.0, 10.0]):
    costs = np.repeat(prices, 100)
    fifo_cost, lifo_cost = sum(costs[:150]), sum(costs[-150:])
    avg_cost = costs.mean() * 150
    for name, cost, closing in [
        ("FIFO", fifo_cost, sum(costs[150:])),
        ("LIFO", lifo_cost, sum(costs[:50])),
        ("average", avg_cost, costs.mean() * 50),
    ]:
        ok(
            f"{prices}: {name} purchase cost splits between expense and stock",
            close(cost + closing, sum(costs)),
        )
    ok(
        f"{prices}: inflation reverses the relative cost ordering under deflation",
        (fifo_cost < lifo_cost) == (prices[0] < prices[1]),
    )
ok(
    "rising-price LIFO tax cash benefit is 50 at a hypothetical 25% rate",
    close((3000 - 1700) * 0.25 - (3000 - 1900) * 0.25, 50),
)
ok("LIFO reserve restatement reconciles inventory, deferred tax and equity", close(200, 50 + 150))
ok("NRV write-down: asset -10 plus DTA 2.5 equals equity -7.5", close(-10 + 2.5, -7.5))
ok(
    "IFRS reversal capped at original cost; US new basis unchanged",
    min(100, 105) == 100 and min(90, 105) == 90,
)
# Asset impairment and sale: cash does not follow the accounting write-down.
carrying, viu, fv_less_cost = 100.0, 82.0, 75.0
recoverable = max(viu, fv_less_cost)
ok("IFRS recoverable amount gives impairment 18", close(carrying - recoverable, 18))
ok("US recoverability screen prevents write-down when undiscounted cash is 110", 110 >= carrying)
ok(
    "US failed screen at 95 followed by FV 80 gives loss 20",
    95 < carrying and close(carrying - 80, 20),
)
ok("sale after impairment: cash 90 less carrying 82 gives gain 8", close(90 - recoverable, 8))
ok(
    "useful-life change is prospective: remaining depreciable 54 over six years",
    close((100 - 2 * 18 - 10) / 6, 9),
)
# Tax case: book PBT 100, permanent fine 10, extra tax depreciation 30,
# warranty accrued 8, cash settlements 3. Taxable profit=85.
taxable = 100 + 10 - 30 + 8 - 3
current_tax = taxable * 0.25
dtl, dta = 30 * 0.25, 5 * 0.25
expense = current_tax + dtl - dta
cash_tax = current_tax + 4 - 6
ok(
    "tax provision reconciles temporary differences and permanent difference",
    close(taxable, 85) and close(expense, 27.5) and close(expense, 0.25 * 100 + 0.25 * 10),
)
ok(
    "current-tax balance ledger separates cash tax",
    close(cash_tax, 19.25) and close(4 + current_tax - cash_tax, 6),
)
ok(
    "OCI-only tax does not affect P&L tax or cash tax",
    close(expense, 27.5) and close((dtl + 5) - dtl, 5),
)
# Lease: end-year payments, no costs/incentives; tax ignored.
lease_pv = sum(30 / 1.06**t for t in (1, 2, 3))
liab = lease_pv
for year in (1, 2, 3):
    lease_interest = liab * 0.06
    principal = 30 - lease_interest
    liab -= principal
    independent = sum(30 / 1.06**t for t in range(1, 4 - year))
    ok(f"lease year {year}: liability equals PV of remaining payments", close(liab, independent))
first_interest = lease_pv * 0.06
finance_expense = lease_pv / 3 + first_interest
operating_rou = lease_pv - (30 - first_interest)
finance_rou = lease_pv * 2 / 3
ok(
    "US operating lease asset/liability difference equals expense-pattern difference",
    close(operating_rou - finance_rou, finance_expense - 30),
)
print("lease", lease_pv, first_interest, finance_expense, finance_rou, operating_rou)
# Pension dual ledgers with no settlements, amendments, tax or asset ceiling.
obligation_end = 100 + 8 + 5 + 4 - 6
assets_end = 80 + 6 + 10 - 6
net_end = obligation_end - assets_end
ifrs_expense, ifrs_oci = 8 + 5 - 4, 4 - (6 - 4)
us_expense, us_oci = 8 + 5 - 4.8, 4 - (6 - 4.8)
ok("pension funded status reconciles separate obligation and asset ledgers", close(net_end, 21))
ok(
    "IFRS P&L plus OCI less contributions reconciles net liability",
    close(20 + ifrs_expense + ifrs_oci - 10, net_end),
)
ok(
    "US expected-return model reconciles same total pension cost",
    close(us_expense + us_oci, ifrs_expense + ifrs_oci),
)
forecast_dbo = 111 + 8.4 + 5.55 - 7
forecast_pa = 90 + 4.5 + 12 - 7
ok(
    "pension forecast reconciles closing deficit and contributions",
    close(forecast_dbo - forecast_pa, 18.45) and close(21 + 9.45 - 12, 18.45),
)
# SBC: services, equity and shares; tax ignored for isolated example.
first_charge = 300 * 20 / 3
second_charge = 270 * 20 * 2 / 3 - first_charge
ok(
    "forfeiture update uses cumulative service charge, not stock-price remeasurement",
    close(first_charge, 2000) and close(second_charge, 1600),
)
ok("SBC noncash equity movement balances reduction in retained earnings", close(-2000 + 2000, 0))
ok(
    "share forecast distinguishes weighted average and closing shares",
    close(1000 - 20 + 100 * 0.5, 1030) and close(1000 - 20 + 100, 1080),
)
ok("SBC cohort expense combines old and new grants", close(6000 / 2 + 6000 / 3, 5000))
# Accounting-choice variants of Meridian: premature sale and maintenance capitalization.
reported = actual.copy()
reported["ar"] += 60
reported["inventory"] -= 36
reported["ppe"] += 20
reported["equity"] += 33
reported_dtl = 11
reported_ni = ni + 33
ok(
    "distorted balance sheet still balances",
    close(
        sum(reported[k] for k in ("cash", "ar", "inventory", "ppe")),
        sum(reported[k] for k in ("ap", "accrual", "debt", "equity")) + reported_dtl,
    ),
)
reported_cfo = reported_ni + 50 + 11 - 90 + 16 + 20 + 5
ok(
    "reported CFO and investing classification reconcile unchanged cash",
    close(reported_cfo, 157.5) and close(100 + reported_cfo - 100 - 70, 87.5),
)
ok(
    "corrections reconcile profit, assets, deferred tax and equity",
    close(44 * 0.75, 33) and close(60 - 36 + 20, 11 + 33),
)
ok(
    "CFO above net income is not proof of reporting quality",
    reported_cfo > reported_ni and close(reported_ni, 145.5),
)
# Factoring with recourse treated here as secured borrowing, not a derecognizing sale.
ok(
    "reclassifying financing inflow out of CFO leaves cash unchanged",
    close((137.5 + 20) - 80 - 70, 137.5 - 80 + (-70 + 20)),
)
# Ratios use average stocks with period flows; purchases for payable days.
avg_assets, avg_equity = (800 + 867.5) / 2, (410 + 482.5) / 2
roe = ni / avg_equity
dupont3 = (ni / 1000) * (1000 / avg_assets) * (avg_assets / avg_equity)
dupont5 = (ni / 150) * (150 / 170) * (170 / 1000) * (1000 / avg_assets) * (avg_assets / avg_equity)
ok("three- and five-factor DuPont equal direct ROE", close(roe, dupont3) and close(roe, dupont5))
ratios = dict(
    current=437.5 / 195,
    quick=237.5 / 195,
    cash=87.5 / 195,
    debt_equity=220 / 482.5,
    interest=170 / 20,
    roe=roe,
    roa=ni / avg_assets,
    turnover=1000 / avg_assets,
    dso=135 / 1000 * 365,
    dio=190 / 600 * 365,
    dpo=110 / 620 * 365,
)
ratios["ccc"] = ratios["dso"] + ratios["dio"] - ratios["dpo"]
print("ratios", ratios)
ok("cash conversion cycle reconciles days", close(ratios["ccc"], 100.1002688172043, 1e-6))
# Stress forecast: receipts/costs linked to closing stocks, year-end financing.
stress_sales = 880.0
stress_cogs = 0.6 * stress_sales
stress_sga = 132 + 0.06 * stress_sales
stress_tax = (stress_sales - stress_cogs - stress_sga - 55 - 17.6) * 0.25
stress_ni = (stress_sales - stress_cogs - stress_sga - 55 - 17.6) - stress_tax
stress_ar = 0.2 * stress_sales
stress_inv = 0.45 * stress_cogs
stress_ap = 0.2 * stress_cogs
stress_accrual = 0.25 * stress_sga
stress_cfo = (
    stress_ni
    + 55
    - (stress_ar - 150)
    - (stress_inv - 200)
    + (stress_ap - 120)
    + (stress_accrual - 45)
)
cash_before = 87.5 + stress_cfo - 90 - 20 - 45
needed = 50 - cash_before
without_dividend = 87.5 + stress_cfo - 90 - 20
draw = max(0, 50 - without_dividend)
closing_debt = 220 - 20 + draw
closing_equity = 482.5 + stress_ni
assets = 50 + stress_ar + stress_inv + 465
liabs_equity = stress_ap + stress_accrual + closing_debt + closing_equity
ok(
    "stress with dividends breaches a 60 facility",
    close(stress_cfo, 49.15) and close(needed, 68.35) and needed > 60,
)
ok(
    "suspending dividends fits proposed 30 facility and reconciles balance sheet",
    close(draw, 23.35) and draw <= 30 and close(assets, liabs_equity),
)
ok(
    "facility draw is funded financing; no unexplained cash or equity plug",
    close(without_dividend + draw, 50) and close(closing_debt, 223.35),
)
print(
    "stress",
    dict(
        ni=stress_ni,
        cfo=stress_cfo,
        draw=draw,
        debt=closing_debt,
        equity=closing_equity,
        assets=assets,
        ebitda=stress_sales - stress_cogs - stress_sga,
    ),
)
# Pricing/volume drivers are multiplicative; inflation can compress cash margins.
ok(
    "price-volume bridge does not add overlapping percentage effects",
    close(1000 * 1.04 * 1.03, 1071.2) and not close(1000 * 1.07, 1071.2),
)

# Independent valuation and accounting controls for the remaining examples.
bond_pv = sum(cf / 1.06**t for t, cf in enumerate([5, 5, 105], 1))
bond_close = bond_pv * 1.06 - 5
remaining_pv = 5 / 1.06 + 105 / 1.06**2
ok(
    "effective-interest carrying amount equals discounted remaining payments",
    close(bond_close, remaining_pv) and close(bond_pv, 97.32698805053836),
)
ok(
    "FVOCI gain bridges measured asset to amortized cost",
    close(bond_close + (102 - bond_close), 102) and close(102 - bond_close, 3.83339266642937),
)
assets = [87.5, 150, 200, 430]
funding = [120, 45, 220, 482.5]
ok(
    "common-size shares independently sum to one on both sides",
    close(sum(a / 867.5 for a in assets), 1) and close(sum(v / 867.5 for v in funding), 1),
)
ok(
    "distributor profit per delivery uses million versus thousand units",
    close(400e6 / 80e3, 5000) and close(450e6 / 100e3, 4500),
)
ok(
    "cash and profitability ratios convey different signals",
    87.5 / 195 < 100 / 170 and 170 / 1000 > 144 / 900,
)
ok(
    "partial DTA recovery reconciles allowance and tax expense",
    close(1.25 - 0.75, 0.5) and close(27.5 + 0.5, 28),
)
ok(
    "rate remeasurement is the change in net deferred balance",
    close((30 - 5) * 0.20 - (7.5 - 1.25), -1.25),
)
ok(
    "nonrecurring normalization retains recurring restructuring",
    close((154 - 12) * 0.75, 106.5) and not close((154 - 12 + 8) * 0.75, 106.5),
)
ok("revised depreciation exhausts carrying amount down to residual", close(6 * 9 + 10, 64))
ok(
    "inflation example preserves revenue minus cost gross profit",
    close((1071.2 - 661.44) / 1071.2, 0.3825242718446602),
)
ok(
    "no pass-through and deflation scenarios",
    close((1040 - 661.44) / 1040, 0.364) and close((950 - 588) / 950, 0.38105263157894737),
)
# Terminal values from an explicit growing cash-flow series (1,000 years).
for g, roc, expected in [
    (0.03, 0.10, 1400),
    (0.04, 0.10, 1500),
    (0.03, 0.08, 1250),
    (0.04, 0.08, 1250),
]:
    pv = sum(100 * (1 + g) ** (t - 1) * (1 - g / roc) / 1.08**t for t in range(1, 1001))
    ok(
        f"terminal value from explicit reinvestment cash stream g={g} ROC={roc}",
        close(pv, expected, 1e-7),
    )
ok(
    "DuPont counterexample attributes ROE increase to leverage",
    close(0.1 * 1.2 * 1.5, 0.18)
    and close(0.08 * 1.2 * 2, 0.192)
    and close(0.08 * 1.2 * 1.5, 0.144),
)
print(f"{checks} accounting numerical checks passed")
