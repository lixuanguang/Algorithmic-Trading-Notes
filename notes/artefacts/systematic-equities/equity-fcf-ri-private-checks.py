"""Equity research, free cash flow, residual income and private-company valuation (2026-10-20).

Worked numbers of the entries written for the equity-research, free-cash-flow, residual-income and private-company
objectives. Harbour Tools plc (hypothetical, EUR millions, valuation date 31 December 2025) is taken from
../financial-statement-analysis/statement-analysis-checks.py, executed with its output suppressed: the 2026-2028
forecast, the valuation conventions (leases as debt, share-based pay a cost, pension deficit a claim) and the
8.49 DCF value. The cost of equity 9.32% and WACC 8.02% follow ../corporate-finance/corporate-finance-checks.py
part 9 (options in market equity). Avon Fittings, Brent Utilities and Fenton Engineering are stand-alone
hypothetical companies; none of the numbers describe a real company.

Independent routes: the Harbour value rebuilt from the forecast against the statement-analysis script; FCFF by the
net-income, EBIT, EBITDA and CFO routes against each other; FCFF and FCFE values of a constant-leverage firm against
each other and against an explicit 3,000-year sum; residual-income values against dividend values with the same
terminal price (finite-horizon identity, contributions included); EVA value against FCFF value; total-beta, build-up
and CAPM costs of equity from their definitions; the Silber regression evaluated directly.

Count convention: one check is one executed ok() call (a call inside a loop counts once per iteration).

Run: uv run python equity-fcf-ri-private-checks.py   (numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import contextlib
import io
import math
import runpy
import sys
from pathlib import Path

# third party library imports
import numpy as np
import scipy
from scipy.optimize import brentq

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


HARBOUR = (
    Path(__file__).resolve().parent.parent
    / "financial-statement-analysis"
    / "statement-analysis-checks.py"
)
with contextlib.redirect_stdout(io.StringIO()):
    H = runpy.run_path(str(HARBOUR))
TAX = H["TAX"]
B25 = H["B"][2025]
SHARES, PRICE, N_OPT = 100.75, 11.0, 5.0
WACC_DCF = 0.08  # the DCF input of the Harbour valuation
bs_call = H["bs_call"]


def option_claim(p):
    return N_OPT * bs_call(p, 8.0, 3.0, 0.03, 0.30, 0.025)


def per_share(equity_pre_options):
    p = equity_pre_options / SHARES
    for _ in range(300):
        new = (equity_pre_options - option_claim(p)) / SHARES
        if abs(new - p) < 1e-12:
            break
        p = new
    return p


KE = 0.03 + 0.93 * (1 + (1 - TAX) * 355.0 / (PRICE * SHARES + option_claim(PRICE))) * 0.055
CLAIMS = 355.0 - B25["db_liab"] * (1 - TAX) - B25["cash"]  # debt + after-tax pension - cash


def harbour_value(fc, wacc=WACC_DCF, g=0.025, ronic=0.12):
    """Value per share from a forecast list, by the conventions of the statement-analysis script part 17."""
    fcff = [H["fcff_valuation"](f) for f in fc]
    nopat_2028 = fc[2]["op"] - TAX * (fc[2]["op"] + fc[2]["sbc"])
    tv = nopat_2028 * (1 + g) * (1 - g / ronic) / (wacc - g)
    ev = sum(c / (1 + wacc) ** (t + 1) for t, c in enumerate(fcff)) + tv / (1 + wacc) ** 3
    return per_share(ev - CLAIMS), ev, fcff


# ---------------------------------------------------------------------------------------------
print("== part 1: a forecast model turned into a value, and its evaluation (Harbour)")
v_base, ev_base, fcff_base = harbour_value(H["base"])
ok(
    "the value rebuilt from the forecast reproduces the statement-analysis script: EV 1,218.45, 8.49 a share",
    close(ev_base, H["v_short"], 1e-9) and close(v_base, H["price_iv"], 1e-9),
)
ok(
    "the forecast balances in every year (assets = liabilities + equity), so no plug drives the cash flows",
    all(close(f["assets"], f["liab_eq"], 1e-6) for f in H["base"]),
)
scen = {
    "downside": dict(vol_growth=(0.0, 0.01, 0.02), price_infl=(0.02, 0.02, 0.02)),
    "upside": dict(vol_growth=(0.05, 0.05, 0.04)),
    "cost overrun": dict(sga_rate=0.185),
    "heavier capex": dict(capex_rate=0.095),
}
vals = {}
for k, kw in scen.items():
    with contextlib.redirect_stdout(io.StringIO()):
        fc = H["forecast"](**kw)
    vals[k] = harbour_value(fc)[0]
print("  scenario values: " + ", ".join(f"{k} {v:.2f}" for k, v in vals.items()))
ok(
    "scenario values bracket the base: downside and cost overrun below 8.49, upside above",
    vals["downside"] < v_base < vals["upside"] and vals["cost overrun"] < v_base,
)
ok(
    "scenario values: downside 4.44, upside 10.42, cost overrun (SG&A 18.5%) 7.16, capex 9.5% of revenue 8.05",
    [round(vals[k], 2) for k in ("downside", "upside", "cost overrun", "heavier capex")]
    == [4.44, 10.42, 7.16, 8.05],
)
ok(
    "terminal-value share of EV is about 0.90: the explicit forecast years carry little of the value",
    0.85 < (H["tv_2028"] / 1.08**3) / ev_base < 0.95,
    f"{H['tv_2028'] / 1.08**3 / ev_base:.4f}",
)
grid = {
    (w, g): harbour_value(H["base"], wacc=w, g=g)[0]
    for w in (0.07, 0.08, 0.09)
    for g in (0.015, 0.025, 0.035)
}
print(
    "  WACC x growth grid: " + ", ".join(f"({w:.0%},{g:.1%}) {v:.2f}" for (w, g), v in grid.items())
)
ok(
    "value falls with WACC and rises with growth at RONIC 12% > WACC",
    grid[(0.07, 0.025)] > grid[(0.08, 0.025)] > grid[(0.09, 0.025)]
    and grid[(0.08, 0.035)] > grid[(0.08, 0.015)],
)

# ---------------------------------------------------------------------------------------------
print("== part 2: research reports - reconciling divergent targets for Harbour")
eps_fwd = H["base"][0]["profit"] / SHARES
target_pe = 18.0 * eps_fwd  # sell-side: peer median forward P/E
eq_ev = 7.8 * 195.0 - CLAIMS
target_ev = per_share(eq_ev)
diff_sources = {
    "multiple vs fundamentals": target_pe - target_ev,
    "EV/EBITDA peers vs DCF": target_ev - v_base,
}
ok(
    "targets: P/E comparables 13.11, EV/EBITDA comparables 11.39, DCF 8.49; the 4.62 gap splits 1.72 + 2.90",
    round(target_pe, 2) == 13.11
    and round(target_ev, 2) == 11.39
    and round(v_base, 2) == 8.49
    and close(sum(diff_sources.values()), target_pe - v_base)
    and [round(v, 2) for v in diff_sources.values()] == [1.72, 2.9],
    ", ".join(f"{k} {v:.2f}" for k, v in diff_sources.items()),
)
w_implied = brentq(lambda w: harbour_value(H["base"], wacc=w)[0] - target_ev, 0.06, 0.08)
ok(
    "the EV/EBITDA target needs a WACC of about 6.95% in the DCF (other inputs held)",
    round(w_implied, 4) == 0.0695,
    f"{w_implied:.5f}",
)

# ---------------------------------------------------------------------------------------------
print("== part 3: FCFF and FCFE from net income, EBIT, EBITDA and CFO (Avon Fittings, one year)")
t = 0.25
rev, cash_costs, dep, interest = 500.0, 380.0, 30.0, 12.0
ebitda = rev - cash_costs
ebit = ebitda - dep
ni = (ebit - interest) * (1 - t)
fc_inv, wc_inv, net_borrow = 45.0, 8.0, 10.0
cfo = ni + dep - wc_inv
fcff_ni = ni + dep + interest * (1 - t) - fc_inv - wc_inv
fcff_ebit = ebit * (1 - t) + dep - fc_inv - wc_inv
fcff_ebitda = ebitda * (1 - t) + dep * t - fc_inv - wc_inv
fcff_cfo = cfo + interest * (1 - t) - fc_inv
fcfe_ni = ni + dep - fc_inv - wc_inv + net_borrow
fcfe_fcff = fcff_ni - interest * (1 - t) + net_borrow
ok(
    "FCFF 44.50 by the net-income, EBIT, EBITDA and CFO routes; FCFE 45.50 from net income or from FCFF",
    all(close(x, 44.5) for x in (fcff_ni, fcff_ebit, fcff_ebitda, fcff_cfo))
    and close(fcfe_ni, 45.5)
    and close(fcfe_fcff, fcfe_ni),
    f"NI {ni:.2f}, EBIT {ebit:.2f}, EBITDA {ebitda:.2f}, CFO {cfo:.2f}",
)
ok(
    "IFRS presentation: if interest paid sits in financing, CFO is 9 higher and the interest term is dropped",
    close((cfo + interest) - interest * t - fc_inv, fcff_cfo),
)
# Harbour 2026 forecast: CFO route (with valuation adjustments) against the NOPAT route.
f26 = H["base"][0]
ok(
    "Harbour 2026 valuation FCFF 31.93: CFO route equals the NOPAT route",
    close(H["fcff_valuation"](f26), H["fcff_nopat_route"](f26), 1e-9)
    and round(H["fcff_valuation"](f26), 2) == 31.93,
)

# ---------------------------------------------------------------------------------------------
print("== part 4: forecasting FCFF and FCFE - payouts, issues and leverage")
base_fcff, base_fcfe = fcff_ni, fcfe_ni
fcfe_more_debt = ni + dep - fc_inv - wc_inv + (net_borrow + 20.0) - 20.0 * 0.06 * (1 - t)
ok(
    "a dividend or buyback changes neither FCFF nor FCFE; borrowing 20 more at 6% raises FCFE by 20 - 0.90 "
    "in the year and leaves FCFF unchanged",
    close(fcfe_more_debt - base_fcfe, 20 - 0.9),
)
for f in H["base"]:
    o, c = f["open"], f["bs"]
    fcfe_stat = f["cfo"] - f["capex"] - f["lease_principal"] - f["loan_repay"] + f["draw"]
    ok(
        f"Harbour {f['year']}: FCFE {fcfe_stat:.2f} = dividends {f['divs']:.2f} + change in cash "
        f"{c['cash'] - o['cash']:.2f}; net borrowing {f['draw'] - f['loan_repay'] - f['lease_principal'] + f['lease_new']:.2f}",
        close(fcfe_stat, f["divs"] + c["cash"] - o["cash"], 1e-9),
    )
# Target-ratio forecasting shortcut (Damodaran): FCFE = NI - (1 - DR)(FCInv - Dep + WCInv).
dr = 0.30
ok(
    "with 30% of net reinvestment debt-financed, FCFE = NI - 0.70 x (45 - 30 + 8) = 58.50 - 16.10 = 42.40",
    close(ni - (1 - dr) * (fc_inv - dep + wc_inv), 42.4) and close(ni, 58.5),
)

# ---------------------------------------------------------------------------------------------
print(
    "== part 5: single- and multistage FCFF and FCFE valuation (Brent Utilities, constant leverage)"
)
g = 0.03
wacc_b, kd_b, t_b, dv = 0.07, 0.05, 0.25, 0.40
fcff1 = 60.0
V = fcff1 / (wacc_b - g)
D = dv * V
E = V - D
ke_b = (wacc_b * V - kd_b * (1 - t_b) * D) / E
fcfe1 = fcff1 - kd_b * (1 - t_b) * D + g * D
ok(
    "FCFF 60 at WACC 7%, g 3%: firm 1,500, debt 600, equity 900; ke 9.17%; FCFE 60 - 22.5 + 18 = 55.5 "
    "discounted at ke gives the same 900",
    close(V, 1500)
    and close(E, 900)
    and round(ke_b, 4) == 0.0917
    and close(fcfe1, 55.5)
    and close(fcfe1 / (ke_b - g), E, 1e-9),
)
long_e = sum(fcfe1 * (1 + g) ** (k - 1) / (1 + ke_b) ** k for k in range(1, 3000))
ok("an explicit 3,000-year FCFE sum agrees", close(long_e, E, 1e-6))
fcfe_wrong = fcfe1 / (wacc_b - g)
ok(
    "discounting FCFE at the WACC overstates equity: 1,387.50 against 900",
    close(fcfe_wrong, 1387.5),
)
# Two-stage FCFE: high growth 10% for five years from FCFE0 = 2.00 a share, then 3%; ke 10% then 9%.
fcfe0, gh, gn, ke_h, ke_s, n = 2.00, 0.12, 0.03, 0.10, 0.09, 5
cf = [fcfe0 * (1 + gh) ** k for k in range(1, n + 1)]
tv = cf[-1] * (1 + gn) / (ke_s - gn)
v2 = sum(c / (1 + ke_h) ** k for k, c in enumerate(cf, 1)) + tv / (1 + ke_h) ** n
ok(
    "two-stage FCFE growing 12%: 2.24 ... 3.52; TV_5 = 3.52 x 1.03 / 6% = 60.51; value at ke 10% then 9%: 48.13",
    round(cf[0], 2) == 2.24
    and round(cf[-1], 2) == 3.52
    and round(tv, 2) == 60.51
    and round(v2, 2) == 48.13,
)
# Three-stage FCFE: 12% for five years, growth falling linearly to 3% over years 6-8 while ke steps
# from 10% to 9%; discounting at the cumulated cost of equity (Damodaran pp. 374-375 structure).
g_path = [0.12] * 5 + [0.09, 0.06, 0.03]
ke_path = [0.10] * 5 + [0.0967, 0.0933, 0.09]
cf3, disc, x3 = [], 1.0, fcfe0
for g_, k_ in zip(g_path, ke_path):
    x3 *= 1 + g_
    disc *= 1 + k_
    cf3.append(x3 / disc)
tv3 = x3 * 1.03 / (0.09 - 0.03)
v3 = sum(cf3) + tv3 / disc
ok(
    "three-stage FCFE: growth 12% for five years, then 9%, 6%, 3% while ke steps to 9%; terminal value at year 8 "
    "of 72.01; value 51.05 against 48.13 two-stage - the transition years add 2.92",
    round(tv3, 2) == 72.01 and round(v3, 2) == 51.05 and round(v3 - v2, 2) == 2.92,
    f"TV {tv3:.4f}, value {v3:.4f}",
)
# A stable-period reinvestment check: g = 3% with stable ROE 12% needs 25% equity reinvestment.
ni5 = 4.0
ok(
    "stable equity reinvestment rate g/ROE = 3%/12% = 25%: FCFE_6 = 4.00 x 1.03 x 0.75 = 3.09",
    close(ni5 * 1.03 * (1 - 0.03 / 0.12), 3.09),
)
sens = {
    (k_, g_): sum(c / (1 + ke_h) ** k for k, c in enumerate(cf, 1))
    + cf[-1] * (1 + g_) / (k_ - g_) / (1 + ke_h) ** n
    for k_ in (0.08, 0.09, 0.10)
    for g_ in (0.02, 0.03, 0.04)
}
print(
    "  terminal sensitivity: "
    + ", ".join(f"(ke {k_:.0%}, g {g_:.0%}) {v:.2f}" for (k_, g_), v in sens.items())
)
ok(
    "the stable cost of equity (8-10%) and growth (2-4%) move the value from 38.46 to 67.46",
    round(min(sens.values()), 2) == 38.46 and round(max(sens.values()), 2) == 67.46,
)

# ---------------------------------------------------------------------------------------------
print("== part 6: cash-flow proxies - dividends, net income and EBITDA against FCFE and FCFF")
f26 = H["base"][0]
nopat26 = f26["op"] - TAX * (f26["op"] + f26["sbc"])
ok(
    "Harbour 2026: EBITDA 227.28, NOPAT 87.28, net income 73.40, valuation FCFF 31.93, FCFE 31.82, dividends 29.36",
    round(f26["ebitda"], 2) == 227.28
    and round(nopat26, 2) == 87.28
    and round(f26["profit"], 2) == 73.4
    and round(fcff_base[0], 2) == 31.93
    and round(f26["divs"] + f26["bs"]["cash"] - f26["open"]["cash"], 2) == 31.82
    and round(f26["divs"], 2) == 29.36,
)
ebitda_cap = f26["ebitda"] / (WACC_DCF - 0.025)
ok(
    "capitalising EBITDA as if it were FCFF (227.28 / 5.5%) gives 4,132, against a DCF EV of 1,218",
    round(ebitda_cap) == 4132 and ebitda_cap > 3 * ev_base,
)
# Damodaran's Table 15.1 relations, checked on Avon Fittings.
ok(
    "EBIT(1 - t) = FCFF + capex - depreciation + change in WC; EBITDA = FCFF + EBIT x t + capex + change in WC",
    close(ebit * (1 - t), fcff_ebit + fc_inv - dep + wc_inv)
    and close(ebitda, fcff_ebit + ebit * t + fc_inv + wc_inv),
)

# ---------------------------------------------------------------------------------------------
print("== part 7: residual income, EVA and MVA")
bv0, roe, kek, payout = 20.0, 0.12, 0.09, 0.5
ri1 = (roe - kek) * bv0
ok(
    "RI = (ROE - ke) x B0 = (12% - 9%) x 20 = 0.60; equivalently NI 2.40 less a 1.80 equity charge",
    close(ri1, 0.6) and close(roe * bv0 - kek * bv0, ri1),
)
# Harbour EVA: NOPAT less WACC x opening invested capital (book equity + debt + after-tax pension - cash).
bsv = H["bs_view"]


def invested_capital(y):
    b = H["B"][y]
    return (
        bsv(y)["eq"]
        + (-(b["term_loan"] + b["revolver"] + b["lease_liab"]))
        - b["db_liab"] * (1 - TAX)
        - b["cash"]
    )


ic24, ic25 = invested_capital(2024), invested_capital(2025)
op25 = H["statements"][2025]["is"]["op"]
nopat25 = op25 - TAX * (op25 + H["YEARS"][2025]["sbc"])
wacc_mkt = 0.0802
eva25 = nopat25 - wacc_mkt * ic24
ev_mkt = PRICE * SHARES + option_claim(PRICE) + CLAIMS
mva = ev_mkt - ic25
print(
    f"  invested capital 2024 {ic24:.2f}, 2025 {ic25:.2f}; NOPAT 2025 {nopat25:.2f}; EVA {eva25:.2f}; MVA {mva:.2f}"
)
ok(
    "Harbour 2025: NOPAT 67.50 on opening capital 945.00 earns 7.14% < WACC 8.02%: EVA -8.29; market EV 1,479.77 "
    "less invested capital 1,000.96 is MVA 478.81",
    round(nopat25, 2) == 67.5
    and round(ic24, 2) == 945.0
    and round(nopat25 / ic24, 4) == 0.0714
    and round(eva25, 2) == -8.29
    and round(ic25, 2) == 1000.96
    and round(mva, 2) == 478.81,
)
add_back = 18.0 * (1 - TAX)
ok(
    "adding back the 18 restructuring charge after tax lifts NOPAT to 81.00 and EVA to 5.21",
    round(nopat25 + add_back, 2) == 81.0 and round(nopat25 + add_back - wacc_mkt * ic24, 2) == 5.21,
)
# EVA value = capital + PV(EVA) equals FCFF value (Damodaran Illustration 32.1 structure, own numbers).
ic0, roc, wacc_e, inv = 200.0, 0.14, 0.09, 20.0
v_eva = (
    ic0
    + (roc - wacc_e) * ic0 / wacc_e
    + sum((roc - wacc_e) * inv / wacc_e / (1 + wacc_e) ** k for k in range(4))
)
nop = [
    roc * (ic0 + inv * k) for k in range(1, 5)
]  # NOPAT years 1-4 (investment at start of each year)
fcff_e = [-inv] + [nop[k] - (inv if k < 3 else 0.0) for k in range(4)]
v_dcf = (
    fcff_e[0]
    + sum(c / (1 + wacc_e) ** (k + 1) for k, c in enumerate(fcff_e[1:]))
    + nop[-1] / wacc_e / (1 + wacc_e) ** 4
)
ok(
    "capital 200 at ROC 14% and WACC 9% plus four 20 investments at 14%: EVA value 350.35 = FCFF value",
    round(v_eva, 2) == 350.35 and close(v_eva, v_dcf, 1e-9),
    f"FCFF route {v_dcf:.4f}",
)

# ---------------------------------------------------------------------------------------------
print("== part 8: single-stage, multistage and continuing residual income")
g_c = roe * (1 - payout)
v_ri = bv0 + ri1 / (kek - g_c)
ok(
    "single stage: 20 + 0.60/(9% - 6%) = 40.00 = DDM 1.20/3%",
    close(v_ri, 40.0) and close(roe * bv0 * payout / (kek - g_c), 40.0),
)
# Multistage with fading RI: RI for 3 years at ROE 15%, then RI persists at omega = 0.6.
bv, pv, ri_path = 20.0, 0.0, []
roes = [0.15, 0.14, 0.13]
for k, r_ in enumerate(roes, 1):
    ri = (r_ - kek) * bv
    ri_path.append(ri)
    pv += ri / (1 + kek) ** k
    bv += r_ * bv * (1 - payout)
omega = 0.6
ri4 = ri_path[-1] * omega
tv_ri = ri4 / (1 + kek - omega)
v_ms = 20.0 + pv + tv_ri / (1 + kek) ** 3
explicit = 20.0 + pv + sum(ri_path[-1] * omega**j / (1 + kek) ** (3 + j) for j in range(1, 4000))
ok(
    "RI 1.20, 1.08, 0.92 over three years, then persisting at omega 0.6: TV_3 1.13, value 23.59; an explicit sum agrees",
    [round(x, 2) for x in ri_path] == [1.2, 1.08, 0.92]
    and round(tv_ri, 2) == 1.13
    and round(v_ms, 2) == 23.59
    and close(v_ms, explicit, 1e-9),
    f"TV {tv_ri:.4f}, value {v_ms:.4f}",
)
v_om0, v_om1 = 20.0 + pv, 20.0 + pv + ri_path[-1] / kek / (1 + kek) ** 3
ok(
    "omega bounds: 0 gives 22.72 (RI stops), 1 gives 30.61 (RI held forever)",
    round(v_om0, 2) == 22.72 and round(v_om1, 2) == 30.61,
)

# ---------------------------------------------------------------------------------------------
print("== part 9: residual income against dividends for Harbour, with the dirty-surplus credit")
fc = H["base"]


def book_eq(bs):
    return bs["share_capital"] + bs["sbp_reserve"] + bs["remeasurement_reserve"] + bs["retained"]


bvs = [H["bs_view"](2025)["eq"]] + [book_eq(f["bs"]) for f in fc]
ni_h = [f["profit"] for f in fc]
div_h = [f["divs"] for f in fc]
contrib = [bvs[k + 1] - bvs[k] - ni_h[k] + div_h[k] for k in range(3)]
ok(
    "forecast book equity grows by profit less dividends plus the equity credit for share-based pay "
    "(9.45, 9.92, 10.42): the dirty-surplus item",
    all(close(c, f["sbc"], 1e-6) for c, f in zip(contrib, fc)),
    ", ".join(f"{c:.4f}" for c in contrib),
)
roe_ss, g_ss = 0.1079, 0.025
pb_t = (roe_ss - g_ss) / (KE - g_ss)
p_t = pb_t * bvs[-1]
v_ddm = sum(d / (1 + KE) ** k for k, d in enumerate(div_h, 1)) + p_t / (1 + KE) ** 3
ri_h = [ni_h[k] - KE * bvs[k] for k in range(3)]
v_ri_naive = (
    bvs[0] + sum(r / (1 + KE) ** k for k, r in enumerate(ri_h, 1)) + (p_t - bvs[-1]) / (1 + KE) ** 3
)
pv_credits = sum(c / (1 + KE) ** k for k, c in enumerate(contrib, 1))
ok(
    "with the same terminal price (P/B on 2028 book), RI on reported book equals the dividend value less the PV "
    "of the equity credits: the finite-horizon identity with a dirty-surplus term",
    close(v_ri_naive, v_ddm - pv_credits, 1e-9)
    and round(v_ddm, 2) == 834.16
    and round(v_ri_naive, 2) == 809.24
    and round(pv_credits, 2) == 24.92
    and round(pb_t, 4) == 1.2148
    and [round(v / SHARES, 2) for v in (v_ddm, v_ri_naive)] == [8.28, 8.03],
    f"DDM {v_ddm:.4f} ({v_ddm / SHARES:.4f} a share), RI {v_ri_naive:.4f} ({v_ri_naive / SHARES:.4f}), PV credits {pv_credits:.4f}, P_T {p_t:.4f}, P/B {pb_t:.4f}",
)
ok(
    "Harbour RI: 2026 ROE on opening book 11.34% against ke 9.32%; RI 13.04, 10.12, 9.86",
    round(ni_h[0] / bvs[0], 4) == 0.1134 and [round(r, 2) for r in ri_h] == [13.04, 10.12, 9.86],
    ", ".join(f"RI {r:.2f}" for r in ri_h),
)
pb_mkt = PRICE * SHARES / bvs[0]
g_implied = KE - (roe_ss - KE) / (pb_mkt - 1)
roe_implied = KE + (pb_mkt - 1) * (KE - g_ss)
ok(
    "implied growth from the market P/B: at P/B 1.71, ke 9.32% and a sustained ROE of 10.79%, residual income "
    "must grow at 7.27% a year; at 2.5% growth the price needs a sustained ROE of 14.18%",
    round(pb_mkt, 2) == 1.71 and round(g_implied, 4) == 0.0727 and round(roe_implied, 4) == 0.1418,
    f"P/B {pb_mkt:.4f}, g {g_implied:.4f}",
)
share_book = bvs[0] / v_ri_naive
share_tv_ri = (p_t - bvs[-1]) / (1 + KE) ** 3 / v_ri_naive
share_tv_ddm = p_t / (1 + KE) ** 3 / v_ddm
ok(
    "value recognition: in the RI value, current book is 80% and the terminal premium over book 17%; in the "
    "dividend value the terminal price is 91%",
    round(share_book, 2) == 0.80
    and round(share_tv_ri, 2) == 0.17
    and round(share_tv_ddm, 2) == 0.91,
    f"book {share_book:.3f}, RI terminal {share_tv_ri:.3f}, DDM terminal {share_tv_ddm:.3f}",
)

# ---------------------------------------------------------------------------------------------
print("== part 10: private company - normalising Fenton Engineering's earnings")
rep = dict(revenue=40.0, ebit=5.6)
adj = dict(owner_salary=-0.30, rent_to_owner=-0.30, litigation=+0.60, personal_expenses=+0.15)
ebit_n = rep["ebit"] + sum(adj.values())
ok(
    "normalised EBIT 5.6 - 0.30 - 0.30 + 0.60 + 0.15 = 5.75 (margin 14.4%)",
    close(ebit_n, 5.75) and round(ebit_n / 40, 3) == 0.144,
)
dep_f, capex_f, dwc_f = 1.2, 1.6, 0.4
nopat_f = ebit_n * (1 - TAX)
fcff_f = nopat_f + dep_f - capex_f - dwc_f
ok(
    "normalised NOPAT 4.3125; FCFF 4.3125 + 1.2 - 1.6 - 0.4 = 3.5125",
    close(nopat_f, 4.3125) and close(fcff_f, 3.5125),
)

# ---------------------------------------------------------------------------------------------
print(
    "== part 11: private company - required return by CAPM, expanded CAPM, build-up and total beta"
)
rf, erp, bu, de_ind, kd_pre = 0.03, 0.055, 0.95, 0.25, 0.065
bl = bu * (1 + (1 - TAX) * de_ind)
ke_capm = rf + bl * erp
ke_exp = ke_capm + 0.02 + 0.015
ke_build = rf + erp + 0.02 + 0.005 + 0.015
total_beta = bl / 0.40
ke_total = rf + total_beta * erp
wd = de_ind / (1 + de_ind)
wacc_pub = (1 - wd) * ke_capm + wd * kd_pre * (1 - TAX)
wacc_priv = (1 - wd) * ke_total + wd * (kd_pre + 0.01) * (1 - TAX)
ok(
    "levered beta 1.128; CAPM 9.20%, expanded CAPM (size 2%, specific 1.5%) 12.70%, build-up 12.50%, "
    "total beta 2.82 -> 18.51%",
    round(bl, 3) == 1.128
    and round(ke_capm, 4) == 0.092
    and round(ke_exp, 4) == 0.127
    and round(ke_build, 4) == 0.125
    and round(total_beta, 2) == 2.82
    and round(ke_total, 4) == 0.1851,
)
ok(
    "WACC at 20% debt: 8.34% for a diversified buyer, 15.93% for an undiversified owner (spread +1 point)",
    round(wacc_pub, 4) == 0.0834 and round(wacc_priv, 4) == 0.1593,
)

# ---------------------------------------------------------------------------------------------
print(
    "== part 12: private company - income, market and asset approaches; control and marketability"
)
g_f, ronic_f = 0.025, 0.12
fcff_ss = nopat_f * (1 + g_f) * (1 - g_f / ronic_f)
ev_pub = fcff_ss / (wacc_pub - g_f)
ev_priv = fcff_ss / (wacc_priv - g_f)
net_debt_f = 6.0
ok(
    "income approach (steady state, RONIC 12%): EV 59.93 to a diversified buyer, 26.05 to an undiversified owner",
    round(ev_pub, 2) == 59.93 and round(ev_priv, 2) == 26.05,
)
ebitda_n = ebit_n + dep_f
ev_gpc = 7.5 * ebitda_n
ev_tx = 6.8 * ebitda_n
ok(
    "market approach: guideline public companies 7.5x normalised EBITDA 6.95 = 52.13 (marketable minority basis); "
    "precedent transactions 6.8x = 47.26 (control basis)",
    round(ev_gpc, 3) == 52.125 and round(ev_tx, 2) == 47.26,
)
nav = 38.0 - 6.0 - 9.5
ok(
    "asset approach: assets at fair value 38.0 less net debt 6.0 and other liabilities 9.5: equity 22.5",
    close(nav, 22.5),
)
eq_control = ev_pub - net_debt_f
dloc = 1 - 1 / 1.25
dlom_silber_10 = 1 - math.exp(4.33 + 0.036 * math.log(10) - 0.142 * math.log(100) + 0.174) / 100
dlom_silber_40 = 1 - math.exp(4.33 + 0.036 * math.log(40) - 0.142 * math.log(100) + 0.174) / 100
dlom = 0.25 + (dlom_silber_40 - dlom_silber_10)
stake = 0.30 * eq_control * (1 - dloc) * (1 - dlom)
ok(
    "Silber regression: discount 48.94% at revenue 10m and 46.33% at 40m, so a 25% benchmark becomes 22.39%",
    round(dlom_silber_10, 4) == 0.4894
    and round(dlom_silber_40, 4) == 0.4633
    and round(dlom, 4) == 0.2239,
)
ok(
    "30% minority stake: 30% of control equity 53.93, less DLOC 20% (control premium 25%) and DLOM 22.39%: 10.05",
    round(eq_control, 2) == 53.93 and close(dloc, 0.2) and round(stake, 2) == 10.05,
    f"combined discount {1 - (1 - dloc) * (1 - dlom):.4f}",
)
ok(
    "the discounts multiply: 1 - 0.80 x 0.7761 = 37.91%, not 20% + 22.39% = 42.39%",
    round(1 - (1 - dloc) * (1 - dlom), 4) == 0.3791,
)

print(f"\n{n_checks} checks executed")
if fails:
    print("FAILED:", fails)
    sys.exit(1)
print("all checks passed")
