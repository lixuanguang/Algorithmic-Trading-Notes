"""ev:backwardation-scarcity-or-premium: a bounded test on EIA's public NYMEX futures and inventory series.

Protocol, fixed before results were computed (batch of 17 October 2026):
Hypotheses.
  S (scarcity, theory of storage): the futures curve is more backwardated when inventories are low relative to their
    seasonal norm, i.e. beta_S < 0 in  B_t = a + beta_S * I_t + e_t.
  P (premium): backwardation forecasts the excess return of holding the futures, i.e. beta_P > 0 in
    r_{t+1} = a + beta_P * B_t + u_{t+1}; also tested jointly with I_t, and out of sample against the historical mean.
Data (EIA, U.S. Energy Information Administration, public domain; files in the ignored reading_materials folder):
  WTI: Cushing crude futures contracts 1, 2, 4 (RCLC1-4, daily); U.S. crude stocks excluding SPR (WCESTUS1, weekly).
  Natural gas: Henry Hub futures contracts 1, 2, 4 (RNGC1-4, daily); Lower-48 working gas (NW2_EPG0_SWO_R48_BCF,
  weekly, from 2010). EIA's futures series end on 5 April 2024.
Timing.
  Month-end t = last date in the month with contracts 1 and 2 observed.
  B_t = ln(C1_t / C2_t) (positive = backwardation); B4_t = ln(C1_t / C4_t) / 3 per month (robustness).
  r_{t+1} = C1_{t+1} / C2_t - 1: contract 2 at the end of month t is contract 1 at the end of month t+1 for both
  WTI (expiry about the 20th-22nd of the month before delivery) and Henry Hub (expiry three business days before the
  delivery month), so this is the return of holding one contract; it is a futures (collateral-excess) return.
  I_t = ln(stocks) at the last weekly observation dated at least 5 days before month-end t (EIA reports with a lag)
  minus the mean of ln(stocks) in the same ISO week of the previous five years (a causal seasonal norm).
Costs. A round trip of two ticks per monthly roll (WTI $0.02/bbl, NG $0.002/MMBtu; ticks from NYMEX Chapters 200
  and 220) is subtracted in the net results; an assumption, not a measured cost.
Inference. OLS with Newey-West (12 lags) standard errors. Out of sample: expanding-window OLS of r on B from 120
  months, forecasts compared with the expanding historical mean (OOS R^2; Clark-West statistic, one-sided).
Sufficient test. S is supported if beta_S < 0 with |t| > 2; P is supported if beta_P > 0 with |t| > 2 in sample
  and the OOS R^2 is positive with a Clark-West t above 1.65. Anything else is reported as not supported.
  Added after the first run and labelled exploratory: the regression of r on the indicator 1[B > 0] and a count of
  months with |r| >= 50 percent; they do not change the pre-specified verdicts.
Run: PYTHONPATH=<path with xlrd> python3 backwardation_test.py <folder with EIA_*.xls>
Writes backwardation_monthly.csv (the derived monthly panel) next to this script and prints the results.
"""
import csv
import datetime as dt
import math
import os
import sys

import numpy as np
import xlrd

SRC = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))


def series(name):
    b = xlrd.open_workbook(os.path.join(SRC, f'EIA_{name}.xls'))
    sh = b.sheet_by_name('Data 1')
    out = {}
    for r in range(3, sh.nrows):
        d, v = sh.row_values(r)[:2]
        if d == '' or v == '':
            continue
        out[dt.date(1899, 12, 30) + dt.timedelta(days=int(d))] = float(v)
    return out


def month_ends(c1, c2):
    ends = {}
    for d in sorted(set(c1) & set(c2)):
        ends[(d.year, d.month)] = d
    return [ends[k] for k in sorted(ends)]


def inv_dev(stocks, when):
    obs = [d for d in stocks if d <= when - dt.timedelta(days=5)]
    if not obs:
        return None
    d = max(obs)
    wk = d.isocalendar()[1]
    hist = [math.log(v) for e, v in stocks.items() if e.isocalendar()[1] == wk and d.year - 5 <= e.year < d.year]
    if len(hist) < 5:
        return None
    return math.log(stocks[d]) - sum(hist) / len(hist)


def ols_nw(y, X, lags=12):
    X = np.column_stack([np.ones(len(y)), X])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X @ b
    n = len(y)
    S = (X * e[:, None]).T @ (X * e[:, None])
    for L in range(1, lags + 1):
        w = 1 - L / (lags + 1)
        G = (X[L:] * e[L:, None]).T @ (X[:-L] * e[:-L, None])
        S += w * (G + G.T)
    XtXi = np.linalg.inv(X.T @ X)
    V = XtXi @ S @ XtXi
    return b, b / np.sqrt(np.diag(V)), n


def oos(y, x, start=120):
    if len(y) <= start + 12:
        return float('nan'), float('nan'), 0
    f_m, f_r, act = [], [], []
    for t in range(start, len(y)):
        X = np.column_stack([np.ones(t), x[:t]])
        b = np.linalg.lstsq(X, y[:t], rcond=None)[0]
        f_r.append(b[0] + b[1] * x[t])
        f_m.append(y[:t].mean())
        act.append(y[t])
    f_m, f_r, act = map(np.array, (f_m, f_r, act))
    r2 = 1 - ((act - f_r) ** 2).sum() / ((act - f_m) ** 2).sum()
    cw = (act - f_m) ** 2 - ((act - f_r) ** 2 - (f_m - f_r) ** 2)
    cw_t = cw.mean() / (cw.std(ddof=1) / math.sqrt(len(cw)))
    return r2, cw_t, len(act)


def run(label, c1n, c2n, c4n, stn, tick, rows_out):
    c1, c2, c4, st = series(c1n), series(c2n), series(c4n), series(stn)
    ends = month_ends(c1, c2)
    rows = []
    for i in range(len(ends) - 1):
        t, t1 = ends[i], ends[i + 1]
        if (t1.year * 12 + t1.month) - (t.year * 12 + t.month) != 1:
            continue
        B = math.log(c1[t] / c2[t])
        B4 = math.log(c1[t] / c4[t]) / 3 if t in c4 else float('nan')
        r = c1[t1] / c2[t] - 1
        rnet = (c1[t1] - c2[t] - 2 * tick) / c2[t]
        I = inv_dev(st, t)
        rows.append((t, B, B4, r, rnet, I))
        rows_out.append((label, t.isoformat(), f'{B:.6f}', f'{B4:.6f}', f'{r:.6f}', f'{rnet:.6f}', '' if I is None else f'{I:.6f}'))
    full = [x for x in rows if x[5] is not None]
    B = np.array([x[1] for x in full]); B4 = np.array([x[2] for x in full])
    r = np.array([x[3] for x in full]); rn = np.array([x[4] for x in full]); I = np.array([x[5] for x in full])
    print(f'\n== {label}: {full[0][0]} to {full[-1][0]} (month-ends with inventory norm), n = {len(full)}')
    bS, tS, _ = ols_nw(B, I)
    print(f'  S: B on I        beta_S = {bS[1]:+.4f}  t = {tS[1]:+.2f}')
    ok4 = ~np.isnan(B4)
    bS4, tS4, _ = ols_nw(B4[ok4], I[ok4])
    print(f'  S (C1/C4 slope): beta   = {bS4[1]:+.4f}  t = {tS4[1]:+.2f}')
    bP, tP, _ = ols_nw(r, B)
    print(f'  P: r on B        beta_P = {bP[1]:+.4f}  t = {tP[1]:+.2f}')
    bI, tI, _ = ols_nw(r, I)
    print(f'  P: r on I        beta   = {bI[1]:+.4f}  t = {tI[1]:+.2f}')
    bJ, tJ, _ = ols_nw(r, np.column_stack([B, I]))
    print(f'  P: r on B and I  beta_B = {bJ[1]:+.4f} (t {tJ[1]:+.2f}), beta_I = {bJ[2]:+.4f} (t {tJ[2]:+.2f})')
    bk = B > 0
    print(f'  mean monthly r: backwardated {r[bk].mean()*100:+.2f}% (n {bk.sum()}), contango {r[~bk].mean()*100:+.2f}% (n {(~bk).sum()})')
    print(f'  net of 2 ticks : backwardated {rn[bk].mean()*100:+.2f}%, contango {rn[~bk].mean()*100:+.2f}%')
    ls = np.where(bk, rn, -r - (r - rn))  # long when backwardated, short when in contango, net of costs
    print(f'  timing rule (long if B>0 else short), net: mean {ls.mean()*100:+.2f}%/month, annualised Sharpe {ls.mean()/ls.std(ddof=1)*math.sqrt(12):+.2f}')
    r2, cw, n = oos(r, B)
    if n:
        print(f'  OOS (from month 121): R^2 = {r2*100:+.2f}%  Clark-West t = {cw:+.2f}  n = {n}')
    else:
        print('  OOS: not computed (sample shorter than the pre-set 120-month start plus a year)')
    bD, tD, _ = ols_nw(r, bk.astype(float))
    print(f'  exploratory (not pre-specified): r on 1[B>0]  diff = {bD[1]*100:+.2f}%  t = {tD[1]:+.2f}')
    q = r[np.abs(r) < 0.5]
    print(f'  exploratory: months with |r| >= 50% dropped: {len(r) - len(q)}')
    return dict(n=len(full), bS=bS[1], tS=tS[1], bP=bP[1], tP=tP[1], r2=r2, cw=cw)


out = []
res = {}
res['WTI'] = run('WTI', 'RCLC1d', 'RCLC2d', 'RCLC4d', 'WCESTUS1w', 0.01, out)
res['NG'] = run('NG', 'RNGC1d', 'RNGC2d', 'RNGC4d', 'NW2_EPG0_SWO_R48_BCFw', 0.001, out)
with open(os.path.join(HERE, 'backwardation_monthly.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['market', 'month_end', 'B_ln_c1_c2', 'B4_ln_c1_c4_per_month', 'r_next', 'r_next_net_2ticks', 'inv_dev'])
    w.writerows(out)
for k, v in res.items():
    S = v['bS'] < 0 and abs(v['tS']) > 2
    P = v['bP'] > 0 and abs(v['tP']) > 2 and v['r2'] > 0 and v['cw'] > 1.65
    print(f'\n{k}: scarcity {"supported" if S else "not supported"}; premium {"supported" if P else "not supported"}')
