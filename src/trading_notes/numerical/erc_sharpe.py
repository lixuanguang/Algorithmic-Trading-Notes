"""When is the ERC portfolio the maximum-Sharpe portfolio? (meth:equal-risk-contribution).

Derivatives and empirical validation (2026-10-17). Maillard, Roncalli and Teiletche (sec. 3.5,
p. 9) say ERC "is optimal" with a constant correlation matrix and equal individual Sharpe ratios,
by checking the first-order condition mu - r = SR(x) Sigma x / sigma(x). That condition is met for
ANY common Sharpe ratio s, so it locates a stationary point, not necessarily a maximum. Own
derivation: with Sigma = D C D (vols D > 0; C constant correlation rho, -1/(n-1) < rho < 1, so
Sigma is positive definite) and mu - r = s * vols, the Sharpe ratio of long-only, fully invested
weights x is SR(x) = s * DR(x), where DR(x) = sum x_i sigma_i / sigma(x) >= 1 is the
diversification ratio, maximised by inverse volatility (= ERC here).
  s > 0: ERC maximises SR (it is also the tangency portfolio Sigma^-1 (mu - r), normalised);
  s = 0: every portfolio has SR 0;
  s < 0: ERC MINIMISES SR among long-only portfolios; the maximum is at a single asset (DR = 1),
         SR = s.
Counterexample: two uncorrelated unit-volatility assets, each with expected excess return -1: ERC
(1/2, 1/2) has Sharpe -sqrt(2), either asset alone -1.
Run: uv run --frozen --no-editable python -m trading_notes.numerical.erc_sharpe   (numpy).
Exits 1 on failure.
"""

# standard library imports
import itertools
import math
import sys
from typing import Final

# third party library imports
import numpy as np
from numpy.typing import NDArray

# project library imports
from trading_notes.numerical.report import CheckReport

VOLS: Final = (0.1, 0.2, 0.3, 0.4)
UNEQUAL_CORRELATIONS: Final = (
    (1, 0.8, 0.1, 0.0),
    (0.8, 1, 0.2, 0.1),
    (0.1, 0.2, 1, -0.3),
    (0.0, 0.1, -0.3, 1.0),
)
SHARPE_RATIOS: Final = (0.4, 0.0, -0.4)  # common Sharpe ratio s: positive, zero, negative


def sharpe(x: NDArray[np.float64], ex: NDArray[np.float64], S: NDArray[np.float64]) -> float:
    """Return the Sharpe ratio x' ex / sqrt(x' Sigma x).

    Args:
        x: Weights, length n.
        ex: Expected excess returns, length n.
        S: Covariance matrix, n x n.
    """
    return float(x @ ex / math.sqrt(x @ S @ x))


def erc(S: NDArray[np.float64], iters: int = 20000) -> NDArray[np.float64]:
    """Return the long-only ERC weights by the fixed-point iteration y_i = 1/(Sigma y)_i.

    The step divides, y / (Sigma y); equal_risk_contribution multiplies by the reciprocal
    instead, and each keeps its own arithmetic.

    Args:
        S: Covariance matrix, n x n.
        iters: Number of iterations.

    Returns:
        Weights summing to one, length n.
    """
    y: NDArray[np.float64] = np.ones(len(S))
    for _ in range(iters):
        y = np.sqrt(y / (S @ y))
    weights: NDArray[np.float64] = y / y.sum()
    return weights


def long_only_grid() -> list[NDArray[np.float64]]:
    """Return every long-only, fully invested four-asset portfolio on a grid of step 1/20."""
    return [np.array(w) / 20 for w in itertools.product(range(21), repeat=4) if sum(w) == 20]


def check_counterexample(report: CheckReport) -> None:
    """Two uncorrelated assets with negative excess returns: ERC is not the maximum."""
    print("== counterexample: two uncorrelated unit-volatility assets, excess return -1 each")
    S = np.eye(2)
    ex = np.array([-1.0, -1.0])
    erc_w = np.array([0.5, 0.5])
    report.ok(
        "ERC Sharpe = -sqrt(2)",
        abs(sharpe(erc_w, ex, S) + math.sqrt(2)) < 1e-12,
        f"{sharpe(erc_w, ex, S):+.6f}",
    )
    report.ok("single asset Sharpe = -1", abs(sharpe(np.array([1.0, 0.0]), ex, S) + 1) < 1e-12)
    report.ok("ERC is not the maximum", sharpe(erc_w, ex, S) < sharpe(np.array([1.0, 0.0]), ex, S))


def check_constant_correlation(report: CheckReport) -> None:
    """Constant correlation: ERC is the grid maximum for s > 0 and the minimum for s < 0."""
    print(
        "== four assets, vols 10/20/30/40%, constant correlation 0.3; long-only grid of step 1/20"
    )
    vols = np.array(VOLS)
    C = np.full((4, 4), 0.3) + 0.7 * np.eye(4)
    S = np.outer(vols, vols) * C
    iv = (1 / vols) / (1 / vols).sum()
    grid = long_only_grid()
    for s in SHARPE_RATIOS:
        ex = s * vols
        srs = np.array([sharpe(x, ex, S) for x in grid])
        e = sharpe(iv, ex, S)
        if s > 0:
            tan = np.linalg.solve(S, ex)
            tan /= tan.sum()
            report.ok(
                f"s = {s:+.1f}: ERC is the grid maximum and the tangency portfolio",
                bool(e >= srs.max() - 1e-12 and np.allclose(tan, iv)),
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
    """Unequal correlations: ERC falls below the tangency Sharpe ratio even for s > 0."""
    print("== unequal correlations break it even for s > 0")
    vols = np.array(VOLS)
    S2 = np.outer(vols, vols) * np.array(UNEQUAL_CORRELATIONS)
    erc2 = erc(S2)
    ex = 0.4 * vols
    tan = np.linalg.solve(S2, ex)
    tan /= tan.sum()
    report.ok(
        "ERC below the tangency Sharpe",
        sharpe(erc2, ex, S2) < sharpe(tan, ex, S2) - 1e-6,
        f"ERC {sharpe(erc2, ex, S2):+.4f} vs tangency {sharpe(tan, ex, S2):+.4f}",
    )


def main() -> int:
    """Run the checks with a fresh report and return the exit status (0 or 1)."""
    report = CheckReport()
    check_counterexample(report)
    check_constant_correlation(report)
    check_unequal_correlations(report)
    if report.failures:
        print("\nFAILED:", report.failures)
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
