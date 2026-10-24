"""Checks behind meth:forecast-scaling-ic.

Source verification (2026-10-17): Grinold and Kahn, Active Portfolio Management, 2nd ed.,
chap. 10, pp. 264-271.

1. Binary model: IC = Cov/(Std r Std g) = 3/(9*4) = 0.0833; refined forecast = 9 * IC * score
   = 0.75 * score; normal scores: |0.75 z| <= 0.75 with probability ~2/3 and |0.75 z| > 1.50
   with probability ~1/20.
2. Two forecasts: Var g = 16, Var g' = 25, Cov(g, g') = 5, Cov(r, g) = 3, Cov(r, g') = 4,
   Var r = 81: regression weights Sigma^-1 c = (0.1467, 0.1307); IC of g' = 4/(9*5) = 0.089;
   combined IC sqrt(c' Sigma^-1 c)/9 = 0.1090.
3. Table 10.1: alpha = residual volatility * 0.09 * score, to within the rounding of the printed
   two-decimal scores.
Run: uv run --frozen --no-editable python -m trading_notes.numerical.forecast_scaling
(numpy, scipy). Exits non-zero on failure.
"""

# standard library imports
import sys
from typing import Final

# third party library imports
import numpy as np
from scipy.stats import norm

# project library imports
from trading_notes.numerical.report import CheckReport

# Table 10.1: name -> (residual volatility, score, printed alpha).
TABLE_10_1: Final = {
    "American Express": (23.26, 0.35, 0.73),
    "AT&T": (15.89, 0.71, 1.01),
    "DuPont": (17.29, 1.58, 2.47),
    "General Motors": (23.46, 1.98, 4.17),
    "IBM": (30.32, -0.67, -1.84),
    "Johnson & Johnson": (18.97, -1.77, -3.02),
    "Procter & Gamble": (16.29, -2.32, -3.40),
    "Exxon": (21.13, 0.00, -0.01),
}


def near(report: CheckReport, name: str, got: float, want: float, tol: float) -> None:
    """Check |got - want| <= tol and print got to five decimals, with want and tol as given."""
    report.ok(name, abs(got - want) <= tol, f"{got:.5f} (want {want}, tol {tol})")


def check_one_forecast(report: CheckReport) -> None:
    """1. The binary model's IC and multiplier, and the normal score probabilities."""
    print("== 1. One forecast")
    ic = 3 / (9 * 4)
    near(report, "IC", ic, 0.0833, 5e-5)
    near(report, "multiplier volatility * IC", 9 * ic, 0.75, 1e-12)
    near(report, "P(|z| <= 1)", 2 * norm.cdf(1) - 1, 2 / 3, 0.02)
    near(report, "P(|z| > 2)", 2 * (1 - norm.cdf(2)), 1 / 20, 0.005)


def check_two_forecasts(report: CheckReport) -> None:
    """2. The regression weights of two forecasts and their combined IC."""
    print("\n== 2. Two forecasts")
    Sig = np.array([[16.0, 5.0], [5.0, 25.0]])
    c = np.array([3.0, 4.0])
    w = np.linalg.solve(Sig, c)
    near(report, "weight on g", w[0], 0.1467, 5e-5)
    near(report, "weight on g'", w[1], 0.1307, 5e-5)
    near(report, "IC of g'", 4 / 45, 0.089, 5e-4)
    near(report, "combined IC", np.sqrt(c @ w) / 9, 0.1090, 5e-5)


def check_table_10_1(report: CheckReport) -> None:
    """3. Each alpha of Table 10.1, within half a unit of its score's last printed digit."""
    print("\n== 3. Table 10.1 (IC 0.09)")
    for name, (vol, score, alpha) in TABLE_10_1.items():
        near(report, name, vol * 0.09 * score, alpha, vol * 0.09 * 0.005 + 0.005)


def main() -> int:
    """Run the three parts with one report.

    Returns:
        The exit status, 0 or 1.
    """
    report = CheckReport()
    check_one_forecast(report)
    check_two_forecasts(report)
    check_table_10_1(report)
    if report.failures:
        print("\nFAILED:", report.failures)
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
