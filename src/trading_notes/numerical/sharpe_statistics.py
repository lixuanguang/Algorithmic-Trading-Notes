"""Checks behind meth:sharpe-ratio-standard-error and meth:deflated-sharpe-ratio.

Source verification (2026-10-17).

1. Lo (2002), FAJ 58(4), eq. (9), p. 38: SE(SR) = sqrt((1 + SR^2/2)/T) under IID returns; his
   examples for T = 60 (0.188 at SR 1.50, 0.303 at SR 3.00).
2. Lo, eqs. (20) and (22), pp. 40-41: eta(q) = q / sqrt(q + 2 sum_{k=1}^{q-1} (q-k) rho_k), and
   for AR(1) returns (rho_k = rho^k) the closed form (22); against Table 2 (p. 41) at q = 12:
   4.17 (rho = -0.2), 3.46 (0), 2.88 (0.2), and a sample of other cells. A Monte Carlo AR(1)
   check of the IID standard error's understatement is not claimed.
3. Bailey and Lopez de Prado, author version of 31 July 2014, eqs. (1)-(2), pp. 7-8, and the
   numerical example, pp. 9-10: SR0 = 0.1132 (non-annualised, 250 observations a year) and
   DSR = 0.9004 for N = 100, V = 1/2 annualised, T = 1250, skewness -3, kurtosis 10, SR = 2.5
   annualised; DSR = 0.9505 at N = 46; and with normal returns (skewness 0, kurtosis 3)
   DSR = 0.9505 "after N = 88".
Run: uv run --frozen --no-editable python -m trading_notes.numerical.sharpe_statistics
(scipy). Exits non-zero on failure.
"""

import math
import sys
from typing import Final

from scipy.stats import norm

from trading_notes.numerical.report import CheckReport

# Lo's Table 2, (q, rho) -> eta(q): the three q = 12 cells quoted in the text and a sample.
TABLE_2: Final = {
    (12, -0.2): 4.17,
    (12, 0.0): 3.46,
    (12, 0.2): 2.88,
    (2, 0.9): 1.03,
    (250, -0.9): 67.65,
    (24, 0.5): 2.91,
    (48, -0.5): 11.84,
    (6, 0.1): 2.25,
}
EULER_GAMMA: Final = 0.5772156649015329  # Euler-Mascheroni
# Bailey and Lopez de Prado's example, converted from annual to per-observation units with
# 250 observations a year: the variance of the trials' Sharpe ratios and the observed SR.
EXAMPLE_V: Final = 0.5 / 250
EXAMPLE_SR: Final = 2.5 / math.sqrt(250)
EXAMPLE_T: Final = 1250  # observations behind the observed SR


def near(report: CheckReport, name: str, got: float, want: float, tol: float) -> None:
    """Check |got - want| <= tol and print got to six decimals, with want and tol as given."""
    report.ok(name, abs(got - want) <= tol, f"{got:.6f} (want {want}, tol {tol})")


def se(sr: float, T: int) -> float:
    """Return Lo's IID standard error of a Sharpe ratio, eq. (9)."""
    return math.sqrt((1 + 0.5 * sr * sr) / T)


def eta_sum(q: int, rho: float) -> float:
    """Return eta(q) by eq. (20), summing the AR(1) autocorrelations rho^k term by term."""
    return q / math.sqrt(q + 2 * sum((q - k) * rho**k for k in range(1, q)))


def eta_22(q: int, rho: float) -> float:
    """Return eta(q) for AR(1) returns by the closed form, eq. (22).

    For positive q the closed form is defined at rho = 0: its correction term is
    0 * (1 - 1/q) = 0, so it simplifies to sqrt(q). The rho = 0 branch returns that value
    directly.
    """
    if rho == 0:
        return math.sqrt(q)
    return math.sqrt(q) * math.pow(
        1 + 2 * rho / (1 - rho) * (1 - (1 - rho**q) / (q * (1 - rho))), -0.5
    )


def sr0(N: int, V: float) -> float:
    """Return the expected maximum Sharpe ratio of N trials with variance V, eq. (2)."""
    return math.sqrt(V) * (
        (1 - EULER_GAMMA) * norm.ppf(1 - 1 / N) + EULER_GAMMA * norm.ppf(1 - 1 / (N * math.e))
    )


def dsr(sr: float, s0: float, T: int, g3: float, g4: float) -> float:
    """Return the deflated Sharpe ratio, eq. (1), for skewness g3 and kurtosis g4."""
    return norm.cdf((sr - s0) * math.sqrt(T - 1) / math.sqrt(1 - g3 * sr + (g4 - 1) / 4 * sr * sr))


def check_standard_error(report: CheckReport) -> None:
    """1. Lo's examples of eq. (9) and its large-SR limit."""
    print("== 1. Lo eq. (9)")
    near(report, "SE at SR 1.50, T 60", se(1.5, 60), 0.188, 5e-4)
    near(report, "SE at SR 3.00, T 60", se(3.0, 60), 0.303, 5e-4)
    near(
        report,
        "SE/SR limit sqrt(1/(2T)) at T 60, SR 1e4",
        se(1e4, 60) / 1e4,
        math.sqrt(1 / 120),
        1e-6,
    )


def check_annualisation(report: CheckReport) -> None:
    """2. Eq. (22) against Table 2, and eq. (20) against eq. (22), cell by cell."""
    print("\n== 2. Lo eqs. (20) and (22), Table 2")
    for (q, rho), want in TABLE_2.items():
        near(
            report, f"eta({q}, rho={rho}) by eq. (22) against Table 2", eta_22(q, rho), want, 0.006
        )
        near(
            report,
            f"eta({q}, rho={rho}) eq. (20) = eq. (22)",
            eta_sum(q, rho),
            eta_22(q, rho),
            1e-9,
        )


def check_deflated_sharpe(report: CheckReport) -> None:
    """3. The deflated Sharpe ratio example, and DSR around N = 88 with normal returns."""
    print("\n== 3. Deflated Sharpe ratio, eqs. (1)-(2) and the example")
    near(report, "SR0 at N = 100 (non-annualised)", sr0(100, EXAMPLE_V), 0.1132, 5e-5)
    near(
        report,
        "DSR at N = 100, skew -3, kurtosis 10",
        dsr(EXAMPLE_SR, sr0(100, EXAMPLE_V), EXAMPLE_T, -3, 10),
        0.9004,
        5e-5,
    )
    near(
        report,
        "DSR at N = 46",
        dsr(EXAMPLE_SR, sr0(46, EXAMPLE_V), EXAMPLE_T, -3, 10),
        0.9505,
        5e-5,
    )
    near(
        report,
        "DSR at N = 88 with normal returns",
        dsr(EXAMPLE_SR, sr0(88, EXAMPLE_V), EXAMPLE_T, 0, 3),
        0.9505,
        5e-4,
    )
    around = ", ".join(
        f"{dsr(EXAMPLE_SR, sr0(N, EXAMPLE_V), EXAMPLE_T, 0, 3):.4f}" for N in (87, 88, 89)
    )
    print(f"     normal returns: DSR at N = 87, 88, 89: {around}")


def main() -> int:
    """Run the three parts with one report.

    Returns:
        The exit status, 0 or 1.
    """
    report = CheckReport()
    check_standard_error(report)
    check_annualisation(report)
    check_deflated_sharpe(report)
    if report.failures:
        print("\nFAILED:", report.failures)
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
