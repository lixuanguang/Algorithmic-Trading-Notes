"""ev:fx-valuation-factors-oos: out-of-sample test of one of Gliner's factors, relative PPP (the real exchange rate),
against a random walk, on public FRED data.

Protocol, fixed before results were computed (batch of 17 October 2026):
Hypothesis. A currency that is dear in real terms relative to its own history depreciates against the U.S. dollar:
  in  ds_{t,t+h} = a + b z_t + e,  b < 0, where z_t is the deviation of the log real exchange rate from its
  expanding-window mean; and the forecast beats a random walk (no change) out of sample.
Data (FRED, retrieved 2026-10-17): monthly spot rates EXJPUS, EXUSUK, EXSZUS, EXCAUS, EXUSAL, EXUSNZ, EXSDUS,
  EXNOUS, EXDNUS (monthly averages of noon buying rates, H.10/G.5); CPI: CPIAUCNS (U.S.) and the OECD MEI series
  JPN/GBR/CHE/CAN/SWE/NOR/DNK CPIALLMINMEI (monthly) and AUS/NZL CPIALLQINMEI (quarterly), which end between June
  2021 (Japan) and April 2025; three-month interbank rates IR3TIB01**M156N for the carry leg. EUR is excluded
  (short history).
Timing. s_t = ln(USD per foreign unit) for month t (a monthly average, not a month-end rate: a known limitation).
  Price levels known at t: monthly CPI of month t-2; quarterly CPI of the latest quarter ending at least four months
  before t. q_t = s_t + ln P*_known - ln P_US_known; z_t = q_t - mean(q_t0..q_t), from 60 months of history.
  Revised CPI is used (no vintages): a small look-ahead, stated.
Statistical test. Per currency, expanding OLS of ds_{t,t+h} on z_t, first forecast at t = January 1985;
  h = 1 and 12 months. OOS R^2 against the random walk, pooled over currencies and per currency; Clark-West
  statistic pooled, with Newey-West (h - 1 lags) standard error.
Economic test. Each month long the three currencies with the lowest z (cheapest), short the three highest, equal
  weights; next-month return ds (spot only, from 1985) and ds + (i* - i_US)/1200 (excess return, months with all
  rates). Costs: 5 bp per unit of turnover (assumption, not a measured spread).
Sufficient test. Statistical support if the pooled h = 12 OOS R^2 > 0 and the Clark-West t > 1.65.
  Economic support if the net excess-return portfolio's mean is positive with Newey-West t > 2.
Run: python3 fx_ppp_oos_test.py <folder with the FRED csv files>. Writes fx_ppp_monthly.csv (derived panel).
"""
import csv
import datetime as dt
import math
import os
import sys

import numpy as np

SRC = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
CCY = {  # spot id, quoted as foreign per USD?, CPI id, quarterly?, rate id
    'JPY': ('EXJPUS', True, 'JPNCPIALLMINMEI', False, 'IR3TIB01JPM156N'),
    'GBP': ('EXUSUK', False, 'GBRCPIALLMINMEI', False, 'IR3TIB01GBM156N'),
    'CHF': ('EXSZUS', True, 'CHECPIALLMINMEI', False, 'IR3TIB01CHM156N'),
    'CAD': ('EXCAUS', True, 'CANCPIALLMINMEI', False, 'IR3TIB01CAM156N'),
    'AUD': ('EXUSAL', False, 'AUSCPIALLQINMEI', True, 'IR3TIB01AUM156N'),
    'NZD': ('EXUSNZ', False, 'NZLCPIALLQINMEI', True, 'IR3TIB01NZM156N'),
    'SEK': ('EXSDUS', True, 'SWECPIALLMINMEI', False, 'IR3TIB01SEM156N'),
    'NOK': ('EXNOUS', True, 'NORCPIALLMINMEI', False, 'IR3TIB01NOM156N'),
    'DKK': ('EXDNUS', True, 'DNKCPIALLMINMEI', False, 'IR3TIB01DKM156N'),
}


def load(i):
    out = {}
    with open(os.path.join(SRC, i + '.csv')) as f:
        r = csv.reader(f)
        next(r)
        for d, v in r:
            if v not in ('', '.'):
                y, m, _ = map(int, d.split('-'))
                out[(y, m)] = float(v)
    return out


def add(ym, k):
    n = ym[0] * 12 + ym[1] - 1 + k
    return (n // 12, n % 12 + 1)


us_cpi, us_r = load('CPIAUCNS'), load('IR3TIB01USM156N')
months = [add((1971, 1), k) for k in range(12 * 56)]
panel = {}
for c, (sid, inv, cid, qtr, rid) in CCY.items():
    sp, cpi, rate = load(sid), load(cid), load(rid)
    rows = {}
    for t in months:
        if t not in sp:
            continue
        s = -math.log(sp[t]) if inv else math.log(sp[t])
        if qtr:
            cands = [k for k in cpi if (t[0] * 12 + t[1]) - (k[0] * 12 + k[1] + 2) >= 4]
            if not cands:
                continue
            pf = cpi[max(cands)]
        else:
            k = add(t, -2)
            if k not in cpi:
                continue
            pf = cpi[k]
        ku = add(t, -2)
        if ku not in us_cpi:
            continue
        rows[t] = dict(s=s, q=s + math.log(pf) - math.log(us_cpi[ku]), i=rate.get(t), iu=us_r.get(t))
    ts = sorted(rows)
    qs = []
    for t in ts:
        qs.append(rows[t]['q'])
        rows[t]['z'] = rows[t]['q'] - sum(qs) / len(qs) if len(qs) >= 60 else None
    panel[c] = rows


start = (1985, 1)
with open(os.path.join(HERE, 'fx_ppp_monthly.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['ccy', 'month', 's_ln_usd_per_fx', 'q_ln_real', 'z_dev', 'i_fx', 'i_us'])
    for c, rows in panel.items():
        for t in sorted(rows):
            r = rows[t]
            w.writerow([c, f'{t[0]}-{t[1]:02d}', f"{r['s']:.6f}", f"{r['q']:.6f}", '' if r['z'] is None else f"{r['z']:.6f}",
                        '' if r['i'] is None else r['i'], '' if r['iu'] is None else r['iu']])

print('Sample per currency (first z, last month):')
for c, rows in panel.items():
    zt = [t for t in sorted(rows) if rows[t]['z'] is not None]
    print(f'  {c}: {zt[0]} to {zt[-1]}')

for h in (1, 12):
    sse_m = sse_rw = 0.0
    cw_all, bsum = [], []
    print(f'\n== h = {h} months: expanding OLS of ds on z, forecasts from {start[0]}-{start[1]:02d}')
    for c, rows in panel.items():
        ts = [t for t in sorted(rows) if rows[t]['z'] is not None and add(t, h) in rows]
        X = np.array([rows[t]['z'] for t in ts])
        Y = np.array([rows[add(t, h)]['s'] - rows[t]['s'] for t in ts])
        fc, act = [], []
        for j, t in enumerate(ts):
            if t < start:
                continue
            tr = [k for k in range(j) if add(ts[k], h) <= t]  # only outcomes known at t
            if len(tr) < 60:
                continue
            A = np.column_stack([np.ones(len(tr)), X[tr]])
            b = np.linalg.lstsq(A, Y[tr], rcond=None)[0]
            fc.append(b[0] + b[1] * X[j]); act.append(Y[j])
        fc, act = np.array(fc), np.array(act)
        r2 = 1 - ((act - fc) ** 2).sum() / (act ** 2).sum()
        A = np.column_stack([np.ones(len(ts)), X]); bfull = np.linalg.lstsq(A, Y, rcond=None)[0]
        bsum.append(bfull[1])
        print(f'  {c}: n = {len(act)}, OOS R^2 vs RW = {r2*100:+.2f}%, full-sample b = {bfull[1]:+.4f}')
        sse_m += ((act - fc) ** 2).sum(); sse_rw += (act ** 2).sum()
        cw_all.extend(list(act ** 2 - ((act - fc) ** 2 - fc ** 2)))
    cw_all = np.array(cw_all)
    lags = max(h - 1, 0)
    xc = cw_all - cw_all.mean(); n = len(xc)
    s2 = (xc @ xc) / n + 2 * sum((1 - L / (lags + 1)) * (xc[L:] @ xc[:-L]) / n for L in range(1, lags + 1))
    cwt = cw_all.mean() / math.sqrt(s2 / n)
    print(f'  pooled OOS R^2 vs RW = {(1 - sse_m / sse_rw)*100:+.2f}%, Clark-West t = {cwt:+.2f} (pooled, NW {lags} lags; serial correlation across stacked currencies ignored)')
    print(f'  full-sample slopes negative for {sum(b < 0 for b in bsum)} of {len(bsum)} currencies')
    if h == 12:
        stat_ok = (1 - sse_m / sse_rw) > 0 and cwt > 1.65

# economic test
alltimes = sorted(set().union(*[set(r) for r in panel.values()]))
spot, exc, costs, used = [], [], [], []
prev_w = {}
for t in alltimes:
    if t < start:
        continue
    t1 = add(t, 1)
    av = [c for c in panel if t in panel[c] and panel[c][t]['z'] is not None and t1 in panel[c]]
    if len(av) < 6:
        continue
    av.sort(key=lambda c: panel[c][t]['z'])
    wts = {c: 1 / 3 for c in av[:3]}
    wts.update({c: -1 / 3 for c in av[-3:]})
    turn = sum(abs(wts.get(c, 0) - prev_w.get(c, 0)) for c in set(wts) | set(prev_w))
    prev_w = wts
    ds = sum(wv * (panel[c][t1]['s'] - panel[c][t]['s']) for c, wv in wts.items())
    spot.append(ds); costs.append(0.0005 * turn); used.append(t)
    if all(panel[c][t]['i'] is not None and panel[c][t]['iu'] is not None for c in wts):
        exc.append((ds + sum(wv * (panel[c][t]['i'] - panel[c][t]['iu']) / 1200 for c, wv in wts.items()), 0.0005 * turn))


def summ(label, x):
    x = np.array(x)
    xc = x - x.mean(); n = len(x); lags = 12
    s2 = (xc @ xc) / n + 2 * sum((1 - L / (lags + 1)) * (xc[L:] @ xc[:-L]) / n for L in range(1, lags + 1))
    t = x.mean() / math.sqrt(s2 / n)
    print(f'  {label}: n = {n}, mean {x.mean()*1200:+.2f}%/yr, vol {x.std(ddof=1)*math.sqrt(12)*100:.2f}%/yr, Sharpe {x.mean()/x.std(ddof=1)*math.sqrt(12):+.2f}, NW t = {t:+.2f}')
    return x.mean(), t


print(f'\n== Value portfolio (long 3 cheapest, short 3 dearest by z), {used[0]} to {used[-1]}')
summ('spot, gross', spot)
summ('spot, net of 5 bp turnover cost', np.array(spot) - np.array(costs))
ex = np.array([e for e, _ in exc]); exn = np.array([e - c for e, c in exc])
summ('excess return incl. interest differential, gross', ex)
m, tt = summ('excess return, net of costs', exn)
print(f'  mean turnover cost {np.mean(costs)*1200:.2f}%/yr; breakeven cost per unit turnover {np.mean(spot)/np.mean(np.array(costs)/0.0005)*1e4:.1f} bp (spot)')
econ_ok = m > 0 and tt > 2
print(f'\nVerdict: statistical (h = 12) {"supported" if stat_ok else "not supported"}; economic {"supported" if econ_ok else "not supported"}')
