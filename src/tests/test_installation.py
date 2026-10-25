"""The project environment holds a current, non-editable copy of trading_notes."""

# CPython skips an editable install's .pth file once macOS marks it hidden, which leaves the
# package unimportable; and uv reinstalls the project editable on any `uv sync` or `uv run`
# without --no-editable. So these tests check the installed copy itself, and that every uv
# command the repository runs or documents passes --no-editable.

import importlib.metadata
import json
import os
import re
import unittest
from pathlib import Path

import trading_notes

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "src" / "trading_notes"
DISTRIBUTION = "algorithmic-trading-notes"
# Not maintained here: the vendored guide, git-ignored local copies and the environment at the
# top level; caches anywhere; dated records of commands as run.
TOP_LEVEL_SKIPPED = {".git", ".venv", "guide", "reading_materials", "reading materials"}
CACHES = {"__pycache__", ".mypy_cache", ".pytest_cache", ".ruff_cache"}
HISTORICAL = {ROOT / "notes" / "source-review-records.md"}
TEXT_SUFFIXES = {".md", ".py", ".tex", ".toml", ".yaml", ".yml"}
# A command that syncs or runs with uv, written out or through the Makefile's $(UV); a
# command name alone in backticks, as prose names it, is not one.
UV_COMMAND = re.compile(r"(?:\buv|\$\(UV\)) (?:sync|run)\b(?!`)[^\n`]*")


def maintained_files() -> list[Path]:
    """Return the repository's maintained text files that may hold uv commands."""
    found = []
    for folder, subfolders, names in os.walk(ROOT):
        here = Path(folder)
        subfolders[:] = sorted(
            name
            for name in subfolders
            if not (here == ROOT and name in TOP_LEVEL_SKIPPED) and name not in CACHES
        )
        found += [
            here / name
            for name in sorted(names)
            if (Path(name).suffix in TEXT_SUFFIXES or name == "Makefile")
            and here / name not in HISTORICAL
        ]
    return found


def sources(root: Path) -> dict[str, bytes]:
    """Return the files below root other than bytecode, by relative path, with their contents."""
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
    }


class Installation(unittest.TestCase):
    """trading_notes is imported from a non-editable copy equal to src/trading_notes."""

    def test_project_is_installed_non_editable(self) -> None:
        """The install records editable false and adds no .pth file."""
        distribution = importlib.metadata.distribution(DISTRIBUTION)
        direct_url: object = json.loads(distribution.read_text("direct_url.json") or "{}")
        self.assertIsInstance(direct_url, dict)
        assert isinstance(direct_url, dict)
        self.assertEqual(direct_url.get("dir_info"), {"editable": False})
        self.assertFalse([f for f in distribution.files or [] if f.suffix == ".pth"])

    def test_imports_come_from_the_installed_copy(self) -> None:
        """The imported package is the installed copy, not the source folder."""
        package = Path(trading_notes.__file__).resolve().parent
        self.assertNotEqual(package, SOURCE)
        self.assertEqual(package.parent.name, "site-packages")

    def test_installed_copy_matches_source(self) -> None:
        """The installed files are exactly the source files, byte for byte."""
        installed = sources(Path(trading_notes.__file__).resolve().parent)
        source = sources(SOURCE)
        self.assertEqual(sorted(installed), sorted(source))
        self.assertEqual([p for p in source if installed[p] != source[p]], [])


class UvCommands(unittest.TestCase):
    """Every command that syncs or runs with uv keeps the non-editable installation.

    A command counts when it is written out: in a recipe, hook, workflow, docstring or code
    block, or inline in prose (`uv run --frozen --no-editable python <script>`). A command name
    alone in backticks (`uv run`) is prose about it, not an instruction. The dated run records of
    notes/source-review-records.md are frozen evidence and not scanned.
    """

    def test_scan_reaches_maintained_instructions(self) -> None:
        """The scan includes the coverage notes, CI, research protocols and all Python."""
        scanned = set(maintained_files())
        python = set((ROOT / "src").rglob("*.py")) - set((ROOT / "src").rglob("__pycache__/*"))
        protocols = set((ROOT / "src" / "data").glob("*/protocols/*.md"))
        self.assertTrue(python and protocols)
        self.assertEqual((python | protocols) - scanned, set())
        self.assertIn(ROOT / "Makefile", scanned)
        self.assertIn(ROOT / "notes" / "coverage" / "README.md", scanned)
        self.assertIn(ROOT / ".github" / "workflows" / "ci.yml", scanned)

    def test_uv_commands_pass_no_editable(self) -> None:
        """Each written-out uv sync or run command in a maintained file passes --no-editable."""
        for path in maintained_files():
            for command in UV_COMMAND.findall(path.read_text()):
                with self.subTest(path=path.relative_to(ROOT).as_posix(), command=command):
                    self.assertIn(" --no-editable", command)

    def test_prose_and_commands_are_told_apart(self) -> None:
        """A bare backticked name is prose; a written-out command is checked, inline or not."""
        self.assertEqual(UV_COMMAND.findall("any `uv sync` or `uv run` without the flag"), [])
        self.assertEqual(
            UV_COMMAND.findall("Run (`uv run --no-editable x.py`) or\n  uv sync --no-editable"),
            ["uv run --no-editable x.py", "uv sync --no-editable"],
        )


if __name__ == "__main__":
    unittest.main()
