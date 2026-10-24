"""Private capital: the worked numbers of the private-capital allocator entries."""

import sys
from collections.abc import Sequence
from typing import Final

import numpy as np
import scipy
from numpy.typing import NDArray
from scipy.optimize import brentq, minimize

from trading_notes.numerical.alternative_investment_structures.hedge_fund_fees import FeeTerms
from trading_notes.numerical.internal_rate import irr
from trading_notes.numerical.private_debt_special_situations.restructuring import (
    ClassVote,
    PlanConfirmation,
    RecoveryWaterfall,
)
from trading_notes.numerical.private_equity_strategies.leveraged_buyout import LeveragedBuyout
from trading_notes.numerical.private_fund_structures.waterfalls import DealBook, EuropeanWaterfall
from trading_notes.numerical.records import Record
from trading_notes.numerical.report import CheckReport
from trading_notes.numerical.tolerance import close

type Floats = NDArray[np.float64]

SEED: Final = 20261020
GROSS: Final = (0.15, -0.10, 0.12, 0.20)  # Brook Relative Value's gross returns, years 1-4
T: Final = 9  # Ashby Fund I: year ends 0..8; flows dated at year ends
ASHBY: Final = DealBook(
    deals={  # deal: (cost, year bought, year sold, exit value)
        "A": (25.0, 0, 4, 60.0),
        "B": (25.0, 1, 5, 40.0),
        "C": (20.0, 2, 7, 50.0),
        "D": (10.0, 3, 6, 0.0),
    }
)
EUROPEAN: Final = EuropeanWaterfall(hurdle=0.08, carry=0.2)
# Corran: EBITDA at entry, the entry multiple and the fees
E0: Final = 50.0
M_IN: Final = 9.0
FEES: Final = 10.0
CORRAN: Final = LeveragedBuyout(ebitda=E0, fees=FEES, entry_multiple=M_IN, exit_multiple=M_IN)
# Assumed waterfall (stated in the entry): the DIP lenders hold a priming first lien granted under
# 11 U.S.C. 364(d) with the pre-petition lenders' consent; the senior lenders agreed a carve-out for
# administrative claims; the senior claim is fully secured (collateral worth at least 200, so no
# 506(a) deficiency claim); the unsecured bonds are one class; old equity is junior to all.
CLAIMS: Final = (
    ("DIP", 40.0),
    ("administrative", 10.0),
    ("senior secured", 200.0),
    ("unsecured", 150.0),
)
HALDEN: Final = RecoveryWaterfall(claims=CLAIMS)


class FundYear(Record):
    """Ashby Fund I's since-inception metrics at one year end.

    Attributes:
        t: The year end.
        dpi: Distributions over paid-in capital.
        rvpi: Residual value (the LP's share of NAV) over paid-in capital.
        tvpi: dpi + rvpi.
        irr: The since-inception IRR with NAV as a final flow; none at year 0.
        nav: The LP's share of NAV after accrued carry.
    """

    t: int
    dpi: float
    rvpi: float
    tvpi: float
    irr: float | None
    nav: float

    @property
    def known_irr(self) -> float:
        """Return the IRR.

        Raises:
            ValueError: At year 0, which has no IRR.
        """
        if self.irr is None:
            raise ValueError(f"no IRR at year {self.t}")
        return self.irr


class AshbyFlows(Record):
    """Ashby Fund I's dated flows, year ends 0 to 8.

    Attributes:
        inv: Deal capital invested.
        proc: Exit proceeds.
        calls: Capital called: deal capital plus management fees.
        lp_eu: The LP's distributions under the European waterfall.
    """

    inv: Floats
    proc: Floats
    calls: Floats
    lp_eu: Floats


def cov(vols: Sequence[float], corr: Sequence[Sequence[float]]) -> Floats:
    """Return the covariance matrix of the volatilities and correlations."""
    c: Floats = np.outer(vols, vols) * np.array(corr, dtype=np.float64)
    return c


def budget(w: Floats) -> float:
    """Return the equality constraint sum(w) - 1."""
    gap: float = w.sum() - 1
    return gap


def check_hedge_fund_fees(report: CheckReport) -> None:
    """Part 1: Brook Relative Value's 2/20 fees, high-water mark and a 4% hard hurdle."""
    print(
        "== part 1: hedge-fund fees - 2/20, high-water mark and a 4% hard hurdle (Brook Relative"
        " Value)"
    )

    hard = FeeTerms().run(GROSS)
    report.ok(
        "net returns 11.20%, -12.00%, 10.00%, 15.89%; incentive fees 1.80, 0, 0, 2.27; NAV 124.74"
        " against 139.10 gross",
        [round(r.net * 100, 2) for r in hard] == [11.2, -12.0, 10.0, 15.89]
        and [round(r.inc, 2) for r in hard] == [1.80, 0.0, 0.0, 2.27]
        and round(hard[-1].nav, 2) == 124.74
        and round(100 * np.prod([1 + g for g in GROSS]), 2) == 139.10,
    )
    report.ok(
        "each year gross value = management fee + incentive fee + closing NAV",
        all(close(r.gross_value, r.mgmt + r.inc + r.nav, 1e-9) for r in hard),
    )
    no_hwm = FeeTerms(high_water_mark=False).run(GROSS)
    soft = FeeTerms(soft=True).run(GROSS)
    report.ok(
        "without a high-water mark year 3 pays an incentive fee of 1.17 on the recovery and the"
        " NAV ends at 122.65; a soft hurdle charges 2.60 in year 1 and ends at 122.96",
        round(no_hwm[2].inc, 2) == 1.17
        and round(no_hwm[-1].nav, 2) == 122.65
        and round(soft[0].inc, 2) == 2.60
        and round(soft[-1].nav, 2) == 122.96,
    )
    fee_drag = (np.prod([1 + g for g in GROSS]) ** 0.25 - 1) - ((hard[-1].nav / 100) ** 0.25 - 1)
    report.ok(
        "annualised: 8.60% gross against 5.68% net, a fee drag of 2.92 points a year",
        round((np.prod([1 + g for g in GROSS]) ** 0.25 - 1) * 100, 2) == 8.60
        and round(((hard[-1].nav / 100) ** 0.25 - 1) * 100, 2) == 5.68
        and round(fee_drag * 100, 2) == 2.92,
    )


def check_waterfalls(report: CheckReport) -> AshbyFlows:
    """Part 2: Ashby Fund I - calls, fees, the European and American waterfalls."""
    print("== part 2: Ashby Fund I - calls, fees, the European and American waterfalls")
    inv, proc = np.zeros(T), np.zeros(T)
    for c, ti, te, x in ASHBY.deals.values():
        inv[ti] += c
        proc[te] += x

    fee = np.array([2.0 if t <= 4 else 0.015 * ASHBY.held_cost(t) for t in range(T)])
    calls = inv + fee
    report.ok(
        "commitment 100: deal capital 80 and management fees 10.75 (2.00 a year for five years on"
        " commitment, then 1.5% of cost still held: 0.45, 0.30); paid-in 90.75",
        close(inv.sum(), 80.0)
        and [round(f, 2) for f in fee[5:]] == [0.45, 0.30, 0.0, 0.0]
        and round(fee.sum(), 2) == 10.75
        and round(calls.sum(), 2) == 90.75,
    )

    lp_eu, gp_eu = EUROPEAN.distribute(calls, proc)
    profit = proc.sum() - calls.sum()
    report.ok(
        "European waterfall: LP receives 60, 40 and 38.15; carry 11.85 paid only in year 7,"
        " exactly 20% of the fund profit of 59.25",
        [round(v, 2) for v in lp_eu[[4, 5, 7]]] == [60.0, 40.0, 38.15]
        and close(gp_eu[:7].sum(), 0.0)
        and round(gp_eu.sum(), 2) == 11.85
        and round(profit, 2) == 59.25
        and close(gp_eu.sum(), 0.2 * profit, 1e-9),
    )
    fee_alloc = fee.sum()
    gp_am = np.zeros(T)
    am_rows: dict[str, float] = {}
    for k, (c, ti, te, x) in ASHBY.deals.items():
        capital = c + fee_alloc * c / inv.sum()
        pref = capital * (1.08 ** (te - ti) - 1)
        lp_d = min(x, capital + pref)
        cash = x - lp_d
        gp_d = min(cash, 0.25 * max(lp_d - capital, 0.0))
        cash -= gp_d
        lp_d += 0.8 * cash
        gp_d += 0.2 * cash
        gp_am[te] += gp_d
        am_rows[k] = gp_d
    clawback = gp_am.sum() - gp_eu.sum()
    report.ok(
        "American (deal-by-deal, fees allocated by cost): carry 6.33 in year 4, 1.42 in year 5 and"
        " 5.46 in year 7 - 13.21 in all, 1.36 more than the whole-fund 11.85 because deal D's loss"
        " is not netted: the clawback",
        [round(am_rows[k], 2) for k in "ABCD"] == [6.33, 1.42, 5.46, 0.0]
        and round(gp_am.sum(), 2) == 13.21
        and round(clawback, 2) == 1.36,
    )
    return AshbyFlows(inv=inv, proc=proc, calls=calls, lp_eu=lp_eu)


def check_fund_metrics(report: CheckReport, flows: AshbyFlows) -> None:
    """Part 3: fund metrics - DPI, RVPI, TVPI, IRR by year (J-curve), gross against net, KS-PME."""
    print(
        "== part 3: fund metrics - DPI, RVPI, TVPI, IRR by year (J-curve), gross against net,"
        " KS-PME"
    )
    inv, proc, calls, lp_eu = flows.inv, flows.proc, flows.calls, flows.lp_eu
    rows3: list[FundYear] = []
    for t in range(T):
        nav = ASHBY.mark(t)
        hyp = proc[: t + 1].copy()
        hyp[t] += nav  # hypothetical liquidation at NAV
        lp_h, _ = EUROPEAN.distribute(calls[: t + 1], hyp)
        lp_nav = lp_h[t] - lp_eu[t]  # LP's share of NAV after accrued carry
        paid = calls[: t + 1].sum()
        dist = lp_eu[: t + 1].sum()
        cf = list(lp_eu[: t + 1] - calls[: t + 1])
        cf[-1] += lp_nav
        rows3.append(
            FundYear(
                t=t,
                dpi=dist / paid,
                rvpi=lp_nav / paid,
                tvpi=(dist + lp_nav) / paid,
                irr=irr(cf) if t else None,
                nav=lp_nav,
            )
        )
    for r in rows3:
        print(
            f"  year {r.t}: DPI {r.dpi:.3f} RVPI {r.rvpi:.3f} TVPI {r.tvpi:.3f}"
            + (f" IRR {r.irr:.4f}" if r.irr is not None else "")
        )
    report.ok(
        "J-curve: TVPI 0.93 in years 0-1 (fees, deals at cost); since-inception IRR -14.8% after"
        " year 1, 3.0% after year 2, 11.7% at liquidation in year 7",
        round(rows3[1].known_irr, 3) == -0.148
        and round(rows3[2].known_irr, 3) == 0.030
        and round(rows3[7].known_irr, 3) == 0.117
        and round(rows3[1].tvpi, 2) == 0.93
        and round(rows3[0].tvpi, 2) == 0.93,
        f"{rows3[1].irr:.4f}",
    )
    report.ok(
        "TVPI = DPI + RVPI every year; DPI crosses 1 in year 5 (1.11) and dips to 1.10 when year-6"
        " fees are called; at liquidation DPI = TVPI = 1.52 and RVPI = 0",
        all(close(r.tvpi, r.dpi + r.rvpi, 1e-12) for r in rows3)
        and rows3[4].dpi < 1 < rows3[5].dpi
        and round(rows3[5].dpi, 2) == 1.11
        and round(rows3[6].dpi, 2) == 1.10
        and round(rows3[-1].dpi, 2) == 1.52
        and close(rows3[-1].rvpi, 0.0, 1e-12),
    )
    gross_irr = irr(proc - inv)
    net_irr = irr(lp_eu - calls)
    report.ok(
        "gross deal IRR 16.87% and MOIC 1.88 against net LP IRR 11.71% and TVPI 1.52: fees and"
        " carry cost 5.2 points a year",
        round(gross_irr * 100, 2) == 16.87
        and round(proc.sum() / inv.sum(), 3) == 1.875
        and round(net_irr * 100, 2) == 11.71
        and round(lp_eu.sum() / calls.sum(), 2) == 1.52
        and round((gross_irr - net_irr) * 100, 1) == 5.2,
        f"gross {gross_irr:.4f}, net {net_irr:.4f}",
    )
    IDX_R = [0.0, 0.10, -0.05, 0.12, 0.08, 0.06, 0.15, -0.10, 0.09]
    index = np.cumprod(
        [1 + r for r in IDX_R]
    )  # index level at each year-end, 1.10 at the end of year 1

    def ks_pme_at(T_: int, nav_T: float = 0.0) -> np.float64:
        """Kaplan-Schoar PME at valuation date T_.

        Index-deflated LP distributions plus residual NAV, over deflated calls. Calls and
        distributions are the LP's net-of-fee and net-of-carry cash flows; NAV is the LP's share
        after accrued carry; the index is a total-return level observed on the same dates.
        """
        num = sum(lp_eu[t] / index[t] for t in range(T_ + 1)) + nav_T / index[T_]
        den = sum(calls[t] / index[t] for t in range(T_ + 1))
        return np.float64(num / den)

    ks_pme = ks_pme_at(T - 1)
    report.ok(
        "KS-PME 1.23 at liquidation (year 8 index, NAV 0): distributions and calls discounted by"
        " the index",
        round(ks_pme, 2) == 1.23 and close(rows3[-1].nav, 0.0, 1e-12),
        f"PME {ks_pme:.4f}",
    )
    pme4_nav = ks_pme_at(4, rows3[4].nav)
    pme4_no_nav = ks_pme_at(4)
    report.ok(
        "interim PME at the end of year 4 includes the LP's residual NAV: 1.10; leaving NAV out"
        " gives 0.56, which treats unrealised value as lost",
        round(pme4_nav, 2) == 1.10 and round(pme4_no_nav, 2) == 0.56,
        f"with NAV {pme4_nav:.4f}, without {pme4_no_nav:.4f}",
    )
    bench = (110.0 / 1.10) / (100.0 / 1.0)
    report.ok(
        "benchmark-matching case: contribute 100 at t = 0, no distributions, NAV 110 at t = 1 with"
        " the index up 10%: PME = (0 + 110/1.10) / (100/1.00) = 1 exactly; the distributions-only"
        " formula would give 0",
        close(bench, 1.0) and close(0.0 / (100.0 / 1.0), 0.0),
    )
    pme_irr = irr(lp_eu / index - calls / index)
    report.ok(
        "the IRR of the index-deflated flows (5.67% a year) is a money-weighted excess return; it"
        " is not the fund's IRR (11.71%) less the index's annualised return",
        round(pme_irr * 100, 2) == 5.67
        and abs(pme_irr - (net_irr - (index[-1] ** (1 / (T - 1)) - 1))) > 0.001,
        f"direct alpha {pme_irr:.4f}",
    )
    g_c = 0.05
    flat_index = (1 + g_c) ** np.arange(T)
    r_defl = irr(lp_eu / flat_index - calls / flat_index)
    report.ok(
        "with a constant 5% index the deflated IRR is the geometric excess (1 + IRR)/(1.05) - 1 ="
        " 6.39%, not the arithmetic 11.71% - 5% = 6.71%",
        close(r_defl, (1 + net_irr) / (1 + g_c) - 1, 1e-9)
        and round(r_defl * 100, 2) == 6.39
        and round((net_irr - g_c) * 100, 2) == 6.71,
    )


def check_valuation(report: CheckReport) -> None:
    """Part 4: the venture capital method (Novaro) and an LBO (Corran)."""
    print(
        "== part 4: valuing venture and buyout investments - the venture capital method and an LBO"
        " (Novaro, Corran)"
    )
    INV, TARGET, YEARS, EXIT_EQ, OLD_SHARES = 8.0, 0.45, 5, 200.0, 1.0  # EUR m; shares in millions
    required = INV * (1 + TARGET) ** YEARS
    stake_exit = required / EXIT_EQ
    retention = (1 - 0.20) * (1 - 0.15)
    stake_now = stake_exit / retention
    post = INV / stake_now
    pre = post - INV
    new_shares = OLD_SHARES * stake_now / (1 - stake_now)
    price = INV / new_shares
    report.ok(
        "Novaro: 8 at a 45% target over five years must become 51.28; with exit equity of 200 that"
        " is 25.64% at exit; later rounds selling 20% and 15% leave a retention of 0.68, so 37.70%"
        " now: post-money 21.22, pre-money 13.22",
        round(required, 2) == 51.28
        and round(stake_exit * 100, 2) == 25.64
        and close(retention, 0.68)
        and round(stake_now * 100, 2) == 37.70
        and round(post, 2) == 21.22
        and round(pre, 2) == 13.22,
    )
    report.ok(
        "1.0m existing shares: 0.605m new shares at 13.22 a share; price x existing shares ="
        " pre-money; new / total = stake",
        round(new_shares, 3) == 0.605
        and round(price, 2) == 13.22
        and close(price * OLD_SHARES, pre, 1e-9)
        and close(new_shares / (OLD_SHARES + new_shares), stake_now, 1e-12),
    )
    report.ok(
        "dividing by (1 + 0.20)(1 + 0.15), as a formula with dilution measured differently would,"
        " gives 18.58% instead of the 37.70% needed: the dilution convention must match",
        round(stake_exit / (1.20 * 1.15) * 100, 2) == 18.58
        and stake_exit / (1.20 * 1.15) < stake_exit < stake_now,
    )

    UNI = [("unitranche", 250.0, 0.09, 0.0)]
    SM = [("senior", 175.0, 0.07, 0.0), ("mezzanine", 75.0, 0.07, 0.05)]
    u, sm = CORRAN.run(UNI), CORRAN.run(SM)
    report.ok(
        "Corran at 9.0x EBITDA of 50 (EV 450, fees 10) with 250 of unitranche: equity 210 grows to"
        " 425.30 at a 9.0x exit after five years of 6% EBITDA growth - MOIC 2.03, IRR 15.16%",
        close(u.eq0, 210.0)
        and round(u.eqx, 2) == 425.30
        and round(u.moic, 2) == 2.03
        and round(u.irr * 100, 2) == 15.16,
    )
    growth_part = (u.path[-1].ebitda - E0) * M_IN
    paydown = 250.0 - u.path[-1].debt
    report.ok(
        "value bridge: EBITDA growth x 9.0 = 152.20, debt repaid 73.10, fees -10.00, multiple"
        " change 0: together the 215.30 equity gain",
        round(growth_part, 2) == 152.20
        and round(paydown, 2) == 73.10
        and close(growth_part + paydown - FEES, u.eqx - u.eq0, 1e-9),
    )
    low_exit = CORRAN.model_copy(update={"exit_multiple": 8.0}).run(UNI)
    report.ok(
        "exiting at 8.0x instead of 9.0x cuts the MOIC to 1.71; the same deal with senior and"
        " mezzanine debt returns 2.03x as well",
        round(low_exit.moic, 2) == 1.71 and round(sm.moic, 2) == 2.03,
    )
    m_star = brentq(
        lambda m: (
            CORRAN.model_copy(update={"entry_multiple": m, "exit_multiple": m}).run(UNI).irr - 0.22
        ),
        5.5,
        9.0,
    )
    report.ok(
        "the deal clears a 22% target IRR only if entry and exit are both about 6.9x EBITDA"
        " (sponsor's maximum price)",
        round(m_star, 1) == 6.9,
        f"{m_star:.3f}",
    )


def check_private_debt(report: CheckReport) -> None:
    """Part 5: private debt credit analysis - Corran's unitranche against senior plus mezzanine."""
    print(
        "== part 5: private debt credit analysis - Corran's unitranche against senior plus"
        " mezzanine"
    )
    E1 = 53.0
    uni_int, sm_int = 0.09 * 250, 0.07 * 175 + 0.07 * 75
    ufcf1 = 0.5 * E1
    report.ok(
        "entry: leverage 5.0x, loan to value 55.6%; year-1 interest cover 2.36x (unitranche, 9%"
        " cash) against 3.03x (7% senior and 7% cash on mezzanine, which also accrues 5% PIK)",
        close(250 / E0, 5.0)
        and round(250 / 450 * 100, 1) == 55.6
        and round(E1 / uni_int, 2) == 2.36
        and round(E1 / sm_int, 2) == 3.03,
    )
    blend = (0.07 * 175 + 0.12 * 75) / 250
    report.ok(
        "all-in cost: senior plus mezzanine 8.5% including PIK against 9.0% for the unitranche;"
        " debt service cover (unlevered FCF + tax shield) / cash interest 1.43x for the bullet"
        " unitranche",
        round(blend * 100, 1) == 8.5 and round((ufcf1 + 0.25 * uni_int) / uni_int, 2) == 1.43,
    )
    report.ok(
        "a 20% EBITDA fall takes leverage to 6.25x, breaching a 6.0x covenant, while unitranche"
        " interest cover is still 1.88x",
        close(250 / (0.8 * E0), 6.25) and round(0.8 * E1 / uni_int, 2) == 1.88,
    )


def check_special_situations(report: CheckReport) -> None:
    """Part 6: Halden Retail's recovery waterfall and a loan-to-own position."""
    print(
        "== part 6: special situations - Halden Retail's recovery waterfall and a loan-to-own"
        " position"
    )
    SENIOR_TO_UNSECURED = sum(c for k, c in CLAIMS if k != "unsecured")

    rec = {ev: HALDEN.recoveries(ev) for ev in (220.0, 250.0, 255.0, 300.0, 350.0)}
    report.ok(
        "absolute priority at EV 300: DIP, administrative and senior claims paid in full;"
        " unsecured recover 33.3%; old equity nothing; distributions sum to EV",
        rec[300.0]["senior secured"] == 1.0
        and round(rec[300.0]["unsecured"] * 100, 1) == 33.3
        and rec[300.0]["equity"] == 0.0
        and close(sum(rec[300.0][k] * c for k, c in CLAIMS) + rec[300.0]["equity"], 300.0),
    )
    report.ok(
        "threshold: claims senior to the bonds are 40 + 10 + 200 = 250; at 250 the bonds get"
        " nothing and the senior class is just paid; at 255 the bonds still receive 5 (3.3%) and"
        " remain the fulcrum",
        close(SENIOR_TO_UNSECURED, 250.0)
        and rec[250.0]["senior secured"] == 1.0
        and rec[250.0]["unsecured"] == 0.0
        and close(rec[255.0]["unsecured"] * 150.0, 5.0)
        and HALDEN.fulcrum(255.0) == "unsecured"
        and HALDEN.fulcrum(249.0) == "senior secured",
    )
    report.ok(
        "below 250 the senior class becomes the fulcrum: at 220 it recovers 85% and the bonds"
        " nothing; at 350 the bonds recover 66.7%",
        round(rec[220.0]["senior secured"] * 100, 1) == 85.0
        and rec[220.0]["unsecured"] == 0.0
        and HALDEN.fulcrum(220.0) == "senior secured"
        and round(rec[350.0]["unsecured"] * 100, 1) == 66.7,
    )
    junior_dip = [
        ("senior secured", 200.0),
        ("DIP", 40.0),
        ("administrative", 10.0),
        ("unsecured", 150.0),
    ]
    report.ok(
        "boundary on the DIP's priority: with only a junior lien on encumbered assets (364(c)(3))"
        " and no carve-out, the senior lenders' collateral comes first; at EV 220 the senior class"
        " is paid in full, the DIP receives 20 of 40 and administrative claims nothing, against"
        " 85% for the senior class under the priming assumption",
        RecoveryWaterfall(claims=tuple(junior_dip)).recoveries(220.0)["senior secured"] == 1.0
        and close(RecoveryWaterfall(claims=tuple(junior_dip)).recoveries(220.0)["DIP"] * 40.0, 20.0)
        and RecoveryWaterfall(claims=tuple(junior_dip)).recoveries(220.0)["administrative"] == 0.0
        and round(HALDEN.recoveries(220.0)["senior secured"] * 100, 1) == 85.0,
    )
    face, cost = 100.0, 20.0
    new_equity = 300.0 - (40.0 + 10.0) - 200.0
    report.ok(
        "loan-to-own: an exit facility of 50 repays the DIP and administrative claims and the 200"
        " senior debt is reinstated, leaving 50 of new equity for the bonds; 100 of the 150 face"
        " bought at 20 becomes 33.3, a 66.7% gain",
        close(new_equity, 50.0)
        and round(face / 150.0 * new_equity, 1) == 33.3
        and round((face / 150.0 * new_equity) / cost - 1, 3) == 0.667,
    )

    fund_yes = ClassVote(ballots=((100.0, True), *[(5.0, False)] * 10))
    fund_no = ClassVote(ballots=((100.0, False), *[(5.0, True)] * 10))
    report.ok(
        "voting (1126(c)): the fund's 100 of 150 is two-thirds in amount, but one holder against"
        " ten voting no fails the number test, so the class rejects; voting no, the fund blocks"
        " acceptance (50/150 in amount) even with ten yeses",
        not fund_yes.accepts() and not fund_no.accepts() and close(100.0 / 150.0, 2 / 3),
    )
    few = ClassVote(ballots=((100.0, True), (25.0, True), (25.0, False)))
    report.ok(
        "with only three holders voting, the fund and one other accepting (125/150 in amount, 2 of"
        " 3 in number) carries the class",
        few.accepts(),
    )

    report.ok(
        "confirmation (1129(b)) differs from class acceptance: a plan that reinstates the senior"
        " debt leaves it unimpaired (1124(2)), so if the bonds reject there is no accepting"
        " impaired class (1129(a)(10)) and no cramdown; if the senior lenders are impaired (new"
        " terms) and accept, the plan can be confirmed over the bonds' rejection provided old"
        " equity receives nothing",
        not PlanConfirmation(impaired_accepting_classes=0, dissenting_impaired=True).confirmable()
        and PlanConfirmation(impaired_accepting_classes=1, dissenting_impaired=True).confirmable()
        and not PlanConfirmation(
            impaired_accepting_classes=1, dissenting_impaired=True, junior_gets_value=True
        ).confirmable(),
    )


def check_smoothing(report: CheckReport, rng: np.random.Generator) -> None:
    """Part 7: smoothed reported returns, and the Geltner-Ross-Zisler unsmoothing."""
    print(
        "== part 7: smoothed reported returns - volatility, beta and the Geltner-Ross-Zisler"
        " unsmoothing"
    )
    PHI = 0.6
    report.ok(
        "an AR(1) smoother r*_t = (1 - phi) r_t + phi r*_t-1 with phi 0.6 reports variance (1 -"
        " phi)/(1 + phi) = 0.25 of the true one: volatility halved",
        close((1 - PHI) / (1 + PHI), 0.25),
    )
    n = 40_000
    mkt = rng.normal(0.02, 0.08, n)
    true = 0.01 + 1.0 * mkt + rng.normal(0, 0.06, n)
    rep = np.empty(n)
    rep[0] = true[0]
    for t in range(1, n):
        rep[t] = (1 - PHI) * true[t] + PHI * rep[t - 1]
    phi_hat = np.corrcoef(rep[1:], rep[:-1])[0, 1]
    unsm = (rep[1:] - phi_hat * rep[:-1]) / (1 - phi_hat)

    def beta(y: Floats, x: Floats) -> np.float64:
        return np.float64(np.cov(y, x)[0, 1] / np.var(x, ddof=1))

    report.ok(
        "simulation (quarterly, true vol 10%, beta 1.0): reported vol about 5% and contemporaneous"
        " beta about 0.4; estimated phi 0.60 and unsmoothing restore vol and beta within 3%",
        bool(
            abs(np.std(rep) / np.std(true) - 0.5) < 0.02
            and abs(beta(rep, mkt) - 0.4) < 0.02
            and abs(phi_hat - PHI) < 0.01
            and abs(np.std(unsm) / np.std(true[1:]) - 1) < 0.03
            and abs(beta(unsm, mkt[1:]) - 1.0) < 0.03
        ),
        f"vol ratio {np.std(rep) / np.std(true):.3f}, beta {beta(rep, mkt):.3f}, phi {phi_hat:.3f},"
        f" unsmoothed vol ratio {np.std(unsm) / np.std(true[1:]):.3f}, beta"
        f" {beta(unsm, mkt[1:]):.3f}",
    )
    sharpe_rep = rep.mean() / np.std(rep)
    sharpe_true = true.mean() / np.std(true)
    report.ok(
        "the reported Sharpe ratio is about twice the true one, because the mean is unchanged and"
        " volatility halved",
        abs(sharpe_rep / sharpe_true - 2.0) < 0.1,
        f"{sharpe_rep / sharpe_true:.3f}",
    )


def check_allocation(report: CheckReport) -> None:
    """Part 8: private against public in an allocation, on reported and unsmoothed inputs."""
    print(
        "== part 8: private against public in a strategic allocation - reported against unsmoothed"
        " inputs"
    )
    MU = np.array(
        [0.045, 0.075, 0.105]
    )  # bonds, public equity, private equity (assumed: 3 points over public)
    RF = 0.03

    COV_REP = cov([0.06, 0.17, 0.09], [[1, 0.1, 0.1], [0.1, 1, 0.45], [0.1, 0.45, 1]])
    COV_UNS = cov([0.06, 0.17, 0.26], [[1, 0.1, 0.1], [0.1, 1, 0.85], [0.1, 0.85, 1]])

    def mv_weights(c: Floats, lam: float = 3.0) -> Floats:
        def utility_loss(w: Floats) -> float:
            loss: float = -(w @ MU - 0.5 * lam * w @ c @ w)
            return loss

        res = minimize(
            utility_loss,
            np.ones(3) / 3,
            bounds=[(0, 1)] * 3,
            constraints=[{"type": "eq", "fun": budget}],
            method="SLSQP",
            options={"ftol": 1e-14},
        )
        return res.x

    w_rep, w_uns = mv_weights(COV_REP), mv_weights(COV_UNS)
    report.ok(
        "reported inputs (PE vol 9%, correlation 0.45, beta 0.24): Sharpe 0.83 and the optimiser"
        " puts 100% in private equity, whose true volatility is 26%",
        bool(
            round((MU[2] - RF) / 0.09, 2) == 0.83
            and round(COV_REP[2, 1] / COV_REP[1, 1], 2) == 0.24
            and w_rep[2] > 0.999
            and round(np.float64(np.sqrt(w_rep @ COV_UNS @ w_rep)), 2) == 0.26
        ),
    )
    report.ok(
        "unsmoothed inputs (vol 26%, correlation 0.85, beta 1.30): Sharpe 0.29 against 0.26 for"
        " public equity; weights 67% bonds, 1% public equity, 32% private equity, portfolio"
        " volatility 9.7%",
        round((MU[2] - RF) / 0.26, 2) == 0.29
        and round((MU[1] - RF) / 0.17, 2) == 0.26
        and round(COV_UNS[2, 1] / COV_UNS[1, 1], 2) == 1.30
        and [round(v, 2) for v in w_uns] == [0.67, 0.01, 0.32]
        and round(np.float64(np.sqrt(w_uns @ COV_UNS @ w_uns)), 3) == 0.097,
        ", ".join(f"{v:.4f}" for v in w_uns),
    )


def main() -> int:
    """Print the versions, then run the eight parts with one report.

    Worked numbers of the entries in compendium/private-capital-allocator/. Every fund, company and
    market path is hypothetical: Brook Relative Value (a hedge fund), Ashby Fund I (a buyout fund),
    Novaro (a venture company), Corran Industrial (a buyout target), Halden Retail (a distressed
    company). Rules and conventions come from Ang (2014), Ippolito (2020), Demaria et al. (2021),
    Metrick and Yasuda (2011), Kaplan and Schoar (2005), Getmansky, Lo and Makarov (2004) and
    Gompers, Kaplan and Mukharlyamov (2016); their published figures are quoted in the entries, not
    reproduced here.

    Independent routes: hedge-fund fees year by year against the NAV identity (gross value = fees +
    net value); the European waterfall tier by tier against the closed-form carry share (20% of fund
    profit after full catch-up); the American waterfall deal by deal against the whole-fund carry,
    giving the clawback; fund IRRs by root-finding against NPV = 0 checks; the KS-PME against its
    definition with an index path; the VC method's stake against the pre- and post-money identities;
    the LBO equity value bridge (EBITDA growth + multiple change + deleveraging) against the exit
    equity less the entry equity; private-debt ratios from their definitions; the distressed
    recovery waterfall against absolute priority totals and the 250 threshold; class voting under
    1126(c) against confirmation under 1129(a)(10) and (b); the PME with residual NAV against an
    index-matching benchmark case; desmoothed volatility against the closed form for an AR(1)
    smoother.

    Part 2 passes Ashby Fund I's flows and LP distributions to part 3.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
    report = CheckReport()
    check_hedge_fund_fees(report)
    flows = check_waterfalls(report)
    check_fund_metrics(report, flows)
    check_valuation(report)
    check_private_debt(report)
    check_special_situations(report)
    check_smoothing(report, np.random.default_rng(SEED))
    check_allocation(report)
    print(f"\n{report.count} checks executed")
    if report.failures:
        print("FAILED:", report.failures)
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
