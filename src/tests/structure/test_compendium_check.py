"""Focused tests for the compendium check on small synthetic repositories."""

import unittest

from trading_notes.structure.compendium import RepositoryInputError
from trading_notes.structure.compendium_check import CompendiumReport, build_report
from trading_notes.structure.json_fields import JsonObject

from .repository import (
    A_WRAPPER,
    GOOD_ENTRY,
    MASTER,
    ROUTES,
    Pathway,
    SyntheticRepository,
    wrapper,
)


class EntryMetadata(unittest.TestCase):
    """Entry structure, citations, labels and pathway listings."""

    def setUp(self) -> None:
        """Create a repository for each test."""
        self.repo = SyntheticRepository()
        self.addCleanup(self.repo.close)
        self.repo.write(
            "notes/pathways/path-x.md",
            "## Entries created or changed\n- `mod:good`\n"
            "## Entry backlog\n- res:later: a stub \\citep[p.~1]{cat-key}\n",
        )

    def gaps(self, entry: str) -> list[str]:
        """Write one entry and return the reported problems."""
        self.repo.write("compendium/sec-a/topic.tex", entry)
        return build_report(self.repo.root)["problems"]

    def test_source_key_with_url_is_known(self) -> None:
        """Source key with url is known."""
        entry = GOOD_ENTRY.replace(r"\citep{src-key}", r"\citep{linked-key}")
        self.assertNotEqual(entry, GOOD_ENTRY)
        self.assertFalse(any("linked-key" in p for p in self.gaps(entry)))

    def test_complete_entry_passes(self) -> None:
        """Complete entry passes."""
        r = (self.gaps(GOOD_ENTRY), build_report(self.repo.root))
        self.assertEqual(r[0], [])
        self.assertEqual(r[1]["pathways"]["path-x"]["entries_listed"], ["mod:good"])
        self.assertEqual(r[1]["pathways"]["path-x"]["backlog_stubs"], 1)

    def test_missing_label_and_wrong_prefix(self) -> None:
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

    def test_citation_and_locator(self) -> None:
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

    def test_bare_citation_allowed_in_further_reading_only(self) -> None:
        """Bare citation allowed in further reading only."""
        self.assertFalse(any("locator for src-key" in p for p in self.gaps(GOOD_ENTRY)))

    def test_editorial_metadata_is_optional(self) -> None:
        """Editorial metadata is optional."""
        self.assertEqual(self.gaps(GOOD_ENTRY), [])

    def test_unlisted_entry_and_dangling_listing(self) -> None:
        """Unlisted entry and dangling listing."""
        self.repo.write("notes/pathways/path-x.md", "## Entries\n- `res:nowhere`\n")
        problems = "\n".join(self.gaps(GOOD_ENTRY))
        self.assertIn("entry `mod:good` is listed in no pathway note", problems)
        self.assertIn("lists `res:nowhere`, which no compendium label defines", problems)

    def test_duplicate_labels(self) -> None:
        """Duplicate labels."""
        self.repo.write("compendium/sec-b/other.tex", GOOD_ENTRY)
        self.repo.write(
            "compendium/sec-b/section.tex",
            wrapper("Section B", ("path-z", "Path Z", ["sec-b/other"])),
        )
        self.assertTrue(any("label `mod:good` defined 2 times" in p for p in self.gaps(GOOD_ENTRY)))

    def test_folder_must_be_a_section_key(self) -> None:
        """Folder must be a section key."""
        self.repo.write("compendium/not-a-section/x.tex", GOOD_ENTRY)
        self.assertTrue(
            any(
                "`not-a-section` is not a section declared in compendium.tex" in p
                for p in build_report(self.repo.root)["problems"]
            )
        )


class SectionDeclaration(unittest.TestCase):
    r"""The master's \qfpart declarations are the only declaration of Parts and sections."""

    def setUp(self) -> None:
        """Create a repository for each test."""
        self.repo = SyntheticRepository()
        self.addCleanup(self.repo.close)
        self.repo.write("compendium/sec-a/topic.tex", GOOD_ENTRY)
        self.repo.write("notes/pathways/sec-a.md", "## Entries\n- `mod:good`\n")

    def problems(self) -> str:
        """Return the reported problems as one string."""
        return "\n".join(build_report(self.repo.root)["problems"])

    def test_declared_sections_and_reachable_entries_pass(self) -> None:
        """Declared sections and reachable entries pass."""
        self.assertEqual(self.problems(), "")

    def test_populated_section_in_a_later_part_passes(self) -> None:
        """Populated section in a later part passes."""
        self.repo.write(
            "compendium/sec-c/section.tex",
            wrapper("Section C", ("path-w", "Path W", ["sec-c/topic"])),
        )
        self.repo.write("compendium/sec-c/topic.tex", GOOD_ENTRY.replace("mod:good", "mod:other"))
        self.repo.write("notes/pathways/sec-c.md", "## Entries\n- `mod:other`\n")
        self.assertEqual(self.problems(), "")

    def test_empty_leading_section_in_a_populated_part_passes(self) -> None:
        """Empty leading section in a populated part passes."""
        self.repo.root.joinpath("compendium/sec-a/section.tex").unlink()
        self.repo.write(
            "compendium/sec-b/section.tex",
            wrapper("Section B", ("path-z", "Path Z", ["sec-a/topic"])),
        )
        self.repo.write("notes/pathways/sec-b.md", "")
        self.assertEqual(self.problems(), "")
        parts = build_report(self.repo.root)["parts"]
        self.assertEqual(parts[0]["populated"], ["sec-b"])
        self.assertEqual(parts[1]["populated"], [])

    def test_section_outside_the_guide_fails(self) -> None:
        """Section outside the guide fails."""
        self.repo.write("compendium/compendium.tex", MASTER.replace("sec-c}", "sec-c, sec-d}"))
        self.assertIn("section `sec-d` is not a section of the pinned guide", self.problems())

    def test_swapped_sections_and_parts_fail(self) -> None:
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

    def test_section_in_the_wrong_part_fails(self) -> None:
        """Section in the wrong part fails, although every key is declared."""
        self.repo.write(
            "compendium/compendium.tex",
            "\\qfpart{part-one}{Part one}{sec-a}\n\\qfpart{part-two}{Part two}{sec-b, sec-c}\n",
        )
        self.assertIn(
            "section `sec-b` is declared in Part `part-two`, the guide places it in `part-one`",
            self.problems(),
        )

    def test_missing_section_and_wrong_part_title_fail(self) -> None:
        """Missing section and wrong part title fail."""
        self.repo.write(
            "compendium/compendium.tex",
            "\\qfpart{part-one}{Part 1}{sec-a, sec-b}\n\\qfpart{part-two}{Part two}{sec-a}\n",
        )
        problems = self.problems()
        self.assertIn("guide section `sec-c` is not declared", problems)
        self.assertIn("section `sec-a` is declared twice", problems)
        self.assertIn("Part `part-one` is titled 'Part 1'", problems)

    def test_retired_overview_is_a_bridge_not_a_section(self) -> None:
        """Retired overview is a bridge not a section."""
        self.repo.write("notes/pathways/old-ab.md", "Now `sec-a` and `sec-b`.\n")
        self.assertEqual(self.problems(), "")
        self.repo.write("notes/pathways/old-ab.md", "Now `sec-a` only.\n")
        self.assertIn("does not name its successor section `sec-b`", self.problems())
        self.repo.write("compendium/compendium.tex", MASTER.replace("sec-c}", "sec-c, old-ab}"))
        self.assertIn("section `old-ab` is a retired guide overview", self.problems())

    def test_populated_section_needs_an_overview_note(self) -> None:
        """Populated section needs an overview note."""
        self.repo.root.joinpath("notes/pathways/sec-a.md").unlink()
        self.repo.write("notes/pathways/path-x.md", "## Entries\n- `mod:good`\n")
        self.assertIn("section `sec-a` is populated but has no overview note", self.problems())

    def test_repeated_input_and_cycle_fail(self) -> None:
        """Repeated input and cycle fail, which set-based reachability would miss."""
        self.repo.write(
            "compendium/sec-a/section.tex",
            wrapper("Section A", ("path-x", "Path X", ["sec-a/topic", "sec-a/topic"])),
        )
        self.assertIn("compendium/sec-a/topic.tex: input 2 times", self.problems())
        self.repo.write("compendium/sec-a/section.tex", A_WRAPPER)
        self.repo.write("compendium/sec-a/topic.tex", GOOD_ENTRY + "\\input{sec-a/loop}\n")
        self.repo.write("compendium/sec-a/loop.tex", "\\input{sec-a/topic}\n")
        self.assertIn(
            "input cycle: compendium/sec-a/section.tex -> compendium/sec-a/topic.tex -> "
            "compendium/sec-a/loop.tex -> compendium/sec-a/topic.tex",
            self.problems(),
        )

    def test_aliased_repeated_input_and_cycle_fail(self) -> None:
        """Repeated input and cycle through an equivalent path fail."""
        self.repo.write(
            "compendium/sec-a/section.tex",
            wrapper("Section A", ("path-x", "Path X", ["sec-a/topic", "sec-a/../sec-a/topic"])),
        )
        self.assertIn("compendium/sec-a/topic.tex: input 2 times", self.problems())
        self.repo.write("compendium/sec-a/section.tex", A_WRAPPER)
        self.repo.write("compendium/sec-a/topic.tex", GOOD_ENTRY + "\\input{sec-a/loop}\n")
        self.repo.write("compendium/sec-a/loop.tex", "\\input{sec-a/./../sec-a/topic.tex}\n")
        self.assertIn(
            "input cycle: compendium/sec-a/section.tex -> compendium/sec-a/topic.tex -> "
            "compendium/sec-a/loop.tex -> compendium/sec-a/topic.tex",
            self.problems(),
        )

    def test_aliased_input_is_one_reachable_file(self) -> None:
        """An equivalent input path reaches its file once, for reachability and headings."""
        self.repo.write(
            "compendium/sec-a/section.tex",
            wrapper("Section A", ("path-x", "Path X", ["sec-a/../sec-a/topic"])),
        )
        self.repo.write("compendium/sec-a/topic.tex", "\\subsection{T}\n" + GOOD_ENTRY)
        self.assertEqual(self.problems(), "")
        self.repo.write(
            "compendium/sec-a/section.tex",
            wrapper("Section A", ("path-x", "Path X", ["../outside"])),
        )
        self.assertIn("\\input{../outside} names a file outside compendium/", self.problems())

    def test_unreachable_prose_only_topic_file_fails(self) -> None:
        """A topic file with only headings or prose must be input; front matter need not be."""
        self.repo.write("compendium/sec-a/orphan.tex", "\\subsection{Orphan}\nProse only.\n")
        self.assertIn("sec-a/orphan.tex: is a topic file but is not reachable", self.problems())
        self.repo.root.joinpath("compendium/sec-a/orphan.tex").unlink()
        self.repo.write("compendium/sec-a/blank.tex", "% comment only\n\n")
        self.repo.write("compendium/front/notation.tex", "\\chapter*{Notation}\n")
        self.repo.write("compendium/house.tex", "\\newcommand{\\qfhouse}{}\n")
        self.assertEqual(self.problems(), "")

    def test_skipped_heading_level_fails(self) -> None:
        """Skipped heading level fails, reading wrapper headings and inputs in order."""
        self.repo.write("compendium/sec-a/topic.tex", "\\subsection{T}\n" + GOOD_ENTRY)
        self.assertEqual(self.problems(), "")
        self.repo.write("compendium/sec-a/topic.tex", "\\subsubsection{T}\n" + GOOD_ENTRY)
        self.assertIn("\\subsubsection skips a heading level", self.problems())
        self.repo.write("compendium/sec-a/section.tex", "\\input{sec-a/topic}\n")
        self.assertIn("needs exactly one \\chapter heading", self.problems())

    def test_planned_section_needs_no_empty_chapter(self) -> None:
        """Planned section needs no empty chapter."""
        self.assertFalse((self.repo.root / "compendium/sec-c").exists())
        self.assertEqual(self.problems(), "")

    def test_undeclared_content_folder_and_overview_note_fail(self) -> None:
        """Undeclared content folder and overview note fail."""
        self.repo.write("compendium/sec-d/section.tex", "\\chapter{Section D}\n")
        self.repo.write("notes/pathways/sec-d.md", "")
        problems = self.problems()
        self.assertIn("folder `sec-d` is not a section declared in compendium.tex", problems)
        self.assertIn("`sec-d` is not a declared section or guide pathway key", problems)

    def test_unreachable_typed_entry_fails(self) -> None:
        """Unreachable typed entry fails."""
        self.repo.write(
            "compendium/sec-a/section.tex", "\\chapter{Section A}\n% \\input{sec-a/topic}\n"
        )
        self.assertIn("sec-a/topic.tex: has typed entries but is not reachable", self.problems())

    def test_wrapper_input_of_a_missing_file_fails(self) -> None:
        """Wrapper input of a missing file fails."""
        self.repo.write(
            "compendium/sec-a/section.tex",
            wrapper("Section A", ("path-x", "Path X", ["sec-a/topic", "sec-a/gone"])),
        )
        self.assertIn("\\input{sec-a/gone} names no file", self.problems())

    def test_duplicate_malformed_and_colliding_keys_fail(self) -> None:
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

    def test_missing_master_or_declaration_fails_without_fallback(self) -> None:
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


class PathwayHierarchy(unittest.TestCase):
    r"""Chapter titles and \qfpathway headings follow the guide's sections and pathways."""

    def setUp(self) -> None:
        """Create a repository with two topic files in section A."""
        self.repo = SyntheticRepository()
        self.addCleanup(self.repo.close)
        self.repo.write("compendium/sec-a/topic.tex", GOOD_ENTRY)
        self.repo.write("compendium/sec-a/more.tex", GOOD_ENTRY.replace("mod:good", "mod:more"))
        self.repo.write("notes/pathways/sec-a.md", "## Entries\n- `mod:good`\n- `mod:more`\n")

    def check(self, *pathways: Pathway, title: str = "Section A") -> CompendiumReport:
        """Write section A's wrapper and return the report."""
        self.repo.write("compendium/sec-a/section.tex", wrapper(title, *pathways))
        return build_report(self.repo.root)

    def problems(self, *pathways: Pathway, title: str = "Section A") -> str:
        """Return the problems for a wrapper as one string."""
        return "\n".join(self.check(*pathways, title=title)["problems"])

    def test_guide_pathways_in_order_pass(self) -> None:
        """Guide pathways in guide order, with their names and entries, pass."""
        r = self.check(("path-x", "Path X", ["sec-a/topic"]), ("path-y", "Path Y", ["sec-a/more"]))
        self.assertEqual(r["problems"], [])
        self.assertEqual(r["pathways_rendered"], {"sec-a": ["path-x", "path-y"]})

    def test_unwritten_pathway_is_omitted(self) -> None:
        """A pathway without local material is omitted; a later one may print alone."""
        r = self.check(("path-y", "Path Y", ["sec-a/topic", "sec-a/more"]))
        self.assertEqual(r["problems"], [])
        self.assertEqual(r["pathways_rendered"], {"sec-a": ["path-y"]})

    def test_wrong_relative_order_fails(self) -> None:
        """Pathways out of the guide's relative order fail."""
        self.assertIn(
            "pathways ['path-y', 'path-x'] are not in the guide's order",
            self.problems(
                ("path-y", "Path Y", ["sec-a/topic"]), ("path-x", "Path X", ["sec-a/more"])
            ),
        )

    def test_displayed_title_must_be_the_guide_name(self) -> None:
        """A pathway or chapter titled otherwise than in the guide fails."""
        problems = self.problems(
            ("path-x", "Path Ex", ["sec-a/topic", "sec-a/more"]), title="Section 1"
        )
        self.assertIn("pathway `path-x` is titled 'Path Ex', the guide 'Path X'", problems)
        self.assertIn("chapter is titled 'Section 1', the guide 'Section A'", problems)

    def test_pathway_of_another_section_or_unknown_fails(self) -> None:
        """A pathway must belong to the chapter's own section and exist in the guide."""
        problems = self.problems(
            ("path-z", "Path Z", ["sec-a/topic"]), ("path-q", "Path Q", ["sec-a/more"])
        )
        self.assertIn("pathway `path-z` belongs to section `sec-b`, not `sec-a`", problems)
        self.assertIn("`path-q` is not a guide specialist pathway", problems)

    def test_repeated_and_empty_pathways_fail(self) -> None:
        """A pathway opened twice, or with no typed entry, fails."""
        self.repo.write("compendium/sec-a/prose.tex", "\\subsection{Prose}\nProse only.\n")
        problems = self.problems(
            ("path-x", "Path X", ["sec-a/topic"]),
            ("path-y", "Path Y", ["sec-a/prose"]),
            ("path-x", "Path X", ["sec-a/more"]),
        )
        self.assertIn("pathway `path-x` is opened twice", problems)
        self.assertIn("pathway `path-y` has no typed entry", problems)

    def test_material_outside_a_pathway_fails(self) -> None:
        r"""An \input before the first pathway, or a bare \section group, fails."""
        self.repo.write(
            "compendium/sec-a/section.tex",
            "\\chapter{Section A}\n\\input{sec-a/topic}\n\\section{Group}\n\\input{sec-a/more}\n",
        )
        problems = "\n".join(build_report(self.repo.root)["problems"])
        self.assertIn("\\input{sec-a/topic} sits outside any numbered pathway", problems)
        self.assertIn("\\section is not a guide pathway heading; use \\qfpathway", problems)

    def test_pathway_or_section_heading_in_a_topic_file_fails(self) -> None:
        r"""Topic files hold \subsection and lower; pathways open only in the wrapper."""
        self.repo.write(
            "compendium/sec-a/more.tex",
            "\\section{T}\n" + GOOD_ENTRY.replace("mod:good", "mod:more"),
        )
        problems = self.problems(("path-x", "Path X", ["sec-a/topic", "sec-a/more"]))
        self.assertIn("sec-a/more.tex:1: \\section in a topic file", problems)
        self.repo.write(
            "compendium/sec-a/more.tex",
            "\\qfpathway{path-y}{Path Y}\n" + GOOD_ENTRY.replace("mod:good", "mod:more"),
        )
        problems = self.problems(("path-x", "Path X", ["sec-a/topic", "sec-a/more"]))
        self.assertIn("sec-a/more.tex:1: \\qfpathway in a topic file", problems)


class NumberedPathwaysOnly(unittest.TestCase):
    r"""Every typed entry sits under a numbered \qfpathway; no other peer heading exists."""

    def setUp(self) -> None:
        """Create a repository with two topic files in section A."""
        self.repo = SyntheticRepository()
        self.addCleanup(self.repo.close)
        self.repo.write(
            "compendium/sec-a/basics.tex",
            "\\subsection{Basics}\n" + GOOD_ENTRY.replace("mod:good", "mod:basic"),
        )
        self.repo.write("compendium/sec-a/topic.tex", "\\subsection{Topic}\n" + GOOD_ENTRY)
        self.repo.write("notes/pathways/sec-a.md", "## Entries\n- `mod:good`\n- `mod:basic`\n")
        self.pathway = "\\qfpathway{path-x}{Path X}\n\\input{sec-a/basics}\n\\input{sec-a/topic}\n"

    def problems(self, text: str) -> str:
        """Write section A's wrapper and return the problems as one string."""
        self.repo.write("compendium/sec-a/section.tex", text)
        return "\n".join(build_report(self.repo.root)["problems"])

    def test_brief_wrapper_introduction_passes(self) -> None:
        """A chapter may open with prose in its wrapper before the first pathway."""
        text = "\\chapter{Section A}\nA short orientation.\n\n" + self.pathway
        self.assertEqual(self.problems(text), "")

    def test_entries_outside_a_numbered_pathway_fail(self) -> None:
        """A topic file input before the first pathway is reported."""
        text = "\\chapter{Section A}\n\\input{sec-a/basics}\n" + self.pathway.replace(
            "\\input{sec-a/basics}\n", ""
        )
        self.assertIn(
            "\\input{sec-a/basics} sits outside any numbered pathway", self.problems(text)
        )

    def test_unnumbered_or_peer_headings_fail(self) -> None:
        """Overview commands and starred sections are not pathway headings, anywhere."""
        problems = self.problems("\\chapter{Section A}\n\\qfoverview\n" + self.pathway)
        self.assertIn("\\qfoverview is not a guide pathway heading", problems)
        problems = self.problems("\\chapter{Section A}\n\\section*{Basics}\n" + self.pathway)
        self.assertIn("\\section* is not a guide pathway heading", problems)
        self.repo.write(
            "compendium/sec-a/basics.tex",
            "\\qfoverviewtopic{Basics}\n" + GOOD_ENTRY.replace("mod:good", "mod:basic"),
        )
        problems = self.problems("\\chapter{Section A}\n" + self.pathway)
        self.assertIn("sec-a/basics.tex:1: \\qfoverviewtopic in a topic file", problems)


class PinnedGuideInputs(unittest.TestCase):
    """A missing or malformed pinned guide stops the run with a named error."""

    def setUp(self) -> None:
        """Create a repository for each test."""
        self.repo = SyntheticRepository()
        self.addCleanup(self.repo.close)

    def error(self) -> str:
        """Run the check, expecting an input error, and return its message."""
        with self.assertRaises(RepositoryInputError) as caught:
            build_report(self.repo.root)
        return str(caught.exception)

    def test_malformed_guide_fields_are_named(self) -> None:
        """Each ill-typed required field is named, not raised as a KeyError or TypeError."""
        routes: JsonObject = {
            **ROUTES,
            "learning_parts": None,
            "routes": [{"id": "sec-a", "name": "Section A", "specialist_order": "path-x"}],
            "specialist_routes": [{"name": "Path X"}],
        }
        self.repo.write_json("guide/learning_routes.json", routes)
        error = self.error()
        self.assertIn(
            "guide/learning_routes.json: `learning_parts` must be a list of objects", error
        )
        self.assertIn("`routes[0]` field `specialist_order` must be a list of strings", error)
        self.assertIn("`specialist_routes[0]` field `id` must be a string", error)

    def test_missing_or_invalid_guide_files_are_named(self) -> None:
        """An unreadable guide or catalogue is named."""
        self.repo.write("guide/learning_routes.json", "{")
        self.assertIn("guide/learning_routes.json: cannot be read as JSON", self.error())
        self.repo.write_json("guide/learning_routes.json", ROUTES)
        (self.repo.root / "guide/institutional_quantitative_finance_reading_list.tex").unlink()
        self.assertIn(
            "institutional_quantitative_finance_reading_list.tex: cannot be read", self.error()
        )


class SuccessiveRuns(unittest.TestCase):
    """Each run reads its own repository afresh; nothing is cached between runs."""

    def test_alternating_and_edited_repositories(self) -> None:
        """Runs on two repositories, and after an edit, each see the current files."""
        good, other = SyntheticRepository(), SyntheticRepository()
        for repo in (good, other):
            self.addCleanup(repo.close)
            repo.write("notes/pathways/sec-a.md", "## Entries\n- `mod:good`\n")
        good.write("compendium/sec-a/topic.tex", GOOD_ENTRY)
        other.write("compendium/sec-a/topic.tex", GOOD_ENTRY.replace("[p.~3]", ""))
        first = build_report(good.root)
        self.assertEqual(first["problems"], [])
        self.assertIn(
            "missing locator for cat-key", "\n".join(build_report(other.root)["problems"])
        )
        self.assertEqual(build_report(good.root), first)
        good.write("compendium/sec-a/section.tex", A_WRAPPER.replace("Section A", "Section 1"))
        self.assertIn(
            "chapter is titled 'Section 1'", "\n".join(build_report(good.root)["problems"])
        )


if __name__ == "__main__":
    unittest.main()
