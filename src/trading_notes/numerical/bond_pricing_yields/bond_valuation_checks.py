"""Bond valuation and interest-rate risk: the worked numbers of eight bond-measure entries."""

import math
import sys
from collections.abc import Callable, Sequence
from datetime import date, timedelta
from typing import Final, overload

import numpy as np
import scipy
from numpy.typing import NDArray
from scipy.optimize import brentq

from trading_notes.numerical.bond_pricing_yields.fixed_rate_bonds import (
    IndexedFloater,
    LinearZeroCurve,
    convexity,
    days_30_360,
    horizon,
    horizon_return_frac,
    mac_duration,
    price_periodic,
    ytm_from_price,
)
from trading_notes.numerical.bond_pricing_yields.sofr_notes import (
    BusinessCalendar,
    SofrFloatingRateNote,
)
from trading_notes.numerical.report import CheckReport
from trading_notes.numerical.tolerance import close

type Floats = NDArray[np.float64]

# Original: 5% semiannual corporate (30/360), coupons 15 Feb/15 Aug, maturity 15 Feb 2034, trade
# 20 Oct 2026, settlement 21 Oct 2026 (T+1), quoted yield 4.80%.
last_cpn: Final = date(2026, 8, 15)
next_cpn: Final = date(2027, 2, 15)
settle: Final = date(2026, 10, 21)
n0: Final = 15  # Feb 2027 ... Feb 2034
y0: Final = 0.048
# One invented government zero curve, z(t) = 3.60% + 0.08% x t, and a steep one.
GENTLE: Final = LinearZeroCurve(a=0.0360, b=0.0008)
STEEP: Final = LinearZeroCurve(a=0.0250, b=0.0030)
# Handbook Exhibit 4-7: 6-year floater, reference 10%, quoted margin 80 bp s.a., price 99.3098 ->
# discount margin 96 bp.
EXHIBIT_4_7: Final = IndexedFloater(reference=0.10, quoted_margin=0.008, periods=12)


def check_treasury_formulas(report: CheckReport) -> None:
    """Part 1: the Treasury's own formulas (31 CFR 356, Appendix B)."""
    print("== part 1: the Treasury's own formulas (31 CFR 356, Appendix B)")
    # Coupon security, regular first period: P[1 + (r/s)(i/2)] = (C/2)(r/s) + (C/2)a_n + 100 v^n
    C, i, r, s, n = 8.75, 0.0884, 184, 184, 59
    v = 1 / (1 + i / 2)
    a_n = (1 - v**n) / (i / 2)
    P = ((C / 2) * (r / s) + (C / 2) * a_n + 100 * v**n) / (1 + (r / s) * (i / 2))
    report.ok("8 3/4% 30-year bond at 8.84%: P = 99.057893", abs(P - 99.057893) < 5e-7, f"{P:.6f}")
    # Bills
    report.ok(
        "bill at 7.610% discount, 90 days: price 98.097500",
        close(100 * (1 - 0.0761 * 90 / 360), 98.0975, 1e-9),
    )
    d = (100 - 95.934567) / 100 * 360 / 182
    report.ok("26-week bill priced 95.934567: discount rate 8.042%", abs(d - 0.080415158) < 1e-9)
    inv = (100 - 99.559444) / 99.559444 * 365 / 20
    report.ok(
        "20-day bill priced 99.559444: investment rate 8.076% (Treasury rounds an intermediate to"
        " .004425)",
        abs(inv - 0.080756) < 5e-6,
    )
    rr, yy, PP = 364, 365, 92.265
    a_, b_, c_ = rr / (2 * yy) - 0.25, rr / yy, (PP - 100) / PP
    inv52 = (-b_ + math.sqrt(b_ * b_ - 4 * a_ * c_)) / (2 * a_)
    report.ok(
        "52-week bill priced 92.265: investment rate 8.237% (quadratic)",
        abs(inv52 - 0.082373244) < 1e-9,
    )
    # The quadratic is the price identity P[1 + (r - y/2)(i/y)](1 + i/2) = 100 solved for i:
    report.ok(
        "the quadratic root satisfies P[1 + (r - y/2)(i/y)](1 + i/2) = 100",
        close(PP * (1 + (rr - yy / 2) * inv52 / yy) * (1 + inv52 / 2), 100, 1e-9),
    )
    # Treasury FRN index: the 13-week bill's high discount rate converted to a simple 360-day
    # money-market rate.
    p13 = 100 * (1 - 0.00095 * 91 / 360)
    idx = (100 - p13) / p13 * 360 / 91
    report.ok(
        "13-week bill at 0.095% discount -> FRN index 0.095022819% (money-market basis)",
        abs(idx - 0.00095022819) < 5e-12,
    )


def check_pricing_between_coupons(report: CheckReport) -> tuple[float, float, float]:
    """Part 2: pricing on and between coupon dates (Handbook chap. 4)."""
    print("== part 2: pricing on and between coupon dates (Handbook chap. 4)")
    report.ok(
        "9% 20-year at 12%: 774.31 (the Handbook adds rounded parts to 774.30); at 7%: 1,213.55",
        abs(10 * price_periodic(9, 0.12, 40) - 774.3055) < 5e-4,
    )
    report.ok("  (at 7%)", abs(10 * price_periodic(9, 0.07, 40) - 1213.55) < 0.005)
    w = days_30_360(date(2021, 7, 17), date(2021, 9, 1)) / 180
    dirty_h = price_periodic(10, 0.065, 12, w=w)
    ai_h = 5 * (180 - 44) / 180
    report.ok("Illustration 4: 44 days of 30/360, w = 0.24444", abs(w - 0.244444) < 1e-6)
    report.ok(
        "full price 120.0281; accrued 3.7778; clean 116.2503",
        abs(dirty_h - 120.0281) < 5e-5 and abs(ai_h - 3.777778) < 1e-6,
    )
    acc_days = days_30_360(last_cpn, settle)
    w0 = (180 - acc_days) / 180
    full0 = price_periodic(5, y0, n0, w=w0)
    ai0 = 2.5 * acc_days / 180
    clean0 = full0 - ai0
    print(
        f"    5% 2034: accrued days {acc_days}, w {w0:.6f}, full {full0:.4f}, AI {ai0:.6f}, clean"
        f" {clean0:.4f}"
    )
    report.ok(
        "accrued days 66 (30/360), accrued interest 0.916667",
        acc_days == 66 and close(ai0, 0.9166667, 1e-7),
    )
    report.ok(
        "full 102.1316, clean 101.2149 at 4.80%",
        abs(full0 - 102.1316) < 5e-5 and abs(clean0 - 101.2149) < 5e-5,
    )
    report.ok(
        "yield round trip: the full price returns 4.80% exactly",
        abs(brentq(lambda y: price_periodic(5, y, n0, w=w0) - full0, 0, 0.2) - y0) < 1e-12,
    )
    # Treasury-style linear first period (Appendix B form) gives a slightly different full
    # price for the same yield.
    v0 = 1 / (1 + y0 / 2)
    # Appendix B II.D: (P + A)[1 + (r/s)(i/2)] = C/2 + (C/2)a_n + 100 v^n, A = [(s -
    # r)/s](C/2). Its own example first:
    vv = 1 / (1 + 0.0954 / 2)
    ex = (4.75 + 4.75 * (1 - vv**19) / 0.0477 + 100 * vv**19) / (1 + (167 / 181) * 0.0954 / 2) - (
        181 - 167
    ) / 181 * 4.75
    report.ok(
        "Appendix B II.D example: 9 1/2% note at 9.54%, P = 99.730918", abs(ex - 99.730918) < 5e-7
    )
    full_lin = (2.5 + sum(2.5 * v0**k for k in range(1, n0)) + 100 * v0 ** (n0 - 1)) / (
        1 + w0 * y0 / 2
    )
    report.ok(
        "the same 4.80% gives 102.1249 with the stub discounted simply (Treasury formula) against"
        " 102.1316 compounded",
        abs(full_lin - 102.1249) < 5e-5 and abs(full_lin - full0 + 0.006656) < 5e-6,
    )
    # Price-yield-coupon relationships on a coupon date (7-year bonds, yield 4.80%)
    p_prem, p_par, p_disc = (
        price_periodic(6, y0, 14),
        price_periodic(4.8, y0, 14),
        price_periodic(3.6, y0, 14),
    )
    report.ok(
        "coupon above yield -> premium; equal -> par; below -> discount",
        p_prem > 100 and close(p_par, 100, 1e-9) and p_disc < 100,
    )
    path = [price_periodic(6, y0, k) for k in (14, 10, 6, 2)]
    report.ok(
        "at an unchanged yield a premium bond's price falls toward par as it ages",
        all(np.diff(path) < 0) and path[-1] > 100,
    )
    dp = [
        (price_periodic(c, y0 + 0.01, m) / price_periodic(c, y0, m) - 1)
        for c, m in ((4.8, 6), (4.8, 30), (0.0, 30))
    ]
    report.ok(
        "+100 bp: 3-year par bond -2.72%, 15-year par -9.93%, 15-year zero -13.60% (longer and"
        " lower coupon move more)",
        abs(dp[0] + 0.027176) < 5e-6
        and abs(dp[1] + 0.099281) < 5e-6
        and abs(dp[2] + 0.135953) < 5e-6,
    )
    up, dn = price_periodic(4.8, y0 + 0.01, 30), price_periodic(4.8, y0 - 0.01, 30)
    report.ok(
        "convex shape: the gain for -100 bp exceeds the loss for +100 bp", (dn - 100) > (100 - up)
    )
    return w0, full0, clean0


def check_yield_spreads(report: CheckReport, w0: float, full0: float, clean0: float) -> None:
    """Part 3: yield measures and spreads."""
    print("== part 3: yield measures and spreads")
    # Periodicity conversion of a 6.00% semiannual yield
    y_sa = 0.06
    ear = (1 + y_sa / 2) ** 2 - 1
    y_q = 4 * ((1 + y_sa / 2) ** 0.5 - 1)
    y_m = 12 * ((1 + y_sa / 2) ** (1 / 6) - 1)
    y_c = 2 * math.log(1 + y_sa / 2)
    report.ok(
        "6.00% s.a. = 6.0900% annual = 5.9557% quarterly = 5.9263% monthly = 5.9118% continuous",
        abs(ear - 0.0609) < 1e-12
        and abs(y_q - 0.059557) < 5e-7
        and abs(y_m - 0.059263) < 5e-7
        and abs(y_c - 0.059118) < 5e-7,
    )
    cy = 5 / clean0
    report.ok(
        "current yield of the 5% 2034 bond: 4.94% (coupon over clean price)",
        abs(cy - 0.049400) < 5e-6,
    )
    # Callable variant: callable 15 Feb 2029 at 102, 15 Feb 2030 at 101, 15 Feb 2031 onward at
    # 100; quoted at a full price.
    full_call = full0  # same price, to compare yields
    calls = {
        "2029-02-15 @102": (5, 102.0),
        "2030-02-15 @101": (7, 101.0),
        "2031-02-15 @100": (9, 100.0),
    }

    def yield_to(n: int, redemption: float, full: float, c: float = 5.0, ww: float = w0) -> float:
        def f(y: float) -> float:
            cp = c / 2
            value: float = (
                sum(
                    (cp + (redemption if k == n else 0)) / (1 + y / 2) ** (k - 1 + ww)
                    for k in range(1, n + 1)
                )
                - full
            )
            return value

        return brentq(f, -0.5, 1.0)

    ytc = {k: yield_to(m, red, full_call) for k, (m, red) in calls.items()}
    ytm0 = yield_to(n0, 100.0, full_call)
    ytw = min([ytm0, *ytc.values()])
    print(
        "    yields to call:",
        {k: round(100 * v, 4) for k, v in ytc.items()},
        "YTM",
        round(100 * ytm0, 4),
    )
    report.ok(
        "yields to call 5.2558% (2029 at 102), 4.8779% (2030 at 101), 4.6841% (2031 at 100); the"
        " last is the yield to worst",
        abs(ytw - ytc["2031-02-15 @100"]) < 1e-12
        and abs(ytw - 0.046841) < 5e-6
        and abs(ytc["2029-02-15 @102"] - 0.052558) < 5e-6,
    )
    # Spreads for the 5% 2034 bond (about 7.3 years). One invented government zero curve,
    # semiannual compounding, z(t) = 3.60% + 0.08% x t, supplies both the government par
    # yields (for the G-spread) and the zero rates (for the Z-spread); swap (SOFR OIS) par
    # rates 7y 3.80% and 10y 3.95% give the I-spread.
    t_mat = (date(2034, 2, 15) - settle).days / 365.25
    times = np.array([(w0 + k) / 2 for k in range(n0)])
    cfs = np.full(n0, 2.5)
    cfs[-1] += 100

    def spreads(a: float, b: float) -> tuple[float, float, float, float]:
        curve = LinearZeroCurve(a=a, b=b)
        p7, p10 = curve.par_yield(7), curve.par_yield(10)
        g = y0 - float(np.interp(t_mat, [7, 10], [p7, p10]))
        z = brentq(
            lambda zz: (
                float(np.sum(cfs / (1 + (curve.zero(times) + zz) / 2) ** (2 * times))) - full0
            ),
            -0.05,
            0.05,
        )
        return p7, p10, g, z

    par7, par10, g_sp, z_sp = spreads(GENTLE.a, GENTLE.b)
    i_sp = y0 - float(np.interp(t_mat, [7, 10], [0.0380, 0.0395]))
    _, _, g_st, z_st = spreads(STEEP.a, STEEP.b)
    print(
        f"    gentle curve: gov par 7y {100 * par7:.4f}%, 10y {100 * par10:.4f}%; G"
        f" {1e4 * g_sp:.2f} bp, Z {1e4 * z_sp:.2f} bp"
    )
    print(
        f"    steep curve (2.50% + 0.30% x t): G {1e4 * g_st:.2f} bp, Z {1e4 * z_st:.2f} bp; I"
        f" {1e4 * i_sp:.2f} bp"
    )
    report.ok(
        "government par yields from the zero curve 3.60% + 0.08% x t: 7-year 4.1333%, 10-year"
        " 4.3425%",
        abs(par7 - 0.041333) < 5e-6 and abs(par10 - 0.043425) < 5e-6,
    )
    report.ok(
        "G-spread 64.4 bp and Z-spread 65.0 bp: close on a gently sloped curve",
        abs(g_sp - 0.006443) < 5e-6 and abs(z_sp - 0.006497) < 5e-6,
    )
    report.ok(
        "even on a steep curve (2.50% + 0.30% x t) a near-par bullet bond's G- and Z-spreads stay"
        " within 1 bp",
        abs(z_st - g_st) < 1e-4,
    )
    # A zero-coupon bond of the same maturity at the same 4.80% yield: G compares it with a
    # par yield, Z with the zero rate.
    g_zero_st = y0 - float(np.interp(t_mat, [7, 10], [STEEP.par_yield(7), STEEP.par_yield(10)]))
    z_zero_st = y0 - STEEP.zero(t_mat)
    report.ok(
        "a 7.3-year zero at 4.80% on the steep curve: G-spread 23.0 bp but Z-spread 10.4 bp,"
        " because the 7.3-year zero\n      rate (4.70%) exceeds the par yield the G-spread uses",
        abs(g_zero_st - 0.002302) < 5e-6 and abs(z_zero_st - 0.001037) < 5e-6,
        f"G {1e4 * g_zero_st:.2f} bp, Z {1e4 * z_zero_st:.2f} bp",
    )
    report.ok("I-spread over the interpolated swap rate: 98.4 bp", abs(i_sp - 0.009839) < 5e-6)


def check_matrix_pricing(report: CheckReport) -> None:
    """Part 4: matrix pricing (IFRS 13 B7 technique; invented quotes)."""
    print("== part 4: matrix pricing (IFRS 13 B7 technique; invented quotes)")
    # Two traded bonds of the same issuer rating and sector, priced on a coupon date: A 4-year
    # 4.0%, B 6-year 5.0%.
    pa, pb = 98.20, 101.10
    ya, yb = ytm_from_price(pa, 4.0, 8), ytm_from_price(pb, 5.0, 12)
    y5 = 0.5 * (ya + yb)  # linear interpolation in maturity at 5 years
    p_matrix = price_periodic(4.5, y5, 10)
    print(
        f"    yA {100 * ya:.4f}%, yB {100 * yb:.4f}%, interpolated 5y {100 * y5:.4f}%, matrix price"
        f" {p_matrix:.4f}"
    )
    report.ok(
        "comparable yields 4.4967% and 4.7869%; interpolated 5-year yield 4.6418%",
        abs(ya - 0.044967) < 5e-6 and abs(yb - 0.047869) < 5e-6,
    )
    report.ok(
        "the untraded 5-year 4.5% bond is matrix-priced at 99.3737", abs(p_matrix - 99.3737) < 5e-5
    )
    # Spread route: benchmark 5-year government at 3.95%, comparable spreads interpolated ->
    # same idea
    spread5 = 0.5 * ((ya - 0.0388) + (yb - 0.0402))
    report.ok(
        "spread route: 4y and 6y spreads over 3.88% and 4.02% benchmarks average 69.2 bp; 3.95% +"
        " 69.2 bp gives the same 4.6418%",
        abs(0.0395 + spread5 - 0.046418) < 5e-6,
    )


def check_floating_money_market(report: CheckReport) -> None:
    """Part 5: floating-rate and money-market measures."""
    print("== part 5: floating-rate and money-market measures")
    report.ok(
        "Exhibit 4-7: at a 96 bp margin the floater prices at 99.3098",
        abs(EXHIBIT_4_7.price(0.0096) - 99.3098) < 5e-5,
    )
    dm_h = brentq(lambda m: EXHIBIT_4_7.price(m) - 99.3098, -0.05, 0.05)
    report.ok(
        "solving back: discount margin 0.96% (48 bp per half-year)", abs(dm_h - 0.0096) < 5e-6
    )
    report.ok(
        "at par the discount margin equals the quoted margin",
        abs(brentq(lambda m: EXHIBIT_4_7.price(m) - 100, -0.05, 0.05) - 0.008) < 1e-10,
    )

    # Original SOFR FRN, explicit schedule. Issued (and priced) 21 October 2026, matures 21 October
    # 2029; quarterly periods on the 21st of Jan/Apr/Jul/Oct, adjusted modified-following to
    # business days. Coupon: SOFR compounded in arrears over the period with no lookback or
    # observation shift (a simplification; issued notes usually use a 2-5 business-day lookback),
    # plus a 75 bp margin, act/360. Compounding follows the New York Fed's SOFR Averages/Index
    # arithmetic: one term per business day, (1 + SOFR_i n_i/360), n_i the calendar days to the next
    # business day, so a Friday rate applies for 3 days in one simple-interest term. Business days
    # here are weekdays other than the eleven Federal Reserve holidays by rule (Sunday holidays move
    # to Monday; Saturday holidays are not observed), an illustrative calendar: SOFR is not
    # published for days SIFMA recommends a full closure, which can differ. Flat SOFR at 4.10%.
    # Discounting: each period at its projected compounded growth plus the discount margin, simple
    # act/360, so the note is at par on a reset date when the discount margin equals the quoted
    # margin.
    calendar = BusinessCalendar.federal_reserve(range(2026, 2031))
    unadj = [date(2026 + (10 + 3 * k - 1) // 12, (10 + 3 * k - 1) % 12 + 1, 21) for k in range(13)]
    sched = [calendar.modified_following(d0) for d0 in unadj]
    sofr_flat, qm_s = 0.041, 0.0075
    frn = SofrFloatingRateNote.on_schedule(calendar, sched, lambda _d: sofr_flat, qm_s)
    periods = frn.periods
    frn_price = frn.price

    days = [p.days for p in periods]
    report.ok(
        "schedule: 12 periods of 90-94 days, 1,097 in all (maturity rolls to Monday 22 October"
        " 2029); each period's\n      weights n_i sum to its calendar days",
        len(periods) == 12
        and sum(days) == (sched[-1] - sched[0]).days == 1097
        and all(p.weights == p.days for p in periods),
        f"days {days}",
    )
    # Independent accrual: a daily SOFR Index (calendar-day loop, updated on business days by
    # 1 + r n/360) compared with the business-day product; and the New York Fed's published
    # Index example, reproduced from its own rates.
    idx, d0, index_at = 1.0, sched[0], {}
    while d0 <= sched[-1]:
        index_at[d0] = idx
        if calendar.is_business_day(d0):
            nxt = calendar.next_business_day(d0)
            idx *= 1 + sofr_flat * (nxt - d0).days / 360
        d0 += timedelta(1)
    report.ok(
        "coupon accrual: index ratios I(end)/I(start) equal each period's business-day compounding"
        " product",
        all(abs(index_at[p.end] / index_at[p.start] - p.growth) < 1e-14 for p in periods),
    )
    ny_fed = 1.0
    for rr, nn in [(0.018, 1), (0.0183, 1), (0.0174, 1), (0.0175, 1), (0.0175, 3)]:
        ny_fed *= 1 + rr * nn / 360
    report.ok(
        "New York Fed SOFR Index example (2-6 April 2018, Friday rate for 3 days): 1.00034365",
        round(ny_fed, 8) == 1.00034365,
    )
    g1, d1 = periods[0].growth, periods[0].days
    weekend_wrong = (1 + sofr_flat / 360) ** d1
    report.ok(
        "first period (92 days): growth 1.010532, an annualised compounded rate of 4.1211% against"
        " 4.10% simple;\n      compounding weekends as separate daily observations would overstate"
        " it",
        abs(g1 - 1.0105316) < 5e-7
        and abs((g1 - 1) * 360 / d1 - 0.041211) < 5e-6
        and weekend_wrong > g1,
        f"{(g1 - 1) * 360 / d1:.6%}; daily-on-weekends {(weekend_wrong - 1) * 360 / d1:.6%}",
    )
    cpn1 = 100 * (g1 - 1 + qm_s * d1 / 360)
    report.ok(
        "first coupon per 100: compounded SOFR 1.053160 + margin 0.191667 = 1.244827",
        abs(100 * (g1 - 1) - 1.053160) < 5e-7 and abs(cpn1 - 1.244827) < 5e-7,
    )
    report.ok(
        "round trip: at a discount margin equal to the 75 bp quoted margin the FRN prices at"
        " exactly 100 on a reset date",
        abs(frn_price(qm_s) - 100) < 1e-10,
    )
    dm_s = brentq(lambda m: frn_price(m) - 99.40, -0.05, 0.05, xtol=1e-14)
    report.ok(
        "SOFR + 75 bp FRN at 99.40: discount margin 96.38 bp, above the quoted margin because it"
        " trades below par;\n      repricing at that margin returns 99.40",
        abs(dm_s - 0.0096381) < 5e-8 and abs(frn_price(dm_s) - 99.40) < 1e-9,
        f"{1e4 * dm_s:.3f} bp",
    )
    # Independent identity: with this discounting, P = 100 + 100 (qm - dm) sum_k (d_k/360)
    # D_k, the margin annuity.
    dfs_k, dfac = [], 1.0
    for period in periods:
        dfac /= period.growth + dm_s * period.days / 360
        dfs_k.append(dfac)
    ann = sum(d_k / 360 * D_k for d_k, D_k in zip(days, dfs_k, strict=True))
    report.ok(
        "identity: 100 + 100 (0.75% - DM) x margin annuity 2.8062 reproduces 99.40",
        abs(100 + 100 * (qm_s - dm_s) * ann - 99.40) < 1e-9 and abs(ann - 2.8062) < 5e-5,
        f"annuity {ann:.6f}",
    )
    # Money-market yields: a 182-day bill quoted at a 4.00% discount
    pb182 = 100 * (1 - 0.04 * 182 / 360)
    mmy = (100 - pb182) / pb182 * 360 / 182
    bey = (100 - pb182) / pb182 * 365 / 182
    ear_b = (100 / pb182) ** (365 / 182) - 1
    print(
        f"    182-day bill: price {pb182:.6f}, money-market yield {100 * mmy:.4f}%, BEY"
        f" {100 * bey:.4f}%, EAR {100 * ear_b:.4f}%"
    )
    report.ok(
        "price 97.977778; money-market (add-on, 360) 4.0826%; investment rate (365) 4.1393%;"
        " effective annual 4.1822%",
        abs(pb182 - 97.977778) < 5e-7
        and abs(mmy - 0.040826) < 5e-6
        and abs(bey - 0.041393) < 5e-6
        and abs(ear_b - 0.041822) < 5e-6,
    )
    report.ok(
        "ordering for a short bill: discount rate < money-market yield < investment rate",
        0.04 < mmy < bey,
    )
    # Add-on CD: 90-day CD at 4.20% add-on (act/360) pays 100*(1 + 0.042*90/360); quoted on a
    # 365-day basis = 4.2583%
    report.ok(
        "a 4.20% act/360 add-on rate is 4.2583% on a 365-day basis",
        abs(0.042 * 365 / 360 - 0.0425833) < 1e-6,
    )


def check_duration_pvbp(report: CheckReport) -> float:
    """Part 6: duration, PVBP and convexity (yield-based, option-free)."""
    print("== part 6: duration, PVBP and convexity (yield-based, option-free)")
    # 7-year 5% s.a. bond at 4.80% on a coupon date (original example)
    c7, n7 = 5.0, 14
    p7 = price_periodic(c7, y0, n7)
    D_mac = mac_duration(c7, y0, n7)
    D_mod = D_mac / (1 + y0 / 2)
    h = 1e-4
    D_app = (price_periodic(c7, y0 - h, n7) - price_periodic(c7, y0 + h, n7)) / (2 * p7 * h)
    C7 = convexity(c7, y0, n7)
    C_app = (price_periodic(c7, y0 - h, n7) + price_periodic(c7, y0 + h, n7) - 2 * p7) / (
        p7 * h * h
    )
    pvbp = p7 * D_mod * 1e-4
    print(
        f"    7y 5% at 4.80%: price {p7:.4f}, Macaulay {D_mac:.4f}, modified {D_mod:.4f}, convexity"
        f" {C7:.3f}, PVBP {pvbp:.5f}"
    )
    report.ok(
        "price 101.1772; Macaulay 5.9987 years; modified 5.8581",
        abs(p7 - 101.1772) < 5e-5 and abs(D_mac - 5.9987) < 5e-5 and abs(D_mod - 5.8581) < 5e-5,
    )
    report.ok(
        "approximate modified duration from +/-1 bp repricing agrees to 1e-6",
        abs(D_app - D_mod) < 1e-6,
    )
    report.ok(
        "convexity 40.63 analytically and by finite difference",
        abs(C7 - 40.629) < 5e-4 and abs(C_app - C7) < 1e-3,
    )
    report.ok(
        "PVBP 0.0593 per 100 of par; money duration 592.70 per 100 of par per unit of yield",
        abs(pvbp - 0.059270) < 5e-6 and abs(p7 * D_mod - 592.705) < 5e-3,
    )
    report.ok(
        "10 million par: about 592,705 per 100 bp, PVBP 5,927 per basis point",
        abs(p7 / 100 * D_mod * 1e7 * 0.01 - 592705) < 1
        and abs(p7 / 100 * D_mod * 1e7 * 1e-4 - 5927.05) < 0.01,
    )
    for dy, exp_full in ((0.001, -0.5843), (0.01, -5.6689), (0.02, -11.0164), (-0.02, 12.5735)):
        full = price_periodic(c7, y0 + dy, n7) / p7 - 1
        d_only = -D_mod * dy
        d_c = d_only + 0.5 * C7 * dy * dy
        print(
            f"    dy {1e4 * dy:+.0f} bp: full {100 * full:+.4f}%, duration {100 * d_only:+.4f}%,"
            f" +convexity {100 * d_c:+.4f}%"
        )
        if abs(dy) >= 0.01:
            report.ok(
                f"dy {1e4 * dy:+.0f} bp: duration+convexity is closer to full repricing than"
                " duration alone",
                abs(d_c - full) < abs(d_only - full),
            )
    report.ok(
        "full repricing: +200 bp -10.943%, -200 bp +12.572%",
        abs(price_periodic(c7, y0 + 0.02, n7) / p7 - 1 + 0.109431) < 5e-6
        and abs(price_periodic(c7, y0 - 0.02, n7) / p7 - 1 - 0.125717) < 5e-6,
    )
    # Properties: zero-coupon Macaulay = maturity; perpetuity limit; longer maturity and lower
    # coupon -> longer duration.
    report.ok(
        "a zero's Macaulay duration equals its maturity (10 years)",
        close(mac_duration(0.0, y0, 20), 10.0, 1e-12),
    )
    report.ok(
        "duration rises with maturity and falls with coupon and with yield level",
        mac_duration(5, y0, 20) > mac_duration(5, y0, 10)
        and mac_duration(3, y0, 20) > mac_duration(5, y0, 20)
        and mac_duration(5, 0.08, 20) < mac_duration(5, y0, 20),
    )
    # Handbook chap. 5: 5% 20-year at 4%: approximate duration 13.09 (20 bp shocks), convexity
    # measure 112.38 (Eq. 5-4)
    V0, Vm, Vp = (
        price_periodic(5, 0.04, 40),
        price_periodic(5, 0.038, 40),
        price_periodic(5, 0.042, 40),
    )
    report.ok(
        "Handbook prices 113.6777, 116.7049, 110.7527",
        abs(V0 - 113.6777) < 5e-5 and abs(Vm - 116.7049) < 5e-5 and abs(Vp - 110.7527) < 5e-5,
    )
    report.ok(
        "duration (V- - V+)/(2 V0 dy) = 13.09", abs((Vm - Vp) / (2 * V0 * 0.002) - 13.09) < 0.005
    )
    report.ok(
        "convexity measure (V+ + V- - 2V0)/(2 V0 dy^2): 112.38 from the printed 4-decimal prices,"
        " 112.27 from exact prices",
        abs((116.7049 + 110.7527 - 2 * 113.6777) / (2 * 113.6777 * 0.002**2) - 112.38) < 0.005
        and abs((Vm + Vp - 2 * V0) / (2 * V0 * 0.002**2) - 112.273) < 0.005,
    )
    report.ok(
        "PVBP at 3.99% and 4.01%: 0.1489 and 0.1486",
        abs(price_periodic(5, 0.0399, 40) - V0 - 0.1489) < 5e-5
        and abs(V0 - price_periodic(5, 0.0401, 40) - 0.1486) < 5e-5,
    )
    # Handbook portfolio duration 8.81 from market-value weights
    mv = np.array([6122823, 2273555, 2521413.0])
    Dp = np.array([4.147, 13.087, 16.290])
    report.ok("Handbook three-bond portfolio duration 8.81", abs(mv @ Dp / mv.sum() - 8.81) < 0.005)
    return D_mac


def check_portfolio_duration(report: CheckReport) -> None:
    """Part 7: portfolio duration and convexity, original three-bond portfolio."""
    print("== part 7: portfolio duration and convexity, original three-bond portfolio")
    # Holdings (par, coupon %, semiannual periods, yield) on a common coupon date
    hold = [(4e6, 3.0, 4, 0.0420), (3e6, 4.5, 14, 0.0460), (3e6, 5.0, 40, 0.0490)]
    vals_rows: list[float] = []
    mods_rows: list[float] = []
    convs_rows: list[float] = []
    for par, c, m, yy_ in hold:
        pr = price_periodic(c, yy_, m)
        vals_rows.append(par * pr / 100)
        mods_rows.append(mac_duration(c, yy_, m) / (1 + yy_ / 2))
        convs_rows.append(convexity(c, yy_, m))
    vals, mods, convs = map(np.array, (vals_rows, mods_rows, convs_rows))
    wts = vals / vals.sum()
    D_port, C_port = wts @ mods, wts @ convs
    contrib = wts * mods
    print(
        f"    weights {np.round(wts, 4)}, mod durations {np.round(mods, 3)}, D_port {D_port:.4f},"
        f" C_port {C_port:.3f}"
    )
    report.ok(
        "contributions to duration sum to the portfolio duration",
        close(contrib.sum(), D_port, 1e-12),
    )
    report.ok(
        "portfolio modified duration 6.3955 and convexity 79.36 (market-value weights)",
        abs(D_port - 6.3955) < 5e-5 and abs(C_port - 79.360) < 5e-3,
    )

    def port_value(shift_by_bond: Sequence[float]) -> float:
        return sum(
            par * price_periodic(c, yy_ + sh, m) / 100
            for (par, c, m, yy_), sh in zip(hold, shift_by_bond, strict=True)
        )

    V_p0 = vals.sum()
    full_par = port_value([0.005] * 3) / V_p0 - 1
    approx = -D_port * 0.005 + 0.5 * C_port * 0.005**2
    report.ok(
        "equal +50 bp yield changes: weighted duration and convexity match full repricing within 1"
        " bp of value",
        abs(full_par - approx) < 1e-4,
        f"{100 * full_par:.4f}% vs {100 * approx:.4f}%",
    )
    twist = [0.0010, 0.0050, 0.0090]
    full_tw = port_value(twist) / V_p0 - 1
    naive = -D_port * np.mean(twist)
    report.ok(
        "a steepening (+10/+50/+90 bp) loses more than the average-shift duration estimate implies",
        full_tw < naive - 0.004,
        f"{100 * full_tw:.3f}% vs {100 * naive:.3f}%",
    )
    # Cash-flow yield of the portfolio differs from the value-weighted average yield
    cf_by_t: dict[int, float] = {}
    for par, c, m, yy_ in hold:
        for k in range(1, m + 1):
            cf_by_t[k] = cf_by_t.get(k, 0) + par * (c / 200 + (1 if k == m else 0))
    cf_yield = brentq(
        lambda y: sum(cf / (1 + y / 2) ** k for k, cf in cf_by_t.items()) - V_p0, 0, 0.2
    )
    report.ok(
        "portfolio cash-flow yield 4.7357% differs from the value-weighted average yield 4.5343%",
        abs(cf_yield - 0.047357) < 5e-6
        and abs(wts @ np.array([h[3] for h in hold]) - 0.045343) < 5e-6,
    )


def check_return_sources(report: CheckReport, D_mac: float) -> None:
    """Part 8: sources of return and the Macaulay-duration horizon."""
    print("== part 8: sources of return and the Macaulay-duration horizon")
    # Buy the 7-year 5% bond at 4.80% (price 101.1754). Hold 3 years; coupons reinvested at the
    # prevailing yield.
    base = horizon(0.048)
    report.ok(
        "unchanged 4.80% yield: 3-year return 4.80% (bond-equivalent) exactly",
        abs(base.ann - 0.048) < 1e-12,
    )
    report.ok(
        "decomposition sums: coupons + interest on interest + pull to par + rate effect = total"
        " gain",
        close(
            base.coupons + base.int_on_int + base.pull_to_par + base.rate_effect,
            base.total,
            1e-9,
        ),
    )
    up100 = horizon(0.058)
    dn100 = horizon(0.038)
    print("    +100 bp:", {k: round(v, 4) for k, v in up100.model_dump().items()})
    report.ok(
        "+100 bp just after purchase: higher reinvestment but a capital loss; 3-year return"
        " 3.8112%",
        abs(up100.ann - 0.038112) < 5e-6
        and up100.rate_effect < 0
        and up100.int_on_int > base.int_on_int,
    )
    report.ok(
        "-100 bp: 5.8103% over 3 years (price gain outweighs lower reinvestment)",
        abs(dn100.ann - 0.058103) < 5e-6,
    )
    # Horizon equal to Macaulay duration (6.0081 years): returns nearly immune to a one-time small
    # parallel shift.
    Hmac = D_mac
    r_up, r_dn = horizon_return_frac(0.0490, Hmac), horizon_return_frac(0.0470, Hmac)
    report.ok(
        "horizon = Macaulay duration: a +/-10 bp shift moves the realised return by under 0.02 bp",
        abs(r_up - 0.048) < 2e-6 and abs(r_dn - 0.048) < 2e-6,
        f"{1e4 * (r_up - 0.048):.4f}, {1e4 * (r_dn - 0.048):.4f} bp",
    )
    report.ok(
        "and both shifts leave it at or above 4.80% (convexity)",
        r_up >= 0.048 - 1e-12 and r_dn >= 0.048 - 1e-12,
    )
    r_short = horizon_return_frac(0.0580, 2.0)
    r_long = horizon_return_frac(0.0580, 7.0)
    report.ok(
        "+100 bp: a 2-year horizon (shorter than duration) loses, the 7-year horizon (maturity)"
        " gains",
        r_short < 0.048 < r_long,
    )


def check_curve_measures(report: CheckReport) -> None:
    """Part 9: curve-based, effective, key-rate and empirical measures."""
    print("== part 9: curve-based, effective, key-rate and empirical measures")
    # Zero curve (continuous compounding) with key-rate vertices; a 7-year 5% bond priced off
    # the curve.
    kr = np.array([0.5, 1, 2, 3, 5, 7, 10])
    z0 = np.array([0.0380, 0.0382, 0.0390, 0.0400, 0.0420, 0.0435, 0.0450])
    tt = np.arange(1, 15) / 2
    cfb = np.full(14, 2.5)
    cfb[-1] += 100

    def pv_curve(zv: Floats, times: Floats = tt, cf: Floats = cfb) -> float:
        zt = np.interp(times, kr, zv)
        return float(np.sum(cf * np.exp(-zt * times)))

    P_c = pv_curve(z0)
    bp = 1e-4
    eff_D = (pv_curve(z0 - bp) - pv_curve(z0 + bp)) / (2 * P_c * bp)
    eff_C = (pv_curve(z0 - bp) + pv_curve(z0 + bp) - 2 * P_c) / (P_c * bp * bp)
    krd_rows: list[float] = []
    for j in range(len(kr)):
        e = np.zeros(len(kr))
        e[j] = bp
        krd_rows.append((pv_curve(z0 - e) - pv_curve(z0 + e)) / (2 * P_c * bp))
    krd = np.array(krd_rows)
    print(
        f"    curve price {P_c:.4f}, effective duration {eff_D:.4f}, convexity {eff_C:.3f}, KRDs"
        f" {np.round(krd, 4)}"
    )
    report.ok(
        "key-rate durations sum to the parallel-shift (effective) duration",
        abs(krd.sum() - eff_D) < 1e-6,
    )
    report.ok(
        "for this option-free bond almost all exposure sits at the 7-year vertex",
        krd[-2] / eff_D > 0.8 and krd[-1] < 1e-9,
    )
    shock = np.array([0, 0, 0.0005, 0.0010, 0.0020, 0.0030, 0.0035])
    dP_krd = -P_c * krd @ shock
    dP_full = pv_curve(z0 + shock) - P_c
    report.ok(
        "a steepening: key-rate durations give -1.7477 against -1.7302 by full repricing (the 1%"
        " gap is convexity)",
        abs(dP_krd + 1.74765) < 5e-5 and abs(dP_full + 1.73019) < 5e-5,
    )
    # Curve-based against yield-based duration for an option-free bond. A parallel shift of
    # the zero curve and a shift of the bond's own yield are different shocks; with one
    # compounding convention (continuous) for both, they give the same duration and convexity
    # only when the curve is flat. Counterexample: 20-year annual 10% bond, face 100, zero
    # curve z(t) = 1% + 0.3% t (continuous); flat-curve control at the bond's own yield.
    t20 = np.arange(1, 21, dtype=float)
    cf20 = np.full(20, 10.0)
    cf20[-1] += 100

    def pv_zero_shift(s: float, zfun: Callable[[Floats], Floats]) -> float:
        return float(np.sum(cf20 * np.exp(-(zfun(t20) + s) * t20)))

    def pv_yield(y: float) -> float:
        return float(np.sum(cf20 * np.exp(-y * t20)))

    def dur_conv(
        f: Callable[[float], float], x0: float, h_d: float = 1e-5, h_c: float = 1e-4
    ) -> tuple[float, float, float]:
        p0 = f(x0)
        dur = (f(x0 - h_d) - f(x0 + h_d)) / (2 * p0 * h_d)
        return p0, dur, (f(x0 - h_c) + f(x0 + h_c) - 2 * p0) / (p0 * h_c * h_c)

    @overload
    def z_slope(t: float) -> float: ...
    @overload
    def z_slope(t: Floats) -> Floats: ...
    def z_slope(t: float | Floats) -> float | Floats:
        return 0.01 + 0.003 * t

    P20, Dz, Cz = dur_conv(lambda s: pv_zero_shift(s, z_slope), 0.0)
    y20 = brentq(lambda y: pv_yield(y) - P20, -0.5, 0.5)
    _, Dyld, Cyld = dur_conv(pv_yield, y20)
    w_z = cf20 * np.exp(-z_slope(t20) * t20) / P20  # analytic weights: zero-rate discounting
    w_y = cf20 * np.exp(-y20 * t20) / P20  # yield discounting
    print(
        f"    20y 10% bond on z(t)=1%+0.3%t: price {P20:.6f}, yield {y20:.6%}; parallel-zero D"
        f" {Dz:.6f} C {Cz:.3f}; yield D {Dyld:.6f} C {Cyld:.3f}"
    )
    report.ok(
        "sloped curve: price 152.050048; parallel-zero-curve duration 10.218587 against yield"
        " duration 11.213091",
        abs(P20 - 152.050048) < 5e-7
        and abs(Dz - 10.218587) < 5e-6
        and abs(Dyld - 11.213091) < 5e-6,
    )
    report.ok(
        "the finite differences match the analytic weighted times: sum t w_z(t) and sum t w_y(t)"
        " (both weights sum to 1)",
        bool(
            abs(t20 @ w_z - Dz) < 1e-6
            and abs(t20 @ w_y - Dyld) < 1e-6
            and abs(w_z.sum() - 1) < 1e-12
        ),
    )
    report.ok(
        "convexity differs too: 146.46 by the zero-curve shift, 172.06 by the yield shift (sum t^2"
        " w)",
        bool(
            abs(Cz - 146.458) < 5e-3
            and abs(Cyld - 172.057) < 5e-3
            and abs((t20**2) @ w_z - Cz) < 1e-3
            and abs((t20**2) @ w_y - Cyld) < 1e-3
        ),
    )
    up_z = pv_zero_shift(0.01, z_slope) / P20 - 1
    up_y = pv_yield(y20 + 0.01) / P20 - 1
    y_after = brentq(lambda y: pv_yield(y) - pv_zero_shift(0.01, z_slope), -0.5, 0.5)
    report.ok(
        "full repricing for +100 bp: -9.525% for the zero-curve shift, -10.400% for the yield"
        " shift; the parallel zero\n      shift moves this bond's yield by only 91.0 bp",
        abs(up_z + 0.09525) < 5e-6
        and abs(up_y + 0.10400) < 5e-6
        and abs((y_after - y20) - 0.009098) < 5e-7,
    )
    Pf, Dzf, Czf = dur_conv(lambda s: pv_zero_shift(s, lambda t: np.full_like(t, y20)), 0.0)
    _, Dyf, Cyf = dur_conv(pv_yield, y20)
    report.ok(
        "flat-curve control (all zero rates at the 5.4546% yield): same price, and the two"
        " durations and\n      convexities coincide",
        abs(Pf - P20) < 1e-9 and abs(Dzf - Dyf) < 1e-8 and abs(Czf - Cyf) < 1e-4,
    )
    zc_t = 20.0
    _, Dz0, Cz0 = dur_conv(lambda s: 100 * math.exp(-(z_slope(zc_t) + s) * zc_t), 0.0)
    y0c = z_slope(zc_t)
    _, Dy0, Cy0 = dur_conv(lambda y: 100 * math.exp(-y * zc_t), y0c)
    report.ok(
        "single cash flow (20-year zero) on the same sloped curve: both durations are 20 and both"
        " convexities 400",
        abs(Dz0 - 20) < 1e-6
        and abs(Dy0 - 20) < 1e-6
        and abs(Cz0 - 400) < 1e-3
        and abs(Cy0 - 400) < 1e-3,
    )

    # Callable at 102 on the coupon date 2.5 years ahead (period 5), zero-volatility exercise:
    # the issuer calls if the bond's value at the call date, computed from today's (shifted)
    # forward curve, exceeds the call price. This removes option time value; the Handbook's
    # lattice example shows the volatility-model version.
    def callable_value(
        zv: Floats, coupon: float = 5.0, call_k: int = 5, call_px: float = 102.0
    ) -> tuple[float, float, bool]:
        zt = np.interp(tt, kr, zv)
        df = np.exp(-zt * tt)
        cf = np.full(14, coupon / 2)
        cf[-1] += 100
        straight = float(cf @ df)
        after = (
            float(cf[call_k:] @ df[call_k:]) / df[call_k - 1]
        )  # forward value at the call date of remaining flows
        if after > call_px:
            cf_called = cf[:call_k].copy()
            cf_called[-1] += call_px
            return float(cf_called @ df[:call_k]), straight, True
        return straight, straight, False

    for lvl in (0.0, -0.006):
        zc = z0 + lvl
        Vc, Vs, called = callable_value(zc)
        eff = (callable_value(zc - 0.0025)[0] - callable_value(zc + 0.0025)[0]) / (2 * Vc * 0.0025)
        mod_like = (callable_value(zc - 0.0025)[1] - callable_value(zc + 0.0025)[1]) / (
            2 * Vs * 0.0025
        )
        print(
            f"    shift {1e4 * lvl:+.0f} bp: callable {Vc:.4f} (called={called}), straight"
            f" {Vs:.4f}, effective D {eff:.3f}, straight D {mod_like:.3f}"
        )
        if lvl == 0.0:
            eff5 = (callable_value(zc - 0.0005)[0] - callable_value(zc + 0.0005)[0]) / (
                2 * Vc * 0.0005
            )
            report.ok(
                "today the call is out of the money: with +/-5 bp shocks effective duration equals"
                " the straight bond's (6.008)",
                not called and abs(eff5 - mod_like) < 0.01,
            )
            report.ok(
                "with +/-25 bp shocks the down shock crosses the exercise boundary and effective"
                " duration drops to 4.96",
                abs(eff - 4.956) < 5e-3
                and callable_value(zc - 0.0025)[2]
                and not callable_value(zc + 0.0025)[2],
            )
        else:
            report.ok(
                "60 bp lower, the call is exercised and effective duration collapses toward the"
                " 2.5-year call date",
                called and eff < 2.6 < mod_like,
            )
    # Handbook Exhibit 5-15 (Black-Derman-Toy lattice prices, 10 bp shifts) -> effective
    # duration and convexity (Eq. 5-6)
    for name, (v0_, vp, vm), (dexp, cexp) in [
        ("option-free", (98.8395557, 98.3796865, 99.3018797), (4.67, 24.84)),
        ("callable", (97.6550524, 97.2132182, 98.0922517), (4.50, -47.46)),
        ("putable", (100.4410453, 100.1343384, 100.7706854), (3.17, 228.32)),
    ]:
        dd = (vm - vp) / (2 * v0_ * 0.001)
        cc = (vm + vp - 2 * v0_) / (v0_ * 0.001**2)
        report.ok(
            f"Handbook {name}: effective duration {dexp}, effective convexity {cexp}",
            abs(dd - dexp) < 0.005 and abs(cc - cexp) < 0.01,
        )
    report.ok(
        "callable: duration 4.50 and convexity -47.46 give -4.74% for +100 bp (Eq. 5-7 scaling)",
        abs(-4.50 * 0.01 + 0.5 * (-47.46) * 0.0001 + 0.0474) < 1e-4,
    )
    # Empirical duration: synthetic monthly data, 120 months. A corporate bond with analytical
    # (rate) duration 6.5 whose credit spread falls when Treasury yields rise (corr -0.5).
    # Regressing returns on Treasury yield changes gives a smaller empirical duration than the
    # analytical one.
    rng = np.random.default_rng(20261018)
    dy_t = rng.normal(0, 0.0020, 120)
    dspread = -0.25 * dy_t + rng.normal(0, 0.0008, 120)
    ret = -6.5 * (dy_t + dspread) + rng.normal(0, 0.0005, 120)
    beta = np.polyfit(dy_t, ret, 1)[0]
    print(f"    empirical duration {-beta:.3f} vs analytical 6.5")
    report.ok(
        "empirical duration 4.63 (population value 6.5 x 0.75 = 4.875), well below the analytical"
        " 6.5",
        abs(-beta - 4.630) < 5e-3 and -beta < 6.5,
    )


def check_municipal_oid(report: CheckReport) -> None:
    """Part 10: discount on a municipal bond, OID against market discount."""
    print("== part 10: discount on a municipal bond, OID against market discount")
    # rule:bond-issuance-legal-tax. U.S. federal income tax for an individual holder, IRS Pub.
    # 550 (2025) and Pub. 1212 (rev. December 2025): tax-exempt OID is exempt interest that is
    # accrued by constant yield and added to basis; market discount (issue price plus OID
    # accrued before purchase, less basis) is not exempt and, for a purchase after 30 April
    # 1993, is ordinary income on disposal or redemption unless below the de minimis 0.25% x
    # full years to maturity.
    face_m, cpn_m, n_m, issue_m = 1000.0, 30.0, 40, 900.0

    def muni_pv(y: float, periods: int) -> float:
        return (
            sum(cpn_m / 2 / (1 + y / 2) ** k for k in range(1, periods + 1))
            + face_m / (1 + y / 2) ** periods
        )

    y_m = brentq(lambda y: muni_pv(y, n_m) - issue_m, 1e-4, 0.2)
    basis = issue_m
    for _ in range(
        10
    ):  # constant-yield accrual period by period: interest at the issue yield less the coupon paid
        basis = basis * (1 + y_m / 2) - cpn_m / 2
    aip_5 = muni_pv(y_m, n_m - 10)
    report.ok(
        "issue at 900 implies 3.7128% s.a.; after five years the adjusted issue price is 918.58 by"
        " period-by-period accrual and by discounting the remaining cash flows at the issue yield",
        abs(y_m - 0.037128) < 5e-7 and close(basis, aip_5, 1e-9) and abs(aip_5 - 918.577) < 5e-4,
    )
    md_b = aip_5 - 850.0
    de_min = 0.0025 * face_m * 15
    oid_left = face_m - aip_5
    gain_b = face_m - (850.0 + oid_left)
    report.ok(
        "holder B at 850: market discount 68.58 exceeds de minimis 37.50; remaining OID 81.42 is"
        " exempt and lifts basis to 931.42; the 68.58 redemption gain equals the market discount"
        " (ordinary income)",
        md_b > de_min
        and abs(md_b - 68.577) < 5e-4
        and abs(oid_left - 81.423) < 5e-4
        and close(gain_b, md_b, 1e-9)
        and close(oid_left + md_b, face_m - 850.0, 1e-9),
    )
    report.ok(
        "holder A sells at 850 after five years: capital loss 68.58 against the OID-adjusted"
        " basis, not 50 against cost",
        abs((850.0 - aip_5) + 68.577) < 5e-4 and close(850.0 - issue_m, -50.0),
    )
    md_900 = aip_5 - 900.0
    report.ok(
        "bought at 900 instead: discount 18.58 is below 37.50, so market discount is zero and the"
        " 18.58 gain is capital; A selling at 950 instead has a capital gain of 31.42",
        md_900 < de_min and abs(md_900 - 18.577) < 5e-4 and abs(950.0 - aip_5 - 31.423) < 5e-4,
    )


def main() -> int:
    """Print the versions, then run the 10 parts with one report.

    The worked numbers of meth:bond-price-from-yield, meth:matrix-pricing,
    def:bond-yield-spread-measures, meth:floating-money-market-yields,
    meth:bond-return-decomposition, meth:yield-duration-pvbp, meth:convexity-portfolio-duration and
    meth:curve-based-empirical-duration, and the municipal original-issue and market discount
    example of rule:bond-issuance-legal-tax (IRS Pub. 550 for 2025, Pub. 1212 rev. December 2025).

    Sources reproduced: the U.S. Treasury's own formulas and worked examples in 31 CFR part 356,
    Appendix B (coupon price at a yield; bill price, discount rate and investment rate); Fabozzi
    (ed.), Handbook of Fixed Income Securities, 9th ed. (2021), chap. 4 Illustrations 1-2 and 4-5
    (prices, a corporate bond between coupon dates), Exhibit 4-7 (a floater's discount margin) and
    chap. 5 (duration 13.09, convexity measure 112.38, PVBP, portfolio duration 8.81, effective
    duration and convexity from printed lattice prices); the New York Fed's SOFR Averages and Index
    arithmetic, whose published Index example is reproduced. Everything else is an original example
    with invented inputs: a 5% 30/360 corporate bond settling on 21 October 2026, a callable
    variant, a dated SOFR FRN, flat or stated curves, a sloped-curve counterexample in which
    parallel-zero-curve and yield duration and convexity differ (with a flat-curve control), and a
    synthetic monthly series for empirical duration (fixed seed).

    Conventions are stated beside each block: semiannual coupons, bond-equivalent (doubled) yields
    unless stated, prices per 100 of par, durations in years, PVBP per 100 of par for one basis
    point.

    Count convention: one check is one executed ok() call (a call inside a loop counts once per
    iteration).

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
    report = CheckReport()
    check_treasury_formulas(report)
    w0, full0, clean0 = check_pricing_between_coupons(report)
    check_yield_spreads(report, w0, full0, clean0)
    check_matrix_pricing(report)
    check_floating_money_market(report)
    D_mac = check_duration_pvbp(report)
    check_portfolio_duration(report)
    check_return_sources(report, D_mac)
    check_curve_measures(report)
    check_municipal_oid(report)
    print()
    if report.failures:
        print(f"{len(report.failures)} check(s) failed: {report.failures}")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
