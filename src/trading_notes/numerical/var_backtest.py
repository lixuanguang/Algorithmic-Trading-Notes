"""Own synthetic check behind meth:var-es-estimation-methods.

Source verification (2026-10-17). Christoffersen (Elements of Financial Risk Management, 2nd
ed., 2012): Historical Simulation (HS) VaR, Filtered Historical Simulation (FHS: a GARCH
variance with the empirical distribution of standardized returns), and the unconditional
coverage test LR_uc = -2 ln[(1-p)^T0 p^T1 / ((1-T1/T)^T0 (T1/T)^T1)] ~ chi2(1), critical value
2.7055 at 10 percent. Checked: (1) 2.7055 is the 90th percentile of chi2(1); (2) on returns
simulated from a GARCH(1,1) with Student-t(6) shocks, 1 percent HS VaR (250-day window) and FHS
VaR (true GARCH filter, empirical residual quantile from the same window) are backtested over
20 000 days: HS's violations cluster (probability of a violation the day after a violation far
above 1 percent) while FHS's do not, the dynamic-updating claim in a setting where the model is
right. This does not test either method on market data.
Run: uv run --frozen --no-editable python -m trading_notes.numerical.var_backtest
(numpy, scipy; about 1 s). Exits non-zero on failure, with no summary line.
"""

# standard library imports
import math
import sys
from dataclasses import dataclass
from typing import Final

# third party library imports
import numpy as np
from numpy.typing import NDArray
from scipy.stats import chi2

# project library imports
from trading_notes.numerical.report import CheckReport

SEED: Final = 1996
OMEGA: Final = 1e-6
ALPHA: Final = 0.08  # GARCH weight on the squared return
BETA: Final = 0.90  # GARCH weight on the previous variance
NU: Final = 6  # Student-t degrees of freedom of the shocks
DAYS: Final = 20250  # simulated days; the first WINDOW only start the backtest
WINDOW: Final = 250  # days of history behind each VaR
P: Final = 0.01  # VaR tail probability


@dataclass(frozen=True)
class GarchPath:
    """One simulated GARCH(1,1)-t path.

    Attributes:
        returns: r_t, length DAYS.
        variances: sigma2_t, the variance r_t was drawn with, known at t - 1; length DAYS.
    """

    returns: NDArray[np.float64]
    variances: NDArray[np.float64]


@dataclass(frozen=True)
class Violations:
    """Each method's VaR violations on days WINDOW to DAYS - 1, in day order.

    Attributes:
        hs: Historical Simulation violations.
        fhs: Filtered Historical Simulation violations.
    """

    hs: NDArray[np.bool_]
    fhs: NDArray[np.bool_]


def lr_uc(hits: NDArray[np.bool_], p: float) -> float:
    """Return Christoffersen's unconditional coverage statistic LR_uc.

    The formula is applied as written: with no violations, or only violations, a log of zero
    raises ValueError. Neither occurs in this example; no clipping or pseudocount is added.

    Args:
        hits: The violation indicators, one per backtest day.
        p: The VaR tail probability.
    """
    T1 = int(hits.sum())
    T0 = len(hits) - T1
    pi = T1 / len(hits)
    return -2 * (
        T0 * math.log(1 - p) + T1 * math.log(p) - T0 * math.log(1 - pi) - T1 * math.log(pi)
    )


def simulate_garch_t(rng: np.random.Generator) -> GarchPath:
    """Simulate DAYS returns from sigma2_0 = OMEGA / (1 - ALPHA - BETA).

    All DAYS Student-t(NU) shocks are drawn at once and scaled to unit variance by
    sqrt(NU / (NU - 2)).
    """
    z = rng.standard_t(NU, DAYS) / math.sqrt(NU / (NU - 2))
    s2 = np.empty(DAYS)
    r = np.empty(DAYS)
    s2[0] = OMEGA / (1 - ALPHA - BETA)
    for t in range(DAYS):
        r[t] = math.sqrt(s2[t]) * z[t]
        if t + 1 < DAYS:
            s2[t + 1] = OMEGA + ALPHA * r[t] ** 2 + BETA * s2[t]
    return GarchPath(r, s2)


def backtest(path: GarchPath, window: int = WINDOW, p: float = P) -> Violations:
    """Backtest HS and FHS VaR on every day from `window` on.

    Day t's VaR uses days t - window to t - 1 only, never day t itself, with np.quantile's
    default (linear) interpolation. HS takes the p-quantile of those returns. FHS takes the
    p-quantile of the same returns divided by their own sigma_t, then scales it by day t's
    sigma_t, which is known the day before. A violation is a return strictly below -VaR.
    """
    r, s2 = path.returns, path.variances
    days = len(r) - window
    hs = np.empty(days, dtype=np.bool_)
    fhs = np.empty(days, dtype=np.bool_)
    for i, t in enumerate(range(window, len(r))):
        past = r[t - window : t]
        var_hs = -np.quantile(past, p)
        zq = np.quantile(past / np.sqrt(s2[t - window : t]), p)
        var_fhs = -math.sqrt(s2[t]) * zq
        hs[i] = r[t] < -var_hs
        fhs[i] = r[t] < -var_fhs
    return Violations(hs, fhs)


def rate_after_violation(hits: NDArray[np.bool_]) -> float:
    """Return the violation rate on days that follow a violation.

    Without a violation before the last day the rate is the mean of no days; NumPy warns and
    returns nan. That does not occur in this example and is not repaired here.
    """
    return float(hits[1:][hits[:-1]].mean())


def check_chi2_critical(report: CheckReport) -> None:
    """(1) The 10 percent critical value 2.7055 is chi2(1)'s 90th percentile."""
    critical = chi2.ppf(0.9, 1)
    report.ok("chi2(1) 90th percentile", abs(critical - 2.7055) < 5e-4, f"{critical:.4f}")


def print_backtests(violations: Violations) -> None:
    """Print each method's violation rate, LR_uc and rate after a violation."""
    for name, h in (("HS", violations.hs), ("FHS", violations.fhs)):
        print(
            f"     {name}: violation rate {h.mean() * 100:.2f}%, LR_uc {lr_uc(h, P):.2f}, "
            f"P(violation | violation yesterday) {rate_after_violation(h) * 100:.1f}%"
        )


def check_clustering(report: CheckReport, violations: Violations) -> None:
    """(2) HS violations cluster; FHS violations cluster less than half as much."""
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

    Returns:
        The exit status, 0 or 1; a failure prints no summary beyond its BAD line.
    """
    report = CheckReport()
    check_chi2_critical(report)
    violations = backtest(simulate_garch_t(np.random.default_rng(SEED)))
    print_backtests(violations)
    check_clustering(report, violations)
    if report.failures:
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
