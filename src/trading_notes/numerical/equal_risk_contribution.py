"""Own checks behind meth:equal-risk-contribution.

Empirical extensions (2026-10-17). Maillard, Roncalli and Teiletche (authors' version of May 2009
of "The properties of equally weighted risk contribution portfolios"): risk contributions
sigma_i(x) = x_i (Sigma x)_i / sigma(x) sum to sigma(x) (sec. 2.1); the long-only ERC portfolio
equalises them (eqs. (1)-(2)); with a constant correlation it is the inverse-volatility portfolio
(eq. (3)); in general x_i is proportional to 1/beta_i (eq. (5)); and
sigma_mv <= sigma_erc <= sigma_1/n (sec. 3.4, appendix A.3). Checked on two covariance matrices
(one constant-correlation, one not); the ERC weights are found by a simple fixed-point iteration
on y_i = 1/(Sigma y)_i (own algorithm, not the paper's SQP), and the long-only minimum-variance
portfolio by projected gradient descent.
Run: uv run --frozen --no-editable python -m trading_notes.numerical.equal_risk_contribution
(numpy). Exits non-zero on failure.
"""

# standard library imports
import sys
from typing import Final

# third party library imports
import numpy as np
from numpy.typing import NDArray

# project library imports
from trading_notes.numerical.report import CheckReport

VOLS: Final = (0.10, 0.20, 0.30, 0.15)
UNEQUAL_CORRELATIONS: Final = (
    (1, 0.8, 0.1, 0.0),
    (0.8, 1, 0.2, 0.1),
    (0.1, 0.2, 1, -0.3),
    (0.0, 0.1, -0.3, 1.0),
)


def erc(S: NDArray[np.float64], iters: int = 20000) -> NDArray[np.float64]:
    """Return the long-only ERC weights by a fixed-point iteration.

    The step multiplies by the reciprocal, y * (1 / (Sigma y)); erc_sharpe divides instead, and
    each keeps its own arithmetic.

    Args:
        S: Covariance matrix, n x n.
        iters: Number of iterations.

    Returns:
        Weights summing to one, length n.
    """
    y: NDArray[np.float64] = np.ones(len(S))
    for _ in range(iters):
        y = np.sqrt(y * (1 / (S @ y)))  # geometric step toward y_i (Sigma y)_i = 1
    weights: NDArray[np.float64] = y / y.sum()
    return weights


def project_to_simplex(x: NDArray[np.float64]) -> NDArray[np.float64]:
    """Return the Euclidean projection of x onto the simplex {w >= 0, sum w = 1}.

    Args:
        x: A point, length n.

    Returns:
        A new array of length n; x is not changed.
    """
    n = len(x)
    u = np.sort(x)[::-1]
    css = np.cumsum(u)
    rho = np.nonzero(u * np.arange(1, n + 1) > (css - 1))[0][-1]
    projected: NDArray[np.float64] = np.maximum(x - (css[rho] - 1) / (rho + 1), 0)
    return projected


def minvar_long_only(
    S: NDArray[np.float64], iters: int = 200000, lr: float = 0.5
) -> NDArray[np.float64]:
    """Return the long-only minimum-variance weights by projected gradient descent.

    Args:
        S: Covariance matrix, n x n.
        iters: Number of gradient steps, each followed by a projection onto the simplex.
        lr: Step size.

    Returns:
        Weights, length n.
    """
    n = len(S)
    x = np.ones(n) / n
    for _ in range(iters):
        x = project_to_simplex(x - lr * (S @ x))
    return x


def rc(x: NDArray[np.float64], S: NDArray[np.float64]) -> tuple[NDArray[np.float64], float]:
    """Return the risk contributions x_i (Sigma x)_i / sigma(x), and sigma(x).

    Args:
        x: Weights, length n.
        S: Covariance matrix, n x n.
    """
    s = float(np.sqrt(x @ S @ x))  # exact: the scalar is only printed with fixed decimals
    return x * (S @ x) / s, s


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
    S = np.outer(vols, vols) * C
    x = erc(S)
    r, s = rc(x, S)
    report.ok(
        "risk contributions sum to portfolio volatility",
        bool(abs(r.sum() - s) < 1e-12),
        f"{r.sum():.6f} vs {s:.6f}",
    )
    report.ok("ERC contributions equal", bool(np.ptp(r) < 1e-10), ", ".join(f"{v:.5f}" for v in r))
    iv = (1 / vols) / (1 / vols).sum()
    beta = (S @ x) / (x @ S @ x)
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
        r_iv, _ = rc(iv, S)
        print(
            "     inverse-volatility risk shares: "
            + ", ".join(f"{v / r_iv.sum() * 100:.1f}%" for v in r_iv)
        )
    mv = minvar_long_only(S)
    s_mv, s_erc, s_eq = np.sqrt(mv @ S @ mv), s, np.sqrt(np.ones(4) @ S @ np.ones(4)) / 4
    report.ok(
        "sigma_mv <= sigma_erc <= sigma_1/n",
        bool(s_mv <= s_erc + 1e-12 <= s_eq + 2e-12),
        f"{s_mv:.5f} <= {s_erc:.5f} <= {s_eq:.5f}",
    )


def check_constant_correlation(report: CheckReport) -> None:
    """The constant-correlation case, where ERC is inverse volatility."""
    check_case(report, "constant correlation 0.3", np.full((4, 4), 0.3) + 0.7 * np.eye(4))


def check_unequal_correlations(report: CheckReport) -> None:
    """The unequal-correlation case, where ERC is not inverse volatility."""
    check_case(report, "unequal correlations", np.array(UNEQUAL_CORRELATIONS))


def main() -> int:
    """Run the checks with a fresh report and return the exit status (0 or 1)."""
    report = CheckReport()
    check_constant_correlation(report)
    check_unequal_correlations(report)
    if report.failures:
        print("\nFAILED:", report.failures)
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
