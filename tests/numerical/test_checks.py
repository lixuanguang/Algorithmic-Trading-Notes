"""Tests of the per-check report and the migrated numerical checks.

The numerical assertions themselves are the checks' own; these tests only confirm how a run
is reported, that each run starts fresh, and that a failure reaches the exit status.

Run: make test (uv run pytest)
"""

# standard library imports
import contextlib
import io
import re
import subprocess
import sys
import tempfile
import unittest
from collections.abc import Callable
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from unittest import mock

# project library imports
from tests.import_probe import HEAVY, import_effects
from trading_notes.numerical import (
    amm_pool,
    country_risk_premium,
    fra_settlement,
    funding_repo,
    multicurve,
)
from trading_notes.numerical.report import CheckReport

ARTEFACTS = Path(__file__).resolve().parents[2] / "notes" / "artefacts"


@dataclass(frozen=True)
class MigratedCheck:
    """A migrated numerical check and what its tests expect of it.

    Attributes:
        module: The implementation module, with `main()`.
        script: Its entrypoint under notes/artefacts/.
        replaced: A check function that the tests replace to force one failure.
        summary: The end of its output after that one forced failure.
        checks: The number of checks a passing run reports.
    """

    module: ModuleType
    script: Path
    replaced: str
    summary: str
    checks: int


LIST_SUMMARY = "\nFAILED: ['forced failure']\n"
CHECKS = [
    MigratedCheck(
        funding_repo,
        ARTEFACTS / "short-term-funding" / "funding-repo-checks.py",
        "check_margin_call",
        "\n1 check(s) failed: ['forced failure']\n",
        11,
    ),
    MigratedCheck(
        fra_settlement,
        ARTEFACTS / "rates-credit-mortgages" / "fra-settlement-check.py",
        "check_convexity",
        LIST_SUMMARY,
        11,
    ),
    MigratedCheck(
        multicurve,
        ARTEFACTS / "rates-credit-mortgages" / "multicurve-check.py",
        "check_two_curves",
        LIST_SUMMARY,
        6,
    ),
    MigratedCheck(
        amm_pool,
        ARTEFACTS / "crypto-perpetuals" / "amm-checks.py",
        "check_concentrated_position",
        LIST_SUMMARY,
        12,
    ),
    MigratedCheck(
        country_risk_premium,
        ARTEFACTS / "corporate-finance" / "country-risk-premium-check.py",
        "check_zero_limit",
        "FAILED: forced failure\n",
        23,
    ),
]
CHECK_LINE = re.compile(r"^  (ok |BAD) ", re.M)


def forced_failure(report: CheckReport, *_: object) -> None:
    """Stand in for a check function, recording one failed check."""
    report.ok("forced failure", False)


def captured(run: Callable[[], int]) -> tuple[int, str]:
    """Return a run's exit status and everything it printed."""
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        status = run()
    return status, out.getvalue()


class Reporting(unittest.TestCase):
    """CheckReport prints each check and keeps the failures of its own run."""

    def test_passing_checks_print_ok_lines(self) -> None:
        """Passing checks print `ok`, with a detail when one is given, and record nothing."""
        report = CheckReport()
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            report.ok("first", True)
            report.ok("second", True, "1.00")
        self.assertEqual(out.getvalue(), "  ok  first\n  ok  second: 1.00\n")
        self.assertEqual(report.failures, [])

    def test_failures_accumulate_in_order(self) -> None:
        """Failures print `BAD`, accumulate in run order and never end the process."""
        report = CheckReport()
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            report.ok("x", False)
            report.ok("y", True)
            report.ok("z", False, "detail")
        self.assertEqual(out.getvalue(), "  BAD x\n  ok  y\n  BAD z: detail\n")
        self.assertEqual(report.failures, ["x", "z"])

    def test_failures_belong_to_one_report(self) -> None:
        """The failure list is a copy, and a new report starts empty."""
        report = CheckReport()
        with contextlib.redirect_stdout(io.StringIO()):
            report.ok("x", False)
        report.failures.append("tampered")
        self.assertEqual(report.failures, ["x"])
        self.assertEqual(CheckReport().failures, [])


class MigratedChecks(unittest.TestCase):
    """The funding-repo and FRA-settlement checks, in process and as scripts."""

    def test_successive_runs_pass_identically(self) -> None:
        """Each run passes with its own report, so two runs print the same thing."""
        for check in CHECKS:
            with self.subTest(check.module.__name__):
                first, second = captured(check.module.main), captured(check.module.main)
                self.assertEqual(first[0], 0)
                self.assertEqual(len(CHECK_LINE.findall(first[1])), check.checks)
                self.assertTrue(first[1].endswith("\nall checks passed\n"))
                self.assertEqual(first, second)

    def test_failure_returns_1_and_does_not_leak(self) -> None:
        """A failed check gives status 1 and its summary; the next run is clean."""
        for check in CHECKS:
            with self.subTest(check.module.__name__):
                with mock.patch.object(check.module, check.replaced, forced_failure):
                    status, out = captured(check.module.main)
                self.assertEqual(status, 1)
                self.assertTrue(out.endswith(check.summary), out[-200:])
                self.assertNotIn("BAD", out.replace("  BAD forced failure\n", ""))
                self.assertEqual(captured(check.module.main)[0], 0)

    def test_entrypoints_run_from_any_directory(self) -> None:
        """Each script passes, isolated, from its own folder and from an unrelated one."""
        with tempfile.TemporaryDirectory() as elsewhere:
            for check in CHECKS:
                for cwd in (check.script.parent, Path(elsewhere)):
                    with self.subTest(check.script.name, cwd=cwd.name):
                        done = subprocess.run(
                            [sys.executable, "-I", "-W", "error", str(check.script)],
                            cwd=cwd,
                            capture_output=True,
                            text=True,
                        )
                        self.assertEqual((done.returncode, done.stderr), (0, ""))
                        self.assertEqual(done.stdout, captured(check.module.main)[1])

    def test_entrypoint_propagates_failure_status(self) -> None:
        """A failed check makes the script exit 1, with no traceback."""
        for check in CHECKS:
            with self.subTest(check.script.name):
                # Replace one check, then execute the script as `python <script>` would.
                code = (
                    f"import runpy, {check.module.__name__} as m\n"
                    "import tests.numerical.test_checks as t\n"
                    f"m.{check.replaced} = t.forced_failure\n"
                    f"runpy.run_path({str(check.script)!r}, run_name='__main__')\n"
                )
                done = subprocess.run(
                    [sys.executable, "-c", code],
                    cwd=Path(__file__).resolve().parents[2],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(done.returncode, 1, done.stderr)
                self.assertTrue(done.stdout.endswith(check.summary))
                self.assertEqual(done.stderr, "")

    def test_imports_have_no_side_effects(self) -> None:
        """Importing the checks prints nothing, opens no data and runs no check."""
        with tempfile.TemporaryDirectory() as elsewhere:
            effects = import_effects(
                [check.module.__name__ for check in CHECKS],
                [*HEAVY, "trading_notes.structure"],
                Path(elsewhere),
            )
            self.assertEqual(effects.returncode, 0, effects.stderr)
            self.assertEqual((effects.opened, effects.printed, effects.loaded), ([], "", []))
            self.assertEqual(list(Path(elsewhere).iterdir()), [])


class ExactCountryRisk(unittest.TestCase):
    """The country-risk example's exact run stays in rational arithmetic."""

    def test_exact_example_is_rational_throughout(self) -> None:
        """Every exact result is a Fraction, equal to its rational closed form."""
        exact = country_risk_premium.example(Fraction)
        self.assertTrue(all(type(value) is Fraction for value in exact.values()), exact)
        self.assertEqual(exact["crp relative sd"], Fraction(10, 3))
        self.assertEqual(exact["ke weighted"], Fraction(331, 25))
        self.assertEqual(exact["ke local inflation"], Fraction(87672, 5125))  # 17.1067317...
        self.assertTrue(all(type(v) is float for v in country_risk_premium.example(float).values()))

    def test_premium_formulas_keep_their_input_type(self) -> None:
        """The premium formulas return Fraction for Fraction inputs and float for floats."""
        third = Fraction(1, 3)
        self.assertIs(type(country_risk_premium.relative_sd_crp(third, third, third)), Fraction)
        self.assertIs(type(country_risk_premium.melded_crp(third, third, third)), Fraction)
        self.assertIs(type(country_risk_premium.default_spread_crp(third)), Fraction)
        self.assertIs(type(country_risk_premium.melded_crp(2.25, 24, 17)), float)


if __name__ == "__main__":
    unittest.main()
