"""Risk-parity examples of Qian (2005) and Maillard, Roncalli and Teiletche (2009, sec. 4.1)."""

import sys
from typing import Final

import numpy as np

from trading_notes.numerical.portfolio_construction_models.risk_contributions import (
    CovarianceModel,
    inverse_volatility,
)
from trading_notes.numerical.report import CheckReport

STOCK_VOL: Final = 0.151
BOND_VOL: Final = 0.046
CORRELATION: Final = 0.2
MRT_VOLS: Final = (0.1, 0.2, 0.3, 0.4)


def stock_bond_model() -> CovarianceModel:
    """Return a new covariance model of Qian's stocks and bonds, in that order."""
    s, b, r = STOCK_VOL, BOND_VOL, CORRELATION
    return CovarianceModel(sigma=np.array([[s * s, r * s * b], [r * s * b, b * b]]))


def check_sixty_forty(report: CheckReport) -> None:
    """Check that a 60/40 portfolio takes about 93% of its variance from stocks."""
    rc = stock_bond_model().variance_shares(np.array([0.6, 0.4]))
    report.ok(
        "60/40: stocks carry about 93% of variance",
        round(rc[0] * 100) == 93,
        f"{rc[0] * 100:.1f}% stocks, {rc[1] * 100:.1f}% bonds",
    )


def check_two_asset_erc(report: CheckReport) -> None:
    """Check that inverse-volatility weights, about 23/77, equalise the variance contributions."""
    s, b = STOCK_VOL, BOND_VOL
    we = np.array([1 / s, 1 / b]) / (1 / s + 1 / b)
    rce = stock_bond_model().variance_shares(we)
    report.ok(
        "two-asset ERC weights about 23/77 with equal contributions",
        bool(round(we[0] * 100) == 23 and abs(rce[0] - 0.5) < 1e-12),
        f"{we[0] * 100:.1f}/{we[1] * 100:.1f}",
    )


def check_inverse_volatility(report: CheckReport) -> None:
    """Check that the four-asset ERC of Maillard et al. is inverse volatility, 48/24/16/12."""
    iv = inverse_volatility(np.array(MRT_VOLS))
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
    return report.summarise()


if __name__ == "__main__":
    sys.exit(main())
