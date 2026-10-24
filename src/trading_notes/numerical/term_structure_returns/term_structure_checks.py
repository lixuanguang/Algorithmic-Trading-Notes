"""Term structure and yield-curve dynamics: curves, break-evens, theories and factor exposures."""

import math
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Final

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.report import CheckReport, print_versions
from trading_notes.numerical.repository import repository_root
from trading_notes.numerical.term_structure_returns.curve_bootstrap import (
    AnnualCurve,
    MonthEndYields,
    PrincipalComponents,
    bootstrap,
)
from trading_notes.numerical.tolerance import close
from trading_notes.records import Record

type Floats = NDArray[np.float64]

DATA: Final = Path("notes/artefacts/term-structure-dynamics/gsw-month-end-zero.csv")
MATS: Final = (1, 2, 3, 5, 7, 10, 20, 30)
N: Final = np.arange(1, 6)
PAR: Final = np.array([0.0380, 0.0400, 0.0415, 0.0425, 0.0430])


class RisingCurve(Record):
    """The invented rising par curve of part 1, bootstrapped, as part 2 reads it.

    Attributes:
        curve: Discount factors, spot rates and one-year forwards.
        forward_one_year: The spot curve one year forward, f(1, 2..5).
    """

    curve: AnnualCurve
    forward_one_year: Floats


def check_curves(report: CheckReport) -> RisingCurve:
    """Part 1: par to spot to forward, and back.

    Args:
        report: The run's report.

    Returns:
        The bootstrapped curve and its spot curve one year forward, for part 2.
    """
    print("== part 1: par -> spot -> forward, and back")
    par, n = PAR, N
    curve = AnnualCurve.from_par(par)
    df, spot, fwd = curve.discount, curve.spot, curve.forward
    print(
        f"    DF {np.round(df, 6)}\n    spot {np.round(100 * spot, 4)}\n    fwd "
        f" {np.round(100 * fwd, 4)}"
    )
    report.ok(
        "every par bond reprices to 100 from the bootstrapped discount factors",
        all(
            close(100 * c * df[: k + 1].sum() + 100 * df[k], 100, 1e-10) for k, c in enumerate(par)
        ),
    )
    report.ok(
        "spot 3.8000, 4.0040, 4.1591, 4.2636, 4.3155%",
        np.allclose(100 * spot, [3.8, 4.0040, 4.1591, 4.2636, 4.3155], atol=5e-5),
    )
    report.ok(
        "one-year forwards 3.8000, 4.2084, 4.4700, 4.5777, 4.5235%",
        np.allclose(100 * fwd, [3.8, 4.2084, 4.4700, 4.5777, 4.5235], atol=5e-5),
    )
    report.ok(
        "spot rates are geometric averages of forwards: (1+s_n)^n = prod(1+f)",
        np.allclose((1 + spot) ** n, np.cumprod(1 + fwd), rtol=0, atol=1e-13),
    )
    par_back = np.array([(1 - df[k]) / df[: k + 1].sum() for k in range(5)])
    report.ok(
        "par yields recovered from the spot curve: c_n = (1 - DF_n)/sum DF",
        np.allclose(par_back, par, atol=1e-13),
    )
    report.ok(
        "on this rising curve forward >= spot >= par at every maturity beyond one year",
        all(fwd[k] >= spot[k] >= par[k] for k in range(1, 5)),
    )
    report.ok(
        "the forward curve turns down at 5 years while spot and par still rise (forwards magnify"
        " slope changes)",
        bool(fwd[4] < fwd[3] and spot[4] > spot[3] and par[4] > par[3]),
    )
    # A 5-year 6% annual bond priced three ways
    cf = np.array([6, 6, 6, 6, 106.0])
    p_spot = float(np.sum(cf / (1 + spot) ** n))
    p_fwd = float(np.sum(cf / np.cumprod(1 + fwd)))
    p_df = float(cf @ df)
    lo, hi = 0.0, 0.2
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if np.sum(cf / (1 + mid) ** n) > p_df:
            lo = mid
        else:
            hi = mid
    ytm6 = 0.5 * (lo + hi)
    report.ok(
        "6% bond: 107.5286 by spot rates, by forwards and by discount factors",
        abs(p_spot - 107.5286) < 5e-5
        and close(p_spot, p_fwd, 1e-10)
        and close(p_spot, p_df, 1e-10),
    )
    report.ok(
        "its yield 4.2948% is below the 4.3155% 5-year spot: a coupon bond's yield averages in the"
        " lower short spots",
        bool(abs(ytm6 - 0.042948) < 5e-6 and ytm6 < spot[4]),
    )
    inv_par = np.array([0.0500, 0.0480, 0.0460, 0.0450, 0.0440])
    inverted = AnnualCurve.from_par(inv_par)
    spot_i, fwd_i = inverted.spot, inverted.forward
    report.ok(
        "on an inverted curve the order reverses: par >= spot >= forward",
        all(inv_par[k] >= spot_i[k] >= fwd_i[k] for k in range(1, 5)),
    )
    f1n = ((1 + spot[1:]) ** n[1:] / (1 + spot[0])) ** (1 / (n[1:] - 1)) - 1
    report.ok(
        "implied spot curve one year forward: f(1,2..5) = 4.2084, 4.3391, 4.4186, 4.4448%",
        np.allclose(100 * f1n, [4.2084, 4.3391, 4.4186, 4.4448], atol=5e-5),
    )
    return RisingCurve(curve=curve, forward_one_year=f1n)


def check_break_evens(report: CheckReport, rising: RisingCurve) -> None:
    """Part 2: forwards as break-evens; rolling yield.

    Args:
        report: The run's report.
        rising: The curve of part 1.
    """
    print("== part 2: forwards as break-evens; rolling yield")
    df, spot, fwd = rising.curve.discount, rising.curve.spot, rising.curve.forward
    f1n, par = rising.forward_one_year, PAR
    s1, s2 = 0.06, 0.0808
    f12 = (1 + s2) ** 2 / (1 + s1) - 1
    report.ok("Ilmanen: s1 6%, s2 8.08% -> f(1,2) = 10.20%", abs(f12 - 0.1020) < 5e-5)
    p2_now, p2_next = 100 / (1 + s2) ** 2, 100 / (1 + f12)
    report.ok(
        "if 10.20% is realised the 2-year zero earns exactly the 6% one-year rate (85.61 -> 90.74)",
        abs(p2_now - 85.61) < 5e-3
        and abs(p2_next - 90.74) < 5e-3
        and close(p2_next / p2_now - 1, s1, 1e-12),
    )
    report.ok("break-even rise in the one-year rate: 420 bp", abs(f12 - s1 - 0.0420) < 5e-5)
    # Forwards realised: every zero earns s1 in year 1; unchanged curve: the n-year zero earns
    # f(n-1, n)
    ret_fwd = [(1 / (1 + f1n[k - 2]) ** (k - 1)) / df[k - 1] - 1 for k in range(2, 6)]
    report.ok(
        "forwards realised: the 2- to 5-year zeros all earn the 3.80% one-year rate",
        np.allclose(ret_fwd, par[0], atol=1e-12),
    )
    ret_unch = [(1 / (1 + spot[k - 2]) ** (k - 1)) / df[k - 1] - 1 for k in range(2, 6)]
    report.ok(
        "unchanged curve: the n-year zero earns the one-year forward f(n-1,n) (its rolling yield)",
        np.allclose(ret_unch, fwd[1:], atol=1e-12),
    )
    approx = [spot[k - 1] + (k - 1) * (spot[k - 1] - spot[k - 2]) for k in range(2, 6)]
    report.ok(
        "Ilmanen's approximation f ~ s_n + (n-1)(s_n - s_(n-1)) is within 2 bp here",
        bool(np.max(np.abs(np.array(approx) - fwd[1:])) < 2e-4),
    )
    report.ok(
        "Ilmanen's Appendix 31C examples: 10.16 vs 10.20, 13.00 vs 13.07, 14.28 vs 14.36, 13.76 vs"
        " 13.77",
        abs(8.08 + 1 * (8.08 - 6.00) - 10.16) < 1e-9
        and abs(9.72 + 2 * (9.72 - 8.08) - 13.00) < 1e-9
        and abs(10.86 + 3 * (10.86 - 9.72) - 14.28) < 1e-9
        and abs(11.44 + 4 * (11.44 - 10.86) - 13.76) < 1e-9,
    )
    # Riding the curve: buy the 5-year zero, hold one year. Unchanged curve: 4.5244% against 3.80%
    # on the 1-year. If the curve instead rises in parallel by 50 bp, the 5-year zero returns less
    # than the 1-year.
    r_up50 = (1 / (1 + spot[3] + 0.005) ** 4) / df[4] - 1
    report.ok(
        "riding: 5-year zero over one year returns 4.5235% if the curve is unchanged, 2.5423% if it"
        " rises 50 bp",
        bool(abs(ret_unch[-1] - 0.045235) < 5e-6 and abs(r_up50 - 0.025423) < 5e-6),
    )
    be = ((1 / df[4]) / (1 + par[0])) ** (1 / 4) - 1 - spot[3]
    report.ok(
        "break-even rise for the ride is 18.1 bp in the 4-year spot, the forward-implied change"
        " f(1,5) - s4",
        bool(abs(be - (f1n[-1] - spot[3])) < 1e-12 and abs(be - 0.001812) < 5e-6),
    )


def check_theories(report: CheckReport) -> None:
    """Part 3: theories - convexity bias and a liquidity premium.

    Args:
        report: The run's report.
    """
    print("== part 3: theories - convexity bias and a liquidity premium")
    # Two periods; the one-year rate in year 2 is 3% or 7% with equal probability; expected 5%.
    r1, ru, rd = 0.05, 0.07, 0.03
    E_r2 = 0.5 * (ru + rd)
    # Local expectations: the 2-year zero earns r1 in expectation over year 1, so
    # P2 = E[1/(1+r2)] / (1+r1)
    P2_leh = 0.5 * (1 / (1 + ru) + 1 / (1 + rd)) / (1 + r1)
    f_leh = (1 / (1 + r1)) / P2_leh - 1
    report.ok(
        "local expectations: f(1,2) = 4.9619% < 5.00% expected rate (convexity bias 3.8 bp)",
        abs(f_leh - 0.049619) < 5e-6 and f_leh < E_r2,
    )
    P2_ueh = 1 / ((1 + r1) * (1 + E_r2))
    ret_ueh = 0.5 * ((1 / (1 + ru)) + (1 / (1 + rd))) / P2_ueh - 1
    report.ok(
        "unbiased expectations (forward = 5%): the 2-year zero then expects 5.0381%, more than the"
        " 5% short rate",
        abs(ret_ueh - 0.050381) < 5e-6 and ret_ueh > r1,
    )
    # Liquidity premium: flat expected short rates 4%, premium 0.10% per year of maturity added to
    # each forward
    exp_short = np.full(5, 0.04)
    lp = 0.001 * np.arange(5)
    fwd_lp = exp_short + lp
    spot_lp = np.cumprod(1 + fwd_lp) ** (1 / N) - 1
    report.ok(
        "flat expected rates plus a rising liquidity premium give an upward-sloping spot curve",
        bool(np.all(np.diff(spot_lp) > 0)),
    )


def check_swap_curve(report: CheckReport) -> None:
    """Part 4: swap curve and swap spread.

    Args:
        report: The run's report.
    """
    print("== part 4: swap curve and swap spread")
    swap = np.array([0.0360, 0.0350, 0.0355, 0.0365, 0.0375])  # annual SOFR OIS par rates, invented
    df_sw = bootstrap(swap)
    report.ok(
        "SOFR OIS par rates bootstrap to discount factors that price each par swap's fixed leg at"
        " par",
        all(close(swap[k] * df_sw[: k + 1].sum() + df_sw[k], 1, 1e-12) for k in range(5)),
    )
    tsy5, sw5 = 0.0405, swap[4]
    report.ok(
        "5-year swap spread = swap rate - Treasury yield = 3.75% - 4.05% = -30 bp",
        bool(abs((sw5 - tsy5) + 0.0030) < 1e-12),
    )
    fwd_sw = np.r_[df_sw[0] ** -1, df_sw[:-1] / df_sw[1:]] - 1
    report.ok(
        "the swap curve's one-year forwards 3.60, 3.40, 3.66, 3.97, 4.19%: a dip priced for policy"
        " easing",
        np.allclose(100 * fwd_sw, [3.6, 3.3966, 3.6554, 3.9732, 4.1909], atol=5e-5),
    )


def check_factor_exposures(report: CheckReport) -> None:
    """Part 5: factor exposures (Hull, sec. 22.9) and a two-factor hedge.

    Args:
        report: The run's report.
    """
    print("== part 5: factor exposures (Hull, sec. 22.9) and a two-factor hedge")
    L = np.array(
        [  # Hull Table 22.9: rows 1, 2, 3, 5, 7, 10, 20, 30 years; columns PC1..PC8
            [0.083, -0.242, 0.685, -0.682, -0.006, -0.025, -0.021, -0.004],
            [0.210, -0.465, 0.376, 0.574, -0.517, -0.031, 0.011, -0.008],
            [0.286, -0.467, 0.006, 0.185, 0.728, 0.347, 0.106, -0.074],
            [0.386, -0.315, -0.332, -0.145, 0.061, -0.604, -0.348, 0.361],
            [0.430, -0.099, -0.349, -0.265, -0.266, -0.008, 0.263, -0.688],
            [0.428, 0.119, -0.153, -0.172, -0.269, 0.515, 0.254, 0.589],
            [0.426, 0.394, 0.172, 0.099, 0.027, 0.244, -0.722, -0.205],
            [0.411, 0.478, 0.323, 0.204, 0.234, -0.434, 0.461, 0.036],
        ]
    )
    sd_scores = np.array([11.54, 3.55, 1.78, 1.25, 0.91, 0.69, 0.62, 0.57])
    var_share = sd_scores**2 / np.sum(sd_scores**2)
    report.ok(
        "Hull: PC1 explains 87.3% of variance, PC1+PC2 95.6%, PC3 a further 2.1%",
        bool(
            abs(var_share[0] - 0.873) < 5e-4
            and abs(var_share[:2].sum() - 0.956) < 5e-4
            and abs(var_share[2] - 0.021) < 5e-4
        ),
    )
    expo = np.zeros(8)
    expo[[1, 2, 3, 4, 5]] = [10, 4, -8, -7, 2]  # $ millions per bp at 2, 3, 5, 7, 10 years
    fexp = expo @ L[:, :2]
    sd_dP = math.sqrt((fexp**2) @ sd_scores[:2] ** 2)
    hull_sd = math.sqrt(1.99**2 * 11.54**2 + 3.06**2 * 3.55**2)
    report.ok(
        "Hull's portfolio: exposures -1.998 and -3.067 (printed -1.99, -3.06); sd 25.50 unrounded,"
        " 25.40 from the printed\n      exposures; Hull prints 25.45, and 2.326 x 25.45 = 59.2 is"
        " his one-day 99% VaR",
        np.allclose(fexp, [-1.998, -3.067], atol=5e-4)
        and abs(sd_dP - 25.498) < 0.001
        and abs(hull_sd - 25.404) < 0.001
        and abs(2.326 * 25.45 - 59.2) < 0.005,
    )
    # Hedge both factors with positions h2, h10 in 2- and 10-year instruments ($m per bp each = 1
    # per unit)
    A = L[[1, 5], :2].T  # rows: factor; columns: instrument
    h = np.linalg.solve(A, -fexp)
    new = expo.copy()
    new[1] += h[0]
    new[5] += h[1]
    report.ok(
        "a 2-year position of -4.80 and a 10-year position of +7.02 ($m per bp) remove both factor"
        " exposures",
        np.allclose(new @ L[:, :2], 0, atol=1e-12) and np.allclose(h, [-4.7985, 7.0226], atol=5e-4),
    )
    resid_sd = math.sqrt(((new @ L[:, 2:]) ** 2) @ sd_scores[2:] ** 2)
    total_sd = math.sqrt(((expo @ L) ** 2) @ sd_scores**2)
    report.ok(
        "residual risk from factors 3-8 remains: sd 14.88 against 32.30 unhedged across all eight"
        " factors",
        abs(resid_sd - 14.88) < 0.005 and abs(total_sd - 32.30) < 0.005,
    )


def check_gsw_history(report: CheckReport, history: MonthEndYields) -> None:
    """Part 6: GSW month-end zero yields, January 1986 - September 2026.

    Args:
        report: The run's report.
        history: The month-end zero yields.
    """
    print("== part 6: GSW month-end zero yields, January 1986 - September 2026")
    dates, mats = history.dates, list(history.maturities)
    dY = 100 * np.diff(history.yields, axis=0)  # monthly changes in basis points
    report.ok(
        "489 month-ends, first 1986-01-31, last 2026-09-30",
        len(dates) == 489 and dates[0] == "1986-01-31" and dates[-1] == "2026-09-30",
    )
    pcs = PrincipalComponents.of(dY)
    share, eigvec = pcs.shares(), pcs.loadings
    sign_changes = [int(np.sum(np.diff(np.sign(eigvec[:, k])) != 0)) for k in range(3)]
    print(f"    variance shares {np.round(100 * share[:4], 2)}; sign changes {sign_changes}")
    print(
        f"    PC1 {np.round(eigvec[:, 0], 3)}\n    PC2 {np.round(eigvec[:, 1], 3)}\n    PC3"
        f" {np.round(eigvec[:, 2], 3)}"
    )
    report.ok(
        "PC1 is a level shift (no sign change), PC2 a slope (one), PC3 a curvature (two)",
        sign_changes == [0, 1, 2],
    )
    report.ok(
        "PC1 explains 85.3%, PC2 10.7%, PC3 2.5% of the variance of monthly changes",
        bool(
            abs(share[0] - 0.8528) < 5e-4
            and abs(share[1] - 0.1071) < 5e-4
            and abs(share[2] - 0.0246) < 5e-4
        ),
    )
    vol = dY.std(axis=0, ddof=1)
    print(
        "    sd of monthly changes (bp) by maturity"
        f" {dict(zip(mats, np.round(vol, 1), strict=True))}"
    )

    def sub_vol(a: str, b: str) -> Floats:
        idx = [i for i in range(1, len(dates)) if a <= dates[i][:7] <= b]
        return np.asarray(dY[np.array(idx) - 1].std(axis=0, ddof=1), dtype=np.float64)

    v_pre, v_zlb, v_post = (
        sub_vol("1986-02", "2007-12"),
        sub_vol("2009-01", "2015-11"),
        sub_vol("2016-01", "2026-09"),
    )
    print(
        f"    1986-2007 {np.round(v_pre, 1)}\n    2009-2015 {np.round(v_zlb, 1)}\n    2016-2026"
        f" {np.round(v_post, 1)}"
    )
    report.ok(
        "full sample: yield volatility is humped, 24.5 bp at 1 year, 28.7 at 5 years, 25.5 at 30"
        " years",
        int(np.argmax(vol)) == mats.index(5)
        and int(np.argmin(vol)) == 0
        and np.allclose(vol[[0, 3, 7]], [24.5, 28.7, 25.5], atol=0.05),
    )
    report.ok(
        "near the zero bound (2009 - Nov 2015) the 1-year yield barely moved: sd 7.2 bp against"
        " 25.9 bp at 10 years;\n      1986-2007 the 1-year sd was 27.5 bp",
        bool(
            abs(v_zlb[0] - 7.2) < 0.05
            and abs(v_zlb[5] - 25.9) < 0.05
            and abs(v_pre[0] - 27.5) < 0.05
        ),
    )
    dur = np.array(mats, dtype=float)  # zero-coupon durations in years
    pvol = dur * vol / 100
    report.ok(
        "price volatility ~ duration x yield volatility: monthly sd about 0.24% for the 1-year"
        " zero, 7.6% for the 30-year",
        bool(abs(pvol[0] - 0.245) < 0.005 and abs(pvol[-1] - 7.64) < 0.01),
        f"{np.round(pvol, 2)}",
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Read the GSW month-end yields from the repository root, then run the six parts.

    The worked numbers of meth:spot-par-forward-curves, meth:forward-rates-expected-returns,
    def:swap-curve-short-term-spreads, res:term-structure-theories and
    meth:yield-curve-factor-exposures.

    Part 1 bootstraps an invented annual par curve (on a coupon date, annual coupons) into
    discount factors, spot and one-year forward rates, reprices every input bond, and prices a 6%
    bond three ways. Part 2 reproduces Ilmanen's break-even example (Fabozzi (ed.), Handbook of
    Fixed Income Securities, 9th ed., 2021, chap. 31, pp. 695 and 711-713) and checks the
    rolling-yield and forwards-realised identities. Part 3 shows the convexity bias that separates
    the local and unbiased expectations hypotheses in a two-state example, and a liquidity premium.
    Part 4 computes a swap spread and swap-curve discount factors. Part 5 reproduces Hull's
    principal-components exposure example (Options, Futures, and Other Derivatives, 11th Global
    ed., sec. 22.9, Tables 22.9-22.11) and hedges two factors with two instruments. Part 6 runs a
    principal-components analysis and a volatility-by-maturity table on month-end
    Gurkaynak-Sack-Wright zero yields, January 1986 to September 2026 (gsw-month-end-zero.csv,
    produced by trading_notes.research.term_structure_returns.gsw_month_end from the Board's
    feds200628.csv).

    Args:
        argv: Command-line arguments: `--root DIR`, the repository root that holds the data
            (default: the working directory).

    Returns:
        The exit status, 0 or 1.
    """
    root = repository_root(__doc__ or "", argv)
    print_versions(np)
    history = MonthEndYields.read(root / DATA, MATS)
    report = CheckReport()
    rising = check_curves(report)
    check_break_evens(report, rising)
    check_theories(report)
    check_swap_curve(report)
    check_factor_exposures(report)
    check_gsw_history(report, history)
    print()
    if report.failures:
        print(f"{len(report.failures)} check(s) failed: {report.failures}")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
