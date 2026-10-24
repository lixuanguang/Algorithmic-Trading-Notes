"""Focused tests for the coverage check on small synthetic repositories.

Run: make test (uv run --frozen --no-editable pytest)
"""

import hashlib
import unittest
from collections.abc import Callable

from trading_notes.structure.coverage_check import CoverageReport, build_report
from trading_notes.structure.json_fields import JsonObject

from .repository import GOOD_ENTRY, SyntheticRepository

HASH_A = hashlib.sha256(b"outline A").hexdigest()
HASH_B = hashlib.sha256(b"outline B").hexdigest()
OUT_A, OUT_B = f"outline:{HASH_A[:12]}", f"outline:{HASH_B[:12]}"
COMPARE = "objective:compare-weighted-returns"


def topics() -> list[JsonObject]:
    """Return the fixture's one topic record."""
    return [
        {
            "id": "topic:return-measurement",
            "title": "Returns",
            "section": "sec-a",
            "prerequisites": [],
        }
    ]


def objectives() -> list[JsonObject]:
    """Return the fixture's objective records: one covered, one missing."""
    return [
        {
            "id": COMPARE,
            "topic": "topic:return-measurement",
            "title": "Compare",
            "operations": ["calculate", "compare"],
            "prerequisites": [],
            "entries": ["mod:good"],
            "candidate_entries": [],
            "coverage": "covered",
            "next_action": None,
            "missing": None,
            "supersedes": None,
            "evidence": {
                "sources": [{"key": "src-key", "locator": "p. 3"}],
                "review_record": "notes/records.md",
                "reading_notes": [],
                "entry_evidence": ["mod:good"],
            },
        },
        # No outline association and no provider, year or level fields.
        {
            "id": "objective:interpret-real-returns",
            "topic": "topic:return-measurement",
            "title": "Real returns",
            "operations": ["interpret"],
            "prerequisites": [],
            "entries": [],
            "candidate_entries": [],
            "coverage": "missing",
            "next_action": "write",
            "missing": "All operations.",
            "supersedes": None,
            "evidence": None,
        },
    ]


def outline(oid: str, digest: str, n_modules: int, n_items: int) -> JsonObject:
    """Return one manifest outline; the counts are the source file's own."""
    return {
        "id": oid,
        "sha256": digest,
        "local_path": f"reading_materials/outlines/outline-{digest[:12]}.pdf",
        "role": "scope-reference",
        "modules": n_modules,
        "bullets": n_items,
        "provenance": {"original_filename": "cfa-level-one-outline.pdf"},
    }


def module(
    oid: str, n: int, bullets: int, occurrences: list[JsonObject] | None = None
) -> JsonObject:
    """Return one crosswalk module record."""
    return {
        "id": f"{oid}:m{n:03d}",
        "outline": oid,
        "ordinal": n,
        "heading": f"Module {n}",
        "component": "shared core" if occurrences else "level",
        "bullets": bullets,
        "occurrences": occurrences or [{"outline": oid, "module": n}],
    }


def item(
    oid: str,
    n: int,
    b: int,
    objective_ids: list[str],
    occurrences: list[str] | None = None,
    gap: str | None = None,
    reviewed: str | None = "2026-10-18",
) -> JsonObject:
    """Return one crosswalk item record, reviewed by default."""
    mid = f"{oid}:m{n:03d}"
    return {
        "id": f"{mid}:b{b:02d}",
        "module": mid,
        "ordinal": b,
        "paraphrase": "p",
        "command_verbs": ["calculate"],
        "objectives": objective_ids,
        "rationale": "r",
        "residual_gap": gap,
        "reviewed": reviewed,
        "occurrences": occurrences or [f"{mid}:b{b:02d}"],
    }


def evidence(objective: JsonObject) -> JsonObject:
    """Return an objective's evidence object, for changes in place."""
    value = objective["evidence"]
    assert isinstance(value, dict)
    return value


class CoverageFixture:
    """Coverage records written into a synthetic repository before each run.

    The repository holds one valid entry, `mod:good`, with its entry evidence and review
    record. Tests change the record lists in place; `report` writes them as the three
    coverage files, with the crosswalk scope counted from the lists unless `scope` is set.
    """

    def __init__(self, repo: SyntheticRepository) -> None:
        """Add the entry, its evidence and the default coverage records to repo."""
        self.repo = repo
        repo.write("compendium/sec-a/topic.tex", GOOD_ENTRY)
        repo.write("notes/pathways/path-x.md", "## Entries\n- `mod:good`\n")
        repo.write_json(
            "notes/entry-evidence.json",
            {
                "mod:good": {
                    "source": "compendium/sec-a/topic.tex",
                    "review": "Checked against p. 3.",
                }
            },
        )
        repo.write("notes/records.md", "# Records\n")
        self.topics = topics()
        self.objectives = objectives()
        self.outlines = [outline(OUT_A, HASH_A, 1, 2)]
        self.modules = [module(OUT_A, 1, 2)]
        self.items = [item(OUT_A, 1, 1, [COMPARE]), item(OUT_A, 1, 2, [COMPARE])]
        self.scope: JsonObject | None = None

    def report(self, verify: bool = False) -> CoverageReport:
        """Write the coverage files and run the checker on the repository."""
        scope = self.scope or {"modules": len(self.modules), "bullets": len(self.items)}
        for name, document in (
            ("objectives.json", {"topics": self.topics, "objectives": self.objectives}),
            ("outline-manifest.json", {"outlines": self.outlines}),
            (
                "outline-crosswalk.json",
                {"scope": scope, "modules": self.modules, "items": self.items},
            ),
        ):
            self.repo.write_json(f"notes/coverage/{name}", {"schema_version": 1, **document})
        return build_report(self.repo.root, verify=verify)

    def problems(self, verify: bool = False) -> str:
        """Return the reported problems as one string."""
        return "\n".join(self.report(verify)["problems"])


class CoverageContract(unittest.TestCase):
    """Structural contract of the coverage records and the outline crosswalk."""

    def setUp(self) -> None:
        """Create a repository for each test."""
        repo = SyntheticRepository()
        self.addCleanup(repo.close)
        self.fx = CoverageFixture(repo)

    def obj(self, n: int = 0) -> JsonObject:
        """Return the n-th objective record."""
        return self.fx.objectives[n]

    def test_valid_records_pass_and_many_items_map_to_one_objective(self) -> None:
        """Valid records pass and many items map to one objective."""
        r = self.fx.report()
        self.assertEqual(r["problems"], [])
        self.assertEqual(r["objectives"], {"covered": 1, "missing": 1})
        self.assertEqual(r["outline_items"], 2)
        self.assertEqual(r["outline_items_by_component"], {"level": {"covered": 2}})

    def test_unknown_label_source_reference_and_duplicate_id_fail(self) -> None:
        """Unknown label source reference and duplicate id fail."""
        self.obj()["entries"] = ["mod:absent"]
        self.fx.items[0]["objectives"] = ["objective:nowhere"]
        self.fx.modules[0]["occurrences"] = [{"outline": "outline:0123456789ab", "module": 1}]
        self.fx.objectives.append(objectives()[1])
        problems = self.fx.problems()
        self.assertIn("names `mod:absent`, which is not a typed compendium entry", problems)
        self.assertIn("maps to unknown `objective:nowhere`", problems)
        self.assertIn("occurrence in unknown `outline:0123456789ab`", problems)
        self.assertIn("duplicate id `objective:interpret-real-returns`", problems)

    def test_invalid_status_and_unsupported_owner_fail(self) -> None:
        """Invalid status and unsupported owner fail."""
        self.obj(1)["coverage"] = "done"
        self.obj(1)["next_action"] = "someday"
        self.fx.topics[0]["section"] = "not-a-section"
        problems = self.fx.problems()
        self.assertIn("invalid coverage 'done'", problems)
        self.assertIn("invalid next action 'someday'", problems)
        self.assertIn("owned by `not-a-section`", problems)

    def test_covered_without_entry_source_or_review_fails(self) -> None:
        """Covered without entry source or review fails."""
        self.obj()["entries"] = []
        self.obj()["evidence"] = {"sources": [], "review_record": "notes/missing.md"}
        problems = self.fx.problems()
        self.assertIn("is covered but maps no entry", problems)
        self.assertIn("is covered without a substantive source", problems)
        self.assertIn("is covered without an existing review record", problems)

    def test_covered_entry_needs_entry_evidence(self) -> None:
        """Covered entry needs entry evidence."""
        self.fx.repo.write("notes/entry-evidence.json", "{}")
        self.assertIn("maps `mod:good`, which has no nonempty entry evidence", self.fx.problems())

    def test_partial_or_missing_needs_gap_and_next_action(self) -> None:
        """Partial or missing needs gap and next action."""
        self.obj(1).update(coverage="partial", missing=None, next_action=None, entries=["mod:good"])
        problems = self.fx.problems()
        self.assertIn("is partial but records no missing requirement", problems)
        self.assertIn("is partial but has no next action", problems)

    def test_source_change_keeps_objective_ids(self) -> None:
        """A new outline edition adds source records.

        Objective identities and coverage are unchanged.
        """
        before = [o["id"] for o in self.fx.objectives]
        self.fx.outlines.append(outline(OUT_B, HASH_B, 1, 1))
        self.fx.modules.append(module(OUT_B, 1, 1))
        self.fx.items.append(item(OUT_B, 1, 1, [COMPARE]))
        r = self.fx.report()
        self.assertEqual(r["problems"], [])
        self.assertEqual([o["id"] for o in self.fx.objectives], before)
        self.assertEqual(r["objectives"], {"covered": 1, "missing": 1})

    def test_shared_core_counted_once_and_identical_wording_kept_separate(self) -> None:
        """Shared core counted once and identical wording kept separate."""
        occ: list[JsonObject] = [{"outline": OUT_A, "module": 2}, {"outline": OUT_B, "module": 2}]
        # Outline B prints only the shared core: one module and one item of its own.
        self.fx.outlines = [outline(OUT_A, HASH_A, 2, 3), outline(OUT_B, HASH_B, 1, 1)]
        self.fx.modules.append(module(OUT_A, 2, 1, occurrences=occ))
        self.fx.items.append(
            item(
                OUT_A,
                2,
                1,
                ["objective:interpret-real-returns"],
                occurrences=[f"{OUT_A}:m002:b01", f"{OUT_B}:m002:b01"],
            )
        )
        r = self.fx.report()
        self.assertEqual(r["problems"], [])
        self.assertEqual(r["outline_items"], 3)  # the second copy adds no item
        self.assertEqual(r["outline_items_by_component"]["shared core"], {"missing": 1})
        # The two items in module 1 share wording but remain two source obligations.
        self.assertEqual(r["outline_items_by_component"]["level"], {"covered": 2})

    def test_scope_totals_and_module_counts_must_reconcile(self) -> None:
        """Scope totals and module counts must reconcile."""
        self.fx.scope = {"modules": 1, "bullets": 3}
        self.fx.modules[0]["bullets"] = 1
        problems = self.fx.problems()
        self.assertIn("scope declares 1 modules / 3 bullets, but lists 1 / 2", problems)
        self.assertIn("declares 1 bullets but has 2 items", problems)

    def test_residual_gap_keeps_an_item_partial(self) -> None:
        """Residual gap keeps an item partial."""
        self.fx.items[1]["residual_gap"] = "Second operation not shown."
        r = self.fx.report()
        self.assertEqual(r["outline_items_by_component"], {"level": {"covered": 1, "partial": 1}})

    def test_provider_token_rejected_in_maintained_names_not_provenance(self) -> None:
        """Provider token rejected in maintained names not provenance."""
        clean = self.fx.problems()
        self.assertNotIn("provider token", clean)  # provenance filename contains it
        self.obj(1)["id"] = "objective:cfa-real-returns"
        self.fx.repo.write(
            "src/tools/cfa_helper.py",
            "def load_cfa_items():\n    cfa_rows = []\n    return cfa_rows\n",
        )
        self.fx.repo.write(
            "compendium/front/sources.tex",
            r"\qfsource{src-key}{A paper}"
            + "\n"
            + r"\qfsource{cfa-curriculum-2027}{Curriculum}"
            + "\n",
        )
        problems = self.fx.problems()
        self.assertIn("`objective:cfa-real-returns` contains the provider token", problems)
        self.assertIn("`src/tools/cfa_helper.py` contains the provider token", problems)
        self.assertIn("`load_cfa_items` contains the provider token", problems)
        self.assertIn("`cfa_rows` contains the provider token", problems)
        self.assertIn("`cfa-curriculum-2027` contains the provider token", problems)

    def test_provider_token_rejected_in_package_and_test_sources(self) -> None:
        """Package and test sources keep their path and Python-name review."""
        self.fx.repo.write("src/pkg/cfa_rules.py", "CFA_LIMIT = 1\n")
        self.fx.repo.write("src/tests/test_x.py", "def check_cfa_case():\n    pass\n")
        problems = self.fx.problems()
        self.assertIn("`src/pkg/cfa_rules.py` contains the provider token", problems)
        self.assertIn("`CFA_LIMIT` contains the provider token", problems)
        self.assertIn("`check_cfa_case` contains the provider token", problems)

    # Regressions for the three findings of the 18 October 2026 audit.

    def test_unreviewed_mapping_is_not_covered_by_covered_objectives(self) -> None:
        """Unreviewed mapping is not covered by covered objectives."""
        self.fx.items[0]["reviewed"] = None
        r = self.fx.report()
        self.assertEqual(r["problems"], [])
        self.assertEqual(r["outline_items_by_component"], {"level": {"covered": 1, "partial": 1}})
        self.fx.items[0]["reviewed"] = "yesterday"
        self.assertIn("malformed review date 'yesterday'", self.fx.problems())

    def test_mapped_label_must_be_a_typed_entry(self) -> None:
        """Mapped label must be a typed entry."""
        self.fx.repo.write(
            "compendium/sec-a/topic.tex",
            GOOD_ENTRY + "\\begin{figure}\\label{fig:flow}\\end{figure}\n",
        )
        self.obj(1)["candidate_entries"] = ["fig:flow"]
        self.assertIn("names `fig:flow`, which is not a typed compendium entry", self.fx.problems())

    def test_covered_objective_with_another_entry_and_stale_evidence_fails(self) -> None:
        """Covered objective with another entry and stale evidence fails."""
        other = GOOD_ENTRY.replace("mod:good", "mod:other").replace("{src-key}", "{linked-key}")
        self.fx.repo.write("compendium/sec-a/topic.tex", GOOD_ENTRY + other)
        self.fx.repo.write("notes/pathways/path-x.md", "## Entries\n- `mod:good`\n- `mod:other`\n")
        self.obj()["entries"] = ["mod:other"]  # evidence still describes mod:good
        problems = self.fx.problems()
        self.assertIn(
            "entry-evidence references ['mod:good'] do not match its mapped entries ['mod:other']",
            problems,
        )
        self.assertIn("maps `mod:other`, which has no nonempty entry evidence", problems)
        self.assertIn("source `src-key` is cited by none of its mapped entries", problems)

    def test_empty_or_misplaced_entry_evidence_fails(self) -> None:
        """Empty or misplaced entry evidence fails."""
        self.fx.repo.write_json(
            "notes/entry-evidence.json", {"mod:good": {"source": "", "review": ""}}
        )
        self.assertIn("maps `mod:good`, which has no nonempty entry evidence", self.fx.problems())
        self.fx.repo.write_json(
            "notes/entry-evidence.json",
            {"mod:good": {"source": "compendium/sec-b/other.tex", "review": "r"}},
        )
        self.assertIn("whose entry evidence names compendium/sec-b/other.tex", self.fx.problems())

    def test_review_only_source_need_not_be_cited(self) -> None:
        """Review only source need not be cited."""
        evidence(self.obj())["review_sources"] = [{"key": "linked-key", "locator": "sec. 2"}]
        self.assertEqual(self.fx.report()["problems"], [])

    def test_dropped_item_with_adjusted_counters_fails_against_the_manifest(self) -> None:
        """Dropped item with adjusted counters fails against the manifest."""
        self.fx.items.pop()
        self.fx.modules[0]["bullets"] = 1  # the scope is recounted from the lists
        self.assertIn(
            f"`{OUT_A}` has 1 module / 1 item occurrences, but the manifest declares 1 / 2",
            self.fx.problems(),
        )

    def test_shared_core_occurrence_counts_in_every_file(self) -> None:
        """Shared core occurrence counts in every file."""
        occ: list[JsonObject] = [{"outline": OUT_A, "module": 2}, {"outline": OUT_B, "module": 2}]
        self.fx.outlines = [outline(OUT_A, HASH_A, 2, 3), outline(OUT_B, HASH_B, 1, 1)]
        self.fx.modules.append(module(OUT_A, 2, 1, occurrences=occ))
        self.fx.items.append(
            item(
                OUT_A, 2, 1, ["objective:interpret-real-returns"], occurrences=[f"{OUT_A}:m002:b01"]
            )
        )
        problems = self.fx.problems()
        self.assertIn("occurrences differ from those of its module", problems)
        self.assertIn(
            f"`{OUT_B}` has 1 module / 0 item occurrences, but the manifest declares 1 / 1",
            problems,
        )

    def test_verify_outlines_detects_missing_and_changed_bytes(self) -> None:
        """Verify outlines detects missing and changed bytes."""
        path = f"reading_materials/outlines/outline-{HASH_A[:12]}.pdf"
        self.assertIn("local copy", self.fx.problems(verify=True))
        self.assertNotIn("source verification", self.fx.problems(verify=False))
        self.fx.repo.write(path, "outline A")
        r = self.fx.report(verify=True)
        self.assertEqual(r["problems"], [])
        self.assertTrue(r["outlines_verified"])
        self.fx.repo.write(path, "outline A, edited")
        self.assertIn("has SHA-256", self.fx.problems(verify=True))


class MalformedRecords(unittest.TestCase):
    """Malformed nested JSON is reported as problems instead of raising a traceback."""

    def test_malformed_fields_are_reported(self) -> None:
        """Each malformed field gives a named problem, and the rest of the run completes."""
        module_a = f"{OUT_A}:m001"
        cases: list[tuple[str, Callable[[CoverageFixture], object], str]] = [
            (
                "objective prerequisites null",
                lambda fx: fx.objectives[0].update(prerequisites=None),
                f"`{COMPARE}` field `prerequisites` must be a list of strings",
            ),
            (
                "objective entries [{}]",
                lambda fx: fx.objectives[0].update(entries=[{}]),
                f"`{COMPARE}` field `entries` must be a list of strings",
            ),
            (
                "module occurrences ['bad']",
                lambda fx: fx.modules[0].update(occurrences=["bad"]),
                f"`{module_a}` field `occurrences` must be a list of objects",
            ),
            (
                "item objectives null",
                lambda fx: fx.items[0].update(objectives=None),
                f"item `{module_a}:b01` maps to no objective",
            ),
            (
                "topic section object",
                lambda fx: fx.topics[0].update(section={}),
                "`topic:return-measurement` field `section` must be a string",
            ),
            (
                "objective supersedes list",
                lambda fx: fx.objectives[1].update(supersedes=[COMPARE]),
                "`objective:interpret-real-returns` field `supersedes` must be a string",
            ),
            (
                "evidence sources string",
                lambda fx: evidence(fx.objectives[0]).update(sources="src-key"),
                f"`{COMPARE}` field `sources` must be a list of objects",
            ),
            (
                "item occurrence number",
                lambda fx: fx.items[1].update(occurrences=[7]),
                f"`{module_a}:b02` field `occurrences` must be a list of strings",
            ),
            (
                "item command verbs number",
                lambda fx: fx.items[0].update(command_verbs=17),
                f"`{module_a}:b01` field `command_verbs` must be a list of strings",
            ),
            (
                "item paraphrase object",
                lambda fx: fx.items[0].update(paraphrase={"unexpected": "object"}),
                f"`{module_a}:b01` field `paraphrase` must be a string",
            ),
            (
                "item rationale list",
                lambda fx: fx.items[0].update(rationale=["unexpected", "list"]),
                f"`{module_a}:b01` field `rationale` must be a string",
            ),
            (
                "item residual gap number",
                lambda fx: fx.items[0].update(residual_gap=0),
                f"`{module_a}:b01` field `residual_gap` must be a string",
            ),
            (
                "scope list",
                lambda fx: setattr(fx, "scope", {"modules": [1], "bullets": 2}),
                "outline-crosswalk.json: `scope` field `modules` must be an integer",
            ),
            (
                "entry evidence list",
                lambda fx: fx.repo.write("notes/entry-evidence.json", "[]"),
                "notes/entry-evidence.json: expected an object of entry-evidence records",
            ),
            (
                "entry evidence not JSON",
                lambda fx: fx.repo.write("notes/entry-evidence.json", "{"),
                "notes/entry-evidence.json: not valid JSON",
            ),
        ]
        for name, corrupt, expected in cases:
            with self.subTest(name):
                repo = SyntheticRepository()
                self.addCleanup(repo.close)
                fx = CoverageFixture(repo)
                corrupt(fx)
                self.assertIn(expected, fx.problems())

    def test_null_or_empty_item_content_keeps_its_meaning(self) -> None:
        """Null or empty item content is missing content, not a type problem."""
        repo = SyntheticRepository()
        self.addCleanup(repo.close)
        fx = CoverageFixture(repo)
        fx.items[0].update(command_verbs=None, paraphrase="", rationale=None)
        fx.items[1].update(residual_gap="")
        problems = fx.problems()
        self.assertNotIn("must be", problems)
        self.assertIn(
            f"item `{OUT_A}:m001:b01` needs a paraphrase, command verbs and a rationale", problems
        )
        self.assertEqual(fx.report()["outline_items_by_component"], {"level": {"covered": 2}})

    def test_null_item_objectives_leave_the_item_missing(self) -> None:
        """An item mapped to null objectives is reported and counted as missing."""
        repo = SyntheticRepository()
        self.addCleanup(repo.close)
        fx = CoverageFixture(repo)
        fx.items[0]["objectives"] = None
        self.assertEqual(
            fx.report()["outline_items_by_component"], {"level": {"covered": 1, "missing": 1}}
        )


class SuccessiveRuns(unittest.TestCase):
    """Each run reads its own repository afresh; nothing is cached between runs."""

    def test_alternating_and_edited_repositories(self) -> None:
        """Runs on two repositories, and after an edit, each see the current files."""
        fixtures = []
        for _ in range(2):
            repo = SyntheticRepository()
            self.addCleanup(repo.close)
            fixtures.append(CoverageFixture(repo))
        good, other = fixtures
        other.items.pop()
        first = good.report()
        self.assertEqual(first["problems"], [])
        self.assertIn("but the manifest declares 1 / 2", other.problems())
        self.assertEqual(good.report(), first)
        good.repo.write("notes/entry-evidence.json", "{}")
        self.assertIn("no nonempty entry evidence", good.problems())


if __name__ == "__main__":
    unittest.main()
