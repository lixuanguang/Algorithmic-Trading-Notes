"""Clustering of HS and FHS VaR violations when a GARCH(1,1)-t model is true (synthetic data)."""

import sys
from typing import Final

import numpy as np
from scipy.stats import chi2

from trading_notes.numerical.report import CheckReport
from trading_notes.numerical.var_es_estimation.var_backtest import (
    GarchT,
    VaRBacktest,
    Violations,
    rate_after_violation,
    unconditional_coverage,
)

SEED: Final = 1996
MODEL: Final = GarchT(omega=1e-6, alpha=0.08, beta=0.90, nu=6)
DAYS: Final = 20250  # simulated days; the first BACKTEST.window only start the backtest
BACKTEST: Final = VaRBacktest(window=250, p=0.01)


def check_chi2_critical(report: CheckReport) -> None:
    """Check that the 10 percent critical value 2.7055 is chi2(1)'s 90th percentile."""
    critical = chi2.ppf(0.9, 1)
    report.ok("chi2(1) 90th percentile", abs(critical - 2.7055) < 5e-4, f"{critical:.4f}")


def print_backtests(violations: Violations) -> None:
    """Print each method's violation rate, LR_uc and rate after a violation."""
    for name, h in (("HS", violations.hs), ("FHS", violations.fhs)):
        print(
            f"     {name}: violation rate {h.mean() * 100:.2f}%, "
            f"LR_uc {unconditional_coverage(h, BACKTEST.p):.2f}, "
            f"P(violation | violation yesterday) {rate_after_violation(h) * 100:.1f}%"
        )


def check_clustering(report: CheckReport, violations: Violations) -> None:
    """Check that HS violations cluster and FHS violations cluster less than half as much."""
    hs_after = rate_after_violation(violations.hs)
    fhs_after = rate_after_violation(violations.fhs)
    report.ok("HS violations cluster", hs_after > 0.04, "conditional rate above 4 percent")
    report.ok(
        "FHS violations do not cluster as much",
        fhs_after < hs_after / 2,
        "conditional rate under half of HS",
    )


def main() -> int:
    """Check the critical value, then simulate, backtest and check the clustering.

    This shows how HS lags a known volatility process; it is not evidence about market data.

    Returns:
        The exit status, 0 or 1.
    """
    report = CheckReport()
    check_chi2_critical(report)
    violations = BACKTEST.run(MODEL.simulate(np.random.default_rng(SEED), DAYS))
    print_backtests(violations)
    check_clustering(report, violations)
    return report.summarise()


if __name__ == "__main__":
    sys.exit(main())
