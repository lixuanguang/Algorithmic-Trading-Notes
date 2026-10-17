"""derivatives and empirical validation (2026-10-17): data:gsw-treasury-curve and ev:term-premia (two descriptive checks, no hypothesis).

Choices recorded before computing (committed with the output, so not a preregistration):
1. GSW (FEDS 2006-28, eq. (22)): recompute the 10-year continuously compounded zero yield from each day's published
   parameters (BETA0-BETA3, TAU1, TAU2) and compare with the published SVENY10. Days with any of these missing are
   skipped; days with BETA3 = 0 (the Nelson-Siegel period, TAU2 missing or unused) use the three-term form.
2. Kim-Wright against ACM: the 10-year zero-coupon term premium, THREEFYTP1000.B (Board's feds200533 file, daily) against
   ACMTP10 (New York Fed, end of month, retained from empirical extensions (2026-10-17)). KW is sampled on the last available day of each
   month; reported: common months, correlation, mean and range of KW - ACM, both series at the last common month and at
   June 2020 and December 1990. Both are model outputs and are revised; this compares two vintages, it tests nothing.
Run: python3 gsw-kw-acm.py <feds200628.csv> <feds200533.csv> <ACMTermPremium.xls>   (numpy, xlrd).
"""
import csv
import datetime as dt
import math
import sys

import numpy as np
import xlrd


def table(path):
    with open(path) as f:
        rows = list(csv.reader(f))
    i = next(k for k, r in enumerate(rows) if r and r[0] == 'Date')
    head = rows[i]
    return head, rows[i + 1:]


def num(x):
    try:
        v = float(x)
        return None if math.isnan(v) else v
    except ValueError:
        return None


head, body = table(sys.argv[1])
c = {h: k for k, h in enumerate(head)}
diffs, n_ns = [], 0
for r in body:
    b0, b1, b2, b3, t1, t2, y10 = (num(r[c[k]]) for k in ('BETA0', 'BETA1', 'BETA2', 'BETA3', 'TAU1', 'TAU2', 'SVENY10'))
    if None in (b0, b1, b2, t1, y10):
        continue
    n = 10.0
    e1 = math.exp(-n / t1)
    y = b0 + b1 * (1 - e1) / (n / t1) + b2 * ((1 - e1) / (n / t1) - e1)
    if b3 not in (None, 0.0) and t2 not in (None, 0.0):
        e2 = math.exp(-n / t2)
        y += b3 * ((1 - e2) / (n / t2) - e2)
    else:
        n_ns += 1
    diffs.append((abs(y - y10), r[0], y, y10))
d = np.array([x[0] for x in diffs])
w = max(diffs)
print(f'GSW: {len(diffs)} days with a 10-year yield; recomputed minus published |diff| max {d.max():.5f} pp '
      f'({w[1]}: {w[2]:.4f} vs {w[3]:.4f}), 99th percentile {np.percentile(d, 99):.5f}; three-term days {n_ns}')
last = diffs[-1]
print(f'  last day {last[1]}: recomputed {last[2]:.4f}, published {last[3]:.4f}')
assert d.max() < 0.001, 'published SVENY10 not reproduced to 0.1 bp'

head, body = table(sys.argv[2])
c = {h: k for k, h in enumerate(head)}
kw = {}
for r in body:
    v = num(r[c['THREEFYTP1000.B']])
    if v is not None:
        y, m, _ = map(int, r[0].split('-'))
        kw[(y, m)] = (r[0], v)          # rows are in date order, so the last day of each month wins
sh = xlrd.open_workbook(sys.argv[3]).sheet_by_name('ACM Monthly')
hd = sh.row_values(0)
acm = {}
for i in range(1, sh.nrows):
    row = sh.row_values(i)
    x = dt.datetime.strptime(row[0], '%d-%b-%Y')
    acm[(x.year, x.month)] = row[hd.index('ACMTP10')]
common = sorted(set(kw) & set(acm))
a = np.array([kw[k][1] for k in common]); b = np.array([acm[k] for k in common])
print(f'KW vs ACM, 10-year term premium: {len(common)} common months, {common[0]} to {common[-1]}')
print(f'  correlation {np.corrcoef(a, b)[0, 1]:.3f}; KW - ACM mean {np.mean(a - b):+.2f} pp, range {np.min(a - b):+.2f} to {np.max(a - b):+.2f}')
print(f'  months both below zero {int(((a < 0) & (b < 0)).sum())}; KW below zero {int((a < 0).sum())}; ACM below zero {int((b < 0).sum())}')
for k in ((1990, 12), (2020, 6), common[-1]):
    if k in kw and k in acm:
        print(f'  {k[0]}-{k[1]:02d}: KW {kw[k][1]:+.2f} ({kw[k][0]}), ACM {acm[k]:+.2f}')
