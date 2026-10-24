"""Convexity, curve inversions before recessions, VIX units, metal shares, carry, CDS, stops."""

import math
import sys
from collections.abc import Sequence
from math import erf, sqrt
from pathlib import Path
from typing import Final

from trading_notes.numerical.business_cycles_policy.recession_signals import (
    RecessionCalendar,
    add_months,
    read_monthly,
)
from trading_notes.numerical.report import require, section
from trading_notes.numerical.repository import repository_root

# The monthly spread series, below the repository root.
DATA: Final = Path("notes/artefacts/multi-asset-systematic-macro")
# NBER peaks and troughs as of 2026-10-16; peak months belong to the expansion.
NBER: Final = RecessionCalendar(
    peaks=("1969-12", "1973-11", "1980-01", "1981-07", "1990-07", "2001-03", "2007-12", "2020-02"),
    troughs=(
        "1970-11",
        "1975-03",
        "1980-07",
        "1982-11",
        "1991-03",
        "2001-11",
        "2009-06",
        "2020-04",
    ),
)


def price(c: float, y: float, n: int) -> float:
    """Return the price of an n-year annual bond paying c per 100 at a flat yield y."""
    return sum(c / (1 + y) ** t for t in range(1, n + 1)) + 100 / (1 + y) ** n


def mod_dur(c: float, y: float, n: int, h: float = 1e-6) -> float:
    """Return the modified duration by a central difference of step h."""
    return -(price(c, y + h, n) - price(c, y - h, n)) / (2 * h) / price(c, y, n)


def phi(z: float) -> float:
    """Return the standard normal distribution function."""
    return 0.5 * (1 + erf(z / sqrt(2)))


def check_convexity() -> list[str]:
    """1. Convexity: better than linear, and a gain both ways only when duration-hedged."""
    failed: list[str] = []
    section("1. positive convexity, unhedged and duration-hedged (mod:duration-convexity)")
    P10, P2 = price(4, 0.04, 10), price(4, 0.04, 2)
    D10, D2 = mod_dur(4, 0.04, 10), mod_dur(4, 0.04, 2)
    k = D10 * P10 / (D2 * P2)  # 2-year face per unit of 10-year face, DV01-matched
    res = {}
    for dy in (0.01, -0.01, 0.0025):
        b = price(4, 0.04 + dy, 10) - P10
        lin = -D10 * P10 * dy
        hedged = b - k * (price(4, 0.04 + dy, 2) - P2)
        res[dy] = (b, lin, hedged)
        print(
            f"  dy {dy:+.4f}: 10y {b:+.4f} per 100 (linear {lin:+.4f}, convexity adds"
            f" {b - lin:+.4f}); long 10y, short {k:.2f}x 2y: {hedged:+.4f}"
        )
    require(failed, "unhedged loses when yields rise", res[0.01][0] < 0 and res[-0.01][0] > 0)
    require(
        failed,
        "unhedged changes -7.7217 and 8.5302",
        abs(res[0.01][0] - (-7.7217)) < 1e-3 and abs(res[-0.01][0] - 8.5302) < 1e-3,
    )
    require(failed, "always better than linear", all(v[0] - v[1] > 0 for v in res.values()))
    require(failed, "hedged gains either way", all(v[2] > 0 for v in res.values()))
    require(failed, "hedged gain grows with dy^2", res[0.0025][2] < res[0.01][2] / 10)
    return failed


def check_inversions(h15: dict[str, float], cmt: dict[str, float]) -> list[str]:
    """2. Inversions: the paper's table, its probit target and onset rules, tested separately."""
    failed: list[str] = []
    section("2. inversions, recession onsets and the twelve-month horizon")
    # (1) the paper's table (p. 6): negative months in the twelve before each recession, and
    # the minimum
    paper = {
        "1970-01": (10, -0.51),
        "1973-12": (6, -1.59),
        "1980-02": (12, -2.20),
        "1981-08": (10, -3.51),
        "1990-08": (3, -0.08),
        "2001-04": (7, -0.70),
    }
    for start, (n, lo) in paper.items():
        w = [add_months(start, -k) for k in range(1, 13)]
        got_n, got_lo = sum(h15[m] < 0 for m in w), min(h15[m] for m in w)
        print(
            f"  (1) recession from {start}: negative months {got_n} (paper {n}), minimum"
            f" {got_lo:.2f} (paper {lo:.2f})"
        )
        require(failed, f"paper's table for {start}", got_n == n and abs(got_lo - lo) <= 0.015)
    require(failed, "the footnote's June 1989 value", round(h15["1989-06"], 2) == -0.16)
    # (2) the paper's probit targets recession STATUS in month t+12 (p. 3)
    a_, b_ = -0.6045, -0.7374
    print(
        f"  (2) P(recession month at t+12) at s = 0: {phi(a_):.3f}; at s = -0.16:"
        f" {phi(a_ + b_ * -0.16):.3f}"
    )
    require(failed, "probit at s = 0", abs(phi(a_) - 0.2727) < 1e-3)
    # (3) onset rules defined here, applied to negative months in expansion
    m_in, e_in = NBER.signal_outcomes(h15, "1968-01", "2005-12")
    print(
        f"  (3) 1968-2005, paper's series: {len(m_in)} negative expansion months, month-rule"
        f" misses {[m for m, o in m_in.items() if o == 'miss']}; episode rule:"
        f" {sorted(set(o for *_, o in e_in))} for {len(e_in)} episodes"
    )
    require(
        failed,
        "1968-2005 month-rule misses",
        [m for m, o in m_in.items() if o == "miss"]
        == ["1968-12", "1978-11", "1978-12", "1979-01", "1989-06", "1989-07"],
    )
    require(
        failed,
        "1968-2005 counts and episode hits",
        len(m_in) == 54 and all(o == "hit" for *_, o in e_in) and len(e_in) == 9,
    )
    for label, series, want in (
        ("paper's series", h15, {"hit": 11, "miss": 5, "provisional miss": 27, "window open": 0}),
        ("CMT proxy", cmt, {"hit": 11, "miss": 5, "provisional miss": 30, "window open": 0}),
    ):
        mo, ep = NBER.signal_outcomes(series, "2006-01", "2026-12")
        tally = {
            k: sum(1 for v in mo.values() if v == k)
            for k in ("hit", "miss", "provisional miss", "window open")
        }
        print(f"  (3) 2006-2026, {label}: {len(mo)} months {tally}; episodes {ep}")
        require(
            failed,
            f"2006-2026 month-rule misses, {label}",
            [m for m, o in mo.items() if o == "miss"]
            == ["2006-08", "2006-09", "2006-10", "2006-11", "2006-12"],
        )
        require(
            failed,
            f"2006-2026 episodes, {label}",
            [o for *_, o in ep][:3] == ["hit", "hit", "hit"]
            and all(o == "provisional miss" for *_, o in ep[3:]),
        )
        require(failed, f"2006-2026 tally, {label}", tally == want)
    return failed


def check_vix() -> list[str]:
    """3. VIX units: 100 x sqrt(annualised 30-day variance)."""
    failed: list[str] = []
    section("3. VIX is 100 x sqrt(annualised 30-day variance)")
    vix = 20.0
    sigma = vix / 100
    var_ann = sigma**2
    var_30d = var_ann * 43200 / 525600  # Cboe: minutes in 30 days / minutes in a year
    print(
        f"  VIX {vix:.0f}: sigma {sigma:.2f}, annualised variance {var_ann:.4f}, 30-day variance"
        f" {var_30d:.5f}"
    )
    print(
        f"  daily sd by the sqrt(252) rule: {sigma / math.sqrt(252):.4%} (an approximation mixing"
        " calendar and trading days)"
    )
    require(
        failed,
        "VIX 20 is variance 0.04",
        abs(var_ann - 0.04) < 1e-12 and abs(100 * math.sqrt(var_ann) - vix) < 1e-9,
    )
    require(failed, "30-day variance", abs(var_30d - 0.04 * 30 / 365) < 1e-12)
    return failed


def check_production_shares() -> list[str]:
    """4. Gold and silver production shares: Gliner pp. 320 and 322 against USGS."""
    failed: list[str] = []
    section("4. production shares: Gliner pp. 320 and 322 against USGS")
    gold = {
        "2011": ({"China": 362, "US": 234, "Australia": 258, "South Africa": 181}, 2660),
        "2012e": ({"China": 370, "US": 230, "Australia": 250, "South Africa": 170}, 2700),
    }
    for yr, (c, w) in gold.items():
        s = sum(c.values()) / w
        print(
            f"  gold {yr} (USGS MCS 2013): China+US+Australia+South Africa {s:.1%} (Gliner: 'more"
            " than 40 percent')"
        )
        require(failed, f"gold share {yr}", 0.37 < s < 0.40)
    t109 = {
        "Mexico": (162.2, 27.3),
        "China": (117.0, 19.7),
        "Peru": (111.3, 18.7),
        "Australia": (56.9, 9.6),
        "Russia": (45.0, 7.6),
        "Poland": (41.2, 6.9),
        "Bolivia": (39.7, 6.7),
        "Chile": (37.0, 6.2),
        "United States": (32.6, 5.5),
        "Argentina": (24.1, 4.1),
        "Other": (120.0, 20.2),
    }
    total = 787.0
    oz = sum(v[0] for v in t109.values())
    pct = sum(v[1] for v in t109.values())
    mc = (t109["Mexico"][0] + t109["China"][0]) / total
    top5 = sum(t109[k][0] for k in ["Mexico", "China", "Peru", "Australia", "Russia"]) / total
    implied = t109["Mexico"][0] / (t109["Mexico"][1] / 100)
    print(
        f"  Table 10.9: ounces sum {oz:.1f} (stated total {total}); printed shares sum {pct:.1f}%"
    )
    print(
        f"  on the stated total: Mexico+China {mc:.1%}, top five {top5:.1%}; printed shares imply"
        f" a denominator of {implied:.0f}"
    )
    usgs = (4250 + 3800) / 24000
    print(f"  USGS MCS 2013, 2012e: Mexico+China {usgs:.1%} of world mine output")
    require(
        failed,
        "Table 10.9 totals",
        abs(oz - total) < 0.05 and abs(mc - 0.3548) < 5e-4 and abs(pct - 132.5) < 0.05,
    )
    require(
        failed,
        "Table 10.9 implied denominator and USGS share",
        590 < implied < 600 and abs(27.3 + 19.7 - 47.0) < 1e-9 and abs(usgs - 0.3354) < 5e-4,
    )
    return failed


def check_carry() -> list[str]:
    """5. Covered parity and funded carry, exact and first order, with simple rates."""
    failed: list[str] = []
    section("5. covered parity and funded carry, simple rates, S = domestic per foreign")
    S0, i_d, i_f, tau = 1.10, 0.05, 0.02, 0.25
    F = S0 * (1 + i_d * tau) / (1 + i_f * tau)

    def funded(ST: float) -> float:
        return ST / S0 * (1 + i_f * tau) - (1 + i_d * tau)

    carry = funded(S0)
    for s in (0.0, 0.01, -0.03):
        exact = funded(S0 * (1 + s))
        approx = (i_f - i_d) * tau + s
        print(
            f"  spot change {s:+.2%}: exact {exact:+.4%}, first order {approx:+.4%}, cross term"
            f" {exact - approx:+.4%}"
        )
    print(
        f"  forward {F:.5f}; hedged at F: {funded(F):+.2e}; forward premium {(F - S0) / S0:+.4%} "
        f"vs (i - i_f) tau {(i_d - i_f) * tau:+.4%}"
    )
    require(
        failed,
        "carry and hedged forward",
        abs(carry - (i_f - i_d) * tau) < 1e-15 and abs(funded(F)) < 1e-12,
    )
    require(
        failed,
        "carry after a 1% move and the forward ratio",
        abs(funded(S0 * 1.01) - 0.00255) < 1e-12
        and abs(F / S0 - (1 + i_d * tau) / (1 + i_f * tau)) < 1e-15,
    )
    return failed


def check_cds() -> list[str]:
    """6. CDS physical and cash settlement agree only at the same recovery value."""
    failed: list[str] = []
    section("6. CDS settlement payouts per 100 notional")
    payouts = []
    for bond_value, auction_price in ((40, 40), (38, 40)):
        phys, cash = 100 - bond_value, 100 - auction_price
        payouts.append((phys, cash))
        print(
            f"  delivered bond worth {bond_value}, auction price {auction_price}: physical {phys},"
            f" cash {cash}"
        )
    require(
        failed,
        "physical equals cash only at the same value",
        payouts[0][0] == payouts[0][1] and payouts[1][0] != payouts[1][1],
    )
    return failed


def check_stops() -> list[str]:
    """7. Andres Drobny's 4:1 after two stops (Drobny 2006, p. 131)."""
    failed: list[str] = []
    section("7. risk/reward after re-entering with the loss counted")
    reward, risk = 4, 1
    for stops in range(3):
        print(
            f"  after {stops} stop(s): reward {reward} against risk {risk + stops} ->"
            f" {reward}:{risk + stops}"
        )
    require(failed, "4:1 becomes 4:3 after two stops", (reward, risk + 2) == (4, 3))
    return failed


def main(argv: Sequence[str] | None = None) -> int:
    """Run the seven sections, print each failed check as BAD, and return the exit status.

    Each section prints its result and checks what the entries state. Section 2 reads
    h15-spread-monthly.csv, the paper's 10-year minus 3-month spread built by
    trading_notes.research.business_cycles_policy.h15_spread, and ust-10y3m-monthly.csv, monthly
    averages of Treasury's daily par yields (10-year minus 3-month and 10-year minus 2-year)
    built from Treasury's daily CSV files for 2006-2026 (retrieved 2026-10-16) by
    trading_notes.research.business_cycles_policy.treasury_spread. Gliner (2014) by PDF page of
    the ebook; Drobny (2006) by printed page.

    Args:
        argv: Command-line arguments: `--root DIR`, the repository root that holds the data
            (default: the working directory).

    Returns:
        The exit status, 0 or 1.
    """
    root = repository_root(__doc__ or "", argv)
    h15 = read_monthly(root / DATA / "h15-spread-monthly.csv", "spread_10y_3m_be", "2026-10")
    cmt = read_monthly(root / DATA / "ust-10y3m-monthly.csv", "spread_10y_3m_cmt", "2026-10")
    failed = [
        *check_convexity(),
        *check_inversions(h15, cmt),
        *check_vix(),
        *check_production_shares(),
        *check_carry(),
        *check_cds(),
        *check_stops(),
    ]
    for name in failed:
        print("BAD", name)
    if failed:
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
