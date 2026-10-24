"""source verification (2026-10-17): illustration behind mod:margin-liquidity-spiral (Brunnermeier and Pedersen, Proposition 5, eq. (24) and p. 19).

Illustrative numbers only, not a calibration.

dp1/deta1 = 1 / (k - l), k = 2 m / (gamma sigma2^2), l = -(dm/dp) x1 + x0  (selling pressure, Z1 > 0).
1. 1/(k - l) equals the series 1/k + l/k^2 + l^2/k^3 + ... for |l| < k (one term per loop of the spiral).
2. Amplification when l > 0; the combined margin-and-loss effect exceeds the sum of the separate effects
   (super-additivity of 1/(k - l) in l, convexity).
Run: uv run --frozen --no-editable python -m trading_notes.numerical.margin_spiral   (standard library).
Exits non-zero on failure.
"""

import sys
from typing import Final

from trading_notes.numerical.report import CheckReport

GAMMA: Final = 2.0  # illustrative
SIGMA2: Final = 0.5
M: Final = 0.25
X1: Final = 1.0  # margin rises as price falls; prior long position against selling
X0: Final = 0.3
DM_DP: Final = -0.2
# Terms of the loop series; |l| / k is 0.5 here, so the remainder is far below the tolerance.
SERIES_TERMS: Final = 200


def loop_strengths() -> tuple[float, float, float]:
    """Return k and the margin and loss components of l, from the illustrative inputs.

    Returns:
        `(k, l_margin, l_loss)` with k = 2 m / (gamma sigma2^2) (= 1.0 here),
        l_margin = -(dm/dp) x1 and l_loss = x0.
    """
    k = 2 * M / (GAMMA * SIGMA2**2)
    return k, -DM_DP * X1, X0


def price_response(k: float, ell: float) -> float:
    """Return the closed form dp1/deta1 = 1 / (k - l) of Proposition 5, eq. (24)."""
    return 1 / (k - ell)


def series_response(k: float, ell: float) -> float:
    """Return the loop series 1/k + l/k^2 + l^2/k^3 + ..., summed independently of the closed form."""
    return sum(ell**n / k ** (n + 1) for n in range(SERIES_TERMS))


def check_series(report: CheckReport) -> None:
    """Check 1: the loop series equals the closed form for the combined l."""
    k, l_margin, l_loss = loop_strengths()
    series = series_response(k, l_margin + l_loss)
    closed = price_response(k, l_margin + l_loss)
    report.ok(f"series = closed form ({series:.6f} vs {closed:.6f})", abs(series - closed) < 1e-12)


def check_amplification(report: CheckReport) -> None:
    """Check 2: each spiral amplifies, and the joint effect is super-additive."""
    k, l_margin, l_loss = loop_strengths()
    base = 1 / k
    margin, loss = price_response(k, l_margin), price_response(k, l_loss)
    report.ok(f"margin spiral amplifies: {margin:.4f} > {base:.4f}", margin > base)
    report.ok(f"loss spiral amplifies: {loss:.4f} > {base:.4f}", loss > base)
    extra_joint = price_response(k, l_margin + l_loss) - base
    extra_sum = (margin - base) + (loss - base)
    report.ok(
        f"joint extra {extra_joint:.4f} > sum of separate extras {extra_sum:.4f}",
        extra_joint > extra_sum,
    )


def main() -> int:
    """Run every check with a fresh report, print the summary and return the exit status (0 or 1)."""
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
