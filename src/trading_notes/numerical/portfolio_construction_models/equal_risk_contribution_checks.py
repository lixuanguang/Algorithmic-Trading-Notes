"""Properties of the equal-risk-contribution portfolio (Maillard, Roncalli and Teiletche, 2009)."""

import sys
from typing import Final

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.portfolio_construction_models.risk_contributions import (
    CovarianceModel,
    inverse_volatility,
    long_only_minimum_variance,
)
from trading_notes.numerical.report import CheckReport

VOLS: Final = (0.10, 0.20, 0.30, 0.15)
UNEQUAL_CORRELATIONS: Final = (
    (1, 0.8, 0.1, 0.0),
    (0.8, 1, 0.2, 0.1),
    (0.1, 0.2, 1, -0.3),
    (0.0, 0.1, -0.3, 1.0),
)


def check_case(report: CheckReport, label: str, C: NDArray[np.float64]) -> None:
    """Check one correlation matrix: contributions, eq. (5), eq. (3) and the volatility order.

    Args:
        report: The run's report.
        label: The case's heading; a label starting "constant" checks eq. (3), any other that
            ERC differs from inverse volatility.
        C: Correlation matrix, 4 x 4.
    """
    print(f"== {label}")
    vols = np.array(VOLS)
    model = CovarianceModel.from_volatilities(VOLS, C)
    x = model.equal_risk_contribution()
    r, s = model.risk_contributions(x), model.volatility(x)
    report.ok(
        "risk contributions sum to portfolio volatility",
        bool(abs(r.sum() - s) < 1e-12),
        f"{r.sum():.6f} vs {s:.6f}",
    )
    report.ok("ERC contributions equal", bool(np.ptp(r) < 1e-10), ", ".join(f"{v:.5f}" for v in r))
    iv = inverse_volatility(vols)
    beta = model.betas(x)
    report.ok("x_i = (1/beta_i)/n (eq. (5))", bool(np.allclose(x, 1 / beta / len(x), atol=1e-10)))
    same = np.allclose(x, iv, atol=1e-8)
    if label.startswith("constant"):
        report.ok(
            "constant correlation: ERC equals inverse volatility (eq. (3))",
            bool(same),
            ", ".join(f"{v:.4f}" for v in x),
        )
    else:
        report.ok(
            "unequal correlations: ERC differs from inverse volatility",
            not same,
            "ERC "
            + ", ".join(f"{v:.4f}" for v in x)
            + " | 1/vol "
            + ", ".join(f"{v:.4f}" for v in iv),
        )
        r_iv = model.risk_contributions(iv)
        print(
            "     inverse-volatility risk shares: "
            + ", ".join(f"{v / r_iv.sum() * 100:.1f}%" for v in r_iv)
        )
    S = model.sigma
    mv = long_only_minimum_variance(S)
    s_mv, s_erc, s_eq = np.sqrt(mv @ S @ mv), s, np.sqrt(np.ones(4) @ S @ np.ones(4)) / 4
    report.ok(
        "sigma_mv <= sigma_erc <= sigma_1/n",
        bool(s_mv <= s_erc + 1e-12 <= s_eq + 2e-12),
        f"{s_mv:.5f} <= {s_erc:.5f} <= {s_eq:.5f}",
    )


def check_constant_correlation(report: CheckReport) -> None:
    """Check the constant-correlation case, where ERC is inverse volatility."""
    check_case(report, "constant correlation 0.3", np.full((4, 4), 0.3) + 0.7 * np.eye(4))


def check_unequal_correlations(report: CheckReport) -> None:
    """Check the unequal-correlation case, where ERC is not inverse volatility."""
    check_case(report, "unequal correlations", np.array(UNEQUAL_CORRELATIONS))


def main() -> int:
    """Run the checks with a fresh report and return the exit status (0 or 1)."""
    report = CheckReport()
    check_constant_correlation(report)
    check_unequal_correlations(report)
    return report.summarise()


if __name__ == "__main__":
    sys.exit(main())
