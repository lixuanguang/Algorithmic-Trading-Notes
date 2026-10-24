"""Tests that the packaged Newey-West helpers are the FX runners' own, bit for bit.

trading_notes.numerical.newey_west holds the pure helpers that fx_panel_inference took from
notes/artefacts/fx-determination-forecasting/fx_ppp_oos_test.py, whose empirical runs (and
fx_carry_test.py through it) still use their own copies until they migrate. These compare the
two on calendar arithmetic across year ends and gaps, and on t statistics with and without
lags, stacked rows and empty months, so that the copies cannot drift apart unnoticed. The
script is loaded without running it; it reads its data only in `main`.

Run: make test (uv run --frozen --no-editable pytest)
"""

import runpy
import unittest
from pathlib import Path

import numpy as np

from trading_notes.numerical import newey_west

SCRIPT = (
    Path(__file__).resolve().parents[3]
    / "notes"
    / "artefacts"
    / "fx-determination-forecasting"
    / "fx_ppp_oos_test.py"
)


def legacy(name: str) -> object:
    """Return one helper of the FX script, loaded under its own name so that main() is not run."""
    namespace: dict[str, object] = runpy.run_path(str(SCRIPT), run_name="fx_ppp_oos_test")
    return namespace[name]


class LegacyHelpers(unittest.TestCase):
    """Each packaged helper returns exactly what the script's copy returns."""

    def test_month_arithmetic(self) -> None:
        """The month helpers agree forwards, backwards and across year ends."""
        add, mdiff = legacy("add"), legacy("mdiff")
        assert callable(add) and callable(mdiff)
        for ym in ((1990, 1), (1999, 12), (2026, 6)):
            for k in (-25, -13, -12, -1, 0, 1, 11, 12, 13, 240):
                with self.subTest(ym=ym, k=k):
                    self.assertEqual(newey_west.add(ym, k), add(ym, k))
                    self.assertEqual(newey_west.mdiff(newey_west.add(ym, k), ym), k)
                    self.assertEqual(mdiff(add(ym, k), ym), k)

    def test_t_statistics(self) -> None:
        """nw_t and panel_nw_t agree exactly on overlapping, stacked and gapped panels."""
        nw_t, panel_nw_t = legacy("nw_t"), legacy("panel_nw_t")
        assert callable(nw_t) and callable(panel_nw_t)
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
