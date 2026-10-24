"""ev:regime-asset-responses-tested, derivatives and empirical validation (2026-10-17): the regime map's "deflation or disinflation" row on
the Philadelphia Fed's quarterly CPI vintages.

Protocol: deflation-row-protocol.md (recorded before this row's results were computed, after the inflation row had
been run on the same data; committed with the results, so not a preregistration). Signal = 1 if, in the vintage dated in
the quarter's middle month m, pi(L) - pi(L-12) <= -1.0 point. Hypothesis: dy10 = GS10(m+3) - GS10(m) < 0, supported if
the signal-minus-other difference is negative with Welch |t| > 2. Alongside: Newey-West t (4 lags), episodes, and the
slope and WTI responses of the inflation row. Loaders are copied from inflation_quarterly_test.py unchanged.
Run: uv run --frozen --no-editable --group empirical python deflation_row_test.py <reading_materials root>
  Writes deflation_quarters.csv.
"""

import csv
import datetime as dt
import math
import os
import sys

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


def vintages(path, sheet, kind):
    """Yield (name, vintage month, {obs month: level}) for each middle-month vintage of the file."""
    wb = openpyxl.load_workbook(path, read_only=True)
    rows = list(wb[sheet].iter_rows(values_only=True))
    head, body = rows[0], rows[1:]
    months = [tuple(map(int, r[0].split(":"))) for r in body]
    for j, name in enumerate(head[1:], start=1):
        yy = int(name[len(kind) : len(kind) + 2])
        year = 1900 + yy if yy >= 60 else 2000 + yy
        if kind == "CPI":  # CPIyyQq: middle month of quarter q
            mm = 3 * int(name[-1]) - 1
        else:  # PCPIyyMmm: keep the middle months only
            mm = int(name[len(kind) + 3 :])
            if mm not in (2, 5, 8, 11):
                continue
        p = {m: row[j] for m, row in zip(months, body) if isinstance(row[j], (int, float))}
        if p:
            yield name, (year, mm), p


def classify(p):
    L = max(p)
    pi = lambda t: 100 * math.log(p[t] / p[add(t, -12)])
    return L, pi(L), pi(L) - pi(add(L, -12))


obs, skipped = [], []
for name, vm, p in vintages(
    os.path.join(ROOT, "derivatives-validation", "empirical", "cpiQvMd.xlsx"), "cpi", "CPI"
):
    try:
        L, pil, accel = classify(p)
    except KeyError:
        skipped.append(name + " (window incomplete)")
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
            pi=pil,
            accel=accel,
            sig=int(accel <= -1.0),
            dy10=gs10[m3] - gs10[vm],
            dslope=(gs10[m3] - tb3[m3]) - (gs10[vm] - tb3[vm]),
            oil=100 * math.log(oil[m3] / oil[vm]),
        )
    )
with open(os.path.join(HERE, "deflation_quarters.csv"), "w", newline="") as f:
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
print("Deflation / disinflation row, quarterly CPI vintages (cpiQvMd.xlsx)")
print(f"vintages used: {len(obs)} ({obs[0]['v']} to {obs[-1]['v']}); skipped: {len(skipped)}")
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


print("\nresponse   role          signal mean   other mean   difference   Welch t   NW t (4 lags)")
for k, role in (("dy10", "H: < 0"), ("dslope", "alongside"), ("oil", "alongside")):
    y = np.array([o[k] for o in obs])
    a, b = y[sig == 1], y[sig == 0]
    t = welch(a, b)
    tn = nw(y, sig.astype(float))
    d = a.mean() - b.mean()
    if k == "dy10":
        verdict = d < 0 and abs(t) > 2
    print(
        f"{k:8s}   {role:10s}   {a.mean():+10.3f}   {b.mean():+10.3f}   {d:+10.3f}   {t:+7.2f}   {tn:+7.2f}"
    )
print(f"\nVerdict (dy10 < 0 with Welch |t| > 2): {'supported' if verdict else 'not supported'}")
