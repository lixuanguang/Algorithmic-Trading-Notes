"""Fixed-income portfolio management: the worked numbers of seven entries."""

import math
import sys
from typing import Final, cast

import numpy as np
import scipy
from numpy.typing import NDArray
from scipy.optimize import brentq, linprog

from trading_notes.numerical.fixed_income_portfolio_management.curve_exposures import (
    AnnualZeroCurve,
    bond,
    horizon_value,
    mac,
)
from trading_notes.numerical.report import CheckReport
from trading_notes.numerical.tolerance import close

type Floats = NDArray[np.float64]

# The invented annual zero curve: 3.00% + 0.15% x years to 10 years, flat after.
CURVE: Final = AnnualZeroCurve(level=0.03, slope=0.0015, flat_after=10.0)


def check_mandates(report: CheckReport) -> None:
    """Part 1: roles, mandates, portfolio risk and an expected-return model."""
    print("== part 1: roles, mandates, portfolio risk and an expected-return model")
    yld, roll, dur, cvx, dy_view, sig_y = 0.046, 0.003, 6.2, 60.0, 0.0025, 0.01
    credit_w, _spread, exp_loss = 0.30, 0.011, 0.002
    er = yld + roll - dur * dy_view + 0.5 * cvx * sig_y**2 - credit_w * exp_loss
    report.ok(
        "benchmark expected return: yield 4.60 + rolldown 0.30 - duration 6.2 x 25 bp view (1.55)"
        " + convexity 0.30 - credit losses 0.06 = 3.59%",
        abs(er - 0.0359) < 1e-12,
        f"{er:.4%}",
    )
    report.ok(
        "risk from rates: duration 6.2 x 1% yield volatility = 6.2% a year; the 25 bp view costs"
        " 1.55%, a quarter of it",
        close(dur * sig_y, 0.062, 1e-12) and close(dur * dy_view, 0.0155, 1e-12),
    )
    vol = {
        rho: math.sqrt(0.6**2 * 0.16**2 + 0.4**2 * 0.062**2 + 2 * rho * 0.6 * 0.4 * 0.16 * 0.062)
        for rho in (-0.2, 0.4)
    }
    report.ok(
        "a 60/40 portfolio (equity 16%, bonds 6.2%) has 9.42% volatility with stock-bond"
        " correlation -0.2 and 10.83% at +0.4: bonds diversify less when the correlation turns"
        " positive",
        abs(vol[-0.2] - 0.0942) < 5e-5 and abs(vol[0.4] - 0.1083) < 5e-5,
        f"{vol[-0.2]:.4f} {vol[0.4]:.4f}",
    )
    liq = {"on-the-run Treasury": 0.0002, "IG corporate": 0.0040, "HY corporate": 0.0100}
    report.ok(
        "selling 50m of each costs half the bid-ask: Treasury 5,000, IG corporate 100,000, high"
        " yield 250,000",
        [round(50e6 * v / 2) for v in liq.values()] == [5000, 100000, 250000],
    )


def check_leverage_taxation(report: CheckReport) -> None:
    """Part 2: leverage and taxation."""
    print("== part 2: leverage and taxation")
    eq, borrowed, c, r_inv = 40.0, 100.0, 0.04, 0.045
    r_e = r_inv + borrowed / eq * (r_inv - c)
    report.ok(
        "MIP: 40m of equity and 100m borrowed at 4% invested at 4.5% -> 5.75% on equity; at 3.5%"
        " -> 2.25%",
        close(r_e, 0.0575, 1e-12) and close(0.035 + borrowed / eq * (0.035 - c), 0.0225, 1e-12),
    )
    report.ok(
        "MIP: equity 100m and 50m borrowed at 6%, invested at 6.5% -> 6.75%",
        close(0.065 + 0.5 * (0.065 - 0.06), 0.0675, 1e-12),
    )
    h = 0.02
    report.ok(
        "repo with a 2% haircut caps leverage at 1/h = 50 times equity; a 3% price fall wipes out"
        " 1.5 times the equity",
        close(1 / h, 50, 1e-9) and close(0.03 * 50, 1.5, 1e-9),
    )
    report.ok(
        "Handbook chap. 9: 6% tax-exempt at a 40% marginal rate is a 10% equivalent taxable yield",
        close(0.06 / (1 - 0.40), 0.10, 1e-12),
    )
    muni, taxable, rate = 0.036, 0.050, 0.37
    report.ok(
        "for a 37% taxpayer, a 3.6% municipal beats a 5.0% taxable bond (3.15% after tax); for a"
        " tax-exempt pension the taxable bond wins by 1.4%",
        close(taxable * (1 - rate), 0.0315, 1e-12)
        and muni > taxable * (1 - rate)
        and close(taxable - muni, 0.014, 1e-12),
    )
    report.ok(
        "borrowing at 4% to buy the 3.6% municipal loses 0.4% before tax and 0.4% after tax: the"
        " interest is not deductible",
        close(muni - 0.04, -0.004, 1e-12),
    )
    loss, gain = 120_000.0, 150_000.0
    report.ok(
        "harvesting a 120,000 loss on bonds against 150,000 of realised gains saves 45,600 at a"
        " 38% capital-gains rate, if the repurchase avoids a wash sale",
        close(loss * 0.38, 45_600, 1e-9) and loss < gain,
    )


def check_ladders(report: CheckReport) -> None:
    """Part 3: liability-driven investing, cash-flow matching and ladders."""
    print("== part 3: liability-driven investing, cash-flow matching and ladders")
    liab_t = np.array([1, 2, 3, 4, 5])
    liab = np.array([10e6, 10e6, 12e6, 12e6, 15e6])
    bonds = [bond(cpn, m) for cpn, m in ((0.03, 1), (0.034, 2), (0.036, 3), (0.038, 4), (0.040, 5))]
    prices = np.array([CURVE.price(*b) for b in bonds]) / 100
    cf_matrix = np.zeros((5, 5))
    for j, (cfs, times) in enumerate(bonds):
        for c_, t_ in zip(cfs, times, strict=True):
            cf_matrix[t_ - 1, j] = c_ / 100
    res = linprog(prices, A_ub=-cf_matrix, b_ub=-liab, bounds=[(0, None)] * 5, method="highs")
    pv_liab = sum(
        liab_t_cf / (1 + CURVE.zero(t)) ** t for liab_t_cf, t in zip(liab, liab_t, strict=True)
    )
    report.ok(
        "cash-flow matching five liabilities (59m) with five annual-coupon bonds: the least-cost"
        " portfolio meets every payment exactly and costs the liabilities' present value on this"
        " curve",
        res.status == 0
        and np.allclose(cf_matrix @ cast(Floats, res.x), liab, atol=1e-3)
        and abs(cast(float, res.fun) - pv_liab) < 1.0,
        f"cost {cast(float, res.fun) / 1e6:.4f}m, PV {pv_liab / 1e6:.4f}m",
    )
    ladder = [bond(0.034 + 0.0015 * (m - 1), m) for m in range(1, 11)]
    ladder_val = [CURVE.price(*b) for b in ladder]
    ladder_dur = sum(
        CURVE.modified_duration(*b) * v for b, v in zip(ladder, ladder_val, strict=True)
    ) / sum(ladder_val)
    report.ok(
        "a 1-10 year ladder (equal face in each year) has a duration of 4.69 and returns a tenth"
        " of its face each year for reinvestment or spending",
        abs(ladder_dur - 4.686) < 0.001,
        f"{ladder_dur:.3f}",
    )

    def rung_cfs(weights: Floats) -> Floats:
        """Annual cash flows (years 1-10) of a ladder holding `weights` units of face a rung."""
        cf = np.zeros(10)
        for w_, (cfs_, times_) in zip(weights, ladder, strict=True):
            for c_, t_ in zip(cfs_, times_, strict=True):
                cf[t_ - 1] += w_ * c_
        return cf

    tw_vec = np.array(
        [CURVE.zero(t, twist=0.005) - CURVE.zero(t) for t in range(1, 11)]
    )  # -50 bp at 1y to +50 bp at 10y
    eq_face = rung_cfs(np.ones(10))
    krd_face = CURVE.key_rates(eq_face)
    analytic = np.array(
        [(k + 1) * eq_face[k] / (1 + CURVE.zero(k + 1)) ** (k + 2) for k in range(10)]
    ) / CURVE.pv_bumped(eq_face, np.zeros(10))
    twist_face = CURVE.pv_bumped(eq_face, tw_vec) / CURVE.pv_bumped(eq_face, np.zeros(10)) - 1
    report.ok(
        "equal-face ladder: key-rate durations rise from 0.1304 (1y) to 0.6363 (10y), not equal;"
        " they match the analytic t CF_t / (1+z_t)^(t+1) / V and sum to its duration 4.686245",
        bool(
            np.allclose(krd_face, analytic, atol=1e-8)
            and abs(krd_face[0] - 0.1304) < 5e-5
            and abs(krd_face[-1] - 0.6363) < 5e-5
            and abs(krd_face.sum() - 4.686245) < 1e-6
            and abs(krd_face.sum() - ladder_dur) < 1e-4
            and np.all(np.diff(krd_face) > 0)
        ),
        " ".join(f"{x:.4f}" for x in krd_face),
    )
    report.ok(
        "a steepening twist (-50 bp at 1y, +50 bp at 10y) changes the equal-face ladder's value by"
        " -0.493% by full repricing; the key-rate first-order estimate is -0.510%: the ladder"
        " carries slope risk",
        bool(abs(twist_face + 0.00493) < 5e-6 and abs(-(krd_face * tw_vec).sum() + 0.00510) < 5e-6),
        f"{twist_face:.4%}",
    )
    unit_pv = np.array([CURVE.pv_bumped(rung_cfs(np.eye(10)[i]), np.zeros(10)) for i in range(10)])
    unit_dd = np.array(
        [unit_pv[i] * CURVE.key_rates(rung_cfs(np.eye(10)[i])).sum() for i in range(10)]
    )
    eq_mv = rung_cfs(1 / unit_pv)  # equal market value per rung (Fabozzi's definition)
    eq_risk = rung_cfs(1 / unit_dd)  # equal dollar duration per rung
    krd_mv, krd_risk = CURVE.key_rates(eq_mv), CURVE.key_rates(eq_risk)
    twist_mv = CURVE.pv_bumped(eq_mv, tw_vec) / CURVE.pv_bumped(eq_mv, np.zeros(10)) - 1
    twist_risk = CURVE.pv_bumped(eq_risk, tw_vec) / CURVE.pv_bumped(eq_risk, np.zeros(10)) - 1
    mv_share_1y = (unit_pv[0] / unit_dd[0]) / np.sum(unit_pv / unit_dd)
    report.ok(
        "equal market value per rung barely changes the profile (0.13 to 0.63, twist -0.48%);"
        " equal dollar duration per rung flattens it (0.25 to 0.35) and nearly removes the twist"
        " exposure (+0.10%), but shortens duration to 3.14 and puts 32% of value in the 1-year"
        " rung",
        bool(
            krd_mv[-1] / krd_mv[0] > 4
            and abs(twist_mv + 0.00483) < 5e-5
            and krd_risk.max() / krd_risk.min() < 1.4
            and abs(twist_risk - 0.00104) < 5e-5
            and abs(krd_risk.sum() - 3.137) < 1e-3
            and abs(mv_share_1y - 0.324) < 1e-3
        ),
        f"MV {krd_mv[0]:.4f}-{krd_mv[-1]:.4f} twist {twist_mv:.3%}; risk"
        f" {krd_risk.min():.4f}-{krd_risk.max():.4f} twist {twist_risk:.3%}, duration"
        f" {krd_risk.sum():.3f}",
    )


def check_immunisation(report: CheckReport) -> None:
    """Part 4: immunising single and multiple liabilities (MIP chap. 6, sec. 4.1)."""
    print("== part 4: immunising single and multiple liabilities (MIP chap. 6, sec. 4.1)")
    report.ok(
        "MIP GIC: 9,642,899 grows to 13,934,413 at 3.75% for ten half-years",
        abs(9_642_899 * 1.0375**10 - 13_934_413) < 1,
    )

    y0 = 0.05
    zero5 = ([100.0], [5])
    coup5 = bond(0.05, 5)
    b1, b10 = ([100.0], [1]), bond(0.05, 10)

    w10 = (5 - mac(*b1, y0)) / (mac(*b10, y0) - mac(*b1, y0))
    p1, p10 = (
        100 / (1 + y0),
        sum(c_ / (1 + y0) ** t_ for c_, t_ in zip(*b10, strict=True)),
    )
    budget = 100 / (1 + y0) ** 5  # cost of the 5-year zero: the immunised target is 100
    units1, units10 = (1 - w10) * budget / p1, w10 * budget / p10
    target = 100.0
    for dy in (-0.02, -0.01, 0.01, 0.02):
        hz_bul = horizon_value(*zero5, y0 + dy, 5)
        hz_cpn = horizon_value(*coup5, y0 + dy, 5) * budget / 100
        hz_bar = units1 * horizon_value(*b1, y0 + dy, 5) + units10 * horizon_value(*b10, y0 + dy, 5)
        report.ok(
            f"parallel {dy:+.0%}: zero exactly 100; duration-matched barbell >= 100 (convexity);"
            f" maturity-matched 5% coupon bond {'falls short' if dy < 0 else 'beats the target'}",
            close(hz_bul, target, 1e-9)
            and hz_bar >= target - 1e-9
            and ((hz_cpn < target) if dy < 0 else (hz_cpn > target)),
            f"barbell {hz_bar:.3f}, coupon bond {hz_cpn:.3f}",
        )
    tw_bar = units1 * horizon_value(*b1, y0, 5, twist=0.01) + units10 * horizon_value(
        *b10, y0, 5, twist=0.01
    )
    report.ok(
        "a twist (reinvestment rates down 100 bp, long rates up 100 bp) leaves the barbell short"
        " of the target; the zero is untouched",
        tw_bar < target - 1 and close(horizon_value(*zero5, y0, 5, twist=0.01), 100, 1e-9),
        f"{tw_bar:.3f}",
    )
    report.ok(
        "barbell weight in the 10-year bond = 56.3% by value for Macaulay duration 5 (1-year zero"
        " and 10-year 5% bond at 5%)",
        abs(w10 - 0.5628) < 5e-4,
        f"{w10:.4f}",
    )
    # multiple liabilities: 10m at 2, 5 and 8 years
    L_t, L_cf = [2, 5, 8], [10.0, 10.0, 10.0]
    pv_l = sum(c_ / (1 + y0) ** t_ for c_, t_ in zip(L_cf, L_t, strict=True))
    d_l = sum(t_ * c_ / (1 + y0) ** t_ for c_, t_ in zip(L_cf, L_t, strict=True)) / pv_l
    zA, zB = 1, 12
    wB = (d_l - zA) / (zB - zA)
    assets = {zA: (1 - wB) * pv_l * (1 + y0) ** zA, zB: wB * pv_l * (1 + y0) ** zB}

    def surplus(dy: float, twist: float = 0.0) -> float:
        a = sum(f / (1 + y0 + dy + (twist if t_ > 5 else -twist)) ** t_ for t_, f in assets.items())
        lv = sum(
            c_ / (1 + y0 + dy + (twist if t_ > 5 else -twist)) ** t_
            for c_, t_ in zip(L_cf, L_t, strict=True)
        )
        return a - lv

    report.ok(
        "multiple liabilities (10m at 2, 5, 8 years): zeros at 1 and 12 years match PV 23.67m and"
        " duration 4.71; asset times bracket every liability date",
        abs(pv_l - 23.674) < 0.001 and abs(d_l - 4.71) < 0.01 and zA < min(L_t) and zB > max(L_t),
        f"PV {pv_l:.3f}, D {d_l:.3f}",
    )
    report.ok(
        "surplus stays non-negative for parallel shifts of -200 to +200 bp (Fong-Vasicek"
        " conditions met)",
        all(surplus(d) >= -1e-9 for d in np.linspace(-0.02, 0.02, 9)),
    )
    report.ok(
        "a twist (rates beyond 5 years +100 bp, within 5 years -100 bp) creates a deficit:"
        " immunisation is for parallel moves",
        surplus(0.0, 0.01) < 0,
        f"{surplus(0.0, 0.01):.3f}m",
    )
    req = 500 * (1 + 0.03 / 2) ** 6
    need = req / (1 + 0.0475 / 2) ** 6
    report.ok(
        "MIP contingent immunisation: 500m must grow to 546.72m at a 3% safety net; immunising at"
        " 4.75% needs 474.90m; cushion 25.10m",
        abs(req - 546.72) < 0.005
        and abs(need - 474.90) < 0.005
        and abs(500 - need - 25.10) < 0.005,
    )

    def p10y(yy: float) -> float:
        return sum(
            c_ / (1 + yy / 2) ** t_ for c_, t_ in zip([2.375] * 19 + [102.375], range(1, 21))
        )

    trig = brentq(lambda yy: 500 * p10y(yy) / p10y(0.0475) - req / (1 + yy / 2) ** 6, 0.0475, 0.20)
    report.ok(
        "if the 500m sits in a 10-year 4.75% bond, the cushion is exhausted if its yield rises to"
        " 5.80%, about 105 bp: the manager must then immunise",
        abs(trig - 0.0580) < 5e-4,
        f"{trig:.4%}",
    )
    before = [1_065_613 * 5.025 * 0.01, 978_376 * 1.232 * 0.01, 1_034_693 * 4.479 * 0.01]
    after = [1_023_704 * 4.246 * 0.01, 1_004_770 * 0.305 * 0.01, 1_002_458 * 3.596 * 0.01]
    ratio_dd = sum(before) / sum(after)
    cash = (ratio_dd - 1) * (1_023_704 + 1_004_770 + 1_002_458)
    report.ok(
        "MIP Exhibits 6-9/6-10: dollar durations 53,548 / 12,054 / 46,343 fall to 43,465 / 3,063 /"
        " 36,049 a year later; rebalancing ratio 1.356 and cash of 1,077,796 (MIP's 1,079,012 uses"
        " the rounded ratio; its 37,315 and 27,526 are averages; the portfolio's dollar duration"
        " is the sum, 111,945, which leaves the ratio unchanged)",
        all(abs(x - y) <= 1 for x, y in zip(before, [53548, 12054, 46343], strict=True))
        and all(abs(x - y) <= 2 for x, y in zip(after, [43465, 3063, 36049], strict=True))
        and abs(ratio_dd - 1.356) < 5e-4
        and abs(round(sum(before) / 3) - 37315) <= 1
        and abs(round(sum(before)) - 111945) <= 1
        and abs(cash - 1_077_796) < 1
        and abs(0.356 * 3_030_932 - 1_079_012) < 1,
        f"ratio {ratio_dd:.4f}, cash {cash:,.0f}",
    )


def check_indexes(report: CheckReport) -> None:
    """Part 5: bond indexes, passive exposure and benchmark choice."""
    print("== part 5: bond indexes, passive exposure and benchmark choice")
    n_index, issue_vol = 10_000, 0.02
    for n_hold in (100, 400, 1600):
        te = issue_vol * math.sqrt(1 / n_hold - 1 / n_index)
        report.ok(
            f"stratified sampling with {n_hold} equal-weight issues matching every cell:"
            f" issue-specific tracking error {te:.2%}",
            te < issue_vol / math.sqrt(n_hold) + 1e-12 and te > 0,
            f"{te:.4%}",
        )
    report.ok(
        "an insurer with 7-year liabilities is better benchmarked to a liability index than to the"
        " broad market: a 6.2-duration aggregate leaves 0.8 years of surplus duration on assets"
        " equal to liabilities",
        close(7.0 - 6.2, 0.8, 1e-12),
    )


def check_curve_positioning(report: CheckReport) -> None:
    """Part 6: curve views: market-consistent, divergent, volatility and cross-currency."""
    print(
        "== part 6: positioning for curve views (market-consistent, divergent, volatility,"
        " cross-currency)"
    )
    p5_0 = 100 / (1 + CURVE.zero(5)) ** 5
    p4_unch = 100 / (1 + CURVE.zero(4)) ** 4
    _f_15 = (1 + CURVE.zero(5)) ** 5 / (1 + CURVE.zero(1)) - 1
    report.ok(
        "market-consistent view (forwards realised): every zero earns the 1-year rate 3.15%;"
        " unchanged curve: the 5-year zero earns 4.352% over a year (rolling yield)",
        abs(p4_unch / p5_0 - 1 - 0.04352) < 5e-5 and CURVE.zero(1) == 0.0315,
        f"{p4_unch / p5_0 - 1:.5f}",
    )
    dv01_2 = CURVE.modified_duration(*bond(0.033, 2)) * CURVE.price(*bond(0.033, 2)) * 1e-4
    dv01_10 = CURVE.modified_duration(*bond(0.045, 10)) * CURVE.price(*bond(0.045, 10)) * 1e-4
    ratio = dv01_10 / dv01_2
    pnl_steep = ratio * (
        CURVE.price(*bond(0.033, 2), twist=0.005) - CURVE.price(*bond(0.033, 2))
    ) - (CURVE.price(*bond(0.045, 10), twist=0.005) - CURVE.price(*bond(0.045, 10)))
    report.ok(
        "divergent view (curve to steepen): DV01-neutral 2s10s steepener buys 4.18 2-year bonds"
        " per 10-year bond sold and gains on a 100 bp twist",
        abs(ratio - 4.179) < 0.001 and pnl_steep > 0,
        f"ratio {ratio:.3f}, gain {pnl_steep:.3f}",
    )
    p5b = CURVE.price(*bond(0.0375, 5))
    d5b = CURVE.modified_duration(*bond(0.0375, 5))
    w_l = (d5b - CURVE.modified_duration(*bond(0.0315, 1))) / (
        CURVE.modified_duration(*bond(0.045, 10)) - CURVE.modified_duration(*bond(0.0315, 1))
    )

    def barbell_minus_bullet(shift: float) -> float:
        bb = (1 - w_l) * CURVE.price(*bond(0.0315, 1), shift=shift) / CURVE.price(
            *bond(0.0315, 1)
        ) + w_l * CURVE.price(*bond(0.045, 10), shift=shift) / CURVE.price(*bond(0.045, 10))
        return bb - CURVE.price(*bond(0.0375, 5), shift=shift) / p5b

    report.ok(
        "volatility view: a duration-matched 1y/10y barbell beats the 5-year bullet for large"
        " parallel moves either way (more convex) and lags it slightly for small ones",
        barbell_minus_bullet(0.015) > 0
        and barbell_minus_bullet(-0.015) > 0
        and barbell_minus_bullet(0.0) == 0,
        f"+150bp {barbell_minus_bullet(0.015):.5f}",
    )
    report.ok(
        "cross-currency: a Bund at 2.6% hedged into dollars with US 3-month 4.3% and EUR 2.2%"
        " earns about 2.6 + 2.1 = 4.7%, above a 4.5% Treasury of similar duration, before hedging"
        " costs",
        close(0.026 + (0.043 - 0.022), 0.047, 1e-12) and 0.047 > 0.045,
    )


def check_curve_strategy(report: CheckReport) -> None:
    """Part 7: key-rate exposure against the benchmark, and a curve strategy's return and risk."""
    print(
        "== part 7: key-rate exposure against the benchmark and the expected return and risk of a"
        " curve strategy"
    )
    keys = [2, 5, 10, 30]
    bench_krd = np.array([0.6, 1.4, 2.4, 1.8])
    port_krd = np.array([0.9, 1.0, 2.0, 2.3])
    active = port_krd - bench_krd
    report.ok(
        "portfolio and benchmark both have duration 6.2 but the portfolio is long 2s and 30s and"
        " short 5s and 10s (a barbell against a bulletier benchmark)",
        close(port_krd.sum(), bench_krd.sum(), 1e-12)
        and active[0] > 0
        and active[3] > 0
        and active[1] < 0
        and active[2] < 0,
        " ".join(f"{k}y {a:+.1f}" for k, a in zip(keys, active, strict=True)),
    )
    scen = {
        "parallel +50": np.array([50, 50, 50, 50]),
        "bear steepener": np.array([0, 25, 50, 75]),
        "butterfly": np.array([-25, 25, 25, -25]),
    }
    rel = {k: float(-(active * v).sum() * 1e-4) for k, v in scen.items()}
    report.ok(
        "relative returns: parallel +50 bp 0.00%; bear steepener (2s 0, 30s +75 bp) -0.075%;"
        " butterfly (wings -25, belly +25) +0.40%",
        abs(rel["parallel +50"]) < 1e-12
        and abs(rel["bear steepener"] + 0.00075) < 1e-9
        and abs(rel["butterfly"] - 0.0040) < 1e-9,
        str({k: round(v, 5) for k, v in rel.items()}),
    )
    roll_diff, conv_diff = -0.0004, 0.0003
    exp_rel = roll_diff + conv_diff
    krd_vol = np.array([0.0080, 0.0090, 0.0085, 0.0075])
    krd_corr = np.array(
        [[1, 0.9, 0.8, 0.7], [0.9, 1, 0.95, 0.85], [0.8, 0.95, 1, 0.92], [0.7, 0.85, 0.92, 1]]
    )
    cov = np.outer(krd_vol, krd_vol) * krd_corr
    te = math.sqrt(active @ cov @ active)
    report.ok(
        "expected relative return: rolldown -4 bp (barbell rolls less) + convexity +3 bp = -1 bp a"
        " year, against a 0.23% tracking error from key-rate yield volatility of 75-90 bp",
        close(exp_rel, -0.0001, 1e-12) and abs(te - 0.00228) < 0.00005,
        f"TE {te:.4%}",
    )


def main() -> int:
    """Print the versions, then run the seven parts with one report.

    The worked numbers of def:fixed-income-mandates-return-model, meth:bond-leverage-taxation,
    meth:liability-matching-ladders, meth:immunisation-liabilities,
    meth:bond-index-exposure-benchmarks, meth:yield-curve-positioning and
    meth:curve-strategy-evaluation.

    Reproduced from Managing Investment Portfolios (2007), chap. 6: the leveraged return 5.75% /
    2.25% (sec. 5.2), the five-year GIC target of 13,934,413 from 9,642,899 at 7.5% (sec. 4.1.1.1),
    contingent immunization (546.72 terminal, 474.90 required, 25.10 cushion; sec. 4.1.1), and the
    dollar-duration rebalancing ratio (sec. 4.1.1.5). Handbook chap. 9: equivalent taxable yield 10%
    (6% at a 40% rate). Original, on an invented annual zero curve (3.00% + 0.15% x years to 10
    years, flat after): an expected-return model for a benchmark, leverage through repo with a
    haircut, after-tax comparison of municipal and taxable bonds, a cash-flow-matched portfolio and
    a ladder with its key-rate profile and twist risk under equal-face, equal-market-value and
    equal-risk allocations, single- and multiple-liability immunisation under parallel shifts and
    twists, a stratified-sampling tracking estimate, curve trades for market-consistent, divergent
    and volatility views, a currency-hedged comparison, and key-rate exposures of a portfolio
    against its benchmark with scenario returns.

    Count convention: one check is one executed ok() call (a call inside a loop counts once per
    iteration).

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
    report = CheckReport()
    check_mandates(report)
    check_leverage_taxation(report)
    check_ladders(report)
    check_immunisation(report)
    check_indexes(report)
    check_curve_positioning(report)
    check_curve_strategy(report)
    print()
    if report.failures:
        print(f"{len(report.failures)} check(s) failed: {report.failures}")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
