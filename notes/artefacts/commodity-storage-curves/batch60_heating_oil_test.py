"""ev:backwardation-scarcity-or-premium, third batch of 17 October 2026: heating oil / ULSD extension.

The protocol (hypotheses S and P, timing rules, acceptance criteria) is in batch60-heating-oil-protocol.md, written
before the heating-oil and distillate data were downloaded; it is committed with these results, so it is a protocol
recorded in advance within the session, not a preregistration. The WTI and Henry Hub v2 test (backwardation_test.py)
is unchanged; this script imports its functions so that every definition (complete month-ends, contract identity,
inventory deviation, availability lag, Newey-West inference, out-of-sample test) is the same code, and adds only:
  * market 'HO': NYMEX heating oil / ULSD futures, assumed to terminate on the last business day of the month before
    the delivery month (rule text not obtained); the roll check below must support it before the verdict is read;
  * distillate stocks (EIA WDISTUS1, WPSR, Wednesday release) with the crude availability lag (F + 6 days).
Data (EIA, public domain; reading_materials/batch60/empirical): EER_EPD2F_PE1_Y35NY_DPG and EER_EPD2F_PE2_Y35NY_DPG
  daily (EIA labels both "New York Harbor No. 2 Heating Oil Future"; contract 2 from February 1994; both end
  5 April 2024), WDISTUS1 weekly.
Run: python3 batch60_heating_oil_test.py <folder with EIA_*.xls>  (numpy, xlrd; a few seconds).
Writes batch60_heating_oil_monthly.csv next to this script.
"""
import csv
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import backwardation_test as bt  # noqa: E402

_expiry = bt.expiry


def expiry(market, cal, y, m, ng_days=3):
    if market != 'HO':
        return _expiry(market, cal, y, m, ng_days)
    import datetime as dt
    if dt.date(y, m, 1) > cal[-1]:
        return None
    return bt.bd_before(cal, dt.date(y, m, 1), 1)  # last trading day before the first day of the delivery month


bt.expiry = expiry
bt.RULES['HO'] = (3,)  # the ng_days argument is ignored for HO
bt.TICK['HO'] = 0.0001  # $/gallon, an assumption (rule text not obtained); used only in the exploratory rule
bt.LAG['HO'] = 6


def series(src, name):
    return bt.series(src, name)


def main(src):
    c1, c2, st = series(src, 'EER_EPD2F_PE1_Y35NY_DPGd'), series(src, 'EER_EPD2F_PE2_Y35NY_DPGd'), series(src, 'WDISTUS1w')
    cal, rows, excluded = bt.build('HO', c1, c2, {}, st)
    print('== HO (NY Harbor No. 2 heating oil / ULSD futures; distillate stocks)')
    print(f'  calendar {cal[0]} to {cal[-1]} ({len(cal)} trading days with both contracts)')
    for t, why in excluded:
        if why != 'gap in months':
            print(f'  excluded month-end {t}: {why}')
    print(f'  excluded for gaps in months: {sum(w == "gap in months" for _, w in excluded)}')
    print('  roll check (mean score x100 at offset -1 / 0 / +1 trading days from the assumed expiry; n):')
    support = []
    for a in range(cal[0].year, cal[-1].year + 1, 5):
        b = min(a + 4, cal[-1].year)
        rc = bt.roll_check('HO', c1, c2, cal, range(a, b + 1))
        print(f'    {a}-{b}: {rc[-1][0]*100:+.2f} / {rc[0][0]*100:+.2f} / {rc[1][0]*100:+.2f}  (n {rc[0][1]})')
        support.append(rc[0][0] > max(rc[-1][0], rc[1][0]))
    print(f'  roll check supports the assumed expiry in {sum(support)} of {len(support)} five-year blocks')
    inv = [x for x in rows if x['I'] is not None]
    B = np.array([x['B'] for x in rows]); r = np.array([x['r'] for x in rows])
    print(f'  price-only sample: {rows[0]["t"]} to {rows[-1]["t"]}, n = {len(rows)}')
    print(f'  inventory sample : {inv[0]["t"]} to {inv[-1]["t"]}, n = {len(inv)}')
    Bi = np.array([x['B'] for x in inv]); Ii = np.array([x['I'] for x in inv])
    bS, tS = bt.ols_nw(Bi, Ii)
    print(f'  S: B on I (inventory sample)        beta_S = {bS[1]:+.4f}  t = {tS[1]:+.2f}')
    inv14 = [x for x in rows if x['I14'] is not None]
    b14, t14 = bt.ols_nw(np.array([x['B'] for x in inv14]), np.array([x['I14'] for x in inv14]))
    print(f'  S sensitivity, report lag F+14 days : beta_S = {b14[1]:+.4f}  t = {t14[1]:+.2f}  (n {len(inv14)})')
    bP, tP = bt.ols_nw(r, B)
    print(f'  P: r on B (price-only sample)       beta_P = {bP[1]:+.4f}  t = {tP[1]:+.2f}')
    r2, cw, n = bt.oos(r, B)
    print(f'  P OOS (price-only, from month 121): R^2 = {r2*100:+.2f}%  Clark-West t = {cw:+.2f}  n = {n}'
          f'  (first forecast {rows[120]["t"]})')
    ex = [x for x in rows if x['rx'] is not None]
    if ex:
        rx = np.array([x['rx'] for x in ex]); rxn = np.array([x['rxnet'] for x in ex]); bx = np.array([x['B'] for x in ex]) > 0
        lx = np.where(bx, rxn, -rx - (rx - rxn))
        _, tl = bt.ols_nw(lx, np.zeros((len(lx), 0)))
        print(f'  exploratory, not part of the verdict: executable timing rule net of 2 ticks, mean {lx.mean()*100:+.2f}%/month '
              f'(NW t {tl[0]:+.2f}, n {len(ex)})')
    else:
        print('  exploratory executable variant: not computed. HO expires on the last trading day of the month, so the '
              'contract that is C2 at month-end t is already C1 on the next trading day, and the v2 executable rule '
              '(same contract as C2 the next day) has no valid month; not part of the protocol\'s verdict')
    S = bS[1] < 0 and tS[1] < -2
    P = bP[1] > 0 and tP[1] > 2 and n > 0 and r2 > 0 and cw > 1.65
    ok_roll = sum(support) >= len(support) - 1
    print(f'\nHO: roll rule {"supported" if ok_roll else "NOT supported (verdict not read)"}; '
          f'scarcity {"supported" if S else "not supported"}; premium {"supported" if P else "not supported"}')
    with open(os.path.join(HERE, 'batch60_heating_oil_monthly.csv'), 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['month_end', 'next_month_end', 'held_contract_delivery', 'B_ln_c1_c2', 'r_next_settle',
                    'inventory_week_used', 'inv_dev', 'inv_dev_lag14'])
        f = lambda v: '' if v is None else f'{v:.6f}'
        for x in rows:
            w.writerow([x['t'].isoformat(), x['t1'].isoformat(), f'{x["dC2"][0]}-{x["dC2"][1]:02d}', f'{x["B"]:.6f}',
                        f'{x["r"]:.6f}', '' if x['F'] is None else x['F'].isoformat(), f(x['I']), f(x['I14'])])


if __name__ == '__main__':
    main(sys.argv[1])
