"""GARCH(1,1) k-step variance forecasts, and EWMA against GARCH when GARCH is true."""

import sys
from typing import Final

import numpy as np

from trading_notes.numerical.report import CheckReport
from trading_notes.numerical.volatility_forecasting.garch import Ewma, Garch11, mse_ratio

MODEL: Final = Garch11(omega=2e-6, alpha=0.08, beta=0.90)
SEED: Final = 1986
K: Final = 10  # forecast step of the Monte Carlo check
PATHS: Final = 200000
DAYS: Final = 60000  # length of the simulated return series
FIRST_FORECAST: Final = 1000  # forecasts are evaluated from this day on


def check_k_step(report: CheckReport, rng: np.random.Generator) -> None:
    """(1) The k-step formula against Monte Carlo from a high starting variance."""
    s2_next = 4 * MODEL.long_run
    mc = MODEL.monte_carlo_forecast(rng, s2_next, K, PATHS)
    formula = MODEL.k_step_forecast(s2_next, K)
    report.ok(
        "k-step GARCH forecast matches simulation (k = 10)",
        abs(mc / formula - 1) < 0.01,
        f"{mc:.3e} vs {formula:.3e}",
    )


def check_ewma_against_garch(report: CheckReport, rng: np.random.Generator) -> None:
    """(2) EWMA against the true GARCH forecast, cumulative variance over h days."""
    series = MODEL.simulate(rng, DAYS)
    ew = Ewma().variances(series.returns, MODEL.long_run)
    out = {}
    for h in (1, 20):
        out[h] = mse_ratio(MODEL, series, ew, h, FIRST_FORECAST)
        print(f"     horizon {h:2d}: MSE(EWMA)/MSE(GARCH) = {out[h]:.3f}")
    report.ok(
        "EWMA close to GARCH at one day (within 10 percent MSE)", out[1] < 1.10, f"{out[1]:.3f}"
    )
    report.ok(
        "EWMA relatively worse at 20 days than at 1 day",
        out[20] > out[1],
        f"{out[20]:.3f} > {out[1]:.3f}",
    )


def main() -> int:
    """Run the checks on one generator, the second continuing the first's stream.

    Own check behind mod:garch-volatility-forecast.
    Christoffersen (2nd ed., chap. 4, PDF p. 81): GARCH(1,1) sigma2_{t+1} = omega + alpha
    R_t^2 + beta sigma2_t with long-run variance sigma2 = omega/(1 - alpha - beta) and
    k-step forecast E_t[sigma2_{t+k}] - sigma2 = (alpha + beta)^(k-1) (sigma2_{t+1} -
    sigma2); RiskMetrics (EWMA, lambda = 0.94) is the case omega = 0, alpha + beta = 1,
    whose forecast is flat in k. Checked: (1) the k-step formula against simulation; (2) in
    a world where GARCH(1,1) is true (synthetic, Gaussian shocks), the out-of-sample mean
    squared error of the cumulative 1-day and 20-day variance forecasts of EWMA relative to
    the true GARCH forecast. This shows only how the difference grows with the horizon when
    GARCH is the data-generating process; it is not evidence about market data.

    Returns:
        The exit status, 0 or 1.
    """
    rng = np.random.default_rng(SEED)
    report = CheckReport()
    check_k_step(report, rng)
    check_ewma_against_garch(report, rng)
    if report.failures:
        print("\nFAILED:", report.failures)
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
