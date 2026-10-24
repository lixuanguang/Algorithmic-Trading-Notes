"""FX carry day counts, convexity-hedge carry, OTC derivatives shares, demographic peaks and OFI."""

import math
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Final

from trading_notes.numerical.currency_carry.funded_carry import FundedCarry
from trading_notes.numerical.multi_asset_systematic_macro.market_statistics import (
    AgePopulations,
    OtcNotionals,
)
from trading_notes.numerical.report import CheckReport
from trading_notes.numerical.repository import repository_root

# The data extracts, below the repository root.
DATA: Final = Path("notes/artefacts/multi-asset-systematic-macro")
# (35-69 peak, 15-64 peak) in Gliner's Table 12.2, as macro_pricing_risk_checks part 15 reads it.
GLINER: Final = {
    "Germany": (2006, 1986),
    "Japan": (2016, 1992),
    "Netherlands": (2012, 1989),
    "United Kingdom": (2012, 2009),
    "United States": (2016, 2007),
    "China": (2032, 2011),
    "Korea": (2023, 2015),
    "Russia": (2025, 2011),
    "Spain": (2022, 2004),
    "India": (2050, 2027),
    "Indonesia": (2050, 2023),
    "Nigeria": (2050, 2050),
    "Philippines": (2050, 2037),
}


def check(report: CheckReport, name: str, got: float, want: float, tol: float) -> None:
    """Check |got - want| <= tol, printing got to eight decimals with want and tol as given."""
    report.ok(name, abs(got - want) <= tol, f"{got:.8f} (want {want}, tol {tol})")


def check_fx_carry(report: CheckReport) -> None:
    """1. FX carry with separate accrual fractions: parity, funded P&L and log excess return."""
    print("1. FX carry, unequal day-count bases")
    position = FundedCarry(spot=1.0, domestic_rate=0.05, foreign_rate=0.02, days=90)
    S0, i_d, i_f = position.spot, position.domestic_rate, position.foreign_rate
    tau_d, tau_f = position.tau_d, position.tau_f
    F = position.forward()
    check(report, "tau_f", tau_f, 0.246575, 5e-7)
    check(report, "F/S0", F / S0, 1.0075314, 5e-8)
    carry = position.pnl(S0)
    check(report, "carry = i_f tau_f - i_d tau_d (%)", 100 * carry, -0.75685, 5e-6)
    check(report, "carry identity", carry, i_f * tau_f - i_d * tau_d, 1e-15)
    check(report, "common-basis carry would be (%)", 100 * (i_f - i_d) * tau_d, -0.75, 1e-12)
    check(
        report, "hedged at F gives zero", F / S0 * (1 + i_f * tau_f) - (1 + i_d * tau_d), 0.0, 1e-15
    )
    s = 0.01
    P = position.pnl(S0 * (1 + s))
    check(report, "Pi(+1%) exact (%)", 100 * P, 0.24808, 5e-6)
    check(report, "Pi = carry + s + s i_f tau_f", P, carry + s + s * i_f * tau_f, 1e-15)
    check(report, "first order carry + s (%)", 100 * (carry + s), 0.24315, 5e-6)
    x = position.log_excess(s)
    check(report, "log excess x (%)", 100 * x, 0.24472, 5e-6)
    check(report, "e^x - 1 = Pi/(1 + i_d tau_d)", math.exp(x) - 1, P / (1 + i_d * tau_d), 1e-15)
    r_d, r_f = math.log(1 + i_d * tau_d) / tau_d, math.log(1 + i_f * tau_f) / tau_d
    check(report, "x with cc rates on common tau", math.log(1 + s) + (r_f - r_d) * tau_d, x, 1e-15)
    check(
        report,
        "forward premium exact",
        (F - S0) / S0,
        (i_d * tau_d - i_f * tau_f) / (1 + i_f * tau_f),
        1e-15,
    )


def price(c: float, y: float, n: int) -> float:
    """Return the price of an n-year annual bond paying c per 100 at a flat yield y."""
    return sum(c / (1 + y) ** t for t in range(1, n + 1)) + 100 / (1 + y) ** n


def dv01(c: float, y: float, n: int) -> float:
    """Return the price change for a 1 bp fall in yield, by a central difference."""
    return (price(c, y - 1e-4, n) - price(c, y + 1e-4, n)) / 2


def check_convexity_carry(report: CheckReport) -> None:
    """2. Zero carry of the DV01-hedged convexity position on a flat 4% curve."""
    print("2. Convexity hedge carry on a flat 4% curve")
    k = dv01(4, 0.04, 10) / dv01(4, 0.04, 2)
    check(report, "hedge ratio k", k, 4.30, 0.005)
    check(report, "10y at par", price(4, 0.04, 10), 100.0, 1e-9)
    check(report, "2y at par", price(4, 0.04, 2), 100.0, 1e-9)
    # Per 100 of 10y face, one year: receive the 10y coupon 4, pay the short 2y coupons 4k; the
    # short's proceeds 100k earn the 4% rebate and the long's 100 is financed at 4%, a net
    # 4k - 4 = 4(k - 1).
    coupon_long, fin_long, coupons_short, rebate = 4.0, 4.0, 4.0 * k, 4.0 * k
    carry_conv = coupon_long - coupons_short + (rebate - fin_long)
    check(report, "carry 4 - 4k + 4(k-1)", carry_conv, 4 - 4 * k + 4 * (k - 1), 1e-12)
    check(report, "carry is zero", carry_conv, 0.0, 1e-12)
    for kk in (1.0, 2.5, 7.0):
        check(report, f"zero for k={kk}", 4 - 4 * kk + 4 * (kk - 1), 0.0, 1e-12)
    for dy in (0.01, -0.01):
        g = (price(4, 0.04 + dy, 10) - 100) - k * (price(4, 0.04 + dy, 2) - 100)
        check(report, f"hedged P&L for {dy:+.2f}", g, 0.274 if dy > 0 else 0.302, 0.0015)


def check_swaps_share(report: CheckReport, bis: OtcNotionals) -> None:
    """3. Interest rate swaps within the BIS OTC interest rate derivatives."""
    print("3. BIS interest rate derivatives by instrument")
    for per in ("2024-S1", "2025-S2"):
        ird = bis[(per, "D", "A")]
        parts = sum(bis[(per, "D", i)] for i in "MNRZ")
        check(report, f"{per} instruments sum to IRD total", parts, ird, 0.01)
        total = bis[(per, "A", "A")]
        print(
            f"  {per}: all OTC {total:.1f}tn, IRD {ird:.1f}tn ({100 * ird / total:.1f}%), "
            f"swaps {bis[(per, 'D', 'N')]:.1f}tn ({100 * bis[(per, 'D', 'N')] / ird:.1f}% of IRD), "
            f"FRAs {100 * bis[(per, 'D', 'M')] / ird:.1f}%,"
            f" options {100 * bis[(per, 'D', 'R')] / ird:.1f}%"
        )
    check(report, "2024-S1 IRD matches the release's $579tn", bis[("2024-S1", "D", "A")], 579, 0.5)
    check(
        report,
        "2025-S2 swap share of IRD (%)",
        100 * bis[("2025-S2", "D", "N")] / bis[("2025-S2", "D", "A")],
        81.4,
        0.05,
    )


def check_population_peaks(report: CheckReport, pop: AgePopulations) -> None:
    """4. Peak years of the 15-64 and 35-69 populations of Gliner's Table 12.2 countries.

    Raises:
        ValueError: If a country's extract does not cover every year from 1950 to 2100.
    """
    print("4. UN WPP 2024 peak years")
    peaks = {}
    for c, (g_prime, g_work) in GLINER.items():
        if sorted(pop.years[c]) != list(range(1950, 2101)):
            raise ValueError(f"{c}: the extract does not cover 1950-2100")
        peaks[c] = (
            pop.peak_year(c, 0, 2100),
            pop.peak_year(c, 1, 2100),
            pop.peak_year(c, 0, 2050),
            pop.peak_year(c, 1, 2050),
        )
        print(
            f"  {c:15} 15-64 peak {peaks[c][0]} (to 2050: {peaks[c][2]}; Gliner {g_work});"
            f"  35-69 peak {peaks[c][1]} (to 2050: {peaks[c][3]}; Gliner {g_prime})"
        )
    check(report, "Japan 15-64 peak", peaks["Japan"][0], 1995, 0)
    check(report, "Germany 35-69 peak", peaks["Germany"][1], 2024, 0)
    check(report, "United States 15-64 still rising in 2100", peaks["United States"][0], 2100, 0)
    check(report, "China 15-64 peak", peaks["China"][0], 2015, 0)


def e_cks(
    pb0: float, qb0: int, pb1: float, qb1: int, pa0: float, qa0: int, pa1: float, qa1: int
) -> int:
    """Return Cont, Kukanov and Stoikov's e_n for one change of the best quotes."""
    return (pb1 >= pb0) * qb1 - (pb1 <= pb0) * qb0 - (pa1 <= pa0) * qa1 + (pa1 >= pa0) * qa0


def of_ccz(p0: float, q0: int, p1: float, q1: int, side: str) -> int:
    """Return Cont, Cucuringu and Zhang's printed OF^{m,b} ("b") or OF^{m,a} for one side."""
    if side == "b":
        return q1 if p1 > p0 else (q1 - q0 if p1 == p0 else -q1)
    return -q1 if p1 > p0 else (q1 - q0 if p1 == p0 else q1)


def check_ofi(report: CheckReport) -> None:
    """5. Best-quote flow when the bid moves away: old size against new size."""
    print("5. OFI conventions on one bid move")
    # bid falls from 100.00 x 300 to 99.99 x 500; ask unchanged at 100.01 x 400
    cks = e_cks(100.00, 300, 99.99, 500, 100.01, 400, 100.01, 400)
    ccz = of_ccz(100.00, 300, 99.99, 500, "b") - of_ccz(100.01, 400, 100.01, 400, "a")
    check(report, "CKS: bid falls, minus the old size", cks, -300, 0)
    check(report, "CCZ: bid falls, minus the new size", ccz, -500, 0)
    # unchanged prices: both give the size changes
    check(
        report,
        "same when prices unchanged",
        e_cks(100, 300, 100, 350, 101, 400, 101, 380),
        of_ccz(100, 300, 100, 350, "b") - of_ccz(101, 400, 101, 380, "a"),
        0,
    )


def check_make_take(report: CheckReport) -> None:
    """6. Foucault, Kadan and Kandel's Proposition 4 against Lehalle and Laruelle's (A.4)."""
    print("6. FKK Proposition 4 and Lehalle-Laruelle (A.4)")
    for D, L, cbar, M, N, beta, gamma in [
        (0.01, 0.05, 0.003, 50, 100, 1.0, 2.0),
        (0.02, 0.03, 0.001, 200, 20, 3.0, 0.5),
    ]:
        q, r = M / N, gamma / beta
        cm_fkk = 0.5 * (D - 2 * (L - cbar) / (1 + (q * r) ** (1 / 3)))
        pim, pit = (L - cbar) / (1 + (q * r) ** (1 / 3)), (L - cbar) / (1 + (q * r) ** (-1 / 3))
        cm_ll = D / 2 - (L - cbar) / (1 + (M / N * gamma / beta) ** (1 / 3))
        check(report, f"c_m FKK = LL (Delta={D}, M/N={q})", cm_fkk, cm_ll, 1e-15)
        check(report, "pi_m + pi_t = L - cbar", pim + pit, L - cbar, 1e-15)
        check(report, "pi_m = Delta/2 - c_m", pim, D / 2 - cm_fkk, 1e-15)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the six parts with one report, printing the failures last.

    1. FX carry with separate accrual fractions (macro-fx.tex, mod:fx-carry-trade): covered
       parity, exact funded P&L, carry, first-order forms and the continuously compounded log
       excess return, for 90 days at 5% ACT/360 against 2% ACT/365.
    2. Zero carry of the DV01-hedged convexity position (interest-rates.tex, Practice): long 100
       face of a 10-year 4% annual-coupon bond at par, short k times the face of a 4% 2-year
       bond at par, flat 4% curve, financing and rebate both at 4%: carry 4 - 4k + 4(k - 1) = 0
       for any k, with k = 4.30 from the DV01 ratio.
    3. Interest rate swaps within the BIS OTC interest rate derivatives
       (monetary-policy-curves.tex, swaps entry): bis-otc-ird-instruments.csv is an extract of
       the BIS bulk file WS_OTC_DERIV2_csv_flat.zip (data.bis.org, retrieved 2026-10-16, sha256
       49e5b5c5...a67e923): half-yearly notional outstanding, all reporting countries, all
       counterparties, all currencies and maturities, net-net basis, USD millions.
    4. Peak years of the 15-64 and 35-69 populations (macro-regimes-data.tex, Gliner's Table
       12.2 countries): wpp2024-working-prime-age.csv sums five-year age groups of the UN World
       Population Prospects 2024, medium variant, file
       WPP2024_PopulationByAge5GroupSex_Medium.csv.gz (population.un.org, retrieved 2026-10-16,
       sha256 a04d7d14...2487cd), 1 July populations 1950-2100 (estimates to 2023, projections
       after). Peaks are taken over 1950-2100 and, for comparison with Gliner's table, which
       stops at 2050, over 1950-2050.
    5. Best-quote flow when a price moves away (order-books.tex, def:order-flow-imbalance): Cont,
       Kukanov and Stoikov's e_n uses the old size, Cont, Cucuringu and Zhang's printed
       OF^{m,b} the new one.
    6. Foucault, Kadan and Kandel's Proposition 4 (high-frequency-trading.tex,
       mod:make-take-fee-speed-race) against Lehalle and Laruelle's (A.4), with
       s*Delta = Delta_FKK/2, Gamma = L and r = gamma/beta.

    Args:
        argv: Command-line arguments: `--root DIR`, the repository root that holds the data
            (default: the working directory).

    Returns:
        The exit status, 0 or 1.
    """
    root = repository_root(__doc__ or "", argv)
    bis = OtcNotionals.read(root / DATA / "bis-otc-ird-instruments.csv")
    pop = AgePopulations.read(root / DATA / "wpp2024-working-prime-age.csv")
    report = CheckReport()
    check_fx_carry(report)
    check_convexity_carry(report)
    check_swaps_share(report, bis)
    check_population_peaks(report, pop)
    check_ofi(report)
    check_make_take(report)
    print("FAILURES:", report.failures if report.failures else "none")
    return 1 if report.failures else 0


if __name__ == "__main__":
    sys.exit(main())
