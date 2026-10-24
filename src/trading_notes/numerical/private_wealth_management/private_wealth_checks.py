"""Private wealth: human capital, taxes, planning, retirement, protection and transfers."""

import datetime
import math
import sys
from typing import Final

import numpy as np
import scipy
from numpy.typing import NDArray
from scipy.optimize import brentq

from trading_notes.numerical.report import CheckReport
from trading_notes.numerical.tolerance import close
from trading_notes.numerical.wealth_planning.household_plan import (
    GoalsPlan,
    Gompertz,
    HumanCapital,
    MarketAssumptions,
    annuity,
)
from trading_notes.numerical.wealth_preservation.tax_drag import AssetLocation, TaxDrag, wash_sale
from trading_notes.numerical.wealth_preservation.us_income_tax import JointIncomeTax
from trading_notes.numerical.wealth_transfer.transfer_rules import (
    EstateTax,
    InheritanceTax,
    PresenceDays,
    TradingPlan,
)

type Floats = NDArray[np.float64]


# US 2026 federal parameters (Rev. Proc. 2025-32 secs. 3.14, 4.01, 4.03, 4.14, 4.37-4.38, 4.42;
# Notice 2025-67) sec. 4.01 Table 1, married filing jointly: (lower edge of the band, rate)
US_MFJ_BRACKETS: Final = [
    (0, 0.10),
    (24_800, 0.12),
    (100_800, 0.22),
    (211_400, 0.24),
    (403_550, 0.32),
    (512_450, 0.35),
    (768_700, 0.37),
]
US_MFJ_ZERO_MAX: Final = 98_900
US_MFJ_15_MAX: Final = 613_700  # sec. 4.03 maximum zero and 15% rate amounts, joint
US_MFJ_STD_DED: Final = 32_200
US_NIIT_JOINT: Final = 250_000  # sec. 4.14; sec. 1411(b)(1), not indexed
US_TOP_ORD: Final = 0.37
US_NIIT: Final = 0.038
US_LTCG_TOP: Final = 0.20
US_ORD_INV: Final = US_TOP_ORD + US_NIIT  # 40.8% on interest for a top-bracket investor
US_QD_INV: Final = US_LTCG_TOP + US_NIIT  # 23.8% on qualified dividends and long-term gains
US_GIFT_EXCL: Final = 19_000
US_BASIC_EXCL: Final = 15_000_000
US_ESTATE_RATE: Final = 0.40
US_401K: Final = 24_500
US_401K_CATCHUP: Final = 8_000
US_IRA: Final = 7_500
US_EXPAT_TAX_TEST: Final = 211_000
US_EXPAT_EXCLUSION: Final = 910_000
# UK 2026 to 2027 (GOV.UK rates pages, updated 6 April 2026)
UK_PA: Final = 12_570
UK_BASIC_BAND: Final = 37_700
UK_DIV: Final = {"basic": 0.1075, "higher": 0.3575, "additional": 0.3935}
UK_CGT_LOW: Final = 0.18
UK_CGT_HIGH: Final = 0.24
UK_CGT_AEA: Final = 3_000
UK_NRB: Final = 325_000
UK_RNRB: Final = 175_000
UK_IHT: Final = 0.40
UK_ISA: Final = 20_000
UK_PENSION_AA: Final = 60_000
UK_LSA: Final = 268_275

E40: Final = 180_000.0
G: Final = 0.01
R_SAFE: Final = 0.035
# Adaeze's after-tax real earnings at 40, growth, discount rate, retirement age (the household
# retires together)
RET: Final = 62
FIN: Final = 600_000.0
RESERVE: Final = 60_000.0
POLICY: Final = FIN - RESERVE  # the goal-funding policy portfolio; the reserve sits outside it
SAVE: Final = 50_000.0
YEARS: Final = 22  # planned saving at each year-end until retirement
EDU: Final = [(8, 200_000.0), (10, 200_000.0)]  # years from now (children now 10 and 8)
MU_E: Final = 0.05
SD_E: Final = 0.17
MU_B: Final = 0.015
SD_B: Final = 0.06
RHO_EB: Final = 0.2  # real capital market assumptions
MARKETS: Final = MarketAssumptions(mu_e=MU_E, sd_e=SD_E, mu_b=MU_B, sd_b=SD_B, rho=RHO_EB)
ADAEZE: Final = HumanCapital(earnings=E40, growth=G, rate=R_SAFE, retirement=RET)


SPEND: Final = 150_000.0
SOCSEC: Final = 60_000.0
YEARS_RET: Final = 30
pv_ret_at62: Final = (SPEND - SOCSEC) * annuity(0.03, YEARS_RET)
OKAFORS: Final = GoalsPlan(
    policy=POLICY, save=SAVE, years=YEARS, education=tuple(EDU), retirement_need=pv_ret_at62
)
US_TAX: Final = JointIncomeTax(
    brackets=tuple((float(lo), rate) for lo, rate in US_MFJ_BRACKETS),
    zero_max=US_MFJ_ZERO_MAX,
    fifteen_max=US_MFJ_15_MAX,
    standard_deduction=US_MFJ_STD_DED,
    niit_threshold=US_NIIT_JOINT,
    niit_rate=US_NIIT,
)
DRAG: Final = TaxDrag(rate=0.06, years=20)


MODE: Final = 88.0
DISP: Final = 10.0  # Gompertz modal age and dispersion, illustrative
MORTALITY: Final = Gompertz(mode=MODE, dispersion=DISP)


BONDS: Final = 500_000.0
STOCKS: Final = 500_000.0
YB: Final = 0.045
DY: Final = 0.02
GY: Final = 0.05


UK_TAPER_THRESHOLD: Final = 2_000_000.0  # IHTA 1984 s. 8D; IHTM46023 (updated 7 April 2026)
LOCATION: Final = AssetLocation(
    bonds=BONDS, stocks=STOCKS, bond_yield=YB, dividend_yield=DY, price_growth=GY
)
IHT: Final = InheritanceTax(residence_band=UK_RNRB, taper_threshold=UK_TAPER_THRESHOLD)


def check_human_capital(report: CheckReport) -> None:
    """Part 1: human capital, financial capital and economic net worth."""
    print(
        "== part 1: human capital, financial capital and economic net worth over the life cycle"
        " (the Okafors)"
    )
    report.ok(
        "Adaeze's human capital (after-tax 180k real at 40, +1% a year, to retirement at 62,"
        " discounted at 3.5%) is 3.00m at 40, 2.02m at 50, 0.42m at 60; running it to 65 would"
        " overstate it at 40 by 0.30m (3.29m)",
        round(ADAEZE.value(40) / 1e6, 2) == 3.00
        and round(ADAEZE.value(50) / 1e6, 2) == 2.02
        and round(ADAEZE.value(60) / 1e6, 2) == 0.42
        and round(ADAEZE.model_copy(update={"retirement": 65}).value(40) / 1e6, 2) == 3.29,
    )
    report.ok(
        "recursion: HC(40) = (earnings in year 1 + HC(41)) / 1.035",
        close(ADAEZE.value(40), (E40 + ADAEZE.value(41)) / (1 + R_SAFE), 1e-6),
    )
    report.ok(
        "the same income discounted at 6% (equity-like risk) is worth 2.36m: riskier income is"
        " less valuable human capital",
        round(ADAEZE.model_copy(update={"rate": 0.06}).value(40) / 1e6, 2) == 2.36
        and ADAEZE.model_copy(update={"rate": 0.06}).value(40) < ADAEZE.value(40),
    )
    g60 = MARKETS.mix(0.60)[2]
    fc = {40: FIN}
    for k in range(1, YEARS + 1):
        fc[40 + k] = RESERVE + OKAFORS.project(g60, years=k)
    report.ok(
        "with the recommended 60/40 policy earning its expected compound 3.03% real, 50k saved a"
        " year and the two education payments made, financial capital (reserve included) rises"
        " from 0.60m at 40 to 0.95m at 50 (after both education payments), 1.83m at 60 and 2.04m"
        " at 62, while human capital falls to zero",
        round(g60 * 100, 2) == 3.03
        and round(fc[50] / 1e6, 2) == 0.95
        and round(fc[60] / 1e6, 2) == 1.83
        and round(fc[62] / 1e6, 2) == 2.04,
    )
    pv_edu = sum(c / 1.035**t for t, c in EDU)
    enw40 = FIN + ADAEZE.value(40) - 400_000 - pv_edu
    report.ok(
        "economic net worth at 40: financial 0.60m + human capital 3.00m - mortgage 0.40m - PV of"
        " the 200k education payments in 8 and 10 years (0.29m) = 2.90m; human capital is 83% of"
        " gross economic assets",
        round(pv_edu / 1e6, 2) == 0.29
        and round(enw40 / 1e6, 2) == 2.90
        and round(ADAEZE.value(40) / (ADAEZE.value(40) + FIN), 2) == 0.83,
    )
    # Total-wealth allocation: Adaeze's HC bond-like; Tunde's HC (2.0m) 50% equity-like.
    # Target 40% equity on total wealth.
    HC_T = 2_000_000.0
    total = FIN + ADAEZE.value(40) + HC_T
    eq_needed = 0.40 * total - 0.5 * HC_T
    report.ok(
        "capacity view: with Tunde's 2.0m of commission income counted as half equity, a 40%"
        " equity target on total wealth (5.60m) needs 1.24m of financial equity, more than the"
        " whole 0.54m policy portfolio; capacity alone would put all of it in equities, so"
        " willingness, not capacity, is the binding constraint",
        round(total / 1e6, 2) == 5.60 and round(eq_needed / 1e6, 2) == 1.24 and eq_needed > POLICY,
    )


def check_taxes_inflation(report: CheckReport) -> None:
    """Part 2: taxes and inflation in investment decisions (US and UK 2026)."""
    print("== part 2: taxes and inflation in investment decisions (US 2026 and UK 2026-27)")
    sim = 100.0
    for _ in range(DRAG.years):
        sim *= 1 + DRAG.rate * (1 - US_ORD_INV)
    report.ok(
        "100 at 6% for 20 years: 320.71 tax-free; 200.99 if taxed annually at 40.8% (US top rate"
        " on interest); 268.18 if gains are deferred and taxed once at 23.8%; a year-by-year"
        " simulation agrees",
        round(100 * (1 + DRAG.rate) ** DRAG.years, 2) == 320.71
        and round(DRAG.accrual(US_ORD_INV), 2) == 200.99
        and round(DRAG.deferred(US_QD_INV), 2) == 268.18
        and close(sim, DRAG.accrual(US_ORD_INV), 1e-9),
    )
    report.ok(
        "the deferred gain's effective annual tax rate is 15.7%, well below its 23.8% statutory"
        " rate, because the tax is paid only at the end",
        round(1 - ((DRAG.deferred(US_QD_INV) / 100) ** (1 / DRAG.years) - 1) / DRAG.rate, 3)
        == 0.157,
    )
    report.ok(
        "UK additional-rate taxpayer: dividends taxed annually at 39.35% leave 204.39 against"
        " 267.74 for gains deferred at 24%; a 1% annual wealth tax leaves 262.31",
        round(DRAG.accrual(UK_DIV["additional"]), 2) == 204.39
        and round(DRAG.deferred(UK_CGT_HIGH), 2) == 267.74
        and round(100 * ((1 + DRAG.rate) * 0.99) ** DRAG.years, 2) == 262.31,
    )
    INFL = 0.025
    real_pre = (1 + DRAG.rate) / (1 + INFL) - 1
    real_post = (1 + DRAG.rate * (1 - US_ORD_INV)) / (1 + INFL) - 1
    report.ok(
        "with 2.5% inflation, a 6% interest return taxed at 40.8% earns 1.03% real: the tax takes"
        " 70% of the 3.41% real return, because it falls on the inflation component too",
        round(real_post * 100, 2) == 1.03
        and round(real_pre * 100, 2) == 3.41
        and round(1 - real_post / real_pre, 2) == 0.70,
    )


def check_okafor_ips(report: CheckReport) -> None:
    """Part 3: the Okafors' required return and IPS."""
    print("== part 3: the Okafors' required return and IPS")
    req = brentq(OKAFORS.funded_gap, -0.05, 0.20)
    req_double = brentq(lambda rr: OKAFORS.funded_gap(rr, p0=FIN), -0.05, 0.20)
    report.ok(
        "retirement at 62 needing 150k real a year for 30 years, 60k from Social Security: PV at"
        " 62 of the 90k gap at a 3% real rate is 1.76m",
        round(pv_ret_at62 / 1e6, 2) == 1.76,
    )
    report.ok(
        "with the 60k reserve held outside, the 0.54m policy portfolio, 50k saved a year for 22"
        " years and the two 200k education payments need a real return of 2.30%; counting the"
        " reserve as goal capital too (0.60m) would give 1.96% while also spending it on"
        " emergencies, which double counts it",
        round(req * 100, 2) == 2.30 and round(req_double * 100, 2) == 1.96,
        f"{req:.4%}",
    )
    report.ok(
        "independent route: projecting the policy portfolio year by year at 2.30%, with saving and"
        " both education payments, reaches exactly the 1.76m retirement need at 62",
        close(OKAFORS.project(req), pv_ret_at62, 1e-3),
    )
    cands = {w: MARKETS.mix(w) for w in (0.7, 0.6, 0.4)}
    report.ok(
        "allocation against the goals (real, illustrative assumptions): 70/30, 60/40 and 40/60"
        " have expected compound returns of 3.22%, 3.03% and 2.57%, all above 2.30%; projected"
        " surpluses over the 1.76m need at 62 of 0.28m, 0.22m and 0.08m",
        [round(cands[w][2] * 100, 2) for w in (0.7, 0.6, 0.4)] == [3.22, 3.03, 2.57]
        and [round((OKAFORS.project(cands[w][2]) - pv_ret_at62) / 1e6, 2) for w in (0.7, 0.6, 0.4)]
        == [0.28, 0.22, 0.08],
    )
    report.ok(
        "allocation against willingness: the Okafors would sell after a one-year loss of about"
        " 15%; the one-in-twenty one-year return is -15.1% for 70/30 (at the limit), -13.4% for"
        " 60/40 and -10.2% for 40/60",
        [round(cands[w][3] * 100, 1) for w in (0.7, 0.6, 0.4)] == [-15.1, -13.4, -10.2],
    )
    tx = US_TAX.household()
    report.ok(
        "2026 joint brackets (Rev. Proc. 2025-32 sec. 4.01 Table 1): the band formula reproduces"
        " the published tax of 116,896 at 512,450 and 206,583.50 at 768,700; the 15% ceiling of"
        " 613,700 (sec. 4.03) lies inside the 35% band, so the ordinary band alone cannot fix the"
        " rate on dividends and gains",
        close(US_TAX.ordinary(512_450), 116_896, 1e-6)
        and close(US_TAX.ordinary(768_700), 206_583.5, 1e-6)
        and 512_450 < US_MFJ_15_MAX < 768_700,
    )
    report.ok(
        "the Okafors' 2026 return: AGI 669,400; taxable income 637,200 after the 32,200 standard"
        " deduction; ordinary taxable income 571,200 (35% band); of the 66,000 of qualified"
        " dividends and long-term gains stacked on top, 42,500 fill the 15% layer to 613,700 and"
        " 23,500 are taxed at 20%; income tax 148,533.50; NIIT 3.8% of the 68,400 of investment"
        " income (less than MAGI over 250k) = 2,599.20",
        close(tx.agi, 669_400)
        and close(tx.ti, 637_200)
        and close(tx.ord, 571_200)
        and 512_450 < tx.ord < 768_700
        and close(tx.at0, 0.0)
        and close(tx.at15, 42_500)
        and close(tx.at20, 23_500)
        and close(tx.tax, 148_533.5, 1e-6)
        and close(tx.niit, 2_599.2, 1e-6),
        f"tax {tx.tax:,.2f}, NIIT {tx.niit:,.2f}",
    )
    report.ok(
        "independent route: integrating the preferential layers piece by piece above ordinary"
        " income gives the same tax; the old inference (all 66,000 at 15%) understates it by 1,175"
        " = 23,500 x 5 points",
        close(US_TAX.stacked(tx.ti, 66_000), tx.tax, 1e-6)
        and close(tx.tax - (US_TAX.ordinary(tx.ord) + 0.15 * 66_000), 1_175, 1e-6),
    )
    mtax = {
        k: (lambda t: t.tax + t.niit)(US_TAX.household(**{k: v + 1.0})) - (tx.tax + tx.niit)
        for k, v in (("wages", 650_000.0), ("interest", 2_400.0), ("ltcg", 60_000.0))
    }
    report.ok(
        "marginal federal rates by finite difference: a further dollar of gains or qualified"
        " dividends costs 23.8% (20% + NIIT), not 18.8%; a further dollar of wages costs 40% (35%"
        " plus the 5 points of one gain dollar pushed from 15% to 20%), and of interest 43.8%:"
        " each deferred 401(k) dollar saves 40%, and bonds belong in tax-deferred accounts",
        round(mtax["ltcg"], 3) == 0.238
        and round(mtax["wages"], 3) == 0.400
        and round(mtax["interest"], 3) == 0.438,
        f"{ {k: round(v, 4) for k, v in mtax.items()} }",
    )
    b_low, b_at, b_high = (
        US_TAX.capital_gains(o + 40_000, 40_000) for o in (571_200, 573_700, 613_700)
    )
    report.ok(
        "boundary cases: with 40,000 of gains on 571,200 of ordinary income (total 611,200) all"
        " gains are at 15%; at exactly 613,700 still all at 15%, and one more dollar of gain is"
        " taxed at 20%; with ordinary income at 613,700 every gain dollar is at 20%; with ordinary"
        " income of 60,000 the first 38,900 of gains are at 0%; the Okafors' 66,000 would all be"
        " at 15% only if ordinary income fell to 547,700 (613,700 - 66,000)",
        close(US_TAX.capital_gains(547_700 + 66_000, 66_000)[2], 66_000)
        and close(US_TAX.capital_gains(547_701 + 66_000, 66_000)[3], 1.0, 1e-6)
        and close(b_low[2], 40_000)
        and close(b_low[3], 0.0)
        and close(b_at[2], 40_000)
        and close(US_TAX.capital_gains(613_701, 40_001)[0] - b_at[0], 0.20, 1e-6)
        and close(b_high[3], 40_000)
        and close(US_TAX.capital_gains(100_000, 40_000)[1], 38_900),
    )
    report.ok(
        "NIIT boundaries (sec. 1411(a)(1)): MAGI of 240,000 owes none; MAGI of 260,000 with 30,000"
        " of investment income owes 3.8% of the 10,000 excess (380), not of the 30,000; the"
        " Okafors' MAGI exceeds 250,000 by more than their investment income, so the whole 68,400"
        " is taxed",
        US_TAX.household(
            wages=240_000.0, deferral=30_000.0, interest=0.0, qdiv=0.0, ltcg=30_000.0
        ).niit
        == 0.0
        and close(
            US_TAX.household(
                wages=260_000.0, deferral=30_000.0, interest=0.0, qdiv=0.0, ltcg=30_000.0
            ).niit,
            380.0,
            1e-9,
        )
        and tx.agi - US_NIIT_JOINT > 68_400,
    )


def check_fee_models(report: CheckReport) -> None:
    """Part 4: wealth-management fee models over 20 years on 2m."""
    print("== part 4: wealth-management fee models over 20 years on 2m")
    A0, GROSS, YRS = 2_000_000.0, 0.06, 20
    aum = flat = comm = A0
    fees_aum = fees_flat = fees_comm = 0.0
    for y in range(YRS):
        f = 0.01 * aum * (1 + GROSS)
        aum = aum * (1 + GROSS) - f
        fees_aum += f
        ff = 12_000 * 1.02**y
        flat = flat * (1 + GROSS) - ff
        fees_flat += ff
        fc_ = 0.0075 * comm * (1 + GROSS)
        comm = comm * (1 + GROSS) - fc_
        fees_comm += fc_
    report.ok(
        "1% of assets charged at each year-end: 2m grows to 5.25m (closed form 2m x (1.06 x"
        " 0.99)^20); a 12k flat retainer rising 2% a year leaves 5.90m; trail commissions and"
        " product costs of 0.75% leave 5.52m",
        round(aum / 1e6, 2) == 5.25
        and close(aum, A0 * (1.06 * 0.99) ** 20, 1e-3)
        and round(flat / 1e6, 2) == 5.90
        and round(comm / 1e6, 2) == 5.52,
    )
    report.ok(
        "the asset-based fee costs 1.17m of terminal wealth against no fee (6.41m); the flat fee"
        " 0.52m",
        round((A0 * 1.06**20 - aum) / 1e6, 2) == 1.17
        and round((A0 * 1.06**20 - flat) / 1e6, 2) == 0.52,
    )


def check_goals_liquidity(report: CheckReport) -> float:
    """Part 5: goals-based plan and liquidity tiers (the Okafors)."""
    print("== part 5: goals-based plan and liquidity tiers (the Okafors)")
    SPENDING_NOW = 120_000.0
    reserve = 0.5 * SPENDING_NOW
    edu_bucket = (
        200_000 / 1.03**2
    )  # first payment brought within 2 years later; here PV of a payment in 2 years at 3%
    pv_resources, pv_goals, fr35 = OKAFORS.funded_ratio(0.035)
    save_needed = brentq(lambda sv: OKAFORS.funded_ratio(0.015, sv)[2] - 1, 0, 200_000)
    report.ok(
        "liquidity tiers: a six-month emergency reserve of 60k in cash, outside the 540k policy"
        " portfolio (600k in total); education money moves to a cash or short-bond bucket once a"
        " payment is within two years (188.5k for a 200k payment at 3%)",
        close(reserve, RESERVE)
        and close(POLICY + RESERVE, FIN)
        and round(edu_bucket / 1e3, 1) == 188.5,
    )
    report.ok(
        "funded ratio at a 3.5% discount rate: PV of the policy portfolio and savings 1.30m"
        " against PV of goals 1.12m: 1.16; at a 1.5% rate the ratio falls to 0.91 and the plan is"
        " short unless saving rises to about 58.1k a year",
        round(pv_resources / 1e6, 2) == 1.30
        and round(pv_goals / 1e6, 2) == 1.12
        and round(fr35, 2) == 1.16
        and round(OKAFORS.funded_ratio(0.015)[2], 2) == 0.91
        and round(save_needed / 1e3, 1) == 58.1,
    )
    return fr35


def check_mortality(report: CheckReport) -> None:
    """Part 6: mortality, disability and longevity (illustrative Gompertz)."""
    print("== part 6: mortality, disability and longevity (illustrative Gompertz mortality)")
    p65_85 = MORTALITY.survival(65, 20)
    p65_95 = MORTALITY.survival(65, 30)
    report.ok(
        "Gompertz mortality (mode 88, dispersion 10): a 65-year-old reaches 80 with 71%"
        " probability, 85 with 53% and 95 with 15%",
        round(MORTALITY.survival(65, 15), 2) == 0.71
        and round(p65_85, 2) == 0.53
        and round(p65_95, 2) == 0.15,
    )
    ann_factor = sum(MORTALITY.survival(65, t) / 1.03**t for t in range(1, 51))
    cert_factor = annuity(0.03, 20)
    report.ok(
        "a life annuity of 1 a year from 65 costs 13.98 at 3% (fair, no loading); a bond ladder to"
        " 85 (20 years) costs 14.88 and runs out while the retiree is alive with 53% probability;"
        " the annuity pays 7.15% of premium for life against 6.72% for 20 years from the ladder",
        round(ann_factor, 2) == 13.98
        and round(cert_factor, 2) == 14.88
        and round(1 / ann_factor * 100, 2) == 7.15
        and round(1 / cert_factor * 100, 2) == 6.72,
    )
    ins_need = 0.75 * ADAEZE.value(40) - 300_000
    report.ok(
        "Adaeze's life insurance need: 75% of her 3.00m human capital (the part that supports the"
        " family) less 0.30m of assets set aside = 1.95m of term cover to 62, falling as she ages",
        round(ins_need / 1e6, 2) == 1.95 and 0.75 * ADAEZE.value(50) - 300_000 < ins_need,
    )
    report.ok(
        "disability cover of 60% of 250k pre-tax pay (150k a year) to 62 replaces 83% of her 180k"
        " after-tax pay if the benefit is untaxed (individually paid premiums)",
        round(150_000 / 180_000, 2) == 0.83,
    )


def check_tax_management(report: CheckReport) -> None:
    """Part 7: tax management - asset location and loss harvesting (US 2026)."""
    print("== part 7: tax management - asset location and loss harvesting (US 2026)")
    good = LOCATION.after_tax(True, US_ORD_INV, US_QD_INV, US_QD_INV)
    bad = LOCATION.after_tax(False, US_ORD_INV, US_QD_INV, US_QD_INV)
    v1, b1, _ = LOCATION.stock_ledger(1, US_QD_INV, US_QD_INV)
    report.ok(
        "one-year reconciliation of the taxable stock account: 500k rises 25,000 in price; the"
        " 10,000 dividend bears 2,380 of tax and 7,620 is reinvested, so value is 532,620, basis"
        " 507,620 and the unrealised gain exactly the 25,000 price rise; in the IRA the whole"
        " dividend is reinvested (535,000)",
        close(v1, 532_620.0, 1e-6)
        and close(b1, 507_620.0, 1e-6)
        and close(v1 - b1, 25_000.0, 1e-6)
        and close(LOCATION.stock_ledger(1, 0.0, 0.0)[0], 535_000.0, 1e-6),
    )
    v20, b20, _ = LOCATION.stock_ledger(20, US_QD_INV, US_QD_INV)
    report.ok(
        "closed form: the taxable stock grows by 1 + g + d(1 - t) = 1.06524 a year, and its basis"
        " is the original cost plus every reinvested after-tax dividend",
        close(v20, STOCKS * (1 + GY + DY * (1 - US_QD_INV)) ** 20, 1e-6)
        and close(
            b20,
            STOCKS
            + sum(
                STOCKS * (1 + GY + DY * (1 - US_QD_INV)) ** k * DY * (1 - US_QD_INV)
                for k in range(20)
            ),
            1e-6,
        ),
    )
    earlier_tx = (
        STOCKS * (1 + DY) ** 20 * (1 + GY) ** 20
    )  # the earlier multiplicative taxable convention, at zero tax
    report.ok(
        "with every tax at zero, location cannot change gross performance: both placements end"
        " with 500k x 1.045^20 + 500k x 1.07^20 = 3,140,699; the earlier convention (taxable"
        " stocks compounding (1 + d)(1 + g), IRA stocks 1 + d + g) would have shown a 36,488"
        " location effect even without tax",
        close(
            LOCATION.after_tax(True, 0.0, 0.0, 0.0, t_ira=0.0),
            LOCATION.after_tax(False, 0.0, 0.0, 0.0, t_ira=0.0),
            1e-6,
        )
        and round(LOCATION.after_tax(True, 0.0, 0.0, 0.0, t_ira=0.0)) == 3_140_699
        and round(earlier_tx - STOCKS * 1.07**20) == 36_488,
    )
    report.ok(
        "500k of bonds (4.5%) and 500k of stocks (2% yield on opening value, 5% price growth), 20"
        " years, top-bracket taxes, IRA taxed at 24% on withdrawal: bonds in the IRA and stocks in"
        " the taxable account end with 2,454,619 after tax against 2,316,409 the other way, an"
        " advantage of 138,211",
        round(good) == 2_454_619 and round(bad) == 2_316_409 and good > bad,
        f"{good:,.0f} vs {bad:,.0f}",
    )
    harvest = 50_000 * US_QD_INV
    report.ok(
        "harvesting a 50k loss against long-term gains saves 11,900 now; if the lower basis is"
        " taxed at the same rate in 10 years, the gain is only the deferral, worth 5,255 at 6%; if"
        " held until death and stepped up (s. 1014), the whole 11,900",
        close(harvest, 11_900.0) and round(harvest * (1 - 1 / 1.06**10)) == 5_255,
    )
    report.ok(
        "the wash-sale rule (s. 1091(a)) disallows the loss if substantially identical stock is"
        " bought within 30 days before or after the sale: a repurchase on day 31 after keeps the"
        " loss, on day 30 loses it; buying a different fund tracking a different index keeps"
        " exposure without the rule applying (interpretation)",
        not wash_sale(100, [131])
        and wash_sale(100, [130])
        and wash_sale(100, [70])
        and not wash_sale(100, [69]),
    )


def check_allocation_review(report: CheckReport, fr35: float) -> None:
    """Part 8: allocation, reporting and review."""
    print("== part 8: allocation, reporting and review")
    v0, flow = POLICY, SAVE  # the Okafors' policy portfolio; the year's saving arrives at mid-year
    mid = v0 * 1.05  # +5.0% in the first half
    v1 = (mid + flow) * 1.064  # +6.4% in the second half
    twr = (mid / v0) * (v1 / (mid + flow)) - 1
    mwr = brentq(lambda rr: v0 * (1 + rr) + flow * (1 + rr) ** 0.5 - v1, -0.5, 1)
    report.ok(
        "the Okafors' first year: 540,000 grows to 567,000 by mid-year, 50,000 is added, and the"
        " year ends at 656,488. TWR 11.72% (chain-linked) measures the manager; MWR 11.78%"
        " measures the client's experience; against an assumed 11.0% benchmark the manager added"
        " 0.72 points",
        close(v1, 656_488.0, 1e-6)
        and round(twr * 100, 2) == 11.72
        and round(mwr * 100, 2) == 11.78
        and round((twr - 0.11) * 100, 2) == 0.72,
        f"TWR {twr:.4%}, MWR {mwr:.4%}",
    )
    res1 = v1 + sum(SAVE / 1.035**t for t in range(1, YEARS))
    goals1 = sum(c / 1.035 ** (t - 1) for t, c in EDU) + pv_ret_at62 / 1.035 ** (YEARS - 1)
    report.ok(
        "progress against the plan (treating the year's return as real): the funded ratio at 3.5%"
        " rises from 1.16 to 1.20 after the year",
        round(fr35, 2) == 1.16 and round(res1 / goals1, 2) == 1.20,
    )


def check_retirement_saving(report: CheckReport) -> None:
    """Part 9: retirement saving across jurisdictions."""
    print("== part 9: retirement saving across jurisdictions")
    contrib, t_now, t_ret, g_ret, yrs = 24_500.0, 0.35, 0.24, 0.06, 25
    trad = contrib * (1 + g_ret) ** yrs * (1 - t_ret)
    roth_cost = contrib * (
        1 - t_now
    )  # after-tax cost of a traditional contribution; a Roth of equal cost
    roth = roth_cost * (1 + g_ret) ** yrs
    report.ok(
        "US: a 24,500 pre-tax 401(k) deferral at a 35% marginal rate, withdrawn at 24% after 25"
        " years at 6%, leaves 79,915 after tax; a Roth contribution of equal after-tax cost"
        " (15,925) leaves 68,348: traditional wins when the retirement rate is lower; at equal"
        " rates the two are identical",
        round(trad) == 79_915
        and round(roth) == 68_348
        and close(contrib * (1 + g_ret) ** yrs * (1 - t_now), roth, 1e-6),
    )
    net = 10_000.0
    gross = net / 0.8  # basic-rate relief at source
    extra_relief = gross * 0.2  # higher-rate relief claimed through self assessment
    pot = gross * 1.06**25
    after = pot * 0.25 + pot * 0.75 * (1 - 0.20)
    isa = (net - extra_relief) * 1.06**25
    report.ok(
        "UK: a higher-rate taxpayer pays 10,000 into a personal pension; basic-rate relief grosses"
        " it up to 12,500 and 2,500 more is reclaimed, so the net cost is 7,500; after 25 years at"
        " 6% the pot is 53,648; 25% tax-free and the rest at 20% leaves 45,601, against 32,189"
        " from the same 7,500 in an ISA",
        close(gross, 12_500.0)
        and close(extra_relief, 2_500.0)
        and round(pot) == 53_648
        and round(after) == 45_601
        and round(isa) == 32_189,
    )
    report.ok(
        "the UK pension's effective tax on withdrawal is 15% (25% tax-free, 75% at 20%); the lump"
        " sum is capped at 268,275 (the lump sum allowance)",
        close(0.75 * 0.20, 0.15) and UK_LSA == 268_275,
    )
    report.ok(
        "2026 US limits: 401(k) 24,500 (+8,000 at 50+), IRA 7,500; UK annual allowance 60,000;"
        " RMDs from 73 (75 for those reaching 74 after 2032)",
        US_401K == 24_500
        and US_401K_CATCHUP == 8_000
        and US_IRA == 7_500
        and UK_PENSION_AA == 60_000,
    )


def check_protection(report: CheckReport) -> None:
    """Part 10: protecting human capital and purchasing power."""
    print("== part 10: protecting human capital and purchasing power")
    emp_w, emp_vol, mkt_vol, rho = 0.40, 0.45, 0.16, 0.5
    port_vol_conc = math.sqrt(
        (emp_w * emp_vol) ** 2
        + ((1 - emp_w) * mkt_vol) ** 2
        + 2 * emp_w * (1 - emp_w) * rho * emp_vol * mkt_vol
    )
    report.ok(
        "Tunde holds 40% of liquid assets in his employer's stock (volatility 45%, correlation 0.5"
        " with a 16%-volatility market): portfolio volatility 24.3% against 16% diversified, while"
        " his pay depends on the same company",
        round(port_vol_conc * 100, 1) == 24.3,
    )
    real_value = 50_000 / 1.03**20
    report.ok(
        "inflation: a level nominal pension of 50k loses 45% of its purchasing power in 20 years"
        " at 3% (27.7k in today's money); an inflation-linked income does not",
        round(real_value / 1e3, 1) == 27.7 and round(1 - real_value / 50_000, 2) == 0.45,
    )
    usd_share, gbp_up = 0.30, 0.10
    report.ok(
        "Margaret Hartley spends in sterling with 30% of assets in US dollars: a 10% rise in"
        " sterling costs 2.7% of her portfolio in sterling (0.30 x (1 - 1/1.10)); hedging half of"
        " it halves the effect",
        round(usd_share * (1 - 1 / (1 + gbp_up)) * 100, 1) == 2.7
        and close(0.5 * usd_share * (1 - 1 / (1 + gbp_up)), usd_share * (1 - 1 / (1 + gbp_up)) / 2),
    )


def check_residence(report: CheckReport) -> None:
    """Part 11: residence and citizenship."""
    print("== part 11: residence and citizenship")
    days = PresenceDays(current=150, previous=120, before_previous=120)
    res, w = days.us_substantial_presence(), days.us_weighted_days()
    short = PresenceDays(current=120, previous=120, before_previous=120)
    report.ok(
        "US substantial presence test (s. 7701(b)(3)): 150 days this year, 120 in each of the two"
        " previous years: 150 + 40 + 20 = 210 weighted days, resident; 120/120/120 gives 160, not"
        " resident",
        res and close(w, 210.0) and not short.us_substantial_presence(),
    )
    report.ok(
        "UK sufficient ties test (RDR3 Tables A and B): a leaver who was resident in the last 3"
        " years and spends 100 days needs 2 ties to stay resident; an arriver with no recent"
        " residence needs 3",
        PresenceDays(current=100).uk_ties_needed(resident_recently=True) == 2
        and PresenceDays(current=100).uk_ties_needed(resident_recently=False) == 3,
    )
    gain_mtm = 3_500_000.0
    taxable = gain_mtm - US_EXPAT_EXCLUSION
    report.ok(
        "US expatriation of a covered expatriate in 2026: 3.5m of unrealised gains treated as"
        " realised (s. 877A), less the 910k exclusion: 2.59m taxable, 616k at 23.8%",
        close(taxable, 2_590_000.0) and round(taxable * US_QD_INV / 1e3) == 616,
    )


def check_complex_situations(report: CheckReport) -> None:
    """Part 12: complex situations - founders and executives."""
    print("== part 12: complex situations - founders and executives")
    gain, basis_fd = 20_000_000.0, 1_000_000.0
    cap = max(15_000_000.0, 10 * basis_fd)
    excluded = min(gain, cap) * 1.0  # held 5+ years, stock acquired after 4 July 2025: 100%
    report.ok(
        "QSBS (s. 1202, stock acquired after 4 July 2025, held 5 years): a 20m gain on 1m of basis"
        " excludes the greater of 15m and 10 x basis = 15m; the remaining 5m is taxed at 23.8%"
        " (1.19m), against 4.76m with no exclusion",
        close(excluded, 15_000_000.0)
        and round((gain - excluded) * US_QD_INV / 1e6, 2) == 1.19
        and round(gain * US_QD_INV / 1e6, 2) == 4.76,
    )
    report.ok(
        "held 3 years the exclusion is 50%, 4 years 75%: 7.5m and 11.25m of the capped 15m",
        close(0.5 * cap, 7_500_000.0) and close(0.75 * cap, 11_250_000.0),
    )
    plan = TradingPlan(adopted=datetime.date(2026, 3, 4))
    report.ok(
        "an officer's Rule 10b5-1 plan adopted 4 March 2026: with the 10-Q filed 7 May, trading"
        " may start on 2 June (90 days); if the 10-Q is filed late on 5 June, on 9 June (two"
        " business days after it); never later than 2 July (120 days)",
        plan.first_trade_date(datetime.date(2026, 5, 7)) == datetime.date(2026, 6, 2)
        and plan.first_trade_date(datetime.date(2026, 6, 5)) == datetime.date(2026, 6, 9)
        and plan.first_trade_date(datetime.date(2026, 8, 1)) == datetime.date(2026, 7, 2),
    )


def check_transfers(report: CheckReport) -> None:
    """Part 13: transferring wealth - gifts, bequests and philanthropy."""
    print("== part 13: transferring wealth - gifts, bequests and philanthropy")
    V0, B0, VD = 5_000_000.0, 1_000_000.0, 10_000_000.0
    # other assets at death, so the estate is taxable at the 40% margin in both cases
    OTHER = 30_000_000.0
    # A: keep the asset; it is in the estate at 10m with a stepped-up basis (s. 1014).
    estate_tax = EstateTax(exemption=US_BASIC_EXCL)
    tax_a = estate_tax.tax(OTHER + VD)
    heirs_a = OTHER + VD - tax_a
    # B: give it now at 5m, using 5m of the unified exemption (Rev. Proc. 2025-32 sec. 3.14);
    # carryover basis 1m (s. 1015).
    tax_b = estate_tax.tax(OTHER, exemption_used=V0)
    heirs_b_hold = OTHER - tax_b + VD
    heirs_b_sell = heirs_b_hold - US_QD_INV * (VD - B0)
    report.ok(
        "a 5m asset (basis 1m) that will be 10m at death, in an estate with 30m of other assets:"
        " keeping it, heirs receive 30.0m after 10.0m of estate tax; giving it now uses 5m of"
        " exemption, so estate tax is 8.0m and heirs receive 32.0m if they keep the asset, but"
        " 29.86m if they sell it and pay 23.8% on the 9m carryover gain",
        close(tax_a, 10_000_000.0)
        and close(heirs_a, 30_000_000.0)
        and close(tax_b, 8_000_000.0)
        and close(heirs_b_hold, 32_000_000.0)
        and round(heirs_b_sell / 1e6, 2) == 29.86,
    )
    report.ok(
        "the gift saves 40% of the 5m growth (2.0m) but forgoes the step-up, costing 2.14m if"
        " heirs sell: worth doing only if the asset will not be sold, or grows faster; in an"
        " estate below the 15m exemption the gift saves nothing and only loses the step-up",
        close(heirs_b_hold - heirs_a, 2_000_000.0)
        and round((heirs_a - heirs_b_sell) / 1e6, 2) == 0.14
        and estate_tax.tax(VD) == 0.0,
    )
    report.ok(
        "residence nil-rate band taper (175k allowance, none transferred, a qualifying home worth"
        " at least the band): 175k at an estate of 2.0m, 125k at 2.1m, nothing at 2.35m or above;"
        " a home worth 100k caps it at 100k",
        close(IHT.residence_nil_rate_band(2_000_000, 900_000), 175_000.0)
        and close(IHT.residence_nil_rate_band(2_100_000, 900_000), 125_000.0)
        and close(IHT.residence_nil_rate_band(2_350_000, 900_000), 0.0)
        and close(IHT.residence_nil_rate_band(2_400_000, 900_000), 0.0)
        and close(IHT.residence_nil_rate_band(1_900_000, 100_000), 100_000.0),
    )
    # One chronology: Margaret gives 500k to her son (annual exemptions already used) and dies
    # 4.5 years later, leaving a 2.4m estate, including a home worth 900k, to her children.
    # She has no band transferred from a former spouse.
    GIFT, YRS_TO_DEATH, ESTATE, HOME = 500_000.0, 4.5, 2_400_000.0, 900_000.0
    nrb_used_by_gift = min(GIFT, UK_NRB)
    tax_gift = (GIFT - nrb_used_by_gift) * IHT.taper_rate(YRS_TO_DEATH)
    nrb_left = UK_NRB - nrb_used_by_gift
    tax_estate = UK_IHT * max(0.0, ESTATE - IHT.residence_nil_rate_band(ESTATE, HOME) - nrb_left)
    tax_no_gift = UK_IHT * max(
        0.0, ESTATE + GIFT - IHT.residence_nil_rate_band(ESTATE + GIFT, HOME) - UK_NRB
    )
    report.ok(
        "the gift fails because Margaret dies 4.5 years after making it (the 4 to 5 year band):"
        " the 325k nil-rate band covers the first part, and 175k is taxed at 24%: 42,000, against"
        " 70,000 within 3 years and nothing after 7",
        IHT.taper_rate(4.5) == 0.24
        and close(tax_gift, 42_000.0)
        and close((GIFT - UK_NRB) * IHT.taper_rate(2.9), 70_000.0)
        and IHT.taper_rate(7.0) == 0.0,
    )
    report.ok(
        "the estate: the gift has consumed the whole nil-rate band, and 2.4m tapers the residence"
        " band to zero, so all 2.4m is taxed at 40%: 960,000 (reusing the 325k band, as the"
        " earlier example did, would give 830,000)",
        close(nrb_left, 0.0)
        and close(tax_estate, 960_000.0)
        and close(UK_IHT * (ESTATE - UK_NRB), 830_000.0),
    )
    report.ok(
        "total 1,002,000 against 1,030,000 had she kept the 500k (estate 2.9m): the gift saved"
        " exactly its taper relief, 16% of 175k = 28,000, because it only moved the nil-rate band"
        " forward in time",
        close(tax_gift + tax_estate, 1_002_000.0)
        and close(tax_no_gift, 1_030_000.0)
        and close(tax_no_gift - tax_gift - tax_estate, (0.40 - 0.24) * (GIFT - UK_NRB)),
    )
    report.ok(
        "had the estate at death been 2.1m instead, 125k of residence band would remain and the"
        " tax would be 790,000; leaving 10% of the net estate to charity lowers the rate to 36%",
        close(
            UK_IHT * (2_100_000 - IHT.residence_nil_rate_band(2_100_000, HOME) - nrb_left),
            790_000.0,
        )
        and close(UK_IHT - 0.04, 0.36),
    )
    pv_payments = 50_000 * annuity(0.05, 20)
    report.ok(
        "a CRAT of 1m paying 5% (50k) a year for 20 years: payments worth 623k at a 5% rate leave"
        " a charitable remainder of 377k, above the 10% minimum (s. 664(d)(1)); a private"
        " foundation must distribute about 5% of non-charitable assets a year (s. 4942(e))",
        round(pv_payments / 1e3) == 623 and 1_000_000 - pv_payments > 100_000,
    )
    report.ok(
        "US annual exclusion 19,000 a donee in 2026 (194,000 to a non-citizen spouse); basic"
        " exclusion 15m; gifting 19,000 to each of 6 grandchildren for 10 years moves 1.14m out of"
        " the estate with no use of the exemption",
        US_GIFT_EXCL * 6 * 10 == 1_140_000,
    )


def main() -> int:
    """Print the versions, then run the 13 parts with one report.

    Worked numbers of the entries in compendium/private-wealth-management/. Every client is
    hypothetical: the Okafors (United States, tax year 2026), Margaret Hartley (United Kingdom, tax
    year 2026 to 2027), Maya Chen (a US citizen moving to London) and Luis Rivera (a US founder).
    Tax parameters are the published 2026 US federal figures (Rev. Proc. 2025-32; Notice 2025-67; 26
    U.S.C.) and the 2026 to 2027 UK figures on GOV.UK; state, local and Scottish taxes, phase-outs
    and credits are ignored. Mortality follows a Gompertz law chosen for illustration, not a life
    table.

    The Okafor case is one linked base case. Financial assets of 600k = a 60k emergency reserve in
    cash held OUTSIDE the policy portfolio + a 540k policy portfolio that funds the goals; the
    reserve is never counted as goal-funding capital. Adaeze (40) and Tunde (42) retire together
    when she is 62, in 22 years, so her human capital runs to 62. The plan counts planned saving of
    50k a year (end of each year, mostly 401(k) deferrals) and two 200k education payments at the
    ends of years 8 and 10; amounts are in today's dollars, retirement spending is before income tax
    on withdrawals, and the taxable account's tax drag is ignored in the funding model. Their 2026
    federal return (married filing jointly, stated assumptions): wages 650k (Adaeze 250k, Tunde 400k
    of salary, commissions and vested RSUs) less 49k of 401(k) deferrals; 2.4k of interest on the
    reserve; 6k of qualified dividends and 60k of net long-term gains (vested employer shares sold
    to stay below 10%); standard deduction 32.2k (Rev. Proc. 2025-32 sec. 4.14). Ordinary taxable
    income 571.2k lies in the 35% band (sec. 4.01 Table 1: 512,450 to 768,700), but the band does
    not fix the rate on dividends and gains: under 26 U.S.C. 1(h)(1) and 1(j)(5) they are stacked on
    top of ordinary income and taxed at 15% only up to taxable income of 613,700 (sec. 4.03), 20%
    above, plus the 3.8% NIIT on the lesser of net investment income and MAGI above 250k (sec.
    1411). Capital market assumptions (illustrative, real): equity 5.0% expected, 17% volatility;
    bonds 1.5%, 6%; correlation 0.2. The asset-location client in part 7 is a separate, top-bracket
    US client.

    Independent routes: human capital by direct discounting against the backward recursion HC(x) =
    (e + HC(x+1))/(1+r); after-tax accumulation by formula against year-by-year simulation; the
    required return by root-finding against the funded-ratio identity; fees by year-by-year
    simulation against closed forms; annuity factors by summation against the survival integral;
    asset location by a year-by-year cash and basis ledger against the closed form, a zero-tax
    comparison and a one-year hand reconciliation; the Okafor funding by the required-return root
    against a forward projection at that return; the Roth and traditional comparison against the
    equal-rate identity; UK pension relief by the gross-up identity; the substantial presence test
    and UK ties by rule; QSBS exclusion against the statutory cap; gift against bequest by full
    after-tax terminal wealth; the UK gift and estate as one chronology against the no-gift estate,
    the difference being the taper relief; the residence nil-rate band taper against its boundary
    cases; the CRAT remainder by annuity factors; the Okafors' federal tax by the sec.
    1(h)(1)(A)-(D) formula against layer-by-layer stacking, the published cumulative bracket
    amounts, finite-difference marginal rates and boundary cases.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
    report = CheckReport()
    check_human_capital(report)
    check_taxes_inflation(report)
    check_okafor_ips(report)
    check_fee_models(report)
    fr35 = check_goals_liquidity(report)
    check_mortality(report)
    check_tax_management(report)
    check_allocation_review(report, fr35)
    check_retirement_saving(report)
    check_protection(report)
    check_residence(report)
    check_complex_situations(report)
    check_transfers(report)
    print(f"\n{report.count} checks executed")
    if report.failures:
        print("FAILED:", report.failures)
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
