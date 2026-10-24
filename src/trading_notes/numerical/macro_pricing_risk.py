"""Macro pricing risk: regimes, transmission maps, rates and carry, and practitioner frameworks.

Numerical checks for macro markets and pricing review (regimes, transmission maps and practitioner
frameworks), 2026-10-16. Each section prints its result and asserts what the entries state.
Locators: Gliner (2014) by chapter, section and PDF page of the ebook (no printed page numbers);
Drobny (2006), printed = PDF - 15.

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
12. CDS settlement and premium arithmetic; Gliner's recovery inference
   (mech:cds-contract-credit-events, def:sovereign-credit-defaults).
13. Variance swap units and payoff; the VIX rule of 16 (def:vix-variance-dividend-swaps).
14. Commodity contract notionals, the 3:2:1 crack spread and platinum's density (physical entries).
15. Gliner's demographic table: which column each peak year comes from
   (def:macroeconomic-indicators).
16. Stocks-to-use with trade (def:contango-backwardation-stocks).
17. Carry-to-risk ratio (mod:fx-carry-trade).

One generator, seeded 37, serves parts 1 and 3 in order; the other parts draw nothing. Each
part returns the names of its failed checks; a failure prints BAD and exits 1, and a passing run
prints nothing for its checks.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.macro_pricing_risk
(numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import sys
from typing import Final

# third party library imports
import numpy as np
from numpy.typing import NDArray
from scipy import stats

type Floats = NDArray[np.float64]

SEED: Final = 37


def section(title: str) -> None:
    """Print a section heading."""
    print("\n== " + title)


def check(failed: list[str], name: str, cond: bool) -> None:
    """Record name in failed when cond is false; a passing check prints nothing."""
    if not cond:
        failed.append(name)


def taylor(p: float, y: float) -> float:
    """Return the Taylor rule rate: inflation p and output gap y, in percent."""
    return p + 0.5 * y + 0.5 * (p - 2) + 2


def gliner_print(p: float, y: float) -> float:
    """Return Gliner's printed second form of the Taylor rule, with 1/(2y) for the output term."""
    return p + 1 / (2 * y) + 0.5 * (p - 2) + 2


def carry_per_dv01(y: float, D: float, r: float) -> float:
    """Return the annual carry per unit of DV01: (yield - repo) / duration."""
    return (y - r) / D


def check_turtle(rng: np.random.Generator) -> list[str]:
    """Part 1: the Turtle N against a standard deviation, and Gliner's stop-out odds."""
    failed: list[str] = []
    section("1. Turtle N against a standard deviation")
    sig, n_days, steps = 1.0, 20_000, 390
    z = rng.normal(0, sig / np.sqrt(steps), (n_days, steps)).cumsum(axis=1)
    close = z[:, -1]
    hi, lo = np.maximum(z.max(axis=1), 0), np.minimum(z.min(axis=1), 0)
    tr = np.maximum.reduce([hi - lo, hi - 0.0, 0.0 - lo])  # previous close at 0, no overnight gap
    print(
        f"  Brownian day with daily sd 1: mean true range {tr.mean():.3f} (theory 2 sqrt(2/pi) ="
        f" {2 * np.sqrt(2 / np.pi):.3f}); mean |close-to-close| {np.abs(close).mean():.3f}"
        f" (sqrt(2/pi) = {np.sqrt(2 / np.pi):.3f})"
    )
    # 390 steps a day bias the range down slightly
    check(
        failed,
        "mean true range within 0.08 of 2 sqrt(2/pi)",
        bool(abs(tr.mean() - 2 * np.sqrt(2 / np.pi)) < 0.08),
    )
    N = tr.mean()
    p1, p2 = stats.norm.cdf(-1), stats.norm.cdf(-2)
    print(
        f"  Gliner: 1N stop hit with prob {p1:.3f} a day (1 in {1 / p1:.2f}), 2N with {p2:.4f}"
        f" (1 in {1 / p2:.1f}) if N were one sd"
    )
    print(
        f"  with N = {N:.2f} sd (an average range, not an sd), a close-to-close loss beyond 2N has"
        f" prob {stats.norm.cdf(-2 * N):.5f}; an intraday low beyond 2N {np.mean(lo < -2 * N):.5f}"
    )
    check(
        failed,
        "2N stop-out odds 0.0228 and below the close-to-close tail",
        bool(abs(p2 - 0.0228) < 1e-3 and stats.norm.cdf(-2 * N) < p2),
    )
    return failed


def check_risk_reward() -> list[str]:
    """Part 2: the expected value of a 1:3 trade and its break-even hit rate."""
    failed: list[str] = []
    section("2. risk/reward arithmetic")
    ev = 0.40 * 75 - 0.60 * 25
    print(
        f"  40% x 75 bp - 60% x 25 bp = {ev:.0f} bp per trade (Gliner, chap. 2, PDF p. 55);"
        f" break-even hit rate at 1:3 = {25 / (25 + 75):.0%}"
    )
    check(failed, "expected value 15 bp per trade", bool(ev == 15 and abs(25 / 100 - 0.25) < 1e-12))
    return failed


def check_correlation(rng: np.random.Generator) -> list[str]:
    """Part 3: a correlation of one still allows a beta of two."""
    failed: list[str] = []
    section("3. correlation one does not mean equal moves")
    a = rng.normal(0, 0.01, 1000)
    b = 2.0 * a
    print(
        f"  b = 2a: correlation {np.corrcoef(a, b)[0, 1]:.3f}, beta {np.polyfit(a, b, 1)[0]:.2f}: a"
        " 1.5% move in a is a 3% move in b"
    )
    check(failed, "b = 2a: correlation one", bool(abs(np.corrcoef(a, b)[0, 1] - 1) < 1e-12))
    return failed


def check_event_hits() -> list[str]:
    """Part 4: the chance of five or more ups in six events by coin flip."""
    failed: list[str] = []
    section("4. a hit rate from six events")
    p_ge5 = stats.binom.sf(4, 6, 0.5)
    print(
        f"  5 of 6 (83%) up after the BoE's six QE announcements: P(>=5 of 6 | coin flip) ="
        f" {p_ge5:.3f}; 6 of 6: {stats.binom.sf(5, 6, 0.5):.3f}"
    )
    check(failed, "P(>=5 of 6) = 7/64", bool(abs(p_ge5 - 7 / 64) < 1e-12))
    return failed


def check_taylor() -> list[str]:
    """Part 5: the Taylor rule and Gliner's printed variant."""
    failed: list[str] = []
    section("5. the Taylor rule")
    print(
        f"  on target (p=2, y=0): {taylor(2, 0):.1f}% (2% real); p=4, y=0: {taylor(4, 0):.1f}%;"
        f" p=2, y=-2: {taylor(2, -2):.1f}%"
    )
    print(
        f"  response to inflation dr/dp = {taylor(3, 0) - taylor(2, 0):.1f} > 1 (the Taylor"
        " principle)"
    )
    print(
        f"  Gliner's printed second form r = p + 1/(2y) + ... at y=2 gives"
        f" {gliner_print(2, 2):.2f}, not {taylor(2, 2):.2f}: a slip for (1/2)y"
    )
    check(
        failed,
        "on-target 4%, a response of 1.5 and Gliner's printed form differs",
        bool(
            taylor(2, 0) == 4
            and taylor(3, 0) - taylor(2, 0) == 1.5
            and abs(gliner_print(2, 2) - taylor(2, 2)) > 0.5
        ),
    )
    return failed


def check_ois() -> list[str]:
    """Part 6: the hike probability implied by an OIS rate."""
    failed: list[str] = []
    section("6. hike probability from an OIS rate")
    base, ois, step = 0.50, 0.625, 0.25
    print(
        f"  Bank Rate {base}%, OIS {ois}%: ({ois}-{base})/{step} = {(ois - base) / step:.0%}"
        " (Gliner, chap. 9, PDF p. 261)"
    )
    # OIS averages the overnight rate over its period: a hike part-way through raises the average by
    # less
    frac_after = 0.6
    prob = (ois - base) / (step * frac_after)
    print(
        f"  if the meeting falls with only {frac_after:.0%} of the OIS period left, the same rate"
        f" implies {prob:.0%} (and >100% is a second hike)"
    )
    check(
        failed,
        "OIS-implied hike probability 50%, above one half at 60% of the period",
        bool(abs((ois - base) / step - 0.5) < 1e-12 and prob > 0.5),
    )
    return failed


def check_contracts() -> list[str]:
    """Part 7: Eurodollar and Treasury futures tick values."""
    failed: list[str] = []
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
    check(
        failed,
        "Eurodollar $25 and the 2y and 5y Treasury ticks",
        bool(
            ed == 25
            and ticks["TU (2y, $200k, 1/4 of 1/32)"] == 15.625
            and ticks["FV (5y, $100k, 1/4 of 1/32)"] == 7.8125
        ),
    )
    return failed


def check_futures_carry() -> list[str]:
    """Part 8: a Treasury future below spot when carry is positive."""
    failed: list[str] = []
    section("8. Treasury futures below the bond with positive carry")
    P, cpn, repo, tau = 100.0, 4.0, 1.0, 0.25
    # ignoring accrued interest, the conversion factor and delivery options
    F = P * (1 + repo / 100 * tau) - cpn * tau
    print(
        f"  bond 100, coupon 4%, repo 1%, 3 months: forward = 100 x (1 + 0.01/4) - 4/4 = {F:.3f} <"
        " 100: carry, not a term premium"
    )
    check(failed, "forward below spot", bool(F < P))
    return failed


def check_steepener() -> list[str]:
    """Part 9: the carry of a DV01-neutral steepener at three rate and repo settings."""
    failed: list[str] = []
    section("9. carry of a DV01-neutral steepener (long 2y, short 10y)")
    for y2, y10, r in [(1.5, 3.0, 1.0), (4.5, 4.0, 5.0), (2.0, 2.5, 2.4)]:
        c = carry_per_dv01(y2, 1.9, r) - carry_per_dv01(y10, 8.5, r)
        print(
            f"  2y {y2}%, 10y {y10}%, repo {r}%: carry per unit DV01 {c:+.3f} ("
            f"{'positive' if c > 0 else 'negative'})"
        )
    check(
        failed,
        "steepener carry positive at 2y 1.5%, 10y 3.0%, repo 1%",
        bool(carry_per_dv01(1.5, 1.9, 1.0) - carry_per_dv01(3.0, 8.5, 1.0) > 0),
    )
    check(
        failed,
        "steepener carry negative at repo 2.4%",
        bool(carry_per_dv01(2.0, 1.9, 2.4) - carry_per_dv01(2.5, 8.5, 2.4) < 0),
    )
    return failed


def check_duration() -> list[str]:
    """Part 10: duration and convexity against a full repricing of a 10-year bond."""
    failed: list[str] = []
    section("10. duration, DV01, convexity")
    c, n, y = 4.0, 10, 0.04
    times = np.arange(1, n + 1)
    cf = np.full(n, c)
    cf[-1] += 100

    def price(yy: float) -> float:
        """Return the bond price at yield yy."""
        value: float = np.sum(cf / (1 + yy) ** times)
        return value

    P0 = price(y)
    h = 1e-4
    Dmod = -(price(y + h) - price(y - h)) / (2 * h) / P0
    C = (price(y + h) - 2 * P0 + price(y - h)) / h**2 / P0
    dv01 = Dmod * P0 / 10_000
    dy = 0.01
    approx_pct = -Dmod * dy + 0.5 * C * dy**2
    exact_pct = price(y + dy) / P0 - 1
    print(
        f"  10y 4% annual bond at par: modified duration {Dmod:.3f}, convexity {C:.1f}, DV01 per"
        f" 100"
        f" = {dv01:.4f}"
    )
    print(
        f"  +100 bp: exact {exact_pct:+.4%}, -D dy + C dy^2/2 = {approx_pct:+.4%} (a percentage of"
        " price, so the price factor matters)"
    )
    check(
        failed,
        "duration and convexity approximation within 5 bp",
        bool(abs(approx_pct - exact_pct) < 5e-4),
    )
    return failed


def check_tips_breakevens() -> list[str]:
    """Part 11: the TIPS index ratio and the breakeven inflation rate."""
    failed: list[str] = []
    section("11. TIPS index ratio, floor, breakevens")
    for infl in [0.05, -0.02]:
        ratio = 1 + infl
        print(
            f"  cumulative CPI change {infl:+.0%}: principal per 100 = {100 * ratio:.0f}; paid at"
            f" maturity {max(100, 100 * ratio):.0f}; coupons on {100 * ratio:.0f} (the floor covers"
            " principal at maturity only)"
        )
    print(
        "  the price is not the index-adjusted principal: price = index ratio x real clean price,"
        " which moves with real yields"
    )
    be = 4.0 - 1.5
    print(
        f"  breakeven 4.0 - 1.5 = {be:.1f}%: expected inflation + inflation risk premium -"
        f" liquidity"
        " premium (not expectations alone)"
    )
    check(failed, "breakeven 4.0 - 1.5 = 2.5", bool(be == 2.5))
    return failed


def check_cds() -> list[str]:
    """Part 12: CDS settlement, the running premium and the recovery sample size."""
    failed: list[str] = []
    section("12. CDS settlement and recovery")
    R = 0.40
    print(
        f"  physical: deliver a bond worth {R:.0%}, receive par: net {1 - R:.0%}; cash: receive par"
        f" minus recovery {1 - R:.0%} (same)"
    )
    print(f"  100 bp running spread paid quarterly: {100 / 4:.0f} bp a quarter")
    mean, sd = 55, 24
    n_needed = ((stats.norm.ppf(0.975) * sd) / (mean - 40)) ** 2
    print(
        f"  Moody's 1983-2006 issuer recoveries mean {mean}%, sd {sd}%: the mean differs from 40%"
        f" at"
        f" 5% if n > {n_needed:.1f} independent issuers; Gliner's 'not enough evidence' depends on"
        f" n,"
        " which he does not give"
    )
    check(failed, "recovery sample size between 9 and 11 issuers", bool(9 < n_needed < 11))
    return failed


def check_variance_swaps() -> list[str]:
    """Part 13: the variance swap payoff and the VIX rule of 16."""
    failed: list[str] = []
    section("13. variance swaps and the VIX")
    units = 1_000_000 / (2 * 24)
    payoff = (29**2 - 24**2) * units
    print(
        f"  vega notional $1m, strike 24: variance units {units:,.0f}; realised 29: payoff"
        f" ${payoff:,.0f} (Gliner, chap. 8, PDF p. 226)"
    )
    print(
        f"  sqrt(252) = {np.sqrt(252):.2f}: VIX 16 (vol points) -> {16 / np.sqrt(252):.2f}% a day;"
        f" VIX 24 -> {24 / np.sqrt(252):.2f}%"
    )
    check(
        failed,
        "variance swap payoff and the VIX rule of 16",
        bool(abs(payoff - 5_520_833.33) < 1 and abs(16 / np.sqrt(252) - 1.008) < 1e-3),
    )
    # the strike is fixed at inception; realised below the strike loses for the long
    print(
        f"  realised 20 against strike 24: payoff ${(20**2 - 24**2) * units:,.0f} (the long pays"
        f" when"
        " realised < strike)"
    )
    return failed


def check_commodities() -> list[str]:
    """Part 14: commodity contract notionals, the 3:2:1 crack spread and platinum's density."""
    failed: list[str] = []
    section("14. commodity contracts, crack spread, platinum")
    print(
        f"  corn 5,000 bu x 500 cents = ${5000 * 5:,.0f}; copper HG 25,000 lb x 350 cents ="
        f" ${25000 * 3.5:,.0f}; gold 100 oz x $1,500 = ${100 * 1500:,.0f}"
    )
    crude, gas, ho = 80.0, 2.40, 2.70  # $/bbl, $/gal, $/gal
    crack = (2 * gas * 42 + 1 * ho * 42 - 3 * crude) / 3
    print(
        f"  3:2:1 with crude $80, gasoline $2.40/gal, heating oil $2.70/gal: ({2 * gas * 42:.1f} +"
        f" {ho * 42:.1f} - {3 * crude:.0f})/3 = ${crack:.2f} per barrel"
    )
    print(
        f"  platinum 21.45 g/cm3 against gold 19.32: ratio {21.45 / 19.32:.2f}, not 'almost twice"
        f" as"
        " heavy'"
    )
    check(
        failed,
        "3:2:1 crack spread and platinum density ratio below 1.2",
        bool(abs(crack - (2 * 2.4 * 42 + 2.7 * 42 - 240) / 3) < 1e-12 and 21.45 / 19.32 < 1.2),
    )
    return failed


def check_demographics() -> list[str]:
    """Part 15: which column of the demographic table each quoted peak year comes from."""
    failed: list[str] = []
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
    check(
        failed,
        "Netherlands working, Germany prime, United Kingdom working",
        bool(
            cols["Netherlands"] == "working"
            and cols["Germany"] == "prime"
            and cols["United Kingdom"] == "working"
        ),
    )
    return failed


def check_stocks_to_use() -> list[str]:
    """Part 16: the ending stocks of a country balance with trade."""
    failed: list[str] = []
    section("16. ending stocks with trade")
    beg, prod, imp, use, exp_ = 10.0, 100.0, 5.0, 95.0, 12.0
    end = beg + prod + imp - use - exp_
    print(
        f"  country balance: {beg} + {prod} + {imp} - {use} - {exp_} = {end}; stocks-to-use"
        f" {end / (use + exp_):.1%} (the identity without trade gives {beg + prod - use})"
    )
    check(failed, "ending stocks 8", bool(end == 8.0))
    return failed


def check_carry_to_risk() -> list[str]:
    """Part 17: carry-to-risk ratios, which can rank two high-yielders differently from carry."""
    failed: list[str] = []
    section("17. carry-to-risk")
    for pair, carry, vol in [("high-yielder A", 5.0, 12.0), ("high-yielder B", 3.0, 6.0)]:
        print(f"  {pair}: carry {carry}% / vol {vol}% = {carry / vol:.2f}")
    print(
        "  ranking by carry and by carry-to-risk can differ (B ranks first by ratio); both ignore"
        " skewness and crash risk"
    )
    check(failed, "B ranks above A on carry-to-risk", bool(3 / 6 > 5 / 12))
    return failed


def main() -> int:
    """Run the seventeen parts, print each failed check as BAD, and return the exit status.

    Returns:
        The exit status, 0 or 1.
    """
    rng = np.random.default_rng(SEED)
    failed = [
        *check_turtle(rng),
        *check_risk_reward(),
        *check_correlation(rng),
        *check_event_hits(),
        *check_taylor(),
        *check_ois(),
        *check_contracts(),
        *check_futures_carry(),
        *check_steepener(),
        *check_duration(),
        *check_tips_breakevens(),
        *check_cds(),
        *check_variance_swaps(),
        *check_commodities(),
        *check_demographics(),
        *check_stocks_to_use(),
        *check_carry_to_risk(),
    ]
    for name in failed:
        print("BAD", name)
    if failed:
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
