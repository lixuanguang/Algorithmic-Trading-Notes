"""Focused tests for check_compendium.py on small synthetic repositories.

Run: make test (uv run pytest)
"""

# standard library imports
import json
import tempfile
import unittest
from pathlib import Path

# project library imports
import check_compendium as ms

ROUTES = {
    "routes": [{"id": "sec-a"}, {"id": "sec-b"}],
    "specialist_routes": [{"id": "path-x"}, {"id": "path-y"}, {"id": "path-z"}],
}
MASTER = "\\qfsections{sec-a, sec-b, sec-c}\n"

GOOD_ENTRY = r"""\begin{qfmodel}[A model]\label{mod:good}
\qffield{Statement} Claim \citep[p.~3]{cat-key}.
\qffield{Further reading} \citep{src-key}.
\end{qfmodel}
"""


class Repo:
    """A throwaway repository laid out like this one."""

    def __init__(self):
        """Create the repository files."""
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.write("guide/learning_routes.json", json.dumps(ROUTES))
        self.write(
            "guide/institutional_quantitative_finance_reading_list.tex",
            r"\CatalogueEntry{cat-key}{A book}" + "\n",
        )
        self.write(
            "compendium/front/sources.tex",
            r"\qfsource{src-key}{A paper}"
            + "\n"
            + r"\qfsource[https://example.org/x]{linked-key}{A page}"
            + "\n",
        )
        self.write("notes/pathways/.keep", "")
        self.write("compendium/compendium.tex", MASTER)
        self.write("compendium/sec-a/section.tex", "\\chapter{A}\n\\input{sec-a/topic}\n")

    def write(self, rel, text):
        """Write text to a path relative to the repository root."""
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def report(self):
        """Run the checker on the repository."""
        return ms.report(self.root)

    def close(self):
        """Remove the repository."""
        self.tmp.cleanup()


class EntryMetadata(unittest.TestCase):
    """Entry structure, citations, labels and pathway listings."""

    def setUp(self):
        """Create a repository for each test."""
        self.repo = Repo()
        self.addCleanup(self.repo.close)
        self.repo.write(
            "notes/pathways/path-x.md",
            "## Entries created or changed\n- `mod:good`\n"
            "## Entry backlog\n- res:later: a stub \\citep[p.~1]{cat-key}\n",
        )

    def gaps(self, entry):
        """Write one entry and return the reported problems."""
        self.repo.write("compendium/sec-a/topic.tex", entry)
        return self.repo.report()["problems"]

    def test_source_key_with_url_is_known(self):
        """Source key with url is known."""
        entry = GOOD_ENTRY.replace(r"\citep{src-key}", r"\citep{linked-key}")
        self.assertNotEqual(entry, GOOD_ENTRY)
        self.assertFalse(any("linked-key" in p for p in self.gaps(entry)))

    def test_complete_entry_passes(self):
        """Complete entry passes."""
        r = (self.gaps(GOOD_ENTRY), self.repo.report())
        self.assertEqual(r[0], [])
        self.assertEqual(r[1]["pathways"]["path-x"]["entries_listed"], ["mod:good"])
        self.assertEqual(r[1]["pathways"]["path-x"]["backlog_stubs"], 1)

    def test_missing_label_and_wrong_prefix(self):
        """Missing label and wrong prefix."""
        self.assertTrue(
            any(
                "missing label" in p for p in self.gaps(GOOD_ENTRY.replace(r"\label{mod:good}", ""))
            )
        )
        self.assertTrue(
            any(
                "label prefix (expected mod:)" in p
                for p in self.gaps(GOOD_ENTRY.replace("mod:good", "res:good"))
            )
        )

    def test_citation_and_locator(self):
        """Citation and locator."""
        self.assertTrue(
            any(
                "missing locator for cat-key" in p
                for p in self.gaps(GOOD_ENTRY.replace(r"\citep[p.~3]{cat-key}", r"\citep{cat-key}"))
            )
        )
        self.assertTrue(
            any(
                "missing citation" in p
                for p in self.gaps(GOOD_ENTRY.replace(r"\citep[p.~3]{cat-key}", ""))
            )
        )
        self.assertTrue(
            any(
                "unknown citation key nobody" in p
                for p in self.gaps(GOOD_ENTRY.replace("{cat-key}", "{nobody}"))
            )
        )

    def test_bare_citation_allowed_in_further_reading_only(self):
        """Bare citation allowed in further reading only."""
        self.assertFalse(any("locator for src-key" in p for p in self.gaps(GOOD_ENTRY)))

    def test_editorial_metadata_is_optional(self):
        """Editorial metadata is optional."""
        self.assertEqual(self.gaps(GOOD_ENTRY), [])

    def test_unlisted_entry_and_dangling_listing(self):
        """Unlisted entry and dangling listing."""
        self.repo.write("notes/pathways/path-x.md", "## Entries\n- `res:nowhere`\n")
        problems = "\n".join(self.gaps(GOOD_ENTRY))
        self.assertIn("entry `mod:good` is listed in no pathway note", problems)
        self.assertIn("lists `res:nowhere`, which no compendium label defines", problems)

    def test_duplicate_labels(self):
        """Duplicate labels."""
        self.repo.write("compendium/sec-b/other.tex", GOOD_ENTRY)
        self.repo.write("compendium/sec-b/section.tex", "\\chapter{B}\n\\input{sec-b/other}\n")
        self.assertTrue(any("label `mod:good` defined 2 times" in p for p in self.gaps(GOOD_ENTRY)))

    def test_folder_must_be_a_section_key(self):
        """Folder must be a section key."""
        self.repo.write("compendium/not-a-section/x.tex", GOOD_ENTRY)
        self.assertTrue(
            any(
                "`not-a-section` is not a section declared in compendium.tex" in p
                for p in self.repo.report()["problems"]
            )
        )


class SectionDeclaration(unittest.TestCase):
    r"""The master's ordered \qfsections list is the only declaration of compendium sections."""

    def setUp(self):
        """Create a repository for each test."""
        self.repo = Repo()
        self.addCleanup(self.repo.close)
        self.repo.write("compendium/sec-a/topic.tex", GOOD_ENTRY)
        self.repo.write("notes/pathways/sec-a.md", "## Entries\n- `mod:good`\n")

    def problems(self):
        """Return the reported problems as one string."""
        return "\n".join(self.repo.report()["problems"])

    def test_declared_sections_and_reachable_entries_pass(self):
        """Declared sections and reachable entries pass."""
        self.assertEqual(self.problems(), "")

    def test_section_outside_the_guide_is_ordinary_when_declared(self):
        """Section outside the guide is ordinary when declared."""
        self.repo.write("compendium/sec-c/section.tex", "\\chapter{C}\n\\input{sec-c/topic}\n")
        self.repo.write("compendium/sec-c/topic.tex", GOOD_ENTRY.replace("mod:good", "mod:other"))
        self.repo.write("notes/pathways/sec-c.md", "## Entries\n- `mod:other`\n")
        self.assertEqual(self.problems(), "")

    def test_planned_section_needs_no_empty_chapter(self):
        """Planned section needs no empty chapter."""
        self.assertFalse((self.repo.root / "compendium/sec-c").exists())
        self.assertEqual(self.problems(), "")

    def test_undeclared_content_folder_and_overview_note_fail(self):
        """Undeclared content folder and overview note fail."""
        self.repo.write("compendium/sec-d/section.tex", "\\chapter{D}\n")
        self.repo.write("notes/pathways/sec-d.md", "")
        problems = self.problems()
        self.assertIn("folder `sec-d` is not a section declared in compendium.tex", problems)
        self.assertIn("`sec-d` is not a declared section or guide pathway key", problems)

    def test_unreachable_typed_entry_fails(self):
        """Unreachable typed entry fails."""
        self.repo.write("compendium/sec-a/section.tex", "\\chapter{A}\n% \\input{sec-a/topic}\n")
        self.assertIn("sec-a/topic.tex: has typed entries but is not reachable", self.problems())

    def test_wrapper_input_of_a_missing_file_fails(self):
        """Wrapper input of a missing file fails."""
        self.repo.write(
            "compendium/sec-a/section.tex",
            "\\chapter{A}\n\\input{sec-a/topic}\n\\input{sec-a/gone}\n",
        )
        self.assertIn("\\input{sec-a/gone} names no file", self.problems())

    def test_duplicate_malformed_and_colliding_keys_fail(self):
        """Duplicate malformed and colliding keys fail."""
        self.repo.write(
            "compendium/compendium.tex", "\\qfsections{sec-a, sec-b, sec-a, Bad_Key, path-x}\n"
        )
        problems = self.problems()
        self.assertIn("section `sec-a` is declared twice", problems)
        self.assertIn("malformed section key 'Bad_Key'", problems)
        self.assertIn("section `path-x` collides with a guide specialist pathway key", problems)

    def test_missing_master_or_declaration_fails_without_fallback(self):
        """Missing master or declaration fails without fallback."""
        for text in (None, "% \\qfsections{sec-a}\n", "\\qfsections{sec-a}\n\\qfsections{sec-b}\n"):
            with self.subTest(text=text):
                path = self.repo.root / "compendium/compendium.tex"
                if text is None:
                    path.unlink(missing_ok=True)
                else:
                    path.write_text(text)
                problems = self.problems()
                self.assertTrue(
                    "compendium.tex: missing" in problems
                    or "expected exactly one \\qfsections declaration" in problems,
                    problems,
                )
                self.assertIn(
                    "folder `sec-a` is not a section declared in compendium.tex", problems
                )


if __name__ == "__main__":
    unittest.main()
