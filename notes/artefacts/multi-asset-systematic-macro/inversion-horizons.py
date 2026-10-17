"""empirical extensions (2026-10-17): status of the post-2005 provisional inversion outcomes (ev:curve-inversion-after-2005).

Inputs: h15-spread-monthly.csv (committed; the paper's bond-equivalent 10y-3m spread rebuilt from H.15, complete months
to September 2026) and NBER's chronology and announcement list as read on 2026-10-17 (business-cycle dates page, data
last updated 14 March 2023; announcements page). Facts used:
  peaks (first contraction month = peak + 1): ..., 2007-12, 2020-02; no peak dated after February 2020;
  announcement dates of peaks: 1980-01 on 1980-06-03, 1981-07 on 1982-01-06, 1990-07 on 1991-04-25,
  2001-03 on 2001-11-26, 2007-12 on 2008-12-01, 2020-02 on 2020-06-08 (lags 5, 6, 9, 8, 12 and 4 months).
For each negative month t inside an expansion from November 2022, the month rule asks whether a recession began in
t+1..t+12, i.e. whether a peak fell in t..t+11. Two separate questions are answered:
  (1) calendar: has month t+12 ended by 17 October 2026 (the window is complete)?
  (2) dating: would a peak at the window's latest month, t+11, have been announced by now if NBER's lag were no
      longer than the longest announced in the list (12 months), i.e. is t+11+12 <= 2026-09 (last complete month)?
A month passing (1) and (2) is a miss beyond the longest past lag: retrospective dating is still possible but would
need a longer lag than any in the list. A month passing (1) only remains open to dating within past lags.
Run: python3 inversion-horizons.py   (standard library). Exits non-zero on failure.
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASOF_LAST_COMPLETE = (2026, 9)
LAGS = {(1980, 1): (1980, 6), (1981, 7): (1982, 1), (1990, 7): (1991, 4), (2001, 3): (2001, 11), (2007, 12): (2008, 12),
        (2020, 2): (2020, 6)}


def n(ym):
    return ym[0] * 12 + ym[1] - 1


def ym(k):
    return (k // 12, k % 12 + 1)


lags = {p: n(a) - n(p) for p, a in LAGS.items()}
maxlag = max(lags.values())
print('NBER peak announcement lags (months): ' + ', '.join(f'{p[0]}-{p[1]:02d}: {l}' for p, l in lags.items()) + f'; max {maxlag}')
neg = []
with open(os.path.join(HERE, 'h15-spread-monthly.csv')) as f:
    for r in csv.DictReader(f):
        y, m = map(int, r['month'].split('-'))
        if r['complete'] == 'yes' and float(r['spread_10y_3m_be']) < 0 and (y, m) >= (2022, 11):
            neg.append((y, m))
print(f'negative complete months from 2022-11: {len(neg)} ({neg[0][0]}-{neg[0][1]:02d} .. {neg[-1][0]}-{neg[-1][1]:02d})')
beyond, within, open_cal = [], [], []
for t in neg:
    cal_done = n(t) + 12 <= n(ASOF_LAST_COMPLETE)
    dated_by_now = n(t) + 11 + maxlag <= n(ASOF_LAST_COMPLETE)
    (beyond if cal_done and dated_by_now else within if cal_done else open_cal).append(t)
fmt = lambda xs: ', '.join(f'{a}-{b:02d}' for a, b in xs) if xs else 'none'
print(f'(1) window complete and (2) beyond the longest past lag: {len(beyond)} months ({fmt(beyond[:1])} .. {fmt(beyond[-1:])})')
print(f'(1) window complete, (2) still within the longest past lag: {len(within)} months: {fmt(within)}')
print(f'window not yet complete: {len(open_cal)} months: {fmt(open_cal)}')
episodes = []
for t in neg:
    if episodes and n(t) == n(episodes[-1][-1]) + 1:
        episodes[-1].append(t)
    else:
        episodes.append([t])
for e in episodes:
    last = e[-1]
    status = 'beyond the longest past lag' if n(last) + 11 + maxlag <= n(ASOF_LAST_COMPLETE) else 'within the longest past lag'
    print(f'episode {e[0][0]}-{e[0][1]:02d} .. {last[0]}-{last[1]:02d} ({len(e)} months): window to {ym(n(last)+12)[0]}-{ym(n(last)+12)[1]:02d} complete; dating {status}')
ok = len(neg) == 27 and len(open_cal) == 0
if not ok:
    print('FAILED: expected 27 negative months, all windows complete')
    sys.exit(1)
print('checks passed')
