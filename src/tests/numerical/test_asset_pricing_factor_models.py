"""Tests of how the asset-pricing check finds and reads the compendium figure it checks.

The example's full run is tested in test_checks.py. These confirm that the figure is read
rather than assumed, and that `--root` locates it from any working directory.

Run: make test (uv run --frozen --no-editable pytest)
"""

import contextlib
import io
import os
import tempfile
import unittest
from pathlib import Path

from trading_notes.numerical import asset_pricing_factor_models as apm
from trading_notes.numerical.report import CheckReport
from trading_notes.numerical.repository import repository_root

ROOT = Path(__file__).resolve().parents[3]


class FigureLocation(unittest.TestCase):
    """The figure check reads the file below the repository root it is given."""

    def test_moved_point_fails_the_figure_check(self) -> None:
        """A figure whose high-beta point is moved off the line fails the figure check."""
        text = (ROOT / apm.FIGURE).read_text()
        self.assertEqual(text.count("(1.6,12.01)"), 1)
        with tempfile.TemporaryDirectory() as folder:
            moved = Path(folder) / apm.FIGURE.name
            moved.write_text(text.replace("(1.6,12.01)", "(1.6,12.11)"))
            report = CheckReport()
            with contextlib.redirect_stdout(io.StringIO()):
                apm.check_figure(report, moved)
        self.assertEqual(
            report.failures,
            [
                "SML drawn from (0, 5.29) to (2, 13.69); points for beta 0.6, 1, 1.6 on it; the"
                " 11.5 forecast above it"
            ],
        )

    def test_root_option_and_default(self) -> None:
        """`--root` gives the resolved root; without it the working directory is the root."""
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(repository_root("", ["--root", folder]), Path(folder).resolve())
            before = Path.cwd()
            os.chdir(folder)
            try:
                self.assertEqual(repository_root("", []), Path(folder).resolve())
            finally:
                os.chdir(before)
        self.assertTrue((repository_root("", ["--root", str(ROOT)]) / apm.FIGURE).is_file())


if __name__ == "__main__":
    unittest.main()
