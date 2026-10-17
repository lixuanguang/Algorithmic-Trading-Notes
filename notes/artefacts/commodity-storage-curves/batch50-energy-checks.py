"""Batch of 17 October 2026 (audit repair): focused checks for the failures found in backwardation_test.py v1.

Each check targets one audit finding, on a synthetic trading calendar or on the rebuilt outputs:
1. Contract identity: NYMEX expiries on a synthetic 2024 calendar (Good Friday, 29 March, closed): CL April 2024
   (CLJ24) 20 March, CL May (CLK24) 22 April, NG April (NGJ24) 26 March; 28 March's C2 (June WTI) is not 5 April's
   C1 (May WTI), the pairing v1 used.
2. Complete holding periods: a calendar ending on 5 April has no complete April, so 28 March has no next month-end.
3. Report availability: a gas report for the week ending Friday F is not usable on Wednesday F+5 (v1's five-day
   rule admitted it) or Thursday F+6, and is on Friday F+7; crude is usable on F+6; Christmas weeks wait 11 days.
4. Samples: the rebuilt panel has gas months before 2015 (price-only) with no inventory value, and the results
   report a gas out-of-sample test (v1 could not).
5. Wording: the results no longer say months were "dropped"; they say they are retained.
6. Execution: the panel's executable return differs from the settlement-to-settlement return, and v1's outputs
   are kept unchanged in v1-2026-10-17/.
Run: python3 batch50-energy-checks.py   (numpy; reads files next to it; under 1 s). Exits non-zero on failure.
"""
import csv
import datetime as dt
import hashlib
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('bt', os.path.join(HERE, 'backwardation_test.py'))
bt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bt)
fails = []


def same(name, got, want):
    ok = got == want
    print(f"  {'ok ' if ok else 'BAD'} {name}: {got} (want {want})")
    if not ok:
        fails.append(name)


d = dt.date
cal = [d(2024, 1, 2) + dt.timedelta(days=k) for k in range(130)]
cal = [x for x in cal if x.weekday() < 5 and x not in {d(2024, 1, 15), d(2024, 2, 19), d(2024, 3, 29)}]
print('== 1. contract identity on a synthetic 2024 calendar')
same('CLJ24 last trading day', bt.expiry('WTI', cal, 2024, 4), d(2024, 3, 20))
same('CLK24 last trading day', bt.expiry('WTI', cal, 2024, 5), d(2024, 4, 22))
same('NGJ24 last trading day', bt.expiry('NG', cal, 2024, 4), d(2024, 3, 26))
same('WTI C2 on 28 March 2024', bt.delivery('WTI', cal, d(2024, 3, 28), 2), (2024, 6))
same('WTI C1 on 5 April 2024', bt.delivery('WTI', cal, d(2024, 4, 5), 1), (2024, 5))
same('v1 pairing (28 Mar C2, 5 Apr C1) is not the same contract', bt.same_contract('WTI', cal, d(2024, 3, 28), 2, d(2024, 4, 5), 1), False)
same('29 Feb C2 is 28 Mar C1 (WTI)', bt.same_contract('WTI', cal, d(2024, 2, 29), 2, d(2024, 3, 28), 1), True)

print('== 2. complete holding periods')
short = [x for x in cal if x <= d(2024, 4, 5)]
same('month-ends of a calendar ending 5 April', bt.complete_month_ends(short)[-2:], [d(2024, 2, 29), d(2024, 3, 28)])

print('== 3. report availability')
F = d(2024, 3, 8)  # a Friday week-ending date
weeks = [F - dt.timedelta(days=7 * k) for k in range(3, -1, -1)]
same('gas, Wednesday F+5', bt.available_week('NG', weeks, F + dt.timedelta(days=5)), F - dt.timedelta(days=7))
same('gas, Thursday F+6', bt.available_week('NG', weeks, F + dt.timedelta(days=6)), F - dt.timedelta(days=7))
same('gas, Friday F+7', bt.available_week('NG', weeks, F + dt.timedelta(days=7)), F)
same('crude, Thursday F+6', bt.available_week('WTI', weeks, F + dt.timedelta(days=6)), F)
X = d(2025, 12, 19)
wx = [X - dt.timedelta(days=7 * k) for k in range(3, -1, -1)]
same('crude, Christmas week, Wednesday 31 Dec 2025 (F+12)', bt.available_week('WTI', wx, d(2025, 12, 31)), X)
same('crude, Christmas week, Monday 29 Dec 2025 (F+10)', bt.available_week('WTI', wx, d(2025, 12, 29)), X - dt.timedelta(days=7))

print('== 4-6. rebuilt outputs')
rows = list(csv.DictReader(open(os.path.join(HERE, 'backwardation_monthly.csv'))))
ng_early = [r for r in rows if r['market'] == 'NG' and r['month_end'] < '2015-01-01']
same('gas price-only months before 2015 present', len(ng_early) > 200, True)
same('...with no inventory deviation', all(r['inv_dev'] == '' for r in ng_early), True)
same('no month-end pair reaches into April 2024', max(r['next_month_end'] for r in rows) < '2024-04-01', True)
res = open(os.path.join(HERE, 'backwardation_results.txt')).read()
ng_part = res.split('== NG')[1]
same('gas out-of-sample test reported', 'P OOS (price-only, from month 121): R^2' in ng_part, True)
same('no "dropped" wording', 'dropped' in res, False)
same('"retained" wording', 'retained in every estimate' in res, True)
same('executable return differs from settlement return somewhere',
     any(r['r_exec_next_day'] != r['r_next_settle'] for r in rows if r['r_exec_next_day']), True)
v1 = open(os.path.join(HERE, 'v1-2026-10-17', 'backwardation_monthly.csv'), 'rb').read()
same('v1 panel preserved (SHA-256 prefix)', hashlib.sha256(v1).hexdigest()[:8], '6953ecd1')

if fails:
    print('\nFAILED:', fails)
    sys.exit(1)
print('\nall checks passed')
