"""The checker scripts and package as a user runs them: as processes, from anywhere.

Each process runs isolated (`python -I`), from an unrelated working directory, so the
package must come from the project environment and not from the script's folder, the
working directory or a path that pytest adds.

Run: make test (uv run --frozen --no-editable pytest)
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from ..import_probe import HEAVY, import_effects
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

        Each module gets its own fresh process, so no heavy dependency is ever allowed here.
        """
        for name in (
            "trading_notes",
            "trading_notes.structure",
            "trading_notes.structure.json_fields",
            "trading_notes.structure.compendium",
            "trading_notes.structure.compendium_check",
            "trading_notes.structure.coverage_check",
            "trading_notes.cli",
            "trading_notes.cli.check_compendium",
            "trading_notes.cli.check_coverage",
        ):
            with self.subTest(name):
                effects = import_effects(
                    [name],
                    [*HEAVY, "trading_notes.numerical", "trading_notes.numerical.report"],
                    self.cwd,
                )
                self.assertEqual(effects.returncode, 0, effects.stderr)
                self.assertEqual((effects.opened, effects.printed, effects.loaded), ([], "", []))
                self.assertEqual(effects.stderr, "")
                self.assertTrue(effects.random_unchanged)
                self.assertEqual(list(self.cwd.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
