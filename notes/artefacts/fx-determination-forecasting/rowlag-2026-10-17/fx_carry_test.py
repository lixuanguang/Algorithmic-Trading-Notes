"""ev:fx-valuation-factors-oos, empirical extensions (2026-10-17): Gliner's carry indicator (the short-rate differential)
as a second factor, out of sample against a random walk.

Protocol: fx-carry-protocol.md, written before any carry result was computed (the FRED files had been used
by the v2 PPP test, so the protocol is not blind to the data; it is committed with the results and is not a
preregistration). The v2 PPP script is imported for its loaders and Newey-West helper only; its test and outputs are
unchanged.
  x_t = i_fx - i_us of month t-1 (OECD MEI IR3TIB01, three-month interbank, monthly averages, % a year);
  ds_{t,t+h} = s_{t+h} - s_t, s = log USD per foreign unit (FRED H.10/G.5 monthly averages); h = 1 and 12;
  expanding OLS pooled across the nine currencies on pairs with outcome month <= t; data from 1985-01, at least
  60 pooled pairs, forecasts from 1995-01; benchmark: random walk (zero change);
  statistical verdict on h = 12: pooled OOS R^2 > 0 and Clark-West t > 1.65 (Newey-West, h-1 lags);
  economic verdict: median-split long-short portfolio, one-month spot change plus the month-t interest accrual,
  less 5 bp per unit of turnover; mean > 0 with Newey-West (12 lags) t > 2. A statistical return on averaged
  prices and interbank rates, not an executable result.
Run: python3 fx_carry_test.py <folder with the FRED csv files>  (numpy). Writes fx_carry_monthly.csv.
"""
import csv
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fx_ppp_oos_test as v2  # noqa: E402

START, FIRST_FC = (1985, 1), (1995, 1)


def main(src):
    us = v2.load(src, 'IR3TIB01USM156N')
    spot, rate = {}, {}
    for c, (sid, inv, _cid, _q, rid) in v2.CCY.items():
        sp = v2.load(src, sid)
        spot[c] = {t: (-math.log(v) if inv else math.log(v)) for t, v in sp.items()}
        rate[c] = v2.load(src, rid)
    x = {c: {t: rate[c][v2.add(t, -1)] - us[v2.add(t, -1)] for t in spot[c]
             if v2.add(t, -1) in rate[c] and v2.add(t, -1) in us and t >= START} for c in v2.CCY}
    with open(os.path.join(HERE, 'fx_carry_monthly.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['ccy', 'month', 's_ln_usd_per_fx', 'x_diff_prev_month', 'i_fx_month', 'i_us_month'])
        for c in v2.CCY:
            for t in sorted(x[c]):
                w.writerow([c, f'{t[0]}-{t[1]:02d}', f'{spot[c][t]:.6f}', f'{x[c][t]:.4f}',
                            rate[c].get(t, ''), us.get(t, '')])
    print('Samples (predictor available): ' + '; '.join(f'{c} {min(x[c])}-{max(x[c])}' for c in v2.CCY if x[c]))
    stat_ok = False
    for h in (1, 12):
        pairs = [(t, c, x[c][t], spot[c][v2.add(t, h)] - spot[c][t]) for c in v2.CCY for t in x[c] if v2.add(t, h) in spot[c]]
        pairs.sort()
        months = sorted({p[0] for p in pairs if p[0] >= FIRST_FC})
        a_all, f_all, by_c = [], [], {}
        last_b = None
        for t in months:
            tr = [p for p in pairs if v2.add(p[0], h) <= t]
            if len(tr) < 60:
                continue
            A = np.column_stack([np.ones(len(tr)), [p[2] for p in tr]])
            b = np.linalg.lstsq(A, np.array([p[3] for p in tr]), rcond=None)[0]
            last_b = b
            for p in pairs:
                if p[0] == t:
                    fc = b[0] + b[1] * p[2]
                    f_all.append(fc); a_all.append(p[3])
                    by_c.setdefault(p[1], []).append((fc, p[3]))
        a, f = np.array(a_all), np.array(f_all)
        r2 = 1 - ((a - f) ** 2).sum() / (a ** 2).sum()
        cw = a ** 2 - ((a - f) ** 2 - f ** 2)
        cwt = v2.nw_t(cw, max(h - 1, 0))
        A = np.column_stack([np.ones(len(pairs)), [p[2] for p in pairs]])
        bfull = np.linalg.lstsq(A, np.array([p[3] for p in pairs]), rcond=None)[0]
        print(f'\n== h = {h}: pooled expanding OLS of ds on x, forecasts {months[0]} onward, n = {len(a)}')
        print(f'  full-sample pooled slope b = {bfull[1]:+.5f} per percentage point (UIP benchmark {-h/1200:+.5f}); '
              f'last expanding b = {last_b[1]:+.5f}')
        for c in v2.CCY:
            if c in by_c:
                ff = np.array([q[0] for q in by_c[c]]); aa = np.array([q[1] for q in by_c[c]])
                print(f'  {c}: n = {len(aa)}, OOS R^2 vs RW = {(1 - ((aa - ff) ** 2).sum() / (aa ** 2).sum())*100:+.2f}%')
        print(f'  pooled OOS R^2 vs RW = {r2*100:+.2f}%, Clark-West t = {cwt:+.2f} (NW {max(h-1,0)} lags; '
              'cross-currency correlation ignored)')
        if h == 12:
            stat_ok = r2 > 0 and cwt > 1.65
    # economic: median-split portfolio
    rets, used, prev = [], [], {}
    for t in sorted(set().union(*[set(x[c]) for c in v2.CCY])):
        t1 = v2.add(t, 1)
        av = [c for c in v2.CCY if t in x[c] and t1 in spot[c] and t in rate[c] and t in us]
        if len(av) < 6:
            continue
        med = float(np.median([x[c][t] for c in av]))
        lo = [c for c in av if x[c][t] > med]; sh = [c for c in av if x[c][t] < med]
        if not lo or not sh:
            continue
        wts = {**{c: 1 / len(lo) for c in lo}, **{c: -1 / len(sh) for c in sh}}
        turn = sum(abs(wts.get(c, 0) - prev.get(c, 0)) for c in set(wts) | set(prev))
        prev = wts
        g = sum(wv * (spot[c][t1] - spot[c][t] + (rate[c][t] - us[t]) / 1200) for c, wv in wts.items())
        rets.append((g, g - 0.0005 * turn)); used.append(t)
    gr = np.array([r[0] for r in rets]); nt = np.array([r[1] for r in rets])
    tn = v2.nw_t(nt, 12)
    sp_only = None
    print(f'\n== Carry portfolio (median split on x), {used[0]} to {used[-1]}, n = {len(nt)} months')
    print(f'  gross: mean {gr.mean()*1200:+.2f}%/yr; net: mean {nt.mean()*1200:+.2f}%/yr, vol {nt.std(ddof=1)*math.sqrt(12)*100:.2f}%/yr, '
          f'Sharpe {nt.mean()/nt.std(ddof=1)*math.sqrt(12):+.2f}, NW t = {tn:+.2f}')
    worst = np.argsort(nt)[:3]
    print('  three worst months: ' + ', '.join(f'{used[i][0]}-{used[i][1]:02d} {nt[i]*100:+.2f}%' for i in sorted(worst)))
    econ_ok = nt.mean() > 0 and tn > 2
    print(f'\nVerdict: statistical (h = 12) {"supported" if stat_ok else "not supported"}; '
          f'economic (statistical portfolio) {"supported" if econ_ok else "not supported"}')


if __name__ == '__main__':
    main(sys.argv[1])
