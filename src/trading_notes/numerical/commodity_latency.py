"""source verification (2026-10-17) (source-review coverage): arithmetic behind figures added from source documents.

1. USGS Mineral Commodity Summaries, February 2026, Aluminum (p. 2): China's share of world smelter production,
   45,000 of 74,000 thousand tonnes in 2025 (estimated) and 44,000 of 72,800 in 2024 (def:metals-markets).
2. EIA, liquefied U.S. natural gas exports, annual, million cubic feet (release of 30 September 2026): 5,508,984 MMcf in
   2025 as billion cubic feet a day, and the growth from 2,924 MMcf in 2013 (def:natural-gas-market).
3. Moallemi and Saglam (revision of 5 February 2013), p. 23, eq. (13): limit-premium reduction in units of the
   standard deviation over the latency interval, sqrt(log(delta^2 / (2 pi sigma^2 dt))), for GS on 4 January 2010
   (delta = $0.058, sigma = $1.92 a day) at 500, 250 and 50 ms, against their 1.4, 1.6 and 2.1; a trading day of
   6.5 hours (23,400 s) is assumed here, which the paper's calibration does not state. Also the latency cost of
   Corollary 1 at 500 ms for the same parameters (not stated in the paper; computed for orientation only).
Run: uv run --frozen --no-editable python -m trading_notes.numerical.commodity_latency   (standard library).
Exits non-zero on failure.
"""

import math
import sys
from typing import Final

from trading_notes.numerical.report import CheckReport

# Moallemi-Saglam calibration for GS on 4 January 2010: half-spread and daily volatility in
# dollars, and the assumed trading day in seconds.
DELTA: Final = 0.058
SIGMA_DAY: Final = 1.92
DAY_SECONDS: Final = 23_400


def near(report: CheckReport, name: str, got: float, want: float, tol: float) -> None:
    """Check |got - want| <= tol, printing got to four decimals with want and tol as given."""
    report.ok(name, abs(got - want) <= tol, f"{got:.4f} (want {want}, tol {tol})")


def latency_sd(ms: float) -> float:
    """Return the price standard deviation over a latency of ms milliseconds, in dollars."""
    return SIGMA_DAY * math.sqrt(ms / 1000 / DAY_SECONDS)


def premium_reduction(sd: float) -> float:
    """Return eq. (13)'s limit-premium reduction sqrt(log(delta^2 / (2 pi sd^2))), in sd units."""
    return math.sqrt(math.log(DELTA**2 / (2 * math.pi * sd**2)))


def check_aluminium(report: CheckReport) -> None:
    """Check 1: China's share of world aluminium smelter production."""
    print("== 1. USGS aluminium")
    near(report, "China share of 2025 smelter output", 45_000 / 74_000, 0.61, 0.005)
    near(report, "China share of 2024 smelter output", 44_000 / 72_800, 0.60, 0.005)


def check_lng(report: CheckReport) -> None:
    """Check 2: U.S. LNG exports a day in 2025, and their growth since 2013."""
    print("\n== 2. EIA LNG exports")
    near(report, "2025 exports, Bcf per day", 5_508_984 / 365 / 1000, 15.1, 0.05)
    near(report, "2025 / 2013 ratio (thousands)", 5_508_984 / 2_924 / 1000, 1.884, 0.001)


def check_latency_calibration(report: CheckReport) -> None:
    """Check 3: the paper's adjustments at 500, 250 and 50 ms; print the latency cost."""
    print("\n== 3. Moallemi-Saglam calibration")
    for ms, want in ((500, 1.4), (250, 1.6), (50, 2.1)):
        near(
            report,
            f"adjustment at {ms} ms, in sd units",
            premium_reduction(latency_sd(ms)),
            want,
            0.05,
        )
    sd = SIGMA_DAY * math.sqrt(0.5 / DAY_SECONDS)
    lc = sd / DELTA * premium_reduction(sd)
    print(
        f"     latency cost (Corollary 1) at 500 ms for these parameters: {lc * 100:.1f}% of the cost of immediacy (orientation only)"
    )


def main() -> int:
    """Run every check with a fresh report, print the summary and return the exit status (0 or 1)."""
    report = CheckReport()
    check_aluminium(report)
    check_lng(report)
    check_latency_calibration(report)
    if report.failures:
        print("\nFAILED:", report.failures)
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
