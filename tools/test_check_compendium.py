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
    "learning_parts": [
        {"id": "part-one", "title": "Part one", "routes": ["sec-a", "sec-b"]},
        {"id": "part-two", "title": "Part two", "routes": ["sec-c"]},
    ],
    "routes": [{"id": "sec-a"}, {"id": "sec-b"}, {"id": "sec-c"}],
    "specialist_routes": [{"id": "path-x"}, {"id": "path-y"}, {"id": "path-z"}],
    "retired_overviews": [{"id": "old-ab", "successors": ["sec-a", "sec-b"]}],
}
MASTER = "\\qfpart{part-one}{Part one}{sec-a, sec-b}\n\\qfpart{part-two}{Part two}{sec-c}\n"

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
        self.write("notes/pathways/sec-a.md", "")
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
    r"""The master's \qfpart declarations are the only declaration of Parts and sections."""

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

    def test_populated_section_in_a_later_part_passes(self):
        """Populated section in a later part passes."""
        self.repo.write("compendium/sec-c/section.tex", "\\chapter{C}\n\\input{sec-c/topic}\n")
        self.repo.write("compendium/sec-c/topic.tex", GOOD_ENTRY.replace("mod:good", "mod:other"))
        self.repo.write("notes/pathways/sec-c.md", "## Entries\n- `mod:other`\n")
        self.assertEqual(self.problems(), "")

    def test_empty_leading_section_in_a_populated_part_passes(self):
        """Empty leading section in a populated part passes."""
        self.repo.root.joinpath("compendium/sec-a/section.tex").unlink()
        self.repo.write("compendium/sec-b/section.tex", "\\chapter{B}\n\\input{sec-a/topic}\n")
        self.repo.write("notes/pathways/sec-b.md", "")
        self.assertEqual(self.problems(), "")
        parts = self.repo.report()["parts"]
        self.assertEqual(parts[0]["populated"], ["sec-b"])
        self.assertEqual(parts[1]["populated"], [])

    def test_section_outside_the_guide_fails(self):
        """Section outside the guide fails."""
        self.repo.write("compendium/compendium.tex", MASTER.replace("sec-c}", "sec-c, sec-d}"))
        self.assertIn("section `sec-d` is not a section of the pinned guide", self.problems())

    def test_swapped_sections_and_parts_fail(self):
        """Swapped sections and parts fail."""
        self.repo.write(
            "compendium/compendium.tex",
            "\\qfpart{part-one}{Part one}{sec-b, sec-a}\n\\qfpart{part-two}{Part two}{sec-c}\n",
        )
        self.assertIn("Part `part-one` orders its sections", self.problems())
        self.repo.write(
            "compendium/compendium.tex",
            "\\qfpart{part-two}{Part two}{sec-c}\n\\qfpart{part-one}{Part one}{sec-a, sec-b}\n",
        )
        self.assertIn("differ from the guide's", self.problems())

    def test_section_in_the_wrong_part_fails(self):
        """Section in the wrong part fails, although every key is declared."""
        self.repo.write(
            "compendium/compendium.tex",
            "\\qfpart{part-one}{Part one}{sec-a}\n\\qfpart{part-two}{Part two}{sec-b, sec-c}\n",
        )
        self.assertIn(
            "section `sec-b` is declared in Part `part-two`, the guide places it in `part-one`",
            self.problems(),
        )

    def test_missing_section_and_wrong_part_title_fail(self):
        """Missing section and wrong part title fail."""
        self.repo.write(
            "compendium/compendium.tex",
            "\\qfpart{part-one}{Part 1}{sec-a, sec-b}\n\\qfpart{part-two}{Part two}{sec-a}\n",
        )
        problems = self.problems()
        self.assertIn("guide section `sec-c` is not declared", problems)
        self.assertIn("section `sec-a` is declared twice", problems)
        self.assertIn("Part `part-one` is titled 'Part 1'", problems)

    def test_retired_overview_is_a_bridge_not_a_section(self):
        """Retired overview is a bridge not a section."""
        self.repo.write("notes/pathways/old-ab.md", "Now `sec-a` and `sec-b`.\n")
        self.assertEqual(self.problems(), "")
        self.repo.write("notes/pathways/old-ab.md", "Now `sec-a` only.\n")
        self.assertIn("does not name its successor section `sec-b`", self.problems())
        self.repo.write("compendium/compendium.tex", MASTER.replace("sec-c}", "sec-c, old-ab}"))
        self.assertIn("section `old-ab` is a retired guide overview", self.problems())

    def test_populated_section_needs_an_overview_note(self):
        """Populated section needs an overview note."""
        self.repo.root.joinpath("notes/pathways/sec-a.md").unlink()
        self.repo.write("notes/pathways/path-x.md", "## Entries\n- `mod:good`\n")
        self.assertIn("section `sec-a` is populated but has no overview note", self.problems())

    def test_repeated_input_and_cycle_fail(self):
        """Repeated input and cycle fail, which set-based reachability would miss."""
        self.repo.write(
            "compendium/sec-a/section.tex",
            "\\chapter{A}\n\\input{sec-a/topic}\n\\input{sec-a/topic}\n",
        )
        self.assertIn("compendium/sec-a/topic.tex: input 2 times", self.problems())
        self.repo.write("compendium/sec-a/section.tex", "\\chapter{A}\n\\input{sec-a/topic}\n")
        self.repo.write("compendium/sec-a/topic.tex", GOOD_ENTRY + "\\input{sec-a/loop}\n")
        self.repo.write("compendium/sec-a/loop.tex", "\\input{sec-a/topic}\n")
        self.assertIn(
            "input cycle: compendium/sec-a/section.tex -> compendium/sec-a/topic.tex -> "
            "compendium/sec-a/loop.tex -> compendium/sec-a/topic.tex",
            self.problems(),
        )

    def test_aliased_repeated_input_and_cycle_fail(self):
        """Repeated input and cycle through an equivalent path fail."""
        self.repo.write(
            "compendium/sec-a/section.tex",
            "\\chapter{A}\n\\input{sec-a/topic}\n\\input{sec-a/../sec-a/topic}\n",
        )
        self.assertIn("compendium/sec-a/topic.tex: input 2 times", self.problems())
        self.repo.write("compendium/sec-a/section.tex", "\\chapter{A}\n\\input{sec-a/topic}\n")
        self.repo.write("compendium/sec-a/topic.tex", GOOD_ENTRY + "\\input{sec-a/loop}\n")
        self.repo.write("compendium/sec-a/loop.tex", "\\input{sec-a/./../sec-a/topic.tex}\n")
        self.assertIn(
            "input cycle: compendium/sec-a/section.tex -> compendium/sec-a/topic.tex -> "
            "compendium/sec-a/loop.tex -> compendium/sec-a/topic.tex",
            self.problems(),
        )

    def test_aliased_input_is_one_reachable_file(self):
        """An equivalent input path reaches its file once, for reachability and headings."""
        self.repo.write(
            "compendium/sec-a/section.tex",
            "\\chapter{A}\n\\section{Group}\n\\input{sec-a/../sec-a/topic}\n",
        )
        self.repo.write("compendium/sec-a/topic.tex", "\\subsection{T}\n" + GOOD_ENTRY)
        self.assertEqual(self.problems(), "")
        self.repo.write("compendium/sec-a/section.tex", "\\chapter{A}\n\\input{../outside}\n")
        self.assertIn("\\input{../outside} names a file outside compendium/", self.problems())

    def test_unreachable_prose_only_topic_file_fails(self):
        """A topic file with only headings or prose must be input; front matter need not be."""
        self.repo.write("compendium/sec-a/orphan.tex", "\\section{Orphan}\nProse only.\n")
        self.assertIn("sec-a/orphan.tex: is a topic file but is not reachable", self.problems())
        self.repo.root.joinpath("compendium/sec-a/orphan.tex").unlink()
        self.repo.write("compendium/sec-a/blank.tex", "% comment only\n\n")
        self.repo.write("compendium/front/notation.tex", "\\chapter*{Notation}\n")
        self.repo.write("compendium/house.tex", "\\newcommand{\\qfhouse}{}\n")
        self.assertEqual(self.problems(), "")

    def test_skipped_heading_level_fails(self):
        """Skipped heading level fails, reading wrapper headings and inputs in order."""
        self.repo.write(
            "compendium/sec-a/section.tex",
            "\\chapter{A}\n\\section{Group}\n\\input{sec-a/topic}\n",
        )
        self.repo.write("compendium/sec-a/topic.tex", "\\subsection{T}\n" + GOOD_ENTRY)
        self.assertEqual(self.problems(), "")
        self.repo.write("compendium/sec-a/section.tex", "\\chapter{A}\n\\input{sec-a/topic}\n")
        self.assertIn("\\subsection skips a heading level", self.problems())
        self.repo.write("compendium/sec-a/section.tex", "\\input{sec-a/topic}\n")
        self.assertIn("needs exactly one \\chapter heading", self.problems())

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
            "compendium/compendium.tex",
            "\\qfpart{part-one}{Part one}{sec-a, sec-b, sec-a, Bad_Key, path-x}\n"
            "\\qfpart{part-two}{Part two}{sec-c}\n",
        )
        problems = self.problems()
        self.assertIn("section `sec-a` is declared twice", problems)
        self.assertIn("malformed section key 'Bad_Key'", problems)
        self.assertIn("section `path-x` collides with a guide specialist pathway key", problems)

    def test_missing_master_or_declaration_fails_without_fallback(self):
        """Missing master or declaration fails without fallback."""
        for text in (None, "% \\qfpart{part-one}{Part one}{sec-a}\n", "\\qfsections{sec-a}\n"):
            with self.subTest(text=text):
                path = self.repo.root / "compendium/compendium.tex"
                if text is None:
                    path.unlink(missing_ok=True)
                else:
                    path.write_text(text)
                problems = self.problems()
                self.assertTrue(
                    "compendium.tex: missing" in problems or "no \\qfpart declaration" in problems,
                    problems,
                )
                self.assertIn(
                    "folder `sec-a` is not a section declared in compendium.tex", problems
                )


if __name__ == "__main__":
    unittest.main()
