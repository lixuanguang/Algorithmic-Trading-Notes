"""Checks that margin and loss spirals amplify a selling shock, and super-additively."""

import sys
from typing import Final

from trading_notes.numerical.crowding_contagion.liquidity_spiral import LiquiditySpiral
from trading_notes.numerical.report import CheckReport

# Illustrative inputs, not a calibration: the margin rises as the price falls against a prior
# long position facing selling.
SPIRAL: Final = LiquiditySpiral(
    gamma=2.0, sigma2=0.5, margin=0.25, position=1.0, loss_position=0.3, margin_slope=-0.2
)
# Terms of the loop series; |l| / k is 0.5 here, so the remainder is far below the tolerance.
SERIES_TERMS: Final = 200


def check_series(report: CheckReport) -> None:
    """Check 1: the loop series equals the closed form for the combined l."""
    ell = SPIRAL.margin_loop + SPIRAL.loss_loop
    series, closed = SPIRAL.series_response(ell, SERIES_TERMS), SPIRAL.response(ell)
    report.ok(f"series = closed form ({series:.6f} vs {closed:.6f})", abs(series - closed) < 1e-12)


def check_amplification(report: CheckReport) -> None:
    """Check 2: each spiral amplifies, and the joint effect is super-additive."""
    base = 1 / SPIRAL.k
    margin, loss = SPIRAL.response(SPIRAL.margin_loop), SPIRAL.response(SPIRAL.loss_loop)
    report.ok(f"margin spiral amplifies: {margin:.4f} > {base:.4f}", margin > base)
    report.ok(f"loss spiral amplifies: {loss:.4f} > {base:.4f}", loss > base)
    extra_joint = SPIRAL.response(SPIRAL.margin_loop + SPIRAL.loss_loop) - base
    extra_sum = (margin - base) + (loss - base)
    report.ok(
        f"joint extra {extra_joint:.4f} > sum of separate extras {extra_sum:.4f}",
        extra_joint > extra_sum,
    )


def main() -> int:
    """Run every check with a fresh report, print the summary and return the exit status (0 or 1).

    Illustration of mod:margin-liquidity-spiral (Brunnermeier and Pedersen, Proposition 5,
    eq. (24) and p. 19): 1/(k - l) equals its loop series for |l| < k; each spiral amplifies
    when l > 0, and the combined effect exceeds the sum of the separate ones (1/(k - l) is
    convex in l).
    """
    report = CheckReport()
    check_series(report)
    check_amplification(report)
    if report.failures:
        print("\nFAILED:", report.failures)
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
