"""ev:regime-asset-responses-tested: the regime map's "recession" row, tested on a regime classified with real-time
data. Only this row is tested; the other rows and Gliner's sector phases are not.

Protocol, fixed before results were computed (batch of 17 October 2026):
Hypothesis (legacy map, def:macro-regime-asset-map): in recession, yields fall, credit spreads widen, equities fall,
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
          DTWEXBGS; chained by changes).
  Vintages with a missing month inside the 15-month window are skipped and listed (found on the first run: the
  October 2025 rate is #N/A in the 2026 vintages).
Test. Mean response in signal quarters minus non-signal quarters, Welch t (quarters are non-overlapping windows).
  For contrast, the same with an ex-post classification: window months inside NBER recessions (peak month excluded,
  trough included), which uses information not available in real time.
Sufficient test. A sign is supported if the real-time difference has the hypothesised sign (dy10 < 0, dcred > 0,
  eq < 0, dfn > 0, usd > 0) with |t| > 2.
Run: PYTHONPATH=<path with openpyxl> python3 regime_recession_test.py <empirical folder>   (expects rucqvmd.xlsx,
  fred/*.csv, french/*.csv). Writes regime_quarters.csv (derived panel).
"""
import csv
import datetime as dt
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
    with open(os.path.join(SRC, 'fred', i + '.csv')) as f:
        r = csv.reader(f); next(r)
        for d, v in r:
            if v not in ('', '.'):
                y, m, _ = map(int, d.split('-'))
                out.setdefault((y, m), []).append(float(v))
    return {k: sum(v) / len(v) for k, v in out.items()}


def french(fn, cols, section_header=None):
    out, on = {}, section_header is None
    with open(os.path.join(SRC, 'french', fn)) as f:
        for line in f:
            if section_header and section_header in line:
                on = True; continue
            if not on:
                continue
            parts = [p.strip() for p in line.split(',')]
            if parts[0] == '' and len(parts) > 1 and parts[1]:
                header = parts; continue
            if len(parts[0]) == 6 and parts[0].isdigit():
                out[(int(parts[0][:4]), int(parts[0][4:]))] = {h: float(x) for h, x in zip(header[1:], parts[1:]) if h in cols}
            elif out and (parts[0] == '' or not parts[0].isdigit()):
                break
    return out


wb = openpyxl.load_workbook(os.path.join(SRC, 'rucqvmd.xlsx'), read_only=True)
rows = list(wb['ruc'].iter_rows(values_only=True))
head = rows[0]
months = [tuple(map(int, r[0].split(':'))) for r in rows[1:]]
signals, skipped = {}, []
for j, name in enumerate(head[1:], start=1):
    yy, q = int(name[3:5]), int(name[6])
    year = 1900 + yy if yy >= 60 else 2000 + yy
    vm = (year, 3 * q - 1)
    u = {m: r[j] for m, r in zip(months, rows[1:]) if isinstance(r[j], (int, float))}
    L = max(u)
    a3 = lambda m: sum(u[add(m, -k)] for k in range(3)) / 3
    try:
        cur = a3(L); prev = min(a3(add(L, -k)) for k in range(1, 13))
    except KeyError:
        skipped.append(name)  # a month inside the 15-month window is missing (#N/A) in this vintage
        continue
    signals[vm] = (cur - prev, L)

gs10, baa = fred('GS10'), fred('BAA')
tw_old, tw_new = fred('TWEXBMTH'), fred('DTWEXBGS')
ff = french('F-F_Research_Data_Factors.csv', {'Mkt-RF', 'RF'})
ind = french('12_Industry_Portfolios.csv', {'NoDur', 'Utils', 'Hlth'}, 'Average Value Weighted Returns -- Monthly')


def dlog_usd(a, b):  # 100 * ln(index_b / index_a), chaining across the splice at 2019-12/2020-01
    tot, m = 0.0, a
    while m < b:
        n = add(m, 1)
        src = tw_old if n <= (2019, 12) else tw_new
        if m not in src or n not in src:
            return None
        tot += 100 * math.log(src[n] / src[m]); m = n
    return tot


peaks_troughs = [((1969, 12), (1970, 11)), ((1973, 11), (1975, 3)), ((1980, 1), (1980, 7)), ((1981, 7), (1982, 11)),
                 ((1990, 7), (1991, 3)), ((2001, 3), (2001, 11)), ((2007, 12), (2009, 6)), ((2020, 2), (2020, 4))]
nber = {m for p, t in peaks_troughs for m in [add(p, k) for k in range(1, (t[0] * 12 + t[1]) - (p[0] * 12 + p[1]) + 1)]}

recs = []
for vm in sorted(signals):
    win = [add(vm, k) for k in (1, 2, 3)]
    m3 = win[-1]
    if not all(w in ff and w in ind for w in win) or m3 not in gs10 or vm not in gs10 or m3 not in baa:
        continue
    r = dict(vm=vm, sahm=signals[vm][0], sig=signals[vm][0] >= 0.5, nb=any(w in nber for w in win),
             dy10=gs10[m3] - gs10[vm], dcred=(baa[m3] - gs10[m3]) - (baa[vm] - gs10[vm]),
             eq=sum(ff[w]['Mkt-RF'] for w in win),
             dfn=sum((ind[w]['NoDur'] + ind[w]['Utils'] + ind[w]['Hlth']) / 3 - (ff[w]['Mkt-RF'] + ff[w]['RF']) for w in win),
             usd=dlog_usd(vm, m3))
    recs.append(r)

with open(os.path.join(HERE, 'regime_quarters.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['vintage_month', 'sahm_realtime', 'signal', 'nber_window', 'dy10', 'dcred', 'eq', 'dfn', 'usd'])
    for r in recs:
        w.writerow([f"{r['vm'][0]}-{r['vm'][1]:02d}", f"{r['sahm']:.3f}", int(r['sig']), int(r['nb'])] +
                   [('' if r[k] is None else f'{r[k]:.4f}') for k in ('dy10', 'dcred', 'eq', 'dfn', 'usd')])

sig = [r for r in recs if r['sig']]
print(f"Quarters: {len(recs)} ({recs[0]['vm']} to {recs[-1]['vm']}); real-time signal in {len(sig)}:")
print('  ' + ', '.join(f"{r['vm'][0]}-{r['vm'][1]:02d}" for r in sig))
print(f"Vintages skipped for a missing month in the window: {', '.join(skipped) or 'none'}")
print(f"NBER-window quarters: {sum(r['nb'] for r in recs)}; overlap with signal: {sum(r['nb'] and r['sig'] for r in recs)}")
want = {'dy10': -1, 'dcred': +1, 'eq': -1, 'dfn': +1, 'usd': +1}
verdict = {}
for key, cls in (('sig', 'real-time Sahm signal'), ('nb', 'ex-post NBER window')):
    print(f'\n== {cls}: mean in regime minus mean outside (Welch t)')
    for k, sgn in want.items():
        a = np.array([r[k] for r in recs if r[key] and r[k] is not None])
        b = np.array([r[k] for r in recs if not r[key] and r[k] is not None])
        d = a.mean() - b.mean()
        t = d / math.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
        ok = np.sign(d) == sgn and abs(t) > 2
        print(f'  {k:6s}: regime {a.mean():+.3f} (n {len(a)}), other {b.mean():+.3f} (n {len(b)}), diff {d:+.3f}, t {t:+.2f}  -> {"supported" if ok else "not supported"}')
        if key == 'sig':
            verdict[k] = ok
print('\nVerdict (real time): ' + '; '.join(f'{k} {"supported" if v else "not supported"}' for k, v in verdict.items()))
