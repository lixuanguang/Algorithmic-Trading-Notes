"""U.S. calendar rules: weekday arithmetic, federal holidays and business days, and Easter."""

import datetime as dt
from collections.abc import Container


def nth_weekday(year: int, month: int, weekday: int, n: int) -> dt.date:
    """Return the n-th weekday (Monday 0 to Sunday 6) of a month."""
    d = dt.date(year, month, 1)
    d += dt.timedelta(days=(weekday - d.weekday()) % 7)
    return d + dt.timedelta(weeks=n - 1)


def last_weekday(year: int, month: int, weekday: int) -> dt.date:
    """Return the last weekday (Monday 0 to Sunday 6) of a month."""
    d = dt.date(year + (month == 12), month % 12 + 1, 1) - dt.timedelta(days=1)
    return d - dt.timedelta(days=(d.weekday() - weekday) % 7)


def observed(d: dt.date) -> dt.date:
    """Return the observed day of a fixed-date holiday: Saturday to Friday, Sunday to Monday."""
    if d.weekday() == 5:
        return d - dt.timedelta(days=1)
    if d.weekday() == 6:
        return d + dt.timedelta(days=1)
    return d


def federal_holidays(year: int) -> set[dt.date]:
    """Return the observed days of the eleven 5 U.S.C. 6103 holidays of a year."""
    return {
        observed(dt.date(year, 1, 1)),
        nth_weekday(year, 1, 0, 3),
        nth_weekday(year, 2, 0, 3),
        last_weekday(year, 5, 0),
        observed(dt.date(year, 6, 19)),
        observed(dt.date(year, 7, 4)),
        nth_weekday(year, 9, 0, 1),
        nth_weekday(year, 10, 0, 2),
        observed(dt.date(year, 11, 11)),
        nth_weekday(year, 11, 3, 4),
        observed(dt.date(year, 12, 25)),
    }


def is_business_day(d: dt.date) -> bool:
    """Return whether d is a weekday that is not a federal holiday of its own year."""
    return d.weekday() < 5 and d not in federal_holidays(d.year)


def rolled_forward(d: dt.date) -> dt.date:
    """Return d if it is a business day, else the next business day."""
    while not is_business_day(d):
        d += dt.timedelta(days=1)
    return d


def add_business_days(d: dt.date, n: int) -> dt.date:
    """Return the n-th business day after d, for n >= 0; d itself is not counted."""
    while n:
        d += dt.timedelta(days=1)
        if is_business_day(d):
            n -= 1
    return d


def easter(year: int) -> dt.date:
    """Return Easter Sunday of a year (Meeus/Jones/Butcher Gregorian algorithm)."""
    a, b, c = year % 19, year // 100, year % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    ell = (32 + 2 * e + 2 * i - h - k) % 7  # l in the algorithm
    m = (a + 11 * h + 22 * ell) // 451
    n = h + ell - 7 * m + 114
    return dt.date(year, n // 31, n % 31 + 1)


def business_day(year: int, month: int, n: int, skip: Container[dt.date]) -> int:
    """Return the day of the month of its n-th weekday that is not in skip."""
    d, count = dt.date(year, month, 1), 0
    while True:
        if d.weekday() < 5 and d not in skip:
            count += 1
            if count == n:
                return d.day
        d += dt.timedelta(days=1)
