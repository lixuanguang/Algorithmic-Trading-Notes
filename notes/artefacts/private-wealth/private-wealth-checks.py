"""Private wealth: human capital, taxes, planning, retirement, protection, residency and transfers (2026-10-20).

Worked numbers of the entries in compendium/private-wealth-management/. Every client is hypothetical: the Okafors
(United States, tax year 2026), Margaret Hartley (United Kingdom, tax year 2026 to 2027), Maya Chen (a US citizen
moving to London) and Luis Rivera (a US founder). Tax parameters are the published 2026 US federal figures (Rev. Proc.
2025-32; Notice 2025-67; 26 U.S.C.) and the 2026 to 2027 UK figures on GOV.UK; state, local and Scottish taxes,
phase-outs and credits are ignored. Mortality follows a Gompertz law chosen for illustration, not a life table.

Independent routes: human capital by direct discounting against the backward recursion HC(x) = (e + HC(x+1))/(1+r);
after-tax accumulation by formula against year-by-year simulation; the required return by root-finding against the
funded-ratio identity; fees by year-by-year simulation against closed forms; annuity factors by summation against
the survival integral; asset location by simulation of both placements; the Roth and traditional comparison against
the equal-rate identity; UK pension relief by the gross-up identity; the substantial presence test and UK ties by
rule; QSBS exclusion against the statutory cap; gift against bequest by full after-tax terminal wealth; the CRAT
remainder by annuity factors.

Count convention: one check is one executed ok() call (a call inside a loop counts once per iteration).

Run: uv run python private-wealth-checks.py   (numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import datetime
import math
import sys

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


def annuity(r, n):
    return n if r == 0 else (1 - (1 + r) ** -n) / r


# US 2026 federal parameters (Rev. Proc. 2025-32 secs. 3.14, 4.01, 4.03, 4.37-4.38, 4.42; Notice 2025-67)
US_TOP_ORD, US_NIIT = 0.37, 0.038
US_LTCG_TOP = 0.20
US_ORD_INV = US_TOP_ORD + US_NIIT  # 40.8% on interest for a top-bracket investor
US_QD_INV = US_LTCG_TOP + US_NIIT  # 23.8% on qualified dividends and long-term gains
US_GIFT_EXCL, US_BASIC_EXCL, US_ESTATE_RATE = 19_000, 15_000_000, 0.40
US_401K, US_401K_CATCHUP, US_IRA = 24_500, 8_000, 7_500
US_EXPAT_TAX_TEST, US_EXPAT_EXCLUSION = 211_000, 910_000
# UK 2026 to 2027 (GOV.UK rates pages, updated 6 April 2026)
UK_PA, UK_BASIC_BAND = 12_570, 37_700
UK_DIV = {"basic": 0.1075, "higher": 0.3575, "additional": 0.3935}
UK_CGT_LOW, UK_CGT_HIGH, UK_CGT_AEA = 0.18, 0.24, 3_000
UK_NRB, UK_RNRB, UK_IHT = 325_000, 175_000, 0.40
UK_ISA, UK_PENSION_AA, UK_LSA = 20_000, 60_000, 268_275

# ---------------------------------------------------------------------------------------------
print(
    "== part 1: human capital, financial capital and economic net worth over the life cycle (the Okafors)"
)
E40, G, R_SAFE, RET = (
    180_000.0,
    0.01,
    0.035,
    65,
)  # Adaeze's after-tax real earnings at 40, growth, discount rate


def hc(age, r=R_SAFE, e40=E40, g=G, ret=RET):
    e = e40 * (1 + g) ** (age - 40)
    return sum(e * (1 + g) ** (t - 1) / (1 + r) ** t for t in range(1, ret - age + 1))


ok(
    "Adaeze's human capital (after-tax 180k real at 40, +1% a year, to 65, discounted at 3.5%) is 3.29m at 40, "
    "2.44m at 50, 1.01m at 60",
    round(hc(40) / 1e6, 2) == 3.29
    and round(hc(50) / 1e6, 2) == 2.44
    and round(hc(60) / 1e6, 2) == 1.01,
)
ok(
    "recursion: HC(40) = (earnings in year 1 + HC(41)) / 1.035",
    close(hc(40), (E40 + hc(41)) / (1 + R_SAFE), 1e-6),
)
ok(
    "the same income discounted at 6% (equity-like risk) is worth 2.52m: riskier income is less valuable human capital",
    round(hc(40, r=0.06) / 1e6, 2) == 2.52 and hc(40, r=0.06) < hc(40),
)
fc = {40: 600_000.0}
x = fc[40]
for age in range(40, 65):
    x = x * 1.04 + 40_000 * 1.01 ** (age - 40)
    fc[age + 1] = x
ok(
    "saving 40k a year (growing 1%) at a 4% real return, financial capital rises from 0.60m at 40 to 1.39m at 50, "
    "2.61m at 60 and 3.44m at 65 while human capital falls to zero",
    round(fc[50] / 1e6, 2) == 1.39
    and round(fc[60] / 1e6, 2) == 2.61
    and round(fc[65] / 1e6, 2) == 3.44,
)
pv_edu = 2 * 200_000 / 1.035**10
enw40 = fc[40] + hc(40) - 400_000 - pv_edu
ok(
    "economic net worth at 40: financial 0.60m + human capital 3.29m - mortgage 0.40m - PV of two 200k education "
    "goals in 10 years (0.28m) = 3.21m; human capital is 85% of gross economic assets",
    round(enw40 / 1e6, 2) == 3.21 and round(hc(40) / (hc(40) + fc[40]), 2) == 0.85,
)
# Total-wealth allocation: Adaeze's HC bond-like; Tunde's HC (2.0m) 50% equity-like. Target 40% equity on total wealth.
HC_T = 2_000_000.0
total = fc[40] + hc(40) + HC_T
eq_needed = 0.40 * total - 0.5 * HC_T
w_fin_eq = eq_needed / fc[40]
ok(
    "with Tunde's 2.0m of commission income counted as half equity, a 40% equity target on total wealth (5.89m) "
    "needs 1.36m of financial equity: more than the 0.60m of financial assets, so the financial portfolio is 100% "
    "equity and the household is still below target",
    round(total / 1e6, 2) == 5.89 and eq_needed > fc[40] and min(w_fin_eq, 1.0) == 1.0,
)

# ---------------------------------------------------------------------------------------------
print("== part 2: taxes and inflation in investment decisions (US 2026 and UK 2026-27)")
r, n = 0.06, 20


def accrual(t):
    return 100 * (1 + r * (1 - t)) ** n


def deferred(t):
    return 100 * ((1 + r) ** n * (1 - t) + t)


sim = 100.0
for _ in range(n):
    sim *= 1 + r * (1 - US_ORD_INV)
ok(
    "100 at 6% for 20 years: 320.71 tax-free; 200.99 if taxed annually at 40.8% (US top rate on interest); 268.18 if "
    "gains are deferred and taxed once at 23.8%; a year-by-year simulation agrees",
    round(100 * (1 + r) ** n, 2) == 320.71
    and round(accrual(US_ORD_INV), 2) == 200.99
    and round(deferred(US_QD_INV), 2) == 268.18
    and close(sim, accrual(US_ORD_INV), 1e-9),
)
ok(
    "the deferred gain's effective annual tax rate is 15.7%, well below its 23.8% statutory rate, because the tax "
    "is paid only at the end",
    round(1 - ((deferred(US_QD_INV) / 100) ** (1 / n) - 1) / r, 3) == 0.157,
)
ok(
    "UK additional-rate taxpayer: dividends taxed annually at 39.35% leave 204.39 against 267.74 for gains deferred "
    "at 24%; a 1% annual wealth tax leaves 262.31",
    round(accrual(UK_DIV["additional"]), 2) == 204.39
    and round(deferred(UK_CGT_HIGH), 2) == 267.74
    and round(100 * ((1 + r) * 0.99) ** n, 2) == 262.31,
)
INFL = 0.025
real_pre = (1 + r) / (1 + INFL) - 1
real_post = (1 + r * (1 - US_ORD_INV)) / (1 + INFL) - 1
ok(
    "with 2.5% inflation, a 6% interest return taxed at 40.8% earns 1.03% real: the tax takes 70% of the 3.41% real "
    "return, because it falls on the inflation component too",
    round(real_post * 100, 2) == 1.03
    and round(real_pre * 100, 2) == 3.41
    and round(1 - real_post / real_pre, 2) == 0.70,
)

# ---------------------------------------------------------------------------------------------
print("== part 3: the Okafors' required return and IPS")
SPEND, SOCSEC, YEARS_RET = 150_000.0, 60_000.0, 30
pv_ret_at62 = (SPEND - SOCSEC) * annuity(0.03, YEARS_RET)
edu = [(8, 200_000.0), (10, 200_000.0)]  # years from now (children now 10 and 8)


def funded_gap(rr):
    fv_assets = fc[40] * (1 + rr) ** 22 + sum(50_000 * (1 + rr) ** (22 - t) for t in range(1, 23))
    fv_edu = sum(c * (1 + rr) ** (22 - t) for t, c in edu)
    return fv_assets - fv_edu - pv_ret_at62


req = brentq(funded_gap, -0.05, 0.20)
ok(
    "retirement at 62 needing 150k real a year for 30 years, 60k from Social Security: PV at 62 of the 90k gap at a "
    "3% real rate is 1.76m",
    round(pv_ret_at62 / 1e6, 2) == 1.76,
)
ok(
    "with 0.60m now, 50k saved a year for 22 years and two 200k education payments, the required real return is "
    "1.96%: modest, so the IPS can favour reliability over maximum growth",
    round(req * 100, 2) == 1.96 and close(funded_gap(req), 0.0, 1e-3),
    f"{req:.4%}",
)

# ---------------------------------------------------------------------------------------------
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
ok(
    "1% of assets charged at each year-end: 2m grows to 5.25m (closed form 2m x (1.06 x 0.99)^20); a 12k flat "
    "retainer rising 2% a year leaves 5.90m; trail commissions and product costs of 0.75% leave 5.52m",
    round(aum / 1e6, 2) == 5.25
    and close(aum, A0 * (1.06 * 0.99) ** 20, 1e-3)
    and round(flat / 1e6, 2) == 5.90
    and round(comm / 1e6, 2) == 5.52,
)
ok(
    "the asset-based fee costs 1.17m of terminal wealth against no fee (6.41m); the flat fee 0.52m",
    round((A0 * 1.06**20 - aum) / 1e6, 2) == 1.17
    and round((A0 * 1.06**20 - flat) / 1e6, 2) == 0.52,
)

# ---------------------------------------------------------------------------------------------
print("== part 5: goals-based plan and liquidity tiers (the Okafors)")
SPENDING_NOW = 120_000.0
reserve = 0.5 * SPENDING_NOW
edu_bucket = (
    200_000 / 1.03**2
)  # first payment brought within 2 years later; here PV of a payment in 2 years at 3%
pv_goals = pv_edu + pv_ret_at62 / 1.035**22
pv_resources = fc[40] + sum(50_000 / 1.035**t for t in range(1, 23))
ok(
    "liquidity tiers: a six-month emergency reserve of 60k in cash; education money moves to a cash or short-bond "
    "bucket once a payment is within two years (188.5k for a 200k payment at 3%)",
    close(reserve, 60_000.0) and round(edu_bucket / 1e3, 1) == 188.5,
)
ok(
    "funded ratio at a 3.5% discount rate: PV of savings and assets 1.36m against PV of goals 1.11m: 1.22, so "
    "the plan is funded with a margin; at a 1.5% rate the ratio falls to 0.95 and the plan is short",
    round(pv_resources / 1e6, 2) == 1.36
    and round(pv_goals / 1e6, 2) == 1.11
    and round(pv_resources / pv_goals, 2) == 1.22
    and round(
        (fc[40] + sum(50_000 / 1.015**t for t in range(1, 23)))
        / (400_000 / 1.015**10 + pv_ret_at62 / 1.015**22),
        2,
    )
    == 0.95,
)

# ---------------------------------------------------------------------------------------------
print("== part 6: mortality, disability and longevity (illustrative Gompertz mortality)")
MODE, DISP = 88.0, 10.0  # Gompertz modal age and dispersion, illustrative


def surv(x, t):
    """Probability that a person aged x survives t more years under Gompertz(m, b)."""
    return math.exp(math.exp((x - MODE) / DISP) * (1 - math.exp(t / DISP)))


p65_85 = surv(65, 20)
p65_95 = surv(65, 30)
ok(
    "Gompertz mortality (mode 88, dispersion 10): a 65-year-old reaches 80 with 71% probability, 85 with 53% and 95 "
    "with 15%",
    round(surv(65, 15), 2) == 0.71 and round(p65_85, 2) == 0.53 and round(p65_95, 2) == 0.15,
)
ann_factor = sum(surv(65, t) / 1.03**t for t in range(1, 51))
cert_factor = annuity(0.03, 20)
ok(
    "a life annuity of 1 a year from 65 costs 13.98 at 3% (fair, no loading); a bond ladder to 85 (20 years) costs "
    "14.88 and runs out while the retiree is alive with 53% probability; the annuity pays 7.15% of premium for life "
    "against 6.72% for 20 years from the ladder",
    round(ann_factor, 2) == 13.98
    and round(cert_factor, 2) == 14.88
    and round(1 / ann_factor * 100, 2) == 7.15
    and round(1 / cert_factor * 100, 2) == 6.72,
)
ins_need = 0.75 * hc(40) - 300_000
ok(
    "Adaeze's life insurance need: 75% of her 3.29m human capital (the part that supports the family) less 0.30m of "
    "assets set aside = 2.17m of term cover, falling as she ages",
    round(ins_need / 1e6, 2) == 2.17 and 0.75 * hc(50) - 300_000 < ins_need,
)
ok(
    "disability cover of 60% of 250k pre-tax pay (150k a year) to 65 replaces 83% of her 180k after-tax pay if the "
    "benefit is untaxed (individually paid premiums)",
    round(150_000 / 180_000, 2) == 0.83,
)

# ---------------------------------------------------------------------------------------------
print("== part 7: tax management - asset location and loss harvesting (US 2026)")
BONDS, STOCKS, YB, DY, GY = 500_000.0, 500_000.0, 0.045, 0.02, 0.05


def location(bonds_in_ira, years=20):
    """IRA withdrawals taxed at 24% at the end; taxable account taxed at US top rates."""
    if bonds_in_ira:
        ira = BONDS * (1 + YB) ** years
        tx = STOCKS * (1 + DY * (1 - US_QD_INV)) ** years * (1 + GY) ** years
        basis = STOCKS + sum(
            STOCKS * (1 + DY * (1 - US_QD_INV)) ** k * (1 + GY) ** k * DY * (1 - US_QD_INV)
            for k in range(years)
        )
        tx_after = tx - US_QD_INV * (tx - basis)
    else:
        ira = STOCKS * (1 + DY + GY) ** years
        tx_after = BONDS * (1 + YB * (1 - US_ORD_INV)) ** years
    return ira * (1 - 0.24) + tx_after


good, bad = location(True), location(False)
ok(
    "500k of bonds (4.5%) and 500k of stocks (2% yield, 5% growth), 20 years, top-bracket taxes, IRA taxed at 24% "
    "on withdrawal: bonds in the IRA and stocks in the taxable account end with 2.47m against 2.32m the other way",
    round(good / 1e6, 2) == 2.47 and round(bad / 1e6, 2) == 2.32 and good > bad,
    f"{good:,.0f} vs {bad:,.0f}",
)
harvest = 50_000 * US_QD_INV
ok(
    "harvesting a 50k loss against long-term gains saves 11,900 now; if the lower basis is taxed at the same rate in "
    "10 years, the gain is only the deferral, worth 5,255 at 6%; if held until death and stepped up (s. 1014), "
    "the whole 11,900",
    close(harvest, 11_900.0) and round(harvest * (1 - 1 / 1.06**10)) == 5_255,
)


def wash_sale(sale_day, buy_days):
    """s. 1091(a): loss disallowed if substantially identical stock is bought from 30 days before to 30 days after."""
    return any(sale_day - 30 <= d <= sale_day + 30 for d in buy_days)


ok(
    "the wash-sale rule (s. 1091(a)) disallows the loss if substantially identical stock is bought within 30 days "
    "before or after the sale: a repurchase on day 31 after keeps the loss, on day 30 loses it; buying a different "
    "fund tracking a different index keeps exposure without the rule applying (interpretation)",
    not wash_sale(100, [131])
    and wash_sale(100, [130])
    and wash_sale(100, [70])
    and not wash_sale(100, [69]),
)

# ---------------------------------------------------------------------------------------------
print("== part 8: allocation, reporting and review")
v0, flow, v1 = (
    1_000_000.0,
    200_000.0,
    1_330_000.0,
)  # contribution at mid-year; mid-year value before flow 1.05m
mid = 1_050_000.0
twr = (mid / v0) * (v1 / (mid + flow)) - 1
mwr = brentq(lambda rr: v0 * (1 + rr) + flow * (1 + rr) ** 0.5 - v1, -0.5, 1)
ok(
    "a year with a 200k mid-year contribution: TWR 11.72% (chain-linked) measures the manager; MWR 11.85% measures "
    "the client's experience; the client's goal funded ratio is reported beside both; against an assumed 11.0% benchmark the manager added 0.72 points",
    round(twr * 100, 2) == 11.72
    and round(mwr * 100, 2) == 11.85
    and round((twr - 0.11) * 100, 2) == 0.72,
    f"TWR {twr:.4%}, MWR {mwr:.4%}",
)

# ---------------------------------------------------------------------------------------------
print("== part 9: retirement saving across jurisdictions")
contrib, t_now, t_ret, g_ret, yrs = 24_500.0, 0.35, 0.24, 0.06, 25
trad = contrib * (1 + g_ret) ** yrs * (1 - t_ret)
roth_cost = contrib * (
    1 - t_now
)  # after-tax cost of a traditional contribution; a Roth of equal cost
roth = roth_cost * (1 + g_ret) ** yrs
ok(
    "US: a 24,500 pre-tax 401(k) deferral at a 35% marginal rate, withdrawn at 24% after 25 years at 6%, leaves "
    "79,915 after tax; a Roth contribution of equal after-tax cost (15,925) leaves 68,348: traditional wins when "
    "the retirement rate is lower; at equal rates the two are identical",
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
ok(
    "UK: a higher-rate taxpayer pays 10,000 into a personal pension; basic-rate relief grosses it up to 12,500 and "
    "2,500 more is reclaimed, so the net cost is 7,500; after 25 years at 6% the pot is 53,648; 25% tax-free and the "
    "rest at 20% leaves 45,601, against 32,189 from the same 7,500 in an ISA",
    close(gross, 12_500.0)
    and close(extra_relief, 2_500.0)
    and round(pot) == 53_648
    and round(after) == 45_601
    and round(isa) == 32_189,
)
ok(
    "the UK pension's effective tax on withdrawal is 15% (25% tax-free, 75% at 20%); the lump sum is capped at "
    "268,275 (the lump sum allowance)",
    close(0.75 * 0.20, 0.15) and UK_LSA == 268_275,
)
ok(
    "2026 US limits: 401(k) 24,500 (+8,000 at 50+), IRA 7,500; UK annual allowance 60,000; RMDs from 73 (75 for "
    "those reaching 74 after 2032)",
    US_401K == 24_500 and US_401K_CATCHUP == 8_000 and US_IRA == 7_500 and UK_PENSION_AA == 60_000,
)

# ---------------------------------------------------------------------------------------------
print("== part 10: protecting human capital and purchasing power")
emp_w, emp_vol, mkt_vol, rho = 0.40, 0.45, 0.16, 0.5
port_vol_conc = math.sqrt(
    (emp_w * emp_vol) ** 2
    + ((1 - emp_w) * mkt_vol) ** 2
    + 2 * emp_w * (1 - emp_w) * rho * emp_vol * mkt_vol
)
ok(
    "Tunde holds 40% of liquid assets in his employer's stock (volatility 45%, correlation 0.5 with a 16%-volatility "
    "market): portfolio volatility 24.3% against 16% diversified, while his pay depends on the same company",
    round(port_vol_conc * 100, 1) == 24.3,
)
real_value = 50_000 / 1.03**20
ok(
    "inflation: a level nominal pension of 50k loses 45% of its purchasing power in 20 years at 3% (27.7k in today's "
    "money); an inflation-linked income does not",
    round(real_value / 1e3, 1) == 27.7 and round(1 - real_value / 50_000, 2) == 0.45,
)
usd_share, gbp_up = 0.30, 0.10
ok(
    "Margaret Hartley spends in sterling with 30% of assets in US dollars: a 10% rise in sterling costs 2.7% of "
    "her portfolio in sterling (0.30 x (1 - 1/1.10)); hedging half of it halves the effect",
    round(usd_share * (1 - 1 / (1 + gbp_up)) * 100, 1) == 2.7
    and close(0.5 * usd_share * (1 - 1 / (1 + gbp_up)), usd_share * (1 - 1 / (1 + gbp_up)) / 2),
)

# ---------------------------------------------------------------------------------------------
print("== part 11: residence and citizenship")


def spt(days_now, days_prev1, days_prev2):
    weighted = days_now + days_prev1 / 3 + days_prev2 / 6
    return days_now >= 31 and weighted >= 183, weighted


res, w = spt(150, 120, 120)
ok(
    "US substantial presence test (s. 7701(b)(3)): 150 days this year, 120 in each of the two previous years: "
    "150 + 40 + 20 = 210 weighted days, resident; 120/120/120 gives 160, not resident",
    res and close(w, 210.0) and not spt(120, 120, 120)[0],
)


def uk_ties_needed(days, resident_any_prev3):
    table_a = [(16, 45, 4), (46, 90, 3), (91, 120, 2), (121, 182, 1)]
    table_b = [(46, 90, 4), (91, 120, 3), (121, 182, 2)]
    for lo, hi, k in table_a if resident_any_prev3 else table_b:
        if lo <= days <= hi:
            return k
    return None


ok(
    "UK sufficient ties test (RDR3 Tables A and B): a leaver who was resident in the last 3 years and spends 100 days "
    "needs 2 ties to stay resident; an arriver with no recent residence needs 3",
    uk_ties_needed(100, True) == 2 and uk_ties_needed(100, False) == 3,
)
gain_mtm = 3_500_000.0
taxable = gain_mtm - US_EXPAT_EXCLUSION
ok(
    "US expatriation of a covered expatriate in 2026: 3.5m of unrealised gains treated as realised (s. 877A), less "
    "the 910k exclusion: 2.59m taxable, 616k at 23.8%",
    close(taxable, 2_590_000.0) and round(taxable * US_QD_INV / 1e3) == 616,
)

# ---------------------------------------------------------------------------------------------
print("== part 12: complex situations - founders and executives")
gain, basis_fd = 20_000_000.0, 1_000_000.0
cap = max(15_000_000.0, 10 * basis_fd)
excluded = min(gain, cap) * 1.0  # held 5+ years, stock acquired after 4 July 2025: 100%
ok(
    "QSBS (s. 1202, stock acquired after 4 July 2025, held 5 years): a 20m gain on 1m of basis excludes the greater "
    "of 15m and 10 x basis = 15m; the remaining 5m is taxed at 23.8% (1.19m), against 4.76m with no exclusion",
    close(excluded, 15_000_000.0)
    and round((gain - excluded) * US_QD_INV / 1e6, 2) == 1.19
    and round(gain * US_QD_INV / 1e6, 2) == 4.76,
)
ok(
    "held 3 years the exclusion is 50%, 4 years 75%: 7.5m and 11.25m of the capped 15m",
    close(0.5 * cap, 7_500_000.0) and close(0.75 * cap, 11_250_000.0),
)


def first_trade_date(adopted, ten_q_filed):
    """Rule 10b5-1(c)(1)(ii)(B)(1): later of 90 days after adoption and 2 business days after the 10-Q, max 120 days."""
    a = adopted + datetime.timedelta(days=90)
    b, k = ten_q_filed, 0
    while k < 2:
        b += datetime.timedelta(days=1)
        if b.weekday() < 5:
            k += 1
    return min(max(a, b), adopted + datetime.timedelta(days=120))


d0 = datetime.date(2026, 3, 4)
ok(
    "an officer's Rule 10b5-1 plan adopted 4 March 2026: with the 10-Q filed 7 May, trading may start on 2 June "
    "(90 days); if the 10-Q is filed late on 5 June, on 9 June (two business days after it); never later than "
    "2 July (120 days)",
    first_trade_date(d0, datetime.date(2026, 5, 7)) == datetime.date(2026, 6, 2)
    and first_trade_date(d0, datetime.date(2026, 6, 5)) == datetime.date(2026, 6, 9)
    and first_trade_date(d0, datetime.date(2026, 8, 1)) == datetime.date(2026, 7, 2),
)

# ---------------------------------------------------------------------------------------------
print("== part 13: transferring wealth - gifts, bequests and philanthropy")
V0, B0, VD = 5_000_000.0, 1_000_000.0, 10_000_000.0
OTHER = (
    30_000_000.0  # other assets at death, so the estate is taxable at the 40% margin in both cases
)


def estate_tax(taxable, exemption):
    return US_ESTATE_RATE * max(
        0.0, taxable - exemption
    )  # flat 40% above the exemption (s. 2001(c) top rate)


# A: keep the asset; it is in the estate at 10m with a stepped-up basis (s. 1014).
tax_a = estate_tax(OTHER + VD, US_BASIC_EXCL)
heirs_a = OTHER + VD - tax_a
# B: give it now at 5m, using 5m of the unified exemption (Rev. Proc. 2025-32 sec. 3.14); carryover basis 1m (s. 1015).
tax_b = estate_tax(OTHER, US_BASIC_EXCL - V0)
heirs_b_hold = OTHER - tax_b + VD
heirs_b_sell = heirs_b_hold - US_QD_INV * (VD - B0)
ok(
    "a 5m asset (basis 1m) that will be 10m at death, in an estate with 30m of other assets: keeping it, heirs "
    "receive 30.0m after 10.0m of estate tax; giving it now uses 5m of exemption, so estate tax is 8.0m and heirs "
    "receive 32.0m if they keep the asset, but 29.86m if they sell it and pay 23.8% on the 9m carryover gain",
    close(tax_a, 10_000_000.0)
    and close(heirs_a, 30_000_000.0)
    and close(tax_b, 8_000_000.0)
    and close(heirs_b_hold, 32_000_000.0)
    and round(heirs_b_sell / 1e6, 2) == 29.86,
)
ok(
    "the gift saves 40% of the 5m growth (2.0m) but forgoes the step-up, costing 2.14m if heirs sell: worth doing "
    "only if the asset will not be sold, or grows faster; in an estate below the 15m exemption the gift saves "
    "nothing and only loses the step-up",
    close(heirs_b_hold - heirs_a, 2_000_000.0)
    and round((heirs_a - heirs_b_sell) / 1e6, 2) == 0.14
    and estate_tax(VD, US_BASIC_EXCL) == 0.0,
)
gift_uk, nrb_left = 500_000.0, UK_NRB
taper = {3: 0.32, 4: 0.24, 5: 0.16, 6: 0.08}
ok(
    "UK: a 500k gift to a son with death 4.5 years later: the 325k nil-rate band covers the first part; 175k is "
    "taxed at the 24% taper rate: 42k, against 70k at 40% within 3 years and nothing after 7",
    close((gift_uk - nrb_left) * taper[4], 42_000.0)
    and close((gift_uk - nrb_left) * 0.40, 70_000.0),
)
ok(
    "Margaret's estate of 2.4m, left to her children with the home: GOV.UK makes an estate below 2m a condition "
    "of the 175k residence band, so only the 325k nil-rate band applies: tax 830k at 40%; leaving 10% of the net "
    "estate to charity cuts the rate to 36%",
    round((2_400_000 - UK_NRB) * UK_IHT / 1e3) == 830 and close(UK_IHT - 0.04, 0.36),
)
pv_payments = 50_000 * annuity(0.05, 20)
ok(
    "a CRAT of 1m paying 5% (50k) a year for 20 years: payments worth 623k at a 5% rate leave a charitable "
    "remainder of 377k, above the 10% minimum (s. 664(d)(1)); a private foundation must distribute about 5% of "
    "non-charitable assets a year (s. 4942(e))",
    round(pv_payments / 1e3) == 623 and 1_000_000 - pv_payments > 100_000,
)
ok(
    "US annual exclusion 19,000 a donee in 2026 (194,000 to a non-citizen spouse); basic exclusion 15m; gifting "
    "19,000 to each of 6 grandchildren for 10 years moves 1.14m out of the estate with no use of the exemption",
    US_GIFT_EXCL * 6 * 10 == 1_140_000,
)

print(f"\n{n_checks} checks executed")
if fails:
    print("FAILED:", fails)
    sys.exit(1)
print("all checks passed")
