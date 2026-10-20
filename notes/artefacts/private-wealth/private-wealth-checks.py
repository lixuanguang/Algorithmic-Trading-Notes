"""Private wealth: human capital, taxes, planning, retirement, protection, residency and transfers (2026-10-20).

Worked numbers of the entries in compendium/private-wealth-management/. Every client is hypothetical: the Okafors
(United States, tax year 2026), Margaret Hartley (United Kingdom, tax year 2026 to 2027), Maya Chen (a US citizen
moving to London) and Luis Rivera (a US founder). Tax parameters are the published 2026 US federal figures (Rev. Proc.
2025-32; Notice 2025-67; 26 U.S.C.) and the 2026 to 2027 UK figures on GOV.UK; state, local and Scottish taxes,
phase-outs and credits are ignored. Mortality follows a Gompertz law chosen for illustration, not a life table.

The Okafor case is one linked base case. Financial assets of 600k = a 60k emergency reserve in cash held OUTSIDE the
policy portfolio + a 540k policy portfolio that funds the goals; the reserve is never counted as goal-funding capital.
Adaeze (40) and Tunde (42) retire together when she is 62, in 22 years, so her human capital runs to 62. The plan counts
planned saving of 50k a year (end of each year, mostly 401(k) deferrals) and two 200k education payments at the ends of
years 8 and 10; amounts are in today's dollars, retirement spending is before income tax on withdrawals, and the taxable
account's tax drag is ignored in the funding model. Their 2026 federal return (married filing jointly, stated
assumptions): wages 650k (Adaeze 250k, Tunde 400k of salary, commissions and vested RSUs) less 49k of 401(k)
deferrals; 2.4k of interest on the reserve; 6k of qualified dividends and 60k of net long-term gains (vested employer
shares sold to stay below 10%); standard deduction 32.2k (Rev. Proc. 2025-32 sec. 4.14). Ordinary taxable income
571.2k lies in the 35% band (sec. 4.01 Table 1: 512,450 to 768,700), but the band does not fix the rate on dividends
and gains: under 26 U.S.C. 1(h)(1) and 1(j)(5) they are stacked on top of ordinary income and taxed at 15% only up to
taxable income of 613,700 (sec. 4.03), 20% above, plus the 3.8% NIIT on the lesser of net investment income and MAGI
above 250k (sec. 1411). Capital market assumptions (illustrative, real): equity 5.0% expected, 17% volatility; bonds
1.5%, 6%; correlation 0.2. The asset-location client in part 7 is a separate, top-bracket US client.

Corrections (2026-10-20, final audit): the reserve was double counted inside a 70/25/5 policy on the full 600k
(required return 1.96%, now 2.30% on 540k); human capital ran to 65 against retirement at 62; part 1 saved 40k growing
1% and ignored the education payments, and parts 1 and 5 discounted both education payments at 10 years; the asset
location compounded taxable dividends and price growth multiplicatively but IRA stocks additively (2.47m, now 2.45m);
the UK gift example said the son survived the donor rather than the donor dying 4.5 years after the gift, the estate
example reused the nil-rate band the gift had consumed, and the residence band was treated as lost above 2m instead
of tapered by 1 for every 2.

Independent routes: human capital by direct discounting against the backward recursion HC(x) = (e + HC(x+1))/(1+r);
after-tax accumulation by formula against year-by-year simulation; the required return by root-finding against the
funded-ratio identity; fees by year-by-year simulation against closed forms; annuity factors by summation against
the survival integral; asset location by a year-by-year cash and basis ledger against
the closed form, a zero-tax comparison and a one-year hand reconciliation; the Okafor funding by the required-return root
against a forward projection at that return; the Roth and traditional comparison against
the equal-rate identity; UK pension relief by the gross-up identity; the substantial presence test and UK ties by
rule; QSBS exclusion against the statutory cap; gift against bequest by full after-tax terminal wealth;
the UK gift and estate as one chronology against the no-gift estate, the difference being the taper relief; the
residence nil-rate band taper against its boundary cases; the CRAT
remainder by annuity factors; the Okafors' federal tax by the sec. 1(h)(1)(A)-(D) formula against layer-by-layer
stacking, the published cumulative bracket amounts, finite-difference marginal rates and boundary cases.

Corrections (2026-10-21, PR #33 correction pass): the IPS inferred a 15% rate on dividends and gains from the 35%
ordinary band, although the 2026 joint 15% ceiling (613,700) lies inside that band; the household's income is now
specified and the rate is computed by stacking.

Count convention: one check is one executed ok() call (a call inside a loop counts once per iteration).

Run: uv run python private-wealth-checks.py   (numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import datetime
import itertools
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


# US 2026 federal parameters (Rev. Proc. 2025-32 secs. 3.14, 4.01, 4.03, 4.14, 4.37-4.38, 4.42; Notice 2025-67)
US_MFJ_BRACKETS = [  # sec. 4.01 Table 1, married filing jointly: (lower edge of the band, rate)
    (0, 0.10),
    (24_800, 0.12),
    (100_800, 0.22),
    (211_400, 0.24),
    (403_550, 0.32),
    (512_450, 0.35),
    (768_700, 0.37),
]
US_MFJ_ZERO_MAX, US_MFJ_15_MAX = (
    98_900,
    613_700,
)  # sec. 4.03 maximum zero and 15% rate amounts, joint
US_MFJ_STD_DED, US_NIIT_JOINT = 32_200, 250_000  # sec. 4.14; sec. 1411(b)(1), not indexed
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
    62,
)  # Adaeze's after-tax real earnings at 40, growth, discount rate, retirement age (the household retires together)
FIN, RESERVE = 600_000.0, 60_000.0
POLICY = FIN - RESERVE  # the goal-funding policy portfolio; the reserve sits outside it
SAVE, YEARS = 50_000.0, 22  # planned saving at each year-end until retirement
EDU = [(8, 200_000.0), (10, 200_000.0)]  # years from now (children now 10 and 8)
MU_E, SD_E, MU_B, SD_B, RHO_EB = 0.05, 0.17, 0.015, 0.06, 0.2  # real capital market assumptions


def mix(w_eq):
    """Arithmetic mean, volatility and compound (lognormal median-adjusted) expected real return of a stock-bond mix."""
    m = w_eq * MU_E + (1 - w_eq) * MU_B
    sd = math.sqrt(
        (w_eq * SD_E) ** 2 + ((1 - w_eq) * SD_B) ** 2 + 2 * w_eq * (1 - w_eq) * RHO_EB * SD_E * SD_B
    )
    s2 = math.log(1 + sd**2 / (1 + m) ** 2)
    ml = math.log(1 + m) - s2 / 2
    return m, sd, math.exp(ml) - 1, math.exp(ml - 1.645 * math.sqrt(s2)) - 1


def project(rr, years=YEARS, p0=POLICY, save=SAVE):
    """Policy portfolio after `years` at return rr, with saving and education payments at year-ends."""
    x = p0
    for t in range(1, years + 1):
        x = x * (1 + rr) + save - sum(c for tt, c in EDU if tt == t)
    return x


def hc(age, r=R_SAFE, e40=E40, g=G, ret=RET):
    e = e40 * (1 + g) ** (age - 40)
    return sum(e * (1 + g) ** (t - 1) / (1 + r) ** t for t in range(1, ret - age + 1))


ok(
    "Adaeze's human capital (after-tax 180k real at 40, +1% a year, to retirement at 62, discounted at 3.5%) is "
    "3.00m at 40, 2.02m at 50, 0.42m at 60; running it to 65 would overstate it at 40 by 0.30m (3.29m)",
    round(hc(40) / 1e6, 2) == 3.00
    and round(hc(50) / 1e6, 2) == 2.02
    and round(hc(60) / 1e6, 2) == 0.42
    and round(hc(40, ret=65) / 1e6, 2) == 3.29,
)
ok(
    "recursion: HC(40) = (earnings in year 1 + HC(41)) / 1.035",
    close(hc(40), (E40 + hc(41)) / (1 + R_SAFE), 1e-6),
)
ok(
    "the same income discounted at 6% (equity-like risk) is worth 2.36m: riskier income is less valuable human capital",
    round(hc(40, r=0.06) / 1e6, 2) == 2.36 and hc(40, r=0.06) < hc(40),
)
g60 = mix(0.60)[2]
fc = {40: FIN}
for k in range(1, YEARS + 1):
    fc[40 + k] = RESERVE + project(g60, years=k)
ok(
    "with the recommended 60/40 policy earning its expected compound 3.03% real, 50k saved a year and the two "
    "education payments made, financial capital (reserve included) rises from 0.60m at 40 to 0.95m at 50 (after both "
    "education payments), 1.83m at 60 and 2.04m at 62, while human capital falls to zero",
    round(g60 * 100, 2) == 3.03
    and round(fc[50] / 1e6, 2) == 0.95
    and round(fc[60] / 1e6, 2) == 1.83
    and round(fc[62] / 1e6, 2) == 2.04,
)
pv_edu = sum(c / 1.035**t for t, c in EDU)
enw40 = FIN + hc(40) - 400_000 - pv_edu
ok(
    "economic net worth at 40: financial 0.60m + human capital 3.00m - mortgage 0.40m - PV of the 200k education "
    "payments in 8 and 10 years (0.29m) = 2.90m; human capital is 83% of gross economic assets",
    round(pv_edu / 1e6, 2) == 0.29
    and round(enw40 / 1e6, 2) == 2.90
    and round(hc(40) / (hc(40) + FIN), 2) == 0.83,
)
# Total-wealth allocation: Adaeze's HC bond-like; Tunde's HC (2.0m) 50% equity-like. Target 40% equity on total wealth.
HC_T = 2_000_000.0
total = FIN + hc(40) + HC_T
eq_needed = 0.40 * total - 0.5 * HC_T
ok(
    "capacity view: with Tunde's 2.0m of commission income counted as half equity, a 40% equity target on total "
    "wealth (5.60m) needs 1.24m of financial equity, more than the whole 0.54m policy portfolio; capacity alone would "
    "put all of it in equities, so willingness, not capacity, is the binding constraint",
    round(total / 1e6, 2) == 5.60 and round(eq_needed / 1e6, 2) == 1.24 and eq_needed > POLICY,
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


def funded_gap(rr, p0=POLICY):
    fv_assets = p0 * (1 + rr) ** YEARS + sum(
        SAVE * (1 + rr) ** (YEARS - t) for t in range(1, YEARS + 1)
    )
    fv_edu = sum(c * (1 + rr) ** (YEARS - t) for t, c in EDU)
    return fv_assets - fv_edu - pv_ret_at62


req = brentq(funded_gap, -0.05, 0.20)
req_double = brentq(lambda rr: funded_gap(rr, p0=FIN), -0.05, 0.20)
ok(
    "retirement at 62 needing 150k real a year for 30 years, 60k from Social Security: PV at 62 of the 90k gap at a "
    "3% real rate is 1.76m",
    round(pv_ret_at62 / 1e6, 2) == 1.76,
)
ok(
    "with the 60k reserve held outside, the 0.54m policy portfolio, 50k saved a year for 22 years and the two 200k "
    "education payments need a real return of 2.30%; counting the reserve as goal capital too (0.60m) would give "
    "1.96% while also spending it on emergencies, which double counts it",
    round(req * 100, 2) == 2.30 and round(req_double * 100, 2) == 1.96,
    f"{req:.4%}",
)
ok(
    "independent route: projecting the policy portfolio year by year at 2.30%, with saving and both education "
    "payments, reaches exactly the 1.76m retirement need at 62",
    close(project(req), pv_ret_at62, 1e-3),
)
cands = {w: mix(w) for w in (0.7, 0.6, 0.4)}
ok(
    "allocation against the goals (real, illustrative assumptions): 70/30, 60/40 and 40/60 have expected compound "
    "returns of 3.22%, 3.03% and 2.57%, all above 2.30%; projected surpluses over the 1.76m need at 62 of 0.28m, 0.22m "
    "and 0.08m",
    [round(cands[w][2] * 100, 2) for w in (0.7, 0.6, 0.4)] == [3.22, 3.03, 2.57]
    and [round((project(cands[w][2]) - pv_ret_at62) / 1e6, 2) for w in (0.7, 0.6, 0.4)]
    == [0.28, 0.22, 0.08],
)
ok(
    "allocation against willingness: the Okafors would sell after a one-year loss of about 15%; the one-in-twenty "
    "one-year return is -15.1% for 70/30 (at the limit), -13.4% for 60/40 and -10.2% for 40/60",
    [round(cands[w][3] * 100, 1) for w in (0.7, 0.6, 0.4)] == [-15.1, -13.4, -10.2],
)


def ord_tax(ti):
    """Regular tax on joint taxable income ti from the sec. 4.01 Table 1 bands."""
    edges = [*US_MFJ_BRACKETS, (math.inf, None)]
    return sum(
        rate * max(0.0, min(ti, hi) - lo) for (lo, rate), (hi, _) in itertools.pairwise(edges)
    )


def cg_tax(ti, ancg):
    """Sec. 1(h)(1)(A)-(D) as modified by 1(j)(5): ancg is adjusted net capital gain (qualified dividends included,
    sec. 1(h)(11)); returns (tax, amount at 0%, at 15%, at 20%). No unrecaptured 1250 or collectibles gain.
    """
    ancg = min(ancg, ti)
    a = ti - ancg  # (A): taxable income reduced by the gain, taxed at ordinary rates
    b = min(ancg, max(0.0, US_MFJ_ZERO_MAX - a))  # (B): 0% up to the maximum zero rate amount
    c = min(ancg - b, max(0.0, US_MFJ_15_MAX - (a + b)))  # (C): 15% up to the maximum 15% amount
    d = ancg - b - c  # (D): 20% on the rest
    return min(ord_tax(a) + 0.15 * c + 0.20 * d, ord_tax(ti)), b, c, d


def stacked_tax(ti, pref):
    """Independent route: ordinary income fills the bands first; each preferential dollar from ti - pref to ti is taxed
    at the rate of the layer it occupies, integrated piece by piece.
    """
    tax, lo = ord_tax(ti - pref), ti - pref
    for top, rate in ((US_MFJ_ZERO_MAX, 0.0), (US_MFJ_15_MAX, 0.15), (math.inf, 0.20)):
        hi = min(ti, top)
        if hi > lo:
            tax += rate * (hi - lo)
            lo = hi
    return tax


def okafor_tax(wages=650_000.0, deferral=49_000.0, interest=2_400.0, qdiv=6_000.0, ltcg=60_000.0):
    """The Okafors' 2026 federal income tax and NIIT (state taxes, payroll taxes and phase-outs ignored)."""
    agi = (
        wages - deferral + interest + qdiv + ltcg
    )  # MAGI equals AGI: no foreign earned income excluded
    ti = agi - US_MFJ_STD_DED
    tax, at0, at15, at20 = cg_tax(ti, qdiv + ltcg)
    niit = US_NIIT * min(interest + qdiv + ltcg, max(0.0, agi - US_NIIT_JOINT))
    return {
        "agi": agi,
        "ti": ti,
        "ord": ti - qdiv - ltcg,
        "tax": tax,
        "niit": niit,
        "at0": at0,
        "at15": at15,
        "at20": at20,
    }


tx = okafor_tax()
ok(
    "2026 joint brackets (Rev. Proc. 2025-32 sec. 4.01 Table 1): the band formula reproduces the published tax of "
    "116,896 at 512,450 and 206,583.50 at 768,700; the 15% ceiling of 613,700 (sec. 4.03) lies inside the 35% band, "
    "so the ordinary band alone cannot fix the rate on dividends and gains",
    close(ord_tax(512_450), 116_896, 1e-6)
    and close(ord_tax(768_700), 206_583.5, 1e-6)
    and 512_450 < US_MFJ_15_MAX < 768_700,
)
ok(
    "the Okafors' 2026 return: AGI 669,400; taxable income 637,200 after the 32,200 standard deduction; ordinary "
    "taxable income 571,200 (35% band); of the 66,000 of qualified dividends and long-term gains stacked on top, "
    "42,500 fill the 15% layer to 613,700 and 23,500 are taxed at 20%; income tax 148,533.50; NIIT 3.8% of the "
    "68,400 of investment income (less than MAGI over 250k) = 2,599.20",
    close(tx["agi"], 669_400)
    and close(tx["ti"], 637_200)
    and close(tx["ord"], 571_200)
    and 512_450 < tx["ord"] < 768_700
    and close(tx["at0"], 0.0)
    and close(tx["at15"], 42_500)
    and close(tx["at20"], 23_500)
    and close(tx["tax"], 148_533.5, 1e-6)
    and close(tx["niit"], 2_599.2, 1e-6),
    f"tax {tx['tax']:,.2f}, NIIT {tx['niit']:,.2f}",
)
ok(
    "independent route: integrating the preferential layers piece by piece above ordinary income gives the same "
    "tax; the old inference (all 66,000 at 15%) understates it by 1,175 = 23,500 x 5 points",
    close(stacked_tax(tx["ti"], 66_000), tx["tax"], 1e-6)
    and close(tx["tax"] - (ord_tax(tx["ord"]) + 0.15 * 66_000), 1_175, 1e-6),
)
mtax = {
    k: (lambda t: t["tax"] + t["niit"])(okafor_tax(**{k: v + 1.0})) - (tx["tax"] + tx["niit"])
    for k, v in (("wages", 650_000.0), ("interest", 2_400.0), ("ltcg", 60_000.0))
}
ok(
    "marginal federal rates by finite difference: a further dollar of gains or qualified dividends costs 23.8% (20% + "
    "NIIT), not 18.8%; a further dollar of wages costs 40% (35% plus the 5 points of one gain dollar pushed from 15% to "
    "20%), and of interest 43.8%: each deferred 401(k) dollar saves 40%, and bonds belong in tax-deferred accounts",
    round(mtax["ltcg"], 3) == 0.238
    and round(mtax["wages"], 3) == 0.400
    and round(mtax["interest"], 3) == 0.438,
    f"{ {k: round(v, 4) for k, v in mtax.items()} }",
)
b_low, b_at, b_high = (cg_tax(o + 40_000, 40_000) for o in (571_200, 573_700, 613_700))
ok(
    "boundary cases: with 40,000 of gains on 571,200 of ordinary income (total 611,200) all gains are at 15%; at "
    "exactly 613,700 still all at 15%, and one more dollar of gain is taxed at 20%; with ordinary income at 613,700 "
    "every gain dollar is at 20%; with ordinary income of 60,000 the first 38,900 of gains are at 0%; the Okafors' "
    "66,000 would all be at 15% only if ordinary income fell to 547,700 (613,700 - 66,000)",
    close(cg_tax(547_700 + 66_000, 66_000)[2], 66_000)
    and close(cg_tax(547_701 + 66_000, 66_000)[3], 1.0, 1e-6)
    and close(b_low[2], 40_000)
    and close(b_low[3], 0.0)
    and close(b_at[2], 40_000)
    and close(cg_tax(613_701, 40_001)[0] - b_at[0], 0.20, 1e-6)
    and close(b_high[3], 40_000)
    and close(cg_tax(100_000, 40_000)[1], 38_900),
)
ok(
    "NIIT boundaries (sec. 1411(a)(1)): MAGI of 240,000 owes none; MAGI of 260,000 with 30,000 of investment income "
    "owes 3.8% of the 10,000 excess (380), not of the 30,000; the Okafors' MAGI exceeds 250,000 by more than their "
    "investment income, so the whole 68,400 is taxed",
    okafor_tax(wages=240_000.0, deferral=30_000.0, interest=0.0, qdiv=0.0, ltcg=30_000.0)["niit"]
    == 0.0
    and close(
        okafor_tax(wages=260_000.0, deferral=30_000.0, interest=0.0, qdiv=0.0, ltcg=30_000.0)[
            "niit"
        ],
        380.0,
        1e-9,
    )
    and tx["agi"] - US_NIIT_JOINT > 68_400,
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


def funded_ratio(d, save=SAVE):
    """PV of goal-funding resources over PV of goals at discount rate d; the reserve is on neither side."""
    res_ = POLICY + sum(save / (1 + d) ** t for t in range(1, YEARS + 1))
    goals_ = sum(c / (1 + d) ** t for t, c in EDU) + pv_ret_at62 / (1 + d) ** YEARS
    return res_, goals_, res_ / goals_


pv_resources, pv_goals, fr35 = funded_ratio(0.035)
save_needed = brentq(lambda sv: funded_ratio(0.015, sv)[2] - 1, 0, 200_000)
ok(
    "liquidity tiers: a six-month emergency reserve of 60k in cash, outside the 540k policy portfolio (600k in total); "
    "education money moves to a cash or short-bond bucket once a payment is within two years (188.5k for a 200k "
    "payment at 3%)",
    close(reserve, RESERVE)
    and close(POLICY + RESERVE, FIN)
    and round(edu_bucket / 1e3, 1) == 188.5,
)
ok(
    "funded ratio at a 3.5% discount rate: PV of the policy portfolio and savings 1.30m against PV of goals 1.12m: "
    "1.16; at a 1.5% rate the ratio falls to 0.91 and the plan is short unless saving rises to about 58.1k a year",
    round(pv_resources / 1e6, 2) == 1.30
    and round(pv_goals / 1e6, 2) == 1.12
    and round(fr35, 2) == 1.16
    and round(funded_ratio(0.015)[2], 2) == 0.91
    and round(save_needed / 1e3, 1) == 58.1,
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
    "Adaeze's life insurance need: 75% of her 3.00m human capital (the part that supports the family) less 0.30m of "
    "assets set aside = 1.95m of term cover to 62, falling as she ages",
    round(ins_need / 1e6, 2) == 1.95 and 0.75 * hc(50) - 300_000 < ins_need,
)
ok(
    "disability cover of 60% of 250k pre-tax pay (150k a year) to 62 replaces 83% of her 180k after-tax pay if the "
    "benefit is untaxed (individually paid premiums)",
    round(150_000 / 180_000, 2) == 0.83,
)

# ---------------------------------------------------------------------------------------------
print("== part 7: tax management - asset location and loss harvesting (US 2026)")
BONDS, STOCKS, YB, DY, GY = 500_000.0, 500_000.0, 0.045, 0.02, 0.05


def stock_ledger(years, tax_div, tax_gain):
    """Taxable stock account, one convention for both placements: each year price rises GY on the opening value, a
    dividend of DY times the opening value is paid at year-end, tax on it is paid, and the rest is reinvested and added
    to basis. Returns (value, basis, after-tax value on liquidation).
    """
    value = basis = STOCKS
    for _ in range(years):
        div = DY * value
        net_div = div * (1 - tax_div)
        value += GY * value + net_div
        basis += net_div
    return value, basis, value - tax_gain * (value - basis)


def location(
    bonds_in_ira, years=20, t_ira=0.24, t_int=US_ORD_INV, t_div=US_QD_INV, t_gain=US_QD_INV
):
    """After-tax wealth when the IRA (taxed at t_ira on withdrawal) holds bonds or stocks and the taxable account the other."""
    if bonds_in_ira:
        ira = BONDS * (1 + YB) ** years
        tx_after = stock_ledger(years, t_div, t_gain)[2]
    else:
        ira = stock_ledger(years, 0.0, 0.0)[0]  # inside the IRA: the same dividend timing, untaxed
        tx_after = (
            BONDS * (1 + YB * (1 - t_int)) ** years
        )  # interest taxed yearly; basis equals value
    return ira * (1 - t_ira) + tx_after


good, bad = location(True), location(False)
v1, b1, _ = stock_ledger(1, US_QD_INV, US_QD_INV)
ok(
    "one-year reconciliation of the taxable stock account: 500k rises 25,000 in price; the 10,000 dividend bears "
    "2,380 of tax and 7,620 is reinvested, so value is 532,620, basis 507,620 and the unrealised gain exactly the "
    "25,000 price rise; in the IRA the whole dividend is reinvested (535,000)",
    close(v1, 532_620.0, 1e-6)
    and close(b1, 507_620.0, 1e-6)
    and close(v1 - b1, 25_000.0, 1e-6)
    and close(stock_ledger(1, 0.0, 0.0)[0], 535_000.0, 1e-6),
)
v20, b20, _ = stock_ledger(20, US_QD_INV, US_QD_INV)
ok(
    "closed form: the taxable stock grows by 1 + g + d(1 - t) = 1.06524 a year, and its basis is the original "
    "cost plus every reinvested after-tax dividend",
    close(v20, STOCKS * (1 + GY + DY * (1 - US_QD_INV)) ** 20, 1e-6)
    and close(
        b20,
        STOCKS
        + sum(
            STOCKS * (1 + GY + DY * (1 - US_QD_INV)) ** k * DY * (1 - US_QD_INV) for k in range(20)
        ),
        1e-6,
    ),
)
zero = {k: 0.0 for k in ("t_ira", "t_int", "t_div", "t_gain")}
earlier_tx = (
    STOCKS * (1 + DY) ** 20 * (1 + GY) ** 20
)  # the earlier multiplicative taxable convention, at zero tax
ok(
    "with every tax at zero, location cannot change gross performance: both placements end with 500k x 1.045^20 + "
    "500k x 1.07^20 = 3,140,699; the earlier convention (taxable stocks compounding (1 + d)(1 + g), IRA stocks 1 + d + g) "
    "would have shown a 36,488 location effect even without tax",
    close(location(True, **zero), location(False, **zero), 1e-6)
    and round(location(True, **zero)) == 3_140_699
    and round(earlier_tx - STOCKS * 1.07**20) == 36_488,
)
ok(
    "500k of bonds (4.5%) and 500k of stocks (2% yield on opening value, 5% price growth), 20 years, top-bracket "
    "taxes, IRA taxed at 24% on withdrawal: bonds in the IRA and stocks in the taxable account end with 2,454,619 "
    "after tax against 2,316,409 the other way, an advantage of 138,211",
    round(good) == 2_454_619 and round(bad) == 2_316_409 and good > bad,
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
v0, flow = POLICY, SAVE  # the Okafors' policy portfolio; the year's saving arrives at mid-year
mid = v0 * 1.05  # +5.0% in the first half
v1 = (mid + flow) * 1.064  # +6.4% in the second half
twr = (mid / v0) * (v1 / (mid + flow)) - 1
mwr = brentq(lambda rr: v0 * (1 + rr) + flow * (1 + rr) ** 0.5 - v1, -0.5, 1)
ok(
    "the Okafors' first year: 540,000 grows to 567,000 by mid-year, 50,000 is added, and the year ends at 656,488. "
    "TWR 11.72% (chain-linked) measures the manager; MWR 11.78% measures the client's experience; against an "
    "assumed 11.0% benchmark the manager added 0.72 points",
    close(v1, 656_488.0, 1e-6)
    and round(twr * 100, 2) == 11.72
    and round(mwr * 100, 2) == 11.78
    and round((twr - 0.11) * 100, 2) == 0.72,
    f"TWR {twr:.4%}, MWR {mwr:.4%}",
)
res1 = v1 + sum(SAVE / 1.035**t for t in range(1, YEARS))
goals1 = sum(c / 1.035 ** (t - 1) for t, c in EDU) + pv_ret_at62 / 1.035 ** (YEARS - 1)
ok(
    "progress against the plan (treating the year's return as real): the funded ratio at 3.5% rises from 1.16 to "
    "1.20 after the year",
    round(fr35, 2) == 1.16 and round(res1 / goals1, 2) == 1.20,
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
UK_TAPER_THRESHOLD = 2_000_000.0  # IHTA 1984 s. 8D; IHTM46023 (updated 7 April 2026)


def taper_rate(years_before_death):
    """Rate on a failed potentially exempt transfer above the nil-rate band (GOV.UK, rules on giving gifts)."""
    for limit, rate in ((3, 0.40), (4, 0.32), (5, 0.24), (6, 0.16), (7, 0.08)):
        if years_before_death < limit:
            return rate
    return 0.0


def rnrb(estate, home, allowance=UK_RNRB, transferred=0.0):
    """Residence nil-rate band: the allowance (plus any transferred) less 1 for every 2 of estate above 2m, capped
    at the value of the qualifying home passing to direct descendants. `estate` is the net value at death before
    exemptions and reliefs, excluding lifetime gifts.
    """
    adjusted = max(0.0, allowance + transferred - max(0.0, estate - UK_TAPER_THRESHOLD) / 2)
    return min(home, adjusted)


ok(
    "residence nil-rate band taper (175k allowance, none transferred, a qualifying home worth at least the band): "
    "175k at an estate of 2.0m, 125k at 2.1m, nothing at 2.35m or above; a home worth 100k caps it at 100k",
    close(rnrb(2_000_000, 900_000), 175_000.0)
    and close(rnrb(2_100_000, 900_000), 125_000.0)
    and close(rnrb(2_350_000, 900_000), 0.0)
    and close(rnrb(2_400_000, 900_000), 0.0)
    and close(rnrb(1_900_000, 100_000), 100_000.0),
)
# One chronology: Margaret gives 500k to her son (annual exemptions already used) and dies 4.5 years later, leaving a
# 2.4m estate, including a home worth 900k, to her children. She has no band transferred from a former spouse.
GIFT, YRS_TO_DEATH, ESTATE, HOME = 500_000.0, 4.5, 2_400_000.0, 900_000.0
nrb_used_by_gift = min(GIFT, UK_NRB)
tax_gift = (GIFT - nrb_used_by_gift) * taper_rate(YRS_TO_DEATH)
nrb_left = UK_NRB - nrb_used_by_gift
tax_estate = UK_IHT * max(0.0, ESTATE - rnrb(ESTATE, HOME) - nrb_left)
tax_no_gift = UK_IHT * max(0.0, ESTATE + GIFT - rnrb(ESTATE + GIFT, HOME) - UK_NRB)
ok(
    "the gift fails because Margaret dies 4.5 years after making it (the 4 to 5 year band): the 325k nil-rate band "
    "covers the first part, and 175k is taxed at 24%: 42,000, against 70,000 within 3 years and nothing after 7",
    taper_rate(4.5) == 0.24
    and close(tax_gift, 42_000.0)
    and close((GIFT - UK_NRB) * taper_rate(2.9), 70_000.0)
    and taper_rate(7.0) == 0.0,
)
ok(
    "the estate: the gift has consumed the whole nil-rate band, and 2.4m tapers the residence band to zero, so all "
    "2.4m is taxed at 40%: 960,000 (reusing the 325k band, as the earlier example did, would give 830,000)",
    close(nrb_left, 0.0)
    and close(tax_estate, 960_000.0)
    and close(UK_IHT * (ESTATE - UK_NRB), 830_000.0),
)
ok(
    "total 1,002,000 against 1,030,000 had she kept the 500k (estate 2.9m): the gift saved exactly its taper relief, "
    "16% of 175k = 28,000, because it only moved the nil-rate band forward in time",
    close(tax_gift + tax_estate, 1_002_000.0)
    and close(tax_no_gift, 1_030_000.0)
    and close(tax_no_gift - tax_gift - tax_estate, (0.40 - 0.24) * (GIFT - UK_NRB)),
)
ok(
    "had the estate at death been 2.1m instead, 125k of residence band would remain and the tax would be 790,000; "
    "leaving 10% of the net estate to charity lowers the rate to 36%",
    close(UK_IHT * (2_100_000 - rnrb(2_100_000, HOME) - nrb_left), 790_000.0)
    and close(UK_IHT - 0.04, 0.36),
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
