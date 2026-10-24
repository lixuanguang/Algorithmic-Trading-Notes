"""Tests of the Sharpe statistics against references independent of the implementation.

The example's full run, with the stated table values, is tested in test_checks.py. These
compare Lo's annualisation factor with the variance of a sum of AR(1) returns computed from
its autocorrelation matrix, the deflated Sharpe ratio with the standard library's normal
distribution instead of SciPy's, the rho = 0 branch, the unit conversions, and confirm that a
changed table value is reported.

Run: make test (uv run --frozen --no-editable pytest)
"""

import contextlib
import io
import math
import unittest
from statistics import NormalDist
from unittest import mock

import numpy as np

from trading_notes.numerical import sharpe_statistics as sh
from trading_notes.numerical.report import CheckReport


def eta_from_covariance(q: int, rho: float) -> float:
    """Return q / sqrt(Var(sum of q unit-variance AR(1) returns)), from the full matrix."""
    lags = np.abs(np.subtract.outer(np.arange(q), np.arange(q)))
    return q / math.sqrt(float(np.sum(np.float64(rho) ** lags)))


class StandardError(unittest.TestCase):
    """Eq. (9): sqrt((1 + SR^2 / 2) / T)."""

    def test_zero_sharpe_ratio(self) -> None:
        """At SR = 0 the standard error is 1 / sqrt(T)."""
        self.assertEqual(sh.se(0.0, 64), 0.125)


class Annualisation(unittest.TestCase):
    """Eqs. (20) and (22) against the variance of a sum of AR(1) returns."""

    def test_both_forms_match_the_covariance_matrix(self) -> None:
        """Every table cell, and a few more, agree with the brute-force variance."""
        cells = [*sh.TABLE_2, (1, 0.5), (3, -0.7), (60, 0.95)]
        for q, rho in cells:
            with self.subTest(q=q, rho=rho):
                want = eta_from_covariance(q, rho)
                self.assertAlmostEqual(sh.eta_sum(q, rho), want, delta=1e-9 * want)
                self.assertAlmostEqual(sh.eta_22(q, rho), want, delta=1e-9 * want)

    def test_zero_correlation(self) -> None:
        """At rho = 0 the closed form returns sqrt(q) itself, and its limit on either side."""
        self.assertEqual(sh.eta_22(12, 0.0), math.sqrt(12))
        self.assertAlmostEqual(sh.eta_sum(12, 0.0), math.sqrt(12), places=14)
        for rho in (1e-7, -1e-7):
            self.assertAlmostEqual(sh.eta_22(12, rho), math.sqrt(12), places=5)


class DeflatedSharpe(unittest.TestCase):
    """Eqs. (1)-(2), with the normal distribution taken from the standard library."""

    def test_against_the_standard_library_normal(self) -> None:
        """SR0 and DSR match a NormalDist evaluation of the same equations."""
        z = NormalDist()
        for N, g3, g4 in ((100, -3, 10), (46, -3, 10), (88, 0, 3)):
            with self.subTest(N=N):
                s0 = math.sqrt(sh.EXAMPLE_V) * (
                    (1 - sh.EULER_GAMMA) * z.inv_cdf(1 - 1 / N)
                    + sh.EULER_GAMMA * z.inv_cdf(1 - 1 / (N * math.e))
                )
                self.assertAlmostEqual(sh.sr0(N, sh.EXAMPLE_V), s0, places=12)
                sr = sh.EXAMPLE_SR
                x = (sr - s0) * math.sqrt(1250 - 1) / math.sqrt(1 - g3 * sr + (g4 - 1) / 4 * sr**2)
                self.assertAlmostEqual(sh.dsr(sr, s0, 1250, g3, g4), z.cdf(x), places=12)

    def test_observed_equal_to_expected_maximum(self) -> None:
        """When SR equals SR0, DSR is one half."""
        self.assertEqual(sh.dsr(0.1, 0.1, 1250, -3, 10), 0.5)

    def test_annual_inputs_become_per_observation(self) -> None:
        """V = 1/2 and SR = 2.5 a year become 1/500 and 2.5 / sqrt(250) per observation."""
        self.assertEqual(sh.EXAMPLE_V, 1 / 500)
        self.assertAlmostEqual(sh.EXAMPLE_SR * math.sqrt(250), 2.5, places=14)
        self.assertEqual(sh.EXAMPLE_T, 5 * 250)


class StatedValues(unittest.TestCase):
    """The table values are stated, not derived: a changed one is reported."""

    def test_changed_table_value_fails(self) -> None:
        """Lo's 4.17 changed to 4.27 fails only its own comparison."""
        changed = {**sh.TABLE_2, (12, -0.2): 4.27}
        report = CheckReport()
        out = io.StringIO()
        with mock.patch.object(sh, "TABLE_2", changed), contextlib.redirect_stdout(out):
            sh.check_annualisation(report)
        self.assertEqual(report.failures, ["eta(12, rho=-0.2) by eq. (22) against Table 2"])
        self.assertIn(
            "  BAD eta(12, rho=-0.2) by eq. (22) against Table 2: "
            "4.170848 (want 4.27, tol 0.006)\n",
            out.getvalue(),
        )


if __name__ == "__main__":
    unittest.main()
