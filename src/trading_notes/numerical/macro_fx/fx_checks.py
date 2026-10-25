"""The relative-PPP forecast test's stale-data rule, outcome eligibility, timing and outputs."""

import csv
import math
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Final

import numpy as np

from trading_notes.data_folders import DataFolder
from trading_notes.numerical.macro_fx.ppp_forecasts import ExpandingForecast, StaleDataRule
from trading_notes.numerical.newey_west import add
from trading_notes.numerical.report import CheckReport
from trading_notes.numerical.repository import repository_root

# The test's retained outputs, below the repository root.
FOLDER: Final = DataFolder(subsection="macro_fx")
RULE: Final = StaleDataRule(monthly_lag=2, min_age=4, max_age=6)


def check_stale_data_rule(report: CheckReport) -> None:
    """2. Quarterly CPI is used four to six months after its quarter, monthly CPI at lag two."""
    print("== 2. stale-data rule")
    q_cpi = {(2025, 1): 100.0}  # 2025Q1, dated at its first month; quarter ends March 2025
    report.same(
        "quarterly, July 2025 (age 4)", RULE.known_price(q_cpi, (2025, 7), True), (100.0, 4)
    )
    report.same(
        "quarterly, September 2025 (age 6)", RULE.known_price(q_cpi, (2025, 9), True), (100.0, 6)
    )
    report.same(
        "quarterly, October 2025 (age 7) refused", RULE.known_price(q_cpi, (2025, 10), True), None
    )
    report.same(
        "quarterly, June 2025 (age 3) not yet known", RULE.known_price(q_cpi, (2025, 6), True), None
    )
    m_cpi = {(2025, 1): 100.0}
    report.same(
        "monthly, March 2025 uses January", RULE.known_price(m_cpi, (2025, 3), False), (100.0, 2)
    )
    report.same(
        "monthly, April 2025 refuses a three-month-old value",
        RULE.known_price(m_cpi, (2025, 4), False),
        None,
    )


def check_eligibility_and_training(report: CheckReport) -> None:
    """1 and 3. Outcomes need only spot rates; each fit uses outcomes observed by its origin."""
    print("== 1 and 3. outcome eligibility and training cutoffs on synthetic data")
    months = [add((1980, 1), k) for k in range(240)]
    spot = {t: 0.01 * math.sin(i / 7.0) for i, t in enumerate(months)}
    last_cpi = months[150]
    z: dict[tuple[int, int], float | None] = {
        t: 0.02 * math.cos(i / 5.0) for i, t in enumerate(months) if t <= last_cpi
    }
    fc, ts, X, Y = ExpandingForecast(horizon=12, start=months[70]).forecasts(spot, z)
    report.same(
        "last forecast at the last predictor month (outcome from spot only)", fc[-1][0], last_cpi
    )
    report.same(
        "outcome of the last forecast is the spot change to t+12",
        abs(fc[-1][2] - (spot[add(last_cpi, 12)] - spot[last_cpi])) < 1e-15,
        True,
    )
    # training cutoff: refit by hand at the first forecast date using only pairs with t' + 12 <= t
    t0 = fc[0][0]
    tr = [k for k in ts if k < t0 and add(k, 12) <= t0]
    b1, b0 = np.polyfit([X[k] for k in tr], [Y[k] for k in tr], 1)
    report.same(
        "first forecast equals an OLS fit on outcomes observed by its date only",
        bool(abs(fc[0][1] - (b0 + b1 * X[t0])) < 1e-12),
        True,
    )
    tr_leaky = [k for k in ts if k < t0]
    c1, c0 = np.polyfit([X[k] for k in tr_leaky], [Y[k] for k in tr_leaky], 1)
    report.same(
        "...and differs from a fit that also uses the 11 unobserved outcomes",
        bool(abs(fc[0][1] - (c0 + c1 * X[t0])) > 1e-6),
        True,
    )


def check_outputs(report: CheckReport, root: Path) -> None:
    """4. The rerun's panel and results."""
    print("== 4. rebuilt outputs")
    with (root / FOLDER.results / "fx_ppp_monthly.csv").open() as fh:
        rows = list(csv.DictReader(fh))
    for c in ("AUD", "NZD"):
        z = [r["month"] for r in rows if r["ccy"] == c and r["z_dev"]]
        report.same(f"{c} last eligible predictor", z[-1], "2025-09")
    report.same(
        "ages recorded and within the rule",
        all(
            r["cpi_age_months"] in ("2", "4", "5", "6")
            for r in rows
            if r["predictor_eligible"] == "1"
        ),
        True,
    )
    res = (root / FOLDER.results / "fx_ppp_results.txt").read_text()
    report.same("portfolio labelled not executable", "not an executable result" in res, True)


def main(argv: Sequence[str] | None = None) -> int:
    """Check the relative-PPP test's rerun against the findings on its first run.

    1. Outcome eligibility does not depend on future CPI: on synthetic series whose CPI stops
       early, forecasts are still made for months whose spot outcome exists (the first run
       needed the panel row, hence CPI, at t+h).
    2. Stale-data rule: quarterly CPI is known from four months after its quarter ends and used
       for at most six; monthly CPI with a two-month lag and nothing older.
    3. Training cutoff: the expanding fit at origin t uses only pairs whose outcome month
       t' + h <= t.
    4. The rebuilt panel and results.

    The stale-data rule and the forecasts are those
    trading_notes.numerical.macro_fx.ppp_forecasts gives the PPP research workflow,
    trading_notes.research.macro_fx.ppp_out_of_sample.

    Args:
        argv: Command-line arguments: `--root DIR`, the repository root that holds the outputs
            (default: the working directory).

    Returns:
        The exit status, 0 or 1.
    """
    root = repository_root(__doc__ or "", argv)
    report = CheckReport()
    check_stale_data_rule(report)
    check_eligibility_and_training(report)
    check_outputs(report, root)
    if report.failures:
        print("\nFAILED:", report.failures)
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
