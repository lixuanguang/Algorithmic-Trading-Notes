"""ev:regime-asset-responses-tested: the regime map's "recession" row, tested on a regime classified with real-time
data. Only this row is tested; the other rows and Gliner's sector phases are not.

Corrected rerun (v2, 17 October 2026). The first run (v1, same day) is kept unchanged in superseded-first-run/. v2 keeps
v1's hypothesis, real-time rule, responses and decision rule, and changes only what an audit found after v1's
results were seen; nothing here is preregistered:
  1. Ex-post window definition stated. v1's NBER window is ANY OVERLAP: a quarter counts if at least one of its
     three response months lies in a recession (peak month excluded, trough included). That remains the reported
     ex-post comparison. ALL MONTHS (all three response months inside a recession) is reported as a sensitivity
     only; neither definition was chosen for its significance.
  2. Dollar definition. TWEXBMTH is the Fed's broad index on goods trade only (published to December 2019);
     DTWEXBGS weights goods and services trade, with new weight formula and composition, from January 2006 (Fed
     FEDS Note of 15 January 2019 and H.10 of 19 February 2019; local copies). v2 tests the dollar on the goods-only
     index alone (1973-2019, consistent definition; the primary dollar result) and, separately, on DTWEXBGS alone
     (2006 onward). v1's splice of the two (by changes, at 2019-12/2020-01) is reported only for continuity, with
     its definition break.
  3. Real-time and ex-post results are printed in separate blocks; only the real-time block is the test. The
     ex-post block uses NBER dates announced months to years later and is a description, not a tradable signal.
  4. Dependence. Quarters do not overlap, but signal quarters cluster in a few episodes and responses are
     heteroskedastic and serially dependent, so Welch t (v1) overstates the information. v2 adds, as a sensitivity
     chosen before computing it, a Newey-West t (4 quarterly lags) from the regression of each response on the
     regime indicator, and prints the number of distinct episodes (runs of consecutive regime quarters).

v1 protocol, as written before v1's results by the batch record's account (committed with them, so not preregistered):
Hypothesis (def:macro-regime-asset-map): in recession, yields fall, credit spreads widen, equities fall,
  the dollar rises and defensive sectors lead. Commodities are not tested (no public, licence-free series used).
Regime, real time. Sahm-type rule on the Philadelphia Fed's Real-Time Data Set unemployment vintages (RUC, quarterly
  vintages of monthly data, 1965Q4-2026Q3): in vintage v, with L the last month reported, signal = 1 if the
  three-month average of the unemployment rate at L minus the minimum of the three-month averages at L-12..L-1 is at
  least 0.50 percentage point. Vintage v is dated in the middle month of its quarter (RTDSM dating).
Responses over the three months after the vintage month m (m+1..m+3), all from public monthly data:
  dy10  = GS10(m+3) - GS10(m)                       (FRED, monthly average 10-year Treasury yield, pp)
  dcred = (BAA - GS10)(m+3) - (BAA - GS10)(m)       (FRED Moody's Baa yield less GS10, pp)
  eq    = sum of Mkt-RF over m+1..m+3               (Ken French, CRSP 202608 file, percent)
  dfn   = sum over m+1..m+3 of mean(NoDur, Utils, Hlth) - (Mkt-RF + RF)   (French 12 industries, value weighted)
  usd   = 100 * ln change of the broad dollar index, m to m+3 (TWEXBMTH to 2019-12, then monthly averages of
          DTWEXBGS; chained by changes). [v2: see correction 2 above.]
  Vintages with a missing month inside the 15-month window are skipped and listed (found on the first run: the
  October 2025 rate is #N/A in the 2026 vintages).
Test. Mean response in signal quarters minus non-signal quarters, Welch t (quarters are non-overlapping windows).
  For contrast, the same with an ex-post classification: window months inside NBER recessions (peak month excluded,
  trough included), which uses information not available in real time.
Sufficient test. A sign is supported if the real-time difference has the hypothesised sign (dy10 < 0, dcred > 0,
  eq < 0, dfn > 0, usd > 0) with |t| > 2.
Run (v2, under 2 s): uv run --frozen --no-editable --group empirical python regime_recession_test.py <empirical folder>   (expects rucqvmd.xlsx,
  fred/*.csv, french/*.csv). Writes regime_quarters.csv (derived panel).
"""

import csv
import math
import os
import sys

import numpy as np
import openpyxl

SRC = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))


def add(ym, k):
    n = ym[0] * 12 + ym[1] - 1 + k
    return (n // 12, n % 12 + 1)


def fred(i):
    out = {}
    with open(os.path.join(SRC, "fred", i + ".csv")) as f:
        r = csv.reader(f)
        next(r)
        for d, v in r:
            if v not in ("", "."):
                y, m, _ = map(int, d.split("-"))
                out.setdefault((y, m), []).append(float(v))
    return {k: sum(v) / len(v) for k, v in out.items()}


def french(fn, cols, section_header=None):
    out, on = {}, section_header is None
    with open(os.path.join(SRC, "french", fn)) as f:
        for line in f:
            if section_header and section_header in line:
                on = True
                continue
            if not on:
                continue
            parts = [p.strip() for p in line.split(",")]
            if parts[0] == "" and len(parts) > 1 and parts[1]:
                header = parts
                continue
            if len(parts[0]) == 6 and parts[0].isdigit():
                out[(int(parts[0][:4]), int(parts[0][4:]))] = {
                    h: float(x) for h, x in zip(header[1:], parts[1:]) if h in cols
                }
            elif out and (parts[0] == "" or not parts[0].isdigit()):
                break
    return out


wb = openpyxl.load_workbook(os.path.join(SRC, "rucqvmd.xlsx"), read_only=True)
rows = list(wb["ruc"].iter_rows(values_only=True))
head = rows[0]
months = [tuple(map(int, r[0].split(":"))) for r in rows[1:]]
signals, skipped = {}, []
for j, name in enumerate(head[1:], start=1):
    yy, q = int(name[3:5]), int(name[6])
    year = 1900 + yy if yy >= 60 else 2000 + yy
    vm = (year, 3 * q - 1)
    u = {m: r[j] for m, r in zip(months, rows[1:]) if isinstance(r[j], (int, float))}
    L = max(u)
    a3 = lambda m: sum(u[add(m, -k)] for k in range(3)) / 3
    try:
        cur = a3(L)
        prev = min(a3(add(L, -k)) for k in range(1, 13))
    except KeyError:
        skipped.append(name)  # a month inside the 15-month window is missing (#N/A) in this vintage
        continue
    signals[vm] = (cur - prev, L)

gs10, baa = fred("GS10"), fred("BAA")
tw_old, tw_new = fred("TWEXBMTH"), fred("DTWEXBGS")
ff = french("F-F_Research_Data_Factors.csv", {"Mkt-RF", "RF"})
ind = french(
    "12_Industry_Portfolios.csv",
    {"NoDur", "Utils", "Hlth"},
    "Average Value Weighted Returns -- Monthly",
)


def dlog_usd(a, b):  # 100 * ln(index_b / index_a), chaining across the splice at 2019-12/2020-01
    tot, m = 0.0, a
    while m < b:
        n = add(m, 1)
        src = tw_old if n <= (2019, 12) else tw_new
        if m not in src or n not in src:
            return None
        tot += 100 * math.log(src[n] / src[m])
        m = n
    return tot


def dlog_one(src, a, b):  # 100 * ln change within one index, or None if either month is missing
    if a not in src or b not in src:
        return None
    return 100 * math.log(src[b] / src[a])


peaks_troughs = [
    ((1969, 12), (1970, 11)),
    ((1973, 11), (1975, 3)),
    ((1980, 1), (1980, 7)),
    ((1981, 7), (1982, 11)),
    ((1990, 7), (1991, 3)),
    ((2001, 3), (2001, 11)),
    ((2007, 12), (2009, 6)),
    ((2020, 2), (2020, 4)),
]
nber = {
    m
    for p, t in peaks_troughs
    for m in [add(p, k) for k in range(1, (t[0] * 12 + t[1]) - (p[0] * 12 + p[1]) + 1)]
}

recs = []
for vm in sorted(signals):
    win = [add(vm, k) for k in (1, 2, 3)]
    m3 = win[-1]
    if (
        not all(w in ff and w in ind for w in win)
        or m3 not in gs10
        or vm not in gs10
        or m3 not in baa
    ):
        continue
    r = dict(
        vm=vm,
        sahm=signals[vm][0],
        sig=signals[vm][0] >= 0.5,
        nb=any(w in nber for w in win),
        nball=all(w in nber for w in win),
        usd_g=dlog_one(tw_old, vm, m3),
        usd_gs=dlog_one(tw_new, vm, m3),
        dy10=gs10[m3] - gs10[vm],
        dcred=(baa[m3] - gs10[m3]) - (baa[vm] - gs10[vm]),
        eq=sum(ff[w]["Mkt-RF"] for w in win),
        dfn=sum(
            (ind[w]["NoDur"] + ind[w]["Utils"] + ind[w]["Hlth"]) / 3
            - (ff[w]["Mkt-RF"] + ff[w]["RF"])
            for w in win
        ),
        usd=dlog_usd(vm, m3),
    )  # v1 splice, kept for continuity
    recs.append(r)

with open(os.path.join(HERE, "regime_quarters.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(
        [
            "vintage_month",
            "sahm_realtime",
            "signal",
            "nber_any_overlap",
            "nber_all_months",
            "dy10",
            "dcred",
            "eq",
            "dfn",
            "usd_goods_only",
            "usd_goods_services",
            "usd_splice_v1",
        ]
    )
    for r in recs:
        w.writerow(
            [
                f"{r['vm'][0]}-{r['vm'][1]:02d}",
                f"{r['sahm']:.3f}",
                int(r["sig"]),
                int(r["nb"]),
                int(r["nball"]),
            ]
            + [
                ("" if r[k] is None else f"{r[k]:.4f}")
                for k in ("dy10", "dcred", "eq", "dfn", "usd_g", "usd_gs", "usd")
            ]
        )

want = {"dy10": -1, "dcred": +1, "eq": -1, "dfn": +1, "usd_g": +1, "usd_gs": +1, "usd": +1}
label = {
    "usd_g": "usd (goods only, TWEXBMTH, to 2019)",
    "usd_gs": "usd (goods+services, DTWEXBGS, 2006-)",
    "usd": "usd (v1 splice; definition break 2020-01)",
}


def nw_diff_t(y, d, lags=4):
    """Slope and Newey-West t of y on a constant and the 0/1 indicator d (time order kept)."""
    X = np.column_stack([np.ones(len(y)), d])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X @ b
    S = (X * e[:, None]).T @ (X * e[:, None])
    for L in range(1, lags + 1):
        G = (X[L:] * e[L:, None]).T @ (X[:-L] * e[:-L, None])
        S += (1 - L / (lags + 1)) * (G + G.T)
    Xi = np.linalg.inv(X.T @ X)
    return b[1], b[1] / math.sqrt((Xi @ S @ Xi)[1, 1])


def episodes(flags):
    return sum(1 for i, f in enumerate(flags) if f and (i == 0 or not flags[i - 1]))


def block(key, title):
    print(f"\n== {title}")
    out = {}
    for k, sgn in want.items():
        sub = [r for r in recs if r[k] is not None]
        a = np.array([r[k] for r in sub if r[key]])
        b = np.array([r[k] for r in sub if not r[key]])
        d = a.mean() - b.mean()
        t = d / math.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
        _, tn = nw_diff_t(np.array([r[k] for r in sub]), np.array([float(r[key]) for r in sub]))
        ok = np.sign(d) == sgn and abs(t) > 2
        span = f"{sub[0]['vm'][0]}-{sub[-1]['vm'][0]}"
        print(
            f"  {label.get(k, k):42s} {span}: regime {a.mean():+.3f} (n {len(a)}, {episodes([r[key] for r in sub])} episodes), "
            f"other {b.mean():+.3f} (n {len(b)}), diff {d:+.3f}, Welch t {t:+.2f}, NW(4) t {tn:+.2f}"
            f"  -> {'sign as hypothesised with |Welch t| > 2' if ok else 'threshold not met'}"
        )
        out[k] = ok
    return out


sig = [r for r in recs if r["sig"]]
print(
    f"Quarters: {len(recs)} ({recs[0]['vm']} to {recs[-1]['vm']}); real-time signal in {len(sig)}:"
)
print("  " + ", ".join(f"{r['vm'][0]}-{r['vm'][1]:02d}" for r in sig))
print(f"Vintages skipped for a missing month in the window: {', '.join(skipped) or 'none'}")
print(
    f"NBER quarters: any overlap {sum(r['nb'] for r in recs)} (overlap with signal {sum(r['nb'] and r['sig'] for r in recs)}); "
    f"all three months inside {sum(r['nball'] for r in recs)} (overlap with signal {sum(r['nball'] and r['sig'] for r in recs)})"
)
print("\nREAL-TIME TEST (the only test; decision rule: hypothesised sign with |Welch t| > 2)")
verdict = block("sig", "real-time Sahm signal: mean in regime minus mean outside")
print("\nEX-POST DESCRIPTION (NBER dates known only later; not a test of a usable classification)")
block("nb", "ex-post NBER window, ANY OVERLAP (v1 definition)")
block("nball", "ex-post NBER window, ALL MONTHS inside (sensitivity)")
print(
    "\nVerdict (real time): "
    + "; ".join(
        f"{label.get(k, k)} {'supported' if v else 'not supported'}" for k, v in verdict.items()
    )
)
