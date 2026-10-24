"""The checker scripts and package as a user runs them: as processes, from anywhere."""

# Each process runs isolated (`python -I`), from an unrelated working directory, so the package
# must come from the project environment and not from the script's folder, the working directory
# or a path that pytest adds.

import json
import platform
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from trading_notes.cli.check_runtime import Runtime

from ..import_probe import HEAVY, dependency_reads, import_effects
from .repository import GOOD_ENTRY, SyntheticRepository
from .test_coverage_check import OUT_A, CoverageFixture

COMPENDIUM_KEYS = [
    "pathways",
    "parts",
    "pathways_rendered",
    "entries",
    "entries_by_section",
    "entries_by_type",
    "entries_with_gaps",
    "problems",
]
COVERAGE_KEYS = [
    "objectives",
    "objectives_total",
    "topics_total",
    "objectives_by_section",
    "next_actions",
    "outline_modules",
    "outline_items",
    "outline_items_by_component",
    "outline_items_unreviewed",
    "outlines_verified",
    "problems",
]


class Entrypoints(unittest.TestCase):
    """Command-line contract of the check_compendium and check_coverage modules."""

    def setUp(self) -> None:
        """Create a valid repository and an unrelated working directory."""
        self.repo = SyntheticRepository()
        self.addCleanup(self.repo.close)
        self.repo.write("compendium/sec-a/topic.tex", GOOD_ENTRY)
        self.repo.write("notes/pathways/sec-a.md", "## Entries\n- `mod:good`\n")
        elsewhere = tempfile.TemporaryDirectory()
        self.addCleanup(elsewhere.cleanup)
        self.cwd = Path(elsewhere.name)

    def run_python(self, *args: str) -> subprocess.CompletedProcess[str]:
        """Run the environment's Python, isolated, from the unrelated directory."""
        return subprocess.run(
            [sys.executable, "-I", *args], cwd=self.cwd, capture_output=True, text=True
        )

    def run_tool(self, name: str, *args: str) -> subprocess.CompletedProcess[str]:
        """Run a checker module of trading_notes.cli on the synthetic repository."""
        return self.run_python(
            "-m", f"trading_notes.cli.{name}", "--root", str(self.repo.root), *args
        )

    def test_json_reports_keep_their_schema(self) -> None:
        """Both JSON reports keep their keys, in order, and pass on valid input."""
        for name, keys in (
            ("check_compendium", COMPENDIUM_KEYS),
            ("check_coverage", COVERAGE_KEYS),
        ):
            with self.subTest(name):
                done = self.run_tool(name, "--json", "--check")
                self.assertEqual(done.stderr, "")
                report = json.loads(done.stdout)
                self.assertEqual(list(report), keys)
                # The synthetic repository has no coverage files, which only coverage reports.
                self.assertEqual(done.returncode, 1 if name == "check_coverage" else 0)

    def test_exit_status_and_text_report(self) -> None:
        """Problems exit 1 only with --check; the text report states its limits."""
        self.repo.write("compendium/sec-a/topic.tex", GOOD_ENTRY.replace("[p.~3]", ""))
        done = self.run_tool("check_compendium")
        self.assertEqual(done.returncode, 0)
        self.assertTrue(done.stdout.startswith("Entries: 1  model 1\n"))
        self.assertIn("missing locator for cat-key", done.stdout)
        self.assertTrue(done.stdout.endswith("not the truth of claims.\n"))
        self.assertEqual(self.run_tool("check_compendium", "--check").returncode, 1)

    def test_unreadable_guide_exits_1_with_a_message(self) -> None:
        """A malformed pinned guide is reported on stderr with status 1, with or without --check."""
        self.repo.write("guide/learning_routes.json", "[]")
        for name in ("check_compendium", "check_coverage"):
            for args in ((), ("--check",), ("--json",)):
                with self.subTest(name, args=args):
                    done = self.run_tool(name, *args)
                    self.assertEqual(done.returncode, 1)
                    self.assertEqual(done.stdout, "")
                    self.assertIn(
                        "error: guide/learning_routes.json: expected a JSON object", done.stderr
                    )
                    self.assertNotIn("Traceback", done.stderr)

    def test_usage_errors_exit_2(self) -> None:
        """Argparse usage errors keep their own status."""
        for name in ("check_compendium", "check_coverage"):
            with self.subTest(name):
                done = self.run_tool(name, "--no-such-option")
                self.assertEqual(done.returncode, 2)
                self.assertIn("unrecognized arguments: --no-such-option", done.stderr)

    def test_malformed_item_content_fails_check(self) -> None:
        """Wrong-typed crosswalk item content fails the coverage check with a named field."""
        fx = CoverageFixture(self.repo)
        self.assertEqual(fx.report()["problems"], [])
        self.assertEqual(self.run_tool("check_coverage", "--check").returncode, 0)
        fx.items[0]["command_verbs"] = 17
        fx.items[1]["residual_gap"] = 0
        fx.report()
        done = self.run_tool("check_coverage", "--check")
        self.assertEqual(done.returncode, 1)
        self.assertIn(
            f"`{OUT_A}:m001:b01` field `command_verbs` must be a list of strings", done.stdout
        )
        self.assertIn(f"`{OUT_A}:m001:b02` field `residual_gap` must be a string", done.stdout)

    def test_package_imports_without_side_effects(self) -> None:
        """Importing each module alone reads no data, prints nothing and loads no numerical code.

        Each module gets its own fresh process. The records need pydantic, which may read the
        installed-package metadata it reads whenever its first model is defined; NumPy,
        pandas, SciPy and the numerical package are never loaded.
        """
        uses_pydantic = {
            "trading_notes": False,
            "trading_notes.records": True,
            "trading_notes.structure": False,
            "trading_notes.structure.json_fields": False,
            "trading_notes.structure.compendium": True,
            "trading_notes.structure.compendium_check": True,
            "trading_notes.structure.coverage_check": True,
            "trading_notes.cli": False,
            "trading_notes.cli.check_compendium": True,
            "trading_notes.cli.check_coverage": True,
            "trading_notes.cli.check_runtime": True,
        }
        startup = dependency_reads(("pydantic",), self.cwd)
        for name, pydantic in uses_pydantic.items():
            with self.subTest(name):
                effects = import_effects(
                    [name],
                    [*HEAVY, "trading_notes.numerical", "trading_notes.numerical.report"],
                    self.cwd,
                )
                self.assertEqual(effects.returncode, 0, effects.stderr)
                self.assertEqual(effects.reads_beyond(startup if pydantic else ()), [])
                self.assertEqual(
                    (effects.printed, effects.loaded), ("", ["pydantic"] if pydantic else [])
                )
                self.assertEqual(effects.stderr, "")
                self.assertTrue(effects.random_unchanged)
                self.assertEqual(list(self.cwd.iterdir()), [])


ROOT = Path(__file__).resolve().parents[3]
SUPPORTED = Runtime(
    implementation="CPython",
    version="3.14.7",
    gil_enabled=True,
    free_threaded_build=False,
    machine="x86_64",
)


class RuntimeCheck(unittest.TestCase):
    """The CI runtime check: pinned CPython version, the GIL, and the supported machine."""

    def test_each_requirement_is_reported(self) -> None:
        """The supported runtime passes; each departure from it is one problem."""
        self.assertEqual(SUPPORTED.problems("3.14.7", "x86_64"), [])
        for change, problem in (
            ({"implementation": "PyPy"}, "implementation PyPy, not CPython"),
            ({"version": "3.14.6"}, "version 3.14.6, not the pinned 3.14.7"),
            ({"gil_enabled": False}, "a free-threaded build or a disabled GIL"),
            ({"free_threaded_build": True}, "a free-threaded build or a disabled GIL"),
            ({"machine": "arm64"}, "machine arm64, not x86_64"),
        ):
            with self.subTest(change):
                runtime = SUPPORTED.model_copy(update=change)
                self.assertEqual(runtime.problems("3.14.7", "x86_64"), [problem])

    def test_current_interpreter(self) -> None:
        """The environment's interpreter is the pinned CPython with the GIL."""
        runtime = Runtime.current()
        self.assertEqual(runtime.machine, platform.machine())
        pinned = (ROOT / ".python-version").read_text().strip()
        self.assertEqual(runtime.problems(pinned, platform.machine()), [])

    def test_command_line_status(self) -> None:
        """Run from elsewhere with --root, it exits 0 on this machine and 1 for another one."""
        with tempfile.TemporaryDirectory() as tmp:
            command = [sys.executable, "-I", "-m", "trading_notes.cli.check_runtime"]
            command += ["--root", str(ROOT), "--machine"]
            ok = subprocess.run(
                [*command, platform.machine()], cwd=tmp, capture_output=True, text=True
            )
            self.assertEqual((ok.returncode, ok.stderr), (0, ""))
            self.assertTrue(ok.stdout.startswith(sys.version))
            bad = subprocess.run(
                [*command, "no-such-machine"], cwd=tmp, capture_output=True, text=True
            )
            self.assertEqual(bad.returncode, 1)
            self.assertIn(f"machine {platform.machine()}, not no-such-machine", bad.stderr)


if __name__ == "__main__":
    unittest.main()
