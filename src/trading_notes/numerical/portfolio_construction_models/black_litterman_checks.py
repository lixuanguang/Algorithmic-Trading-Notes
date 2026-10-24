"""Limits and Bayesian form of the Black-Litterman posterior on a three-asset example."""

import sys
from typing import Final

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.portfolio_construction_models.black_litterman import BlackLitterman
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


def example() -> BlackLitterman:
    """Return the example market, with one view on asset 1 alone, as new arrays."""
    vol = np.array(VOL)
    sigma = np.outer(vol, vol) * np.array(CORRELATION)
    p = np.array([[1.0, 0, 0]])
    return BlackLitterman.from_market_weights(
        sigma, MARKET_WEIGHTS, DELTA, p, np.array([VIEW_EXCESS]), TAU
    )


def gaussian_conditioning(m: BlackLitterman, omega: NDArray[np.float64]) -> NDArray[np.float64]:
    """Return the mean of E[R] given the views by conditioning a joint normal.

    Independent of the precision form: with E[R] ~ N(pi, tau Sigma) and the observation
    y = P E[R] + eps equal to Q, this is the conditional mean of E[R] given y.
    """
    s_y = m.p @ (m.tau * m.sigma) @ m.p.T + omega
    cond = m.pi + (m.tau * m.sigma) @ m.p.T @ np.linalg.solve(s_y, m.q - m.p @ m.pi)
    return np.asarray(cond, dtype=np.float64)


def check_limits(report: CheckReport, m: BlackLitterman) -> None:
    """Check the no-view and certain-view limits."""
    e_none = m.posterior_mean(np.array([[NO_VIEW_VARIANCE]]))
    report.ok(
        "no views -> equilibrium",
        bool(np.allclose(e_none, m.pi, atol=1e-9)),
        f"{np.round(e_none - m.pi, 12)}",
    )
    e_cert = m.posterior_mean(np.array([[CERTAIN_VIEW_VARIANCE]]))
    miss = (m.p @ e_cert)[0] - m.q[0]
    report.ok("certain view holds exactly", bool(abs(miss) < 1e-9), f"{miss}")


def check_posterior(report: CheckReport, m: BlackLitterman) -> None:
    """Check agreement with Gaussian conditioning, and a view moving a correlated asset."""
    omega = np.array([[VIEW_VARIANCE]])
    e = m.posterior_mean(omega)
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
    """Run the checks on new inputs with a fresh report and return the exit status (0 or 1)."""
    report = CheckReport()
    m = example()
    check_limits(report, m)
    check_posterior(report, m)
    return report.summarise()


if __name__ == "__main__":
    sys.exit(main())
