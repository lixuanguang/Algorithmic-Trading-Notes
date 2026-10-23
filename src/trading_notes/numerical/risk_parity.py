"""Own checks behind the risk-parity passages.

Derivatives and empirical validation (2026-10-17).
1. Qian (PanAgora, September 2005, p. 1): with stock and bond excess-return volatilities 15.1%
   and 4.6% and correlation 0.2 (Russell 1000 and Lehman Aggregate, 1983-2004), a 60/40
   portfolio takes about 93% of its variance from stocks, and the two-asset
   equal-risk-contribution weights are about 23/77 (p. 2).
2. Maillard, Roncalli and Teiletche (2009, sec. 4.1): with volatilities 10/20/30/40% and a
   common correlation, ERC is 48/24/16/12% (inverse volatility).
Run: uv run --frozen --no-editable python -m trading_notes.numerical.risk_parity   (numpy).
Exits 1 on failure.
"""

# standard library imports
import sys
from typing import Final

# third party library imports
import numpy as np
from numpy.typing import NDArray

# project library imports
from trading_notes.numerical.report import CheckReport

STOCK_VOL: Final = 0.151
BOND_VOL: Final = 0.046
CORRELATION: Final = 0.2
MRT_VOLS: Final = (0.1, 0.2, 0.3, 0.4)


def stock_bond_covariance() -> NDArray[np.float64]:
    """Return a new 2 x 2 covariance matrix of Qian's stocks and bonds, in that order."""
    s, b, r = STOCK_VOL, BOND_VOL, CORRELATION
    return np.array([[s * s, r * s * b], [r * s * b, b * b]])


def variance_shares(w: NDArray[np.float64], S: NDArray[np.float64]) -> NDArray[np.float64]:
    """Return each asset's share w_i (Sigma w)_i / w' Sigma w of the portfolio variance.

    Args:
        w: Weights, length n.
        S: Covariance matrix, n x n.
    """
    shares: NDArray[np.float64] = w * (S @ w) / (w @ S @ w)
    return shares


def check_sixty_forty(report: CheckReport) -> None:
    """A 60/40 portfolio takes about 93% of its variance from stocks."""
    rc = variance_shares(np.array([0.6, 0.4]), stock_bond_covariance())
    report.ok(
        "60/40: stocks carry about 93% of variance",
        round(rc[0] * 100) == 93,
        f"{rc[0] * 100:.1f}% stocks, {rc[1] * 100:.1f}% bonds",
    )


def check_two_asset_erc(report: CheckReport) -> None:
    """Inverse-volatility weights, about 23/77, equalise the two variance contributions."""
    s, b = STOCK_VOL, BOND_VOL
    we = np.array([1 / s, 1 / b]) / (1 / s + 1 / b)
    rce = variance_shares(we, stock_bond_covariance())
    report.ok(
        "two-asset ERC weights about 23/77 with equal contributions",
        bool(round(we[0] * 100) == 23 and abs(rce[0] - 0.5) < 1e-12),
        f"{we[0] * 100:.1f}/{we[1] * 100:.1f}",
    )


def check_inverse_volatility(report: CheckReport) -> None:
    """Maillard, Roncalli and Teiletche's four-asset ERC is inverse volatility, 48/24/16/12."""
    v = np.array(MRT_VOLS)
    iv = (1 / v) / (1 / v).sum()
    report.ok(
        "MRT sec. 4.1: 48/24/16/12",
        np.allclose(np.round(iv * 100), [48, 24, 16, 12]),
        ", ".join(f"{x * 100:.1f}" for x in iv),
    )


def main() -> int:
    """Run the checks with a fresh report and return the exit status (0 or 1)."""
    report = CheckReport()
    check_sixty_forty(report)
    check_two_asset_erc(report)
    check_inverse_volatility(report)
    if report.failures:
        print("\nFAILED:", report.failures)
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
