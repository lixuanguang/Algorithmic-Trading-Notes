"""ev:regime-asset-responses-tested, empirical extensions (2026-10-17): the regime map's "inflation shock" row, classified
in real time. The recession-row test (regime_recession_test.py) and its outputs are unchanged.

Protocol and its two deviations (both recorded before any result was computed): inflation-row-protocol.md.
It is committed with these results, so it is a protocol recorded in advance within the session, not a preregistration.
  Regime: Philadelphia Fed Real-Time Data Set, CPI (PCPI), monthly vintages of monthly data (pcpiMvMd.xlsx); the
    middle-month vintage of each quarter (February, May, August, November) stands for the quarterly vintage. In a
    vintage with last reported month L, pi(L) = 100 ln(P_L/P_{L-12}); signal = 1 if pi(L) - pi(L-12) >= 1.0 point.
    The vintage month m is the vintage's own month (PCPIyyMmm).
  Responses over m+1..m+3:
    dy10   = GS10(m+3) - GS10(m)                       (FRED GS10, retained from the recession test);
    dslope = (GS10 - TB3)(m+3) - (GS10 - TB3)(m)        (TB3 = monthly business-day average of H.15's 3-month bill,
                                                        discount basis, from the committed daily extract);
    oil    = 100 ln(RWTC(m+3)/RWTC(m))                  (EIA Cushing WTI spot, monthly average; a spot price).
  Test: mean in signal quarters minus non-signal quarters, Welch t; supported if dy10 > 0, dslope > 0, oil > 0 with
    |t| > 2. Reported alongside: Newey-West t (4 lags) from the regression on the indicator, and episode counts.
Run: uv run --group empirical python inflation_regime_test.py <reading_materials root>
  (expects empirical-extensions/empirical/pcpiMvMd.xlsx, empirical-extensions/empirical/EIA_RWTCm.xls, source-verification/empirical/fred/GS10.csv).
Writes inflation_monthly_vintage_quarters.csv.
"""

# standard library imports
import csv
import datetime as dt
import math
import os
import sys

# third party library imports
import numpy as np
import openpyxl
import xlrd

ROOT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
H15 = os.path.join(HERE, "..", "multi-asset-systematic-macro", "h15-daily-3m-10y.csv")


def add(ym, k):
    n = ym[0] * 12 + ym[1] - 1 + k
    return (n // 12, n % 12 + 1)


def monthly_mean(pairs):
    acc = {}
    for d, v in pairs:
        acc.setdefault(d, []).append(v)
    return {k: sum(v) / len(v) for k, v in acc.items()}


gs10 = {}
with open(os.path.join(ROOT, "source-verification", "empirical", "fred", "GS10.csv")) as f:
    r = csv.reader(f)
    next(r)
    gs10 = monthly_mean(
        [(tuple(map(int, d.split("-")[:2])), float(v)) for d, v in r if v not in ("", ".")]
    )
tb3 = []
with open(H15) as f:
    for row in csv.DictReader(f):
        if row["tb3m_discount"] not in ("", "ND"):
            y, m, _ = map(int, row["date"].split("-"))
            tb3.append(((y, m), float(row["tb3m_discount"])))
tb3 = monthly_mean(tb3)
sh = xlrd.open_workbook(
    os.path.join(ROOT, "empirical-extensions", "empirical", "EIA_RWTCm.xls")
).sheet_by_name("Data 1")
oil = {}
for i in range(3, sh.nrows):
    d, v = sh.row_values(i)[:2]
    if d != "" and v != "":
        x = dt.date(1899, 12, 30) + dt.timedelta(days=int(d))
        oil[(x.year, x.month)] = float(v)

wb = openpyxl.load_workbook(
    os.path.join(ROOT, "empirical-extensions", "empirical", "pcpiMvMd.xlsx"), read_only=True
)
rows = list(wb["pcpi"].iter_rows(values_only=True))
head, body = rows[0], rows[1:]
months = [tuple(map(int, r[0].split(":"))) for r in body]
obs, skipped = [], []
for j, name in enumerate(head[1:], start=1):
    yy, mm = int(name[4:6]), int(name[7:])
    year = 1900 + yy if yy >= 60 else 2000 + yy
    if mm not in (2, 5, 8, 11):
        continue
    vm = (year, mm)
    p = {m: row[j] for m, row in zip(months, body) if isinstance(row[j], (int, float))}
    L = max(p)
    try:
        pi = lambda t: 100 * math.log(p[t] / p[add(t, -12)])
        accel = pi(L) - pi(add(L, -12))
    except KeyError:
        skipped.append(name)
        continue
    m3 = add(vm, 3)
    if not all(k in src for k in (vm, m3) for src in (gs10, tb3, oil)):
        skipped.append(name + " (responses incomplete)")
        continue
    obs.append(
        dict(
            v=name,
            m=vm,
            L=L,
            pi=pi(L),
            accel=accel,
            sig=int(accel >= 1.0),
            dy10=gs10[m3] - gs10[vm],
            dslope=(gs10[m3] - tb3[m3]) - (gs10[vm] - tb3[vm]),
            oil=100 * math.log(oil[m3] / oil[vm]),
        )
    )

with open(os.path.join(HERE, "inflation_monthly_vintage_quarters.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(
        [
            "vintage",
            "vintage_month",
            "last_cpi_month",
            "pi_12m",
            "accel_12m",
            "signal",
            "dy10",
            "dslope",
            "oil",
        ]
    )
    for o in obs:
        w.writerow(
            [
                o["v"],
                f"{o['m'][0]}-{o['m'][1]:02d}",
                f"{o['L'][0]}-{o['L'][1]:02d}",
                f"{o['pi']:.3f}",
                f"{o['accel']:.3f}",
                o["sig"],
                f"{o['dy10']:.4f}",
                f"{o['dslope']:.4f}",
                f"{o['oil']:.4f}",
            ]
        )

sig = np.array([o["sig"] for o in obs])
runs = sum(1 for i, s in enumerate(sig) if s and (i == 0 or not sig[i - 1]))
print(
    f"vintages used: {len(obs)} ({obs[0]['v']} to {obs[-1]['v']}); skipped: {', '.join(skipped) if skipped else 'none'}"
)
print(
    f"signal quarters: {int(sig.sum())} in {runs} episodes: "
    + ", ".join(o["v"] for o, s in zip(obs, sig) if s)
)


def welch(a, b):
    return (a.mean() - b.mean()) / math.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))


def nw(y, x, lags=4):
    X = np.column_stack([np.ones(len(y)), x])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X @ b
    S = (X * e[:, None]).T @ (X * e[:, None])
    for L in range(1, lags + 1):
        G = (X[L:] * e[L:, None]).T @ (X[:-L] * e[:-L, None])
        S += (1 - L / (lags + 1)) * (G + G.T)
    Xi = np.linalg.inv(X.T @ X)
    return b[1] / math.sqrt((Xi @ S @ Xi)[1, 1])


verdict = {}
print("\nresponse   hypothesis   signal mean   other mean   difference   Welch t   NW t (4 lags)")
for k, hyp in (("dy10", "> 0"), ("dslope", "> 0"), ("oil", "> 0")):
    y = np.array([o[k] for o in obs])
    a, b = y[sig == 1], y[sig == 0]
    t = welch(a, b)
    tn = nw(y, sig.astype(float))
    d = a.mean() - b.mean()
    verdict[k] = d > 0 and abs(t) > 2
    print(
        f"{k:8s}   {hyp:10s}   {a.mean():+10.3f}   {b.mean():+10.3f}   {d:+10.3f}   {t:+7.2f}   {tn:+7.2f}"
    )
print(
    "\nVerdict (Welch |t| > 2, hypothesised sign): "
    + "; ".join(f"{k} {'supported' if v else 'not supported'}" for k, v in verdict.items())
)
