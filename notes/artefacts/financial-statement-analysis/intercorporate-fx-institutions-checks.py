"""Intercorporate investments, foreign-currency reporting and financial institutions (2026-10-20).

Worked numbers of the entries for the intercorporate-investment, foreign-currency and financial-institution
objectives. Penrose Group (an IFRS reporter in EUR millions), its investee Quay Ltd, its US subsidiary Penrose Inc.,
its hyperinflationary subsidiary Penrose Andina, the multinational Larch Brands, Tamar Bank and Wren Insurance are
hypothetical, as are Linden Life and Rowan Life (part 10, added 2026-10-20 after the audit); none of their numbers
describe a real company. Rule references: IAS 28 paras. 5-6, 10, 32, 38; IFRS 10
paras. 7, 22, B86, B94; IFRS 12 App. A, B21; FAS 167 summary, paras. 14A-14G and Example 1 (C2-C12); IFRS 11 paras. 15-16, 20, 24; IFRS 3 paras. 19, 32; IFRS 9 paras. 4.1.4, 5.7.5; IAS 21
paras. 21, 23, 28, 39-42, 48; IAS 29 paras. 3, 11-12, 27-28; FAS 52 paras. 5-16; FAS 141R para. 20; ASU 2016-01
(summary); Basel Framework RBC20.1, RBC30.2, LEV20.7, LCR20.5, NSF20.2; Hull (2023) pp. 28-30 and 59-60;
Subramanyam and Wild (2009) pp. 304-306 (BritCo).

Independent routes: equity-method carrying amount as a running balance against the investor's share of the
investee's fair-value net assets plus goodwill; consolidated balance sheet built line by line against the
one-line (equity-method) parent equity; the cumulative translation adjustment as a plug against its direct
decomposition by rate changes; the temporal remeasurement result as a plug against the net monetary position;
constant-currency growth from local-currency series against the reported figure less the translation effect;
bank and insurer ratios from their definitions against the published examples they reproduce.

Count convention: one check is one executed ok() call (a call inside a loop counts once per iteration).

Run: uv run python intercorporate-fx-institutions-checks.py   (numpy). Exits 1 on failure.
"""

# standard library imports
import sys

# third party library imports
import numpy as np

print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}")
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
print("== part 1: classifying an intercorporate investment (IFRS, with the US GAAP contrast)")


def classify(
    stake,
    influence_evidence=False,
    power=False,
    variable_returns=False,
    principal=True,
    joint=False,
    rights="net assets",
):
    """IFRS 10 control first; then IFRS 11 joint control; then IAS 28 significant influence; else IFRS 9.

    Corrected 2026-10-20 (audit): control is derived from its three elements (IFRS 10 para. 7) instead of being
    passed in as a conclusion. power is True, False or None (the facts about who directs the relevant activities
    are not given); designing a vehicle or bearing its losses is not an input to power (paras. B51, B54).
    """
    if power is None and variable_returns:
        return (
            "not determinable: identify who holds substantive rights over the relevant activities"
        )
    if power and variable_returns and principal:
        return "subsidiary: consolidate (IFRS 10)"
    if joint:
        return (
            "joint venture: equity method (IFRS 11.24)"
            if rights == "net assets"
            else "joint operation: own share of assets, liabilities, revenue and expenses (IFRS 11.20)"
        )
    if stake >= 0.20 or influence_evidence:
        return "associate: equity method (IAS 28.16)"
    if variable_returns and stake == 0.0:
        return "interest in an unconsolidated structured entity: IFRS 9 measurement, IFRS 12 disclosure"
    return "financial asset: FVPL, or FVOCI if elected for equity not held for trading (IFRS 9)"


# (stake, influence, power, variable returns, joint, rights, expected)
cases = [
    (0.10, False, False, True, False, "net assets", "financial asset"),
    (0.15, True, False, True, False, "net assets", "associate"),
    (0.30, False, False, True, False, "net assets", "associate"),
    (0.50, False, False, True, True, "net assets", "joint venture"),
    (0.50, False, False, True, True, "assets and obligations", "joint operation"),
    (0.45, False, True, True, False, "net assets", "subsidiary"),
    # Structured leasing vehicle, 0% of the (administrative) votes, Penrose holds the first-loss note:
    (
        0.0,
        False,
        True,
        True,
        False,
        "net assets",
        "subsidiary",
    ),  # Penrose decides remarketing and defaults
    (
        0.0,
        False,
        False,
        True,
        False,
        "net assets",
        "interest in an unconsolidated",
    ),  # servicer decides
    (
        0.0,
        False,
        None,
        True,
        False,
        "net assets",
        "not determinable",
    ),  # designed it, bears losses, no more
]
for st, inf, pw, vr, jt, rt, expect in cases:
    ok(
        f"stake {st:.0%}, influence {inf}, power {pw}, variable returns {vr}, joint {jt} ({rt}) -> {expect}",
        classify(st, inf, pw, vr, True, jt, rt).startswith(expect),
    )
# FAS 167 Example 1 (paras. C2-C12), the US contrast: bondholders absorb losses after the $6 equity but have no rights
# to direct the defaulted loans; the special servicer, which directs them and holds the equity, is the primary
# beneficiary; the primary servicer's administrative activities are not the significant ones.
holders = {
    "special servicer (equity)": dict(power=True, loss_absorption=True),
    "bondholders": dict(power=False, loss_absorption=True),
    "primary servicer (fixed fee)": dict(power=False, loss_absorption=False),
}
pb = [k for k, v in holders.items() if v["power"] and v["loss_absorption"]]
ok(
    "FAS 167 Example 1: only the special servicer has both power and significant loss exposure; the bondholders "
    "have variable returns without power",
    pb == ["special servicer (equity)"]
    and holders["bondholders"]["loss_absorption"]
    and not holders["bondholders"]["power"],
)

# ---------------------------------------------------------------------------------------------
print("== part 2: the equity method - Penrose buys 30% of Quay on 1 January 2026")
quay_bv0, uplift, life = 300.0, 40.0, 10  # PP&E fair value 40 above book, ten-year remaining life
quay_ni, quay_div = 40.0, 10.0
cost30 = 108.0
goodwill30 = cost30 - 0.30 * (quay_bv0 + uplift)
share_ni = 0.30 * quay_ni - 0.30 * uplift / life
carrying = cost30 + share_ni - 0.30 * quay_div
fv_net_assets_end = quay_bv0 + uplift + quay_ni - quay_div - uplift / life
ok(
    "cost 108 = 30% of fair-value net assets 340 (102) + goodwill 6; share of profit 12 - 1.2 extra depreciation "
    "= 10.8; dividends 3 reduce the investment: carrying amount 115.8",
    close(goodwill30, 6.0) and close(share_ni, 10.8) and close(carrying, 115.8),
)
ok(
    "independent route: 30% x end fair-value net assets 366 + goodwill 6 = 115.8",
    close(0.30 * fv_net_assets_end + goodwill30, carrying),
)
# A 10% stake: IFRS 9 FVPL against the FVOCI election, and US GAAP (ASU 2016-01) FV-NI.
cost10, fv10_end, div10 = 36.0, 39.0, 1.0
ok(
    "10% stake: FVPL puts the 3 fair-value gain and 1 dividend in profit (4); FVOCI puts 3 in OCI, never "
    "recycled, and 1 in profit; US GAAP has no OCI option for equity securities",
    close((fv10_end - cost10) + div10, 4.0) and close(div10, 1.0),
)

# ---------------------------------------------------------------------------------------------
print(
    "== part 3: consolidation of a 70% stake, partial and full goodwill, against the one-line method"
)
cost70, nci_fv = 260.0, 105.0
fvna = quay_bv0 + uplift
gw_partial = cost70 + 0.30 * fvna - fvna
gw_full = cost70 + nci_fv - fvna
ok(
    "IFRS 3.19/32: proportionate NCI 102 gives goodwill 22; NCI at fair value 105 gives goodwill 25 "
    "(FAS 141R.20 requires fair value)",
    close(gw_partial, 22.0) and close(gw_full, 25.0),
)
# Penrose stand-alone 2026: revenue 1,000, profit before investee income 80, dividends paid 30.
pen = dict(revenue=1000.0, ni=80.0, div=30.0, assets0=1200.0, liab=700.0)
quay = dict(
    revenue=400.0, assets_book_end=530.0, liab_end=200.0
)  # book: 500 + 40 profit - 10 dividends + 10 other
nci_share_ni = 0.30 * (quay_ni - uplift / life)
parent_ni_cons = pen["ni"] + quay_ni - uplift / life - nci_share_ni
parent_ni_equity = pen["ni"] + 0.70 * (quay_ni - uplift / life)
ok(
    "profit attributable to Penrose 105.2 whether Quay is consolidated (80 + 40 - 4 - NCI 10.8) or carried in one "
    "line (80 + 70% x 36)",
    close(parent_ni_cons, parent_ni_equity) and close(parent_ni_cons, 105.2),
)
eq_parent_end = 500.0 + parent_ni_equity - pen["div"]
inv70_end = cost70 + 0.70 * (quay_ni - uplift / life) - 0.70 * quay_div
pen_own_assets_end = pen["assets0"] - cost70 + pen["ni"] - pen["div"] + 0.70 * quay_div
assets_equity_method = pen_own_assets_end + inv70_end
nci_end_partial = 0.30 * fvna + nci_share_ni - 0.30 * quay_div
quay_fv_assets_end = quay["assets_book_end"] + uplift - uplift / life
assets_cons = (
    pen_own_assets_end + quay_fv_assets_end + gw_partial
)  # the 7 dividend received is group cash
liab_cons = pen["liab"] + quay["liab_end"]
ok(
    "consolidated balance sheet balances: assets = liabilities + parent equity + NCI",
    close(assets_cons, liab_cons + eq_parent_end + nci_end_partial, 1e-9),
    f"assets {assets_cons:.2f}, liabilities {liab_cons:.2f}, parent equity {eq_parent_end:.2f}, NCI {nci_end_partial:.2f}",
)
ok(
    "the one-line method gives the same parent equity 575.2 with assets of 1,275.2 against 1,585.0 consolidated",
    close(assets_equity_method, pen["liab"] + eq_parent_end)
    and close(eq_parent_end, 575.2)
    and close(assets_equity_method, 1275.2)
    and round(assets_cons, 1) == 1585.0,
)
methods = {
    "equity method": dict(
        rev=pen["revenue"],
        ni=parent_ni_equity,
        assets=assets_equity_method,
        liab=pen["liab"],
        eq=eq_parent_end,
    ),
    "proportionate (70%)": dict(
        rev=pen["revenue"] + 0.70 * quay["revenue"],
        ni=parent_ni_equity,
        assets=pen_own_assets_end + 0.70 * quay_fv_assets_end + gw_partial,
        liab=pen["liab"] + 0.70 * quay["liab_end"],
        eq=eq_parent_end,
    ),
    "full consolidation": dict(
        rev=pen["revenue"] + quay["revenue"],
        ni=parent_ni_cons,
        assets=assets_cons,
        liab=liab_cons,
        eq=eq_parent_end + nci_end_partial,
    ),
}
ratios = {
    k: dict(
        margin=m["ni"] / m["rev"],
        roa=m["ni"] / m["assets"],
        turnover=m["rev"] / m["assets"],
        de=m["liab"] / m["eq"],
    )
    for k, m in methods.items()
}
for k, r in ratios.items():
    print(
        f"  {k:22s} margin {r['margin']:.4f} ROA {r['roa']:.4f} turnover {r['turnover']:.4f} liabilities/equity {r['de']:.4f}"
    )
ok(
    "proportionate consolidation balances too: assets = liabilities + parent equity",
    close(
        methods["proportionate (70%)"]["assets"],
        methods["proportionate (70%)"]["liab"] + eq_parent_end,
        1e-9,
    ),
)
ok(
    "same profit, different ratios: the one-line method shows the highest margin (10.52%) and ROA (8.25%) and the "
    "lowest liabilities/equity (1.22); full consolidation the lowest margin (7.51%) and ROA (6.64%); proportionate "
    "consolidation the highest liabilities/equity (1.46), adding 70% of Quay's liabilities with no NCI in equity",
    round(ratios["equity method"]["margin"], 4) == 0.1052
    and round(ratios["equity method"]["roa"], 4) == 0.0825
    and round(ratios["full consolidation"]["margin"], 4) == 0.0751
    and round(ratios["full consolidation"]["roa"], 4) == 0.0664
    and round(ratios["equity method"]["de"], 2) == 1.22
    and round(ratios["proportionate (70%)"]["de"], 2) == 1.46
    and ratios["proportionate (70%)"]["de"]
    > ratios["full consolidation"]["de"]
    > ratios["equity method"]["de"],
)

# ---------------------------------------------------------------------------------------------
print("== part 4: translating Penrose Inc. (USD) into EUR - current rate against temporal")
r_hist, r_open, r_avg, r_q4, r_close = 0.85, 0.90, 0.92, 0.94, 0.95  # EUR per USD
r_inv_open = 0.89  # opening inventory was bought at 0.89
# Opening balances (USD): cash 30, receivables 70, inventory 60, PP&E 330 (bought at 0.85), payables 60, debt 240.
op = dict(
    cash=30.0, receivables=70.0, inventory=60.0, ppe=330.0, payables=60.0, debt=240.0, capital=150.0
)
# Flows in the year (USD): credit sales 600 and other cash costs 100 evenly (average rate); purchases 360 evenly and
# 70 in the fourth quarter; depreciation 30; debt repaid 40 (monetary for monetary, no effect on the net position).
sales, other, purch_avg, purch_q4, dep_usd, repay = 600.0, 100.0, 360.0, 70.0, 30.0, 40.0
cl = dict(
    cash=50.0, receivables=80.0, inventory=70.0, ppe=300.0, payables=60.0, debt=200.0, capital=150.0
)
cogs_usd = op["inventory"] + purch_avg + purch_q4 - cl["inventory"]
ni_usd = sales - cogs_usd - dep_usd - other
nmp = lambda b: b["cash"] + b["receivables"] - b["payables"] - b["debt"]  # net monetary position
na = lambda b: b["cash"] + b["receivables"] + b["inventory"] + b["ppe"] - b["payables"] - b["debt"]
ok(
    "the USD statements articulate: COGS 420, net income 50; net assets 190 -> 240; net monetary position "
    "-200 -> -130 (+600 sales - 430 purchases - 100 costs)",
    close(cogs_usd, 420.0)
    and close(ni_usd, 50.0)
    and close(na(op), 190.0)
    and close(na(cl), 240.0)
    and close(nmp(op), -200.0)
    and close(nmp(cl), nmp(op) + sales - purch_avg - purch_q4 - other),
)
# Current rate method (IAS 21.39): assets and liabilities at the closing rate, income at the average rate.
re_open_eur = 34.0
cta_open = r_open * na(op) - r_hist * op["capital"] - re_open_eur
ni_cr = r_avg * ni_usd
cta_close = r_close * na(cl) - r_hist * cl["capital"] - re_open_eur - ni_cr
cta_year_direct = na(op) * (r_close - r_open) + ni_usd * (r_close - r_avg)
ok(
    "current rate: net assets 228.0, net income 46.0; translation adjustment 9.5 -> 20.5, a year's gain of 11.0 "
    "= opening net assets 190 x 0.05 + profit 50 x 0.03, taken to OCI",
    close(r_close * na(cl), 228.0)
    and close(ni_cr, 46.0)
    and close(cta_open, 9.5)
    and close(cta_close, 20.5)
    and close(cta_close - cta_open, cta_year_direct)
    and close(cta_year_direct, 11.0),
)
# Source reproduction: Subramanyam and Wild (2009) pp. 304-306, BritCo (GBP functional, USD presentation).
brit_na_open, brit_ni, brit_capital = 350_000.0, 150_000.0, 300_000.0
brit_usd_ni = brit_ni * 1.30
brit_cta_year = (
    (brit_na_open + brit_ni) * 1.40 - brit_capital * 1.10 - (60_000.0 + brit_usd_ni) - 30_000.0
)
ok(
    "Subramanyam's BritCo: translated net income 195,000; year's translation adjustment 85,000 as the balancing "
    "figure and directly as 350,000 x 0.20 + 150,000 x 0.10; cumulative 115,000",
    close(brit_usd_ni, 195_000.0)
    and close(brit_cta_year, 85_000.0)
    and close(brit_na_open * (1.40 - 1.20) + brit_ni * (1.40 - 1.30), brit_cta_year)
    and close(30_000.0 + brit_cta_year, 115_000.0),
)
# Temporal method (remeasurement as if EUR were functional): monetary items at closing, non-monetary at historical.
tm_na = lambda b, r_m, r_inv: r_m * nmp(b) + r_inv * b["inventory"] + r_hist * b["ppe"]
tm_open, tm_close = tm_na(op, r_open, r_inv_open), tm_na(cl, r_close, r_q4)
cogs_eur = (
    r_inv_open * op["inventory"] + r_avg * purch_avg + r_q4 * purch_q4 - r_q4 * cl["inventory"]
)
pre = r_avg * sales - cogs_eur - r_hist * dep_usd - r_avg * other
remeas = tm_close - tm_open - pre
remeas_direct = (
    nmp(op) * (r_close - r_open)
    + (sales - purch_avg - other) * (r_close - r_avg)
    - purch_q4 * (r_close - r_q4)
)
ok(
    "temporal: net assets 153.9 -> 197.3; COGS 384.6 at historical rates; profit before remeasurement 49.9; "
    "remeasurement loss 6.5 in profit, equal to -200 x 0.05 + 140 x 0.03 - 70 x 0.01",
    round(tm_open, 1) == 153.9
    and round(tm_close, 1) == 197.3
    and round(cogs_eur, 1) == 384.6
    and round(pre, 1) == 49.9
    and close(remeas, remeas_direct, 1e-9)
    and round(remeas, 1) == -6.5,
)
cur = {
    "current rate": dict(
        gross=(sales - cogs_usd) / sales,
        current_ratio=(cl["cash"] + cl["receivables"] + cl["inventory"]) / cl["payables"],
        ni=ni_cr,
        de=r_close * (cl["payables"] + cl["debt"]) / (r_close * na(cl)),
    ),
    "temporal": dict(
        gross=(r_avg * sales - cogs_eur) / (r_avg * sales),
        current_ratio=(r_close * (cl["cash"] + cl["receivables"]) + r_q4 * cl["inventory"])
        / (r_close * cl["payables"]),
        ni=pre + remeas,
        de=r_close * (cl["payables"] + cl["debt"]) / tm_close,
    ),
}
for k, r in cur.items():
    print(
        f"  {k:13s} gross margin {r['gross']:.4f} current ratio {r['current_ratio']:.4f} liabilities/equity {r['de']:.4f} net income {r['ni']:.4f}"
    )
ok(
    "the current rate preserves local ratios (gross margin 30.0%, current ratio 3.33, liabilities/equity 1.083); "
    "the temporal method changes them (30.3%, 3.32, 1.252) and reports profit of 43.4 against 46.0",
    round(cur["current rate"]["gross"], 3) == 0.3
    and round(cur["current rate"]["current_ratio"], 2) == 3.33
    and round(cur["current rate"]["de"], 3) == 1.083
    and round(cur["temporal"]["gross"], 3) == 0.303
    and round(cur["temporal"]["current_ratio"], 2) == 3.32
    and round(cur["temporal"]["de"], 3) == 1.252
    and round(cur["temporal"]["ni"], 1) == 43.4,
)
ok(
    "exposure to a further 0.05 rise in the USD: +12.0 to equity through OCI (net assets 240) under the current "
    "rate; -6.5 through profit (net monetary liabilities 130) under the temporal method",
    close(na(cl) * 0.05, 12.0) and close(nmp(cl) * 0.05, -6.5),
)

# ---------------------------------------------------------------------------------------------
print(
    "== part 5: hyperinflation - Penrose Andina under IAS 29 + IAS 21.42 against US GAAP remeasurement"
)
idx_buy, idx_open, idx_close = (
    100.0,
    180.0,
    250.0,
)  # general price index: three-year cumulative inflation 150%
eur_per_lcu_buy, eur_per_lcu_close = 0.020, 0.008
ppe_lcu = 1000.0
ppe_restated = ppe_lcu * idx_close / idx_buy
ok(
    "cumulative inflation 150% over three years exceeds the 100% indicator (IAS 29.3(e); FAS 52.11)",
    idx_close / idx_buy - 1 > 1.0,
)
ifrs_ppe = ppe_restated * eur_per_lcu_close
us_ppe = ppe_lcu * eur_per_lcu_buy
ok(
    "PP&E of 1,000 LCU: IFRS restates to 2,500 LCU and translates at 0.008 = EUR 20.0; US GAAP remeasures at "
    "the historical 0.020 = EUR 20.0 - equal only when the currency fell exactly with inflation",
    close(ifrs_ppe, 20.0) and close(us_ppe, 20.0),
)
eur_per_lcu_close2 = 0.010  # the currency fell less than prices rose
ok(
    "if the currency fell less (to 0.010), IFRS gives EUR 25.0 and US GAAP still EUR 20.0",
    close(ppe_restated * eur_per_lcu_close2, 25.0),
)
net_monetary_assets = 400.0
loss = net_monetary_assets * (idx_close / idx_open - 1)
ok(
    "holding 400 LCU of net monetary assets through the year (index 180 -> 250) loses 155.6 LCU of purchasing "
    "power, reported in profit (IAS 29.27-28)",
    round(loss, 1) == 155.6,
)

# ---------------------------------------------------------------------------------------------
print("== part 6: transaction exposure - a USD receivable on Penrose's EUR books")
usd_sale = 10.0
rev_eur = usd_sale * 0.90
recv_close = usd_sale * 0.95
settle = usd_sale * 0.93
ok(
    "sale at 0.90 recorded at EUR 9.0 (IAS 21.21); receivable remeasured at 0.95 = 9.5, gain 0.5 in profit "
    "(IAS 21.23, 28); settled at 0.93, loss 0.2 next year; total 0.3 = 10 x (0.93 - 0.90)",
    close(rev_eur, 9.0)
    and close(recv_close - rev_eur, 0.5)
    and close(settle - recv_close, -0.2)
    and close(settle - rev_eur, 0.3),
)

# ---------------------------------------------------------------------------------------------
print(
    "== part 7: multinational results - currency in growth and in the effective tax rate (Larch Brands)"
)
seg = {  # local-currency sales year 1, year 2; EUR per unit average rate year 1, year 2
    "euro area": (500.0, 520.0, 1.00, 1.00),
    "United States": (400.0, 440.0, 0.92, 0.86),
    "United Kingdom": (200.0, 196.0, 1.15, 1.18),
}
y1 = sum(a * r1 for a, b, r1, r2 in seg.values())
y2 = sum(b * r2 for a, b, r1, r2 in seg.values())
const = sum(b * r1 for a, b, r1, r2 in seg.values())
fx_effect = y2 - const
ok(
    "reported growth 2.89% = constant-currency growth 4.75% plus a currency effect of -1.87 points",
    round(y2 / y1 - 1, 4) == 0.0289
    and round(const / y1 - 1, 4) == 0.0475
    and round(fx_effect / y1, 4) == -0.0187
    and close(y2 / y1 - 1, const / y1 - 1 + fx_effect / y1),
    f"year 1 {y1:.2f}, year 2 {y2:.2f}, at year-1 rates {const:.2f}",
)
organic_us = 440 / 400 - 1
ok(
    "US local-currency growth 10% is the sustainable signal; the USD's fall turns it into 2.8% in EUR",
    close(organic_us, 0.10) and round(440 * 0.86 / (400 * 0.92) - 1, 3) == 0.028,
)
pbt = {"euro area": 60.0, "United States": 50.0, "United Kingdom": 20.0}
rates = {"euro area": 0.25, "United States": 0.21, "United Kingdom": 0.25}
nondeductible, prior_year_credit = 4.0, -1.5
tax = sum(pbt[k] * rates[k] for k in pbt) + 0.25 * nondeductible + prior_year_credit
etr = tax / sum(pbt.values())
recon = (
    0.25 * sum(pbt.values())
    + (0.21 - 0.25) * pbt["United States"]
    + 0.25 * nondeductible
    + prior_year_credit
)
ok(
    "ETR 23.08%: 25% statutory x 130 = 32.5, foreign rate differential -2.0, non-deductible +1.0, prior-year -1.5 "
    "(IAS 12.81(c) numerical reconciliation)",
    close(tax, recon) and close(tax, 30.0) and round(etr, 4) == 0.2308,
    f"tax {tax:.2f}, ETR {etr:.4f}",
)
pbt_shift = {"euro area": 50.0, "United States": 60.0, "United Kingdom": 20.0}
tax_shift = (
    sum(pbt_shift[k] * rates[k] for k in pbt_shift) + 0.25 * nondeductible + prior_year_credit
)
ok(
    "shifting 10 of profit to the US lowers tax to 29.6 and the ETR to 22.77% with no change in any tax rate: a mix effect",
    close(tax_shift, 29.6) and round(tax_shift / 130, 4) == 0.2277,
)
ok(
    "excluding the non-recurring prior-year credit the rate is 24.2%, the basis for forecasting",
    round((tax - prior_year_credit) / 130, 3) == 0.242,
)

# ---------------------------------------------------------------------------------------------
print("== part 8: banks - Hull's DLC example and a CAMELS review of Tamar Bank")
dlc = dict(nii=3.0, loan_losses=-0.8, nonint_inc=0.9, nonint_exp=-2.5)
pre_tax = sum(dlc.values())
ok(
    "Hull's DLC: pre-tax income 0.6 on assets 100 and equity 5 is a 12% pre-tax ROE",
    close(pre_tax, 0.6) and close(pre_tax / 5, 0.12),
)
stress = pre_tax - 3.2
after_tax = stress * 0.7
ok(
    "loan losses rising by 3.2% of assets give a pre-tax loss of 2.6 and an after-tax loss of about 1.8: equity "
    "falls from 5 to 3.2; at 1% equity the bank is insolvent",
    close(stress, -2.6)
    and round(after_tax, 2) == -1.82
    and round(5 + after_tax, 1) == 3.2
    and 1 + after_tax < 0,
)
tb = {  # Tamar Bank, two years (EUR billions)
    2025: dict(
        cet1=6.6,
        at1=1.0,
        t2=1.4,
        rwa=60.0,
        exposure=150.0,
        loans=100.0,
        npl=2.5,
        allowance=1.5,
        deposits=110.0,
        nii=3.3,
        fees=1.0,
        opex=2.6,
        provisions=0.4,
        tax_rate=0.25,
        avg_assets=148.0,
        avg_earning=135.0,
        hqla=22.0,
        outflows30=18.0,
        asf=118.0,
        rsf=105.0,
        equity=8.0,
    ),
    2026: dict(
        cet1=6.4,
        at1=1.0,
        t2=1.4,
        rwa=64.0,
        exposure=158.0,
        loans=108.0,
        npl=4.3,
        allowance=1.9,
        deposits=112.0,
        nii=3.4,
        fees=0.9,
        opex=2.8,
        provisions=1.1,
        tax_rate=0.25,
        avg_assets=154.0,
        avg_earning=140.0,
        hqla=19.0,
        outflows30=18.5,
        asf=120.0,
        rsf=116.0,
        equity=7.8,
    ),
}
rat = {}
for y, b in tb.items():
    ni_b = (b["nii"] + b["fees"] - b["opex"] - b["provisions"]) * (1 - b["tax_rate"])
    rat[y] = dict(
        cet1=b["cet1"] / b["rwa"],
        tier1=(b["cet1"] + b["at1"]) / b["rwa"],
        total=(b["cet1"] + b["at1"] + b["t2"]) / b["rwa"],
        leverage=(b["cet1"] + b["at1"]) / b["exposure"],
        npl=b["npl"] / b["loans"],
        coverage=b["allowance"] / b["npl"],
        cost_risk=b["provisions"] / b["loans"],
        nim=b["nii"] / b["avg_earning"],
        cost_income=b["opex"] / (b["nii"] + b["fees"]),
        roa=ni_b / b["avg_assets"],
        roe=ni_b / b["equity"],
        lcr=b["hqla"] / b["outflows30"],
        nsfr=b["asf"] / b["rsf"],
        ltd=b["loans"] / b["deposits"],
    )
for y, r in rat.items():
    print(f"  {y}: " + ", ".join(f"{k} {v:.4f}" for k, v in r.items()))
mins = dict(
    cet1=0.045 + 0.025, tier1=0.06 + 0.025, total=0.08 + 0.025, leverage=0.03, lcr=1.0, nsfr=1.0
)
ok(
    "2026: CET1 10.0%, Tier 1 11.56%, total 13.75%, leverage 4.68%, LCR 103%, NSFR 103%: every Basel minimum "
    "(with the 2.5% conservation buffer) met, but with a narrower margin than 2025",
    all(rat[2026][k] >= v for k, v in mins.items())
    and [round(rat[2026][k], 4) for k in ("cet1", "tier1", "total", "leverage")]
    == [0.1, 0.1156, 0.1375, 0.0468]
    and all(rat[2026][k] < rat[2025][k] for k in ("cet1", "lcr", "nsfr")),
)
ok(
    "asset quality: NPL ratio 2.50% -> 3.98%, coverage 60% -> 44%, cost of risk 0.40% -> 1.02%",
    [round(rat[2025]["npl"], 4), round(rat[2026]["npl"], 4)] == [0.025, 0.0398]
    and [round(rat[2025]["coverage"], 2), round(rat[2026]["coverage"], 2)] == [0.6, 0.44]
    and [round(rat[2025]["cost_risk"], 4), round(rat[2026]["cost_risk"], 4)] == [0.004, 0.0102],
)
ok(
    "earnings: ROE battered from 12.19% to 3.85%, cost/income 60.5% -> 65.1%, NIM 2.44% -> 2.43%",
    [round(rat[y]["roe"], 4) for y in (2025, 2026)] == [0.1219, 0.0385]
    and [round(rat[y]["cost_income"], 3) for y in (2025, 2026)] == [0.605, 0.651]
    and [round(rat[y]["nim"], 4) for y in (2025, 2026)] == [0.0244, 0.0243],
)
gap_1y = -12.0  # rate-sensitive assets less liabilities repricing within a year (EUR bn)
ok(
    "sensitivity to market risk: a one-year repricing gap of -12 bn loses 0.24 bn of NII for +200 bp, 16% of "
    "2026 income before provisions",
    close(gap_1y * 0.02, -0.24) and round(0.24 / (3.4 + 0.9 - 2.8), 2) == 0.16,
)
b26 = tb[2026]
topup = 0.60 * b26["npl"] - b26["allowance"]
pretax26 = b26["nii"] + b26["fees"] - b26["opex"] - b26["provisions"]
ok(
    "restoring 60% coverage needs about 0.68 bn of provisions, more than 2026 pre-tax profit of 0.40 bn",
    round(topup, 2) == 0.68 and round(pretax26, 2) == 0.40 and topup > pretax26,
)

# ---------------------------------------------------------------------------------------------
print("== part 9: insurers - Hull's operating ratio and Wren Insurance")
lr, er, divr, invr = 0.75, 0.30, 0.01, 0.09
ok(
    "Hull Table 3.2: loss 75% + expense 30% = combined 105%; with 1% dividends 106%; less investment income 9% "
    "= operating ratio 97%",
    close(lr + er, 1.05) and close(lr + er + divr, 1.06) and close(lr + er + divr - invr, 0.97),
)
wren = {
    2025: dict(
        nep=800.0,
        losses=520.0,
        lae=60.0,
        uw_exp=200.0,
        pol_div=0.0,
        inv_inc=72.0,
        reserves_prior=1200.0,
        development=-15.0,
        own_funds=900.0,
        scr=500.0,
        equity=850.0,
        invested=2400.0,
    ),
    2026: dict(
        nep=840.0,
        losses=610.0,
        lae=66.0,
        uw_exp=205.0,
        pol_div=0.0,
        inv_inc=70.0,
        reserves_prior=1250.0,
        development=35.0,
        own_funds=870.0,
        scr=540.0,
        equity=820.0,
        invested=2450.0,
    ),
}
wr = {}
for y, w in wren.items():
    loss_ratio = (w["losses"] + w["lae"]) / w["nep"]
    exp_ratio = w["uw_exp"] / w["nep"]
    combined = loss_ratio + exp_ratio
    wr[y] = dict(
        loss=loss_ratio,
        expense=exp_ratio,
        combined=combined,
        operating=combined - w["inv_inc"] / w["nep"],
        yield_=w["inv_inc"] / w["invested"],
        solvency=w["own_funds"] / w["scr"],
        premium_leverage=w["nep"] / w["equity"],
        development=w["development"] / w["reserves_prior"],
    )
for y, r in wr.items():
    print(f"  {y}: " + ", ".join(f"{k} {v:.4f}" for k, v in r.items()))
ok(
    "Wren: combined ratio 97.5% -> 104.9% (losses including adjustment 72.5% -> 80.5%), operating ratio "
    "88.5% -> 96.5%, adverse reserve development 2.8% of opening reserves, solvency ratio 180% -> 161%",
    [round(wr[y]["combined"], 4) for y in (2025, 2026)] == [0.975, 1.0488]
    and [round(wr[y]["operating"], 4) for y in (2025, 2026)] == [0.885, 0.9655]
    and round(wr[2026]["development"], 4) == 0.028
    and [round(wr[y]["solvency"], 2) for y in (2025, 2026)] == [1.8, 1.61],
)
uw_result_2026 = wren[2026]["nep"] - wren[2026]["losses"] - wren[2026]["lae"] - wren[2026]["uw_exp"]
ok(
    "2026 underwriting loss of 41 is covered by investment income of 70; without the 35 of adverse development "
    "the combined ratio would have been 100.7%",
    close(uw_result_2026, -41.0)
    and round((wren[2026]["losses"] - 35 + wren[2026]["lae"] + wren[2026]["uw_exp"]) / 840, 4)
    == 1.0071,
)
ok(
    "Wren: 2025 reserve release 1.3% of opening reserves; 2026 expense ratio 24.4%, yield 2.9%; premiums/equity "
    "0.94 -> 1.02; Hull's DLC funding debt/equity 95/5 = 19",
    round(wr[2025]["development"], 3) == -0.013
    and round(wr[2026]["expense"], 3) == 0.244
    and round(wr[2026]["yield_"], 3) == 0.029
    and [round(wr[y]["premium_leverage"], 2) for y in (2025, 2026)] == [0.94, 1.02]
    and close(95 / 5, 19.0),
)
ok(
    "Tamar 2025 leverage 5.07%, LCR 122%, NSFR 112%, loans/deposits 91% -> 96%",
    round(rat[2025]["leverage"], 4) == 0.0507
    and round(rat[2025]["lcr"], 2) == 1.22
    and round(rat[2025]["nsfr"], 2) == 1.12
    and [round(rat[y]["ltd"], 2) for y in (2025, 2026)] == [0.91, 0.96],
)

# ---------------------------------------------------------------------------------------------
print(
    "== part 10: life insurers - Solvency II shocks, rate matching and new-business value (Linden, Rowan)"
)
# Hypothetical, EUR millions. Flat risk-free rate 3%; Gompertz mortality q_x = 0.00005 exp(0.095 x). Shocks from
# Delegated Regulation (EU) 2015/35 Arts. 137 (mortality +15%), 138 (longevity -20%), 142(6)(b) (mass lapse 40%);
# correlations Art. 136 and Directive 2009/138/EC Annex IV (life-market 0.25). Risk margin held at 40 (an input).
R_F = 0.03


def q_x(age, mult=1.0):
    return np.minimum(1.0, mult * 0.00005 * np.exp(0.095 * age))


def alive(age0, n, mult=1.0):
    qs = q_x(age0 + np.arange(n), mult)
    return np.concatenate([[1.0], np.cumprod(1 - qs)[:-1]]), qs


def disc(n, r):
    return (1 + r) ** -np.arange(1, n + 1)


def annuity_bel(pay, r=R_F, m=1.0, n=46):  # paid at the end of each year to survivors from age 65
    s_, q_ = alive(65, n, m)
    return float(np.sum(pay * s_ * (1 - q_) * disc(n, r)))


def term_bel(S, P, r=R_F, m=1.0, n=20):  # claims at year end, premiums in advance, ages 45-64
    s_, q_ = alive(45, n, m)
    d_ = disc(n, r)
    return float(np.sum(S * s_ * q_ * d_) - np.sum(P * s_ * d_ * (1 + r)))


def savings_bel(G, r=R_F, T=10):
    return G / (1 + r) ** T


CORR_LIFE = np.array(
    [[1, -0.25, 0.0], [-0.25, 1, 0.25], [0.0, 0.25, 1]]
)  # mortality, longevity, lapse


def life_insurer(pay, S, P, G, SV, A, TA, RM=40.0):
    def bel(r=R_F, ma=1.0, mt=1.0):
        return annuity_bel(pay, r, ma) + term_bel(S, P, r, mt) + savings_bel(G, r)

    def assets(r):
        return A * ((1 + R_F) / (1 + r)) ** TA

    b0 = bel()
    of_ = A - b0 - RM
    up = (assets(R_F + 0.005) - bel(R_F + 0.005)) - (A - b0)
    dn = (assets(R_F - 0.005) - bel(R_F - 0.005)) - (A - b0)
    mkt = max(0.0, -up, -dn)
    longev, mort = bel(ma=0.8) - b0, bel(mt=1.15) - b0
    lapse = 0.4 * max(SV - savings_bel(G), 0.0)
    v = np.array([max(mort, 0.0), max(longev, 0.0), lapse])
    life = float(np.sqrt(v @ CORR_LIFE @ v))
    scr = float(np.sqrt(life**2 + mkt**2 + 2 * 0.25 * life * mkt))
    return dict(
        ann=annuity_bel(pay),
        term=term_bel(S, P),
        sav=savings_bel(G),
        bel=b0,
        of=of_,
        up=up,
        dn=dn,
        longev=longev,
        mort=mort,
        lapse=lapse,
        life=life,
        scr=scr,
        ratio=of_ / scr,
    )


lin = life_insurer(100, 2000, 22, 1250, 1000, 2170, 10)
row = life_insurer(20, 20000, 220, 2500, 2000, 2100, 6)
keys = ("ann", "term", "sav", "of", "up", "dn", "longev", "mort", "lapse", "life", "scr")
print("  Linden " + ", ".join(f"{k_} {lin[k_]:.2f}" for k_ in keys) + f", ratio {lin['ratio']:.4f}")
print("  Rowan  " + ", ".join(f"{k_} {row[k_]:.2f}" for k_ in keys) + f", ratio {row['ratio']:.4f}")
ok(
    "Linden: best estimates 1,046.7 / -62.7 / 930.1; own funds 215.8; rates +50/-50 bp -15.6/+15.7; longevity "
    "99.5, mortality 37.3, mass lapse 28.0; life SCR 107.8, SCR 112.7, ratio 191.5%",
    [round(lin[k_], 1) for k_ in keys]
    == [1046.7, -62.7, 930.1, 215.8, -15.6, 15.7, 99.5, 37.3, 28.0, 107.8, 112.7]
    and round(lin["ratio"], 3) == 1.915,
)
ok(
    "Rowan: best estimates 209.3 / -626.5 / 1,860.2; own funds 617.0; rates +59.7/-66.6; longevity 19.9, "
    "mortality 373.1, mass lapse 55.9; life SCR 373.6, SCR 395.6, ratio 156.0%; 139% after the rate fall alone",
    [round(row[k_], 1) for k_ in keys]
    == [209.3, -626.5, 1860.2, 617.0, 59.7, -66.6, 19.9, 373.1, 55.9, 373.6, 395.6]
    and round(row["ratio"], 3) == 1.560
    and round((row["of"] + row["dn"]) / row["scr"], 2) == 1.39,
)
# Independent route for the annuity best estimate: a backward recursion V_x = (1 - q_x)(pay + V_{x+1}) / (1 + r).
v_rec = 0.0
for age_ in range(65 + 46 - 1, 64, -1):
    v_rec = (1 - q_x(age_)) * (100 + v_rec) / (1 + R_F)
ok(
    "the annuity best estimate by backward recursion equals the expected-cash-flow sum; the longevity shock raises "
    "it and the mortality shock lowers it (the offset in Hull, pp. 56-57)",
    close(v_rec, annuity_bel(100), 1e-9)
    and annuity_bel(100, m=0.8) > annuity_bel(100) > annuity_bel(100, m=1.15),
)
v_check = np.array([lin["mort"], lin["longev"], lin["lapse"]])
ok(
    "aggregation by hand: life SCR^2 = sum of squares - 2 x 0.25 x mortality x longevity + 2 x 0.25 x longevity "
    "x lapse; the diversified life SCR is below the 164.8 simple sum",
    close(
        lin["life"] ** 2,
        float(np.sum(v_check**2)) - 0.5 * v_check[0] * v_check[1] + 0.5 * v_check[1] * v_check[2],
        1e-9,
    )
    and lin["life"] < v_check.sum()
    and round(v_check.sum(), 1) == 164.8,
)


def new_business(S, load, acq=5.0, exp_rate=0.03, tax=0.25, coc=0.06, ra_rate=0.05, n=20):
    s_, q_ = alive(45, n)
    d_ = disc(n, R_F)
    claims = S * s_ * q_
    P = (1 + load) * np.sum(claims * d_) / np.sum(s_ * d_ * (1 + R_F))
    pv_claims = float(np.sum(claims * d_))
    pvnbp = float(np.sum(P * s_ * d_ * (1 + R_F)))
    pv_exp = acq + exp_rate * pvnbp
    s2, q2 = alive(45, n, 1.15)
    scr_new = float(np.sum(S * s2 * q2 * d_)) - pv_claims
    remaining = np.array(
        [np.sum(claims[t_:] * (1 + R_F) ** -(np.arange(t_, n) - t_ + 1)) for t_ in range(n)]
    )
    coc_cost = coc * scr_new * float(np.sum(remaining / remaining[0] * d_))
    ra = ra_rate * pv_claims
    profit = pvnbp - pv_claims - pv_exp
    return dict(
        pvnbp=pvnbp,
        claims=pv_claims,
        exp=pv_exp,
        profit=profit,
        ra=ra,
        csm=max(profit - ra, 0.0),
        loss=max(ra - profit, 0.0),
        vnb=profit * (1 - tax) - coc_cost,
    )


nb40, nb15 = new_business(500, 0.40), new_business(500, 0.15)
ok(
    "new term business at a 40% loading: PVNBP 89.55, claims 63.96, expenses 7.69, risk adjustment 3.20, CSM 14.70; "
    "VNB 7.21, a margin of 8.05% of PVNBP; fulfilment cash flows + CSM = PV premiums (no day-one profit)",
    [round(nb40[k_], 2) for k_ in ("pvnbp", "claims", "exp", "ra", "csm", "vnb")]
    == [89.55, 63.96, 7.69, 3.20, 14.70, 7.21]
    and round(nb40["vnb"] / nb40["pvnbp"], 4) == 0.0805
    and close(nb40["claims"] + nb40["exp"] + nb40["ra"] + nb40["csm"], nb40["pvnbp"], 1e-9),
)
ok(
    "at a 15% loading expected profit is still 2.39, but after the risk adjustment the group is onerous: loss 0.81 "
    "at once, no CSM; VNB -4.42",
    round(nb15["profit"], 2) == 2.39
    and nb15["csm"] == 0.0
    and round(nb15["loss"], 2) == 0.81
    and round(nb15["vnb"], 2) == -4.42,
)
cnp = dict(vnb=782.0, pvnbp=28201.0, up=1248.0, dn=-1158.0)
ok(
    "CNP Assurances 2017 (reported): VNB / PVNBP = 2.8%; the rate sensitivities are asymmetric (+1,248 against "
    "-1,158)",
    round(cnp["vnb"] / cnp["pvnbp"], 3) == 0.028 and cnp["up"] + cnp["dn"] > 0,
)

print(f"\n{n_checks} checks executed")
if fails:
    print("FAILED:", fails)
    sys.exit(1)
print("all checks passed")
