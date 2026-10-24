"""When the equal-risk-contribution portfolio maximises, or minimises, the Sharpe ratio."""

import itertools
import math
import sys
from typing import Final

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.portfolio_construction_models.risk_contributions import (
    CovarianceModel,
    inverse_volatility,
)
from trading_notes.numerical.report import CheckReport

VOLS: Final = (0.1, 0.2, 0.3, 0.4)
UNEQUAL_CORRELATIONS: Final = (
    (1, 0.8, 0.1, 0.0),
    (0.8, 1, 0.2, 0.1),
    (0.1, 0.2, 1, -0.3),
    (0.0, 0.1, -0.3, 1.0),
)
SHARPE_RATIOS: Final = (0.4, 0.0, -0.4)  # common Sharpe ratio s: positive, zero, negative


def long_only_grid() -> list[NDArray[np.float64]]:
    """Return every long-only, fully invested four-asset portfolio on a grid of step 1/20."""
    return [np.array(w) / 20 for w in itertools.product(range(21), repeat=4) if sum(w) == 20]


def check_counterexample(report: CheckReport) -> None:
    """Check two uncorrelated assets with negative excess returns, where ERC is not the maximum."""
    print("== counterexample: two uncorrelated unit-volatility assets, excess return -1 each")
    model = CovarianceModel(sigma=np.eye(2))
    ex = np.array([-1.0, -1.0])
    erc_w = np.array([0.5, 0.5])
    report.ok(
        "ERC Sharpe = -sqrt(2)",
        abs(model.sharpe(erc_w, ex) + math.sqrt(2)) < 1e-12,
        f"{model.sharpe(erc_w, ex):+.6f}",
    )
    single = np.array([1.0, 0.0])
    report.ok("single asset Sharpe = -1", abs(model.sharpe(single, ex) + 1) < 1e-12)
    report.ok("ERC is not the maximum", model.sharpe(erc_w, ex) < model.sharpe(single, ex))


def check_constant_correlation(report: CheckReport) -> None:
    """Check that ERC is the grid maximum for s > 0 and the minimum for s < 0."""
    print(
        "== four assets, vols 10/20/30/40%, constant correlation 0.3; long-only grid of step 1/20"
    )
    vols = np.array(VOLS)
    model = CovarianceModel.from_volatilities(VOLS, np.full((4, 4), 0.3) + 0.7 * np.eye(4))
    iv = inverse_volatility(vols)
    grid = long_only_grid()
    for s in SHARPE_RATIOS:
        ex = s * vols
        srs = np.array([model.sharpe(x, ex) for x in grid])
        e = model.sharpe(iv, ex)
        if s > 0:
            report.ok(
                f"s = {s:+.1f}: ERC is the grid maximum and the tangency portfolio",
                bool(e >= srs.max() - 1e-12 and np.allclose(model.tangency(ex), iv)),
                f"ERC {e:+.4f}, grid max {srs.max():+.4f}",
            )
        elif s == 0:
            report.ok(
                "s = 0: all Sharpe ratios are zero",
                bool(np.abs(srs).max() < 1e-12 and abs(e) < 1e-12),
            )
        else:
            report.ok(
                f"s = {s:+.1f}: ERC is the grid MINIMUM; maximum = s at a single asset",
                bool(e <= srs.min() + 1e-12 and abs(srs.max() - s) < 1e-12),
                f"ERC {e:+.4f}, grid min {srs.min():+.4f}, grid max {srs.max():+.4f}",
            )


def check_unequal_correlations(report: CheckReport) -> None:
    """Check that ERC falls below the tangency Sharpe ratio with unequal correlations."""
    print("== unequal correlations break it even for s > 0")
    vols = np.array(VOLS)
    model = CovarianceModel.from_volatilities(VOLS, np.array(UNEQUAL_CORRELATIONS))
    erc2 = model.equal_risk_contribution()
    ex = 0.4 * vols
    tan = model.tangency(ex)
    report.ok(
        "ERC below the tangency Sharpe",
        model.sharpe(erc2, ex) < model.sharpe(tan, ex) - 1e-6,
        f"ERC {model.sharpe(erc2, ex):+.4f} vs tangency {model.sharpe(tan, ex):+.4f}",
    )


def main() -> int:
    """Run the checks with a fresh report and return the exit status (0 or 1).

    With a constant correlation and a common Sharpe ratio s for every asset, the long-only Sharpe
    ratio is s times the diversification ratio, which inverse volatility (here ERC) maximises: ERC
    is the maximum for s > 0 and the minimum for s < 0, so the first-order condition alone does not
    make it optimal.
    """
    report = CheckReport()
    check_counterexample(report)
    check_constant_correlation(report)
    check_unequal_correlations(report)
    return report.summarise()


if __name__ == "__main__":
    sys.exit(main())
