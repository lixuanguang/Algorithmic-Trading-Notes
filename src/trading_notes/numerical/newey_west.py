"""Calendar-month arithmetic and Newey-West t statistics for single and pooled score series.

Moved unchanged in formula and operation order from the pure helpers of
notes/artefacts/fx-determination-forecasting/fx_ppp_oos_test.py, which keeps its own copies until
its empirical run migrates. Months are (year, month) pairs with month 1 to 12.
"""

import math
from collections.abc import Sequence

import numpy as np
from numpy.typing import ArrayLike

type Month = tuple[int, int]


def add(ym: Month, k: int) -> Month:
    """Return the month k calendar months after ym (before it for negative k)."""
    n = ym[0] * 12 + ym[1] - 1 + k
    return (n // 12, n % 12 + 1)


def mdiff(a: Month, b: Month) -> int:
    """Return the number of calendar months from b to a."""
    return (a[0] * 12 + a[1]) - (b[0] * 12 + b[1])


def nw_t(x: ArrayLike, lags: int) -> np.float64:
    """Return the t statistic for the mean of one series, Bartlett weights over `lags` lags."""
    x = np.asarray(x, dtype=np.float64)
    xc = x - x.mean()
    n = len(x)
    s2 = (xc @ xc) / n + 2 * sum(
        (1 - L / (lags + 1)) * (xc[L:] @ xc[:-L]) / n for L in range(1, lags + 1)
    )
    return np.float64(x.mean() / math.sqrt(s2 / n))


def panel_nw_t(rows: Sequence[tuple[Month, float]], lags: int) -> np.float64:
    """Return the t statistic for the mean of pooled scores, in calendar time.

    `rows` = [(forecast-origin month, score), ...]. The scores are summed within each origin
    month (S_m, n_m rows), giving one observation per calendar month; months with no rows count
    as zero on a complete monthly grid. With mu the pooled mean (every row weighted 1/N), the
    long-run variance of sum_m (S_m - n_m mu) is estimated with Bartlett weights over `lags`
    calendar months, and Var(mu) = LRV / N^2. Contemporaneous dependence across currencies is
    absorbed in S_m; overlap is handled by the lags. With one row per month this equals nw_t.
    """
    by: dict[Month, tuple[float, int]] = {}
    for m, v in rows:
        s, n = by.get(m, (0.0, 0))
        by[m] = (s + v, n + 1)
    lo, hi = min(by), max(by)
    grid = [add(lo, k) for k in range(mdiff(hi, lo) + 1)]
    S = np.array([by.get(m, (0.0, 0))[0] for m in grid])
    n_m = np.array([by.get(m, (0.0, 0))[1] for m in grid])
    N = n_m.sum()
    mu = S.sum() / N
    u = S - n_m * mu
    lrv = u @ u + 2 * sum((1 - L / (lags + 1)) * (u[L:] @ u[:-L]) for L in range(1, lags + 1))
    return np.float64(mu / math.sqrt(lrv / N**2))
