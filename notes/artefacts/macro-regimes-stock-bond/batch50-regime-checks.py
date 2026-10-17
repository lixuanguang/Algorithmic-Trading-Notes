"""Batch of 17 October 2026 (audit repair): focused checks for the findings on regime_recession_test.py v1.

1. Window definitions: every ALL-MONTHS quarter is an ANY-OVERLAP quarter, and the counts are 34 and 23.
2. The any-overlap (v1) ex-post results are preserved exactly in the v2 output for the series v1 used.
3. Dollar definitions are kept apart: goods-only changes exist only for windows ending by December 2019, goods-and-
   services changes only for windows starting from January 2006; the v1 splice is reported separately.
4. Real-time and ex-post blocks are separate and labelled; the decision rule is applied to the real-time block.
5. v1's derived panel is preserved.
Run: python3 batch50-regime-checks.py   (standard library; reads files next to it). Exits non-zero on failure.
"""
import csv
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
fails = []


def same(name, got, want):
    ok = got == want
    print(f"  {'ok ' if ok else 'BAD'} {name}: {got} (want {want})")
    if not ok:
        fails.append(name)


rows = list(csv.DictReader(open(os.path.join(HERE, 'regime_quarters.csv'))))
same('all-months subset of any-overlap', all(r['nber_any_overlap'] == '1' for r in rows if r['nber_all_months'] == '1'), True)
same('any-overlap count', sum(r['nber_any_overlap'] == '1' for r in rows), 34)
same('all-months count', sum(r['nber_all_months'] == '1' for r in rows), 23)


def add3(ym):
    y, m = map(int, ym.split('-'))
    n = y * 12 + m - 1 + 3
    return f'{n // 12}-{n % 12 + 1:02d}'


same('goods-only only for windows ending by 2019-12', all(add3(r['vintage_month']) <= '2019-12' for r in rows if r['usd_goods_only']), True)
same('goods-and-services only from 2006-01', all(r['vintage_month'] >= '2006-01' for r in rows if r['usd_goods_services']), True)

v1 = open(os.path.join(HERE, 'v1-2026-10-17', 'regime_recession_results.txt')).read()
v2 = open(os.path.join(HERE, 'regime_recession_results.txt')).read()
v1_block = v1.split('== ex-post NBER window')[1]
v2_block = v2.split('ANY OVERLAP (v1 definition)')[1].split('== ex-post NBER window, ALL MONTHS')[0]
for k in ('dy10', 'dcred', 'eq', 'dfn'):
    a = re.search(rf'{k}\s*: regime ([+-][0-9.]+).*diff ([+-][0-9.]+), t ([+-][0-9.]+)', v1_block).groups()
    b = re.search(rf'\n  {k}\s+[0-9-]+: regime ([+-][0-9.]+).*diff ([+-][0-9.]+), Welch t ([+-][0-9.]+)', v2_block).groups()
    same(f'v1 any-overlap result preserved for {k}', b, a)
a = re.search(r'usd\s*: regime ([+-][0-9.]+).*diff ([+-][0-9.]+), t ([+-][0-9.]+)', v1_block).groups()
b = re.search(r'usd \(v1 splice[^)]*\)\s+[0-9-]+: regime ([+-][0-9.]+).*diff ([+-][0-9.]+), Welch t ([+-][0-9.]+)', v2_block).groups()
same('v1 any-overlap dollar (splice) preserved', b, a)
same('real-time block precedes and is labelled the only test', v2.index('REAL-TIME TEST') < v2.index('EX-POST DESCRIPTION'), True)
same('verdict line refers to real time', 'Verdict (real time)' in v2, True)
p1 = open(os.path.join(HERE, 'v1-2026-10-17', 'regime_quarters.csv'), 'rb').read()
same('v1 panel preserved (SHA-256 prefix)', hashlib.sha256(p1).hexdigest()[:8], '82ce2b97')

if fails:
    print('\nFAILED:', fails)
    sys.exit(1)
print('\nall checks passed')
