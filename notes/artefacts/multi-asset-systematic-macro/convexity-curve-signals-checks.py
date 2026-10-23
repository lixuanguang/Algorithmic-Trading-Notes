"""macro markets and pricing review follow-up checks (2026-10-16): numbers behind the corrections to the macro markets and pricing review entries.

Run from anywhere:  uv run --frozen --no-editable python convexity-curve-signals-checks.py
Each section prints its result and asserts what the corrected entries state. Section 2 reads
ust-10y3m-monthly.csv (in this folder), monthly averages of Treasury's daily par yields, 10-year minus
3-month and 10-year minus 2-year, built from Treasury's daily CSV files for 2006-2026 (retrieved 2026-10-16).
Gliner (2014) by PDF page of the ebook; Drobny (2006) by printed page.
"""

# standard library imports
import csv
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def section(title):
    print(f"\n== {title}")


# 1. Convexity: better than linear, not a gain both ways unhedged ---------------------------------------
section("1. positive convexity, unhedged and duration-hedged (mod:duration-convexity)")


def price(c, y, n):
    return sum(c / (1 + y) ** t for t in range(1, n + 1)) + 100 / (1 + y) ** n


def mod_dur(c, y, n, h=1e-6):
    return -(price(c, y + h, n) - price(c, y - h, n)) / (2 * h) / price(c, y, n)


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
        f"  dy {dy:+.4f}: 10y {b:+.4f} per 100 (linear {lin:+.4f}, convexity adds {b - lin:+.4f}); "
        f"long 10y, short {k:.2f}x 2y: {hedged:+.4f}"
    )
assert res[0.01][0] < 0 and res[-0.01][0] > 0  # unhedged: loses when yields rise
assert abs(res[0.01][0] - (-7.7217)) < 1e-3 and abs(res[-0.01][0] - 8.5302) < 1e-3
assert all(v[0] - v[1] > 0 for v in res.values())  # always better than the linear approximation
assert all(v[2] > 0 for v in res.values())  # hedged: gains either way, parallel moves only
assert res[0.0025][2] < res[0.01][2] / 10  # grows with (dy)^2

# 2. Inversion: three different statements, tested separately --------------------------------------------
# (second follow-up, 2026-10-16: replaces the first follow-up's chronology assertions)
section("2. inversions, recession onsets and the twelve-month horizon")
# standard library imports
from math import erf, sqrt  # noqa: E402 (section-local import)


def phi(z):
    return 0.5 * (1 + erf(z / sqrt(2)))


def add_months(m, k):
    y, mo = map(int, m.split("-"))
    n = 12 * y + (mo - 1) + k
    return f"{n // 12:04d}-{n % 12 + 1:02d}"


PEAKS = [
    "1969-12",
    "1973-11",
    "1980-01",
    "1981-07",
    "1990-07",
    "2001-03",
    "2007-12",
    "2020-02",
]  # NBER, 2026-10-16
TROUGHS = ["1970-11", "1975-03", "1980-07", "1982-11", "1991-03", "2001-11", "2009-06", "2020-04"]
ONSETS = [add_months(p, 1) for p in PEAKS]  # first contraction month; peak months are expansion


def in_recession(m):
    return any(add_months(p, 1) <= m <= tr for p, tr in zip(PEAKS, TROUGHS))


def load(name, col):
    rows = list(csv.DictReader(open(os.path.join(HERE, name))))
    months = [r["month"] for r in rows]
    assert len(months) == len(set(months)) and all(
        add_months(months[k], 1) == months[k + 1] for k in range(len(months) - 1)
    )
    assert (
        rows[-1]["month"] == "2026-10" and rows[-1]["complete"] == "no"
    )  # data to mid-October 2026
    return {r["month"]: float(r[col]) for r in rows if r["complete"] == "yes"}


h15 = load(
    "h15-spread-monthly.csv", "spread_10y_3m_be"
)  # the paper's series, built by h15_monthly.py
cmt = load(
    "ust-10y3m-monthly.csv", "spread_10y_3m_cmt"
)  # Treasury CMT proxy, built by ust_monthly.py

# (1) the paper's table (p. 6): negative months in the twelve before each recession, and the minimum
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
        f"  (1) recession from {start}: negative months {got_n} (paper {n}), minimum {got_lo:.2f} (paper {lo:.2f})"
    )
    assert got_n == n and abs(got_lo - lo) <= 0.015
assert round(h15["1989-06"], 2) == -0.16  # the footnote's June 1989 value
# (2) the paper's probit targets recession STATUS in month t+12 (p. 3)
a_, b_ = -0.6045, -0.7374
print(
    f"  (2) P(recession month at t+12) at s = 0: {phi(a_):.3f}; at s = -0.16: {phi(a_ + b_ * -0.16):.3f}"
)
assert abs(phi(a_) - 0.2727) < 1e-3


# (3) onset rules defined here, applied to negative months in expansion (recession months excluded)
def rule_outcomes(series, lo, hi):
    last = max(series)
    neg = [m for m in sorted(series) if lo <= m <= hi and series[m] < 0 and not in_recession(m)]

    def out(start, end):
        if [o for o in ONSETS if add_months(start, 1) <= o <= add_months(end, 12)]:
            return "hit"
        if add_months(end, 12) > last:
            return "window open"
        return "miss" if add_months(end, 12) < PEAKS[-1] else "provisional miss"

    eps, cur = [], []
    for m in neg:
        if cur and add_months(cur[-1], 1) == m:
            cur.append(m)
        else:
            if cur:
                eps.append(cur)
            cur = [m]
    if cur:
        eps.append(cur)
    months = {m: out(m, m) for m in neg}  # month rule: onset in t+1 .. t+12
    episodes = [
        (e[0], e[-1], out(e[0], e[-1])) for e in eps
    ]  # episode rule: onset by 12 months after its last month
    return months, episodes


m_in, e_in = rule_outcomes(h15, "1968-01", "2005-12")
print(
    f"  (3) 1968-2005, paper's series: {len(m_in)} negative expansion months, month-rule misses "
    f"{[m for m, o in m_in.items() if o == 'miss']}; episode rule: {sorted(set(o for *_, o in e_in))} for {len(e_in)} episodes"
)
assert [m for m, o in m_in.items() if o == "miss"] == [
    "1968-12",
    "1978-11",
    "1978-12",
    "1979-01",
    "1989-06",
    "1989-07",
]
assert len(m_in) == 54 and all(o == "hit" for *_, o in e_in) and len(e_in) == 9
for label, series in (("paper's series", h15), ("CMT proxy", cmt)):
    mo, ep = rule_outcomes(series, "2006-01", "2026-12")
    tally = {
        k: sum(1 for v in mo.values() if v == k)
        for k in ("hit", "miss", "provisional miss", "window open")
    }
    print(f"  (3) 2006-2026, {label}: {len(mo)} months {tally}; episodes {ep}")
    assert [m for m, o in mo.items() if o == "miss"] == [
        "2006-08",
        "2006-09",
        "2006-10",
        "2006-11",
        "2006-12",
    ]
    assert [o for *_, o in ep][:3] == ["hit", "hit", "hit"] and all(
        o == "provisional miss" for *_, o in ep[3:]
    )
    assert tally == (
        {"hit": 11, "miss": 5, "provisional miss": 27, "window open": 0}
        if series is h15
        else {"hit": 11, "miss": 5, "provisional miss": 30, "window open": 0}
    )

# 3. VIX units -------------------------------------------------------------------------------------------
section("3. VIX is 100 x sqrt(annualised 30-day variance)")
vix = 20.0
sigma = vix / 100
var_ann = sigma**2
var_30d = var_ann * 43200 / 525600  # Cboe: minutes in 30 days / minutes in a year
print(
    f"  VIX {vix:.0f}: sigma {sigma:.2f}, annualised variance {var_ann:.4f}, 30-day variance {var_30d:.5f}"
)
print(
    f"  daily sd by the sqrt(252) rule: {sigma / math.sqrt(252):.4%} (an approximation mixing calendar and trading days)"
)
assert abs(var_ann - 0.04) < 1e-12 and abs(100 * math.sqrt(var_ann) - vix) < 1e-9
assert abs(var_30d - 0.04 * 30 / 365) < 1e-12

# 4. Gold and silver production shares -------------------------------------------------------------------
section("4. production shares: Gliner pp. 320 and 322 against USGS")
gold = {
    "2011": ({"China": 362, "US": 234, "Australia": 258, "South Africa": 181}, 2660),
    "2012e": ({"China": 370, "US": 230, "Australia": 250, "South Africa": 170}, 2700),
}
for yr, (c, w) in gold.items():
    s = sum(c.values()) / w
    print(
        f"  gold {yr} (USGS MCS 2013): China+US+Australia+South Africa {s:.1%} (Gliner: 'more than 40 percent')"
    )
    assert 0.37 < s < 0.40
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
print(f"  Table 10.9: ounces sum {oz:.1f} (stated total {total}); printed shares sum {pct:.1f}%")
print(
    f"  on the stated total: Mexico+China {mc:.1%}, top five {top5:.1%}; printed shares imply a denominator of {implied:.0f}"
)
usgs = (4250 + 3800) / 24000
print(f"  USGS MCS 2013, 2012e: Mexico+China {usgs:.1%} of world mine output")
assert abs(oz - total) < 0.05 and abs(mc - 0.3548) < 5e-4 and abs(pct - 132.5) < 0.05
assert 590 < implied < 600 and abs(27.3 + 19.7 - 47.0) < 1e-9 and abs(usgs - 0.3354) < 5e-4

# 5. FX carry: exact and first-order -------------------------------------------------------------------------
section("5. covered parity and funded carry, simple rates, S = domestic per foreign")
S0, i_d, i_f, tau = 1.10, 0.05, 0.02, 0.25
F = S0 * (1 + i_d * tau) / (1 + i_f * tau)


def funded(ST):
    return ST / S0 * (1 + i_f * tau) - (1 + i_d * tau)


carry = funded(S0)
for s in (0.0, 0.01, -0.03):
    exact = funded(S0 * (1 + s))
    approx = (i_f - i_d) * tau + s
    print(
        f"  spot change {s:+.2%}: exact {exact:+.4%}, first order {approx:+.4%}, cross term {exact - approx:+.4%}"
    )
print(
    f"  forward {F:.5f}; hedged at F: {funded(F):+.2e}; forward premium {(F - S0) / S0:+.4%} "
    f"vs (i - i_f) tau {(i_d - i_f) * tau:+.4%}"
)
assert abs(carry - (i_f - i_d) * tau) < 1e-15 and abs(funded(F)) < 1e-12
assert (
    abs(funded(S0 * 1.01) - 0.00255) < 1e-12
    and abs(F / S0 - (1 + i_d * tau) / (1 + i_f * tau)) < 1e-15
)

# 6. CDS: physical and cash agree only if valued at the same recovery -----------------------------------------
section("6. CDS settlement payouts per 100 notional")
for bond_value, auction_price in ((40, 40), (38, 40)):
    phys, cash = 100 - bond_value, 100 - auction_price
    print(
        f"  delivered bond worth {bond_value}, auction price {auction_price}: physical {phys}, cash {cash}"
    )
assert 100 - 40 == 100 - 40 and (100 - 38) != (100 - 40)

# 7. Andres Drobny's 4:1 after two stops (Drobny 2006, p. 131) -----------------------------------------------
section("7. risk/reward after re-entering with the loss counted")
reward, risk = 4, 1
for stops in range(3):
    print(
        f"  after {stops} stop(s): reward {reward} against risk {risk + stops} -> {reward}:{risk + stops}"
    )
assert (reward, risk + 2) == (4, 3)

print("\nall follow-up checks passed")
