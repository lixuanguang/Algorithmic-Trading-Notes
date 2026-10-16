"""Second source follow-up of slices 33-37 (2026-10-16): arithmetic behind figures added from rulebooks and data releases.

1. Tick values of the CBOT Treasury futures as the current chapters state them (Chapters 18-21 and 40, Rules xx102.B-C):
   face value x tick in points / 100, against Gliner's 2013-2014 ticks; only the 2-year differs.
2. Tick values of the NYMEX, COMEX and CBOT contracts read (Chapters 200, 220, 107, 111-113, 10, 11 and 14):
   contract unit x minimum fluctuation.
3. Copper end-use groupings: the ICA 2023 dataset (World sheet, 2022, copper content of semis; market shares in row 50,
   group shares in row 51) and the ICSG World Copper Factbook 2025 chart (2024, p. 48), grouped as building
   construction, infrastructure and equipment manufacture, against Gliner's 33/15/52; and the sum of the aluminium demand
   shares named by the IAI/MPP strategy (pp. 15 and 26).
4. EIA's OPEC shares (Today in Energy, 23 June 2026): world output implied by 28.0 million b/d at 35 percent, and the share
   without the UAE's 3.4 million b/d.
5. The ISM rule (Manufacturing on the first and Services on the third business day of the month) against ISM's 2026
   calendar, with business days counted against U.S. federal holidays computed from their statutory rules (5 U.S.C. 6103,
   Saturday holidays observed on Friday). The rule reproduces every listed date except January (ISM states its own holiday
   on 2 January) and Services in April (6 April; Good Friday, 3 April 2026, is not a federal holiday, so ISM evidently
   skips it too: an inference, not stated on the calendar).
Run: python3 source-followup-checks-2.py   (standard library only). Exits non-zero on failure.
"""
import datetime as dt
import sys

fails = []


def check(name, got, want, tol=1e-9):
    ok = abs(got - want) <= tol
    print(f"  {'ok ' if ok else 'BAD'} {name}: {got:.6f} (want {want}, tol {tol})")
    if not ok:
        fails.append(name)


def same(name, got, want):
    ok = got == want
    print(f"  {'ok ' if ok else 'BAD'} {name}: {got} (want {want})")
    if not ok:
        fails.append(name)


def head(t):
    print('\n== ' + t)


head('1. CBOT Treasury futures tick values (current chapters)')
treasury = {  # face value, minimum fluctuation in points (outrights)
    'TU 2-year (Ch. 21)': (200_000, 1 / 32 / 8, 7.8125),
    'FV 5-year (Ch. 20)': (100_000, 1 / 32 / 4, 7.8125),
    'TY/ZN 10-year (Ch. 19)': (100_000, 1 / 32 / 2, 15.625),
    'US bond (Ch. 18)': (100_000, 1 / 32, 31.25),
    'UB ultra bond (Ch. 40)': (100_000, 1 / 32, 31.25),
}
for name, (face, tick, stated) in treasury.items():
    check(name, face * tick / 100, stated)
check('TU at Gliner\'s quarter of a 32nd', 200_000 * (1 / 32 / 4) / 100, 15.625)
check('TU current tick / Gliner\'s', (1 / 32 / 8) / (1 / 32 / 4), 0.5)

head('2. Commodity tick values')
commodity = {  # contract unit, minimum fluctuation per unit, dollars per contract
    'CL 1,000 bbl x $0.01': (1_000, 0.01, 10.0),
    'NG 10,000 MMBtu x $0.001': (10_000, 0.001, 10.0),
    'NG spreads x $0.00025': (10_000, 0.00025, 2.5),
    'HG 25,000 lb x $0.0005': (25_000, 0.0005, 12.5),
    'SI 5,000 oz x $0.005 outright': (5_000, 0.005, 25.0),
    'SI 5,000 oz x $0.001 spread': (5_000, 0.001, 5.0),
    'GC 100 oz x $0.10': (100, 0.10, 10.0),
    'COMEX aluminium 25 t x $0.25': (25, 0.25, 6.25),
    'CBOT grains 5,000 bu x $0.0025': (5_000, 0.0025, 12.5),
}
for name, (unit, tick, stated) in commodity.items():
    check(name, unit * tick, stated)
check('CL delivery tolerance, barrels at +2%', 1_000 * 1.02, 1_020)

head('3. Copper end-use groupings and aluminium shares')
ica_market = [4.2083793015276552, 0.76511760889195024, 0.94861350411016909, 0.79479482170798033,
              19.497719024914005, 14.583362908716403, 2.7216005691841221, 6.007597156799795,
              5.5101284837715587, 7.4870418064821722, 0.86976542572695381, 4.5753255198324805,
              8.8742914720268331, 7.8847039039644278, 5.75899235199625, 9.5125661403472481]
check('ICA market shares sum', sum(ica_market), 100.0, 1e-9)
building, infra = sum(ica_market[0:5]), sum(ica_market[5:7])
industrial, transport, other = sum(ica_market[7:9]), sum(ica_market[9:12]), sum(ica_market[12:16])
check('ICA building construction (row 51)', building, 26.214624261151759, 1e-9)
check('ICA infrastructure (row 51)', infra, 17.304963477900525, 1e-9)
check('ICA industrial (row 51)', industrial, 11.517725640571353, 1e-9)
check('ICA transport (row 51)', transport, 12.932132752041607, 1e-9)
check('ICA other equipment (row 51)', other, 32.030553868334756, 1e-9)
check('ICA equipment manufacture', industrial + transport + other, 56.48, 0.005)
icsg = {'building': 26, 'infrastructure': 17, 'transport': 13, 'industrial': 12, 'consumer etc.': 23, 'others': 9}
check('ICSG 2024 end-use sum', sum(icsg.values()), 100)
check('ICSG 2024 equipment manufacture', icsg['transport'] + icsg['industrial'] + icsg['consumer etc.'] + icsg['others'], 57)
check('Gliner 52/33/15 sum', 52 + 33 + 15, 100)
check('IAI named aluminium shares sum', 26 + 24 + 11 + 11 + 8 + 8 + 6, 94)

head('4. EIA OPEC shares, 2025')
world = 28.0 / 0.35
check('world crude output implied, million b/d', world, 80.0, 1e-9)
check('OPEC share without the UAE, percent', 100 * (28.0 - 3.4) / world, 30.75, 1e-9)
same('rounds to EIA\'s 31 percent', round(100 * (28.0 - 3.4) / world), 31)


head('5. ISM 2026 release dates against the first and third business days')


def nth_weekday(year, month, weekday, n):
    d = dt.date(year, month, 1)
    d += dt.timedelta(days=(weekday - d.weekday()) % 7)
    return d + dt.timedelta(weeks=n - 1)


def last_weekday(year, month, weekday):
    d = dt.date(year, month + 1, 1) - dt.timedelta(days=1)
    return d - dt.timedelta(days=(d.weekday() - weekday) % 7)


def observed(d):
    return d - dt.timedelta(days=1) if d.weekday() == 5 else d + dt.timedelta(days=1) if d.weekday() == 6 else d


def federal_holidays(y):
    return {observed(dt.date(y, 1, 1)), nth_weekday(y, 1, 0, 3), nth_weekday(y, 2, 0, 3), last_weekday(y, 5, 0),
            observed(dt.date(y, 6, 19)), observed(dt.date(y, 7, 4)), nth_weekday(y, 9, 0, 1), nth_weekday(y, 10, 0, 2),
            observed(dt.date(y, 11, 11)), nth_weekday(y, 11, 3, 4), observed(dt.date(y, 12, 25))}


def easter(y):  # Meeus/Jones/Butcher Gregorian algorithm
    a, b, c = y % 19, y // 100, y % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    n = h + l - 7 * m + 114
    return dt.date(y, n // 31, n % 31 + 1)


def business_day(y, month, n, skip):
    d, count = dt.date(y, month, 1), 0
    while True:
        if d.weekday() < 5 and d not in skip:
            count += 1
            if count == n:
                return d.day
        d += dt.timedelta(days=1)


hol = federal_holidays(2026)
same('Easter 2024, 2025 (known dates)', [easter(2024), easter(2025)], [dt.date(2024, 3, 31), dt.date(2025, 4, 20)])
same('July 4, 2026 observed on Friday 3 July', observed(dt.date(2026, 7, 4)), dt.date(2026, 7, 3))
same('Good Friday 2026', easter(2026) - dt.timedelta(days=2), dt.date(2026, 4, 3))
ism = {1: (5, 7), 2: (2, 4), 3: (2, 4), 4: (1, 6), 5: (1, 5), 6: (1, 3), 7: (1, 6), 8: (3, 5), 9: (1, 3),
       10: (1, 5), 11: (2, 4), 12: (1, 3)}
mismatch = []
for month, (mfg, svc) in ism.items():
    rule = (business_day(2026, month, 1, hol), business_day(2026, month, 3, hol))
    if rule != (mfg, svc):
        mismatch.append((month, rule, (mfg, svc)))
print('  federal-holiday rule vs ISM (month, rule, ISM):', mismatch)
same('months where the plain rule differs', [m[0] for m in mismatch], [1, 4])
extra = hol | {dt.date(2026, 1, 2), easter(2026) - dt.timedelta(days=2)}
same('all twelve months with ISM\'s 2 January and Good Friday skipped',
     all((business_day(2026, m, 1, extra), business_day(2026, m, 3, extra)) == v for m, v in ism.items()), True)

if fails:
    print('\nFAILED:', fails)
    sys.exit(1)
print('\nall checks passed')
