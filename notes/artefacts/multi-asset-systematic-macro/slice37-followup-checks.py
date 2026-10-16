"""Slice-37 follow-up checks (2026-10-16): numbers behind the corrections to the slice-37 entries.

Run from anywhere:  /opt/homebrew/bin/python3.10 slice37-followup-checks.py
Each section prints its result and asserts what the corrected entries state. Section 2 reads
ust-10y3m-monthly.csv (in this folder), monthly averages of Treasury's daily par yields, 10-year minus
3-month and 10-year minus 2-year, built from Treasury's daily CSV files for 2006-2026 (retrieved 2026-10-16).
Gliner (2014) by PDF page of the ebook; Drobny (2006) by printed page.
"""
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


P10, P2 = price(4, .04, 10), price(4, .04, 2)
D10, D2 = mod_dur(4, .04, 10), mod_dur(4, .04, 2)
k = D10 * P10 / (D2 * P2)                       # 2-year face per unit of 10-year face, DV01-matched
res = {}
for dy in (0.01, -0.01, 0.0025):
    b = price(4, .04 + dy, 10) - P10
    lin = -D10 * P10 * dy
    hedged = b - k * (price(4, .04 + dy, 2) - P2)
    res[dy] = (b, lin, hedged)
    print(f"  dy {dy:+.4f}: 10y {b:+.4f} per 100 (linear {lin:+.4f}, convexity adds {b - lin:+.4f}); "
          f"long 10y, short {k:.2f}x 2y: {hedged:+.4f}")
assert res[0.01][0] < 0 and res[-0.01][0] > 0             # unhedged: loses when yields rise
assert abs(res[0.01][0] - (-7.7217)) < 1e-3 and abs(res[-0.01][0] - 8.5302) < 1e-3
assert all(v[0] - v[1] > 0 for v in res.values())          # always better than the linear approximation
assert all(v[2] > 0 for v in res.values())                 # hedged: gains either way, parallel moves only
assert res[0.0025][2] < res[0.01][2] / 10                  # grows with (dy)^2

# 2. Inversion after Estrella-Trubin's sample ------------------------------------------------------------
section("2. 10-year minus 3-month monthly averages since 2006 against NBER peaks")
rows = list(csv.DictReader(open(os.path.join(HERE, "ust-10y3m-monthly.csv"))))
neg = [r["month"] for r in rows if float(r["spread_10y_3m_cmt"]) < 0]
runs, start, prev = [], None, None
for m in neg:
    y, mo = map(int, m.split("-"))
    idx = 12 * y + mo
    if prev is None or idx != prev + 1:
        if start:
            runs.append((start, last))
        start = m
    prev, last = idx, m
runs.append((start, last))
print("  negative months (runs):", runs)
peaks = ["2007-12", "2020-02"]                             # NBER peaks after 2005, as of 2026-10-16


def months_between(a, b):
    ya, ma = map(int, a.split("-")); yb, mb = map(int, b.split("-"))
    return 12 * (yb - ya) + (mb - ma)


for a, b in runs:
    nxt = [p for p in peaks if months_between(b, p) >= 0]
    lead = months_between(a, nxt[0]) if nxt else None
    print(f"  run {a} to {b}: next NBER peak {nxt[0] if nxt else 'none dated'}"
          + (f", {lead} months after the first negative month" if lead is not None else ""))
assert ("2022-11", "2024-11") in runs                      # the long 2022-24 run
assert min(float(r["spread_10y_3m_cmt"]) for r in rows) < -1.7  # deepest about -1.73 (May 2023)
assert not [p for p in peaks if p > "2022-11"]              # no peak dated after it as of retrieval

# 3. VIX units -------------------------------------------------------------------------------------------
section("3. VIX is 100 x sqrt(annualised 30-day variance)")
vix = 20.0
sigma = vix / 100
var_ann = sigma ** 2
var_30d = var_ann * 43200 / 525600                         # Cboe: minutes in 30 days / minutes in a year
print(f"  VIX {vix:.0f}: sigma {sigma:.2f}, annualised variance {var_ann:.4f}, 30-day variance {var_30d:.5f}")
print(f"  daily sd by the sqrt(252) rule: {sigma / math.sqrt(252):.4%} (an approximation mixing calendar and trading days)")
assert abs(var_ann - 0.04) < 1e-12 and abs(100 * math.sqrt(var_ann) - vix) < 1e-9
assert abs(var_30d - 0.04 * 30 / 365) < 1e-12

# 4. Gold and silver production shares -------------------------------------------------------------------
section("4. production shares: Gliner pp. 320 and 322 against USGS")
gold = {"2011": ({"China": 362, "US": 234, "Australia": 258, "South Africa": 181}, 2660),
        "2012e": ({"China": 370, "US": 230, "Australia": 250, "South Africa": 170}, 2700)}
for yr, (c, w) in gold.items():
    s = sum(c.values()) / w
    print(f"  gold {yr} (USGS MCS 2013): China+US+Australia+South Africa {s:.1%} (Gliner: 'more than 40 percent')")
    assert 0.37 < s < 0.40
t109 = {"Mexico": (162.2, 27.3), "China": (117.0, 19.7), "Peru": (111.3, 18.7), "Australia": (56.9, 9.6),
        "Russia": (45.0, 7.6), "Poland": (41.2, 6.9), "Bolivia": (39.7, 6.7), "Chile": (37.0, 6.2),
        "United States": (32.6, 5.5), "Argentina": (24.1, 4.1), "Other": (120.0, 20.2)}
total = 787.0
oz = sum(v[0] for v in t109.values())
pct = sum(v[1] for v in t109.values())
mc = (t109["Mexico"][0] + t109["China"][0]) / total
top5 = sum(t109[k][0] for k in ["Mexico", "China", "Peru", "Australia", "Russia"]) / total
implied = t109["Mexico"][0] / (t109["Mexico"][1] / 100)
print(f"  Table 10.9: ounces sum {oz:.1f} (stated total {total}); printed shares sum {pct:.1f}%")
print(f"  on the stated total: Mexico+China {mc:.1%}, top five {top5:.1%}; printed shares imply a denominator of {implied:.0f}")
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
    print(f"  spot change {s:+.2%}: exact {exact:+.4%}, first order {approx:+.4%}, cross term {exact - approx:+.4%}")
print(f"  forward {F:.5f}; hedged at F: {funded(F):+.2e}; forward premium {(F - S0) / S0:+.4%} "
      f"vs (i - i_f) tau {(i_d - i_f) * tau:+.4%}")
assert abs(carry - (i_f - i_d) * tau) < 1e-15 and abs(funded(F)) < 1e-12
assert abs(funded(S0 * 1.01) - 0.00255) < 1e-12 and abs(F / S0 - (1 + i_d * tau) / (1 + i_f * tau)) < 1e-15

# 6. CDS: physical and cash agree only if valued at the same recovery -----------------------------------------
section("6. CDS settlement payouts per 100 notional")
for bond_value, auction_price in ((40, 40), (38, 40)):
    phys, cash = 100 - bond_value, 100 - auction_price
    print(f"  delivered bond worth {bond_value}, auction price {auction_price}: physical {phys}, cash {cash}")
assert 100 - 40 == 100 - 40 and (100 - 38) != (100 - 40)

# 7. Andres Drobny's 4:1 after two stops (Drobny 2006, p. 131) -----------------------------------------------
section("7. risk/reward after re-entering with the loss counted")
reward, risk = 4, 1
for stops in range(3):
    print(f"  after {stops} stop(s): reward {reward} against risk {risk + stops} -> {reward}:{risk + stops}")
assert (reward, risk + 2) == (4, 3)

print("\nall follow-up checks passed")
