"""Worked numbers of the free-cash-flow, residual-income and private-company valuation entries."""

import math
import sys
from typing import Final

import numpy as np
import scipy
from scipy.optimize import brentq

from trading_notes.numerical.company_case.harbour import (
    GROSS_DEBT,
    MARKET_PRICE,
    SHARES,
    TAX,
    YEARS,
    ForecastCase,
    HarbourCase,
    YearForecast,
    market_cost_of_equity,
    nopat_route_fcff,
    option_claim,
    price_after_options,
    valuation_fcff,
)
from trading_notes.numerical.records import Record
from trading_notes.numerical.report import CheckReport, print_versions
from trading_notes.numerical.tolerance import close

WACC_DCF: Final = 0.08  # the DCF input of the Harbour valuation


def harbour_claims(case: HarbourCase) -> float:
    """Return debt + after-tax pension deficit - cash at the end of 2025."""
    B25 = case.balances[2025]
    return GROSS_DEBT - B25["db_liab"] * (1 - TAX) - B25["cash"]


def harbour_value(
    case: HarbourCase,
    fc: list[YearForecast],
    wacc: float = WACC_DCF,
    g: float = 0.025,
    ronic: float = 0.12,
) -> tuple[float, float, list[float]]:
    """Rebuild the value per share from a forecast, independently of the case's valuation.

    Returns:
        The value per share after options, the enterprise value and the three FCFFs.
    """
    fcff = [valuation_fcff(f) for f in fc]
    nopat_2028 = fc[2].op - TAX * (fc[2].op + fc[2].sbc)
    tv = nopat_2028 * (1 + g) * (1 - g / ronic) / (wacc - g)
    ev = sum(c / (1 + wacc) ** (t + 1) for t, c in enumerate(fcff)) + tv / (1 + wacc) ** 3
    return price_after_options(ev - harbour_claims(case)), ev, fcff


class AvonFittings(Record):
    """Avon Fittings' one-year accounts, from which the cash-flow routes start.

    Attributes:
        t: Tax rate.
        dep: Depreciation.
        interest: Interest expense.
        ebitda: EBITDA.
        ebit: EBIT.
        ni: Net income.
        fc_inv: Fixed-capital investment.
        wc_inv: Working-capital investment.
        net_borrow: Net borrowing.
        cfo: Operating cash flow under US GAAP (interest in operating).
        fcff_ni: FCFF by the net-income route.
        fcff_ebit: FCFF by the EBIT route.
        fcfe_ni: FCFE by the net-income route.
    """

    t: float
    dep: float
    interest: float
    ebitda: float
    ebit: float
    ni: float
    fc_inv: float
    wc_inv: float
    net_borrow: float
    cfo: float
    fcff_ni: float
    fcff_ebit: float
    fcfe_ni: float


def avon_fittings() -> AvonFittings:
    """Return Avon Fittings' accounts and its FCFF and FCFE."""
    t = 0.25
    rev, cash_costs, dep, interest = 500.0, 380.0, 30.0, 12.0
    ebitda = rev - cash_costs
    ebit = ebitda - dep
    ni = (ebit - interest) * (1 - t)
    fc_inv, wc_inv, net_borrow = 45.0, 8.0, 10.0
    return AvonFittings(
        t=t,
        dep=dep,
        interest=interest,
        ebitda=ebitda,
        ebit=ebit,
        ni=ni,
        fc_inv=fc_inv,
        wc_inv=wc_inv,
        net_borrow=net_borrow,
        cfo=ni + dep - wc_inv,
        fcff_ni=ni + dep + interest * (1 - t) - fc_inv - wc_inv,
        fcff_ebit=ebit * (1 - t) + dep - fc_inv - wc_inv,
        fcfe_ni=ni + dep - fc_inv - wc_inv + net_borrow,
    )


class Fenton(Record):
    """Fenton Engineering's normalised operating profit and its costs of capital.

    Attributes:
        ebit: Normalised EBIT.
        dep: Depreciation.
        nopat: Normalised NOPAT.
        wacc_public: WACC for a diversified buyer, from CAPM.
        wacc_private: WACC for an undiversified owner, from total beta and a 1-point wider spread.
    """

    ebit: float
    dep: float
    nopat: float
    wacc_public: float
    wacc_private: float


def fenton() -> Fenton:
    """Return Fenton Engineering's normalised profit and costs of capital."""
    adj = dict(owner_salary=-0.30, rent_to_owner=-0.30, litigation=+0.60, personal_expenses=+0.15)
    ebit_n = 5.6 + sum(adj.values())
    rf, erp, bu, de_ind, kd_pre = 0.03, 0.055, 0.95, 0.25, 0.065
    bl = bu * (1 + (1 - TAX) * de_ind)
    ke_capm = rf + bl * erp
    ke_total = rf + bl / 0.40 * erp
    wd = de_ind / (1 + de_ind)
    return Fenton(
        ebit=ebit_n,
        dep=1.2,
        nopat=ebit_n * (1 - TAX),
        wacc_public=(1 - wd) * ke_capm + wd * kd_pre * (1 - TAX),
        wacc_private=(1 - wd) * ke_total + wd * (kd_pre + 0.01) * (1 - TAX),
    )


def check_forecast_value(report: CheckReport, case: HarbourCase) -> None:
    """Check a forecast model turned into a value, and its evaluation."""
    print("== part 1: a forecast model turned into a value, and its evaluation (Harbour)")
    v_base, ev_base, _ = harbour_value(case, case.base)
    report.ok(
        "the value rebuilt from the forecast reproduces the company case: EV 1,218.45, 8.49 a"
        " share",
        close(ev_base, case.valuation.enterprise_value, 1e-9)
        and close(v_base, case.valuation.price, 1e-9),
    )
    report.ok(
        "the forecast balances in every year (assets = liabilities + equity), so no plug drives the"
        " cash flows",
        all(close(f.assets, f.liab_eq, 1e-6) for f in case.base),
    )
    scen = {
        "downside": ForecastCase(vol_growth=(0.0, 0.01, 0.02), price_infl=(0.02, 0.02, 0.02)),
        "upside": ForecastCase(vol_growth=(0.05, 0.05, 0.04)),
        "cost overrun": ForecastCase(sga_rate=0.185),
        "heavier capex": ForecastCase(capex_rate=0.095),
    }
    vals = {k: harbour_value(case, case.forecast(kw))[0] for k, kw in scen.items()}
    print("  scenario values: " + ", ".join(f"{k} {v:.2f}" for k, v in vals.items()))
    report.ok(
        "scenario values bracket the base: downside and cost overrun below 8.49, upside above",
        vals["downside"] < v_base < vals["upside"] and vals["cost overrun"] < v_base,
    )
    report.ok(
        "scenario values: downside 4.44, upside 10.42, cost overrun (SG&A 18.5%) 7.16, capex 9.5%"
        " of"
        " revenue 8.05",
        [round(vals[k], 2) for k in ("downside", "upside", "cost overrun", "heavier capex")]
        == [4.44, 10.42, 7.16, 8.05],
    )
    tv_2028 = case.valuation.terminal_value
    report.ok(
        "terminal-value share of EV is about 0.90: the explicit forecast years carry little of the"
        " value",
        0.85 < (tv_2028 / 1.08**3) / ev_base < 0.95,
        f"{tv_2028 / 1.08**3 / ev_base:.4f}",
    )
    grid = {
        (w, g): harbour_value(case, case.base, wacc=w, g=g)[0]
        for w in (0.07, 0.08, 0.09)
        for g in (0.015, 0.025, 0.035)
    }
    print(
        "  WACC x growth grid: "
        + ", ".join(f"({w:.0%},{g:.1%}) {v:.2f}" for (w, g), v in grid.items())
    )
    report.ok(
        "value falls with WACC and rises with growth at RONIC 12% > WACC",
        grid[(0.07, 0.025)] > grid[(0.08, 0.025)] > grid[(0.09, 0.025)]
        and grid[(0.08, 0.035)] > grid[(0.08, 0.015)],
    )


def check_research_targets(report: CheckReport, case: HarbourCase) -> None:
    """Check the reconciliation of divergent research targets for Harbour."""
    print("== part 2: research reports - reconciling divergent targets for Harbour")
    v_base = harbour_value(case, case.base)[0]
    eps_fwd = case.base[0].profit / SHARES
    target_pe = 18.0 * eps_fwd  # sell-side: peer median forward P/E
    eq_ev = 7.8 * 195.0 - harbour_claims(case)
    target_ev = price_after_options(eq_ev)
    diff_sources = {
        "multiple vs fundamentals": target_pe - target_ev,
        "EV/EBITDA peers vs DCF": target_ev - v_base,
    }
    report.ok(
        "targets: P/E comparables 13.11, EV/EBITDA comparables 11.39, DCF 8.49; the 4.62 gap splits"
        " 1.72 + 2.90",
        round(target_pe, 2) == 13.11
        and round(target_ev, 2) == 11.39
        and round(v_base, 2) == 8.49
        and close(sum(diff_sources.values()), target_pe - v_base)
        and [round(v, 2) for v in diff_sources.values()] == [1.72, 2.9],
        ", ".join(f"{k} {v:.2f}" for k, v in diff_sources.items()),
    )
    w_implied = brentq(lambda w: harbour_value(case, case.base, wacc=w)[0] - target_ev, 0.06, 0.08)
    report.ok(
        "the EV/EBITDA target needs a WACC of about 6.95% in the DCF (other inputs held)",
        round(w_implied, 4) == 0.0695,
        f"{w_implied:.5f}",
    )


def check_cash_flow_routes(report: CheckReport, case: HarbourCase) -> None:
    """Check FCFF and FCFE from net income, EBIT, EBITDA and CFO."""
    print(
        "== part 3: FCFF and FCFE from net income, EBIT, EBITDA and CFO (Avon Fittings, one year)"
    )
    a = avon_fittings()
    t, dep, interest, ebitda, ebit, ni = a.t, a.dep, a.interest, a.ebitda, a.ebit, a.ni
    fc_inv, wc_inv, net_borrow, cfo = a.fc_inv, a.wc_inv, a.net_borrow, a.cfo
    fcff_ni, fcff_ebit, fcfe_ni = a.fcff_ni, a.fcff_ebit, a.fcfe_ni
    fcff_ebitda = ebitda * (1 - t) + dep * t - fc_inv - wc_inv
    fcff_cfo = cfo + interest * (1 - t) - fc_inv
    fcfe_fcff = fcff_ni - interest * (1 - t) + net_borrow
    report.ok(
        "FCFF 44.50 by the net-income, EBIT, EBITDA and CFO routes; FCFE 45.50 from net income or"
        " from FCFF",
        all(close(x, 44.5) for x in (fcff_ni, fcff_ebit, fcff_ebitda, fcff_cfo))
        and close(fcfe_ni, 45.5)
        and close(fcfe_fcff, fcfe_ni),
        f"NI {ni:.2f}, EBIT {ebit:.2f}, EBITDA {ebitda:.2f}, CFO {cfo:.2f}",
    )
    # With interest paid in financing and taxes paid in operating (IAS 7 paras. 34A, 35), CFO is
    # built from cash receipts and payments, not by adjusting the US GAAP figure.
    taxes_paid = t * (ebit - interest)
    cfo_int_fin = ebitda - taxes_paid - wc_inv
    cfo_tax_fin = ebitda - t * ebit - wc_inv  # the interest tax saving also shown in financing
    report.ok(
        "interest paid in financing, taxes in operating: CFO 120 - 19.50 - 8 = 92.50 (12 above the"
        " US GAAP 80.50); FCFF = CFO - interest x t - FCInv = 44.50",
        close(cfo_int_fin, 92.5)
        and close(cfo_int_fin - cfo, interest)
        and close(cfo_int_fin - interest * t - fc_inv, fcff_ebit),
    )
    report.ok(
        "omitting the interest tax shield gives 47.50, overstating FCFF by 3.00; CFO is 89.50 and"
        " FCFF = CFO - FCInv only if the tax saving is also classified in financing",
        close(cfo_int_fin - fc_inv, 47.5)
        and close(cfo_int_fin - fc_inv - fcff_ebit, interest * t)
        and close(cfo_tax_fin, 89.5)
        and close(cfo_tax_fin - fc_inv, fcff_ebit),
    )
    # Harbour 2026 forecast: CFO route (with valuation adjustments) against the NOPAT route.
    f26 = case.base[0]
    report.ok(
        "Harbour 2026 valuation FCFF 31.93: CFO route equals the NOPAT route",
        close(valuation_fcff(f26), nopat_route_fcff(f26), 1e-9)
        and round(valuation_fcff(f26), 2) == 31.93,
    )


def fcfe_actual(f: YearForecast) -> float:
    """Return a forecast year's FCFE: CFO less capital spending and scheduled debt, plus draws."""
    return f.cfo - f.capex - f.lease_principal - f.loan_repay + f.draw


def check_cash_flow_forecasts(report: CheckReport, case: HarbourCase) -> None:
    """Check forecasting FCFF and FCFE under payout, issue and leverage policies."""
    print("== part 4: forecasting FCFF and FCFE - payouts, issues and leverage")
    a = avon_fittings()
    t, dep, ni, fc_inv, wc_inv = a.t, a.dep, a.ni, a.fc_inv, a.wc_inv
    base_fcfe = a.fcfe_ni
    fcfe_more_debt = ni + dep - fc_inv - wc_inv + (a.net_borrow + 20.0) - 20.0 * 0.06 * (1 - t)
    report.ok(
        "with net borrowing fixed at 10, borrowing 20 more at 6% (drawn at the start of the year)"
        " raises FCFE by 20 - 0.90 in the year and leaves FCFF unchanged",
        close(fcfe_more_debt - base_fcfe, 20 - 0.9),
    )
    # Uses of FCFE under the fixed policy: dividends 30, buyback 10, no issue; cash takes the rest.
    d_cash = base_fcfe - 30.0 - 10.0
    report.ok(
        "fixed borrowing: FCFE 45.50 = dividends 30 + buyback 10 + cash increase 5.50; five more of"
        " dividends cut the cash increase to 0.50 and leave FCFE at 45.50",
        close(d_cash, 5.5) and close(base_fcfe - 35.0 - 10.0, 0.5),
    )
    for f in case.base:
        o, c = f.opening, f.balance_sheet
        fcfe_stat = fcfe_actual(f)
        net_borrowing = f.draw - f.loan_repay - f.lease_principal + f.lease_new
        report.ok(
            f"Harbour {f.year}: FCFE {fcfe_stat:.2f} = dividends {f.divs:.2f} + change in cash "
            f"{c['cash'] - o['cash']:.2f}; net borrowing {net_borrowing:.2f}",
            close(fcfe_stat, f.divs + c["cash"] - o["cash"], 1e-9),
        )
    # Under the revolver policy the revolver tops cash up to 40, so a higher dividend is borrowed
    # and actual FCFE rises with it; FCFE before the revolver (scheduled loan and lease flows
    # only) and FCFF barely move.
    hi = case.forecast(ForecastCase(payout=0.50))
    lo26, hi26 = case.base[0], hi[0]
    report.ok(
        "2026 at payout 50% instead of 40%: dividend 36.62 (from 29.36), revolver draw 38.28 (from"
        " 30.81), actual FCFE 39.08 (from 31.82) - FCFE does not stay unchanged: it rises by 7.26",
        round(hi26.divs, 2) == 36.62
        and round(hi26.draw, 2) == 38.28
        and round(lo26.draw, 2) == 30.81
        and round(fcfe_actual(hi26), 2) == 39.08
        and round(fcfe_actual(lo26), 2) == 31.82
        and fcfe_actual(hi26) - fcfe_actual(lo26) > 7.0,
        f"{fcfe_actual(lo26):.4f} -> {fcfe_actual(hi26):.4f}",
    )
    report.ok(
        "at 50% the identity still holds: FCFE = dividends + change in cash (2.46, unchanged); no"
        " shares issued",
        all(
            close(fcfe_actual(f), f.divs + f.balance_sheet["cash"] - f.opening["cash"], 1e-9)
            for f in hi
        )
        and round(hi26.balance_sheet["cash"] - hi26.opening["cash"], 2) == 2.46
        and all(close(f.balance_sheet["share_capital"], f.opening["share_capital"]) for f in hi),
    )
    report.ok(
        "FCFE before the revolver 1.01 -> 0.80 (extra interest only); valuation FCFF 31.93 ->"
        " 31.88:"
        " FCFF credits the full tax saving on the extra interest, of which only 20% is settled in"
        " cash within the year",
        round(fcfe_actual(lo26) - lo26.draw, 2) == 1.01
        and round(fcfe_actual(hi26) - hi26.draw, 2) == 0.80
        and round(valuation_fcff(lo26), 2) == 31.93
        and round(valuation_fcff(hi26), 2) == 31.88
        and close(
            valuation_fcff(lo26) - valuation_fcff(hi26),
            0.8 * TAX * (hi26.interest_paid - lo26.interest_paid),
            1e-9,
        ),
    )
    # Target-ratio forecasting shortcut (Damodaran): FCFE = NI - (1 - DR)(FCInv - Dep + WCInv).
    dr = 0.30
    report.ok(
        "with 30% of net reinvestment debt-financed, FCFE = NI - 0.70 x (45 - 30 + 8) = 58.50 -"
        " 16.10 = 42.40",
        close(ni - (1 - dr) * (fc_inv - dep + wc_inv), 42.4) and close(ni, 58.5),
    )


def check_multistage_fcf(report: CheckReport) -> None:
    """Check single- and multistage FCFF and FCFE valuation at constant leverage."""
    print(
        "== part 5: single- and multistage FCFF and FCFE valuation (Brent Utilities, constant"
        " leverage)"
    )
    g = 0.03
    wacc_b, kd_b, t_b, dv = 0.07, 0.05, 0.25, 0.40
    fcff1 = 60.0
    V = fcff1 / (wacc_b - g)
    D = dv * V
    E = V - D
    ke_b = (wacc_b * V - kd_b * (1 - t_b) * D) / E
    fcfe1 = fcff1 - kd_b * (1 - t_b) * D + g * D
    report.ok(
        "FCFF 60 at WACC 7%, g 3%: firm 1,500, debt 600, equity 900; ke 9.17%; FCFE 60 - 22.5 + 18"
        " ="
        " 55.5 discounted at ke gives the same 900",
        close(V, 1500)
        and close(E, 900)
        and round(ke_b, 4) == 0.0917
        and close(fcfe1, 55.5)
        and close(fcfe1 / (ke_b - g), E, 1e-9),
    )
    long_e = sum(fcfe1 * (1 + g) ** (k - 1) / (1 + ke_b) ** k for k in range(1, 3000))
    report.ok("an explicit 3,000-year FCFE sum agrees", close(long_e, E, 1e-6))
    fcfe_wrong = fcfe1 / (wacc_b - g)
    report.ok(
        "discounting FCFE at the WACC overstates equity: 1,387.50 against 900",
        close(fcfe_wrong, 1387.5),
    )
    # Two-stage FCFE: high growth 12% for five years from FCFE0 = 2.00 a share, then 3%; ke 10%
    # then 9%.
    fcfe0, gh, gn, ke_h, ke_s, n = 2.00, 0.12, 0.03, 0.10, 0.09, 5
    cf = [fcfe0 * (1 + gh) ** k for k in range(1, n + 1)]
    tv = cf[-1] * (1 + gn) / (ke_s - gn)
    v2 = sum(c / (1 + ke_h) ** k for k, c in enumerate(cf, 1)) + tv / (1 + ke_h) ** n
    report.ok(
        "two-stage FCFE growing 12%: 2.24 ... 3.52; TV_5 = 3.52 x 1.03 / 6% = 60.51; value at ke"
        " 10%"
        " then 9%: 48.13",
        round(cf[0], 2) == 2.24
        and round(cf[-1], 2) == 3.52
        and round(tv, 2) == 60.51
        and round(v2, 2) == 48.13,
    )
    # Three-stage FCFE: 12% for five years, growth falling linearly to 3% over years 6-8 while ke
    # steps from 10% to 9%; discounting at the cumulated cost of equity (Damodaran pp. 374-375).
    g_path = [0.12] * 5 + [0.09, 0.06, 0.03]
    ke_path = [0.10] * 5 + [0.0967, 0.0933, 0.09]
    cf3, disc, x3 = [], 1.0, fcfe0
    for g_, k_ in zip(g_path, ke_path, strict=True):
        x3 *= 1 + g_
        disc *= 1 + k_
        cf3.append(x3 / disc)
    tv3 = x3 * 1.03 / (0.09 - 0.03)
    v3 = sum(cf3) + tv3 / disc
    report.ok(
        "three-stage FCFE: growth 12% for five years, then 9%, 6%, 3% while ke steps to 9%;"
        " terminal value at year 8 of 72.01; value 51.05 against 48.13 two-stage - the transition"
        " years add 2.92",
        round(tv3, 2) == 72.01 and round(v3, 2) == 51.05 and round(v3 - v2, 2) == 2.92,
        f"TV {tv3:.4f}, value {v3:.4f}",
    )
    # A stable-period reinvestment check: g = 3% with stable ROE 12% needs 25% equity reinvestment.
    ni5 = 4.0
    report.ok(
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
    report.ok(
        "the stable cost of equity (8-10%) and growth (2-4%) move the value from 38.46 to 67.46",
        round(min(sens.values()), 2) == 38.46 and round(max(sens.values()), 2) == 67.46,
    )


def check_cash_flow_proxies(report: CheckReport, case: HarbourCase) -> None:
    """Check dividends, net income and EBITDA against FCFE and FCFF."""
    print("== part 6: cash-flow proxies - dividends, net income and EBITDA against FCFE and FCFF")
    _, ev_base, fcff_base = harbour_value(case, case.base)
    f26 = case.base[0]
    nopat26 = f26.op - TAX * (f26.op + f26.sbc)
    report.ok(
        "Harbour 2026: EBITDA 227.28, NOPAT 87.28, net income 73.40, valuation FCFF 31.93, FCFE"
        " 31.82, dividends 29.36",
        round(f26.ebitda, 2) == 227.28
        and round(nopat26, 2) == 87.28
        and round(f26.profit, 2) == 73.4
        and round(fcff_base[0], 2) == 31.93
        and round(f26.divs + f26.balance_sheet["cash"] - f26.opening["cash"], 2) == 31.82
        and round(f26.divs, 2) == 29.36,
    )
    ebitda_cap = f26.ebitda / (WACC_DCF - 0.025)
    report.ok(
        "capitalising EBITDA as if it were FCFF (227.28 / 5.5%) gives 4,132, against a DCF EV of"
        " 1,218",
        round(ebitda_cap) == 4132 and ebitda_cap > 3 * ev_base,
    )
    # Damodaran's Table 15.1 relations, checked on Avon Fittings.
    a = avon_fittings()
    report.ok(
        "EBIT(1 - t) = FCFF + capex - depreciation + change in WC; EBITDA = FCFF + EBIT x t + capex"
        " + change in WC",
        close(a.ebit * (1 - a.t), a.fcff_ebit + a.fc_inv - a.dep + a.wc_inv)
        and close(a.ebitda, a.fcff_ebit + a.ebit * a.t + a.fc_inv + a.wc_inv),
    )


# Residual-income example inputs: book value, ROE, cost of equity and payout.
BV0, ROE, KE_RI, PAYOUT = 20.0, 0.12, 0.09, 0.5


def check_eva(report: CheckReport, case: HarbourCase) -> None:
    """Check residual income, EVA and MVA."""
    print("== part 7: residual income, EVA and MVA")
    bv0, roe, kek = BV0, ROE, KE_RI
    ri1 = (roe - kek) * bv0
    report.ok(
        "RI = (ROE - ke) x B0 = (12% - 9%) x 20 = 0.60; equivalently NI 2.40 less a 1.80 equity"
        " charge",
        close(ri1, 0.6) and close(roe * bv0 - kek * bv0, ri1),
    )

    # Harbour EVA: NOPAT less WACC x opening invested capital (book equity + debt + after-tax
    # pension - cash).
    def invested_capital(y: int) -> float:
        """Return book equity plus debt and after-tax pension deficit, less cash, at year-end y."""
        b = case.balances[y]
        return (
            case.balance_view(y).eq
            + (-(b["term_loan"] + b["revolver"] + b["lease_liab"]))
            - b["db_liab"] * (1 - TAX)
            - b["cash"]
        )

    ic24, ic25 = invested_capital(2024), invested_capital(2025)
    op25 = case.statements[2025].income["op"]
    nopat25 = op25 - TAX * (op25 + YEARS[2025].sbc)
    wacc_mkt = 0.0802
    eva25 = nopat25 - wacc_mkt * ic24
    ev_mkt = MARKET_PRICE * SHARES + option_claim(MARKET_PRICE) + harbour_claims(case)
    mva = ev_mkt - ic25
    print(
        f"  invested capital 2024 {ic24:.2f}, 2025 {ic25:.2f}; NOPAT 2025 {nopat25:.2f}; EVA"
        f" {eva25:.2f}; MVA {mva:.2f}"
    )
    report.ok(
        "Harbour 2025: NOPAT 67.50 on opening capital 945.00 earns 7.14% < WACC 8.02%: EVA -8.29;"
        " market EV 1,479.77 less invested capital 1,000.96 is MVA 478.81",
        round(nopat25, 2) == 67.5
        and round(ic24, 2) == 945.0
        and round(nopat25 / ic24, 4) == 0.0714
        and round(eva25, 2) == -8.29
        and round(ic25, 2) == 1000.96
        and round(mva, 2) == 478.81,
    )
    add_back = 18.0 * (1 - TAX)
    report.ok(
        "adding back the 18 restructuring charge after tax lifts NOPAT to 81.00 and EVA to 5.21",
        round(nopat25 + add_back, 2) == 81.0
        and round(nopat25 + add_back - wacc_mkt * ic24, 2) == 5.21,
    )
    # EVA value = capital + PV(EVA) equals FCFF value (Damodaran Illustration 32.1 structure, own
    # numbers).
    ic0, roc, wacc_e, inv = 200.0, 0.14, 0.09, 20.0
    v_eva = (
        ic0
        + (roc - wacc_e) * ic0 / wacc_e
        + sum((roc - wacc_e) * inv / wacc_e / (1 + wacc_e) ** k for k in range(4))
    )
    # NOPAT of years 1-4, with investment at the start of each year.
    nop = [roc * (ic0 + inv * k) for k in range(1, 5)]
    fcff_e = [-inv] + [nop[k] - (inv if k < 3 else 0.0) for k in range(4)]
    v_dcf = (
        fcff_e[0]
        + sum(c / (1 + wacc_e) ** (k + 1) for k, c in enumerate(fcff_e[1:]))
        + nop[-1] / wacc_e / (1 + wacc_e) ** 4
    )
    report.ok(
        "capital 200 at ROC 14% and WACC 9% plus four 20 investments at 14%: EVA value 350.35 ="
        " FCFF value",
        round(v_eva, 2) == 350.35 and close(v_eva, v_dcf, 1e-9),
        f"FCFF route {v_dcf:.4f}",
    )


def check_residual_income_stages(report: CheckReport) -> None:
    """Check single-stage, multistage and continuing residual income."""
    print("== part 8: single-stage, multistage and continuing residual income")
    bv0, roe, kek, payout = BV0, ROE, KE_RI, PAYOUT
    ri1 = (roe - kek) * bv0
    g_c = roe * (1 - payout)
    v_ri = bv0 + ri1 / (kek - g_c)
    report.ok(
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
    explicit = (
        20.0 + pv + sum(ri_path[-1] * omega**j / (1 + kek) ** (3 + j) for j in range(1, 4000))
    )
    report.ok(
        "RI 1.20, 1.08, 0.92 over three years, then persisting at omega 0.6: TV_3 1.13, value"
        " 23.59;"
        " an explicit sum agrees",
        [round(x, 2) for x in ri_path] == [1.2, 1.08, 0.92]
        and round(tv_ri, 2) == 1.13
        and round(v_ms, 2) == 23.59
        and close(v_ms, explicit, 1e-9),
        f"TV {tv_ri:.4f}, value {v_ms:.4f}",
    )
    v_om0, v_om1 = 20.0 + pv, 20.0 + pv + ri_path[-1] / kek / (1 + kek) ** 3
    report.ok(
        "omega bounds: 0 gives 22.72 (RI stops), 1 gives 30.61 (RI held forever)",
        round(v_om0, 2) == 22.72 and round(v_om1, 2) == 30.61,
    )


def book_equity(bs: dict[str, float]) -> float:
    """Return book equity from a forecast balance sheet."""
    return bs["share_capital"] + bs["sbp_reserve"] + bs["remeasurement_reserve"] + bs["retained"]


def check_residual_income_harbour(report: CheckReport, case: HarbourCase) -> None:
    """Check residual income against dividends for Harbour, with the dirty-surplus credit."""
    print("== part 9: residual income against dividends for Harbour, with the dirty-surplus credit")
    KE = market_cost_of_equity()
    fc = case.base
    bvs = [case.balance_view(2025).eq] + [book_equity(f.balance_sheet) for f in fc]
    ni_h = [f.profit for f in fc]
    div_h = [f.divs for f in fc]
    contrib = [bvs[k + 1] - bvs[k] - ni_h[k] + div_h[k] for k in range(3)]
    report.ok(
        "forecast book equity grows by profit less dividends plus the equity credit for share-based"
        " pay (9.45, 9.92, 10.42): the dirty-surplus item",
        all(close(c, f.sbc, 1e-6) for c, f in zip(contrib, fc, strict=True)),
        ", ".join(f"{c:.4f}" for c in contrib),
    )
    roe_ss, g_ss = 0.1079, 0.025
    pb_t = (roe_ss - g_ss) / (KE - g_ss)
    p_t = pb_t * bvs[-1]
    v_ddm = sum(d / (1 + KE) ** k for k, d in enumerate(div_h, 1)) + p_t / (1 + KE) ** 3
    ri_h = [ni_h[k] - KE * bvs[k] for k in range(3)]
    v_ri_naive = (
        bvs[0]
        + sum(r / (1 + KE) ** k for k, r in enumerate(ri_h, 1))
        + (p_t - bvs[-1]) / (1 + KE) ** 3
    )
    pv_credits = sum(c / (1 + KE) ** k for k, c in enumerate(contrib, 1))
    report.ok(
        "with the same terminal price (P/B on 2028 book), RI on reported book equals the dividend"
        " value less the PV of the equity credits: the finite-horizon identity with a dirty-surplus"
        " term",
        close(v_ri_naive, v_ddm - pv_credits, 1e-9)
        and round(v_ddm, 2) == 834.16
        and round(v_ri_naive, 2) == 809.24
        and round(pv_credits, 2) == 24.92
        and round(pb_t, 4) == 1.2148
        # simple division per share, before the option claim: see the next checks
        and [round(v / SHARES, 2) for v in (v_ddm, v_ri_naive)] == [8.28, 8.03],
        f"DDM {v_ddm:.4f} ({v_ddm / SHARES:.4f} a share), RI {v_ri_naive:.4f}"
        f" ({v_ri_naive / SHARES:.4f}), PV credits {pv_credits:.4f}, P_T {p_t:.4f}, P/B"
        f" {pb_t:.4f}",
    )
    report.ok(
        "Harbour RI: 2026 ROE on opening book 11.34% against ke 9.32%; RI 13.04, 10.12, 9.86",
        round(ni_h[0] / bvs[0], 4) == 0.1134
        and [round(r, 2) for r in ri_h] == [13.04, 10.12, 9.86],
        ", ".join(f"RI {r:.2f}" for r in ri_h),
    )
    # Book value plus RI values every equity claim book equity supports, including the five
    # million vested options; the DDM aggregate also includes the dividends that future grantees
    # will receive. Per common share both need the option claim removed at the price it implies,
    # as in the DCF bridge.
    p_ri = price_after_options(v_ri_naive)
    p_brent = brentq(lambda p: p * SHARES + option_claim(p) - v_ri_naive, 1.0, 20.0)
    opt_ri = option_claim(p_ri)
    report.ok(
        "per common share: p = (809.24 - 5 C(p)) / 100.75 = 7.9557, options 7.70; the fixed point"
        " equals a root-finder solution; simple division (8.0322) overstates by the option claim"
        " per share",
        round(p_ri, 4) == 7.9557
        and close(p_ri, p_brent, 1e-9)
        and round(opt_ri, 2) == 7.70
        and round(v_ri_naive / SHARES, 4) == 8.0322
        and close(v_ri_naive / SHARES - p_ri, opt_ri / SHARES, 1e-9),
        f"{p_ri:.6f}, options {opt_ri:.4f}",
    )
    common_ddm = v_ddm - pv_credits - opt_ri
    report.ok(
        "dividend route on the same claims: 834.16 - 24.92 (future grants) - 7.70 (vested options)"
        " ="
        " 801.54 = 7.9557 x 100.75; deducting the options does not double count the grants charged"
        " in RI",
        round(common_ddm, 2) == 801.54 and close(common_ddm / SHARES, p_ri, 1e-9),
    )
    pb_mkt = MARKET_PRICE * SHARES / bvs[0]
    pb_claims = (MARKET_PRICE * SHARES + option_claim(MARKET_PRICE)) / bvs[0]
    g_implied = KE - (roe_ss - KE) / (pb_claims - 1)
    roe_implied = KE + (pb_claims - 1) * (KE - g_ss)
    g_common = KE - (roe_ss - KE) / (pb_mkt - 1)
    roe_common = KE + (pb_mkt - 1) * (KE - g_ss)
    report.ok(
        "implied growth on all equity claims: market equity 1,108.25 + options 17.94 = 1,126.19,"
        " P/B"
        " 1.74; at ke 9.32% and a sustained ROE of 10.79% residual income must grow 7.34% a year;"
        " at 2.5% growth the price needs ROE 14.37% (shares alone: P/B 1.71, 7.27% and 14.18%)",
        round(MARKET_PRICE * SHARES + option_claim(MARKET_PRICE), 2) == 1126.19
        and round(pb_claims, 2) == 1.74
        and round(g_implied, 4) == 0.0734
        and round(roe_implied, 4) == 0.1437
        and round(pb_mkt, 2) == 1.71
        and round(g_common, 4) == 0.0727
        and round(roe_common, 4) == 0.1418,
        f"P/B {pb_claims:.4f}, g {g_implied:.4f}, ROE {roe_implied:.4f}",
    )
    # Justified P/B applied to book is also an aggregate over all equity claims.
    just_agg = pb_t * bvs[0]
    p_just = price_after_options(just_agg)
    report.ok(
        "justified P/B 1.2148 x book 647.38 = 786.43 for all equity claims: 7.81 by simple"
        " division,"
        " 7.74 a common share after the vested options",
        round(just_agg, 2) == 786.43
        and round(just_agg / SHARES, 2) == 7.81
        and round(p_just, 2) == 7.74,
        f"{p_just:.4f}",
    )
    share_book = bvs[0] / v_ri_naive
    share_tv_ri = (p_t - bvs[-1]) / (1 + KE) ** 3 / v_ri_naive
    share_tv_ddm = p_t / (1 + KE) ** 3 / v_ddm
    report.ok(
        "value recognition: in the RI value, current book is 80% and the terminal premium over book"
        " 17%; in the dividend value the terminal price is 91%",
        round(share_book, 2) == 0.80
        and round(share_tv_ri, 2) == 0.17
        and round(share_tv_ddm, 2) == 0.91,
        f"book {share_book:.3f}, RI terminal {share_tv_ri:.3f}, DDM terminal {share_tv_ddm:.3f}",
    )


def check_normalised_earnings(report: CheckReport) -> None:
    """Check the normalisation of Fenton Engineering's earnings."""
    print("== part 10: private company - normalising Fenton Engineering's earnings")
    f = fenton()
    report.ok(
        "normalised EBIT 5.6 - 0.30 - 0.30 + 0.60 + 0.15 = 5.75 (margin 14.4%)",
        close(f.ebit, 5.75) and round(f.ebit / 40, 3) == 0.144,
    )
    capex_f, dwc_f = 1.6, 0.4
    fcff_f = f.nopat + f.dep - capex_f - dwc_f
    report.ok(
        "normalised NOPAT 4.3125; FCFF 4.3125 + 1.2 - 1.6 - 0.4 = 3.5125",
        close(f.nopat, 4.3125) and close(fcff_f, 3.5125),
    )


def check_private_required_return(report: CheckReport) -> None:
    """Check required returns by CAPM, expanded CAPM, build-up and total beta."""
    print(
        "== part 11: private company - required return by CAPM, expanded CAPM, build-up and total"
        " beta"
    )
    rf, erp, bu, de_ind = 0.03, 0.055, 0.95, 0.25
    bl = bu * (1 + (1 - TAX) * de_ind)
    ke_capm = rf + bl * erp
    ke_exp = ke_capm + 0.02 + 0.015
    ke_build = rf + erp + 0.02 + 0.005 + 0.015
    total_beta = bl / 0.40
    ke_total = rf + total_beta * erp
    f = fenton()
    report.ok(
        "levered beta 1.128; CAPM 9.20%, expanded CAPM (size 2%, specific 1.5%) 12.70%, build-up"
        " 12.50%, total beta 2.82 -> 18.51%",
        round(bl, 3) == 1.128
        and round(ke_capm, 4) == 0.092
        and round(ke_exp, 4) == 0.127
        and round(ke_build, 4) == 0.125
        and round(total_beta, 2) == 2.82
        and round(ke_total, 4) == 0.1851,
    )
    report.ok(
        "WACC at 20% debt: 8.34% for a diversified buyer, 15.93% for an undiversified owner (spread"
        " +1 point)",
        round(f.wacc_public, 4) == 0.0834 and round(f.wacc_private, 4) == 0.1593,
    )


def check_private_valuation(report: CheckReport) -> None:
    """Check income, market and asset approaches, and control and marketability discounts."""
    print(
        "== part 12: private company - income, market and asset approaches; control and"
        " marketability"
    )
    f = fenton()
    g_f, ronic_f = 0.025, 0.12
    fcff_ss = f.nopat * (1 + g_f) * (1 - g_f / ronic_f)
    ev_pub = fcff_ss / (f.wacc_public - g_f)
    ev_priv = fcff_ss / (f.wacc_private - g_f)
    net_debt_f = 6.0
    report.ok(
        "income approach (steady state, RONIC 12%): EV 59.93 to a diversified buyer, 26.05 to an"
        " undiversified owner",
        round(ev_pub, 2) == 59.93 and round(ev_priv, 2) == 26.05,
    )
    ebitda_n = f.ebit + f.dep
    ev_gpc = 7.5 * ebitda_n
    ev_tx = 6.8 * ebitda_n
    report.ok(
        "market approach: guideline public companies 7.5x normalised EBITDA 6.95 = 52.13"
        " (marketable minority basis); precedent transactions 6.8x = 47.26 (control basis)",
        round(ev_gpc, 3) == 52.125 and round(ev_tx, 2) == 47.26,
    )
    nav = 38.0 - 6.0 - 9.5
    report.ok(
        "asset approach: assets at fair value 38.0 less net debt 6.0 and other liabilities 9.5:"
        " equity 22.5",
        close(nav, 22.5),
    )
    eq_control = ev_pub - net_debt_f
    dloc = 1 - 1 / 1.25
    dlom_silber_10 = 1 - math.exp(4.33 + 0.036 * math.log(10) - 0.142 * math.log(100) + 0.174) / 100
    dlom_silber_40 = 1 - math.exp(4.33 + 0.036 * math.log(40) - 0.142 * math.log(100) + 0.174) / 100
    dlom = 0.25 + (dlom_silber_40 - dlom_silber_10)
    stake = 0.30 * eq_control * (1 - dloc) * (1 - dlom)
    report.ok(
        "Silber regression: discount 48.94% at revenue 10m and 46.33% at 40m, so a 25% benchmark"
        " becomes 22.39%",
        round(dlom_silber_10, 4) == 0.4894
        and round(dlom_silber_40, 4) == 0.4633
        and round(dlom, 4) == 0.2239,
    )
    report.ok(
        "30% minority stake: 30% of control equity 53.93, less DLOC 20% (control premium 25%) and"
        " DLOM 22.39%: 10.05",
        round(eq_control, 2) == 53.93 and close(dloc, 0.2) and round(stake, 2) == 10.05,
        f"combined discount {1 - (1 - dloc) * (1 - dlom):.4f}",
    )
    report.ok(
        "the discounts multiply: 1 - 0.80 x 0.7761 = 37.91%, not 20% + 22.39% = 42.39%",
        round(1 - (1 - dloc) * (1 - dlom), 4) == 0.3791,
    )
    # Total beta and marketability are different effects (Damodaran Table 24.2 applies both for a
    # private sale), so an undiversified buyer's stake value keeps the marketability discount.
    stake_undiv = 0.30 * (ev_priv - net_debt_f) * (1 - dloc) * (1 - dlom)
    report.ok(
        "undiversified buyer: 30% of (26.05 - 6.0) = 20.05 equity, less DLOC and DLOM: 3.73;"
        " dropping the DLOM as a supposed double count would give 4.81, pricing the stake as if it"
        " could be sold freely",
        round(ev_priv - net_debt_f, 2) == 20.05
        and round(stake_undiv, 2) == 3.73
        and round(0.30 * (ev_priv - net_debt_f) * (1 - dloc), 2) == 4.81,
    )


def main() -> int:
    """Build the Harbour case, then run the 12 parts with one report.

    Harbour Tools plc (hypothetical, EUR millions, valuation date 31 December 2025) comes from
    trading_notes.numerical.company_case: the 2026-2028 forecast, the valuation conventions (leases
    as debt, share-based pay a cost, pension deficit a claim) and the 8.49 DCF value. The cost of
    equity 9.32% and WACC 8.02% follow the corporate-finance checks (options in market equity). Avon
    Fittings, Brent Utilities and Fenton Engineering are stand-alone hypothetical companies.
    Independent routes: the Harbour value rebuilt from the forecast against the company case; FCFF
    by the net-income, EBIT, EBITDA and CFO routes against each other; FCFF and FCFE values of a
    constant-leverage firm against each other and an explicit 3,000-year sum; residual-income values
    against dividend values with the same terminal price (contributions included); EVA value against
    FCFF value; total-beta, build-up and CAPM costs of equity from their definitions; the Silber
    regression evaluated directly.

    Returns:
        The exit status, 0 or 1.
    """
    print_versions(np, scipy)
    case = HarbourCase()
    report = CheckReport()
    check_forecast_value(report, case)
    check_research_targets(report, case)
    check_cash_flow_routes(report, case)
    check_cash_flow_forecasts(report, case)
    check_multistage_fcf(report)
    check_cash_flow_proxies(report, case)
    check_eva(report, case)
    check_residual_income_stages(report)
    check_residual_income_harbour(report, case)
    check_normalised_earnings(report)
    check_private_required_return(report)
    check_private_valuation(report)
    print(f"\n{report.count} checks executed")
    return report.summarise()


if __name__ == "__main__":
    sys.exit(main())
