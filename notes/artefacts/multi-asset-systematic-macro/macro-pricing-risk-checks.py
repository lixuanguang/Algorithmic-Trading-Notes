"""Numerical checks for macro markets and pricing review (regimes, transmission maps and
practitioner frameworks), 2026-10-16.

Run with numpy and scipy:  uv run python macro-pricing-risk-checks.py
Each section prints its result and asserts what the entries state. Locators: Gliner (2014) by chapter,
section and PDF page of the ebook (no printed page numbers); Drobny (2006), printed = PDF - 15.

1. Turtle N against a standard deviation; Gliner's stop-out odds (meth:macro-position-sizing-risk).
2. Risk/reward arithmetic and the break-even hit rate (same entry).
3. Correlation is not equal moves (Gliner chap. 4) (def:global-macro-strategy).
4. A query's hit rate on six events (meth:macro-event-queries).
5. The Taylor rule (Taylor 1993, eq. (1)) and Gliner's printed variant (mod:taylor-rule).
6. Probability of a hike from an OIS rate (meth:policy-path-ois-futures).
7. Contract arithmetic: Eurodollar and Treasury futures ticks (same; conv:government-bond-futures).
8. Futures below spot with positive carry (conv:government-bond-futures).
9. Carry of a DV01-neutral steepener (meth:curve-trades-carry-rolldown).
10. Duration, DV01 and convexity (mod:duration-convexity).
11. TIPS index ratio, floor and breakevens (def:tips-breakevens).
12. CDS settlement and premium arithmetic; Gliner's recovery inference (mech:cds-contract-credit-events,
    def:sovereign-credit-defaults).
13. Variance swap units and payoff; the VIX rule of 16 (def:vix-variance-dividend-swaps).
14. Commodity contract notionals, the 3:2:1 crack spread and platinum's density (physical entries).
15. Gliner's demographic table: which column each peak year comes from (def:macroeconomic-indicators).
16. Stocks-to-use with trade (def:contango-backwardation-stocks).
17. Carry-to-risk ratio (mod:fx-carry-trade).
"""

# third party library imports
import numpy as np
from scipy import stats

rng = np.random.default_rng(37)


def section(title):
    print("\n== " + title)


# 1. Turtle N ------------------------------------------------------------------------------------
section("1. Turtle N against a standard deviation")
sig, n_days, steps = 1.0, 20_000, 390
z = rng.normal(0, sig / np.sqrt(steps), (n_days, steps)).cumsum(axis=1)
close = z[:, -1]
hi, lo = np.maximum(z.max(axis=1), 0), np.minimum(z.min(axis=1), 0)
tr = np.maximum.reduce([hi - lo, hi - 0.0, 0.0 - lo])  # previous close at 0, no overnight gap
print(
    f"  Brownian day with daily sd 1: mean true range {tr.mean():.3f} (theory 2 sqrt(2/pi) = {2 * np.sqrt(2 / np.pi):.3f}); "
    f"mean |close-to-close| {np.abs(close).mean():.3f} (sqrt(2/pi) = {np.sqrt(2 / np.pi):.3f})"
)
assert (
    abs(tr.mean() - 2 * np.sqrt(2 / np.pi)) < 0.08
)  # 390 steps a day bias the range down slightly
N = tr.mean()
p1, p2 = stats.norm.cdf(-1), stats.norm.cdf(-2)
print(
    f"  Gliner: 1N stop hit with prob {p1:.3f} a day (1 in {1 / p1:.2f}), 2N with {p2:.4f} (1 in {1 / p2:.1f}) if N were one sd"
)
print(
    f"  with N = {N:.2f} sd (an average range, not an sd), a close-to-close loss beyond 2N has prob {stats.norm.cdf(-2 * N):.5f};"
    f" an intraday low beyond 2N {np.mean(lo < -2 * N):.5f}"
)
assert abs(p2 - 0.0228) < 1e-3 and stats.norm.cdf(-2 * N) < p2


# 2. Risk/reward ---------------------------------------------------------------------------------
section("2. risk/reward arithmetic")
ev = 0.40 * 75 - 0.60 * 25
print(
    f"  40% x 75 bp - 60% x 25 bp = {ev:.0f} bp per trade (Gliner, chap. 2, PDF p. 55); break-even hit rate at 1:3 = {25 / (25 + 75):.0%}"
)
assert ev == 15 and abs(25 / 100 - 0.25) < 1e-12


# 3. Correlation and beta ----------------------------------------------------------------------------
section("3. correlation one does not mean equal moves")
a = rng.normal(0, 0.01, 1000)
b = 2.0 * a
print(
    f"  b = 2a: correlation {np.corrcoef(a, b)[0, 1]:.3f}, beta {np.polyfit(a, b, 1)[0]:.2f}: a 1.5% move in a is a 3% move in b"
)
assert abs(np.corrcoef(a, b)[0, 1] - 1) < 1e-12


# 4. Query hit rates on six events -----------------------------------------------------------------
section("4. a hit rate from six events")
p_ge5 = stats.binom.sf(4, 6, 0.5)
print(
    f"  5 of 6 (83%) up after the BoE's six QE announcements: P(>=5 of 6 | coin flip) = {p_ge5:.3f}; 6 of 6: {stats.binom.sf(5, 6, 0.5):.3f}"
)
assert abs(p_ge5 - 7 / 64) < 1e-12


# 5. Taylor rule --------------------------------------------------------------------------------------
section("5. the Taylor rule")
taylor = lambda p, y: p + 0.5 * y + 0.5 * (p - 2) + 2
print(
    f"  on target (p=2, y=0): {taylor(2, 0):.1f}% (2% real); p=4, y=0: {taylor(4, 0):.1f}%; p=2, y=-2: {taylor(2, -2):.1f}%"
)
print(
    f"  response to inflation dr/dp = {taylor(3, 0) - taylor(2, 0):.1f} > 1 (the Taylor principle)"
)
gliner_print = lambda p, y: p + 1 / (2 * y) + 0.5 * (p - 2) + 2
print(
    f"  Gliner's printed second form r = p + 1/(2y) + ... at y=2 gives {gliner_print(2, 2):.2f}, not {taylor(2, 2):.2f}: a slip for (1/2)y"
)
assert (
    taylor(2, 0) == 4
    and taylor(3, 0) - taylor(2, 0) == 1.5
    and abs(gliner_print(2, 2) - taylor(2, 2)) > 0.5
)


# 6. OIS-implied probability ----------------------------------------------------------------------------
section("6. hike probability from an OIS rate")
base, ois, step = 0.50, 0.625, 0.25
print(
    f"  Bank Rate {base}%, OIS {ois}%: ({ois}-{base})/{step} = {(ois - base) / step:.0%} (Gliner, chap. 9, PDF p. 261)"
)
# OIS averages the overnight rate over its period: a hike part-way through raises the average by less
frac_after = 0.6
prob = (ois - base) / (step * frac_after)
print(
    f"  if the meeting falls with only {frac_after:.0%} of the OIS period left, the same rate implies {prob:.0%} (and >100% is a second hike)"
)
assert abs((ois - base) / step - 0.5) < 1e-12 and prob > 0.5


# 7. Contract arithmetic -----------------------------------------------------------------------------------
section("7. Eurodollar and Treasury futures ticks")
ed = 1_000_000 * 0.0001 * 90 / 360
print(f"  Eurodollar: $1,000,000 x 1 bp x 90/360 = ${ed:.0f}")
ticks = {
    "TU (2y, $200k, 1/4 of 1/32)": 200_000 * (1 / 32) / 100 / 4,
    "FV (5y, $100k, 1/4 of 1/32)": 100_000 * (1 / 32) / 100 / 4,
    "TY (10y, $100k, 1/2 of 1/32)": 100_000 * (1 / 32) / 100 / 2,
    "US (bond, $100k, 1/32)": 100_000 * (1 / 32) / 100,
}
for k, v in ticks.items():
    print(f"  {k}: ${v:.4f}")
assert (
    ed == 25
    and ticks["TU (2y, $200k, 1/4 of 1/32)"] == 15.625
    and ticks["FV (5y, $100k, 1/4 of 1/32)"] == 7.8125
)


# 8. Futures below spot with positive carry ------------------------------------------------------------------
section("8. Treasury futures below the bond with positive carry")
P, cpn, repo, tau = 100.0, 4.0, 1.0, 0.25
F = (
    P * (1 + repo / 100 * tau) - cpn * tau
)  # ignoring accrued interest, the conversion factor and delivery options
print(
    f"  bond 100, coupon 4%, repo 1%, 3 months: forward = 100 x (1 + 0.01/4) - 4/4 = {F:.3f} < 100: carry, not a term premium"
)
assert F < P


# 9. Steepener carry ------------------------------------------------------------------------------------------
section("9. carry of a DV01-neutral steepener (long 2y, short 10y)")


def carry_per_dv01(y, D, r):  # annual carry per unit of DV01: (yield - repo) / duration
    return (y - r) / D


for y2, y10, r in [(1.5, 3.0, 1.0), (4.5, 4.0, 5.0), (2.0, 2.5, 2.4)]:
    c = carry_per_dv01(y2, 1.9, r) - carry_per_dv01(y10, 8.5, r)
    print(
        f"  2y {y2}%, 10y {y10}%, repo {r}%: carry per unit DV01 {c:+.3f} ({'positive' if c > 0 else 'negative'})"
    )
assert carry_per_dv01(1.5, 1.9, 1.0) - carry_per_dv01(3.0, 8.5, 1.0) > 0
assert carry_per_dv01(2.0, 1.9, 2.4) - carry_per_dv01(2.5, 8.5, 2.4) < 0


# 10. Duration and convexity ------------------------------------------------------------------------------------
section("10. duration, DV01, convexity")
c, n, y = 4.0, 10, 0.04
times = np.arange(1, n + 1)
cf = np.full(n, c)
cf[-1] += 100
price = lambda yy: np.sum(cf / (1 + yy) ** times)
P0 = price(y)
h = 1e-4
Dmod = -(price(y + h) - price(y - h)) / (2 * h) / P0
C = (price(y + h) - 2 * P0 + price(y - h)) / h**2 / P0
dv01 = Dmod * P0 / 10_000
dy = 0.01
approx_pct = -Dmod * dy + 0.5 * C * dy**2
exact_pct = price(y + dy) / P0 - 1
print(
    f"  10y 4% annual bond at par: modified duration {Dmod:.3f}, convexity {C:.1f}, DV01 per 100 = {dv01:.4f}"
)
print(
    f"  +100 bp: exact {exact_pct:+.4%}, -D dy + C dy^2/2 = {approx_pct:+.4%} (a percentage of price, so the price factor matters)"
)
assert abs(approx_pct - exact_pct) < 5e-4


# 11. TIPS and breakevens ---------------------------------------------------------------------------------------------
section("11. TIPS index ratio, floor, breakevens")
for infl in [0.05, -0.02]:
    ratio = 1 + infl
    print(
        f"  cumulative CPI change {infl:+.0%}: principal per 100 = {100 * ratio:.0f}; paid at maturity {max(100, 100 * ratio):.0f}; "
        f"coupons on {100 * ratio:.0f} (the floor covers principal at maturity only)"
    )
print(
    "  the price is not the index-adjusted principal: price = index ratio x real clean price, which moves with real yields"
)
be = 4.0 - 1.5
print(
    f"  breakeven 4.0 - 1.5 = {be:.1f}%: expected inflation + inflation risk premium - liquidity premium (not expectations alone)"
)
assert be == 2.5


# 12. CDS ------------------------------------------------------------------------------------------------------------------
section("12. CDS settlement and recovery")
R = 0.40
print(
    f"  physical: deliver a bond worth {R:.0%}, receive par: net {1 - R:.0%}; cash: receive par minus recovery {1 - R:.0%} (same)"
)
print(f"  100 bp running spread paid quarterly: {100 / 4:.0f} bp a quarter")
mean, sd = 55, 24
n_needed = ((stats.norm.ppf(0.975) * sd) / (mean - 40)) ** 2
print(
    f"  Moody's 1983-2006 issuer recoveries mean {mean}%, sd {sd}%: the mean differs from 40% at 5% if n > {n_needed:.1f} independent issuers;"
    " Gliner's 'not enough evidence' depends on n, which he does not give"
)
assert 9 < n_needed < 11


# 13. Variance swaps and the VIX ------------------------------------------------------------------------------------------
section("13. variance swaps and the VIX")
units = 1_000_000 / (2 * 24)
payoff = (29**2 - 24**2) * units
print(
    f"  vega notional $1m, strike 24: variance units {units:,.0f}; realised 29: payoff ${payoff:,.0f} (Gliner, chap. 8, PDF p. 226)"
)
print(
    f"  sqrt(252) = {np.sqrt(252):.2f}: VIX 16 (vol points) -> {16 / np.sqrt(252):.2f}% a day; VIX 24 -> {24 / np.sqrt(252):.2f}%"
)
assert abs(payoff - 5_520_833.33) < 1 and abs(16 / np.sqrt(252) - 1.008) < 1e-3
# the strike is fixed at inception; realised below the strike loses for the long
print(
    f"  realised 20 against strike 24: payoff ${(20**2 - 24**2) * units:,.0f} (the long pays when realised < strike)"
)


# 14. Commodity arithmetic -----------------------------------------------------------------------------------------------------
section("14. commodity contracts, crack spread, platinum")
print(
    f"  corn 5,000 bu x 500 cents = ${5000 * 5:,.0f}; copper HG 25,000 lb x 350 cents = ${25000 * 3.5:,.0f}; gold 100 oz x $1,500 = ${100 * 1500:,.0f}"
)
crude, gas, ho = 80.0, 2.40, 2.70  # $/bbl, $/gal, $/gal
crack = (2 * gas * 42 + 1 * ho * 42 - 3 * crude) / 3
print(
    f"  3:2:1 with crude $80, gasoline $2.40/gal, heating oil $2.70/gal: ({2 * gas * 42:.1f} + {ho * 42:.1f} - {3 * crude:.0f})/3 = ${crack:.2f} per barrel"
)
print(
    f"  platinum 21.45 g/cm3 against gold 19.32: ratio {21.45 / 19.32:.2f}, not 'almost twice as heavy'"
)
assert abs(crack - (2 * 2.4 * 42 + 2.7 * 42 - 240) / 3) < 1e-12 and 21.45 / 19.32 < 1.2


# 15. Demographics columns ----------------------------------------------------------------------------------------------------
section("15. Gliner's Table 12.2: prime-saving (35-69) against working-age (15-64) peaks")
table = {
    "Germany": (2006, 1986),
    "Japan": (2016, 1992),
    "Netherlands": (2012, 1989),
    "United Kingdom": (2012, 2009),
    "United States": (2016, 2007),
    "China": (2032, 2011),
    "Korea": (2023, 2015),
    "Russia": (2025, 2011),
    "Spain": (2022, 2004),
    "India": (2050, 2027),
    "Indonesia": (2050, 2023),
    "Nigeria": (2050, 2050),
    "Philippines": (2050, 2037),
}
quoted = {
    "Germany": 2006,
    "Japan": 2016,
    "Netherlands": 1989,
    "United Kingdom": 2009,
    "United States": 2007,
    "China": 2032,
    "Korea": 2023,
    "Russia": 2025,
    "Spain": 2022,
    "India": 2050,
    "Indonesia": 2050,
    "Nigeria": 2050,
    "Philippines": 2050,
}
cols = {
    k: ("prime" if quoted[k] == v[0] else "working") + ("" if v[0] != v[1] else " (same)")
    for k, v in table.items()
}
print(
    "  quoted 'peak working-age' year matches:",
    ", ".join(f"{k} {quoted[k]} -> {cols[k]}" for k in table),
)
assert (
    cols["Netherlands"] == "working"
    and cols["Germany"] == "prime"
    and cols["United Kingdom"] == "working"
)


# 16. Stocks-to-use ---------------------------------------------------------------------------------------------------------------
section("16. ending stocks with trade")
beg, prod, imp, use, exp_ = 10.0, 100.0, 5.0, 95.0, 12.0
end = beg + prod + imp - use - exp_
print(
    f"  country balance: {beg} + {prod} + {imp} - {use} - {exp_} = {end}; stocks-to-use {end / (use + exp_):.1%} "
    f"(the identity without trade gives {beg + prod - use})"
)
assert end == 8.0


# 17. Carry-to-risk ----------------------------------------------------------------------------------------------------------------
section("17. carry-to-risk")
for pair, carry, vol in [("high-yielder A", 5.0, 12.0), ("high-yielder B", 3.0, 6.0)]:
    print(f"  {pair}: carry {carry}% / vol {vol}% = {carry / vol:.2f}")
print(
    "  ranking by carry and by carry-to-risk can differ (B ranks first by ratio); both ignore skewness and crash risk"
)
assert 3 / 6 > 5 / 12

print("\nall checks passed")
