"""Batch of 17 October 2026 (audit repair): the separate timestamps of an EDGAR filing, behind
data:holdings-insider-filing-lags.

Rule checked (17 CFR 232.13(a)(2) and (a)(4), eCFR text for 15 October 2026; business days per 232.12): a direct
transmission commencing by 5:30 p.m. Eastern on a business day is deemed filed that day, later ones the next business
day; Forms 3, 4, 5, 144, Schedules 13D, 13G and 14N (and their amendments) are deemed filed the same day up to 10 p.m.
So the official filing date can differ from the calendar date of acceptance, and neither is the time the filing was
public or the time a user first saw it.

Corrected 2026-10-17 (third batch). The first version's fallback, "the start of the next business day after the
acceptance time", was not conservative: EDGAR's page "Determine the Status of My Filing" (dated June 4, 2024, last
reviewed Oct. 31, 2024; read from the Wayback Machine capture of 5 October 2026 because sec.gov refused the script)
says most submissions that begin transmission after 5:30 p.m. "will receive a filing date of 6:00 a.m. ET the next
business day and will not be disseminated by EDGAR until the next business day". So such a filing cannot be public at
00:00, and the page gives no time on that day by which it will be. No text read bounds dissemination from above.
The panel therefore keeps two quantities:
  available_at(rec)   = recorded dissemination time, else recorded first-observed time, else None (unknown: the
                        filing does not enter a decision-time panel on this record alone);
  not_before(rec)     = a lower bound only (acceptance time; for an after-cutoff submission whose form is not on the
                        page's same-day list, 06:00 on the next business day). Using a filing before this bound is
                        certain look-ahead; using it after the bound is not thereby safe.
Schedules 13D, 13G and 14N are deemed filed the same day up to 10 p.m. under 232.13(a)(4), but the page's same-day
dissemination list (3, 4, 5, 144 and their amendments, and MEF/POS 462B forms) does not include them; their lower
bound is therefore the acceptance time only.
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


SAME_DAY_DISSEMINATION = {'3', '4', '5', '144'}  # page list, with /A amendments; MEF and POS 462B forms omitted here


def available_at(rec):
    """Recorded availability, or None when no dissemination or first-observed time was recorded."""
    for key in ('disseminated', 'first_observed'):
        if rec.get(key):
            return rec[key]
    return None


def not_before(rec):
    """Lower bound on public availability; never a substitute for available_at."""
    acc = rec['accepted']
    base = rec['form'].split('/')[0]
    if acc.time() > dt.time(17, 30) and base not in SAME_DAY_DISSEMINATION and base not in LATE_FORMS:
        return dt.datetime.combine(next_business_day(acc.date()), dt.time(6, 0))
    return acc


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
same('original without a recorded time: availability unknown, not midnight', available_at(orig), None)
same('original lower bound: 06:00 on the next business day', not_before(orig), T(2026, 11, 17, 6, 0))
same('the old midnight fallback is before the lower bound (look-ahead)',
     dt.datetime.combine(next_business_day(orig['accepted'].date()), dt.time(0, 0)) < not_before(orig), True)
same('released positions available at their own first-observed time', available_at(conf), T(2027, 9, 14, 9, 40))
same('the release does not back-date the original period', conf['period'] == orig['period'] and available_at(conf) > not_before(orig), True)
# after the cutoff before a holiday: 10-Q begun 18:10 on Wed 25 Nov 2026 -> filing date and lower bound Fri 27 Nov 06:00
tenq = {'form': '10-Q', 'accepted': T(2026, 11, 25, 18, 10)}
same('10-Q after cutoff before Thanksgiving: filing date Fri 27 Nov', filing_date('10-Q', tenq['accepted']), dt.date(2026, 11, 27))
same('10-Q after cutoff before Thanksgiving: not before Fri 27 Nov 06:00', not_before(tenq), T(2026, 11, 27, 6, 0))
same('10-Q without recorded times stays unknown', available_at(tenq), None)
# Form 4 after 5:30 is on the page's same-day list: lower bound is acceptance, availability still needs a record
f4 = {'form': '4', 'accepted': T(2026, 11, 19, 21, 30), 'disseminated': T(2026, 11, 19, 21, 31)}
same('Form 4 at 21:30: lower bound is acceptance', not_before(f4), f4['accepted'])
same('Form 4 at 21:30: recorded dissemination is used', available_at(f4), T(2026, 11, 19, 21, 31))
# Schedule 13D/A after 5:30: filed same day under 232.13(a)(4); the page does not list it for same-day dissemination
d13 = {'form': 'SC 13D/A', 'accepted': T(2026, 11, 19, 19, 0)}
same('SC 13D/A at 19:00: filed the same day', filing_date(d13['form'], d13['accepted']), dt.date(2026, 11, 19))
same('SC 13D/A at 19:00: lower bound is acceptance only', not_before(d13), d13['accepted'])
# a recorded first observation earlier than the lower bound would be a data error, flagged rather than used
bad = {'form': '10-K', 'accepted': T(2026, 11, 19, 18, 0), 'first_observed': T(2026, 11, 19, 23, 0)}
same('first-observed before the lower bound is flagged', available_at(bad) < not_before(bad), True)
if fails:
    print('\nFAILED:', fails)
    sys.exit(1)
print('\nall checks passed')
