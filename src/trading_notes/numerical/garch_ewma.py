"""Own check behind mod:garch-volatility-forecast.

Empirical extensions (2026-10-17). Christoffersen (2nd ed., chap. 4, PDF p. 81): GARCH(1,1)
sigma2_{t+1} = omega + alpha R_t^2 + beta sigma2_t with long-run variance
sigma2 = omega/(1 - alpha - beta) and k-step forecast
E_t[sigma2_{t+k}] - sigma2 = (alpha + beta)^(k-1) (sigma2_{t+1} - sigma2); RiskMetrics (EWMA,
lambda = 0.94) is the case omega = 0, alpha + beta = 1, whose forecast is flat in k. Checked: (1)
the k-step formula against simulation; (2) in a world where GARCH(1,1) is true (synthetic,
Gaussian shocks), the out-of-sample mean squared error of the cumulative 1-day and 20-day
variance forecasts of EWMA relative to the true GARCH forecast. This shows only how the
difference grows with the horizon when GARCH is the data-generating process; it is not evidence
about market data.
Run: uv run --frozen --no-editable python -m trading_notes.numerical.garch_ewma
(numpy; about 1 s). Exits non-zero on failure.
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

OMEGA: Final = 2e-6
ALPHA: Final = 0.08
BETA: Final = 0.90
LONG_RUN: Final = OMEGA / (1 - ALPHA - BETA)
SEED: Final = 1986
K: Final = 10  # forecast step of the Monte Carlo check
PATHS: Final = 200000
DAYS: Final = 60000  # length of the simulated return series
FIRST_FORECAST: Final = 1000  # forecasts are evaluated from this day on


@dataclass(frozen=True)
class GarchSeries:
    """One simulated GARCH(1,1) series.

    Attributes:
        returns: R_t, length DAYS.
        variances: sigma2_t, the variance R_t was drawn with, known at t - 1; length DAYS.
    """

    returns: NDArray[np.float64]
    variances: NDArray[np.float64]


def k_step_forecast(s2_next: float, k: int) -> float:
    """Return E_t[sigma2_{t+k}] = sigma2 + (alpha + beta)^(k-1) (sigma2_{t+1} - sigma2)."""
    return LONG_RUN + (ALPHA + BETA) ** (k - 1) * (s2_next - LONG_RUN)


def monte_carlo_forecast(rng: np.random.Generator, s2_next: float, k: int, paths: int) -> float:
    """Return the mean of sigma2_{t+k} over simulated paths started at sigma2_{t+1} = s2_next.

    Each of the k - 1 steps draws one vector of `paths` shocks; no closed form is used.
    """
    s2 = np.full(paths, s2_next)
    for _ in range(k - 1):
        R = np.sqrt(s2) * rng.standard_normal(paths)
        s2 = OMEGA + ALPHA * R**2 + BETA * s2
    return float(s2.mean())


def simulate_series(rng: np.random.Generator, n: int) -> GarchSeries:
    """Simulate n days from sigma2_0 = sigma2, drawing one scalar shock per day in order."""
    R = np.empty(n)
    s2 = np.empty(n)
    s2[0] = LONG_RUN
    for t in range(n):
        R[t] = np.sqrt(s2[t]) * rng.standard_normal()
        if t + 1 < n:
            s2[t + 1] = OMEGA + ALPHA * R[t] ** 2 + BETA * s2[t]
    return GarchSeries(R, s2)


def ewma_variances(R: NDArray[np.float64]) -> NDArray[np.float64]:
    """Return the RiskMetrics variances ew_t, from ew_0 = sigma2, each known at t - 1."""
    n = len(R)
    ew = np.empty(n)
    ew[0] = LONG_RUN
    for t in range(n - 1):
        ew[t + 1] = 0.94 * ew[t] + 0.06 * R[t] ** 2
    return ew


def mse_ratio(series: GarchSeries, ew: NDArray[np.float64], h: int) -> float:
    """Return MSE(EWMA) / MSE(GARCH) of the cumulative variance forecast over days t..t+h-1.

    Each forecast is made with the variances for day t, from day FIRST_FORECAST to DAYS - h - 1.
    """
    R, s2 = series.returns, series.variances
    idx = np.arange(FIRST_FORECAST, len(R) - h)
    real = np.array([np.sum(R[t : t + h] ** 2) for t in idx])
    g = np.array(
        [sum(LONG_RUN + (ALPHA + BETA) ** j * (s2[t] - LONG_RUN) for j in range(h)) for t in idx]
    )
    e = h * ew[idx]
    return float(np.mean((real - e) ** 2) / np.mean((real - g) ** 2))


def check_k_step(report: CheckReport, rng: np.random.Generator) -> None:
    """(1) The k-step formula against Monte Carlo from a high starting variance."""
    s2_next = 4 * LONG_RUN
    mc = monte_carlo_forecast(rng, s2_next, K, PATHS)
    formula = k_step_forecast(s2_next, K)
    report.ok(
        "k-step GARCH forecast matches simulation (k = 10)",
        abs(mc / formula - 1) < 0.01,
        f"{mc:.3e} vs {formula:.3e}",
    )


def check_ewma_against_garch(report: CheckReport, rng: np.random.Generator) -> None:
    """(2) EWMA against the true GARCH forecast, cumulative variance over h days."""
    series = simulate_series(rng, DAYS)
    ew = ewma_variances(series.returns)
    out = {}
    for h in (1, 20):
        out[h] = mse_ratio(series, ew, h)
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
