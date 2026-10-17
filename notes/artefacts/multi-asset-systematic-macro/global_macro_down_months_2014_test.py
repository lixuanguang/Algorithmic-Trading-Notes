"""ev:global-macro-returns-after-2013, empirical extensions (2026-10-17): the original protocol's window, January 2014 to
July 2026, on the Barclay Global Macro Index workbook.

Why a second script. method validation (2026-10-17) ran the protocol on January 2022 - July 2026 only (global_macro_down_months_test.py,
55 months, kept unchanged with its outputs as the recent-period comparison), stating that earlier history needed
registration. That statement was wrong: BarclayHedge's public index page offers the whole history through its ordinary
Excel form (POST https://portal.barclayhedge.com/cgi-bin/indices/ghsndx_JSON.cgi with dump=excel&prog_cod=ghsmc), which an
audit used without registration. The workbook was retrieved the same way on 2026-10-17 07:58 UTC; its SHA-256,
ead890c4274a7cdd7f92e3da23d15dbd0359dd239bf6a3841cddf437853d1097, equals the audit's. The window and the rules below
are the protocol's (recorded in the source verification (2026-10-17) before any index data were seen) and method validation (2026-10-17)'s
data choices (fixed before its computation); none was chosen after seeing this window's results:
  * window: January 2014 to July 2026 inclusive, both bounds enforced explicitly;
  * months the workbook marks as estimated (cells carrying '*' notes: August and September 2026) are excluded, and no
    estimated month may fall inside the window;
  * benchmark: Ken French's Mkt-RF; down months are those with Mkt-RF < 0; index excess return = index - RF;
  * statistics exactly as in global_macro_down_months_test.py (mean with IID t, correlation with Fisher-z interval,
    OLS beta with t interval, Lo's normal-moment IID Sharpe standard error, ten worst benchmark months);
  * pre-set verdict: crisis protection only if the down-month mean is positive with t > 2.
Diagnostics added in this batch (not part of the protocol's verdict): the same statistics on 2022-01..2026-07 from the
workbook, and a month-by-month comparison with the 55 values read from the HTML page in method validation (2026-10-17), to detect
revisions between the two retrievals. The index is computed by BarclayHedge from reporting funds; its constituents and
past values can change (late reporters, new funds, closures), so every figure is as of the retrieval time.
Run: python3 global_macro_down_months_2014_test.py <workbook .xls> <French factors csv>
     (numpy, scipy, xlrd 2.0.1 for the .xls; under 1 s). Writes global_macro_monthly_2014.csv next to this script.
"""
import csv
import hashlib
import math
import os
import sys

import numpy as np
import xlrd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
START, END = (2014, 1), (2026, 7)
WORKBOOK_SHA256 = 'ead890c4274a7cdd7f92e3da23d15dbd0359dd239bf6a3841cddf437853d1097'


def workbook(path):
    """Monthly returns {(y, m): r} and the set of months marked as estimated."""
    sh = xlrd.open_workbook(path).sheet_by_index(0)
    header = sh.row_values(1)
    assert header[1:13] == ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], header
    out, estimated = {}, set()
    for i in range(2, sh.nrows):
        row = sh.row_values(i)
        if not isinstance(row[0], float):
            continue
        y = int(row[0])
        for k in range(12):
            c = row[1 + k]
            if isinstance(c, float):
                out[(y, k + 1)] = c
            elif isinstance(c, str) and c.strip():
                assert '*' in c, (y, k + 1, c)  # any non-numeric cell must be a marked estimate
                estimated.add((y, k + 1))
    return out, estimated


def french(path):
    out = {}
    for line in open(path):
        p = [x.strip() for x in line.split(',')]
        if len(p[0]) == 6 and p[0].isdigit():
            out[(int(p[0][:4]), int(p[0][4:]))] = (float(p[1]) / 100, float(p[4]) / 100)
        elif out and (not p[0] or not p[0].isdigit()):
            break
    return out


def report(label, months, r, mk, rf):
    ex = r - rf
    T = len(r)
    sr = ex.mean() / ex.std(ddof=1)
    print(f'{label}: window {months[0][0]}-{months[0][1]:02d} to {months[-1][0]}-{months[-1][1]:02d}, T = {T} months')
    print(f'  all months: mean {r.mean()*100:+.2f}%/month, vol {r.std(ddof=1)*math.sqrt(12)*100:.2f}%/yr, '
          f'monthly Sharpe (excess) {sr:+.3f} (Lo IID s.e. {math.sqrt((1 + sr**2 / 2) / T):.3f}), '
          f'annualised {sr*math.sqrt(12):+.2f}')
    res = {}
    for name, sel in (('down', mk < 0), ('up', mk >= 0)):
        a, b = r[sel], mk[sel]
        n = len(a)
        tmean = a.mean() / (a.std(ddof=1) / math.sqrt(n))
        rho = np.corrcoef(a, b)[0, 1]
        z = np.arctanh(rho); half = 1.96 / math.sqrt(n - 3)
        lr = stats.linregress(b, a)
        tcrit = stats.t.ppf(0.975, n - 2)
        print(f'  {name:5s} months (n {n}): mean {a.mean()*100:+.4f}% (t {tmean:+.4f}), correlation {rho:+.2f} '
              f'[{math.tanh(z-half):+.2f}, {math.tanh(z+half):+.2f}], beta {lr.slope:+.3f} '
              f'[{lr.slope - tcrit*lr.stderr:+.3f}, {lr.slope + tcrit*lr.stderr:+.3f}]')
        res[name] = (n, a.mean(), tmean)
    worst = np.argsort(mk, kind='stable')[:10]
    print(f'  ten worst benchmark months: benchmark mean {mk[worst].mean()*100:+.2f}%, index mean {r[worst].mean()*100:+.2f}% '
          f'({", ".join(f"{months[i][0]}-{months[i][1]:02d}" for i in sorted(worst))})')
    n, m, t = res['down']
    ok = m > 0 and t > 2
    print(f'  verdict (pre-set rule): crisis protection {"supported" if ok else "not supported"} in this window')
    return res


def main(xls_path, ff_path):
    digest = hashlib.sha256(open(xls_path, 'rb').read()).hexdigest()
    print(f'workbook SHA-256 {digest} ({"matches" if digest == WORKBOOK_SHA256 else "DIFFERS FROM"} the audited snapshot)')
    idx, est = workbook(xls_path)
    ff = french(ff_path)
    print(f'estimated months excluded: {", ".join(f"{y}-{m:02d}" for y, m in sorted(est))}')
    window = [(y, m) for y in range(START[0], END[0] + 1) for m in range(1, 13) if START <= (y, m) <= END]
    missing = [m for m in window if m not in idx or m not in ff]
    assert not [m for m in window if m in est], 'an estimated month falls inside the window'
    assert not missing, f'months missing from the inputs: {missing}'
    rows = [(m, idx[m], ff[m][0], ff[m][1]) for m in window]
    with open(os.path.join(HERE, 'global_macro_monthly_2014.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['month', 'barclay_global_macro', 'mkt_rf', 'rf'])
        for m, r, mk, rf in rows:
            w.writerow([f'{m[0]}-{m[1]:02d}', f'{r:.4f}', f'{mk:.4f}', f'{rf:.4f}'])
    arr = lambda k: np.array([x[k] for x in rows])
    r, mk, rf = arr(1), arr(2), arr(3)
    report('Protocol window (Barclay Global Macro Index workbook, net; French Mkt-RF)', window, r, mk, rf)
    sub = [i for i, m in enumerate(window) if m >= (2022, 1)]
    report('Recent-period comparison from the workbook', [window[i] for i in sub], r[sub], mk[sub], rf[sub])
    page = {}
    for row in csv.DictReader(open(os.path.join(HERE, 'global_macro_monthly.csv'))):
        y, m = row['month'].split('-')
        page[(int(y), int(m))] = float(row['barclay_global_macro'])
    diffs = [(m, page[m], round(idx[m], 4)) for m in sorted(page) if abs(page[m] - round(idx[m], 4)) > 5e-5]
    print(f'revision check against method validation (2026-10-17)\'s page values (55 months, 4 decimals): '
          f'{len(diffs)} months differ' + (': ' + '; '.join(f'{m[0]}-{m[1]:02d} {a:+.4f} -> {b:+.4f}' for m, a, b in diffs) if diffs else ''))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
