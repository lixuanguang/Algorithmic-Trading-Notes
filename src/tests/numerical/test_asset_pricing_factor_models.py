"""Tests of the asset-pricing figure check, its --root option and the CAPM and APT classes."""

# The example's full run is tested in test_checks.py. These confirm that the figure is read rather
# than assumed, and that `--root` locates it from any working directory.

import contextlib
import io
import os
import tempfile
import unittest
from pathlib import Path

import numpy as np

from trading_notes.numerical.asset_pricing_models import asset_pricing_checks as apm
from trading_notes.numerical.asset_pricing_models.capm import (
    AptPricing,
    CapmFit,
    MarketLines,
    replicating_weights,
)
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


class CapmAndApt(unittest.TestCase):
    """The regression's closed forms, the market lines and APT replication."""

    def test_exact_line_has_zero_residuals(self) -> None:
        """Y = 0.5 + 2x fits exactly: alpha 0.5, beta 2, R^2 1, zero standard errors."""
        x = np.array([-1.0, 0.0, 1.0, 2.0])
        fit = CapmFit.of(x, 0.5 + 2 * x)
        self.assertAlmostEqual(fit.alpha, 0.5, places=14)
        self.assertAlmostEqual(fit.beta, 2.0, places=14)
        self.assertAlmostEqual(fit.r_squared, 1.0, places=14)
        self.assertAlmostEqual(fit.se_beta, 0.0, places=14)

    def test_cml_at_systematic_risk_equals_sml(self) -> None:
        """An asset's systematic s.d. beta s_M puts the CML on the SML's return."""
        lines = MarketLines(risk_free=5.29, premium=4.20, market_sd=16.0)
        self.assertAlmostEqual(lines.cml(1.25 * 16.0), lines.sml(1.25), places=12)

    def test_replica_matches_sensitivities_and_price(self) -> None:
        """Replicating weights sum to one, match the target and earn the APT return."""
        apt = AptPricing(zero_beta=4.0, premia=np.array([3.0, 1.5]))
        portfolios = np.array([[1.0, 0.5], [0.5, -0.5], [1.5, 1.0]])
        target = np.array([0.8, 0.2])
        w = replicating_weights(portfolios, target)
        np.testing.assert_allclose(w @ portfolios, target, atol=1e-12)
        self.assertAlmostEqual(w.sum(), 1.0, places=12)
        self.assertAlmostEqual(
            float(w @ apt.expected(portfolios)), float(apt.expected(target[None, :])[0]), 12
        )


if __name__ == "__main__":
    unittest.main()
