"""source verification (2026-10-17): deadline arithmetic behind data:holdings-insider-filing-lags.

13F: 45 calendar days after quarter end (17 CFR 240.13f-1(a)(1)); 13D: five business days after the acquisition
(240.13d-1(a)); Form 4: before the end of the second business day after execution (15 U.S.C. 78p(a)(2)(C));
a due date on a Saturday, Sunday or holiday moves to the next business day (240.0-3(a)).
Business days exclude weekends and U.S. federal holidays (5 U.S.C. 6103, observed-day rule), computed here.
Run: uv run python filing-checks.py   (standard library). Exits non-zero on failure.
"""

# standard library imports
import datetime as dt
import sys

fails = []


def same(name, got, want):
    ok = got == want
    print(f"  {'ok ' if ok else 'BAD'} {name}: {got} (want {want})")
    if not ok:
        fails.append(name)


def nth_weekday(y, m, wd, n):
    d = dt.date(y, m, 1)
    d += dt.timedelta((wd - d.weekday()) % 7)
    return d + dt.timedelta(7 * (n - 1))


def last_weekday(y, m, wd):
    d = dt.date(y, m + 1, 1) - dt.timedelta(1) if m < 12 else dt.date(y, 12, 31)
    return d - dt.timedelta((d.weekday() - wd) % 7)


def observed(d):
    return (
        d - dt.timedelta(1) if d.weekday() == 5 else d + dt.timedelta(1) if d.weekday() == 6 else d
    )


def holidays(y):
    return {
        observed(dt.date(y, 1, 1)),
        nth_weekday(y, 1, 0, 3),
        nth_weekday(y, 2, 0, 3),
        last_weekday(y, 5, 0),
        observed(dt.date(y, 6, 19)),
        observed(dt.date(y, 7, 4)),
        nth_weekday(y, 9, 0, 1),
        nth_weekday(y, 10, 0, 2),
        observed(dt.date(y, 11, 11)),
        nth_weekday(y, 11, 3, 4),
        observed(dt.date(y, 12, 25)),
    }


def is_bd(d):
    return d.weekday() < 5 and d not in holidays(d.year)


def roll(d):
    while not is_bd(d):
        d += dt.timedelta(1)
    return d


def add_bd(d, n):
    while n:
        d += dt.timedelta(1)
        if is_bd(d):
            n -= 1
    return d


same("Thanksgiving 2026", nth_weekday(2026, 11, 3, 4), dt.date(2026, 11, 26))
same("Veterans Day 2026 is a Wednesday holiday", dt.date(2026, 11, 11) in holidays(2026), True)
raw = dt.date(2026, 9, 30) + dt.timedelta(45)
same("13F raw due date for Q3 2026", raw, dt.date(2026, 11, 14))
same("13F raw due date is a Saturday", raw.weekday(), 5)
same("13F due after roll (Rule 0-3)", roll(raw), dt.date(2026, 11, 16))
same(
    "Form 4 for a trade on Fri 20 Nov 2026", add_bd(dt.date(2026, 11, 20), 2), dt.date(2026, 11, 24)
)
same(
    "13D for an acquisition on Mon 23 Nov 2026",
    add_bd(dt.date(2026, 11, 23), 5),
    dt.date(2026, 12, 1),
)
same(
    "Form 4 latest under deemed execution (3 + 2 business days) from Fri 20 Nov",
    add_bd(dt.date(2026, 11, 20), 5),
    dt.date(2026, 11, 30),
)
if fails:
    print("\nFAILED:", fails)
    sys.exit(1)
print("\nall checks passed")
