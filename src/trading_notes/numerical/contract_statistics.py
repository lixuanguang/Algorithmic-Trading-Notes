"""Second source follow-up of order books and order flow / macro markets and pricing reviews (2026-10-16): arithmetic behind figures added from rulebooks and data releases.

1. Tick values of the CBOT Treasury futures as the current chapters state them (Chapters 18-21 and 40, Rules xx102.B-C):
   face value x tick in points / 100, against Gliner's 2013-2014 ticks; only the 2-year differs. Added 2026-10-17: the Ultra
   Bond's intermonth-spread tick of a quarter of a 32nd ($7.8125; Rule 40102.C) against its outright 32nd ($31.25).
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
The holiday calendar below serves only check 5, for 2026; it is not shared with other checks.
Run: uv run --frozen --no-editable python -m trading_notes.numerical.contract_statistics   (standard library only).
Exits non-zero on failure.
"""

# standard library imports
import datetime as dt
import sys
from collections.abc import Container, Mapping
from typing import Final

# project library imports
from trading_notes.numerical.report import CheckReport

TREASURY: Final[Mapping[str, tuple[int, float, float]]] = {
    # face value, minimum fluctuation in points (outrights), stated tick value in dollars
    "TU 2-year (Ch. 21)": (200_000, 1 / 32 / 8, 7.8125),
    "FV 5-year (Ch. 20)": (100_000, 1 / 32 / 4, 7.8125),
    "TY/ZN 10-year (Ch. 19)": (100_000, 1 / 32 / 2, 15.625),
    "US bond (Ch. 18)": (100_000, 1 / 32, 31.25),
    "UB ultra bond (Ch. 40)": (100_000, 1 / 32, 31.25),
}
COMMODITY: Final[Mapping[str, tuple[int, float, float]]] = {
    # contract unit, minimum fluctuation per unit, dollars per contract
    "CL 1,000 bbl x $0.01": (1_000, 0.01, 10.0),
    "NG 10,000 MMBtu x $0.001": (10_000, 0.001, 10.0),
    "NG spreads x $0.00025": (10_000, 0.00025, 2.5),
    "HG 25,000 lb x $0.0005": (25_000, 0.0005, 12.5),
    "SI 5,000 oz x $0.005 outright": (5_000, 0.005, 25.0),
    "SI 5,000 oz x $0.001 spread": (5_000, 0.001, 5.0),
    "GC 100 oz x $0.10": (100, 0.10, 10.0),
    "COMEX aluminium 25 t x $0.25": (25, 0.25, 6.25),
    "CBOT grains 5,000 bu x $0.0025": (5_000, 0.0025, 12.5),
}
# ICA 2023 dataset, World sheet, 2022 market shares (row 50), percent.
ICA_MARKET: Final = (
    4.2083793015276552,
    0.76511760889195024,
    0.94861350411016909,
    0.79479482170798033,
    19.497719024914005,
    14.583362908716403,
    2.7216005691841221,
    6.007597156799795,
    5.5101284837715587,
    7.4870418064821722,
    0.86976542572695381,
    4.5753255198324805,
    8.8742914720268331,
    7.8847039039644278,
    5.75899235199625,
    9.5125661403472481,
)
# ICSG World Copper Factbook 2025, 2024 end-use shares, percent.
ICSG: Final[Mapping[str, int]] = {
    "building": 26,
    "infrastructure": 17,
    "transport": 13,
    "industrial": 12,
    "consumer etc.": 23,
    "others": 9,
}
# ISM's 2026 calendar: month -> (Manufacturing day, Services day).
ISM_2026: Final[Mapping[int, tuple[int, int]]] = {
    1: (5, 7),
    2: (2, 4),
    3: (2, 4),
    4: (1, 6),
    5: (1, 5),
    6: (1, 3),
    7: (1, 6),
    8: (3, 5),
    9: (1, 3),
    10: (1, 5),
    11: (2, 4),
    12: (1, 3),
}


def near(report: CheckReport, name: str, got: float, want: float, tol: float = 1e-9) -> None:
    """Check |got - want| <= tol, printing got to six decimals with want and tol as given."""
    report.ok(name, abs(got - want) <= tol, f"{got:.6f} (want {want}, tol {tol})")


def head(t: str) -> None:
    """Print a section heading after a blank line."""
    print("\n== " + t)


def nth_weekday(year: int, month: int, weekday: int, n: int) -> dt.date:
    """Return the n-th weekday (Monday 0 to Sunday 6) of a month."""
    d = dt.date(year, month, 1)
    d += dt.timedelta(days=(weekday - d.weekday()) % 7)
    return d + dt.timedelta(weeks=n - 1)


def last_weekday(year: int, month: int, weekday: int) -> dt.date:
    """Return the last weekday (Monday 0 to Sunday 6) of a month before December."""
    d = dt.date(year, month + 1, 1) - dt.timedelta(days=1)
    return d - dt.timedelta(days=(d.weekday() - weekday) % 7)


def observed(d: dt.date) -> dt.date:
    """Return the observed day of a fixed-date holiday: Saturday to Friday, Sunday to Monday."""
    return (
        d - dt.timedelta(days=1)
        if d.weekday() == 5
        else d + dt.timedelta(days=1)
        if d.weekday() == 6
        else d
    )


def federal_holidays(y: int) -> set[dt.date]:
    """Return the observed days of the eleven 5 U.S.C. 6103 holidays of year y."""
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


def easter(y: int) -> dt.date:
    """Return Easter Sunday of year y (Meeus/Jones/Butcher Gregorian algorithm)."""
    a, b, c = y % 19, y // 100, y % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    ell = (32 + 2 * e + 2 * i - h - k) % 7  # l in the algorithm
    m = (a + 11 * h + 22 * ell) // 451
    n = h + ell - 7 * m + 114
    return dt.date(y, n // 31, n % 31 + 1)


def business_day(y: int, month: int, n: int, skip: Container[dt.date]) -> int:
    """Return the day of the month of its n-th weekday that is not in skip."""
    d, count = dt.date(y, month, 1), 0
    while True:
        if d.weekday() < 5 and d not in skip:
            count += 1
            if count == n:
                return d.day
        d += dt.timedelta(days=1)


def check_treasury_ticks(report: CheckReport) -> None:
    """Check 1: CBOT Treasury futures tick values against the current chapters."""
    head("1. CBOT Treasury futures tick values (current chapters)")
    for name, (face, tick, stated) in TREASURY.items():
        near(report, name, face * tick / 100, stated)
    near(
        report,
        "UB intermonth spread, a quarter of a 32nd (Rule 40102.C)",
        100_000 * (1 / 32 / 4) / 100,
        7.8125,
    )
    near(report, "UB outright tick / spread tick", (1 / 32) / (1 / 32 / 4), 4.0)
    near(report, "TU at Gliner's quarter of a 32nd", 200_000 * (1 / 32 / 4) / 100, 15.625)
    near(report, "TU current tick / Gliner's", (1 / 32 / 8) / (1 / 32 / 4), 0.5)


def check_commodity_ticks(report: CheckReport) -> None:
    """Check 2: NYMEX, COMEX and CBOT tick values as contract unit x minimum fluctuation."""
    head("2. Commodity tick values")
    for name, (unit, tick, stated) in COMMODITY.items():
        near(report, name, unit * tick, stated)
    near(report, "CL delivery tolerance, barrels at +2%", 1_000 * 1.02, 1_020)


def check_end_use_shares(report: CheckReport) -> None:
    """Check 3: copper end-use groupings and the named aluminium demand shares."""
    head("3. Copper end-use groupings and aluminium shares")
    ica_market = ICA_MARKET
    near(report, "ICA market shares sum", sum(ica_market), 100.0, 1e-9)
    building, infra = sum(ica_market[0:5]), sum(ica_market[5:7])
    industrial, transport, other = (
        sum(ica_market[7:9]),
        sum(ica_market[9:12]),
        sum(ica_market[12:16]),
    )
    near(report, "ICA building construction (row 51)", building, 26.214624261151759, 1e-9)
    near(report, "ICA infrastructure (row 51)", infra, 17.304963477900525, 1e-9)
    near(report, "ICA industrial (row 51)", industrial, 11.517725640571353, 1e-9)
    near(report, "ICA transport (row 51)", transport, 12.932132752041607, 1e-9)
    near(report, "ICA other equipment (row 51)", other, 32.030553868334756, 1e-9)
    near(report, "ICA equipment manufacture", industrial + transport + other, 56.48, 0.005)
    icsg = ICSG
    near(report, "ICSG 2024 end-use sum", sum(icsg.values()), 100)
    near(
        report,
        "ICSG 2024 equipment manufacture",
        icsg["transport"] + icsg["industrial"] + icsg["consumer etc."] + icsg["others"],
        57,
    )
    near(report, "Gliner 52/33/15 sum", 52 + 33 + 15, 100)
    near(report, "IAI named aluminium shares sum", 26 + 24 + 11 + 11 + 8 + 8 + 6, 94)


def check_opec_shares(report: CheckReport) -> None:
    """Check 4: world output implied by OPEC's share, and the share without the UAE."""
    head("4. EIA OPEC shares, 2025")
    world = 28.0 / 0.35
    near(report, "world crude output implied, million b/d", world, 80.0, 1e-9)
    near(report, "OPEC share without the UAE, percent", 100 * (28.0 - 3.4) / world, 30.75, 1e-9)
    report.same("rounds to EIA's 31 percent", round(100 * (28.0 - 3.4) / world), 31)


def check_ism_calendar(report: CheckReport) -> None:
    """Check 5: the first and third business-day rule against ISM's 2026 calendar."""
    head("5. ISM 2026 release dates against the first and third business days")
    hol = federal_holidays(2026)
    report.same(
        "Easter 2024, 2025 (known dates)",
        [easter(2024), easter(2025)],
        [dt.date(2024, 3, 31), dt.date(2025, 4, 20)],
    )
    report.same(
        "July 4, 2026 observed on Friday 3 July", observed(dt.date(2026, 7, 4)), dt.date(2026, 7, 3)
    )
    report.same("Good Friday 2026", easter(2026) - dt.timedelta(days=2), dt.date(2026, 4, 3))
    mismatch: list[tuple[int, tuple[int, int], tuple[int, int]]] = []
    for month, (mfg, svc) in ISM_2026.items():
        rule = (business_day(2026, month, 1, hol), business_day(2026, month, 3, hol))
        if rule != (mfg, svc):
            mismatch.append((month, rule, (mfg, svc)))
    print("  federal-holiday rule vs ISM (month, rule, ISM):", mismatch)
    report.same("months where the plain rule differs", [m[0] for m in mismatch], [1, 4])
    extra = hol | {dt.date(2026, 1, 2), easter(2026) - dt.timedelta(days=2)}
    report.same(
        "all twelve months with ISM's 2 January and Good Friday skipped",
        all(
            (business_day(2026, m, 1, extra), business_day(2026, m, 3, extra)) == v
            for m, v in ISM_2026.items()
        ),
        True,
    )


def main() -> int:
    """Run every check with a fresh report, print the summary and return the exit status (0 or 1)."""
    report = CheckReport()
    check_treasury_ticks(report)
    check_commodity_ticks(report)
    check_end_use_shares(report)
    check_opec_shares(report)
    check_ism_calendar(report)
    if report.failures:
        print("\nFAILED:", report.failures)
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
