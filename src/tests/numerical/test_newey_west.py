"""Tests of the packaged Newey-West helpers against the FX runner's original copies, bit for bit.

trading_notes.numerical.newey_west holds the pure helpers that fx_panel_inference took from
notes/artefacts/fx-determination-forecasting/fx_ppp_oos_test.py. That script, and fx_carry_test.py
through it, now import them from the package; the copies they used before are kept here as the
reference. These compare the two on calendar arithmetic across year ends and gaps, and on t
statistics with and without lags, stacked rows and empty months, and check that the script binds
the packaged helpers. The script is loaded without running it; it reads its data only in `main`.

Run: make test (uv run --frozen --no-editable pytest)
"""

import math
import runpy
import unittest
from collections.abc import Sequence
from pathlib import Path

import numpy as np
from numpy.typing import ArrayLike

from trading_notes.numerical import newey_west

SCRIPT = (
    Path(__file__).resolve().parents[3]
    / "notes"
    / "artefacts"
    / "fx-determination-forecasting"
    / "fx_ppp_oos_test.py"
)
Month = tuple[int, int]


# The script's own helpers before they moved into the package, as they were run.
def add(ym: Month, k: int) -> Month:
    """Return the month k months after ym."""
    n = ym[0] * 12 + ym[1] - 1 + k
    return (n // 12, n % 12 + 1)


def mdiff(a: Month, b: Month) -> int:
    """Return the months from b to a."""
    return (a[0] * 12 + a[1]) - (b[0] * 12 + b[1])


def nw_t(values: ArrayLike, lags: int) -> float:
    """Return the Newey-West t statistic of the mean of x."""
    x = np.asarray(values, dtype=np.float64)
    xc = x - x.mean()
    n = len(x)
    s2 = (xc @ xc) / n + 2 * sum(
        (1 - L / (lags + 1)) * (xc[L:] @ xc[:-L]) / n for L in range(1, lags + 1)
    )
    return float(x.mean() / math.sqrt(s2 / n))


def panel_nw_t(rows: Sequence[tuple[Month, float]], lags: int) -> float:
    """Return the calendar-time t statistic of the mean of pooled scores."""
    by: dict[Month, tuple[float, int]] = {}
    for m, v in rows:
        s, count = by.get(m, (0.0, 0))
        by[m] = (s + v, count + 1)
    lo, hi = min(by), max(by)
    grid = [add(lo, k) for k in range(mdiff(hi, lo) + 1)]
    S = np.array([by.get(m, (0.0, 0))[0] for m in grid])
    n = np.array([by.get(m, (0.0, 0))[1] for m in grid])
    N = n.sum()
    mu = S.sum() / N
    u = S - n * mu
    lrv = u @ u + 2 * sum((1 - L / (lags + 1)) * (u[L:] @ u[:-L]) for L in range(1, lags + 1))
    return float(mu / math.sqrt(lrv / N**2))


class ScriptBinding(unittest.TestCase):
    """The FX script runs the packaged helpers, not copies of its own."""

    def test_script_imports_the_package_helpers(self) -> None:
        """add, nw_t and panel_nw_t in the script's namespace are the package's objects."""
        namespace = runpy.run_path(str(SCRIPT), run_name="fx_ppp_oos_test")
        for name in ("add", "nw_t", "panel_nw_t"):
            with self.subTest(name=name):
                self.assertIs(namespace[name], getattr(newey_west, name))


class OriginalHelpers(unittest.TestCase):
    """Each packaged helper returns exactly what the script's original copy returned."""

    def test_month_arithmetic(self) -> None:
        """The month helpers agree forwards, backwards and across year ends."""
        for ym in ((1990, 1), (1999, 12), (2026, 6)):
            for k in (-25, -13, -12, -1, 0, 1, 11, 12, 13, 240):
                with self.subTest(ym=ym, k=k):
                    self.assertEqual(newey_west.add(ym, k), add(ym, k))
                    self.assertEqual(newey_west.mdiff(newey_west.add(ym, k), ym), k)
                    self.assertEqual(mdiff(add(ym, k), ym), k)

    def test_t_statistics(self) -> None:
        """nw_t and panel_nw_t agree exactly on overlapping, stacked and gapped panels."""
        rng = np.random.default_rng(1)
        months = [newey_west.add((1999, 10), k) for k in range(60)]
        x = rng.standard_normal(60) + 0.1
        rows = [(m, v + c) for m, v in zip(months, x, strict=True) for c in (-0.2, 0.0, 0.5)]
        gapped = [row for i, row in enumerate(rows) if not 30 <= i // 3 < 34]
        for lags in (0, 1, 11):
            with self.subTest(lags=lags):
                self.assertEqual(newey_west.nw_t(x, lags), nw_t(x, lags))
                self.assertEqual(newey_west.nw_t(list(x), lags), nw_t(list(x), lags))
                for panel in (rows, gapped, rows[::-1]):
                    self.assertEqual(newey_west.panel_nw_t(panel, lags), panel_nw_t(panel, lags))


if __name__ == "__main__":
    unittest.main()
