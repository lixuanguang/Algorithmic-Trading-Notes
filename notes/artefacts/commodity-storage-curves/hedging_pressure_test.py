"""ev:backwardation-scarcity-or-premium, derivatives and empirical validation (2026-10-17): does WTI hedging pressure predict returns?

Protocol (written before the COT files were downloaded; committed with the results, so not a preregistration):
hedging-pressure-protocol.md.
  HP_t = (commercial short - commercial long) / (commercial short + commercial long), CFTC legacy futures-only report,
  contract market code 067651, from the latest report with positions date R and R + 3 days <= t (month-end settlement).
  H: beta > 0 in r_{t+1} = a + beta HP_t + u, r the v2 WTI held-contract return (column r_next_settle of
  backwardation_monthly.csv, simple return as the WTI protocol defines it); supported if Newey-West (12 lags) t > 2 and
  the expanding out-of-sample R^2 from month 121 is positive with Clark-West t > 1.65 (backwardation_test.oos).
  Reported alongside: corr(HP_t, B_t) and r on B and HP jointly.
Run: python3 hedging_pressure_test.py <folder with deacot*.zip>  (numpy). Writes hedging_pressure_monthly.csv.
"""
import bisect
import csv
import datetime as dt
import glob
import io
import os
import sys
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import backwardation_test as bt  # noqa: E402

rep, names = {}, {}
for path in sorted(glob.glob(os.path.join(sys.argv[1], 'deacot*.zip'))):
    z = zipfile.ZipFile(path)
    for n in z.namelist():
        r = csv.reader(io.TextIOWrapper(z.open(n), encoding='latin-1'))
        h = next(r)
        ci = {k: h.index(k) for k in ('Market and Exchange Names', 'As of Date in Form YYYY-MM-DD', 'CFTC Contract Market Code',
                                      'Commercial Positions-Long (All)', 'Commercial Positions-Short (All)')}
        for row in r:
            if row[ci['CFTC Contract Market Code']].strip() != '067651':
                continue
            d = dt.date.fromisoformat(row[ci['As of Date in Form YYYY-MM-DD']].strip())
            lo, sh = float(row[ci['Commercial Positions-Long (All)']]), float(row[ci['Commercial Positions-Short (All)']])
            rep[d] = (sh - lo) / (sh + lo)
            names.setdefault(row[ci['Market and Exchange Names']].strip(), [d, d])
            nm = names[row[ci['Market and Exchange Names']].strip()]
            nm[0], nm[1] = min(nm[0], d), max(nm[1], d)
dates = sorted(rep)
print(f'COT 067651: {len(dates)} weekly reports, {dates[0]} to {dates[-1]}')
for k, (a, b) in sorted(names.items(), key=lambda x: x[1][0]):
    print(f'  name "{k}": {a} to {b}')

rows = []
with open(os.path.join(HERE, 'backwardation_monthly.csv')) as f:
    for x in csv.DictReader(f):
        if x['market'] != 'WTI':
            continue
        t = dt.date.fromisoformat(x['month_end'])
        i = bisect.bisect_right(dates, t - dt.timedelta(days=3)) - 1
        if i < 0:
            continue
        rows.append(dict(t=t, R=dates[i], hp=rep[dates[i]], B=float(x['B_ln_c1_c2']), r=float(x['r_next_settle'])))
print(f'sample: {rows[0]["t"]} to {rows[-1]["t"]}, n = {len(rows)} months; report age at month-end '
      f'{min((x["t"] - x["R"]).days for x in rows)}-{max((x["t"] - x["R"]).days for x in rows)} days')
hp = np.array([x['hp'] for x in rows]); r = np.array([x['r'] for x in rows]); B = np.array([x['B'] for x in rows])
print(f'HP: mean {hp.mean():+.3f}, sd {hp.std(ddof=1):.3f}, min {hp.min():+.3f}, max {hp.max():+.3f}')
b, t = bt.ols_nw(r, hp)
print(f'H: r on HP   beta = {b[1]:+.4f}  NW t = {t[1]:+.2f}')
r2, cw, n = bt.oos(r, hp)
print(f'H OOS (from month 121): R^2 = {r2*100:+.2f}%  Clark-West t = {cw:+.2f}  n = {n}  (first forecast {rows[120]["t"]})')
print(f'alongside: corr(HP, B) = {np.corrcoef(hp, B)[0, 1]:+.3f}')
bj, tj = bt.ols_nw(r, np.column_stack([B, hp]))
print(f'alongside: r on B and HP   beta_B = {bj[1]:+.4f} (t {tj[1]:+.2f}), beta_HP = {bj[2]:+.4f} (t {tj[2]:+.2f})')
ok = b[1] > 0 and t[1] > 2 and n > 0 and r2 > 0 and cw > 1.65
print(f'\nVerdict: hedging pressure {"supported" if ok else "not supported"}')
with open(os.path.join(HERE, 'hedging_pressure_monthly.csv'), 'w', newline='') as fh:
    w = csv.writer(fh)
    w.writerow(['month_end', 'cot_positions_date', 'hp', 'B_ln_c1_c2', 'r_next_settle'])
    for x in rows:
        w.writerow([x['t'].isoformat(), x['R'].isoformat(), f"{x['hp']:.6f}", f"{x['B']:.6f}", f"{x['r']:.6f}"])
