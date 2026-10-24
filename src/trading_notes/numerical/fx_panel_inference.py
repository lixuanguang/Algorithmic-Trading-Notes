"""Pooled Clark-West inference: calendar-month lags and cross-currency dependence.

Focused check for the pooled Clark-West inference (derivatives and empirical validation
(2026-10-17)): panel_nw_t must treat lags as calendar months and absorb contemporaneous
cross-currency dependence, never treat stacked currency rows as months.

1. K perfectly correlated currencies (identical scores in each month) carry no more information
   than one: the panel t must equal nw_t on the single monthly series, for every K and lag
   count. A row-stacked Newey-West (the superseded method) inflates it by about sqrt(K) and
   fails this test.
2. Row order inside a month must not matter (a row-lag estimator depends on it).
3. Independent currencies: the panel t must be close to sqrt(K) times a single currency's t on
   average.
4. A month with no rows is a zero on the calendar grid, so lags stay calendar months across
   gaps.

The helpers are those of fx_ppp_oos_test.py, now in trading_notes.numerical.newey_west. One
generator, seeded 20261017, draws the common series and then serves parts 2 and 3 in order.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.fx_panel_inference
(numpy only; exits 1 on failure).
"""

# standard library imports
import math
import sys
from typing import Final

# third party library imports
import numpy as np
from numpy.typing import NDArray

# project library imports
from trading_notes.numerical.newey_west import Month, add, nw_t, panel_nw_t

type Floats = NDArray[np.float64]

SEED: Final = 20261017
T: Final = 360  # months
H: Final = 12  # forecast horizon; the scores overlap over H - 1 months


def check(failures: list[str], name: str, cond: bool | np.bool, detail: str) -> None:
    """Print `PASS  <name>: <detail>` or `FAIL  <name>: <detail>`, and record a failure."""
    print(f"{'PASS' if cond else 'FAIL'}  {name}: {detail}")
    if not cond:
        failures.append(name)


def check_identical_currencies(failures: list[str], months: list[Month], x: Floats) -> None:
    """1. K identical currencies give the single series' t; row stacking inflates it."""
    h = H
    for K in (1, 7, 9):
        rows = [(m, v) for m, v in zip(months, x) for _ in range(K)]
        for lags in (0, h - 1):
            single, panel, stacked = (
                nw_t(x, lags),
                panel_nw_t(rows, lags),
                nw_t([v for _, v in rows], lags),
            )
            check(
                failures,
                f"identical currencies K={K}, lags={lags}",
                abs(panel - single) < 1e-9,
                f"panel {panel:+.4f}, single series {single:+.4f}, row-stacked {stacked:+.4f}",
            )
            if K > 1 and lags:
                check(
                    failures,
                    f"row-stacked differs, K={K}",
                    abs(stacked - single) > 0.5,
                    f"row-stacked would be {stacked / single:.2f} times the correct t",
                )


def check_row_order(
    failures: list[str], months: list[Month], x: Floats, rng: np.random.Generator
) -> None:
    """2. Shuffling rows within the panel leaves the calendar-time t unchanged."""
    h = H
    rows = [(m, v + c) for m, v in zip(months, x) for c in (-0.3, 0.0, 0.3)]
    shuffled = [rows[i] for i in rng.permutation(len(rows))]
    check(
        failures,
        "row order inside months",
        abs(panel_nw_t(rows, h - 1) - panel_nw_t(shuffled, h - 1)) < 1e-9,
        f"{panel_nw_t(rows, h - 1):+.4f} both ways; row-stacked"
        f" {nw_t([v for _, v in rows], h - 1):+.4f} vs "
        f"{nw_t([v for _, v in shuffled], h - 1):+.4f}",
    )


def check_independent_currencies(
    failures: list[str], months: list[Month], rng: np.random.Generator
) -> None:
    """3. Nine independent currencies scale the t by about sqrt(9) = 3."""
    h = H
    ratios = []
    for _rep in range(200):
        K = 9
        panel_x = (
            np.array(
                [
                    [rng.standard_normal(T + h)[k : k + h].sum() / math.sqrt(h) for k in range(T)]
                    for _ in range(K)
                ]
            )
            + 0.05
        )
        t1 = np.mean([nw_t(panel_x[c], h - 1) for c in range(K)])
        tp = panel_nw_t([(m, panel_x[c, i]) for i, m in enumerate(months) for c in range(K)], h - 1)
        ratios.append(tp / t1)
    check(
        failures,
        "independent currencies scale by about sqrt(K)",
        abs(np.median(ratios) / 3 - 1) < 0.15,
        f"median ratio panel / single = {np.median(ratios):.2f} (sqrt(9) = 3)",
    )


def check_empty_months(failures: list[str], months: list[Month], x: Floats) -> None:
    """4. Months with no rows are zeros on the calendar grid, so lags stay calendar months."""
    h = H
    gap = [(m, v) for m, v in zip(months, x) if not (100 <= months.index(m) < 103)]
    filled = [(m, (v if not (100 <= months.index(m) < 103) else 0.0)) for m, v in zip(months, x)]
    mu_gap = sum(v for _, v in gap) / len(gap)
    by = np.array([v - (0 if 100 <= i < 103 else 1) * mu_gap for i, (_, v) in enumerate(filled)])
    lrv = by @ by + 2 * sum((1 - L / h) * (by[L:] @ by[:-L]) for L in range(1, h))
    check(
        failures,
        "empty months stay on the calendar grid",
        abs(panel_nw_t(gap, h - 1) - mu_gap / math.sqrt(lrv / len(gap) ** 2)) < 1e-9,
        f"{panel_nw_t(gap, h - 1):+.4f}",
    )


def main() -> int:
    """Draw the overlapping score series, then run the four parts.

    Returns:
        The exit status, 0 or 1; nothing is printed beyond the check lines.
    """
    rng = np.random.default_rng(SEED)
    h = H
    months = [add((1990, 1), k) for k in range(T)]
    e = rng.standard_normal(T + h)
    x = (
        np.array([e[k : k + h].sum() for k in range(T)]) / math.sqrt(h) + 0.05
    )  # MA(h-1) overlap, small mean
    failures: list[str] = []
    check_identical_currencies(failures, months, x)
    check_row_order(failures, months, x, rng)
    check_independent_currencies(failures, months, rng)
    check_empty_months(failures, months, x)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
