"""Checks behind mod:black-litterman.

Source verification (2026-10-17). Black and Litterman, Goldman Sachs Fixed Income Research,
October 1991, Appendix, points 6-8 (PDF pp. 41-42, page image): Pi = delta Sigma W;
E[R] ~ N(Pi, tau Sigma); views P E[R] = Q + eps, eps ~ N(0, Omega), Omega diagonal;
posterior mean  Ebar = [(tau Sigma)^-1 + P' Omega^-1 P]^-1 [(tau Sigma)^-1 Pi + P' Omega^-1 Q].
Checked on a three-asset example (numbers chosen here): (1) no-view limit, Omega -> infinity,
gives Pi; (2) certain views, Omega -> 0, satisfy P Ebar = Q; (3) the formula equals the
precision-weighted (Bayesian) mean computed independently by conditioning a joint normal; (4) a
view on asset 1 alone moves asset 2's expected return through the covariance, while Sigma itself,
used in the optimiser, is unchanged by the formula.
Run: uv run --frozen --no-editable python -m trading_notes.numerical.black_litterman   (numpy).
Exits non-zero on failure.
"""

# standard library imports
import sys
from dataclasses import dataclass
from typing import Final

# third party library imports
import numpy as np
from numpy.typing import NDArray

# project library imports
from trading_notes.numerical.report import CheckReport

VOL: Final = (0.15, 0.20, 0.10)
CORRELATION: Final = ((1, 0.6, 0.2), (0.6, 1, 0.3), (0.2, 0.3, 1))
MARKET_WEIGHTS: Final = (0.5, 0.3, 0.2)
DELTA: Final = 2.5  # risk aversion
TAU: Final = 0.05  # scale of the uncertainty of E[R] relative to Sigma
VIEW_EXCESS: Final = 0.03  # the view: asset 1 returns 3 points above its equilibrium return
VIEW_VARIANCE: Final = 0.0004  # Omega of the worked posterior
NO_VIEW_VARIANCE: Final = 1e12  # Omega -> infinity
CERTAIN_VIEW_VARIANCE: Final = 1e-12  # Omega -> 0


@dataclass(frozen=True)
class Market:
    """The three-asset example with one view; build a new one with `market()` for each run.

    Attributes:
        sigma: Covariance matrix Sigma, 3 x 3.
        pi: Equilibrium excess returns Pi = delta Sigma W, length 3.
        p: View matrix P, 1 x 3: one view, on asset 1 alone.
        q: View returns Q, length 1.
    """

    sigma: NDArray[np.float64]
    pi: NDArray[np.float64]
    p: NDArray[np.float64]
    q: NDArray[np.float64]


def market() -> Market:
    """Return the example's inputs as new arrays."""
    vol = np.array(VOL)
    sigma = np.outer(vol, vol) * np.array(CORRELATION)
    pi = DELTA * sigma @ np.array(MARKET_WEIGHTS)
    return Market(sigma, pi, np.array([[1.0, 0, 0]]), np.array([pi[0] + VIEW_EXCESS]))


def posterior_mean(m: Market, omega: NDArray[np.float64]) -> NDArray[np.float64]:
    """Return the Black-Litterman posterior mean in the paper's precision form.

    Args:
        m: The market and its view.
        omega: View covariance Omega, 1 x 1.

    Returns:
        Ebar, length 3.
    """
    a = np.linalg.inv(TAU * m.sigma) + m.p.T @ np.linalg.inv(omega) @ m.p
    b = np.linalg.inv(TAU * m.sigma) @ m.pi + m.p.T @ np.linalg.inv(omega) @ m.q
    return np.asarray(np.linalg.solve(a, b), dtype=np.float64)  # already float64: no copy


def gaussian_conditioning(m: Market, omega: NDArray[np.float64]) -> NDArray[np.float64]:
    """Return the mean of E[R] given the views, by conditioning a joint normal.

    Independent of `posterior_mean`: E[R] ~ N(Pi, tau Sigma); the observation y = P E[R] + eps
    equals Q; this is the conditional mean of E[R] given y.

    Args:
        m: The market and its view.
        omega: View covariance Omega, 1 x 1.

    Returns:
        The conditional mean, length 3.
    """
    s_y = m.p @ (TAU * m.sigma) @ m.p.T + omega
    cond = m.pi + (TAU * m.sigma) @ m.p.T @ np.linalg.solve(s_y, m.q - m.p @ m.pi)
    return np.asarray(cond, dtype=np.float64)  # already float64: no copy


def check_limits(report: CheckReport, m: Market) -> None:
    """Checks 1-2: the no-view and certain-view limits."""
    e_none = posterior_mean(m, np.array([[NO_VIEW_VARIANCE]]))
    report.ok(
        "no views -> equilibrium",
        bool(np.allclose(e_none, m.pi, atol=1e-9)),
        f"{np.round(e_none - m.pi, 12)}",
    )
    e_cert = posterior_mean(m, np.array([[CERTAIN_VIEW_VARIANCE]]))
    miss = (m.p @ e_cert)[0] - m.q[0]
    report.ok("certain view holds exactly", bool(abs(miss) < 1e-9), f"{miss}")


def check_posterior(report: CheckReport, m: Market) -> None:
    """Checks 3-4: agreement with Gaussian conditioning, and a view moving a correlated asset."""
    omega = np.array([[VIEW_VARIANCE]])
    e = posterior_mean(m, omega)
    cond = gaussian_conditioning(m, omega)
    report.ok(
        "equals Gaussian conditioning",
        bool(np.allclose(e, cond, atol=1e-12)),
        f"{np.round(e - cond, 14)}",
    )
    report.ok(
        "view on asset 1 moves asset 2 (correlated)",
        bool(e[1] - m.pi[1] > 1e-4),
        f"{(e[1] - m.pi[1]) * 100:+.3f} pp",
    )
    print(f"  equilibrium {np.round(m.pi * 100, 3)} -> posterior {np.round(e * 100, 3)} (percent)")


def main() -> int:
    """Run the checks on new inputs with a fresh report and return the exit status (0 or 1).

    A failure prints no summary: the BAD lines are the whole report, as in the original script.
    """
    report = CheckReport()
    m = market()
    check_limits(report, m)
    check_posterior(report, m)
    if report.failures:
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
