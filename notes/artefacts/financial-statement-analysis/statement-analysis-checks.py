"""Financial statement analysis (2026-10-20): the worked numbers of the accounting and statement-analysis entries.

Part 1 builds Harbour Tools plc, a hypothetical IFRS reporter (EUR millions, calendar years 2024-2025), as a
double-entry ledger. The statements are derived from the ledger; the direct cash flow is the sum of tagged cash
postings, and the indirect cash flow is derived separately from the income statement and balance-sheet changes.
The two must agree, the balance sheet must balance and every equity component must roll forward. Later parts
reuse the case for ratios, quality indicators, a three-year forecast, an integrated credit decision, comparability
adjustments and the IFRS 18 transition, and add stand-alone examples for revenue allocation, capitalisation,
EPS, inventory cost formulas, intangibles, impairment, leases, pensions, share-based pay, taxes and forecasting.

Independent routes: ledger versus statement identities; direct versus indirect cash flow; closed-form versus
simulated or iterated quantities; amortisation schedules versus annuity formulas; unit-by-unit inventory layers
versus summary formulas; invariance checks (currency units, classification changes that move but do not change
cash). Numbers are illustrative, not data about any real company.

Count convention: one check is one executed ok() call (a call inside a loop counts once per iteration).

Run: uv run python statement-analysis-checks.py   (numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import math
import sys
from collections import defaultdict

# third party library imports
import numpy as np
import scipy
from scipy.stats import norm

print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
fails = []
n_checks = 0


def ok(name, cond, detail=""):
    global n_checks
    n_checks += 1
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


# ---------------------------------------------------------------------------------------------
print("== part 1: Harbour Tools plc ledger, statements and reconciliations")

# Account classes. Debit balances positive, credit balances negative inside the ledger.
ASSETS = [
    "cash",
    "receivables",
    "inventory",
    "ppe_gross",
    "acc_dep",
    "rou",
    "development",
    "goodwill",
]
LIABS = [
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
EQUITY = ["share_capital", "sbp_reserve", "remeasurement_reserve", "retained"]
INCOME = [
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
OCI = ["oci_remeasurement"]


class Ledger:
    def __init__(self, opening):
        self.bal = defaultdict(float)
        for k, v in opening.items():
            self.bal[k] = v
        self.cash_tags = defaultdict(float)  # (activity, line) -> cash amount
        self.flows = defaultdict(float)  # income and OCI accounts for the year

    def post(self, entries, tag=None):
        """entries: list of (account, debit-positive amount); must sum to zero."""
        assert abs(sum(a for _, a in entries)) < 1e-9, entries
        for acct, amt in entries:
            if acct in INCOME or acct in OCI:
                self.flows[acct] += amt
            else:
                self.bal[acct] += amt
            if acct == "cash":
                assert tag is not None, entries
                self.cash_tags[tag] += amt

    def close_year(self):
        """Close income to retained earnings and OCI to its reserve; return the year's flows."""
        flows = dict(self.flows)
        profit = -sum(flows.get(a, 0.0) for a in INCOME)
        self.bal["retained"] -= profit
        self.bal["remeasurement_reserve"] += flows.get("oci_remeasurement", 0.0)
        tags = dict(self.cash_tags)
        self.flows = defaultdict(float)
        self.cash_tags = defaultdict(float)
        return flows, tags, profit


opening_2023 = {  # balances at 31 December 2023; credits negative
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
opening_2023["retained"] = -sum(opening_2023.values())  # equity residual at the opening date only
L = Ledger(opening_2023)
TAX = 0.25
LEASE_RATE = 0.05
LOAN_RATE = 0.04
DB_RATE = 0.04


def year(L, y):
    """Post one year of Harbour's transactions; parameters differ between 2024 and 2025."""
    p = YEARS[y]
    b = L.bal
    # Sales on credit and collections.
    L.post([("receivables", p["revenue"]), ("revenue", -p["revenue"])])
    collections = b["receivables"] - p["receivables_end"]
    L.post([("cash", collections), ("receivables", -collections)], ("op", "customers"))
    # Production: purchases on credit, production labour accrued, production depreciation, all into inventory.
    L.post([("inventory", p["purchases"]), ("payables", -p["purchases"])])
    L.post([("inventory", p["prod_labour"]), ("accrued_wages", -p["prod_labour"])])
    L.post([("inventory", p["dep"]), ("acc_dep", -p["dep"])])
    cogs = b["inventory"] - p["inventory_end"]
    L.post([("cogs", cogs), ("inventory", -cogs)])
    pay_sup = -(b["payables"]) + p["payables_end"]  # payables are negative balances
    L.post([("payables", pay_sup), ("cash", -pay_sup)], ("op", "suppliers"))
    # Selling and administration.
    L.post([("sga", p["sa_wages"]), ("accrued_wages", -p["sa_wages"])])
    wages_paid = -(b["accrued_wages"]) + p["accrued_wages_end"]
    L.post([("accrued_wages", wages_paid), ("cash", -wages_paid)], ("op", "employees"))
    L.post([("sga", p["other_sga"]), ("cash", -p["other_sga"])], ("op", "other_sga"))
    L.post([("sga", p["rou_dep"]), ("rou", -p["rou_dep"])])
    L.post([("sga", p["sbc"]), ("sbp_reserve", -p["sbc"])])
    # Pension: service cost in S&A, net interest in finance costs, remeasurement in OCI, contributions in cash.
    net_interest = DB_RATE * -b["db_liab"]
    L.post([("sga", p["service_cost"]), ("db_liab", -p["service_cost"])])
    L.post([("fin_pension", net_interest), ("db_liab", -net_interest)])
    L.post([("oci_remeasurement", p["remeasurement_loss"]), ("db_liab", -p["remeasurement_loss"])])
    L.post([("db_liab", p["db_contrib"]), ("cash", -p["db_contrib"])], ("op", "pension_contrib"))
    # Research and development: research expensed in cash, development capitalised (investing), amortised.
    L.post([("rnd", p["research"]), ("cash", -p["research"])], ("op", "research"))
    L.post([("development", p["dev_capex"]), ("cash", -p["dev_capex"])], ("inv", "development"))
    L.post([("rnd", p["dev_amort"]), ("development", -p["dev_amort"])])
    # Restructuring (2025 only): provision, partly paid.
    if p["restructuring"]:
        L.post([("restructuring", p["restructuring"]), ("restructuring_prov", -p["restructuring"])])
        L.post(
            [("restructuring_prov", p["restructuring_paid"]), ("cash", -p["restructuring_paid"])],
            ("op", "restructuring"),
        )
    # Property, plant and equipment: capital expenditure and a disposal with a gain.
    L.post([("ppe_gross", p["capex"]), ("cash", -p["capex"])], ("inv", "capex"))
    cost, accd, proceeds = p["disposal"]
    L.post(
        [
            ("cash", proceeds),
            ("acc_dep", accd),
            ("ppe_gross", -cost),
            ("other_income", -(proceeds - cost + accd)),
        ],
        ("inv", "disposal"),
    )
    # Lease: interest accrues, payment reduces the liability; interest paid classified as operating (IAS 7 choice).
    lease_int = LEASE_RATE * -b["lease_liab"]
    L.post([("fin_lease", lease_int), ("lease_liab", -lease_int)])
    L.post(
        [
            ("lease_liab", p["lease_payment"] - lease_int),
            ("cash", -(p["lease_payment"] - lease_int)),
        ],
        ("fin", "lease_principal"),
    )
    L.post([("lease_liab", lease_int), ("cash", -lease_int)], ("op", "interest_paid"))
    if p["new_lease"]:
        L.post([("rou", p["new_lease"]), ("lease_liab", -p["new_lease"])])  # non-cash addition
    # Term loan: interest on the opening balance, paid; scheduled repayment.
    loan_int = LOAN_RATE * -b["term_loan"]
    L.post([("fin_loan", loan_int), ("cash", -loan_int)], ("op", "interest_paid"))
    L.post([("term_loan", p["loan_repay"]), ("cash", -p["loan_repay"])], ("fin", "loan_repay"))
    # Share options exercised for cash.
    L.post(
        [("cash", p["exercise_cash"]), ("share_capital", -p["exercise_cash"])],
        ("fin", "share_issue"),
    )
    # Taxes: taxable profit adjusts for the non-deductible share-based expense and accelerated tax depreciation.
    pbt = -sum(L.flows[a] for a in INCOME if a not in ("current_tax", "deferred_tax"))
    taxable = (
        pbt + p["sbc"] + p["restructuring"] - p["restructuring_paid"] - (p["tax_dep"] - p["dep"])
    )
    current = TAX * taxable
    deferred = TAX * (p["tax_dep"] - p["dep"]) - TAX * (
        p["restructuring"] - p["restructuring_paid"]
    )
    L.post([("current_tax", current), ("tax_payable", -current)])
    L.post([("deferred_tax", deferred), ("dtl", -deferred)])
    tax_paid = -(b["tax_payable"]) + p["tax_payable_end"]
    L.post([("tax_payable", tax_paid), ("cash", -tax_paid)], ("op", "tax_paid"))
    # Dividends declared and paid; a year-end revolver draw (no interest accrues in the year of the draw).
    L.post([("retained", p["dividends"]), ("cash", -p["dividends"])], ("fin", "dividends"))
    if p["revolver_draw"]:
        L.post(
            [("cash", p["revolver_draw"]), ("revolver", -p["revolver_draw"])], ("fin", "revolver")
        )
    return pbt, taxable


YEARS = {
    2024: dict(
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
    2025: dict(
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

statements = {}
prev = dict(L.bal)
for y in (2024, 2025):
    pbt, taxable = year(L, y)
    flows, tags, profit = L.close_year()
    statements[y] = dict(
        flows=flows,
        tags=tags,
        profit=profit,
        pbt=pbt,
        taxable=taxable,
        open=prev,
        close=dict(L.bal),
    )
    prev = dict(L.bal)


def is_lines(f):
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


for y in (2024, 2025):
    s = statements[y]
    s["is"] = is_lines(s["flows"])
    c, o = s["close"], s["open"]
    assets = sum(c[a] for a in ASSETS)
    liabs = -sum(c[a] for a in LIABS)
    equity = -sum(c[a] for a in EQUITY)
    ok(
        f"{y}: balance sheet balances (assets {assets:.2f} = liabilities {liabs:.2f} + equity {equity:.2f})",
        close(assets, liabs + equity, 1e-9),
    )
    ok(
        f"{y}: ledger profit equals income-statement profit",
        close(s["profit"], s["is"]["profit"], 1e-9),
    )
    # Direct method: sum of tagged cash postings by activity.
    cfo_direct = sum(v for (act, _), v in s["tags"].items() if act == "op")
    cfi = sum(v for (act, _), v in s["tags"].items() if act == "inv")
    cff = sum(v for (act, _), v in s["tags"].items() if act == "fin")
    s.update(cfo=cfo_direct, cfi=cfi, cff=cff)
    # Indirect method from statements only (no ledger tags).
    d = {k: c[k] - o[k] for k in c}
    i = s["is"]
    noncash = (
        (-d["acc_dep"] - (-YEARS[y]["disposal"][1]))
        + YEARS[y]["rou_dep"]
        + YEARS[y]["dev_amort"]
        + YEARS[y]["sbc"]
        + s["flows"]["deferred_tax"]
    )
    # Pension: P&L cost (service + net interest) less contributions = change in liability less OCI part.
    pension_adj = -d["db_liab"] - YEARS[y]["remeasurement_loss"]
    wc = (
        -d["receivables"]
        - d["inventory"]
        - d["payables"]
        - d["accrued_wages"]
        - d["tax_payable"]
        - d["restructuring_prov"]
    )
    cfo_indirect = i["profit"] + noncash - i["other_income"] + pension_adj + wc
    ok(
        f"{y}: indirect CFO equals direct CFO ({cfo_direct:.2f})",
        close(cfo_indirect, cfo_direct, 1e-9),
        f"indirect {cfo_indirect:.4f}",
    )
    ok(
        f"{y}: CFO + CFI + CFF equals change in cash",
        close(cfo_direct + cfi + cff, d["cash"], 1e-9),
        f"{cfo_direct:.2f} {cfi:.2f} {cff:.2f}",
    )
    # Equity roll-forward by component.
    eq_open, eq_close = -sum(o[a] for a in EQUITY), -sum(c[a] for a in EQUITY)
    roll = (
        eq_open
        + i["profit"]
        + i["oci"]
        + YEARS[y]["sbc"]
        + YEARS[y]["exercise_cash"]
        - YEARS[y]["dividends"]
    )
    ok(
        f"{y}: total equity rolls forward (profit, OCI, share-based pay, exercise, dividends)",
        close(roll, eq_close, 1e-9),
    )
    ok(
        f"{y}: retained earnings roll forward",
        close(-o["retained"] + i["profit"] - YEARS[y]["dividends"], -c["retained"], 1e-9),
    )

for y in (2024, 2025):
    s, i = statements[y], statements[y]["is"]
    print(
        f"  {y} IS: revenue {i['revenue']:.2f} cogs {i['cogs']:.2f} gross {i['gross']:.2f} sga {i['sga']:.2f} "
        f"rnd {i['rnd']:.2f} restr {i['restructuring']:.2f} other {i['other_income']:.2f} op {i['op']:.2f} "
        f"fin {i['fin']:.2f} pbt {i['pbt']:.2f} tax {i['tax']:.2f} profit {i['profit']:.4f} oci {i['oci']:.2f}"
    )
    print(
        f"  {y} CF: CFO {s['cfo']:.4f} CFI {s['cfi']:.2f} CFF {s['cff']:.4f}; tags "
        + ", ".join(f"{k[0]}:{k[1]} {v:.2f}" for k, v in sorted(s["tags"].items()))
    )
    c = s["close"]
    print(f"  {y} BS: " + ", ".join(f"{k} {c[k]:.2f}" for k in ASSETS + LIABS + EQUITY))
print(
    "  2023 opening BS: " + ", ".join(f"{k} {opening_2023[k]:.2f}" for k in ASSETS + LIABS + EQUITY)
)


# ---------------------------------------------------------------------------------------------
print(
    "== part 2: common-size statements, ratio families and return decompositions (Harbour 2024-2025)"
)
B = {2023: opening_2023, 2024: statements[2024]["close"], 2025: statements[2025]["close"]}
NEXT_PRINCIPAL = {
    2024: (25, 28 - LEASE_RATE * 60),
    2025: (25, 28 - LEASE_RATE * 65),
}  # (term loan, lease)


def bs_view(y):
    b = B[y]
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
    return dict(
        ca=ca,
        ta=ta,
        cl=cl,
        debt=debt,
        eq=eq,
        net_ppe=b["ppe_gross"] + b["acc_dep"],
        nfo=debt - b["db_liab"] - b["cash"],
    )


def avg(f, y):
    return (f(y) + f(y - 1)) / 2


R = {}
for y in (2024, 2025):
    i, v = statements[y]["is"], bs_view(y)
    p = YEARS[y]
    ebitda = i["op"] + p["dep"] + p["rou_dep"] + p["dev_amort"]
    r = dict(
        gross_margin=i["gross"] / i["revenue"],
        op_margin=i["op"] / i["revenue"],
        net_margin=i["profit"] / i["revenue"],
        dso=365 / (i["revenue"] / avg(lambda t: B[t]["receivables"], y)),
        doh=365 / (i["cogs"] / avg(lambda t: B[t]["inventory"], y)),
        dpo=365 / (p["purchases"] / avg(lambda t: -B[t]["payables"], y)),
        fat=i["revenue"] / avg(lambda t: bs_view(t)["net_ppe"], y),
        tat=i["revenue"] / avg(lambda t: bs_view(t)["ta"], y),
        current=v["ca"] / v["cl"],
        quick=(B[y]["cash"] + B[y]["receivables"]) / v["cl"],
        cash_ratio=B[y]["cash"] / v["cl"],
        debt_equity=v["debt"] / v["eq"],
        net_debt_ebitda=(v["debt"] - B[y]["cash"]) / ebitda,
        net_debt_adj_ebitda=(v["debt"] - B[y]["cash"]) / (ebitda + i["restructuring"]),
        coverage=i["op"] / i["fin"],
        ebitda=ebitda,
        roa=i["profit"] / avg(lambda t: bs_view(t)["ta"], y),
        roe=i["profit"] / avg(lambda t: bs_view(t)["eq"], y),
        lev=avg(lambda t: bs_view(t)["ta"], y) / avg(lambda t: bs_view(t)["eq"], y),
        tax_burden=i["profit"] / i["pbt"],
        interest_burden=i["pbt"] / i["op"],
    )
    r["ccc"] = r["dso"] + r["doh"] - r["dpo"]
    R[y] = r
    ok(
        f"{y}: three-factor DuPont reproduces ROE",
        close(r["net_margin"] * r["tat"] * r["lev"], r["roe"], 1e-12),
    )
    ok(
        f"{y}: five-factor DuPont reproduces ROE",
        close(
            r["tax_burden"] * r["interest_burden"] * r["op_margin"] * r["tat"] * r["lev"],
            r["roe"],
            1e-12,
        ),
    )
    # RNOA + LEV x spread: operating tax = total tax + statutory tax shield on finance costs.
    nfe = i["fin"] * (1 - TAX)
    nopat = i["profit"] + nfe
    noa_avg = avg(lambda t: bs_view(t)["eq"] + bs_view(t)["nfo"], y)
    nfo_avg = avg(lambda t: bs_view(t)["nfo"], y)
    eq_avg = avg(lambda t: bs_view(t)["eq"], y)
    rnoa, nfr = nopat / noa_avg, nfe / nfo_avg
    r.update(rnoa=rnoa, nfr=nfr, flev=nfo_avg / eq_avg, nopat=nopat, noa_avg=noa_avg)
    ok(
        f"{y}: ROE = RNOA + FLEV x (RNOA - NFR)",
        close(rnoa + r["flev"] * (rnoa - nfr), r["roe"], 1e-12),
        f"RNOA {rnoa:.4%}, FLEV {r['flev']:.4f}, NFR {nfr:.4%}, ROE {r['roe']:.4%}",
    )
    print(f"  {y} ratios: " + ", ".join(f"{k} {val:.4f}" for k, val in r.items()))
    cs = {
        k: i[k] / i["revenue"]
        for k in ("cogs", "gross", "sga", "rnd", "restructuring", "op", "fin", "tax", "profit")
    }
    ok(
        f"{y}: common-size income statement lines reconcile to 100% of revenue",
        close(
            1
            - cs["cogs"]
            - cs["sga"]
            - cs["rnd"]
            - cs["restructuring"]
            + i["other_income"] / i["revenue"]
            - cs["fin"]
            - cs["tax"],
            cs["profit"],
            1e-12,
        ),
    )
    ta = bs_view(y)["ta"]
    csb = {a: B[y][a] / ta for a in ASSETS}
    ok(f"{y}: common-size balance sheet assets sum to 100%", close(sum(csb.values()), 1.0, 1e-12))
    print(f"  {y} common-size IS: " + ", ".join(f"{k} {v:.2%}" for k, v in cs.items()))
    print(f"  {y} common-size assets: " + ", ".join(f"{k} {v:.2%}" for k, v in csb.items()))
    print(f"  {y} BS view: " + ", ".join(f"{k} {val:.2f}" for k, val in bs_view(y).items()))

# Covenant breach at year-end makes the whole term loan current (IAS 1 para. 74).
v25 = bs_view(2025)
breach_cl = v25["cl"] + (-B[2025]["term_loan"] - 25)
ok(
    "covenant breach: current ratio falls from 1.84 to 0.94",
    round(v25["ca"] / v25["cl"], 2) == 1.84 and round(v25["ca"] / breach_cl, 2) == 0.94,
    f"current liabilities {breach_cl:.2f}",
)
ok(
    "debt to equity rises from 0.55 to 0.60 with the after-tax pension deficit",
    round(v25["debt"] / v25["eq"], 2) == 0.55
    and round((v25["debt"] - B[2025]["db_liab"] * (1 - TAX)) / v25["eq"], 2) == 0.60,
)
# Exact log attribution of the ROE change 2024 -> 2025 across the five DuPont factors.
fac = ["tax_burden", "interest_burden", "op_margin", "tat", "lev"]
logs = {f: math.log(R[2025][f] / R[2024][f]) for f in fac}
ok(
    "log attribution of ROE change sums exactly",
    close(sum(logs.values()), math.log(R[2025]["roe"] / R[2024]["roe"]), 1e-12),
    ", ".join(f"{f} {v:+.4f}" for f, v in logs.items()),
)
# Same attribution in percentage points by proportional allocation of the ROE change.
droe = R[2025]["roe"] - R[2024]["roe"]
pp = {f: droe * logs[f] / sum(logs.values()) for f in fac}
print(
    "  ROE change attribution (pp): "
    + ", ".join(f"{f} {v * 100:+.3f}" for f, v in pp.items())
    + f"; total {droe * 100:+.3f}"
)
# Restructuring add-back: ROE 2025 excluding the after-tax restructuring charge (tax at 25%, deductible).
i25 = statements[2025]["is"]
adj_profit = i25["profit"] + i25["restructuring"] * (1 - TAX)
ok(
    "2025 ROE excluding restructuring (after-tax 13.5) is higher than reported",
    adj_profit / avg(lambda t: bs_view(t)["eq"], 2025) > R[2025]["roe"],
    f"adjusted profit {adj_profit:.2f}, ROE {adj_profit / avg(lambda t: bs_view(t)['eq'], 2025):.4%}",
)
# Currency-unit invariance: restating in EUR thousands leaves every ratio unchanged.
scaled_roe = (i25["profit"] * 1000) / (avg(lambda t: bs_view(t)["eq"], 2025) * 1000)
ok("ratios are invariant to the currency unit", close(scaled_roe, R[2025]["roe"], 1e-12))


# ---------------------------------------------------------------------------------------------
print("== part 3: cash-flow interpretation, free cash flow and coverage (Harbour 2025)")
s25 = statements[2025]
t25 = s25["tags"]
interest_paid = -t25[("op", "interest_paid")]
capex_net = -(t25[("inv", "capex")] + t25[("inv", "development")] + t25[("inv", "disposal")])
fcff_cfo = s25["cfo"] + interest_paid * (1 - TAX) - capex_net
# Damodaran's route: EBIT(1-t) + D&A - capex - change in WC; reconcile the non-cash items explicitly.
p25 = YEARS[2025]
da = p25["dep"] + p25["rou_dep"] + p25["dev_amort"]
d = {k: B[2025][k] - B[2024][k] for k in B[2025]}
dwc = (
    d["receivables"] + d["inventory"] + d["payables"] + d["accrued_wages"] + d["restructuring_prov"]
)
ebit = i25["op"]
fcff_ebit_book = ebit * (1 - TAX) + da - capex_net - dwc
# Differences: actual cash tax vs statutory tax on EBIT, SBC, pension cost vs contribution, disposal loss, lease
# principal (leases are financing here, so the ROU depreciation added back is offset by treating lease payments as
# debt service), and tax-payable change.
cash_tax_on_ebit = -t25[("op", "tax_paid")] + interest_paid * TAX
recon = (
    (ebit - cash_tax_on_ebit)
    + da
    + p25["sbc"]
    + (p25["service_cost"] - p25["db_contrib"])
    - i25["other_income"]
    - capex_net
    - dwc
)
ok(
    "FCFF from CFO equals EBIT less cash operating taxes plus non-cash items less investment",
    close(fcff_cfo, recon, 1e-9),
    f"FCFF {fcff_cfo:.4f}; textbook EBIT(1-t) route {fcff_ebit_book:.4f}",
)
net_borrowing = (
    t25[("fin", "loan_repay")] + t25[("fin", "revolver")] + t25[("fin", "lease_principal")]
)
fcfe = s25["cfo"] - capex_net + net_borrowing
fcfe_from_fcff = fcff_cfo - interest_paid * (1 - TAX) + net_borrowing
ok(
    "FCFE from CFO equals FCFF less after-tax interest plus net borrowing",
    close(fcfe, fcfe_from_fcff, 1e-9),
    f"FCFE {fcfe:.4f}, net borrowing {net_borrowing:.2f}",
)
ok(
    "FCFE reconciles to dividends + buybacks - issues + change in cash",
    close(fcfe, -t25[("fin", "dividends")] - t25[("fin", "share_issue")] + d["cash"], 1e-9),
)
# Explicit bridge from the EBIT(1-t) route to the CFO route, item by item.
bridge = dict(
    sbc=p25["sbc"],
    pension_service_less_contrib=p25["service_cost"] - p25["db_contrib"],
    disposal_loss=-i25["other_income"],
    cash_vs_statutory_tax_on_ebit=TAX * ebit - cash_tax_on_ebit,
)
ok(
    "FCFF bridge: EBIT route + SBC + (service cost - contributions) + disposal loss + tax difference = CFO route",
    close(fcff_ebit_book + sum(bridge.values()), fcff_cfo, 1e-9),
    ", ".join(f"{k} {v:+.2f}" for k, v in bridge.items()),
)
debt_close = bs_view(2025)["debt"]
cov = dict(
    cfo_to_debt=s25["cfo"] / debt_close,
    cfo_to_capex=s25["cfo"] / capex_net,
    cash_interest_cov=(s25["cfo"] + interest_paid - t25[("op", "tax_paid")]) / interest_paid,
    debt_payback_years=debt_close / s25["cfo"],
    retained_cfo_to_investment=(s25["cfo"] + t25[("fin", "dividends")]) / capex_net,
    adequacy_2y=(statements[2024]["cfo"] + s25["cfo"])
    / (
        -(statements[2024]["tags"][("inv", "capex")] + t25[("inv", "capex")])
        - (statements[2024]["tags"][("inv", "development")] + t25[("inv", "development")])
        + max(0, B[2024]["inventory"] - B[2023]["inventory"])
        + max(0, d["inventory"])
        - statements[2024]["tags"][("fin", "dividends")]
        - t25[("fin", "dividends")]
    ),
)
cs_cf = {k: v / i25["revenue"] for k, v in t25.items()}
print("  2025 coverage: " + ", ".join(f"{k} {v:.4f}" for k, v in cov.items()))
print(
    "  2025 common-size cash flows (% revenue): "
    + ", ".join(f"{k[0]}:{k[1]} {v:.2%}" for k, v in sorted(cs_cf.items()))
)
ok(
    "cash interest coverage exceeds 10 and CFO covers net investment",
    cov["cash_interest_cov"] > 10 and cov["cfo_to_capex"] > 1,
    f"FCFF {fcff_cfo:.2f}, FCFE {fcfe:.2f}",
)
# Sustainability decomposition of 2025 CFO: working-capital, provision and pension-funding effects.
wc_effect = -dwc
ok(
    "2025 CFO components: provision build adds 12, working capital absorbs cash",
    close(d["restructuring_prov"] * -1, 12, 1e-9) and wc_effect < 12,
    f"working capital incl. provision {wc_effect:+.2f}",
)


# ---------------------------------------------------------------------------------------------
print("== part 4: basic and diluted EPS with antidilution (Kestrel, illustrative)")
# Shares: 40m at 1 Jan; 6m issued 1 Apr; 2m bought back 1 Oct; 1-for-10 bonus issue 30 Nov (retrospective).
months = 12
wa_pre_bonus = 40 + 6 * 9 / months - 2 * 3 / months
wa = wa_pre_bonus * 1.1
# Day-count independent check: monthly share counts averaged.
monthly = [40] * 3 + [46] * 6 + [44] * 3
ok(
    "weighted average shares: formula equals month-by-month average",
    close(np.mean(monthly) * 1.1, wa, 1e-12),
    f"{wa:.4f}m",
)
profit, pref_cum, pref_conv_div = 50.0, 2.0, 3.0
basic_num = profit - pref_cum - pref_conv_div
basic = basic_num / wa
avg_price = 12.0
# Potential shares: (name, numerator add-back, incremental shares)
opt_vested = ("options_vested", 0.0, 3.0 - 3.0 * 8 / avg_price)
opt_unvested_price = (
    9 + 3.5
)  # IAS 33 para 47A: exercise price plus unrecognised future-service fair value
opt_unvested = (
    "options_unvested",
    0.0,
    max(0.0, 1.0 - 1.0 * opt_unvested_price / avg_price) if opt_unvested_price < avg_price else 0.0,
)
bond = ("convertible_bond", 6.0 * (1 - 0.25), 5.0)
pref = ("convertible_pref", pref_conv_div, 2.5)
pot = [opt_vested, opt_unvested, bond, pref]
seq = sorted([p for p in pot if p[2] > 0], key=lambda p: p[1] / p[2])
num, den, included = basic_num, wa, []
for name, add, sh in seq:
    trial = (num + add) / (den + sh)
    if trial < num / den:
        num, den = num + add, den + sh
        included.append(name)
diluted = num / den
# Independent route: minimum EPS over all subsets of potential shares (maximum dilution).
best = min(
    (
        (basic_num + sum(p[1] for p, b in zip(pot, mask) if b))
        / (wa + sum(p[2] for p, b in zip(pot, mask) if b)),
        mask,
    )
    for mask in np.ndindex(*(2,) * len(pot))
)
ok(
    "IAS 33 sequencing gives the most dilutive EPS (equals the subset minimum)",
    close(best[0], diluted, 1e-12),
    f"basic {basic:.4f}, diluted {diluted:.4f}, included {included}",
)
ok(
    "convertible preference shares are antidilutive (EPI 1.20 exceeds diluted EPS)",
    "convertible_pref" not in included and pref[1] / pref[2] > diluted,
)
ok(
    "unvested options with 47A-adjusted price 12.50 above average 12 add no shares",
    opt_unvested[2] == 0.0,
)
# Harbour 2025 basic EPS: 100m shares at 1 Jan 2025, 0.75m issued on exercise at EUR 8 on 1 Jul 2025.
h_wa = 100 + 0.75 * 0.5
h_basic = statements[2025]["is"]["profit"] / h_wa
h_inc = 5.0 - 5.0 * 8 / 11  # 5m vested options at EUR 8, average price EUR 11
h_diluted = statements[2025]["is"]["profit"] / (h_wa + h_inc)
ok(
    "Harbour 2025 EPS: basic and diluted (treasury-stock method)",
    h_diluted < h_basic,
    f"basic {h_basic:.4f}, diluted {h_diluted:.4f}, incremental shares {h_inc:.4f}m",
)


# ---------------------------------------------------------------------------------------------
print(
    "== part 5: revenue recognition (allocation, timing, variable consideration, principal/agent)"
)
tp = 1000.0
ssp = {"equipment": 900.0, "installation": 100.0, "service_24m": 200.0}
alloc = {k: tp * v / sum(ssp.values()) for k, v in ssp.items()}
ok(
    "relative stand-alone selling price allocation sums to the transaction price",
    close(sum(alloc.values()), tp, 1e-9),
    ", ".join(f"{k} {v:.2f}" for k, v in alloc.items()),
)
# Delivery 1 Nov 2025 (equipment), installation completed 30 Nov 2025, service 1 Dec 2025-30 Nov 2027 straight-line.
rev_2025 = alloc["equipment"] + alloc["installation"] + alloc["service_24m"] / 24
rev_2026 = alloc["service_24m"] * 12 / 24
rev_2027 = alloc["service_24m"] * 11 / 24
ok(
    "revenue over the contract life equals the transaction price",
    close(rev_2025 + rev_2026 + rev_2027, tp, 1e-9),
    f"2025 {rev_2025:.4f}, 2026 {rev_2026:.4f}, 2027 {rev_2027:.4f}",
)
# Paid in full on signing (1 Oct 2025): contract liability at 31 Dec 2025.
ok(
    "contract liability at year-end equals unsatisfied service obligation",
    close(tp - rev_2025, rev_2026 + rev_2027, 1e-9),
    f"{tp - rev_2025:.4f}",
)
# Variable consideration: volume rebate. Expected value of the price vs constrained amount.
outcomes = np.array([100.0, 95.0, 90.0])  # price per unit after rebate tiers
probs = np.array([0.5, 0.3, 0.2])
ev = outcomes @ probs
# Constraint: include only the amount for which a significant reversal is highly probable not to occur.
cum = np.cumsum(probs)  # outcomes sorted from highest price: P(price >= outcome)
# Illustrative reading of "highly probable": at least 90 percent (the standard sets no numeric threshold).
constrained = max(o for o, pr in zip(outcomes, cum) if pr >= 0.9)
ok(
    "constrained variable consideration is below the expected value",
    constrained < ev,
    f"expected {ev:.2f}, constrained {constrained:.2f}",
)
# Principal vs agent: same profit, different revenue and margins.
gross_sale, cost_to_vendor = 100.0, 85.0
principal = dict(revenue=gross_sale, profit=gross_sale - cost_to_vendor)
agent = dict(revenue=gross_sale - cost_to_vendor, profit=gross_sale - cost_to_vendor)
ok(
    "principal and agent presentations give the same profit but different margins",
    close(principal["profit"], agent["profit"])
    and agent["profit"] / agent["revenue"] > principal["profit"] / principal["revenue"],
    f"margins {principal['profit'] / principal['revenue']:.0%} vs {agent['profit'] / agent['revenue']:.0%}",
)


# ---------------------------------------------------------------------------------------------
print("== part 6: capitalising versus expensing (development spend amortised over three years)")


def capitalisation_paths(spend, life=3):
    asset, out = 0.0, []
    for t, x in enumerate(spend):
        amort = sum(
            spend[k] / life for k in range(max(0, t - life), t)
        )  # straight-line from the following year
        asset += x - amort
        out.append(dict(amort=amort, asset=asset, expense_diff=x - amort))
    return out


for label, spend in (("constant", [30.0] * 6), ("growing 10%", [30.0 * 1.1**t for t in range(6)])):
    path = capitalisation_paths(spend)
    cum_diff = sum(p["expense_diff"] for p in path)
    ok(
        f"{label} spend: cumulative pre-tax profit difference equals the capitalised asset",
        close(cum_diff, path[-1]["asset"], 1e-9),
        f"year-6 profit uplift {path[-1]['expense_diff']:.3f}, asset {path[-1]['asset']:.3f}",
    )
    if label == "constant":
        ok(
            "constant spend: profit uplift vanishes once amortisation catches up (year 4 onward)",
            all(abs(p["expense_diff"]) < 1e-9 for p in path[3:]),
        )
# Cash flow: total cash is identical; classification moves 30 from operating to investing.
cfo_expense, cfo_cap = 200.0 - 30.0, 200.0
# Interest capitalisation (IAS 23): coverage ratio rises although cash interest is unchanged.
ebit, interest_total, capitalised = 60.0, 20.0, 8.0
ok(
    "capitalised borrowing costs raise reported interest coverage",
    ebit / (interest_total - capitalised) > ebit / interest_total,
    f"{ebit / interest_total:.2f}x -> {ebit / (interest_total - capitalised):.2f}x",
)


# ---------------------------------------------------------------------------------------------
print("== part 7: inventory cost formulas, LIFO restatement, liquidation and net realisable value")


def run_inventory(open_layers, purchases, units_sold, method):
    """Periodic system; layers are [units, unit cost]; returns COGS and closing layers."""
    layers = [list(lay) for lay in open_layers] + [list(p) for p in purchases]
    if method == "wac":
        units = sum(u for u, _ in layers)
        cost = sum(u * c for u, c in layers)
        unit = cost / units
        return units_sold * unit, [[units - units_sold, unit]]
    order = layers if method == "fifo" else layers[::-1]
    remaining, cogs, kept = units_sold, 0.0, []
    for u, c in order:
        take = min(u, remaining)
        cogs += take * c
        remaining -= take
        if u - take > 0:
            kept.append([u - take, c])
    return cogs, (kept if method == "fifo" else kept[::-1])


open_layers = [[40, 500.0]]
for label, price in (("rising", 600.0), ("falling", 400.0)):
    res = {m: run_inventory(open_layers, [[60, price]], 30, m) for m in ("fifo", "wac", "lifo")}
    sales = 30 * 800.0
    gp = {m: sales - res[m][0] for m in res}
    end = {m: sum(u * c for u, c in res[m][1]) for m in res}
    available = 40 * 500 + 60 * price
    ok(
        f"{label} costs: COGS + closing inventory = goods available for every method",
        all(close(res[m][0] + end[m], available, 1e-9) for m in res),
        ", ".join(f"{m} GP {gp[m]:.0f} end {end[m]:.0f}" for m in res),
    )
    order_ok = (
        gp["fifo"] > gp["wac"] > gp["lifo"] if price > 500 else gp["fifo"] < gp["wac"] < gp["lifo"]
    )
    ok(f"{label} costs: gross-profit ordering FIFO vs WAC vs LIFO", order_ok)
    if price > 500:
        econ = 30 * (800 - 600)
        holding = 30 * (600 - 500)
        ok(
            "rising costs: FIFO gross profit = economic profit + holding gain",
            close(gp["fifo"], econ + holding, 1e-9),
        )
# LIFO to FIFO restatement with a LIFO reserve (US GAAP reporter; IFRS prohibits LIFO).
lifo_inv, reserve_open, reserve_close, t = 1999.0, 950.0, 1002.0, 0.35
fifo_inv = lifo_inv + reserve_close
cogs_lifo = 5000.0
cogs_fifo = cogs_lifo - (reserve_close - reserve_open)
ok(
    "LIFO to FIFO: COGS falls by the increase in the reserve; equity rises by reserve x (1 - t)",
    close(cogs_lifo - cogs_fifo, 52.0, 1e-9) and close(reserve_close * (1 - t), 651.3, 1e-9),
    f"FIFO inventory {fifo_inv:.0f}, after-tax equity uplift {reserve_close * (1 - t):.1f}",
)
# Inflation estimate from a LIFO reporter: r = change in reserve / prior FIFO inventory.
r_est = (reserve_close - reserve_open) / (1366.0 + 950.0)
ok(
    "FIFO-to-LIFO bridge: COGS_LIFO = COGS_FIFO + BI_FIFO x r",
    close(cogs_fifo + (1366.0 + 950.0) * r_est, cogs_lifo, 1e-9),
    f"r = {r_est:.4%}",
)
# LIFO liquidation: selling old cheap layers raises profit when prices rise.
cogs_normal, _ = run_inventory([[40, 500.0]], [[30, 600.0]], 30, "lifo")
cogs_liq, _ = run_inventory([[40, 500.0]], [[10, 600.0]], 30, "lifo")
ok(
    "LIFO liquidation lowers COGS when older layers are cheaper",
    cogs_liq < cogs_normal,
    f"liquidation profit {cogs_normal - cogs_liq:.0f}",
)
# Net realisable value: write-down and reversal under IAS 2; US LCNRV records no annual reversal.
cost, nrv1, nrv2 = 100.0, 80.0, 95.0
wd = max(0.0, cost - nrv1)
ifrs_reversal = min(wd, max(0.0, min(cost, nrv2) - (cost - wd)))
ok(
    "IAS 2 reversal is limited to the original write-down",
    close(ifrs_reversal, 15.0) and ifrs_reversal <= wd,
    f"write-down {wd:.0f}, reversal {ifrs_reversal:.0f}",
)


# ---------------------------------------------------------------------------------------------
print(
    "== part 8: intangibles - purchased, internally developed and acquired in a business combination"
)
consideration, book_net = 500.0, 250.0
uplifts = {
    "ppe": 30.0,
    "customer_relationships": 90.0,
    "brand_indefinite": 60.0,
    "in_process_rnd": 40.0,
}
dtl_bc = TAX * sum(uplifts.values())
identifiable = book_net + sum(uplifts.values()) - dtl_bc
goodwill = consideration - identifiable
ok(
    "goodwill = consideration - fair value of identifiable net assets (including DTL on uplifts)",
    close(goodwill, 85.0, 1e-9),
    f"identifiable {identifiable:.2f}, goodwill {goodwill:.2f}",
)
# Post-acquisition annual charges: customer relationships over 10 years; brand, IPR&D and goodwill not amortised.
annual_amort_bc = uplifts["customer_relationships"] / 10 + uplifts["ppe"] / 6
# Internal development: IFRS capitalises once criteria are met (24 of 40 spent), US GAAP expenses all (non-software).
spent, after_criteria = 40.0, 24.0
ifrs_expense, us_expense = spent - after_criteria, spent
# Purchased patent: capitalised at cost 50, amortised over 5 years under both frameworks.


# ---------------------------------------------------------------------------------------------
print("== part 9: impairment (IAS 36 vs US two-step), reversal, derecognition and PP&E age")
carrying, undiscounted, fvlcod, viu, fair_value = 200.0, 230.0, 150.0, 170.0, 165.0
recoverable = max(fvlcod, viu)
ifrs_loss = max(0.0, carrying - recoverable)
us_loss = (carrying - fair_value) if undiscounted < carrying else 0.0
ok(
    "IAS 36 impairs to recoverable amount; US recoverability test passes on undiscounted flows",
    close(ifrs_loss, 30.0) and us_loss == 0.0,
    f"IFRS loss {ifrs_loss:.0f}, US loss {us_loss:.0f}",
)
# Remaining life 5 years, straight-line. Next year recoverable amount recovers to 190.
life = 5
dep_no_imp = carrying / life
carrying_no_imp_y1 = carrying - dep_no_imp
carrying_y1 = (carrying - ifrs_loss) - (carrying - ifrs_loss) / life
reversal = min(190.0, carrying_no_imp_y1) - carrying_y1
ok(
    "IAS 36 reversal capped at the carrying amount that would have existed without impairment",
    close(carrying_y1 + reversal, carrying_no_imp_y1, 1e-9),
    f"reversal {reversal:.2f}",
)
# Ratio effect: after impairment, depreciation falls and asset base shrinks, so ROA rises.
ebit_pre = 50.0  # operating profit before this asset's depreciation
roa_before = (ebit_pre - dep_no_imp) / (carrying - dep_no_imp / 2)
roa_after = (ebit_pre - (carrying - ifrs_loss) / life) / (
    (carrying - ifrs_loss) - (carrying - ifrs_loss) / life / 2
)
ok(
    "future ROA rises after a write-down (lower depreciation, smaller base)",
    roa_after > roa_before,
    f"{roa_before:.4%} -> {roa_after:.4%}",
)
# Derecognition: gain = net proceeds - carrying amount; proceeds are investing cash.
ok(
    "derecognition gain = proceeds - carrying amount reproduces Harbour's 2024 other income from the ledger",
    close(13 - (40 - 30), statements[2024]["is"]["other_income"], 1e-12),
)
# Harbour 2025 PP&E disclosure analysis.
gross, accd, dep = B[2025]["ppe_gross"], -B[2025]["acc_dep"], YEARS[2025]["dep"]
avg_age, total_life, remaining = accd / dep, gross / dep, (gross - accd) / dep
ok(
    "PP&E average age + remaining life = average total life",
    close(avg_age + remaining, total_life, 1e-12),
    f"age {avg_age:.2f}y, remaining {remaining:.2f}y, total {total_life:.2f}y",
)


# ---------------------------------------------------------------------------------------------
print("== part 10: lessee (IFRS 16 vs ASC 842 operating) and lessor accounting")
pay, n, rate = 100.0, 5, 0.05
pv = pay * (1 - (1 + rate) ** -n) / rate
liab, rows = pv, []
for t in range(1, n + 1):
    interest = liab * rate
    liab = liab + interest - pay
    rows.append(dict(t=t, interest=interest, closing=liab))
ok(
    "lease liability amortises to zero; closed-form annuity matches the schedule",
    close(rows[-1]["closing"], 0.0, 1e-9),
    f"PV {pv:.4f}, year-1 interest {rows[0]['interest']:.4f}",
)
ifrs_exp = [pv / n + r["interest"] for r in rows]
us_exp = [pay] * n
ok(
    "total lease expense equals total payments under both models",
    close(sum(ifrs_exp), sum(us_exp), 1e-9),
)
ok(
    "IFRS 16 expense is front-loaded relative to the straight-line ASC 842 operating cost",
    ifrs_exp[0] > us_exp[0] > ifrs_exp[-1],
    f"IFRS year 1 {ifrs_exp[0]:.2f}, year 5 {ifrs_exp[-1]:.2f}",
)
# ASC 842 operating ROU asset = liability adjusted for accrued straight-line differences (no prepayment here).
us_rou = []
liab_t, rou_t = pv, pv
for r in rows:
    amort = pay - r["interest"]  # single cost 100 = accretion + ROU amortisation
    rou_t -= amort
    us_rou.append(rou_t)
ok(
    "ASC 842 operating ROU asset equals the lease liability throughout (even payments, no incentives)",
    all(close(a, r["closing"], 1e-9) for a, r in zip(us_rou, rows)),
)
ifrs_rou_y1 = pv - pv / n
ok(
    "year 1: IFRS 16 ROU asset is below the US operating ROU asset (faster depreciation)",
    ifrs_rou_y1 < us_rou[0],
    f"IFRS {ifrs_rou_y1:.2f} vs US {us_rou[0]:.2f}",
)
# Lessor: finance lease (net investment) vs operating lease (asset retained, straight-line income).
asset_cost = pv  # selling-price = PV, no selling profit for simplicity
fin_income = [r["interest"] for r in rows]
op_income = [pay - asset_cost / n] * n
ok(
    "lessor: finance-lease interest income and operating-lease net income sum to the same total",
    close(sum(fin_income), sum(op_income), 1e-9),
    f"{sum(fin_income):.2f}",
)


# ---------------------------------------------------------------------------------------------
print("== part 11: defined benefit pensions (IAS 19 vs US GAAP), sensitivity and modelling")
dbo0, fva0, disc, exp_ret, act_ret = 1000.0, 800.0, 0.04, 0.06, 0.02
service, benefits, contrib, act_loss = 30.0, 50.0, 40.0, 20.0
aoci_loss_open, remaining_service = 120.0, 10.0
interest_cost = disc * dbo0
dbo1 = dbo0 + service + interest_cost + act_loss - benefits
fva1 = fva0 * (1 + act_ret) + contrib - benefits
deficit0, deficit1 = dbo0 - fva0, dbo1 - fva1
# IFRS: service + net interest in P&L; remeasurements in OCI.
ifrs_pl = service + disc * deficit0
ifrs_oci = act_loss + (disc * fva0 - act_ret * fva0)
# US GAAP: expected return on assets; corridor amortisation of the opening net loss.
corridor = 0.10 * max(dbo0, fva0)
amort = max(0.0, aoci_loss_open - corridor) / remaining_service
us_pl = service + interest_cost - exp_ret * fva0 + amort
us_oci = act_loss + (exp_ret * fva0 - act_ret * fva0) - amort
ok(
    "funded status roll-forward: deficit change = total cost - contributions (both frameworks)",
    close(deficit1 - deficit0, ifrs_pl + ifrs_oci - contrib, 1e-9)
    and close(ifrs_pl + ifrs_oci, us_pl + us_oci, 1e-9),
    f"deficit {deficit0:.0f} -> {deficit1:.0f}; IFRS P&L {ifrs_pl:.2f} OCI {ifrs_oci:.2f}; US P&L {us_pl:.2f} OCI {us_oci:.2f}",
)
ok("US expected-return accounting reports lower P&L cost than IAS 19 here", us_pl < ifrs_pl)
# Economic cost: service + interest - actual return + actuarial loss.
economic = service + interest_cost - act_ret * fva0 + act_loss
ok(
    "economic pension cost equals total comprehensive cost",
    close(economic, ifrs_pl + ifrs_oci, 1e-9),
    f"{economic:.2f}",
)
# Sensitivity: obligation as level benefit payments; duration approximation vs exact repricing.
cfs = np.full(25, 1.0)
times = np.arange(1, 26)
pv_dbo = lambda y: float(np.sum(cfs / (1 + y) ** times))
dur_mod = float(np.sum(times * cfs / (1 + disc) ** (times + 1))) / pv_dbo(disc)
exact = pv_dbo(disc + 0.005) / pv_dbo(disc) - 1
approx = -dur_mod * 0.005
ok(
    "+50bp discount rate: modified-duration approximation is close to exact repricing (convexity small)",
    abs(exact - approx) < 0.004,
    f"exact {exact:.4%}, duration {approx:.4%}, duration {dur_mod:.2f}",
)
# Modelling: debt-like adjustment and operating/financing split (Harbour 2025 deficit 48.16).
db_after_tax = -B[2025]["db_liab"] * (1 - TAX)
ok(
    "after-tax pension deficit treated as debt-like claim",
    close(db_after_tax, 36.12, 1e-9),
    f"{db_after_tax:.2f}",
)


# ---------------------------------------------------------------------------------------------
print(
    "== part 12: share-based payment - fair value, vesting, forfeiture true-up and dilution modelling"
)


def bs_call(S, K, T, r, sigma, q=0.0):
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return S * math.exp(-q * T) * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)


S0, K, T_exp, r_f, vol, q = 20.0, 20.0, 5.0, 0.03, 0.30, 0.01
fv = bs_call(S0, K, T_exp, r_f, vol, q)
z = np.random.default_rng(42).standard_normal(1_000_000)
ST = S0 * np.exp((r_f - q - 0.5 * vol**2) * T_exp + vol * math.sqrt(T_exp) * z)
mc = math.exp(-r_f * T_exp) * np.maximum(ST - K, 0).mean()
ok(
    "grant-date fair value: Black-Scholes-Merton matches Monte Carlo",
    abs(mc - fv) < 0.02,
    f"BSM {fv:.4f}, MC {mc:.4f}",
)
granted, expected_forfeit, actual_forfeit = 3.0, 0.10, 0.15
cum_expected = [granted * (1 - expected_forfeit) * fv * t / 3 for t in (1, 2)]
final = granted * (1 - actual_forfeit) * fv
exp_y = [cum_expected[0], cum_expected[1] - cum_expected[0], final - cum_expected[1]]
ok(
    "IFRS 2 true-up: cumulative expense equals fair value of options that vest",
    close(sum(exp_y), final, 1e-12),
    ", ".join(f"{e:.4f}" for e in exp_y),
)
ok("true-up lowers the year-3 charge when forfeitures exceed expectations", exp_y[2] < exp_y[0])
# Forecast dilution: treasury-stock incremental shares at a forecast average price.
outstanding = granted * (1 - actual_forfeit)
for price in (25.0, 18.0):
    inc = max(0.0, outstanding - outstanding * K / price)
    print(f"  forecast price {price:.0f}: incremental diluted shares {inc:.4f}m")
ok(
    "dilution is zero when the forecast price is below the exercise price",
    max(0.0, outstanding - outstanding * K / 18.0) == 0.0,
)


# ---------------------------------------------------------------------------------------------
print("== part 13: income taxes - temporary and permanent differences, deferred tax, rate measures")
i25 = statements[2025]["is"]
statutory_tax = TAX * i25["pbt"]
perm = TAX * YEARS[2025]["sbc"]
ok(
    "Harbour 2025 rate reconciliation: statutory tax + non-deductible SBC = tax expense",
    close(statutory_tax + perm, i25["tax"], 1e-9),
    f"statutory {statutory_tax:.4f}, permanent {perm:.4f}, total {i25['tax']:.4f}",
)
etr = i25["tax"] / i25["pbt"]
current_rate = statements[2025]["flows"]["current_tax"] / i25["pbt"]
cash_rate = -statements[2025]["tags"][("op", "tax_paid")] / i25["pbt"]
ok(
    "ETR, current-tax rate and cash tax rate differ in the expected order",
    cash_rate < current_rate < etr,
    f"ETR {etr:.4%}, current {current_rate:.4%}, cash {cash_rate:.4%}",
)
# Temporary difference: carrying amount vs tax base of PP&E.
tax_base_gap = (90 - 60) + (92 - 66)  # cumulative excess tax depreciation 2024-2025
dta_restr = TAX * (18 - 6)
ok(
    "closing DTL = opening DTL + 25% of accelerated depreciation - DTA on the unpaid restructuring provision",
    close(-B[2025]["dtl"], 30 + TAX * tax_base_gap - dta_restr, 1e-9),
    f"DTL {-B[2025]['dtl']:.2f}",
)
# Rate change: DTL of 41 remeasured from 25% to 20% when enacted.
dtl_temp_diff = -B[2025]["dtl"] / TAX
ok(
    "enacted rate cut remeasures the deferred tax liability through tax expense",
    close(dtl_temp_diff * 0.20, 32.8, 1e-9),
    f"deferred tax income {-B[2025]['dtl'] - dtl_temp_diff * 0.20:.2f}",
)
# Analytical treatment: growing capex keeps the DTL from reversing (equity-like); a shrinking asset base reverses it.
book_dep_life, tax_dep_life = 10, 5
for label, growth in (("growing 5%", 0.05), ("no new capex after year 10", None)):
    dtl_path, assets = [], []
    for yr in range(30):
        if growth is None:
            spend = 100.0 if yr < 10 else 0.0
        else:
            spend = 100.0 * (1 + growth) ** yr
        assets.append(spend)
        book = sum(a / book_dep_life for k, a in enumerate(assets) if 0 <= yr - k < book_dep_life)
        taxd = sum(a / tax_dep_life for k, a in enumerate(assets) if 0 <= yr - k < tax_dep_life)
        dtl_path.append((dtl_path[-1] if dtl_path else 0.0) + TAX * (taxd - book))
    print(
        f"  {label}: DTL year 10 {dtl_path[9]:.2f}, year 20 {dtl_path[19]:.2f}, year 30 {dtl_path[29]:.2f}"
    )
    if growth is None:
        ok("without new capex the DTL fully reverses", close(dtl_path[-1], 0.0, 1e-9))
    else:
        ok(
            "with growing capex the DTL keeps rising (no net reversal)",
            dtl_path[29] > dtl_path[19] > dtl_path[9],
        )


# ---------------------------------------------------------------------------------------------
print(
    "== part 14: reporting and earnings quality - an aggressive 2025 variant and accrual persistence"
)
b24, b25 = B[2024], B[2025]
rep = dict(
    profit=statements[2025]["is"]["profit"],
    cfo=statements[2025]["cfo"],
    cfi=statements[2025]["cfi"],
    revenue=1080.0,
    receivables=180.0,
    payables=124.0,
    purchases=485.0,
    development=60.0,
    gross=statements[2025]["is"]["gross"],
)
var = dict(rep)
# (a) bill-and-hold shipment recognised before control passes: revenue 30, cost 19.5, tax 25% unpaid at year-end.
var.update(
    revenue=rep["revenue"] + 30, receivables=rep["receivables"] + 30, gross=rep["gross"] + 10.5
)
var["profit"] += 10.5 * (1 - TAX)
# (b) 15 of selling and administrative cost capitalised as development (tax deduction kept: deferred tax).
var["profit"] += 15 * (1 - TAX)
var["development"] += 15
var["cfo"] += 15
var["cfi"] -= 15
# (c) supplier finance: 25 of invoices paid by a bank, Harbour pays the bank in 2026; payables stay in trade payables.
var["payables"] += 25
var["cfo"] += 25


def quality(x, reclass_sfa=False):
    noa_open = bs_view(2024)["eq"] + bs_view(2024)["nfo"]
    noa_close = bs_view(2025)["eq"] + bs_view(2025)["nfo"]
    cfo = x["cfo"] - (
        25 if reclass_sfa else 0
    )  # supplier finance treated as borrowing, not operating cash
    return dict(
        cfo_to_profit=cfo / x["profit"],
        dso=365 * (x["receivables"] + b24["receivables"]) / 2 / x["revenue"],
        dpo=365
        * (x["payables"] - (25 if reclass_sfa else 0) + (-b24["payables"]))
        / 2
        / x["purchases"],
        cf_accruals=(x["profit"] - cfo - x["cfi"]) / ((noa_open + noa_close) / 2),
        accrual_amount=x["profit"] - cfo - x["cfi"],
        dev_growth=x["development"] / b24["development"] - 1,
        gross_margin=x["gross"] / x["revenue"],
    )


q_rep, q_var, q_var_adj = quality(rep), quality(var), quality(var, reclass_sfa=True)
print("  reported: " + ", ".join(f"{k} {v:.4f}" for k, v in q_rep.items()))
print("  variant:  " + ", ".join(f"{k} {v:.4f}" for k, v in q_var.items()))
print(
    "  variant, supplier finance as debt: "
    + ", ".join(f"{k} {v:.4f}" for k, v in q_var_adj.items())
)
ok(
    "variant: profit up 19.125 with CFO up 40 - CFO/profit stays healthy, so it does not flag the problem",
    close(var["profit"] - rep["profit"], 19.125, 1e-9) and q_var["cfo_to_profit"] > 2,
)
ok(
    "variant: DSO, DPO and capitalised-development growth rise",
    q_var["dso"] > q_rep["dso"] + 3
    and q_var["dpo"] > q_rep["dpo"] + 9
    and q_var["dev_growth"] > q_rep["dev_growth"] + 0.25,
)
ok(
    "supplier finance masks accruals: they fall by 5.875; with it reclassified as debt they rise by the 19.125 profit boost",
    close(q_var["accrual_amount"] - q_rep["accrual_amount"], -5.875, 1e-9)
    and close(q_var_adj["accrual_amount"] - q_rep["accrual_amount"], 19.125, 1e-9),
)
# Sloan's balance-sheet accrual measure for Harbour 2025 (current operating accruals less depreciation).
d_ca = (b25["receivables"] + b25["inventory"]) - (b24["receivables"] + b24["inventory"])
d_cl = -(b25["payables"] + b25["accrued_wages"] + b25["restructuring_prov"]) + (
    b24["payables"] + b24["accrued_wages"] + b24["restructuring_prov"]
)
sloan = (d_ca - d_cl - YEARS[2025]["dep"]) / ((bs_view(2025)["ta"] + bs_view(2024)["ta"]) / 2)
print(
    f"  Harbour 2025 Sloan accrual measure (excluding cash, short-term debt and taxes payable): {sloan:.4%}"
)
# Persistence: simulated panel in which the accrual component is less persistent than the cash component.
rng = np.random.default_rng(1996)
N = 40_000
acc = rng.normal(0.0, 0.05, N)
cash = rng.normal(0.10, 0.07, N)
roa_next = 0.02 + 0.60 * acc + 0.85 * cash + rng.normal(0, 0.03, N)
X = np.column_stack([np.ones(N), acc, cash])
coef = np.linalg.lstsq(X, roa_next, rcond=None)[0]
pooled = np.polyfit(acc + cash, roa_next, 1)[0]
ok(
    "simulated persistence: OLS recovers lower accrual than cash coefficient; pooled slope lies between",
    coef[1] < pooled < coef[2] and abs(coef[1] - 0.60) < 0.02 and abs(coef[2] - 0.85) < 0.02,
    f"accrual {coef[1]:.3f}, cash {coef[2]:.3f}, pooled {pooled:.3f}",
)


# ---------------------------------------------------------------------------------------------
print(
    "== part 15: Harbour three-year forecast (2026-2028) with an explicit revolver rule and no balancing plug"
)


def forecast(
    price_infl=(0.03, 0.025, 0.025),
    vol_growth=(0.03, 0.03, 0.03),
    var_cost_infl=(0.04, 0.03, 0.025),
    fixed_infl=0.03,
    payout=0.40,
    acquisition=None,
    rcf_limit=100.0,
    min_cash=40.0,
    capex_rate=0.085,
    lockup=None,
    sga_rate=0.175,
):
    """Return yearly statements. Cash comes from the cash-flow statement; the revolver tops cash up to min_cash
    (repays when cash is above it). Interest on the revolver uses the average balance, solved by iteration.
    """
    o = dict(B[2025])
    o = {
        k: (v if (k in ASSETS and k != "acc_dep") else -v) for k, v in o.items()
    }  # credits and acc_dep positive
    vol, price, vcost, fixed = 100.0, 10.8, 4.8, 151.0
    out = []
    prior_lev = (bs_view(2025)["debt"] - B[2025]["cash"]) / R[2025]["ebitda"]
    for k in range(3):
        y = 2026 + k
        vol *= 1 + vol_growth[k]
        price *= 1 + price_infl[k]
        vcost *= 1 + var_cost_infl[k]
        fixed *= 1 + fixed_infl
        acq_ebitda = acquisition["ebitda"] * (1 + 0.03) ** k if acquisition else 0.0
        organic = vol * price
        acq_rev = acquisition["revenue"] * 1.03**k if acquisition else 0.0
        revenue = organic + acq_rev
        dep = 0.069 * o["ppe_gross"]
        cogs = vol * vcost + fixed + dep
        sga_cash = sga_rate * organic
        sbc = 9.0 * 1.05 ** (k + 1)
        service = 11.0 * 1.03 ** (k + 1)
        rou_dep = 24.0
        research = 0.024 * organic
        dev_amort = o["development"] / 5
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
            - (acquisition["amort"] if acquisition else 0.0)
        )
        lease_int = LEASE_RATE * o["lease_liab"]
        loan_int = LOAN_RATE * o["term_loan"]
        pens_int = DB_RATE * o["db_liab"]
        acq_amort = acquisition["amort"] if acquisition else 0.0
        capex = capex_rate * organic
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
        acq_cash = acquisition["price"] if (acquisition and k == 0) else 0.0
        rev_draw, iters = 0.0, 0
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
            cff_pre = -loan_repay - lease_principal - divs - lease_int * 0
            # Interest paid is inside CFO (profit after finance costs); the revolver closes the gap to min_cash.
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
            goodwill=o["goodwill"] + (acquisition["goodwill"] if (acquisition and k == 0) else 0.0),
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
            # Acquired intangibles and PP&E (net of goodwill) arrive with the purchase price.
            c["ppe_gross"] += acquisition["ppe"]
            c["development"] += acquisition["intangibles"]
        if acquisition:
            c["development"] -= acq_amort
        assets = (
            c["cash"]
            + c["receivables"]
            + c["inventory"]
            + c["ppe_gross"]
            - c["acc_dep"]
            + c["rou"]
            + c["development"]
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
        debt = c["term_loan"] + c["revolver"] + c["lease_liab"]
        out.append(
            dict(
                year=y,
                revenue=revenue,
                cogs=cogs,
                op=op,
                fin=fin,
                pbt=pbt,
                tax=tax,
                profit=profit,
                cfo=cfo,
                cfi=cfi,
                divs=divs,
                draw=rev_draw,
                iters=iters,
                assets=assets,
                liab_eq=liab_eq,
                bs=c,
                ebitda=ebitda,
                debt=debt,
                net_debt=debt - c["cash"],
                gross_margin=(organic - cogs) / organic,
                interest_cover=ebitda / fin,
                rcf=c["revolver"],
                liquidity=c["cash"] + rcf_limit - c["revolver"],
                interest_paid=lease_int + loan_int + rcf_int,
                capex=capex + dev_capex,
                organic=organic,
                vol=vol,
                price=price,
                vcost=vcost,
                lease_principal=lease_principal,
            )
        )
        prior_lev = (debt - c["cash"]) / ebitda
        o = c
    return out


base = forecast()
for f in base:
    ok(
        f"{f['year']}: forecast balance sheet balances without a plug (cash from the CFS, revolver by rule)",
        close(f["assets"], f["liab_eq"], 1e-6),
        f"assets {f['assets']:.4f}, iterations {f['iters']}",
    )
    print(
        f"  {f['year']}: revenue {f['revenue']:.2f} GM {f['gross_margin']:.4f} EBIT {f['op']:.2f} fin {f['fin']:.2f} "
        f"profit {f['profit']:.2f} CFO {f['cfo']:.2f} CFI {f['cfi']:.2f} div {f['divs']:.2f} RCF draw {f['draw']:+.2f} "
        f"RCF {f['rcf']:.2f} cash {f['bs']['cash']:.2f} net debt/EBITDA {f['net_debt'] / f['ebitda']:.3f} "
        f"EBITDA/interest {f['interest_cover']:.2f}"
    )
ok(
    "revenue growth decomposes into volume and price: (1.03)(1.03) - 1 = 6.09% in 2026",
    close(base[0]["revenue"] / 1080.0 - 1, 1.03 * 1.03 - 1, 1e-12),
)


# ---------------------------------------------------------------------------------------------
print("== part 16: competition, cost pass-through, inflation and deflation")
shock = 0.06  # 2026 variable-cost inflation
res = {}
for theta in (
    1.0,
    0.5,
    0.0,
):  # share of the cost shock passed into price (strong buyer power -> low theta)
    f = forecast(price_infl=(theta * shock, 0.025, 0.025), var_cost_infl=(shock, 0.03, 0.025))[0]
    res[theta] = f
    print(
        f"  pass-through {theta:.0%}: price x{1 + theta * shock:.3f}, gross margin {f['gross_margin']:.4f}, EBIT {f['op']:.2f}"
    )
margins = {th: res[th]["op"] / res[th]["revenue"] for th in res}
ok(
    "EBIT and EBIT margin fall monotonically as pass-through weakens (11.56%, 9.57%, 7.45%)",
    res[1.0]["op"] > res[0.5]["op"] > res[0.0]["op"]
    and [round(margins[th] * 100, 2) for th in (1.0, 0.5, 0.0)] == [11.56, 9.57, 7.45],
    ", ".join(f"{th:.0%}: {m:.4%}" for th, m in margins.items()),
)
cm = {th: (res[th]["price"] - res[th]["vcost"]) / res[th]["price"] for th in res}
ok(
    "full pass-through of a uniform per-unit cost rise preserves the contribution margin percentage",
    close(cm[1.0], (10.8 - 4.8) / 10.8, 1e-12),
    f"{cm[1.0]:.4%}",
)
# Real versus nominal growth: nominal = (1 + real)(1 + inflation) - 1; deflating with the wrong index misstates volume.
nominal = base[1]["revenue"] / base[0]["revenue"] - 1
ok(
    "2027 nominal revenue growth = (1 + volume)(1 + price) - 1",
    close(nominal, 1.03 * 1.025 - 1, 1e-12),
    f"{nominal:.4%}",
)
# Deflation with fixed costs: operating leverage turns a 2% price-and-cost decline into a larger EBIT decline.
defl = forecast(
    price_infl=(-0.02, -0.02, -0.02), var_cost_infl=(-0.02, -0.02, -0.02), fixed_infl=0.0
)[0]
flat = forecast(price_infl=(0.0, 0.0, 0.0), var_cost_infl=(0.0, 0.0, 0.0), fixed_infl=0.0)[0]
ok(
    "deflation: EBIT falls proportionally more than revenue when fixed costs do not deflate",
    (defl["op"] / flat["op"] - 1) < (defl["revenue"] / flat["revenue"] - 1),
    f"revenue {defl['revenue'] / flat['revenue'] - 1:+.2%}, EBIT {defl['op'] / flat['op'] - 1:+.2%}",
)


# ---------------------------------------------------------------------------------------------
print("== part 17: forecast horizon, steady state and terminal value consistency")
wacc = 0.08
fcff = [f["cfo"] + f["interest_paid"] * (1 - TAX) - f["capex"] for f in base]
nopat_2028 = base[2]["op"] * (1 - TAX)


def tv_value(nopat_next, g, ronic, r):
    return nopat_next * (1 - g / ronic) / (r - g)


tvs = [tv_value(nopat_2028 * (1 + g), g, wacc, wacc) / (1 + g) for g in (0.0, 0.02, 0.04)]
ok(
    "value-neutral growth: with return on new capital equal to WACC the terminal value does not depend on g",
    max(tvs) - min(tvs) < 1e-9,
    f"TV / NOPAT_2028 = {tvs[0] / nopat_2028:.4f} = 1/WACC",
)
g_ss, ronic_ss = 0.025, 0.12
tv_2028 = tv_value(nopat_2028 * (1 + g_ss), g_ss, ronic_ss, wacc)
v_short = sum(c / (1 + wacc) ** (t + 1) for t, c in enumerate(fcff)) + tv_2028 / (1 + wacc) ** 3
# Explicit extension 2029-2040 with the same steady-state rule, then a terminal value: must give the same value.
ext, nop = [], nopat_2028
for t in range(12):
    nop *= 1 + g_ss
    ext.append(nop * (1 - g_ss / ronic_ss))
tv_2040 = tv_value(nop * (1 + g_ss), g_ss, ronic_ss, wacc)
v_long = (
    sum(c / (1 + wacc) ** (t + 1) for t, c in enumerate(fcff))
    + sum(c / (1 + wacc) ** (t + 4) for t, c in enumerate(ext))
    + tv_2040 / (1 + wacc) ** 15
)
ok(
    "lengthening the explicit horizon with the steady-state rule leaves value unchanged",
    close(v_short, v_long, 1e-6),
    f"enterprise value {v_short:.2f}; terminal share {tv_2028 / (1 + wacc) ** 3 / v_short:.1%}",
)
# A horizon that ends before steady state: capitalising 2028's transitory revenue growth in a Gordon value of FCFF.
g_bad = base[2]["revenue"] / base[1]["revenue"] - 1
naive_tv = fcff[2] * (1 + g_bad) / (wacc - g_bad)
ok(
    "ending the horizon before steady state (Gordon on 2028 FCFF at transitory growth) overstates the terminal value",
    naive_tv > 1.5 * tv_2028,
    f"2028 revenue growth {g_bad:.2%}; naive TV {naive_tv:.2f} vs steady-state TV {tv_2028:.2f}",
)
# Forecast reasonableness: 2026 RNOA implied by the forecast against the 2025 actual (Subramanyam's ROIC check).
f0 = base[0]
noa_open = bs_view(2025)["eq"] + bs_view(2025)["nfo"]
bs26 = f0["bs"]
eq26 = (
    bs26["share_capital"] + bs26["sbp_reserve"] + bs26["remeasurement_reserve"] + bs26["retained"]
)
nfo26 = bs26["term_loan"] + bs26["revolver"] + bs26["lease_liab"] + bs26["db_liab"] - bs26["cash"]
rnoa26 = (f0["profit"] + f0["fin"] * (1 - TAX)) / ((noa_open + eq26 + nfo26) / 2)
ok(
    "2026 forecast RNOA lies between the 2025 actual and the 2024 level (a margin recovery, not a step change)",
    R[2025]["rnoa"] < rnoa26 < R[2024]["rnoa"] + 0.01,
    f"RNOA 2025 {R[2025]['rnoa']:.4%}, 2026 forecast {rnoa26:.4%}; EBIT margin {f0['op'] / f0['revenue']:.4%}",
)
hi_cost = forecast(sga_rate=0.185)[0]
approx = f0["revenue"] * 0.01 * (1 - TAX)
ok(
    "one-point EBIT-margin sensitivity: model profit change matches revenue x 1% x (1 - t) up to revolver interest",
    abs((f0["profit"] - hi_cost["profit"]) - approx) < 0.2,
    f"model {f0['profit'] - hi_cost['profit']:.4f}, approximation {approx:.4f}",
)


# ---------------------------------------------------------------------------------------------
print("== part 18: forecast biases - interval calibration and an outside-view adjustment")
true_sd, believed_sd = 0.10, 0.05
z80 = norm.ppf(0.90)
cover_closed = 2 * norm.cdf(z80 * believed_sd / true_sd) - 1
errors = np.random.default_rng(7).normal(0, true_sd, 200_000)
cover_sim = np.mean(np.abs(errors) < z80 * believed_sd)
ok(
    "overconfident 80% intervals (half the true dispersion) cover about 48% of outcomes",
    abs(cover_sim - cover_closed) < 0.005,
    f"closed form {cover_closed:.4f}, simulated {cover_sim:.4f}",
)
past = np.random.default_rng(8).normal(0, true_sd, 5_000)  # reference class of past forecast errors
lo, hi = np.quantile(past, [0.10, 0.90])
cover_fix = np.mean((errors > lo) & (errors < hi))
ok(
    "intervals set from the reference-class error distribution restore about 80% coverage",
    abs(cover_fix - 0.80) < 0.01,
    f"{cover_fix:.4f}",
)


# ---------------------------------------------------------------------------------------------
print(
    "== part 19: comparability - restating a US GAAP peer (Ridgeline Tools Inc.) and Harbour to a common basis"
)
rg = dict(
    revenue=1200.0,
    cogs=820.0,
    sga=230.0,
    rnd=45.0,
    interest=12.0,
    inventory=150.0,
    lifo_open=40.0,
    lifo_close=48.0,
    lease_liab=120.0,
    rou=115.0,
    lease_cost=30.0,
    debt=200.0,
    cash=50.0,
    equity=600.0,
    total_assets=1100.0,
    dep=40.0,
)
rg["ebit"] = rg["revenue"] - rg["cogs"] - rg["sga"] - rg["rnd"]
rg["ni"] = (rg["ebit"] - rg["interest"]) * (1 - TAX)
adj = dict(rg)
# (1) LIFO to FIFO: inventory + reserve; COGS - change in reserve; DTL + reserve x t; equity + reserve x (1 - t).
adj["cogs"] -= rg["lifo_close"] - rg["lifo_open"]
adj["inventory"] += rg["lifo_close"]
d_assets_1, d_liab_1, d_eq_1 = (
    rg["lifo_close"],
    TAX * rg["lifo_close"],
    (1 - TAX) * rg["lifo_close"],
)
ok(
    "LIFO-to-FIFO adjustment keeps the balance sheet balanced",
    close(d_assets_1, d_liab_1 + d_eq_1, 1e-12),
)
# (2) Operating lease cost (straight-line, in SG&A) replaced by ROU depreciation and lease interest (IFRS 16 basis).
rou_dep_rg = rg["rou"] / 5
lease_int_rg = LEASE_RATE * rg["lease_liab"]
adj["sga"] = rg["sga"] - rg["lease_cost"] + rou_dep_rg
adj["interest"] = rg["interest"] + lease_int_rg
adj["ebit"] = adj["revenue"] - adj["cogs"] - adj["sga"] - adj["rnd"]
adj["ni"] = (adj["ebit"] - adj["interest"]) * (1 - TAX)
ebitda_rep = rg["ebit"] + rg["dep"]
ebitda_adj = adj["ebit"] + rg["dep"] + rou_dep_rg
ok(
    "restatement: EBITDA rises by the operating lease cost plus the increase in the LIFO reserve",
    close(ebitda_adj - ebitda_rep, rg["lease_cost"] + (rg["lifo_close"] - rg["lifo_open"]), 1e-12),
)
# (3) Development: Harbour restated to expensing (the common, conservative basis): 2025 spend 22 vs amortisation 12.
h_op_us_basis = statements[2025]["is"]["op"] - (YEARS[2025]["dev_capex"] - YEARS[2025]["dev_amort"])
h_dev_asset = B[2025]["development"]
peer = dict(
    harbour_reported=dict(
        ebit_margin=statements[2025]["is"]["op"] / 1080, nd_ebitda=R[2025]["net_debt_ebitda"]
    ),
    harbour_common=dict(
        ebit_margin=h_op_us_basis / 1080,
        nd_ebitda=(bs_view(2025)["debt"] - B[2025]["cash"])
        / (
            R[2025]["ebitda"]
            - YEARS[2025]["dev_capex"]
            + YEARS[2025]["dev_amort"]
            - YEARS[2025]["dev_amort"]
        ),
    ),
    ridgeline_reported=dict(
        ebit_margin=rg["ebit"] / rg["revenue"], nd_ebitda=(rg["debt"] - rg["cash"]) / ebitda_rep
    ),
    ridgeline_common=dict(
        ebit_margin=adj["ebit"] / adj["revenue"],
        nd_ebitda=(rg["debt"] + rg["lease_liab"] - rg["cash"]) / ebitda_adj,
    ),
)
for k, v in peer.items():
    print(f"  {k}: EBIT margin {v['ebit_margin']:.4%}, net debt/EBITDA {v['nd_ebitda']:.3f}")
gap_rep = peer["ridgeline_reported"]["ebit_margin"] - peer["harbour_reported"]["ebit_margin"]
gap_common = peer["ridgeline_common"]["ebit_margin"] - peer["harbour_common"]["ebit_margin"]
lev_gap_rep = peer["harbour_reported"]["nd_ebitda"] - peer["ridgeline_reported"]["nd_ebitda"]
lev_gap_common = peer["harbour_common"]["nd_ebitda"] - peer["ridgeline_common"]["nd_ebitda"]
ok(
    "common basis: Ridgeline's margin lead widens from 0.14 to 2.31 points while the leverage gap narrows",
    gap_rep < 0.002 and gap_common > 0.02 and 0 < lev_gap_common < lev_gap_rep,
    f"margin gap {gap_rep:.4%} -> {gap_common:.4%}; leverage gap {lev_gap_rep:.3f}x -> {lev_gap_common:.3f}x",
)


# ---------------------------------------------------------------------------------------------
print("== part 20: effects of accounting changes - IFRS 18, an estimate change and a policy change")
f26 = base[0]
cfo_ias7, cfo_ifrs18 = f26["cfo"], f26["cfo"] + f26["interest_paid"]
ok(
    "IFRS 18: moving interest paid to financing raises CFO by interest paid and leaves the change in cash unchanged",
    close(cfo_ifrs18 - cfo_ias7, f26["interest_paid"], 1e-12),
    f"2026 CFO {cfo_ias7:.2f} -> {cfo_ifrs18:.2f}; CFO/debt {cfo_ias7 / f26['debt']:.3f} -> {cfo_ifrs18 / f26['debt']:.3f}",
)
# A standard change: Harbour 2025 under an operating-lease model (lease payments 28 expensed) against IFRS 16.
op_lease_op = i25["op"] + YEARS[2025]["rou_dep"] - YEARS[2025]["lease_payment"]
op_lease_ebitda = R[2025]["ebitda"] - YEARS[2025]["lease_payment"]
op_lease_nd = bs_view(2025)["debt"] - B[2025]["cash"] - (-B[2025]["lease_liab"])
op_lease_fin = i25["fin"] - LEASE_RATE * 60
ok(
    "IFRS 16 versus an operating-lease model: EBITDA 195 vs 167, net debt/EBITDA 1.63 vs 1.51, EBIT cover 5.76 vs 6.76",
    close(op_lease_ebitda, 167.0, 1e-9)
    and round(op_lease_nd / op_lease_ebitda, 2) == 1.51
    and round(op_lease_op / op_lease_fin, 2) == 6.76,
    f"operating profit {op_lease_op:.2f}, finance costs {op_lease_fin:.2f}",
)
# Management-defined performance measure: adjusted operating profit excluding restructuring (2025).
i25 = statements[2025]["is"]
mpm = i25["op"] + i25["restructuring"]
mpm_tax = TAX * i25["restructuring"]
ok(
    "MPM reconciliation: operating profit + restructuring = adjusted operating profit; tax effect 25%",
    close(mpm, 111.0, 1e-12) and close(mpm_tax, 4.5, 1e-12),
)
# Change in estimate (prospective): useful life of a machine extended from 10 to 14 years after 4 years.
cost_m, resid = 100.0, 0.0
nbv = cost_m - 4 * cost_m / 10
new_dep = (nbv - resid) / (14 - 4)
ok(
    "estimate change: remaining carrying amount spread over the revised remaining life (no restatement)",
    close(new_dep * 10 + 40, cost_m, 1e-12),
    f"depreciation {cost_m / 10:.1f} -> {new_dep:.1f}",
)
# Policy change (retrospective): FIFO to weighted average lowers the 1 Jan 2025 inventory by 4 (tax follows book here).
opening_effect = -4.0 * (1 - TAX)
ok(
    "policy change: opening retained earnings of the earliest period restated by the after-tax cumulative effect",
    close(opening_effect, -3.0, 1e-12),
)


# ---------------------------------------------------------------------------------------------
print(
    "== part 21: integrated analysis - lender decision on Harbour's facility request (1 March 2026)"
)
acq = dict(
    price=60.0, revenue=50.0, ebitda=9.0, amort=2.0, goodwill=30.0, ppe=10.0, intangibles=20.0
)
down = dict(
    price_infl=(0.015, 0.02, 0.025),
    vol_growth=(-0.04, 0.0, 0.02),
    var_cost_infl=(0.06, 0.03, 0.025),
)
policy = dict(
    min_undrawn=10.0, max_lev=2.25, min_cover=6.0
)  # covenant 2.50x net debt/EBITDA with 10% headroom
options = {
    "A: 160 facility, no conditions": dict(acquisition=acq, rcf_limit=160.0),
    "B: 160 facility, dividend lock-up above 1.75x": dict(
        acquisition=acq, rcf_limit=160.0, lockup=1.75
    ),
    "C: keep 100, no acquisition": dict(rcf_limit=100.0, lockup=1.75),
}
verdict = {}
for name, kw in options.items():
    passes = True
    for scen, extra in (("base", {}), ("downside", down)):
        r = forecast(**kw, **extra)
        peak = max(x["rcf"] for x in r)
        undrawn = kw["rcf_limit"] - peak
        lev = max(x["net_debt"] / x["ebitda"] for x in r)
        cover = min(x["interest_cover"] for x in r)
        pens_adj_lev = max(
            (x["net_debt"] + x["bs"]["db_liab"] * (1 - TAX)) / x["ebitda"] for x in r
        )
        good = (
            undrawn >= policy["min_undrawn"]
            and lev <= policy["max_lev"]
            and cover >= policy["min_cover"]
        )
        passes &= good
        print(
            f"  {name} [{scen}]: peak RCF {peak:.2f}, undrawn {undrawn:.2f}, max net debt/EBITDA {lev:.3f} "
            f"(with after-tax pension deficit {pens_adj_lev:.3f}), min EBITDA/interest {cover:.2f}, "
            f"dividends {[round(x['divs'], 2) for x in r]}, balanced {all(abs(x['assets'] - x['liab_eq']) < 1e-6 for x in r)}"
        )
    verdict[name] = passes
ok(
    "only the conditional option B meets the liquidity, leverage and cover tests in both scenarios",
    verdict
    == {
        "A: 160 facility, no conditions": False,
        "B: 160 facility, dividend lock-up above 1.75x": True,
        "C: keep 100, no acquisition": False,
    },
    str(verdict),
)

print(f"\n{n_checks} checks executed")
if fails:
    print("FAILED:", fails)
    sys.exit(1)
print("all checks passed")
