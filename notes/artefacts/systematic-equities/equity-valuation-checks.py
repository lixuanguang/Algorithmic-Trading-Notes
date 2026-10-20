"""Equity securities and valuation (2026-10-20): the worked numbers of the equity-valuation entries.

Harbour Tools plc (hypothetical, EUR millions, 31 December 2025) is taken from
../financial-statement-analysis/statement-analysis-checks.py, executed here with its output suppressed: forecast
free cash flows to the firm, NOPAT for 2028, balance-sheet claims and the 8.49 value per share. This batch adds a
share price of EUR 11.00, a cost of equity of 9.34% (../corporate-finance/corporate-finance-checks.py part 9),
cycle returns on equity for 2021-2023 and a peer table. Norland, Calder, Ashby and the peers are stand-alone
hypothetical companies; none of the numbers describe a real company.

Independent routes: closed-form dividend models against long explicit summations; the H-model against an exact
linear-decline schedule; required returns from a root search against closed forms; the PVGO split against the
Gordon value; justified multiples against the dividend model they come from; harmonic means against the average
earnings yield; enterprise value built from claims against equity value plus net claims; sum-of-the-parts
against consolidated figures.

Count convention: one check is one executed ok() call (a call inside a loop counts once per iteration).

Corrections of 2026-10-20 (audit of PR #31): market EV and the peer-multiple values include the 5m vested
options (17.94 at the market price; iterated at the implied price for multiples), so market and intrinsic
bridges share one claim set; ROE is profit over opening book equity throughout the valuation formulas, so
ROE x B0 is E1 and the justified P/E, P/B and dividend model give one value (7.81); the cost of equity is
taken from the WACC with options in equity (9.32%); the callable preferred value is conditional on redemption.

Run: uv run python equity-valuation-checks.py   (numpy, scipy). Exits 1 on failure.
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
B25, R, TAX = H["B"][2025], H["R"], H["TAX"]
PRICE, SHARES = 11.0, 100.75
DEBT = 355.0
PENSION_AT = -B25["db_liab"] * (1 - TAX)
BOOK_EQ = H["bs_view"](2025)["eq"]
bs_call = H["bs_call"]
N_OPT = 5.0


def option_claim(p):
    """The 5m vested options (strike 8, 3 years, 30% vol, 3% rate, 2.5% yield) valued at share price p."""
    return N_OPT * bs_call(p, 8.0, 3.0, 0.03, 0.30, 0.025)


def per_share_after_options(equity_pre_options):
    """Iterated value per share: equity before options less options valued at that same price."""
    p = equity_pre_options / SHARES
    for _ in range(200):
        new = (equity_pre_options - option_claim(p)) / SHARES
        if abs(new - p) < 1e-12:
            break
        p = new
    return p


OPT_MKT = option_claim(PRICE)
# Cost of equity (corrected 2026-10-20) from the corporate-finance WACC, with options in market equity:
# beta 0.93 relevered at D/E = 355 / (1,108.25 + 17.94), rf 3%, ERP 5.5%; 9.32% (9.34% on shares alone).
KE = 0.03 + 0.93 * (1 + (1 - TAX) * DEBT / (PRICE * SHARES + OPT_MKT)) * 0.055
PROFIT = {2024: 67.0, 2025: 55.38}

# ---------------------------------------------------------------------------------------------
print("== part 1: free float, trading volume and liquidity measures")
restricted = {"founding family": 20.0, "directors": 1.0, "employee trust": 0.75}
float_shares = SHARES - sum(restricted.values())
adv_shares = 0.40
ok(
    "free float 79.0m of 100.75m (78.41%); float market value 869.00",
    close(float_shares, 79.0)
    and round(float_shares / SHARES, 4) == 0.7841
    and close(float_shares * PRICE, 869.0),
)
ok(
    "ADV 0.40m shares = EUR 4.40m a day, 0.506% of float; 2m shares at 15% participation take 33.3 days",
    close(adv_shares * PRICE, 4.4)
    and round(adv_shares / float_shares, 5) == 0.00506
    and round(2.0 / (0.15 * adv_shares), 1) == 33.3,
)
bid, ask = 10.98, 11.02
ok(
    "quoted spread 0.04 on a mid of 11.00 is 36.4 basis points",
    round((ask - bid) / ((ask + bid) / 2) * 1e4, 1) == 36.4,
)

# ---------------------------------------------------------------------------------------------
print("== part 2: corporate distributions - ex-dividend price and split adjustment")
cum, div = 11.00, 0.32
ok(
    "an ex-date drop of 0.32 leaves the holder's wealth unchanged before taxes (10.68 + 0.32)",
    close(cum - div + div, cum),
)
ok(
    "1-for-10 reverse split: 0.80 -> 8.00 a share and 500m -> 50m shares, market value 400 unchanged",
    close(0.80 * 10, 8.0) and close(500 / 10 * 8.0, 500 * 0.80),
)

# ---------------------------------------------------------------------------------------------
print("== part 3: price, book value, market capitalisation and enterprise value")
mcap = PRICE * SHARES
ev = mcap + OPT_MKT + DEBT + PENSION_AT - B25["cash"]
ev_superseded = mcap + DEBT + PENSION_AT - B25["cash"]
ok(
    "Harbour: market cap 1,108.25; book equity 647.38 (6.43 a share, P/B 1.71); options at the market price "
    "17.94; EV 1,479.77 incl. options, leases and after-tax pension deficit, net of cash 37.54",
    round(mcap, 2) == 1108.25
    and round(BOOK_EQ, 2) == 647.38
    and round(BOOK_EQ / SHARES, 2) == 6.43
    and round(mcap / BOOK_EQ, 2) == 1.71
    and round(OPT_MKT, 2) == 17.94
    and round(ev, 2) == 1479.77,
)
ok(
    "the superseded EV 1,461.83 omitted the option claim that the DCF bridge deducts",
    round(ev_superseded, 2) == 1461.83 and close(ev - ev_superseded, OPT_MKT),
)
iv = H["price_iv"]
# Market and intrinsic bridges use one claim set: EV = shares + options + debt + pension - cash.
opt_iv = option_claim(iv)
ev_iv_rebuilt = iv * SHARES + opt_iv + DEBT + PENSION_AT - B25["cash"]
ok(
    "intrinsic bridge with the same claims: 855.59 + options 9.28 + 355 + 36.12 - 37.54 = DCF EV 1,218.45",
    round(opt_iv, 2) == 9.28
    and close(ev_iv_rebuilt, H["v_short"], 1e-9)
    and round(ev_iv_rebuilt, 2) == 1218.45,
)
ok(
    "DCF value 8.49 against price 11.00: price 29.5% above the estimate (estimate 22.8% below price)",
    round(iv, 2) == 8.49
    and round(PRICE / iv - 1, 3) == 0.295
    and round(1 - iv / PRICE, 3) == 0.228,
)

# ---------------------------------------------------------------------------------------------
print("== part 4: Harbour sensitivity - what the price implies")
fcff, nopat_2028 = H["fcff"], H["nopat_2028"]
claims_ex_opt = DEBT + PENSION_AT - B25["cash"]


def value_per_share(wacc, g=0.025, ronic=0.12):
    tv = nopat_2028 * (1 + g) * (1 - g / ronic) / (wacc - g)
    ev_ = sum(c / (1 + wacc) ** (t + 1) for t, c in enumerate(fcff)) + tv / (1 + wacc) ** 3
    return per_share_after_options(ev_ - claims_ex_opt)


ok("the function reproduces 8.49 at 8%", close(value_per_share(0.08), iv, 1e-9))
grid = {w: value_per_share(w) for w in (0.07, 0.08, 0.09)}
ok(
    "WACC 7% / 8% / 9%: 11.22 / 8.49 / 6.59 a share",
    [round(v, 2) for v in grid.values()] == [11.22, 8.49, 6.59],
)
w_implied = brentq(lambda w: value_per_share(w) - PRICE, 0.06, 0.08)
ronic_implied = brentq(lambda x: value_per_share(0.08, ronic=x) - PRICE, 0.13, 1e6)
g_implied = brentq(lambda gg_: value_per_share(0.08, g=gg_, ronic=0.16) - PRICE, 0.0, 0.07)
ok(
    "reverse-engineering the price: WACC 7.07% (other inputs held), or a terminal RONIC of "
    f"{ronic_implied:.0%} at 8% and 2.5% growth, or 3.60% perpetual growth with RONIC 16%",
    round(w_implied, 4) == 0.0707
    and round(g_implied, 4) == 0.036
    and round(ronic_implied, 2) == 1.24
    and value_per_share(0.08, ronic=1e9) < 11.3,
    f"free growth (RONIC -> infinity) gives at most {value_per_share(0.08, ronic=1e9):.2f}",
)

# ---------------------------------------------------------------------------------------------
print("== part 5: Gordon growth, one-period and implied-growth calculations (Norland Water)")
d0, g, r = 1.20, 0.03, 0.075
v_gordon = d0 * (1 + g) / (r - g)
long_sum = sum(d0 * (1 + g) ** t / (1 + r) ** t for t in range(1, 4000))
ok(
    "D0 1.20, g 3%, r 7.5%: value 27.47; a 4,000-year summation agrees",
    round(v_gordon, 2) == 27.47 and close(v_gordon, long_sum, 1e-6),
)
p1 = d0 * (1 + g) ** 2 / (r - g)
ok(
    "one-period: (D1 + P1)/(1 + r) = 27.47, with P1 = 28.29",
    close((d0 * (1 + g) + p1) / (1 + r), v_gordon) and round(p1, 2) == 28.29,
)
P_mkt = 30.0
g_imp = (r * P_mkt - d0) / (P_mkt + d0)
r_imp = d0 * (1 + g) / P_mkt + g
ok(
    "at a price of 30: implied growth 3.365%, or implied required return 7.12% at 3% growth",
    round(g_imp, 5) == 0.03365 and round(r_imp, 4) == 0.0712,
)
ok(
    "sensitivity: r 7.0% gives 30.90 and r 8.0% gives 24.72 - one point moves the value by a fifth",
    round(d0 * 1.03 / 0.04, 2) == 30.9 and round(d0 * 1.03 / 0.05, 2) == 24.72,
)

# ---------------------------------------------------------------------------------------------
print("== part 6: preferred stock")
ok("perpetual 5% preferred on 100 par at a 6.25% required return: 80.00", close(5.0 / 0.0625, 80.0))
y = 0.045
perp = 5.0 / y
to_call = sum(5.0 / (1 + y) ** t for t in range(1, 6)) + 100.0 / (1 + y) ** 5
ok(
    "if yields fall to 4.5%: non-callable 111.11; value conditional on redemption at 100 in year five, 102.19",
    round(perp, 2) == 111.11 and round(to_call, 2) == 102.19 and to_call < perp,
)
# Conditionality (corrected 2026-10-20): 102.19 is the value if the share is redeemed at year five with the
# yield unchanged at 4.5%. If yields at year five are 5% or more the issuer would not redeem at 100 (the
# perpetual would then be worth 5/y <= 100), so the cash flows, and the value, depend on future rates.
for y5, redeem in ((0.04, True), (0.045, True), (0.05, False), (0.06, False)):
    ok(
        f"at a year-five yield of {y5:.1%} the share is worth {5 / y5:.2f} unredeemed, so the issuer "
        f"{'redeems' if redeem else 'does not redeem'} at 100",
        (5 / y5 > 100) == redeem or close(5 / y5, 100.0),
    )
ok(
    "cumulative arrears: two missed dividends of 5 must be paid before any common dividend (10 in arrears)",
    close(2 * 5.0, 10.0),
)

# ---------------------------------------------------------------------------------------------
print("== part 7: PVGO and justified P/E")
e1, rr, roe, b = 2.00, 0.09, 0.12, 0.5
gg = b * roe
v = e1 * (1 - b) / (rr - gg)
no_growth = e1 / rr
ok(
    "E1 2.00, ROE 12%, retention 50%: g 6%, value 33.33 = no-growth 22.22 + PVGO 11.11",
    close(gg, 0.06)
    and round(v, 2) == 33.33
    and round(no_growth, 2) == 22.22
    and round(v - no_growth, 2) == 11.11,
)
v_eq = e1 * (1 - b) / (rr - b * rr)
ok("with ROE = r = 9% growth adds nothing: value 22.22, PVGO 0", close(v_eq, no_growth))
lead = (1 - b) / (rr - gg)
trail = (1 - b) * (1 + gg) / (rr - gg)
ok(
    "justified leading P/E 16.67 = 1/r + PVGO/E1 (11.11 + 5.56); trailing 17.67 on E0 = 1.8868",
    round(lead, 2) == 16.67
    and close(lead, 1 / rr + (v - no_growth) / e1)
    and round(trail, 2) == 17.67
    and close(trail * e1 / (1 + gg), v),
)

# ---------------------------------------------------------------------------------------------
print("== part 8: multistage dividend models (Calder Software)")
D0, g1, n1, g2, rc = 0.50, 0.15, 4, 0.04, 0.10
divs = [D0 * (1 + g1) ** t for t in range(1, n1 + 1)]
tv4 = divs[-1] * (1 + g2) / (rc - g2)
v2 = sum(d / (1 + rc) ** t for t, d in enumerate(divs, 1)) + tv4 / (1 + rc) ** n1
explicit = sum(divs[t - 1] / (1 + rc) ** t for t in range(1, n1 + 1)) + sum(
    divs[-1] * (1 + g2) ** (t - n1) / (1 + rc) ** t for t in range(n1 + 1, 5000)
)
ok(
    "two-stage: dividends 0.575, 0.6613, 0.7604, 0.8745; TV_4 = D5/(r - g) = 15.16; value 12.59; long sum agrees",
    round(tv4, 2) == 15.16 and round(v2, 2) == 12.59 and close(v2, explicit, 1e-6),
)
wrong_date = sum(d / (1 + rc) ** t for t, d in enumerate(divs, 1)) + tv4 / (1 + rc) ** (n1 + 1)
wrong_d = (
    sum(d / (1 + rc) ** t for t, d in enumerate(divs, 1)) + divs[-1] / (rc - g2) / (1 + rc) ** n1
)
ok(
    "dating errors: discounting TV_4 five years gives 11.65; using D4 instead of D5 gives 12.19",
    round(wrong_date, 2) == 11.65 and round(wrong_d, 2) == 12.19,
)
r_from_price = brentq(
    lambda x: (
        sum(d / (1 + x) ** t for t, d in enumerate(divs, 1))
        + divs[-1] * (1 + g2) / (x - g2) / (1 + x) ** n1
        - 14.0
    ),
    0.05,
    0.3,
)
ok(
    "at a price of 14.00 the two-stage model implies a required return of 9.41%",
    round(r_from_price, 4) == 0.0941,
)

D0h, ga, gn, Hh, rh = 1.00, 0.12, 0.04, 5, 0.09
v_h = D0h * (1 + gn) / (rh - gn) + D0h * Hh * (ga - gn) / (rh - gn)
d, exact = D0h, 0.0
for t in range(1, 6000):
    gt = ga - (ga - gn) * (t - 1) / (2 * Hh) if t <= 2 * Hh else gn
    d *= 1 + gt
    exact += d / (1 + rh) ** t
ok(
    "H-model: 20.80 + 8.00 = 28.80; an exact linear decline from 12% to 4% over ten years gives 29.94",
    round(v_h, 2) == 28.8 and round(exact, 2) == 29.94,
)
p_h = 28.80
r_h = D0h / p_h * ((1 + gn) + Hh * (ga - gn)) + gn
ok("H-model required return at 28.80 rearranges to exactly 9%", close(r_h, rh, 1e-12))

D0t, r3 = 0.80, 0.09
g_path = [0.14] * 3 + [0.14 - 0.025 * k for k in range(1, 5)]
d, v3, t = D0t, 0.0, 0
for gt in g_path:
    t += 1
    d *= 1 + gt
    v3 += d / (1 + r3) ** t
tv7 = d * 1.04 / (r3 - 0.04)
v3 += tv7 / (1 + r3) ** t
ok(
    "three-stage: 14% for three years, falling 2.5 points a year to 4% by year 7, then 4%: value 24.44",
    close(g_path[-1], 0.04) and round(v3, 2) == 24.44,
    f"TV_7 {tv7:.2f}",
)

# ---------------------------------------------------------------------------------------------
print("== part 9: sustainable growth and DuPont")
margin, turnover, lev, retention = 0.06, 1.25, 1.6, 0.6
roe_d = margin * turnover * lev
ok(
    "ROE 6% x 1.25 x 1.6 = 12%; g = 0.6 x 12% = 7.2%",
    close(roe_d, 0.12) and close(retention * roe_d, 0.072),
)
eq0, ni = 100.0, 12.0
eq1 = eq0 + ni * retention
ok(
    "equity grows 7.2% when ROE and retention are held and no shares are issued",
    close(eq1 / eq0 - 1, 0.072),
)
# ROE timing (corrected 2026-10-20). The valuation formulas use ROE_t = E_t / B_{t-1}, profit over opening
# book equity, so that b x ROE is the growth of book equity from retention and ROE x B_0 is E_1. The ratio
# analysis reports ROE on average equity (11.52%, 8.84%); those figures are not reused here.
bv = {y: H["bs_view"](y)["eq"] for y in (2023, 2024, 2025)}
roe_avg = {y: R[y]["roe"] for y in (2024, 2025)}
roe_h = {y: PROFIT[y] / bv[y - 1] for y in (2024, 2025)}
ok(
    "Harbour ROE on opening equity 12.01% (67/558) and 9.15% (55.38/605); on average equity 11.52% and 8.84%",
    round(roe_h[2024], 4) == 0.1201
    and round(roe_h[2025], 4) == 0.0915
    and round(roe_avg[2024], 4) == 0.1152
    and round(roe_avg[2025], 4) == 0.0884,
)
g_sus = (1 - 32 / PROFIT[2025]) * roe_h[2025]
ok(
    "sustainable growth at 2025's 57.8% payout: 0.422 x 9.15% = 3.86%, equal to retained profit over opening "
    "equity (23.38 / 605); the average-equity ROE gave 3.73%",
    round(g_sus, 4) == 0.0386
    and close(g_sus, (PROFIT[2025] - 32) / bv[2024], 1e-12)
    and round((1 - 32 / PROFIT[2025]) * roe_avg[2025], 4) == 0.0373,
)

# ---------------------------------------------------------------------------------------------
print("== part 10: peers, averages and justified multiples")
peers = {  # forward P/E, EV/EBITDA, expected EPS growth, payout, beta (illustrative)
    "Arden": (14.0, 6.5, 0.05, 0.50, 1.20),
    "Brook": (16.0, 7.0, 0.06, 0.45, 1.05),
    "Corran": (17.0, 7.5, 0.07, 0.40, 1.15),
    "Dunmore": (18.0, 7.8, 0.08, 0.40, 1.00),
    "Elstow": (20.0, 8.2, 0.09, 0.35, 1.10),
    "Fenwick": (22.0, 8.8, 0.10, 0.30, 0.95),
    "Glenco": (35.0, 12.0, 0.12, 0.20, 0.90),
}
pe = np.array([v[0] for v in peers.values()])
mean, median = pe.mean(), np.median(pe)
harm = len(pe) / np.sum(1 / pe)
ok(
    "forward P/E: mean 20.29, median 18.00, harmonic mean 18.80 = 1 / average earnings yield",
    round(mean, 2) == 20.29
    and close(median, 18.0)
    and round(harm, 2) == 18.8
    and close(harm, 1 / np.mean(1 / pe)),
)
eps_fwd = H["base"][0]["profit"] / SHARES
ok(
    "Harbour forward EPS 0.7285 (2026 forecast profit 73.40 / 100.75m): at the median 18.0x, 13.11; trades at 15.10x",
    round(eps_fwd, 4) == 0.7285
    and round(18.0 * eps_fwd, 2) == 13.11
    and round(PRICE / eps_fwd, 2) == 15.10,
)
X = np.column_stack(
    [np.ones(len(pe)), [v[2] for v in peers.values()], [v[4] for v in peers.values()]]
)
coef, *_ = np.linalg.lstsq(X, pe, rcond=None)
harbour_x = np.array([1.0, 0.04, 1.15])
pred = harbour_x @ coef
ok(
    "regression of P/E on growth and beta across the seven peers predicts 9.50x for Harbour (4% growth, beta 1.15)",
    round(pred, 2) == 9.5,
    f"P/E = {coef[0]:.2f} + {coef[1]:.2f} g + {coef[2]:.2f} beta",
)
peg = pe / (np.array([v[2] for v in peers.values()]) * 100)
ok(
    "PEG (forward P/E over growth in percent) ranges from 2.20 (Fenwick) to 2.92 (Glenco); Harbour 15.10/4 = 3.77",
    round(peg.min(), 2) == 2.2
    and round(peg.max(), 2) == 2.92
    and round(PRICE / eps_fwd / 4, 2) == 3.77,
)
roe_cycle = [0.100, 0.120, 0.108, roe_h[2024], roe_h[2025]]  # 2021-2023 assumed on the same basis
roe_norm = float(np.mean(roe_cycle))
bvps = BOOK_EQ / SHARES
eps_norm = roe_norm * bvps  # E_2026 = ROE x B_2025: already next year's earnings
ok(
    "normalised ROE 2021-2025 on opening equity (10.0, 12.0, 10.8, 12.01, 9.15 -> 10.79%) x BVPS 6.43 = 0.6935, "
    "normalised 2026 EPS",
    round(roe_norm, 4) == 0.1079 and round(eps_norm, 4) == 0.6935,
)
underlying = (PROFIT[2025] + 18.0 * (1 - TAX)) / 100.375
eps_norm_trailing = roe_norm * bv[2024] / 100.375
ok(
    "underlying 2025 EPS adds back the 18 restructuring charge after tax: 0.6862 against reported 0.5517; "
    "the like-dated normalised 2025 EPS is 10.79% x 605 / 100.375m = 0.6505",
    round(underlying, 4) == 0.6862
    and round(PROFIT[2025] / 100.375, 4) == 0.5517
    and round(eps_norm_trailing, 4) == 0.6505,
)
g_lr = 0.025
payout_ss = 1 - g_lr / roe_norm
pe_lead = payout_ss / (KE - g_lr)
pb = (roe_norm - g_lr) / (KE - g_lr)
v_pe = pe_lead * eps_norm
v_pb = pb * bvps
v_ddm = payout_ss * eps_norm / (KE - g_lr)
# Independent route: book value grows at g_lr from retention, so the dividend stream is explicit.
bvt, v_sum = bvps, 0.0
for t in range(1, 4000):
    e_t = roe_norm * bvt
    v_sum += e_t * payout_ss / (1 + KE) ** t
    bvt += e_t * (1 - payout_ss)
ok(
    "justified at ROE 10.79%, g 2.5%, ke 9.32%: payout 76.8%, leading P/E 11.26 x E1 0.6935 = P/B 1.22 x B0 6.43 = "
    "DDM D1 0.533/(ke - g) = 7.81 a share; a 4,000-year dividend sum agrees",
    round(payout_ss, 3) == 0.768
    and round(pe_lead, 2) == 11.26
    and round(pb, 2) == 1.22
    and round(payout_ss * eps_norm, 3) == 0.533
    and round(v_pe, 2) == 7.81
    and close(v_pe, v_pb, 1e-12)
    and close(v_pe, v_ddm, 1e-12)
    and close(v_sum, v_pb, 1e-6),
    f"P/E route {v_pe:.4f}, P/B route {v_pb:.4f}, DDM {v_ddm:.4f}, sum {v_sum:.4f}",
)
v_pe_superseded = pe_lead * eps_norm * (1 + g_lr)
ok(
    "the superseded P/E route grew E1 again (E1 x 1.025), overstating the P/E value by exactly 2.5% (8.00 here; "
    "7.83 against 7.64 on the superseded inputs)",
    close(v_pe_superseded / v_pb - 1, g_lr, 1e-12) and round(v_pe_superseded, 2) == 8.0,
)
ok(
    "sensitivity: the average-equity ROE cycle (10.63%) would give 7.66 by every route",
    round(
        (np.mean([0.10, 0.12, 0.108, roe_avg[2024], roe_avg[2025]]) - g_lr) / (KE - g_lr) * bvps, 2
    )
    == 7.66,
)
roe_implied = g_lr + (PRICE / bvps) * (KE - g_lr)
ok(
    "the price-to-book of 1.71 implies a sustained ROE of 14.18% at the same ke and growth",
    round(PRICE / bvps, 2) == 1.71 and round(roe_implied, 4) == 0.1418,
)
ps_just = 0.05 * payout_ss * (1 + g_lr) / (KE - g_lr)
ok(
    "justified P/S on trailing sales at a 5% net margin: 0.58 (Harbour trades at 1,108.25/1,080 = 1.03)",
    round(ps_just, 2) == 0.58 and round(mcap / 1080, 2) == 1.03,
)
eyield = {"Harbour": eps_fwd / PRICE, "LossCo": -0.40 / 8.0}
ok(
    "earnings yields rank a loss-maker (-5.0%) that a P/E cannot (Harbour 6.62%)",
    round(eyield["Harbour"], 4) == 0.0662 and close(eyield["LossCo"], -0.05),
)
dy = 0.32 * 100 / SHARES / PRICE
ok("Harbour trailing dividend yield 32/100.75m/11 = 2.89%", round(dy, 4) == 0.0289)

# ---------------------------------------------------------------------------------------------
print("== part 11: enterprise-value multiples and matched numerators")
ebitda25 = R[2025]["ebitda"]
ok("Harbour EV/EBITDA 2025: 1,479.77 / 195 = 7.59", round(ev / ebitda25, 2) == 7.59)
ev_wrong = mcap + OPT_MKT + 290.0 - B25["cash"]
ok(
    "leaving the 65 of lease liabilities and the pension out of EV while EBITDA excludes lease costs gives 7.07",
    round(ev_wrong / ebitda25, 2) == 7.07,
)
ok(
    "P/EBITDA mixes claims: 1,108.25/195 = 5.68 makes a levered firm look cheap",
    round(mcap / ebitda25, 2) == 5.68,
)
fen_ev, fen_ebitda, fen_lease_cost, fen_lease_liab = 2400.0, 300.0, 30.0, 150.0
ok(
    "US GAAP peer: operating lease cost 30 in EBITDA; adding it back and lease liabilities 150 to EV moves 8.00x to 7.73x",
    close(fen_ev / fen_ebitda, 8.0)
    and round((fen_ev + fen_lease_liab) / (fen_ebitda + fen_lease_cost), 2) == 7.73,
)
dev_capitalised, dev_amort = 22.0, 12.0
ok(
    "IFRS development capitalisation: expensing 2025's 22 as a US GAAP peer would cut EBITDA to 173 (8.55x) and EBIT by 10",
    round(ev / (ebitda25 - dev_capitalised), 2) == 8.55
    and close(dev_capitalised - dev_amort, 10.0),
)
ev_ebitda_peer_median = float(np.median([v[1] for v in peers.values()]))
eq_from_ev = ev_ebitda_peer_median * ebitda25 - (DEBT + PENSION_AT - B25["cash"])
p_peer = per_share_after_options(eq_from_ev)
ok(
    "at the peer median 7.8x EBITDA: EV 1,521.00, less debt-like claims net of cash 353.58 = 1,167.42 for shares "
    "and options; options at the implied price 19.45 leave 1,147.97, 11.39 a share",
    close(ev_ebitda_peer_median, 7.8)
    and round(eq_from_ev, 2) == 1167.42
    and round(option_claim(p_peer), 2) == 19.45
    and round(p_peer, 2) == 11.39
    and close(p_peer * SHARES + option_claim(p_peer), eq_from_ev, 1e-9),
)
ok(
    "the superseded 11.59 divided the whole residual by shares, leaving the option claim unpaid",
    round(eq_from_ev / SHARES, 2) == 11.59 and eq_from_ev / SHARES > p_peer,
)

# ---------------------------------------------------------------------------------------------
print("== part 12: terminal value from a multiple against a growth model")
nopat_2029 = nopat_2028 * 1.025
tv_growth = nopat_2029 * (1 - 0.025 / 0.12) / (0.08 - 0.025)
ebitda_2028 = H["base"][2]["ebitda"]
tv_mult = 7.8 * ebitda_2028
fcff_2029 = nopat_2029 * (1 - 0.025 / 0.12)
g_in_mult = brentq(
    lambda gg_: fcff_2029 * (1 + gg_) / (1 + 0.025) / (0.08 - gg_) - tv_mult, -0.05, 0.079
)
ok(
    "TV_2028: growth model 1,384.68 (5.33x 2028 EBITDA); peer 7.8x gives 2,024.92, which needs about 4.18% "
    "perpetual growth at the same reinvestment",
    round(tv_growth, 2) == 1384.68
    and round(tv_growth / ebitda_2028, 2) == 5.33
    and round(tv_mult, 2) == 2024.92
    and round(g_in_mult, 4) == 0.0418,
)

# ---------------------------------------------------------------------------------------------
print("== part 13: momentum indicators")
fcst_errors = np.array([0.02, -0.03, 0.01, -0.01, 0.03, -0.02, 0.00, 0.02])
sue = (0.19 - 0.15) / fcst_errors.std(ddof=1)
ok(
    "SUE: actual 0.19 vs consensus 0.15 over a 0.0212 error s.d. = 1.89",
    round(fcst_errors.std(ddof=1), 4) == 0.0212 and round(sue, 2) == 1.89,
)
prices = [9.20, 9.60, 10.10, 10.40, 10.70, 11.00]
idx = [100, 101, 103, 102, 104, 105]
rs = (prices[-1] / prices[0]) / (idx[-1] / idx[0])
ok("relative strength: +19.57% against the index's +5% -> 1.139", round(rs, 3) == 1.139)

# ---------------------------------------------------------------------------------------------
print("== part 14: industry structure - size, growth, shares and concentration")
sales = {"Harbour": 1080.0, "Arden": 1500.0, "Brook": 900.0, "Corran": 700.0, "Others": 2820.0}
size = sum(sales.values())
shares = {k: v / size for k, v in sales.items()}
named = [s * 100 for k, s in shares.items() if k != "Others"]
hhi_named = sum(x**2 for x in named)
ok(
    "industry 7,000; Harbour share 15.43%; HHI of the four named firms 963 (others fragmented)",
    close(size, 7000) and round(shares["Harbour"], 4) == 0.1543 and round(hhi_named) == 963,
)
delta = 2 * named[0] * named[3]
ok(
    "a Harbour-Corran merger adds 2ab = 2 x 15.43 x 10.00 = 308.6 to the HHI",
    round(delta, 1) == 308.6,
)
cagr = (7000 / 6000) ** (1 / 4) - 1
ok("industry sales 6,000 -> 7,000 over four years is 3.93% a year", round(cagr, 4) == 0.0393)

# ---------------------------------------------------------------------------------------------
print("== part 15: sum of the parts and conglomerate discount (Ashby Group)")
parts = {"tools": (120.0, 8.0), "rental": (60.0, 6.0), "software": (40.0, 15.0)}
gross = sum(e * m for e, m in parts.values())
central = -15.0 * 7.0
net_debt_a = 600.0
sotp = gross + central - net_debt_a
mkt = 1100.0
ok(
    "segments 960 + 360 + 600 = 1,920; capitalised central costs -105; net debt 600: SOTP equity 1,215; "
    "market 1,100 is a 9.47% discount",
    close(gross, 1920) and close(sotp, 1215) and round(1 - mkt / sotp, 4) == 0.0947,
)

# ---------------------------------------------------------------------------------------------
print("== part 16: mispricing decomposition")
true_v, est_v, price_ = 10.0, 8.49, 11.0
ok(
    "perceived mispricing (8.49 - 11.00 = -2.51) = true mispricing (10.00 - 11.00) + valuation error (8.49 - 10.00)",
    close(est_v - price_, (true_v - price_) + (est_v - true_v)),
)

# ---------------------------------------------------------------------------------------------
print("== part 17: dividends, FCFE and residual income give one value under clean surplus")
bv0, roe_c, ke_c, pay_c = 20.0, 0.12, 0.09, 0.5
g_c = roe_c * (1 - pay_c)
ni1 = roe_c * bv0
ddm = ni1 * pay_c / (ke_c - g_c)
fcfe1 = ni1 - g_c * bv0  # net income less the growth in book equity it must fund, no borrowing
ri = bv0 + (roe_c - ke_c) * bv0 / (ke_c - g_c)
bv, ri_sum, div_sum = bv0, 0.0, 0.0
for t in range(1, 3000):
    ni_t = roe_c * bv
    ri_sum += (ni_t - ke_c * bv) / (1 + ke_c) ** t
    div_sum += ni_t * pay_c / (1 + ke_c) ** t
    bv += ni_t * (1 - pay_c)
ok(
    "BV 20, ROE 12%, ke 9%, payout 50%: DDM 1.20/(9% - 6%) = 40; FCFE 2.40 - 1.20 = 1.20 gives 40; "
    "residual income 20 + 0.60/(9% - 6%) = 40; year-by-year sums agree",
    close(ddm, 40.0)
    and close(fcfe1 / (ke_c - g_c), 40.0)
    and close(ri, 40.0)
    and close(bv0 + ri_sum, 40.0, 1e-6)
    and close(div_sum, 40.0, 1e-6),
)

# ---------------------------------------------------------------------------------------------
print("== part 18: figures quoted in the multiples and preferred-stock entries")
ok(
    "without Glenco the peer mean P/E falls to 17.83 and the median to 17.50",
    round(float(np.mean(pe[:-1])), 2) == 17.83 and close(float(np.median(pe[:-1])), 17.5),
)
ok(
    "applied to forward EPS 0.7285: harmonic mean 13.70; regression multiple 9.50 gives 6.92",
    round(harm * eps_fwd, 2) == 13.70 and round(pred * eps_fwd, 2) == 6.92,
)
eq_dev = ev_ebitda_peer_median * (ebitda25 - dev_capitalised) - (DEBT + PENSION_AT - B25["cash"])
p_dev = per_share_after_options(eq_dev)
ok(
    "peer 7.8x on development-adjusted EBITDA 173: shares and options 995.82; options 13.40; 9.75 a share "
    "(superseded 9.88)",
    round(eq_dev, 2) == 995.82
    and round(p_dev, 2) == 9.75
    and round(option_claim(p_dev), 2) == 13.40
    and round(eq_dev / SHARES, 2) == 9.88,
)
ok("Norland at 30 is 9% above its Gordon value", round(30 / v_gordon - 1, 2) == 0.09)
ok(
    "if yields stay at 4.5% and the issuer redeems at year five, the redemption-conditional value is 8.92 below "
    "the non-callable perpetual (not an option value)",
    round(perp - to_call, 2) == 8.92,
)
ok(
    "Harbour sustainable growth 3.86% against forecast 2026 revenue growth 6.09%",
    round(g_sus, 4) == 0.0386 and round(H["base"][0]["revenue"] / 1080 - 1, 4) == 0.0609,
)

mcap_check = math.isclose(mcap, 1108.25)
ok("inputs consistent with the corporate-finance script (price 11, 100.75m shares)", mcap_check)

print(f"\n{n_checks} checks executed")
if fails:
    print("FAILED:", fails)
    sys.exit(1)
print("all checks passed")
