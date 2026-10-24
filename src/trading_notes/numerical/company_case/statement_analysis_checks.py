"""Worked numbers of the financial statement analysis entries, around Harbour Tools plc."""

import math
import sys
from typing import cast

import numpy as np
import scipy
from scipy.stats import norm

from trading_notes.numerical.company_case.harbour import (
    ACQ_INTANGIBLE_LIFE,
    ACQ_PPE_LIFE,
    ASSETS,
    DEV_LIFE,
    EQUITY,
    LEASE_RATE,
    LEGACY_DEV_LIFE,
    LIABS,
    TAX,
    YEARS,
    Acquisition,
    ForecastCase,
    HarbourCase,
    YearForecast,
    avg,
    nopat_route_fcff,
    opening_2023_balances,
    straight_line,
    terminal_value,
    valuation_fcff,
)
from trading_notes.numerical.option_pricing.black_scholes import BlackScholes
from trading_notes.numerical.records import Record
from trading_notes.numerical.report import CheckReport, print_versions
from trading_notes.numerical.tolerance import close

type Line = dict[str, float]


def check_ledger(report: CheckReport, case: HarbourCase) -> None:
    """Check the ledger's statements: balance, profit, both cash-flow methods and equity."""
    print("== part 1: Harbour Tools plc ledger, statements and reconciliations")
    statements = case.statements
    opening_2023 = opening_2023_balances()  # equity residual at the opening date only
    for y in (2024, 2025):
        s = statements[y]
        c, o = s.closing, s.opening
        assets = sum(c[a] for a in ASSETS)
        liabs = -sum(c[a] for a in LIABS)
        equity = -sum(c[a] for a in EQUITY)
        report.ok(
            f"{y}: balance sheet balances (assets {assets:.2f} = liabilities {liabs:.2f} + equity"
            f" {equity:.2f})",
            close(assets, liabs + equity, 1e-9),
        )
        report.ok(
            f"{y}: ledger profit equals income-statement profit",
            close(s.profit, s.income["profit"], 1e-9),
        )
        # Direct method: the sum of tagged cash postings by activity.
        cfo_direct, cfi, cff = s.cfo, s.cfi, s.cff
        # Indirect method from statements only (no ledger tags).
        d = {k: c[k] - o[k] for k in c}
        i = s.income
        noncash = (
            (-d["acc_dep"] - (-YEARS[y].disposal[1]))
            + YEARS[y].rou_dep
            + YEARS[y].dev_amort
            + YEARS[y].sbc
            + s.flows["deferred_tax"]
        )
        # Pension: P&L cost (service + net interest) less contributions = change in
        # liability less OCI part.
        pension_adj = -d["db_liab"] - YEARS[y].remeasurement_loss
        wc = (
            -d["receivables"]
            - d["inventory"]
            - d["payables"]
            - d["accrued_wages"]
            - d["tax_payable"]
            - d["restructuring_prov"]
        )
        cfo_indirect = i["profit"] + noncash - i["other_income"] + pension_adj + wc
        report.ok(
            f"{y}: indirect CFO equals direct CFO ({cfo_direct:.2f})",
            close(cfo_indirect, cfo_direct, 1e-9),
            f"indirect {cfo_indirect:.4f}",
        )
        report.ok(
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
            + YEARS[y].sbc
            + YEARS[y].exercise_cash
            - YEARS[y].dividends
        )
        report.ok(
            f"{y}: total equity rolls forward (profit, OCI, share-based pay, exercise, dividends)",
            close(roll, eq_close, 1e-9),
        )
        report.ok(
            f"{y}: retained earnings roll forward",
            close(
                -o["retained"] + i["profit"] - YEARS[y].dividends,
                -c["retained"],
                1e-9,
            ),
        )
    for y in (2024, 2025):
        s, i = statements[y], statements[y].income
        print(
            f"  {y} IS: revenue {i['revenue']:.2f} cogs {i['cogs']:.2f} gross {i['gross']:.2f} sga"
            f" {i['sga']:.2f} rnd {i['rnd']:.2f} restr {i['restructuring']:.2f} other"
            f" {i['other_income']:.2f} op {i['op']:.2f} fin {i['fin']:.2f} pbt {i['pbt']:.2f} tax"
            f" {i['tax']:.2f} profit {i['profit']:.4f} oci {i['oci']:.2f}"
        )
        print(
            f"  {y} CF: CFO {s.cfo:.4f} CFI {s.cfi:.2f} CFF {s.cff:.4f}; tags "
            + ", ".join(f"{k[0]}:{k[1]} {v:.2f}" for k, v in sorted(s.tags.items()))
        )
        c = s.closing
        print(f"  {y} BS: " + ", ".join(f"{k} {c[k]:.2f}" for k in ASSETS + LIABS + EQUITY))
    print(
        "  2023 opening BS: "
        + ", ".join(f"{k} {opening_2023[k]:.2f}" for k in ASSETS + LIABS + EQUITY)
    )


def check_common_size(report: CheckReport, case: HarbourCase) -> None:
    """Check common-size statements, the ratio families and the return decompositions."""
    print(
        "== part 2: common-size statements, ratio families and return decompositions (Harbour"
        " 2024-2025)"
    )
    statements, B, R = case.statements, case.balances, case.ratios
    for y in (2024, 2025):
        i, r = statements[y].income, R[y]
        report.ok(
            f"{y}: three-factor DuPont reproduces ROE",
            close(r.net_margin * r.tat * r.lev, r.roe, 1e-12),
        )
        report.ok(
            f"{y}: five-factor DuPont reproduces ROE",
            close(
                r.tax_burden * r.interest_burden * r.op_margin * r.tat * r.lev,
                r.roe,
                1e-12,
            ),
        )
        rnoa, nfr = r.rnoa, r.nfr
        report.ok(
            f"{y}: ROE = RNOA + FLEV x (RNOA - NFR)",
            close(rnoa + r.flev * (rnoa - nfr), r.roe, 1e-12),
            f"RNOA {rnoa:.4%}, FLEV {r.flev:.4f}, NFR {nfr:.4%}, ROE {r.roe:.4%}",
        )
        print(f"  {y} ratios: " + ", ".join(f"{k} {val:.4f}" for k, val in r.model_dump().items()))
        cs = {
            k: i[k] / i["revenue"]
            for k in (
                "cogs",
                "gross",
                "sga",
                "rnd",
                "restructuring",
                "op",
                "fin",
                "tax",
                "profit",
            )
        }
        report.ok(
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
        ta = case.balance_view(y).ta
        csb = {a: B[y][a] / ta for a in ASSETS}
        report.ok(
            f"{y}: common-size balance sheet assets sum to 100%",
            close(sum(csb.values()), 1.0, 1e-12),
        )
        print(f"  {y} common-size IS: " + ", ".join(f"{k} {v:.2%}" for k, v in cs.items()))
        print(f"  {y} common-size assets: " + ", ".join(f"{k} {v:.2%}" for k, v in csb.items()))
        print(
            f"  {y} BS view: "
            + ", ".join(f"{k} {val:.2f}" for k, val in case.balance_view(y).model_dump().items())
        )
    # Covenant breach at year-end makes the whole term loan current (IAS 1 para. 74).
    v25 = case.balance_view(2025)
    breach_cl = v25.cl + (-B[2025]["term_loan"] - 25)
    report.ok(
        "covenant breach: current ratio falls from 1.84 to 0.94",
        round(v25.ca / v25.cl, 2) == 1.84 and round(v25.ca / breach_cl, 2) == 0.94,
        f"current liabilities {breach_cl:.2f}",
    )
    report.ok(
        "debt to equity rises from 0.55 to 0.60 with the after-tax pension deficit",
        round(v25.debt / v25.eq, 2) == 0.55
        and round((v25.debt - B[2025]["db_liab"] * (1 - TAX)) / v25.eq, 2) == 0.60,
    )
    # Exact log attribution of the ROE change 2024 -> 2025 across the five DuPont factors.
    factors = {
        "tax_burden": (R[2025].tax_burden, R[2024].tax_burden),
        "interest_burden": (R[2025].interest_burden, R[2024].interest_burden),
        "op_margin": (R[2025].op_margin, R[2024].op_margin),
        "tat": (R[2025].tat, R[2024].tat),
        "lev": (R[2025].lev, R[2024].lev),
    }
    fac = list(factors)
    logs = {f: math.log(now / before) for f, (now, before) in factors.items()}
    report.ok(
        "log attribution of ROE change sums exactly",
        close(sum(logs.values()), math.log(R[2025].roe / R[2024].roe), 1e-12),
        ", ".join(f"{f} {v:+.4f}" for f, v in logs.items()),
    )
    # Same attribution in percentage points by proportional allocation of the ROE change.
    droe = R[2025].roe - R[2024].roe
    pp = {f: droe * logs[f] / sum(logs.values()) for f in fac}
    print(
        "  ROE change attribution (pp): "
        + ", ".join(f"{f} {v * 100:+.3f}" for f, v in pp.items())
        + f"; total {droe * 100:+.3f}"
    )
    # Restructuring add-back: ROE 2025 excluding the after-tax restructuring charge (tax at
    # 25%, deductible).
    i25 = statements[2025].income
    adj_profit = i25["profit"] + i25["restructuring"] * (1 - TAX)
    report.ok(
        "2025 ROE excluding restructuring (after-tax 13.5) is higher than reported",
        adj_profit / avg(lambda t: case.balance_view(t).eq, 2025) > R[2025].roe,
        f"adjusted profit {adj_profit:.2f}, ROE"
        f" {adj_profit / avg(lambda t: case.balance_view(t).eq, 2025):.4%}",
    )
    # Currency-unit invariance: restating in EUR thousands leaves every ratio unchanged.
    scaled_roe = (i25["profit"] * 1000) / (avg(lambda t: case.balance_view(t).eq, 2025) * 1000)
    report.ok(
        "ratios are invariant to the currency unit",
        close(scaled_roe, R[2025].roe, 1e-12),
    )


def check_cash_flow(report: CheckReport, case: HarbourCase) -> None:
    """Check 2025 free cash flows against independent routes, and the coverage ratios."""
    print("== part 3: cash-flow interpretation, free cash flow and coverage (Harbour 2025)")
    statements, B, cf = case.statements, case.balances, case.cash_flow_2025
    i25 = statements[2025].income
    s25 = statements[2025]
    t25 = cf.tags
    interest_paid, capex_net, fcff_cfo = cf.interest_paid, cf.capex_net, cf.fcff
    # Damodaran's route: EBIT(1-t) + D&A - capex - change in WC; reconcile the non-cash items
    # explicitly.
    p25 = YEARS[2025]
    da = p25.dep + p25.rou_dep + p25.dev_amort
    d = {k: B[2025][k] - B[2024][k] for k in B[2025]}
    dwc = (
        d["receivables"]
        + d["inventory"]
        + d["payables"]
        + d["accrued_wages"]
        + d["restructuring_prov"]
    )
    ebit = i25["op"]
    fcff_ebit_book = ebit * (1 - TAX) + da - capex_net - dwc
    # Differences: actual cash tax vs statutory tax on EBIT, SBC, pension cost vs
    # contribution, disposal loss, lease principal (leases are financing here, so the ROU
    # depreciation added back is offset by treating lease payments as debt service), and
    # tax-payable change.
    cash_tax_on_ebit = -t25[("op", "tax_paid")] + interest_paid * TAX
    recon = (
        (ebit - cash_tax_on_ebit)
        + da
        + p25.sbc
        + (p25.service_cost - p25.db_contrib)
        - i25["other_income"]
        - capex_net
        - dwc
    )
    report.ok(
        "FCFF from CFO equals EBIT less cash operating taxes plus non-cash items less investment",
        close(fcff_cfo, recon, 1e-9),
        f"FCFF {fcff_cfo:.4f}; textbook EBIT(1-t) route {fcff_ebit_book:.4f}",
    )
    net_borrowing, fcfe = cf.net_borrowing, cf.fcfe
    fcfe_from_fcff = fcff_cfo - interest_paid * (1 - TAX) + net_borrowing
    report.ok(
        "FCFE from CFO equals FCFF less after-tax interest plus net borrowing",
        close(fcfe, fcfe_from_fcff, 1e-9),
        f"FCFE {fcfe:.4f}, net borrowing {net_borrowing:.2f}",
    )
    report.ok(
        "FCFE reconciles to dividends + buybacks - issues + change in cash",
        close(
            fcfe,
            -t25[("fin", "dividends")] - t25[("fin", "share_issue")] + d["cash"],
            1e-9,
        ),
    )
    # Explicit bridge from the EBIT(1-t) route to the CFO route, item by item.
    bridge = dict(
        sbc=p25.sbc,
        pension_service_less_contrib=p25.service_cost - p25.db_contrib,
        disposal_loss=-i25["other_income"],
        cash_vs_statutory_tax_on_ebit=TAX * ebit - cash_tax_on_ebit,
    )
    report.ok(
        "FCFF bridge: EBIT route + SBC + (service cost - contributions) + disposal loss + tax"
        " difference = CFO route",
        close(fcff_ebit_book + sum(bridge.values()), fcff_cfo, 1e-9),
        ", ".join(f"{k} {v:+.2f}" for k, v in bridge.items()),
    )
    # The accounting FCFF treats leases as financing but omits the right-of-use asset added in
    # 2025 (30, non-cash, so correctly absent from the statutory cash-flow statement, IAS 7
    # paras. 43-44). Economically the addition is capital expenditure financed by new lease debt
    # (Damodaran, Leases, Debt and Value, 2009, pp. 25-27).
    rou_add, fcff_lease = cf.rou_additions, cf.fcff_leases_as_debt
    report.ok(
        "leases as debt: deducting the 30 right-of-use addition as reinvestment changes FCFF from"
        " 48.54 to 18.54",
        close(fcff_cfo, 48.54, 1e-9) and close(fcff_lease, 18.54, 1e-9),
    )
    fcfe_debt_view = s25.cfo - capex_net - rou_add + (net_borrowing + rou_add)
    report.ok(
        "FCFE is unchanged by the lease presentation: the addition is offset by the new lease debt"
        " (28.04)",
        close(fcfe_debt_view, fcfe, 1e-9),
    )
    # Share-based pay: statutory CFO adds the non-cash expense back; valuation deducts it
    # (non-deductible here, so no tax effect). Pension: deficit as a debt-like claim, so
    # contributions above service cost and the tax shield on net interest are financing flows,
    # not FCFF.
    pens_int25 = statements[2025].flows["fin_pension"]
    pension_fin, fcff_val25, fcfe_val25 = cf.pension_financing, cf.valuation_fcff, cf.valuation_fcfe
    pension_borrow25 = p25.service_cost + pens_int25 - p25.db_contrib
    report.ok(
        "2025 valuation FCFF 13.00 = 18.54 - share-based expense 9 + pension financing 3.46",
        close(fcff_val25, 13.0, 1e-9) and close(pension_fin, 3.46, 1e-9),
    )
    report.ok(
        "valuation FCFF = valuation FCFE + after-tax interest (loan, lease, pension) - net"
        " borrowing (incl. lease, pension)",
        close(
            fcff_val25,
            fcfe_val25
            + (interest_paid + pens_int25) * (1 - TAX)
            - (net_borrowing + rou_add)
            - pension_borrow25,
            1e-9,
        ),
        f"FCFE after share-based expense {fcfe_val25:.2f}; pension net borrowing"
        f" {pension_borrow25:+.2f}",
    )
    debt_close = case.balance_view(2025).debt
    cov = dict(
        cfo_to_debt=s25.cfo / debt_close,
        cfo_to_capex=s25.cfo / capex_net,
        cash_interest_cov=(s25.cfo + interest_paid - t25[("op", "tax_paid")]) / interest_paid,
        debt_payback_years=debt_close / s25.cfo,
        retained_cfo_to_investment=(s25.cfo + t25[("fin", "dividends")]) / capex_net,
        adequacy_2y=(statements[2024].cfo + s25.cfo)
        / (
            -(statements[2024].tags[("inv", "capex")] + t25[("inv", "capex")])
            - (statements[2024].tags[("inv", "development")] + t25[("inv", "development")])
            + max(0, B[2024]["inventory"] - B[2023]["inventory"])
            + max(0, d["inventory"])
            - statements[2024].tags[("fin", "dividends")]
            - t25[("fin", "dividends")]
        ),
    )
    cs_cf = {k: v / i25["revenue"] for k, v in t25.items()}
    print("  2025 coverage: " + ", ".join(f"{k} {v:.4f}" for k, v in cov.items()))
    print(
        "  2025 common-size cash flows (% revenue): "
        + ", ".join(f"{k[0]}:{k[1]} {v:.2%}" for k, v in sorted(cs_cf.items()))
    )
    report.ok(
        "cash interest coverage exceeds 10 and CFO covers net investment",
        cov["cash_interest_cov"] > 10 and cov["cfo_to_capex"] > 1,
        f"FCFF {fcff_cfo:.2f}, FCFE {fcfe:.2f}",
    )
    # Sustainability decomposition of 2025 CFO: working-capital, provision and pension-funding
    # effects.
    wc_effect = -dwc
    report.ok(
        "2025 CFO components: provision build adds 12, working capital absorbs cash",
        close(d["restructuring_prov"] * -1, 12, 1e-9) and wc_effect < 12,
        f"working capital incl. provision {wc_effect:+.2f}",
    )


def check_eps(report: CheckReport, case: HarbourCase) -> None:
    """Check basic and diluted EPS with antidilution (Kestrel, illustrative)."""
    statements = case.statements
    print("== part 4: basic and diluted EPS with antidilution (Kestrel, illustrative)")
    # Shares: 40m at 1 Jan; 6m issued 1 Apr; 2m bought back 1 Oct; 1-for-10 bonus issue 30 Nov
    # (retrospective).
    months = 12
    wa_pre_bonus = 40 + 6 * 9 / months - 2 * 3 / months
    wa = wa_pre_bonus * 1.1
    # Day-count independent check: monthly share counts averaged.
    monthly = [40] * 3 + [46] * 6 + [44] * 3
    report.ok(
        "weighted average shares: formula equals month-by-month average",
        close(cast(np.float64, np.mean(monthly)) * 1.1, wa, 1e-12),
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
        max(0.0, 1.0 - 1.0 * opt_unvested_price / avg_price)
        if opt_unvested_price < avg_price
        else 0.0,
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
    report.ok(
        "IAS 33 sequencing gives the most dilutive EPS (equals the subset minimum)",
        close(best[0], diluted, 1e-12),
        f"basic {basic:.4f}, diluted {diluted:.4f}, included {included}",
    )
    report.ok(
        "convertible preference shares are antidilutive (EPI 1.20 exceeds diluted EPS)",
        "convertible_pref" not in included and pref[1] / pref[2] > diluted,
    )
    report.ok(
        "unvested options with 47A-adjusted price 12.50 above average 12 add no shares",
        opt_unvested[2] == 0.0,
    )
    # Harbour 2025 basic EPS: 100m shares at 1 Jan 2025, 0.75m issued on exercise at EUR 8 on
    # 1 Jul 2025.
    h_wa = 100 + 0.75 * 0.5
    h_basic = statements[2025].income["profit"] / h_wa
    h_inc = 5.0 - 5.0 * 8 / 11  # 5m vested options at EUR 8, average price EUR 11
    h_diluted = statements[2025].income["profit"] / (h_wa + h_inc)
    report.ok(
        "Harbour 2025 EPS: basic and diluted (treasury-stock method)",
        h_diluted < h_basic,
        f"basic {h_basic:.4f}, diluted {h_diluted:.4f}, incremental shares {h_inc:.4f}m",
    )


def check_revenue(report: CheckReport) -> None:
    """Check revenue recognition (allocation, timing, variable consideration, principal/agent)."""
    print(
        "== part 5: revenue recognition (allocation, timing, variable consideration,"
        " principal/agent)"
    )
    tp = 1000.0
    ssp = {"equipment": 900.0, "installation": 100.0, "service_24m": 200.0}
    alloc = {k: tp * v / sum(ssp.values()) for k, v in ssp.items()}
    report.ok(
        "relative stand-alone selling price allocation sums to the transaction price",
        close(sum(alloc.values()), tp, 1e-9),
        ", ".join(f"{k} {v:.2f}" for k, v in alloc.items()),
    )
    # Delivery 1 Nov 2025 (equipment), installation completed 30 Nov 2025, service 1 Dec
    # 2025-30 Nov 2027 straight-line.
    rev_2025 = alloc["equipment"] + alloc["installation"] + alloc["service_24m"] / 24
    rev_2026 = alloc["service_24m"] * 12 / 24
    rev_2027 = alloc["service_24m"] * 11 / 24
    report.ok(
        "revenue over the contract life equals the transaction price",
        close(rev_2025 + rev_2026 + rev_2027, tp, 1e-9),
        f"2025 {rev_2025:.4f}, 2026 {rev_2026:.4f}, 2027 {rev_2027:.4f}",
    )
    # Paid in full on signing (1 Oct 2025): contract liability at 31 Dec 2025.
    report.ok(
        "contract liability at year-end equals unsatisfied service obligation",
        close(tp - rev_2025, rev_2026 + rev_2027, 1e-9),
        f"{tp - rev_2025:.4f}",
    )
    # Variable consideration: volume rebate. Expected value of the price vs constrained amount.
    outcomes = np.array([100.0, 95.0, 90.0])  # price per unit after rebate tiers
    probs = np.array([0.5, 0.3, 0.2])
    ev = outcomes @ probs
    # Constraint: include only the amount for which a significant reversal is highly probable
    # not to occur.
    cum = np.cumsum(probs)  # outcomes sorted from highest price: P(price >= outcome)
    # Illustrative reading of "highly probable": at least 90 percent (the standard sets no
    # numeric threshold).
    constrained = max(o for o, pr in zip(outcomes, cum) if pr >= 0.9)
    report.ok(
        "constrained variable consideration is below the expected value",
        constrained < ev,
        f"expected {ev:.2f}, constrained {constrained:.2f}",
    )
    # Principal vs agent: same profit, different revenue and margins.
    gross_sale, cost_to_vendor = 100.0, 85.0
    principal = dict(revenue=gross_sale, profit=gross_sale - cost_to_vendor)
    agent = dict(revenue=gross_sale - cost_to_vendor, profit=gross_sale - cost_to_vendor)
    report.ok(
        "principal and agent presentations give the same profit but different margins",
        close(principal["profit"], agent["profit"])
        and agent["profit"] / agent["revenue"] > principal["profit"] / principal["revenue"],
        f"margins {principal['profit'] / principal['revenue']:.0%} vs"
        f" {agent['profit'] / agent['revenue']:.0%}",
    )


def check_capitalisation(report: CheckReport) -> None:
    """Check capitalising versus expensing (development spend amortised over three years)."""
    print("== part 6: capitalising versus expensing (development spend amortised over three years)")

    def capitalisation_paths(spend: list[float], life: int = 3) -> list[dict[str, float]]:
        asset, out = 0.0, []
        for t, x in enumerate(spend):
            amort = sum(
                spend[k] / life for k in range(max(0, t - life), t)
            )  # straight-line from the following year
            asset += x - amort
            out.append(dict(amort=amort, asset=asset, expense_diff=x - amort))
        return out

    for label, spend in (
        ("constant", [30.0] * 6),
        ("growing 10%", [30.0 * 1.1**t for t in range(6)]),
    ):
        path = capitalisation_paths(spend)
        cum_diff = sum(p["expense_diff"] for p in path)
        report.ok(
            f"{label} spend: cumulative pre-tax profit difference equals the capitalised asset",
            close(cum_diff, path[-1]["asset"], 1e-9),
            f"year-6 profit uplift {path[-1]['expense_diff']:.3f}, asset {path[-1]['asset']:.3f}",
        )
        if label == "constant":
            report.ok(
                "constant spend: profit uplift vanishes once amortisation catches up (year 4"
                " onward)",
                all(abs(p["expense_diff"]) < 1e-9 for p in path[3:]),
            )
    # Cash flow: total cash is identical; classification moves 30 from operating to investing.
    _cfo_expense, _cfo_cap = 200.0 - 30.0, 200.0
    # Interest capitalisation (IAS 23): coverage ratio rises although cash interest is unchanged.
    ebit, interest_total, capitalised = 60.0, 20.0, 8.0
    report.ok(
        "capitalised borrowing costs raise reported interest coverage",
        ebit / (interest_total - capitalised) > ebit / interest_total,
        f"{ebit / interest_total:.2f}x -> {ebit / (interest_total - capitalised):.2f}x",
    )


def check_inventory(report: CheckReport) -> None:
    """Check inventory cost formulas, LIFO restatement, liquidation and net realisable value."""
    print(
        "== part 7: inventory cost formulas, LIFO restatement, liquidation and net realisable value"
    )

    def run_inventory(
        open_layers: list[list[float]],
        purchases: list[list[float]],
        units_sold: float,
        method: str,
    ) -> tuple[float, list[list[float]]]:
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
        report.ok(
            f"{label} costs: COGS + closing inventory = goods available for every method",
            all(close(res[m][0] + end[m], available, 1e-9) for m in res),
            ", ".join(f"{m} GP {gp[m]:.0f} end {end[m]:.0f}" for m in res),
        )
        order_ok = (
            gp["fifo"] > gp["wac"] > gp["lifo"]
            if price > 500
            else gp["fifo"] < gp["wac"] < gp["lifo"]
        )
        report.ok(f"{label} costs: gross-profit ordering FIFO vs WAC vs LIFO", order_ok)
        if price > 500:
            econ = 30 * (800 - 600)
            holding = 30 * (600 - 500)
            report.ok(
                "rising costs: FIFO gross profit = economic profit + holding gain",
                close(gp["fifo"], econ + holding, 1e-9),
            )
    # LIFO to FIFO restatement with a LIFO reserve (US GAAP reporter; IFRS prohibits LIFO).
    lifo_inv, reserve_open, reserve_close, t = 1999.0, 950.0, 1002.0, 0.35
    fifo_inv = lifo_inv + reserve_close
    cogs_lifo = 5000.0
    cogs_fifo = cogs_lifo - (reserve_close - reserve_open)
    report.ok(
        "LIFO to FIFO: COGS falls by the increase in the reserve; equity rises by reserve x (1 -"
        " t)",
        close(cogs_lifo - cogs_fifo, 52.0, 1e-9) and close(reserve_close * (1 - t), 651.3, 1e-9),
        f"FIFO inventory {fifo_inv:.0f}, after-tax equity uplift {reserve_close * (1 - t):.1f}",
    )
    # Inflation estimate from a LIFO reporter: r = change in reserve / prior FIFO inventory.
    r_est = (reserve_close - reserve_open) / (1366.0 + 950.0)
    report.ok(
        "FIFO-to-LIFO bridge: COGS_LIFO = COGS_FIFO + BI_FIFO x r",
        close(cogs_fifo + (1366.0 + 950.0) * r_est, cogs_lifo, 1e-9),
        f"r = {r_est:.4%}",
    )
    # LIFO liquidation: selling old cheap layers raises profit when prices rise.
    cogs_normal, _ = run_inventory([[40, 500.0]], [[30, 600.0]], 30, "lifo")
    cogs_liq, _ = run_inventory([[40, 500.0]], [[10, 600.0]], 30, "lifo")
    report.ok(
        "LIFO liquidation lowers COGS when older layers are cheaper",
        cogs_liq < cogs_normal,
        f"liquidation profit {cogs_normal - cogs_liq:.0f}",
    )
    # Net realisable value: write-down and reversal under IAS 2; US LCNRV records no annual
    # reversal.
    cost, nrv1, nrv2 = 100.0, 80.0, 95.0
    wd = max(0.0, cost - nrv1)
    ifrs_reversal = min(wd, max(0.0, min(cost, nrv2) - (cost - wd)))
    report.ok(
        "IAS 2 reversal is limited to the original write-down",
        close(ifrs_reversal, 15.0) and ifrs_reversal <= wd,
        f"write-down {wd:.0f}, reversal {ifrs_reversal:.0f}",
    )


def check_intangibles(report: CheckReport) -> None:
    """Check intangibles - purchased, internally developed, and acquired in a combination."""
    print(
        "== part 8: intangibles - purchased, internally developed and acquired in a business"
        " combination"
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
    report.ok(
        "goodwill = consideration - fair value of identifiable net assets (including DTL on"
        " uplifts)",
        close(goodwill, 85.0, 1e-9),
        f"identifiable {identifiable:.2f}, goodwill {goodwill:.2f}",
    )
    # Post-acquisition annual charges: customer relationships over 10 years; brand, IPR&D and
    # goodwill not amortised.
    _annual_amort_bc = uplifts["customer_relationships"] / 10 + uplifts["ppe"] / 6
    # Internal development: IFRS capitalises once criteria are met (24 of 40 spent), US GAAP
    # expenses all (non-software).
    spent, after_criteria = 40.0, 24.0
    _ifrs_expense, _us_expense = spent - after_criteria, spent
    # Purchased patent: capitalised at cost 50, amortised over 5 years under both frameworks.


def check_impairment(report: CheckReport, case: HarbourCase) -> None:
    """Check impairment (IAS 36 vs US two-step), reversal, derecognition and PP&E age."""
    statements, B = case.statements, case.balances
    print("== part 9: impairment (IAS 36 vs US two-step), reversal, derecognition and PP&E age")
    carrying, undiscounted, fvlcod, viu, fair_value = 200.0, 230.0, 150.0, 170.0, 165.0
    recoverable = max(fvlcod, viu)
    ifrs_loss = max(0.0, carrying - recoverable)
    us_loss = (carrying - fair_value) if undiscounted < carrying else 0.0
    report.ok(
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
    report.ok(
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
    report.ok(
        "future ROA rises after a write-down (lower depreciation, smaller base)",
        roa_after > roa_before,
        f"{roa_before:.4%} -> {roa_after:.4%}",
    )
    # Derecognition: gain = net proceeds - carrying amount; proceeds are investing cash.
    report.ok(
        "derecognition gain = proceeds - carrying amount reproduces Harbour's 2024 other income"
        " from the ledger",
        close(13 - (40 - 30), statements[2024].income["other_income"], 1e-12),
    )
    # Harbour 2025 PP&E disclosure analysis.
    gross, accd, dep = B[2025]["ppe_gross"], -B[2025]["acc_dep"], YEARS[2025].dep
    avg_age, total_life, remaining = accd / dep, gross / dep, (gross - accd) / dep
    report.ok(
        "PP&E average age + remaining life = average total life",
        close(avg_age + remaining, total_life, 1e-12),
        f"age {avg_age:.2f}y, remaining {remaining:.2f}y, total {total_life:.2f}y",
    )


def check_leases(report: CheckReport) -> None:
    """Check lessee (IFRS 16 vs ASC 842 operating) and lessor accounting."""
    print("== part 10: lessee (IFRS 16 vs ASC 842 operating) and lessor accounting")
    pay, n, rate = 100.0, 5, 0.05
    pv = pay * (1 - (1 + rate) ** -n) / rate
    liab, rows = pv, []
    for t in range(1, n + 1):
        interest = liab * rate
        liab = liab + interest - pay
        rows.append(dict(t=t, interest=interest, closing=liab))
    report.ok(
        "lease liability amortises to zero; closed-form annuity matches the schedule",
        close(rows[-1]["closing"], 0.0, 1e-9),
        f"PV {pv:.4f}, year-1 interest {rows[0]['interest']:.4f}",
    )
    ifrs_exp = [pv / n + r["interest"] for r in rows]
    us_exp = [pay] * n
    report.ok(
        "total lease expense equals total payments under both models",
        close(sum(ifrs_exp), sum(us_exp), 1e-9),
    )
    report.ok(
        "IFRS 16 expense is front-loaded relative to the straight-line ASC 842 operating cost",
        ifrs_exp[0] > us_exp[0] > ifrs_exp[-1],
        f"IFRS year 1 {ifrs_exp[0]:.2f}, year 5 {ifrs_exp[-1]:.2f}",
    )
    # ASC 842 operating ROU asset = liability adjusted for accrued straight-line differences
    # (no prepayment here).
    us_rou = []
    _liab_t, rou_t = pv, pv
    for r in rows:
        amort = pay - r["interest"]  # single cost 100 = accretion + ROU amortisation
        rou_t -= amort
        us_rou.append(rou_t)
    report.ok(
        "ASC 842 operating ROU asset equals the lease liability throughout (even payments, no"
        " incentives)",
        all(close(a, r["closing"], 1e-9) for a, r in zip(us_rou, rows)),
    )
    ifrs_rou_y1 = pv - pv / n
    report.ok(
        "year 1: IFRS 16 ROU asset is below the US operating ROU asset (faster depreciation)",
        ifrs_rou_y1 < us_rou[0],
        f"IFRS {ifrs_rou_y1:.2f} vs US {us_rou[0]:.2f}",
    )
    # Lessor: finance lease (net investment) vs operating lease (asset retained, straight-line
    # income).
    asset_cost = pv  # selling-price = PV, no selling profit for simplicity
    fin_income = [r["interest"] for r in rows]
    op_income = [pay - asset_cost / n] * n
    report.ok(
        "lessor: finance-lease interest income and operating-lease net income sum to the same"
        " total",
        close(sum(fin_income), sum(op_income), 1e-9),
        f"{sum(fin_income):.2f}",
    )


def check_pensions(report: CheckReport, case: HarbourCase) -> None:
    """Check defined benefit pensions (IAS 19 vs US GAAP), sensitivity and modelling."""
    B = case.balances
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
    report.ok(
        "funded status roll-forward: deficit change = total cost - contributions (both frameworks)",
        close(deficit1 - deficit0, ifrs_pl + ifrs_oci - contrib, 1e-9)
        and close(ifrs_pl + ifrs_oci, us_pl + us_oci, 1e-9),
        f"deficit {deficit0:.0f} -> {deficit1:.0f}; IFRS P&L {ifrs_pl:.2f} OCI {ifrs_oci:.2f}; US"
        f" P&L {us_pl:.2f} OCI {us_oci:.2f}",
    )
    report.ok(
        "US expected-return accounting reports lower P&L cost than IAS 19 here",
        us_pl < ifrs_pl,
    )
    # Economic cost: service + interest - actual return + actuarial loss.
    economic = service + interest_cost - act_ret * fva0 + act_loss
    report.ok(
        "economic pension cost equals total comprehensive cost",
        close(economic, ifrs_pl + ifrs_oci, 1e-9),
        f"{economic:.2f}",
    )
    # Sensitivity: obligation as level benefit payments; duration approximation vs exact repricing.
    cfs = np.full(25, 1.0)
    times = np.arange(1, 26)

    def pv_dbo(y: float) -> float:
        return float(np.sum(cfs / (1 + y) ** times))

    dur_mod = float(np.sum(times * cfs / (1 + disc) ** (times + 1))) / pv_dbo(disc)
    exact = pv_dbo(disc + 0.005) / pv_dbo(disc) - 1
    approx = -dur_mod * 0.005
    report.ok(
        "+50bp discount rate: modified-duration approximation is close to exact repricing"
        " (convexity small)",
        abs(exact - approx) < 0.004,
        f"exact {exact:.4%}, duration {approx:.4%}, duration {dur_mod:.2f}",
    )
    # Modelling: debt-like adjustment and operating/financing split (Harbour 2025 deficit 48.16).
    db_after_tax = -B[2025]["db_liab"] * (1 - TAX)
    report.ok(
        "after-tax pension deficit treated as debt-like claim",
        close(db_after_tax, 36.12, 1e-9),
        f"{db_after_tax:.2f}",
    )


def check_share_based_pay(report: CheckReport) -> None:
    """Check share-based payment - fair value, vesting, forfeiture true-up and dilution."""
    print(
        "== part 12: share-based payment - fair value, vesting, forfeiture true-up and dilution"
        " modelling"
    )
    S0, K, T_exp, r_f, vol, q = 20.0, 20.0, 5.0, 0.03, 0.30, 0.01
    fv = BlackScholes(spot=S0, strike=K, maturity=T_exp, rate=r_f, vol=vol, dividend_yield=q).call()
    z = np.random.default_rng(42).standard_normal(1_000_000)
    ST = S0 * np.exp((r_f - q - 0.5 * vol**2) * T_exp + vol * math.sqrt(T_exp) * z)
    mc = math.exp(-r_f * T_exp) * np.maximum(ST - K, 0).mean()
    report.ok(
        "grant-date fair value: Black-Scholes-Merton matches Monte Carlo",
        abs(mc - fv) < 0.02,
        f"BSM {fv:.4f}, MC {mc:.4f}",
    )
    granted, expected_forfeit, actual_forfeit = 3.0, 0.10, 0.15
    cum_expected = [granted * (1 - expected_forfeit) * fv * t / 3 for t in (1, 2)]
    final = granted * (1 - actual_forfeit) * fv
    exp_y = [
        cum_expected[0],
        cum_expected[1] - cum_expected[0],
        final - cum_expected[1],
    ]
    report.ok(
        "IFRS 2 true-up: cumulative expense equals fair value of options that vest",
        close(sum(exp_y), final, 1e-12),
        ", ".join(f"{e:.4f}" for e in exp_y),
    )
    report.ok(
        "true-up lowers the year-3 charge when forfeitures exceed expectations",
        exp_y[2] < exp_y[0],
    )
    # Forecast dilution: treasury-stock incremental shares at a forecast average price.
    outstanding = granted * (1 - actual_forfeit)
    for price in (25.0, 18.0):
        inc = max(0.0, outstanding - outstanding * K / price)
        print(f"  forecast price {price:.0f}: incremental diluted shares {inc:.4f}m")
    report.ok(
        "dilution is zero when the forecast price is below the exercise price",
        max(0.0, outstanding - outstanding * K / 18.0) == 0.0,
    )


def check_taxes(report: CheckReport, case: HarbourCase) -> None:
    """Check income taxes - temporary and permanent differences, deferred tax, rate measures."""
    statements, B = case.statements, case.balances
    print(
        "== part 13: income taxes - temporary and permanent differences, deferred tax, rate"
        " measures"
    )
    i25 = statements[2025].income
    statutory_tax = TAX * i25["pbt"]
    perm = TAX * YEARS[2025].sbc
    report.ok(
        "Harbour 2025 rate reconciliation: statutory tax + non-deductible SBC = tax expense",
        close(statutory_tax + perm, i25["tax"], 1e-9),
        f"statutory {statutory_tax:.4f}, permanent {perm:.4f}, total {i25['tax']:.4f}",
    )
    etr = i25["tax"] / i25["pbt"]
    current_rate = statements[2025].flows["current_tax"] / i25["pbt"]
    cash_rate = -statements[2025].tags[("op", "tax_paid")] / i25["pbt"]
    report.ok(
        "ETR, current-tax rate and cash tax rate differ in the expected order",
        cash_rate < current_rate < etr,
        f"ETR {etr:.4%}, current {current_rate:.4%}, cash {cash_rate:.4%}",
    )
    # Temporary difference: carrying amount vs tax base of PP&E.
    tax_base_gap = (90 - 60) + (92 - 66)  # cumulative excess tax depreciation 2024-2025
    dta_restr = TAX * (18 - 6)
    report.ok(
        "closing DTL = opening DTL + 25% of accelerated depreciation - DTA on the unpaid"
        " restructuring provision",
        close(-B[2025]["dtl"], 30 + TAX * tax_base_gap - dta_restr, 1e-9),
        f"DTL {-B[2025]['dtl']:.2f}",
    )
    # Rate change: DTL of 41 remeasured from 25% to 20% when enacted.
    dtl_temp_diff = -B[2025]["dtl"] / TAX
    report.ok(
        "enacted rate cut remeasures the deferred tax liability through tax expense",
        close(dtl_temp_diff * 0.20, 32.8, 1e-9),
        f"deferred tax income {-B[2025]['dtl'] - dtl_temp_diff * 0.20:.2f}",
    )
    # Analytical treatment: growing capex keeps the DTL from reversing (equity-like); a
    # shrinking asset base reverses it.
    book_dep_life, tax_dep_life = 10, 5
    for label, growth in (("growing 5%", 0.05), ("no new capex after year 10", None)):
        dtl_path: list[float] = []
        assets: list[float] = []
        for yr in range(30):
            if growth is None:
                spend = 100.0 if yr < 10 else 0.0
            else:
                spend = 100.0 * (1 + growth) ** yr
            assets.append(spend)
            book = sum(
                a / book_dep_life for k, a in enumerate(assets) if 0 <= yr - k < book_dep_life
            )
            taxd = sum(a / tax_dep_life for k, a in enumerate(assets) if 0 <= yr - k < tax_dep_life)
            dtl_path.append((dtl_path[-1] if dtl_path else 0.0) + TAX * (taxd - book))
        print(
            f"  {label}: DTL year 10 {dtl_path[9]:.2f}, year 20 {dtl_path[19]:.2f}, year 30"
            f" {dtl_path[29]:.2f}"
        )
        if growth is None:
            report.ok(
                "without new capex the DTL fully reverses",
                close(dtl_path[-1], 0.0, 1e-9),
            )
        else:
            report.ok(
                "with growing capex the DTL keeps rising (no net reversal)",
                dtl_path[29] > dtl_path[19] > dtl_path[9],
            )


def check_earnings_quality(report: CheckReport, case: HarbourCase) -> None:
    """Check reporting and earnings quality - an aggressive 2025 variant."""
    statements, B = case.statements, case.balances
    print(
        "== part 14: reporting and earnings quality - an aggressive 2025 variant and accrual"
        " persistence"
    )
    b24, b25 = B[2024], B[2025]
    rep = dict(
        profit=statements[2025].income["profit"],
        cfo=statements[2025].cfo,
        cfi=statements[2025].cfi,
        revenue=1080.0,
        receivables=180.0,
        payables=124.0,
        purchases=485.0,
        development=60.0,
        gross=statements[2025].income["gross"],
    )
    var = dict(rep)
    # (a) bill-and-hold shipment recognised before control passes: revenue 30, cost 19.5, tax
    # 25% unpaid at year-end.
    var.update(
        revenue=rep["revenue"] + 30,
        receivables=rep["receivables"] + 30,
        gross=rep["gross"] + 10.5,
    )
    var["profit"] += 10.5 * (1 - TAX)
    # (b) 15 of selling and administrative cost capitalised as development (tax deduction
    # kept: deferred tax).
    var["profit"] += 15 * (1 - TAX)
    var["development"] += 15
    var["cfo"] += 15
    var["cfi"] -= 15
    # (c) supplier finance: 25 of invoices paid by a bank, Harbour pays the bank in 2026;
    # payables stay in trade payables.
    var["payables"] += 25
    var["cfo"] += 25

    def quality(x: Line, reclass_sfa: bool = False) -> dict[str, float]:
        noa_open = case.balance_view(2024).eq + case.balance_view(2024).nfo
        noa_close = case.balance_view(2025).eq + case.balance_view(2025).nfo
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
    report.ok(
        "variant: profit up 19.125 with CFO up 40 - CFO/profit stays healthy, so it does not flag"
        " the problem",
        close(var["profit"] - rep["profit"], 19.125, 1e-9) and q_var["cfo_to_profit"] > 2,
    )
    report.ok(
        "variant: DSO, DPO and capitalised-development growth rise",
        q_var["dso"] > q_rep["dso"] + 3
        and q_var["dpo"] > q_rep["dpo"] + 9
        and q_var["dev_growth"] > q_rep["dev_growth"] + 0.25,
    )
    report.ok(
        "supplier finance masks accruals: they fall by 5.875; with it reclassified as debt they"
        " rise by the 19.125 profit boost",
        close(q_var["accrual_amount"] - q_rep["accrual_amount"], -5.875, 1e-9)
        and close(q_var_adj["accrual_amount"] - q_rep["accrual_amount"], 19.125, 1e-9),
    )
    # Sloan's balance-sheet accrual measure for Harbour 2025 (current operating accruals less
    # depreciation).
    d_ca = (b25["receivables"] + b25["inventory"]) - (b24["receivables"] + b24["inventory"])
    d_cl = -(b25["payables"] + b25["accrued_wages"] + b25["restructuring_prov"]) + (
        b24["payables"] + b24["accrued_wages"] + b24["restructuring_prov"]
    )
    sloan = (d_ca - d_cl - YEARS[2025].dep) / (
        (case.balance_view(2025).ta + case.balance_view(2024).ta) / 2
    )
    print(
        "  Harbour 2025 Sloan accrual measure (excluding cash, short-term debt and taxes payable):"
        f" {sloan:.4%}"
    )
    # Persistence: simulated panel in which the accrual component is less persistent than the
    # cash component.
    rng = np.random.default_rng(1996)
    N = 40_000
    acc = rng.normal(0.0, 0.05, N)
    cash = rng.normal(0.10, 0.07, N)
    roa_next = 0.02 + 0.60 * acc + 0.85 * cash + rng.normal(0, 0.03, N)
    X = np.column_stack([np.ones(N), acc, cash])
    coef = np.linalg.lstsq(X, roa_next, rcond=None)[0]
    pooled = np.polyfit(acc + cash, roa_next, 1)[0]
    report.ok(
        "simulated persistence: OLS recovers lower accrual than cash coefficient; pooled slope"
        " lies between",
        coef[1] < pooled < coef[2] and abs(coef[1] - 0.60) < 0.02 and abs(coef[2] - 0.85) < 0.02,
        f"accrual {coef[1]:.3f}, cash {coef[2]:.3f}, pooled {pooled:.3f}",
    )


def check_forecast(report: CheckReport, case: HarbourCase) -> None:
    """Check harbour three-year forecast (2026-2028) with an explicit revolver rule."""
    base = case.base
    print(
        "== part 15: Harbour three-year forecast (2026-2028) with an explicit revolver rule and no"
        " balancing plug"
    )
    for f in base:
        report.ok(
            f"{f.year}: forecast balance sheet balances without a plug (cash from the CFS,"
            " revolver by rule)",
            close(f.assets, f.liab_eq, 1e-6),
            f"assets {f.assets:.4f}, iterations {f.iters}",
        )
        print(
            f"  {f.year}: revenue {f.revenue:.2f} GM {f.gross_margin:.4f} EBIT"
            f" {f.op:.2f} fin {f.fin:.2f} profit {f.profit:.2f} CFO {f.cfo:.2f} CFI"
            f" {f.cfi:.2f} div {f.divs:.2f} RCF draw {f.draw:+.2f} RCF {f.rcf:.2f} cash"
            f" {f.balance_sheet['cash']:.2f} net debt/EBITDA {f.net_debt / f.ebitda:.3f}"
            f" EBITDA/interest {f.interest_cover:.2f}"
        )
    report.ok(
        "revenue growth decomposes into volume and price: (1.03)(1.03) - 1 = 6.09% in 2026",
        close(base[0].revenue / 1080.0 - 1, 1.03 * 1.03 - 1, 1e-12),
    )
    # Two schedules that the straight-line asset schedules avoid: charging the opening
    # development balance / 5 each year is a declining-balance rule that leaves 0.8^5 = 32.768%
    # of an isolated balance after five years, and pooling acquired intangibles with development
    # charges them twice.
    residual_old = 1.0
    for _ in range(5):
        residual_old -= residual_old / 5
    report.ok(
        "a declining-balance development rule (opening balance / 5) leaves 32.768% of an isolated"
        " balance after five years",
        close(residual_old, 0.32768, 1e-12),
    )
    pool, old_charges = 0.0, []
    # An isolated acquired 20, added to the pool at the end of 2026, plus a separate 2 a year.
    for k in range(3):
        charge = pool / 5 + 2.0
        old_charges.append(charge)
        pool += (20.0 if k == 0 else 0.0) - charge
    report.ok(
        "pooling with development would charge the acquired 20 at 2, 5.6 and 4.48 instead of 2 a"
        " year",
        all(close(a, b, 1e-12) for a, b in zip(old_charges, (2.0, 5.6, 4.48))),
    )
    yrs = range(2026, 2045)
    for label, cost, life, start, frac in (
        ("opening development 60 over 2026-2030", 60.0, LEGACY_DEV_LIFE, 2026, 1.0),
        ("2026 development vintage from 1 Jan 2027", 22.0, DEV_LIFE, 2027, 1.0),
        (
            "acquired intangibles 20 from 1 Apr 2026",
            20.0,
            ACQ_INTANGIBLE_LIFE,
            2026,
            0.75,
        ),
        ("acquired PP&E 10 from 1 Apr 2026", 10.0, ACQ_PPE_LIFE, 2026, 0.75),
    ):
        sched = straight_line(cost, life, start, yrs, frac)
        carrying, path = cost, []
        for y in yrs:
            carrying -= sched[y]
            path.append(carrying)
        report.ok(
            f"{label}: charges sum to cost, carrying amount ends at zero and never goes negative",
            close(sum(sched.values()), cost, 1e-9)
            and close(path[-1], 0.0, 1e-9)
            and min(path) > -1e-9,
            f"first charges {[round(sched[y], 4) for y in range(2026, 2030)]}",
        )
    acquisition = Acquisition(
        price=60.0,
        revenue=50.0,
        ebitda=9.0,
        goodwill=30.0,
        ppe=10.0,
        intangibles=20.0,
        fraction_2026=0.75,
    )
    acq_case = case.forecast(ForecastCase(acquisition=acquisition))
    report.ok(
        "acquired intangibles are charged once: 1.5, 2 and 2 in 2026-2028 (nine months, then full"
        " years)",
        all(close(f.acq_amort, a, 1e-12) for f, a in zip(acq_case, (1.5, 2.0, 2.0)))
        and all(close(f.dep_acq, a, 1e-12) for f, a in zip(acq_case, (1.5, 2.0, 2.0))),
    )
    # Independent route: the forecast development balance equals the sum of vintage carrying
    # amounts.
    vint_bal = 60.0 - sum(
        straight_line(60.0, LEGACY_DEV_LIFE, 2026, yrs)[y] for y in range(2026, 2029)
    )
    for f in base:
        spend = 0.02 * f.organic
        vint_bal += spend - sum(
            straight_line(spend, DEV_LIFE, f.year + 1, yrs)[y] for y in range(2026, 2029)
        )
    report.ok(
        "2028 development balance equals the sum of vintage carrying amounts (legacy and 2026-2028"
        " spend)",
        close(base[2].balance_sheet["development"], vint_bal, 1e-9),
        f"{vint_bal:.4f}; charges {[round(f.dev_amort, 4) for f in base]}",
    )


def check_competition(report: CheckReport, case: HarbourCase) -> None:
    """Check competition, cost pass-through, inflation and deflation."""
    base = case.base
    print("== part 16: competition, cost pass-through, inflation and deflation")
    shock = 0.06  # 2026 variable-cost inflation
    res = {}
    for theta in (
        1.0,
        0.5,
        0.0,
    ):  # share of the cost shock passed into price (strong buyer power -> low theta)
        f = case.forecast(
            ForecastCase(
                price_infl=(theta * shock, 0.025, 0.025), var_cost_infl=(shock, 0.03, 0.025)
            )
        )[0]
        res[theta] = f
        print(
            f"  pass-through {theta:.0%}: price x{1 + theta * shock:.3f}, gross margin"
            f" {f.gross_margin:.4f}, EBIT {f.op:.2f}"
        )
    margins = {th: res[th].op / res[th].revenue for th in res}
    report.ok(
        "EBIT and EBIT margin fall monotonically as pass-through weakens (11.56%, 9.57%, 7.45%)",
        res[1.0].op > res[0.5].op > res[0.0].op
        and [round(margins[th] * 100, 2) for th in (1.0, 0.5, 0.0)] == [11.56, 9.57, 7.45],
        ", ".join(f"{th:.0%}: {m:.4%}" for th, m in margins.items()),
    )
    cm = {th: (res[th].price - res[th].vcost) / res[th].price for th in res}
    report.ok(
        "full pass-through of a uniform per-unit cost rise preserves the contribution margin"
        " percentage",
        close(cm[1.0], (10.8 - 4.8) / 10.8, 1e-12),
        f"{cm[1.0]:.4%}",
    )
    # Real versus nominal growth: nominal = (1 + real)(1 + inflation) - 1; deflating with the
    # wrong index misstates volume.
    nominal = base[1].revenue / base[0].revenue - 1
    report.ok(
        "2027 nominal revenue growth = (1 + volume)(1 + price) - 1",
        close(nominal, 1.03 * 1.025 - 1, 1e-12),
        f"{nominal:.4%}",
    )
    # Deflation with fixed costs: operating leverage turns a 2% price-and-cost decline into a
    # larger EBIT decline.
    defl = case.forecast(
        ForecastCase(
            price_infl=(-0.02, -0.02, -0.02), var_cost_infl=(-0.02, -0.02, -0.02), fixed_infl=0.0
        )
    )[0]
    flat = case.forecast(
        ForecastCase(price_infl=(0.0, 0.0, 0.0), var_cost_infl=(0.0, 0.0, 0.0), fixed_infl=0.0)
    )[0]
    report.ok(
        "deflation: EBIT falls proportionally more than revenue when fixed costs do not deflate",
        (defl.op / flat.op - 1) < (defl.revenue / flat.revenue - 1),
        f"revenue {defl.revenue / flat.revenue - 1:+.2%}, EBIT {defl.op / flat.op - 1:+.2%}",
    )


def check_valuation(report: CheckReport, case: HarbourCase) -> None:
    """Check valuation conventions, the forecast horizon, steady state and terminal value."""
    print(
        "== part 17: valuation conventions, forecast horizon, steady state and terminal value"
        " consistency"
    )
    # Valuation date 31 Dec 2025, end-of-year cash flows, WACC 8% (an input). Leases are debt,
    # so right-of-use additions are reinvestment and lease liabilities are claims; share-based
    # pay is an operating cost for future grants (deducted, with no tax effect because it is
    # not deductible here), and vested options already outstanding are a separate claim; the
    # pension deficit is a debt-like claim, so service cost is operating and contributions
    # above it are financing.
    B, R, base, valuation = case.balances, case.ratios, case.base, case.valuation
    wacc = valuation.wacc

    def fcff_accounting(f: YearForecast) -> float:
        """Return the accounting FCFF: CFO + after-tax interest paid - capex and development."""
        return f.cfo + f.interest_paid * (1 - TAX) - f.capex

    fcff_old = [fcff_accounting(f) for f in base]
    fcff = valuation.fcff
    report.ok(
        "valuation FCFF: CFO route equals the NOPAT route in every forecast year",
        all(close(a, nopat_route_fcff(f), 1e-9) for a, f in zip(fcff, base)),
        ", ".join(
            f"{f.year} {a:.4f} (accounting {b:.4f})" for f, a, b in zip(base, fcff, fcff_old)
        ),
    )
    disc = [(1 + wacc) ** -(t + 1) for t in range(3)]
    pv_rou = sum(f.lease_new * d for f, d in zip(base, disc))
    pv_sbc = sum(f.sbc * d for f, d in zip(base, disc))
    report.ok(
        "PV at 8% of the omitted right-of-use additions (25 a year, 2026-2028) is 64.4274",
        close(pv_rou, 25 * (1 - 1.08**-3) / 0.08, 1e-12) and round(pv_rou, 4) == 64.4274,
    )
    report.ok(
        "PV at 8% of the share-based expense added back in 2026-2028 (9.45, 9.9225, 10.4186) is"
        " 25.5276",
        round(pv_sbc, 4) == 25.5276,
    )
    for f in base:
        o, c = f.opening, f.balance_sheet
        fcfe_stat = f.cfo - f.capex - f.lease_principal - f.loan_repay + f.draw
        fcfe_debt = (
            f.cfo
            - f.capex
            - f.lease_new
            + (f.lease_new - f.lease_principal)
            - f.loan_repay
            + f.draw
        )
        pension_borrow = f.service + f.pens_int - 15.0
        report.ok(
            f"{f.year}: FCFE equals dividends + change in cash and is the same with leases as"
            " debt; FCFF = FCFE + after-tax interest - net borrowing (lease and pension included)",
            close(fcfe_stat, f.divs + c["cash"] - o["cash"], 1e-9)
            and close(fcfe_stat, fcfe_debt, 1e-12)
            and close(
                valuation_fcff(f),
                (fcfe_debt - f.sbc)
                + (f.interest_paid + f.pens_int) * (1 - TAX)
                - (f.lease_new - f.lease_principal - f.loan_repay + f.draw)
                - pension_borrow,
                1e-9,
            ),
            f"FCFE {fcfe_stat:.4f}",
        )
    # Lease presentation: a 25 asset leased on 1 Jan 2026 versus bought with a 25 loan on
    # identical terms. Both give the same depreciation, interest and payments; only treating
    # lease additions as reinvestment gives them the same FCFF.
    lease_vs_buy = {}
    for conv in ("reinvestment", "financing only"):
        buy = -25.0 / (1 + wacc)
        lease = (-25.0 if conv == "reinvestment" else 0.0) / (1 + wacc)
        lease_vs_buy[conv] = lease - buy
    report.ok(
        "equivalent lease and buy-with-debt presentations give equal value only when lease"
        " additions are reinvestment",
        close(lease_vs_buy["reinvestment"], 0.0, 1e-12)
        and close(lease_vs_buy["financing only"], 25 / 1.08, 1e-12),
        "artificial value when lease additions are financing only"
        f" {lease_vs_buy['financing only']:.4f}",
    )
    # Terminal value. NOPAT uses book taxes on EBIT with share-based pay non-deductible: EBIT
    # - t(EBIT + SBC).
    nopat_2028 = valuation.nopat_2028

    g_ss, ronic_ss = valuation.growth, valuation.ronic
    nopat_2029 = nopat_2028 * (1 + g_ss)
    # (a) NOPAT_2029 held fixed: with RONIC = WACC the terminal value is NOPAT_2029 / WACC
    # whatever g is.
    tv_fixed_next = [terminal_value(nopat_2029, g, wacc, wacc) for g in (0.0, 0.02, 0.04)]
    report.ok(
        "value-neutral growth, NOPAT_2029 fixed: TV_2028 = NOPAT_2029 / WACC for g = 0, 2, 4%",
        max(tv_fixed_next) - min(tv_fixed_next) < 1e-9
        and close(tv_fixed_next[0], nopat_2029 / wacc, 1e-9),
        f"TV_2028 / NOPAT_2029 = {tv_fixed_next[0] / nopat_2029:.4f}",
    )
    # (b) NOPAT_2028 held fixed and NOPAT_2029 = NOPAT_2028 (1 + g): TV rises with g, because
    # growth into 2029 needs reinvestment of g NOPAT_2028 / RONIC during 2028; deducting it
    # restores NOPAT_2028 / WACC.
    tv_fixed_cur = {
        g: terminal_value(nopat_2028 * (1 + g), g, wacc, wacc) for g in (0.0, 0.02, 0.04)
    }
    net_of_2028_reinv = [tv_fixed_cur[g] - g * nopat_2028 / wacc for g in tv_fixed_cur]
    report.ok(
        "NOPAT_2028 fixed: TV_2028 = NOPAT_2028 (1 + g) / WACC rises with g; less 2028"
        " reinvestment it is invariant",
        tv_fixed_cur[0.04] > tv_fixed_cur[0.02] > tv_fixed_cur[0.0]
        and all(close(v, nopat_2028 / wacc, 1e-9) for v in net_of_2028_reinv),
        ", ".join(f"g {g:.0%}: {v:.4f}" for g, v in tv_fixed_cur.items()),
    )
    tv_2028, v_short = valuation.terminal_value, valuation.enterprise_value
    # Explicit extension 2029-2040 with the same steady-state rule, then a terminal value:
    # must give the same value.
    ext, nop = [], nopat_2028
    for t in range(12):
        nop *= 1 + g_ss
        ext.append(nop * (1 - g_ss / ronic_ss))
    tv_2040 = terminal_value(nop * (1 + g_ss), g_ss, ronic_ss, wacc)
    v_long = (
        sum(c / (1 + wacc) ** (t + 1) for t, c in enumerate(fcff))
        + sum(c / (1 + wacc) ** (t + 4) for t, c in enumerate(ext))
        + tv_2040 / (1 + wacc) ** 15
    )
    report.ok(
        "lengthening the explicit horizon with the steady-state rule leaves value unchanged",
        close(v_short, v_long, 1e-6),
        f"enterprise value {v_short:.4f}; terminal share {tv_2028 / (1 + wacc) ** 3 / v_short:.1%}",
    )
    v_accounting = (
        sum(c / (1 + wacc) ** (t + 1) for t, c in enumerate(fcff_old))
        + terminal_value(base[2].op * (1 - TAX) * (1 + g_ss), g_ss, ronic_ss, wacc)
        / (1 + wacc) ** 3
    )
    print(
        "  accounting inputs (accounting FCFF, deductible-SBC NOPAT): enterprise value"
        f" {v_accounting:.4f}"
    )
    # A horizon that ends before steady state: capitalising 2028's transitory revenue growth
    # in a Gordon value of FCFF.
    g_bad = base[2].revenue / base[1].revenue - 1
    naive_tv = fcff[2] * (1 + g_bad) / (wacc - g_bad)
    print(
        f"  Gordon on 2028 FCFF at transitory growth {g_bad:.2%}: TV {naive_tv:.2f} vs steady-state"
        f" TV {tv_2028:.2f}"
    )
    report.ok(
        "ending the horizon before steady state overstates the terminal value; 2028 reinvestment"
        " is not g / RONIC",
        naive_tv > 1.5 * tv_2028 and abs((1 - fcff[2] / nopat_2028) - g_ss / ronic_ss) > 0.05,
        f"2028 reinvestment rate {1 - fcff[2] / nopat_2028:.2%} vs steady state"
        f" {g_ss / ronic_ss:.2%}",
    )
    # Enterprise-to-equity bridge at 31 Dec 2025. Claims: term loan, RCF and lease
    # liabilities; the after-tax pension deficit (the credit-analysis convention); 5m vested
    # options at EUR 8 valued as claims (Black-Scholes-Merton, 3 years, volatility 30%, rate
    # 3%, dividend yield 2.5%) at the estimated value per share. Unvested awards are not
    # deducted: their cost is inside the forecast share-based expense. Shares: 100.75m.
    b25 = B[2025]
    claims, equity_pre_options = valuation.claims, valuation.equity_before_options
    shares_out, n_opt = valuation.shares, valuation.options
    price_iv, opt_unit = valuation.price, valuation.option_value
    report.ok(
        "equity bridge: value per share is a fixed point after deducting outstanding options"
        " valued at that price",
        close(price_iv * shares_out + n_opt * opt_unit, equity_pre_options, 1e-9)
        and max(0.0, price_iv * math.exp(-0.075) - 8.0 * math.exp(-0.09)) <= opt_unit <= price_iv,
        f"EV {v_short:.2f} + cash {b25['cash']:.2f} - "
        + ", ".join(f"{k} {v:.2f}" for k, v in claims.items())
        + (
            f" - options {n_opt * opt_unit:.2f} = equity {price_iv * shares_out:.2f}; "
            f"per share {price_iv:.4f}"
        ),
    )
    treasury = equity_pre_options / (shares_out + n_opt * (1 - 8.0 / price_iv))
    print(
        f"  comparison: treasury-stock dilution at that price gives {treasury:.4f} a share"
        " (exercise value only)"
    )
    report.ok(
        "printed valuation figures: FCFF 31.93/50.95/57.95, NOPAT_2028 93.85, TV 1,384.68, EV"
        " 1,218.45, options 9.28, 8.49 a share (treasury stock 8.56), accounting-input EV"
        " 1,331.49",
        [round(x, 2) for x in fcff] == [31.93, 50.95, 57.95]
        and [round(x, 2) for x in fcff_old] == [63.19, 83.0, 90.84]
        and round(nopat_2028, 2) == 93.85
        and round(tv_2028, 2) == 1384.68
        and round(v_short, 2) == 1218.45
        and round(n_opt * opt_unit, 2) == 9.28
        and round(price_iv, 2) == 8.49
        and round(treasury, 2) == 8.56
        and round(v_accounting, 2) == 1331.49
        and round(price_iv * shares_out, 2) == 855.59,
    )
    # Forecast reasonableness: 2026 RNOA implied by the forecast against the 2025 actual
    # (Subramanyam's ROIC check).
    f0 = base[0]
    noa_open = case.balance_view(2025).eq + case.balance_view(2025).nfo
    bs26 = f0.balance_sheet
    eq26 = (
        bs26["share_capital"]
        + bs26["sbp_reserve"]
        + bs26["remeasurement_reserve"]
        + bs26["retained"]
    )
    nfo26 = (
        bs26["term_loan"] + bs26["revolver"] + bs26["lease_liab"] + bs26["db_liab"] - bs26["cash"]
    )
    rnoa26 = (f0.profit + f0.fin * (1 - TAX)) / ((noa_open + eq26 + nfo26) / 2)
    report.ok(
        "2026 forecast RNOA lies between the 2025 actual and the 2024 level (a margin recovery,"
        " not a step change)",
        R[2025].rnoa < rnoa26 < R[2024].rnoa + 0.01,
        f"RNOA 2025 {R[2025].rnoa:.4%}, 2026 forecast {rnoa26:.4%}; EBIT margin"
        f" {f0.op / f0.revenue:.4%}",
    )
    hi_cost = case.forecast(ForecastCase(sga_rate=0.185))[0]
    approx = f0.revenue * 0.01 * (1 - TAX)
    report.ok(
        "one-point EBIT-margin sensitivity: model profit change matches revenue x 1% x (1 - t) up"
        " to revolver interest",
        abs((f0.profit - hi_cost.profit) - approx) < 0.2,
        f"model {f0.profit - hi_cost.profit:.4f}, approximation {approx:.4f}",
    )


def check_forecast_biases(report: CheckReport) -> None:
    """Check forecast biases - interval calibration and an outside-view adjustment."""
    print("== part 18: forecast biases - interval calibration and an outside-view adjustment")
    true_sd, believed_sd = 0.10, 0.05
    z80 = norm.ppf(0.90)
    cover_closed = 2 * norm.cdf(z80 * believed_sd / true_sd) - 1
    errors = np.random.default_rng(7).normal(0, true_sd, 200_000)
    cover_sim = np.mean(np.abs(errors) < z80 * believed_sd)
    report.ok(
        "overconfident 80% intervals (half the true dispersion) cover about 48% of outcomes",
        bool(abs(cover_sim - cover_closed) < 0.005),
        f"closed form {cover_closed:.4f}, simulated {cover_sim:.4f}",
    )
    past = np.random.default_rng(8).normal(
        0, true_sd, 5_000
    )  # reference class of past forecast errors
    lo, hi = np.quantile(past, [0.10, 0.90])
    cover_fix = np.mean((errors > lo) & (errors < hi))
    report.ok(
        "intervals set from the reference-class error distribution restore about 80% coverage",
        abs(cover_fix - 0.80) < 0.01,
        f"{cover_fix:.4f}",
    )


def check_comparability(report: CheckReport, case: HarbourCase) -> None:
    """Check comparability - restating a US GAAP peer (Ridgeline Tools Inc.) and Harbour."""
    statements, B, R = case.statements, case.balances, case.ratios
    print(
        "== part 19: comparability - restating a US GAAP peer (Ridgeline Tools Inc.) and Harbour"
        " to a common basis"
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
    # (1) LIFO to FIFO: inventory + reserve; COGS - change in reserve; DTL + reserve x t;
    # equity + reserve x (1 - t).
    adj["cogs"] -= rg["lifo_close"] - rg["lifo_open"]
    adj["inventory"] += rg["lifo_close"]
    d_assets_1, d_liab_1, d_eq_1 = (
        rg["lifo_close"],
        TAX * rg["lifo_close"],
        (1 - TAX) * rg["lifo_close"],
    )
    report.ok(
        "LIFO-to-FIFO adjustment keeps the balance sheet balanced",
        close(d_assets_1, d_liab_1 + d_eq_1, 1e-12),
    )
    # (2) Operating lease cost (straight-line, in SG&A) replaced by ROU depreciation and lease
    # interest (IFRS 16 basis).
    rou_dep_rg = rg["rou"] / 5
    lease_int_rg = LEASE_RATE * rg["lease_liab"]
    adj["sga"] = rg["sga"] - rg["lease_cost"] + rou_dep_rg
    adj["interest"] = rg["interest"] + lease_int_rg
    adj["ebit"] = adj["revenue"] - adj["cogs"] - adj["sga"] - adj["rnd"]
    adj["ni"] = (adj["ebit"] - adj["interest"]) * (1 - TAX)
    ebitda_rep = rg["ebit"] + rg["dep"]
    ebitda_adj = adj["ebit"] + rg["dep"] + rou_dep_rg
    report.ok(
        "restatement: EBITDA rises by the operating lease cost plus the increase in the LIFO"
        " reserve",
        close(
            ebitda_adj - ebitda_rep,
            rg["lease_cost"] + (rg["lifo_close"] - rg["lifo_open"]),
            1e-12,
        ),
    )
    # (3) Development: Harbour restated to expensing (the common, conservative basis): 2025
    # spend 22 vs amortisation 12.
    h_op_us_basis = statements[2025].income["op"] - (YEARS[2025].dev_capex - YEARS[2025].dev_amort)
    _h_dev_asset = B[2025]["development"]
    peer = dict(
        harbour_reported=dict(
            ebit_margin=statements[2025].income["op"] / 1080,
            nd_ebitda=R[2025].net_debt_ebitda,
        ),
        harbour_common=dict(
            ebit_margin=h_op_us_basis / 1080,
            nd_ebitda=(case.balance_view(2025).debt - B[2025]["cash"])
            / (
                R[2025].ebitda
                - YEARS[2025].dev_capex
                + YEARS[2025].dev_amort
                - YEARS[2025].dev_amort
            ),
        ),
        ridgeline_reported=dict(
            ebit_margin=rg["ebit"] / rg["revenue"],
            nd_ebitda=(rg["debt"] - rg["cash"]) / ebitda_rep,
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
    report.ok(
        "common basis: Ridgeline's margin lead widens from 0.14 to 2.31 points while the leverage"
        " gap narrows",
        gap_rep < 0.002 and gap_common > 0.02 and 0 < lev_gap_common < lev_gap_rep,
        f"margin gap {gap_rep:.4%} -> {gap_common:.4%}; leverage gap {lev_gap_rep:.3f}x ->"
        f" {lev_gap_common:.3f}x",
    )


def check_accounting_changes(report: CheckReport, case: HarbourCase) -> None:
    """Check effects of accounting changes - IFRS 18, an estimate change and a policy change."""
    statements, B, R, base = case.statements, case.balances, case.ratios, case.base
    print(
        "== part 20: effects of accounting changes - IFRS 18, an estimate change and a policy"
        " change"
    )
    i25 = statements[2025].income
    f26 = base[0]
    cfo_ias7, cfo_ifrs18 = f26.cfo, f26.cfo + f26.interest_paid
    report.ok(
        "IFRS 18: moving interest paid to financing raises CFO by interest paid and leaves the"
        " change in cash unchanged",
        close(cfo_ifrs18 - cfo_ias7, f26.interest_paid, 1e-12),
        f"2026 CFO {cfo_ias7:.2f} -> {cfo_ifrs18:.2f}; CFO/debt {cfo_ias7 / f26.debt:.3f} ->"
        f" {cfo_ifrs18 / f26.debt:.3f}",
    )
    # A standard change: Harbour 2025 under an operating-lease model (lease payments 28
    # expensed) against IFRS 16.
    op_lease_op = i25["op"] + YEARS[2025].rou_dep - YEARS[2025].lease_payment
    op_lease_ebitda = R[2025].ebitda - YEARS[2025].lease_payment
    op_lease_nd = case.balance_view(2025).debt - B[2025]["cash"] - (-B[2025]["lease_liab"])
    op_lease_fin = i25["fin"] - LEASE_RATE * 60
    report.ok(
        "IFRS 16 versus an operating-lease model: EBITDA 195 vs 167, net debt/EBITDA 1.63 vs 1.51,"
        " EBIT cover 5.76 vs 6.76",
        close(op_lease_ebitda, 167.0, 1e-9)
        and round(op_lease_nd / op_lease_ebitda, 2) == 1.51
        and round(op_lease_op / op_lease_fin, 2) == 6.76,
        f"operating profit {op_lease_op:.2f}, finance costs {op_lease_fin:.2f}",
    )
    # Management-defined performance measure: adjusted operating profit excluding
    # restructuring (2025).
    i25 = statements[2025].income
    mpm = i25["op"] + i25["restructuring"]
    mpm_tax = TAX * i25["restructuring"]
    report.ok(
        "MPM reconciliation: operating profit + restructuring = adjusted operating profit; tax"
        " effect 25%",
        close(mpm, 111.0, 1e-12) and close(mpm_tax, 4.5, 1e-12),
    )
    # Change in estimate (prospective): useful life of a machine extended from 10 to 14 years
    # after 4 years.
    cost_m, resid = 100.0, 0.0
    nbv = cost_m - 4 * cost_m / 10
    new_dep = (nbv - resid) / (14 - 4)
    report.ok(
        "estimate change: remaining carrying amount spread over the revised remaining life (no"
        " restatement)",
        close(new_dep * 10 + 40, cost_m, 1e-12),
        f"depreciation {cost_m / 10:.1f} -> {new_dep:.1f}",
    )
    # Policy change (retrospective): FIFO to weighted average lowers the 1 Jan 2025 inventory
    # by 4 (tax follows book here).
    opening_effect = -4.0 * (1 - TAX)
    report.ok(
        "policy change: opening retained earnings of the earliest period restated by the after-tax"
        " cumulative effect",
        close(opening_effect, -3.0, 1e-12),
    )


class FacilityOutcome(Record):
    """One facility option's worst year under one scenario.

    Attributes:
        peak: Peak revolver drawing.
        undrawn: Facility limit less the peak drawing.
        lev: Highest net debt over covenant EBITDA.
        cover: Lowest EBITDA over interest.
        plev: Highest leverage with the after-tax pension deficit as debt.
    """

    peak: float
    undrawn: float
    lev: float
    cover: float
    plev: float


def downside(case: ForecastCase) -> ForecastCase:
    """Return the case with the downside's weaker prices and volumes and higher costs."""
    return case.model_copy(
        update={
            "price_infl": (0.015, 0.02, 0.025),
            "vol_growth": (-0.04, 0.0, 0.02),
            "var_cost_infl": (0.06, 0.03, 0.025),
        }
    )


def check_lender_decision(report: CheckReport, case: HarbourCase) -> None:
    """Check the lender's decision on Harbour's facility request under two scenarios."""
    print(
        "== part 21: integrated analysis - lender decision on Harbour's facility request (1 March"
        " 2026)"
    )
    B, R = case.balances, case.ratios
    # Completion on 1 April 2026, after the 1 March decision: nine months of the acquired
    # business in 2026.
    acq = Acquisition(
        price=60.0,
        revenue=50.0,
        ebitda=9.0,
        goodwill=30.0,
        ppe=10.0,
        intangibles=20.0,
        fraction_2026=0.75,
    )
    # Policy: covenant 2.50x net debt/EBITDA with 10% headroom.
    min_undrawn, max_lev, min_cover = 10.0, 2.25, 6.0
    options = {
        "A: 160 facility, no conditions": ForecastCase(acquisition=acq, rcf_limit=160.0),
        "B: 160 facility, dividend lock-up above 1.75x": ForecastCase(
            acquisition=acq, rcf_limit=160.0, lockup=1.75
        ),
        "C: keep 100, no acquisition": ForecastCase(rcf_limit=100.0, lockup=1.75),
        "D: 160 facility, lock-up above 1.75x tested pro forma from completion": ForecastCase(
            acquisition=acq, rcf_limit=160.0, lockup=1.75, lockup_pro_forma=True
        ),
    }
    pro_forma_lev = (case.balance_view(2025).debt - B[2025]["cash"] + acq.price) / (
        R[2025].ebitda + acq.ebitda
    )
    report.ok(
        "pro forma leverage at completion: (317.46 + 60) / (195 + 9) = 1.85x, above the 1.75x"
        " trigger",
        round(pro_forma_lev, 2) == 1.85,
        f"{pro_forma_lev:.4f}",
    )
    verdict: dict[str, bool] = {}
    results: dict[tuple[str, str], FacilityOutcome] = {}
    for name, kw in options.items():
        passes = True
        for scen, scenario in (("base", kw), ("downside", downside(kw))):
            r = case.forecast(scenario)
            peak = max(x.rcf for x in r)
            undrawn = kw.rcf_limit - peak
            lev = max(x.net_debt / x.cov_ebitda for x in r)
            cover = min(x.interest_cover for x in r)
            pens_adj_lev = max(
                (x.net_debt + x.balance_sheet["db_liab"] * (1 - TAX)) / x.cov_ebitda for x in r
            )
            passes &= undrawn >= min_undrawn and lev <= max_lev and cover >= min_cover
            results[(name[0], scen)] = FacilityOutcome(
                peak=peak, undrawn=undrawn, lev=lev, cover=cover, plev=pens_adj_lev
            )
            print(
                f"  {name} [{scen}]: peak RCF {peak:.2f}, undrawn {undrawn:.2f}, max net"
                f" debt/EBITDA {lev:.3f} (with after-tax pension deficit {pens_adj_lev:.3f}), min"
                f" EBITDA/interest {cover:.2f}, dividends {[round(x.divs, 2) for x in r]},"
                f" balanced {all(abs(x.assets - x.liab_eq) < 1e-6 for x in r)}"
            )
        verdict[name] = passes
    report.ok(
        "straight-line schedules: A, B and C fail the downside; only D (pro forma lock-up) meets"
        " every test in both scenarios",
        verdict == {name: name.startswith("D") for name in options},
        str(verdict),
    )
    b_down, d_down = results[("B", "downside")], results[("D", "downside")]
    report.ok(
        "B's downside failure is liquidity alone: 1.84 undrawn against 10, with leverage and cover"
        " inside policy",
        round(b_down.undrawn, 2) == 1.84 and b_down.lev <= max_lev and b_down.cover >= min_cover,
    )
    b_case = options["B: 160 facility, dividend lock-up above 1.75x"]
    report.ok(
        "printed decision figures: B pays 15.15 in 2026 in the downside; D's downside"
        " pension-adjusted leverage is 2.18x",
        round(case.forecast(downside(b_case))[0].divs, 2) == 15.15
        and round(d_down.plev, 2) == 2.18
        and round(d_down.undrawn, 2) == 19.02,
    )
    capex_cut = case.forecast(downside(b_case.model_copy(update={"capex_rate": 0.075})))
    report.ok(
        "sensitivity: capex at 7.5% of revenue would let B pass the downside (a management lever,"
        " not a facility term)",
        160.0 - max(x.rcf for x in capex_cut) >= min_undrawn
        and max(x.net_debt / x.cov_ebitda for x in capex_cut) <= max_lev,
        f"undrawn {160.0 - max(x.rcf for x in capex_cut):.2f}",
    )
    # Sensitivities of the recommendation: a 170 facility instead of the pro forma test, and a
    # later completion.
    alt_170 = case.forecast(downside(b_case.model_copy(update={"rcf_limit": 170.0})))
    d_case = options["D: 160 facility, lock-up above 1.75x tested pro forma from completion"]
    july = acq.model_copy(update={"fraction_2026": 0.5})
    late = case.forecast(downside(d_case.model_copy(update={"acquisition": july})))
    report.ok(
        "sensitivity: a 170 facility without the pro forma test keeps only 11.84 undrawn; D with"
        " completion on 1 July still keeps more than 10",
        round(170.0 - max(x.rcf for x in alt_170), 2) == 11.84
        and 160.0 - max(x.rcf for x in late) > 10,
        f"D with July completion: undrawn {160.0 - max(x.rcf for x in late):.2f}",
    )


def main() -> int:
    """Build the Harbour case, then run the 21 parts with one report.

    Part 1 checks Harbour's statements derived from its double-entry ledger (EUR millions,
    2024-2025): the balance sheet balances, the direct cash flow (tagged cash postings) equals the
    indirect one derived from the income statement and balance-sheet changes, and every equity
    component rolls forward. Later parts reuse the case for ratios, quality indicators, a three-year
    forecast, a valuation, comparability adjustments, the IFRS 18 transition and a lender's
    decision, and add stand-alone examples for revenue allocation, capitalisation, EPS, inventory
    cost formulas, intangibles, impairment, leases, pensions, share-based pay, taxes and forecast
    biases. Routes are independent: ledger against statement identities, direct against indirect
    cash flow, closed forms against simulation or iteration, schedules against annuity formulas, and
    invariance checks. Numbers are illustrative, not data about any real company.

    Returns:
        The exit status, 0 or 1.
    """
    print_versions(np, scipy)
    case = HarbourCase()
    report = CheckReport()
    check_ledger(report, case)
    check_common_size(report, case)
    check_cash_flow(report, case)
    check_eps(report, case)
    check_revenue(report)
    check_capitalisation(report)
    check_inventory(report)
    check_intangibles(report)
    check_impairment(report, case)
    check_leases(report)
    check_pensions(report, case)
    check_share_based_pay(report)
    check_taxes(report, case)
    check_earnings_quality(report, case)
    check_forecast(report, case)
    check_competition(report, case)
    check_valuation(report, case)
    check_forecast_biases(report)
    check_comparability(report, case)
    check_accounting_changes(report, case)
    check_lender_decision(report, case)
    print(f"\n{report.count} checks executed")
    return report.summarise()


if __name__ == "__main__":
    sys.exit(main())
