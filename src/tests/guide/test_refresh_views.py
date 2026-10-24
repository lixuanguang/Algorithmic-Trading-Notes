"""Tests of the guide generator against the vendored guide, and of its input checks."""

# A full refresh of the vendored guide/ into a temporary folder must reproduce the committed guide
# source, HTML notes and recency export byte for byte, from an unrelated working folder. Broken
# route files and catalogue commands must stop the refresh with an error instead.

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Final

from trading_notes.guide.charts import spread
from trading_notes.guide.routes import LearningRoutes, RouteError, RouteIndex
from trading_notes.guide.tex_text import (
    TexError,
    argument,
    check_one_line_commands,
    tex_escape,
    to_html,
)

GUIDE: Final = Path(__file__).resolve().parents[3] / "guide"
OUTPUTS: Final = (
    "institutional_quantitative_finance_learning_guide.tex",
    "catalogue_extended_notes.html",
    "catalogue_recency.json",
)


def refresh(guide: Path, output: Path, cwd: Path) -> subprocess.CompletedProcess[str]:
    """Run the generator as a user would, isolated, from cwd, on a guide folder."""
    return subprocess.run(
        [
            sys.executable,
            "-I",
            "-W",
            "error",
            "-m",
            "trading_notes.guide.refresh_views",
            "--guide",
            str(guide),
            "--output",
            str(output),
        ],
        cwd=cwd,
        capture_output=True,
        text=True,
    )


class FullRefresh(unittest.TestCase):
    """The committed outputs are exactly what the generator writes from the vendored sources."""

    def test_reproduces_the_committed_outputs(self) -> None:
        """Three files byte for byte, written only to the output folder, with the summary line."""
        with tempfile.TemporaryDirectory() as out, tempfile.TemporaryDirectory() as elsewhere:
            done = refresh(GUIDE, Path(out), Path(elsewhere))
            self.assertEqual((done.returncode, done.stderr), (0, ""))
            self.assertTrue(done.stdout.startswith("Refreshed 49 overview routes"))
            self.assertEqual(sorted(p.name for p in Path(out).iterdir()), sorted(OUTPUTS))
            for name in OUTPUTS:
                with self.subTest(name):
                    self.assertEqual((Path(out) / name).read_bytes(), (GUIDE / name).read_bytes())
            self.assertEqual(list(Path(elsewhere).iterdir()), [])

    def test_root_locates_the_guide(self) -> None:
        """With --root and no --guide, the sources are read from ROOT/guide."""
        with tempfile.TemporaryDirectory() as out, tempfile.TemporaryDirectory() as elsewhere:
            done = subprocess.run(
                [
                    sys.executable,
                    "-I",
                    "-m",
                    "trading_notes.guide.refresh_views",
                    "--root",
                    str(GUIDE.parent),
                    "--output",
                    out,
                ],
                cwd=elsewhere,
                capture_output=True,
                text=True,
            )
            self.assertEqual((done.returncode, done.stderr), (0, ""))
            name = OUTPUTS[2]
            self.assertEqual((Path(out) / name).read_bytes(), (GUIDE / name).read_bytes())

    def test_broken_route_file_stops_the_refresh(self) -> None:
        """A bare section number in prose exits 1 with the rule's message and writes nothing."""
        with tempfile.TemporaryDirectory() as tmp:
            root, out = Path(tmp) / "guide", Path(tmp) / "out"
            root.mkdir()
            for name in (
                "institutional_quantitative_finance_reading_list.tex",
                "institutional_quantitative_finance_reading_list.aux",
                "learning_routes.json",
            ):
                shutil.copy(GUIDE / name, root / name)
            data = json.loads((root / "learning_routes.json").read_text())
            data["routes"][0]["outcome"] += " See Section 3."
            (root / "learning_routes.json").write_text(json.dumps(data))
            done = refresh(root, out, Path(tmp))
            self.assertEqual(done.returncode, 1)
            self.assertIn("not numbers", done.stderr)
            self.assertFalse(out.exists())


class RouteRules(unittest.TestCase):
    """The route index rejects files that would print wrong numbers or broken links."""

    def setUp(self) -> None:
        """Load the vendored route file as data."""
        self.data = json.loads((GUIDE / "learning_routes.json").read_text())

    def index(self) -> RouteIndex:
        """Validate the possibly edited data and index it."""
        return RouteIndex(LearningRoutes.model_validate(self.data))

    def test_vendored_routes_pass(self) -> None:
        """The committed file satisfies every rule."""
        index = self.index()
        self.assertEqual((len(index.overviews), len(index.routes)), (49, 276))

    def test_unknown_reference_and_unknown_field(self) -> None:
        """A reference to a missing route fails the checks; an unknown field fails validation."""
        self.data["routes"][0]["outcome"] += " [[no-such-route]]"
        with self.assertRaises(RouteError):
            self.index()
        self.data = json.loads((GUIDE / "learning_routes.json").read_text())
        self.data["specialist_routes"][0]["specialist_order"] = []
        with self.assertRaises(ValueError):
            self.index()

    def test_moved_legacy_label(self) -> None:
        """An inherited legacy label must stay with its original overview key."""
        labelled = [r for r in self.data["routes"] if "legacy_label" in r]
        labelled[0]["legacy_label"], labelled[1]["legacy_label"] = (
            labelled[1]["legacy_label"],
            labelled[0]["legacy_label"],
        )
        with self.assertRaises(RouteError):
            self.index()

    def test_prose_prints_current_numbers(self) -> None:
        """Route and part references print as links to their numbers, or plain inside links."""
        index = self.index()
        first = index.parts[0]
        key = first.routes[0]
        self.assertEqual(
            index.prose(f"see [[{key}]] in [[part:{first.id}]] & more"),
            rf"see \hyperref[route-{key}]{{\ref*{{route-{key}}}}} in"
            rf" \hyperref[part-{first.id}]{{I}} \& more",
        )
        self.assertEqual(index.prose(f"[[{key}]]", linked=False), rf"\ref*{{route-{key}}}")


class TexHelpers(unittest.TestCase):
    """Argument parsing, escaping, one-line commands, HTML rendering and node spreading."""

    def test_argument_parsing(self) -> None:
        """Nested and escaped braces are read; an unbalanced argument raises TexError."""
        self.assertEqual(argument(r"x {a{b}\}c} y", 1), (r"a{b}\}c", 11))
        with self.assertRaises(TexError):
            argument("{open", 0)
        with self.assertRaises(TexError):
            argument("x", 0)

    def test_escape_and_html(self) -> None:
        """TeX specials are escaped; accents, links and dashes render as HTML."""
        self.assertEqual(tex_escape("a_b & 50%"), r"a\_b \& 50\%")
        self.assertEqual(
            to_html(r"G\"odel -- \emph{x} \href{https://e.org/a\_b}{y}"),
            'Gödel \u2013 <em>x</em> <a href="https://e.org/a_b">y</a>',
        )

    def test_catalogue_commands_fill_one_line(self) -> None:
        """A command continuing on the next line is rejected."""
        good = "\\ExtendedNote{a}{b}\n"
        check_one_line_commands(good)
        with self.assertRaises(TexError):
            check_one_line_commands("\\ExtendedNote{a}{b\nc}\n")

    def test_spread_keeps_order_spacing_and_bounds(self) -> None:
        """Three targets at 1, two apart: 1, 3, 5 shift back by their mean gap only to lo = 0."""
        self.assertEqual(spread([1.0, 1.0, 1.0], 2.0, 0.0, 10.0), [0.0, 2.0, 4.0])
        self.assertEqual(spread([5.0, 5.0], 2.0, 0.0, 10.0), [4.0, 6.0])
        self.assertEqual(spread([9.0, 9.0], 2.0, 0.0, 10.0), [8.0, 10.0])


if __name__ == "__main__":
    unittest.main()
