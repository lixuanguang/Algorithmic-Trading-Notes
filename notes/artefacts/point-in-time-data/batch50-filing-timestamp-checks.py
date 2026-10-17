"""Batch of 17 October 2026 (audit repair): the separate timestamps of an EDGAR filing, behind
data:holdings-insider-filing-lags.

Rule checked (17 CFR 232.13(a)(2) and (a)(4), eCFR text for 15 October 2026; business days per 232.12): a direct
transmission commencing by 5:30 p.m. Eastern on a business day is deemed filed that day, later ones the next business
day; Forms 3, 4, 5, 144, Schedules 13D, 13G and 14N (and their amendments) are deemed filed the same day up to 10 p.m.
So the official filing date can differ from the calendar date of acceptance, and neither is the time the filing was
public or the time a user first saw it. The panel's availability time is an own convention, not an SEC guarantee:
  available_at = first_observed if recorded, else the start of the next business day after the acceptance time
(conservative: no fixed delay after acceptance is assumed).
Synthetic records only; no SEC data are used. Run: python3 batch50-filing-timestamp-checks.py (standard library).
"""
import datetime as dt
import sys

fails = []
LATE_FORMS = {'3', '4', '5', '144', 'SC 13D', 'SC 13G', 'SC 14N'}
HOLIDAYS_2026 = {dt.date(2026, 11, 11), dt.date(2026, 11, 26), dt.date(2026, 12, 25)}  # 5 U.S.C. 6103, Nov-Dec 2026


def same(name, got, want):
    ok = got == want
    print(f"  {'ok ' if ok else 'BAD'} {name}: {got} (want {want})")
    if not ok:
        fails.append(name)


def business_day(d):
    return d.weekday() < 5 and d not in HOLIDAYS_2026


def next_business_day(d):
    d += dt.timedelta(days=1)
    while not business_day(d):
        d += dt.timedelta(days=1)
    return d


def filing_date(form, start_et):
    """Deemed filing date for a direct transmission commencing at start_et (Eastern, naive)."""
    d = start_et.date()
    if not business_day(d):
        return next_business_day(d)
    base = form.split('/')[0]
    cutoff = dt.time(22, 0) if base in LATE_FORMS else dt.time(17, 30)
    return d if start_et.time() <= cutoff else next_business_day(d)


def available_at(rec):
    if rec.get('first_observed'):
        return rec['first_observed']
    return dt.datetime.combine(next_business_day(rec['accepted'].date()), dt.time(0, 0))


T = dt.datetime
same('10-K starting 18:00 on Thu 19 Nov 2026 is filed Fri 20 Nov', filing_date('10-K', T(2026, 11, 19, 18, 0)), dt.date(2026, 11, 20))
same('Form 4 starting 21:30 on Thu 19 Nov 2026 is filed the same day', filing_date('4', T(2026, 11, 19, 21, 30)), dt.date(2026, 11, 19))
same('SC 13D/A starting 22:01 on Wed 25 Nov 2026 is filed Fri 27 Nov (Thanksgiving)', filing_date('SC 13D/A', T(2026, 11, 25, 22, 1)), dt.date(2026, 11, 27))
same('13F-HR starting 17:31 on Mon 16 Nov 2026 is filed Tue 17 Nov', filing_date('13F-HR', T(2026, 11, 16, 17, 31)), dt.date(2026, 11, 17))

# a record carries every timestamp separately; the amendment and the later release are separate records
orig = {'form': '13F-HR', 'period': dt.date(2026, 9, 30), 'accepted': T(2026, 11, 16, 17, 31), 'first_observed': None}
conf = {'form': '13F-HR/A', 'period': dt.date(2026, 9, 30), 'accepted': T(2027, 9, 14, 9, 5),
        'first_observed': T(2027, 9, 14, 9, 40), 'note': 'positions omitted under confidential treatment, later released'}
same('original filing date differs from its acceptance date', filing_date(orig['form'], orig['accepted']) != orig['accepted'].date(), True)
same('original available from the next business day (no fixed delay assumed)', available_at(orig), T(2026, 11, 17, 0, 0))
same('released positions available at their own first-observed time', available_at(conf), T(2027, 9, 14, 9, 40))
same('the release does not back-date the original period', conf['period'] == orig['period'] and available_at(conf) > available_at(orig), True)
if fails:
    print('\nFAILED:', fails)
    sys.exit(1)
print('\nall checks passed')
