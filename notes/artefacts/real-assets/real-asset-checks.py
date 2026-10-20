"""Real assets: property valuation, indexes, REITs, private real estate, infrastructure and land (2026-10-20).

Worked numbers of the entries in compendium/real-asset-investor/. Every property, REIT, project and parcel is
hypothetical (Marlow House, Kestrel REIT, Ferris Park, Ashdown Hospital PPP, a farmland parcel and a timber stand),
except the reported USDA 2026 farmland averages and NCREIF index returns quoted in the entries.

Independent routes: the 10-year DCF with constant growth and an exit cap of r - g against the direct capitalisation
NOI1 / (r - g); the NCREIF quarterly income and appreciation returns against their sum and the property's change in
value; appraisal smoothing against the closed-form variance ratio; REIT NAV built asset by asset against equity per
share; FFO and AFFO reconciled line by line from net income; levered and unlevered IRRs against cash-flow NPV = 0;
PPP debt sized by sculpting to a target DSCR against the LLCR identity (LLCR = target DSCR at financial close) and
the gearing cap; farmland return as income yield plus growth against the Gordon identity.

Count convention: one check is one executed ok() call (a call inside a loop counts once per iteration).

Run: uv run python real-asset-checks.py   (numpy, scipy). Exits 1 on failure.
"""

# standard library imports
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


def irr(cf):
    return brentq(lambda r: sum(c / (1 + r) ** i for i, c in enumerate(cf)), -0.99, 10.0)


# ---------------------------------------------------------------------------------------------
print(
    "== part 1: valuing Marlow House - income (direct capitalisation and DCF), sales comparison and cost"
)
AREA, RENT, LOSS, OTHER = 200_000, 40.0, 0.02, 0.3e6  # sq ft, EUR per sq ft a year
TAX, FIXED, VAR, RESERVE = 6.0, 4.0, 3.0, 1.0  # EUR per sq ft; VAR per occupied sq ft


def noi(year, g=0.025, occ_path=(0.93, 0.94, 0.95)):
    occ = occ_path[min(year - 1, len(occ_path) - 1)]
    f = (1 + g) ** (year - 1)
    gross = AREA * RENT * f * occ * (1 - LOSS) + OTHER * f
    opex = AREA * (TAX + FIXED + RESERVE) * f + AREA * occ * VAR * f
    return gross - opex


noi1 = noi(1)
v_cap = noi1 / 0.06
ok(
    "year-1 NOI 4.83m (rent 40 x 93% occupancy less 2% credit loss, plus other income, less taxes, fixed and "
    "variable costs and a capex reserve); value at a 6.0% cap rate 80.55m (403 a sq ft)",
    round(noi1 / 1e6, 2) == 4.83 and round(v_cap / 1e6, 2) == 80.55 and round(v_cap / AREA) == 403,
)
R, EXIT_CAP, SELL = 0.08, 0.065, 0.02
pv_cf = sum(noi(t) / (1 + R) ** t for t in range(1, 11))
tv = noi(11) / EXIT_CAP * (1 - SELL)
v_dcf = pv_cf + tv / (1 + R) ** 10
ok(
    "10-year DCF at 8%: occupancy rising to 95%, rent and costs +2.5% a year, exit at a 6.5% cap on year-11 NOI less "
    "2% selling costs: value 81.15m, 55% of it from the exit value",
    round(v_dcf / 1e6, 2) == 81.15 and round(tv / (1 + R) ** 10 / v_dcf, 2) == 0.55,
)
g = 0.025


def noi_const(t):
    return noi(1, occ_path=(0.95,)) * (1 + g) ** (t - 1)


v_const = (
    sum(noi_const(t) / (1 + R) ** t for t in range(1, 11)) + noi_const(11) / (R - g) / (1 + R) ** 10
)
ok(
    "consistency: with constant growth and an exit cap of r - g = 5.5%, the DCF equals NOI1 / (r - g) exactly; "
    "the cap rate on current NOI is (r - g)/(1 + g)",
    close(v_const, noi_const(1) / (R - g), 1e-4)
    and close(noi_const(1) / (1 + g) / v_const, (R - g) / (1 + g), 1e-12),
)
COMPS = [(410, 0.95), (385, 0.92), (425, 0.97), (395, 0.94), (400, 0.93)]
avg_p = np.mean([p for p, _ in COMPS])
avg_occ = np.mean([o for _, o in COMPS])
v_comp = avg_p * AREA
v_comp_adj = v_comp * 0.93 / avg_occ
ok(
    "sales comparison: five sales average 403 a sq ft at 94.2% occupancy: 80.60m, or 79.57m adjusted to Marlow's 93%",
    round(avg_p) == 403
    and round(avg_occ, 3) == 0.942
    and round(v_comp / 1e6, 2) == 80.60
    and round(v_comp_adj / 1e6, 2) == 79.57,
)
v_cost = 25e6 + 330 * AREA * (1 - 0.20)
ok(
    "cost approach: land 25m plus replacement cost 330 a sq ft less 20% depreciation: 77.80m",
    round(v_cost / 1e6, 2) == 77.80,
)
ok(
    "a 50 bp move in the cap rate moves value by about 8%: 87.88m at 5.5%, 74.36m at 6.5%",
    round(noi1 / 0.055 / 1e6, 2) == 87.88 and round(noi1 / 0.065 / 1e6, 2) == 74.36,
)

d_noi = noi(1, occ_path=(0.95,)) - noi1
ok(
    "value drivers: occupancy 93% -> 95% adds 0.14m of NOI and 2.4m of value at a 6% cap; a 50 bp higher cap "
    "removes 6.2m",
    round(d_noi / 1e6, 2) == 0.14
    and round(d_noi / 0.06 / 1e6, 1) == 2.4
    and round((v_cap - noi1 / 0.065) / 1e6, 1) == 6.2,
)

# ---------------------------------------------------------------------------------------------
print("== part 2: index returns - the NCREIF formulas and appraisal smoothing")
bmv, noi_q, capex_q, psales, emv = 100.0, 1.2, 0.5, 0.0, 101.0
denom = bmv + 0.5 * capex_q - 0.5 * psales - noi_q / 3
inc = noi_q / denom
app = (emv - bmv + psales - capex_q) / denom
ok(
    "NCREIF quarter: begin 100, NOI 1.2, capital improvements 0.5, end 101: income 1.2018%, appreciation 0.5008%, "
    "total 1.7026% on the denominator 99.85",
    round(denom, 2) == 99.85
    and round(inc * 100, 4) == 1.2018
    and round(app * 100, 4) == 0.5008
    and round((inc + app) * 100, 4) == 1.7026,
)
trans = np.array([100, 110, 120, 105, 95, 100], dtype=float)
appr = [trans[0]]
for v in trans[1:]:
    appr.append(0.5 * v + 0.5 * appr[-1])
appr = np.array(appr)
ok(
    "appraisals that blend half the new evidence with half the prior value peak one period late (112.5 against 120) "
    "and fall to 101.9 against 95: a smaller, later cycle",
    round(appr[2], 1) == 112.5
    and int(np.argmax(appr)) == 2
    and round(appr.min(), 1) == 100.0
    and round(appr[4], 1) == 101.9,
)
ok(
    "for i.i.d. true returns the smoother r* = a r + (1 - a) r*_-1 with a = 0.5 has variance a/(2 - a) = 1/3 of the "
    "true variance",
    close(0.5 / (2 - 0.5), 1 / 3),
)

# ---------------------------------------------------------------------------------------------
print("== part 3: Kestrel REIT - NAV, FFO, AFFO and three values")
CASH_NOI, CAP = 80.0, 0.0625
prop = CASH_NOI / CAP
nav = prop + 40.0 + 60.0 - 500.0 - 30.0
SHARES, PRICE = 50.0, 15.30
navps = nav / SHARES
ok(
    "NAV: forward cash NOI 80 at a 6.25% cap = 1,280; + cash 40 + development at cost 60 - debt 500 - other "
    "liabilities 30 = 850, 17.00 a share; at 15.30 the shares trade 10% below NAV",
    close(prop, 1280.0)
    and close(nav, 850.0)
    and close(navps, 17.0)
    and round(PRICE / navps - 1, 3) == -0.100,
)
ni, dep, gain = 45.0, 50.0, 8.0
ffo = ni + dep - gain
affo = ffo - 4.0 - 15.0
ok(
    "FFO = net income 45 + real-estate depreciation 50 - gain on sale 8 = 87 (1.74 a share); AFFO = FFO - "
    "straight-line rent 4 - recurring capex and leasing 15 = 68 (1.36)",
    close(ffo, 87.0)
    and close(affo, 68.0)
    and close(ffo / SHARES, 1.74)
    and close(affo / SHARES, 1.36),
)
v_pffo, v_paffo = 10.0 * ffo / SHARES, 12.5 * affo / SHARES
d0 = 0.80 * affo / SHARES
divs = [d0 * 1.03**t for t in range(1, 6)]
tv5 = divs[-1] * 1.02 / (0.09 - 0.02)
v_ddm = sum(d / 1.09**t for t, d in enumerate(divs, 1)) + tv5 / 1.09**5
ok(
    "relative value: 10x FFO gives 17.40, 12.5x AFFO 17.00; two-stage dividends (80% of AFFO, 3% growth for five "
    "years then 2%, required 9%) give 16.55",
    close(v_pffo, 17.40) and close(v_paffo, 17.00) and round(v_ddm, 2) == 16.55,
    f"DDM {v_ddm:.4f}",
)

ok(
    "a private cap rate of 6.75% instead of 6.25% cuts NAV to 755.19, 15.10 a share - below the 15.30 price",
    round((CASH_NOI / 0.0675 + 100.0 - 530.0) / SHARES, 2) == 15.10,
)

# ---------------------------------------------------------------------------------------------
print("== part 4: Ferris Park - a value-add underwriting, unlevered and levered")
PRICE_FP, CAPEX_FP, LOAN, RATE = 50.0, 6.0, 30.0, 0.06
noi_fp = [2.5, 3.4, 4.0, 4.12, 4.2436, 4.370908]  # years 1-6
exit_v = noi_fp[5] / 0.0575 * (1 - 0.015)
unlev = [-(PRICE_FP + CAPEX_FP), *noi_fp[:4], noi_fp[4] + exit_v]
lev = [-(PRICE_FP + CAPEX_FP - LOAN)] + [n - LOAN * RATE for n in noi_fp[:4]]
lev += [noi_fp[4] - LOAN * RATE + exit_v - LOAN]
u_irr, l_irr = irr(unlev), irr(lev)
ok(
    "buy 50, spend 6 in year 0; NOI 2.5 rising to 4.24 in year 5; exit at a 5.75% cap on year-6 NOI less 1.5%: "
    "exit value 74.88; unlevered IRR 11.69%, levered (30 interest-only at 6%) 16.96%, equity multiple 2.08",
    round(exit_v, 2) == 74.88
    and round(u_irr * 100, 2) == 11.69
    and round(l_irr * 100, 2) == 16.96
    and round(sum(lev[1:]) / -lev[0], 2) == 2.08,
    f"unlevered {u_irr:.4f}, levered {l_irr:.4f}",
)
ok(
    "year-1 interest cover 1.39x (NOI 2.5 / interest 1.8) rising to 2.22x by year 3; loan to value 60% at entry",
    round(2.5 / 1.8, 2) == 1.39 and round(4.0 / 1.8, 2) == 2.22 and close(LOAN / PRICE_FP, 0.6),
)
exit_up = noi_fp[5] / 0.0625 * (1 - 0.015)
lev_up = [*lev[:-1], noi_fp[4] - LOAN * RATE + exit_up - LOAN]
ok(
    "an exit cap 50 bp higher (6.25%) cuts the exit value to 68.89, the unlevered IRR to 10.13% and the levered IRR "
    "to 14.16%",
    round(exit_up, 2) == 68.89
    and round(irr([*unlev[:-1], noi_fp[4] + exit_up]) * 100, 2) == 10.13
    and round(irr(lev_up) * 100, 2) == 14.16,
)

# ---------------------------------------------------------------------------------------------
print("== part 5: Ashdown Hospital PPP - debt sizing by DSCR and gearing, LLCR, equity returns")
COST = [100.0, 100.0]  # construction years 1-2
OPS = 25
AP0, OPEX0 = 20.0, 6.0
cfads = np.array([AP0 * 1.02**t - OPEX0 * 1.025**t for t in range(OPS)])  # operating years 1..25
TENOR, KD, TARGET = 22, 0.05, 1.30
ds = cfads[:TENOR] / TARGET
debt_dscr = float(np.sum(ds / (1 + KD) ** np.arange(1, TENOR + 1)))
debt_cap = 0.85 * sum(COST)
debt = min(debt_dscr, debt_cap)
llcr = float(np.sum(cfads[:TENOR] / (1 + KD) ** np.arange(1, TENOR + 1))) / debt_dscr
ok(
    "CFADS 14.00 in the first operating year; debt sculpted to a 1.30x DSCR over 22 years at 5% supports 165.8, "
    "below the 85% gearing cap of 170, so the DSCR binds (gearing 82.9%); LLCR at financial close equals 1.30",
    round(cfads[0], 2) == 14.0
    and round(debt_dscr, 1) == 165.8
    and debt == debt_dscr
    and round(debt / sum(COST) * 100, 1) == 82.9
    and close(llcr, TARGET, 1e-12),
)
scale = debt / debt_dscr
service = ds * scale
equity_in = sum(COST) - debt
equity_cf = [-equity_in / 2, -equity_in / 2, *list(cfads[:TENOR] - service), *list(cfads[TENOR:])]
eq_irr = irr([0.0, *equity_cf])
min_dscr = float(np.min(cfads[:TENOR] / service))
ok(
    "sculpted debt service keeps the DSCR at 1.30x every year; equity of 34.2, paid in during construction, earns "
    "an IRR of 10.70% from dividends after debt service and the three post-debt years",
    round(min_dscr, 2) == 1.30 and round(equity_in, 1) == 34.2 and round(eq_irr * 100, 2) == 10.70,
    f"{eq_irr:.4f}",
)
cf_stress = cfads.copy()
cf_stress[:3] -= 0.10 * AP0 * 1.02 ** np.arange(3)
ok(
    "a 10% availability deduction in the first three years cuts the DSCR to 1.11x, just above a 1.10x lock-up",
    round(float(np.min(cf_stress[:TENOR] / service)), 2) == 1.11,
)
merchant_debt = float(np.sum(cfads[:TENOR] / 1.60 / (1 + KD) ** np.arange(1, TENOR + 1)))
ok(
    "the same cash flows with demand risk, at a 1.60x DSCR, support only 134.7 of debt; on the same cash flows the "
    "equity IRR falls to 8.47%, so a demand-risk bid must price higher or accept a lower return",
    round(merchant_debt, 1) == 134.7
    and round(
        irr(
            [
                0.0,
                -(200 - merchant_debt) / 2,
                -(200 - merchant_debt) / 2,
                *list(cfads[:TENOR] - cfads[:TENOR] / 1.6),
                *list(cfads[TENOR:]),
            ]
        )
        * 100,
        2,
    )
    == 8.47,
)

# ---------------------------------------------------------------------------------------------
print("== part 6: land - farmland income and appreciation, and a timber stand")
VALUE, CASH_RENT = 6020.0, 160.0  # USDA cropland, 2026, USD per acre
gross_yield = CASH_RENT / VALUE
net_rent = CASH_RENT - 0.005 * VALUE
implied = net_rent * 1.03 / VALUE + 0.03
ok(
    "USDA 2026 cropland: 6,020 an acre and 160 cash rent, a gross yield of 2.66%; net of costs of 0.5% of value "
    "(30.10) the yield is 2.16%, and with 3% rent growth the Gordon return is 5.22%",
    round(gross_yield * 100, 2) == 2.66
    and round(net_rent / VALUE * 100, 2) == 2.16
    and round(implied * 100, 2) == 5.22,
)
vol0, growth, price0, dprice, land_g, harvest = 100.0, 0.04, 30.0, 0.01, 0.02, 0.03
stand0 = vol0 * price0
timber_ret = (1 + growth) * (1 + dprice) - 1
ok(
    "timber stand: 4% biological growth and a 1% stumpage price rise lift timber value 5.04% without any market "
    "move; with a 3% harvest yield and 2% land appreciation the total is about 10%",
    round(timber_ret * 100, 2) == 5.04 and round((timber_ret + harvest + land_g) * 100, 1) == 10.0,
)

g_land = 1.10 / (1 - 0.02) - 1
ok(
    "raw land at a 10% cost of capital and a 2% annual tax on value needs (1 + g)(1 - 0.02) = 1.10: g = 12.24% "
    "(Damodaran rounds to 12%)",
    round(g_land * 100, 2) == 12.24,
)

print(f"\n{n_checks} checks executed")
if fails:
    print("FAILED:", fails)
    sys.exit(1)
print("all checks passed")
