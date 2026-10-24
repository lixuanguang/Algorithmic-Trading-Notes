"""Tests of where the asset-pricing check finds the compendium figure it checks.

The example's full run is tested in test_checks.py, from the entry's folder. The last check
reads the security market line drawn in the compendium: by default relative to the working
directory, as the original script did from its folder, and at the location the entrypoint
passes from anywhere else. These confirm that the figure is read rather than assumed, and that
the default from an unrelated folder fails as the original script did, rather than passing.

Run: make test (uv run --frozen --no-editable pytest)
"""

# standard library imports
import contextlib
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

# project library imports
from trading_notes.numerical import asset_pricing_factor_models as apm

FIGURE = (
    Path(__file__).resolve().parents[2]
    / "compendium"
    / "asset-pricing"
    / "figures"
    / "security-market-line.tikz"
)


class FigureLocation(unittest.TestCase):
    """The figure check reads the file it is given."""

    def test_moved_point_fails_the_figure_check(self) -> None:
        """A figure whose high-beta point is moved off the line fails only the figure check."""
        text = FIGURE.read_text()
        self.assertEqual(text.count("(1.6,12.01)"), 1)
        with tempfile.TemporaryDirectory() as folder:
            moved = Path(folder) / FIGURE.name
            moved.write_text(text.replace("(1.6,12.01)", "(1.6,12.11)"))
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                status = apm.main(moved)
        self.assertEqual(status, 1)
        self.assertTrue(
            out.getvalue().endswith(
                "\nFAILED: SML drawn from (0, 5.29) to (2, 13.69); points for beta 0.6, 1, 1.6 on"
                " it; the 11.5 forecast above it\n"
            )
        )

    def test_default_from_an_unrelated_folder_fails(self) -> None:
        """Run from elsewhere, the default path finds no figure: the run stops with an error."""
        with tempfile.TemporaryDirectory() as elsewhere:
            done = subprocess.run(
                [sys.executable, "-I", "-m", apm.__name__],
                cwd=elsewhere,
                capture_output=True,
                text=True,
            )
        self.assertEqual(done.returncode, 1)
        self.assertNotIn("all checks passed", done.stdout)
        self.assertTrue(done.stdout.endswith("== figure: security market line coordinates\n"))
        self.assertIn("FileNotFoundError", done.stderr)
        self.assertIn(str(apm.FIGURE), done.stderr)


if __name__ == "__main__":
    unittest.main()
