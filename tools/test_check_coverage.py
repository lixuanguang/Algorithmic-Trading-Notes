"""Focused tests for check_coverage.py on small synthetic repositories.

Run: make test (uv run pytest)
"""

# standard library imports
import copy
import hashlib
import json
import unittest

# project library imports
import check_coverage as cov
from test_check_compendium import GOOD_ENTRY, Repo

HASH_A = hashlib.sha256(b"outline A").hexdigest()
HASH_B = hashlib.sha256(b"outline B").hexdigest()
OUT_A, OUT_B = f"outline:{HASH_A[:12]}", f"outline:{HASH_B[:12]}"

OBJECTIVES = {
    "schema_version": 1,
    "topics": [
        {
            "id": "topic:return-measurement",
            "title": "Returns",
            "section": "sec-a",
            "prerequisites": [],
        }
    ],
    "objectives": [
        {
            "id": "objective:compare-weighted-returns",
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
    ],
}


def manifest(*outlines):
    """Each outline as (id, digest, modules, items); the counts are the source file's own."""
    return {
        "schema_version": 1,
        "outlines": [
            {
                "id": oid,
                "sha256": digest,
                "local_path": f"reading_materials/outlines/outline-{digest[:12]}.pdf",
                "role": "scope-reference",
                "modules": n_modules,
                "bullets": n_items,
                "provenance": {"original_filename": "cfa-level-one-outline.pdf"},
            }
            for oid, digest, n_modules, n_items in outlines
        ],
    }


def module(outline, n, bullets, occurrences=None):
    """Return one crosswalk module record."""
    return {
        "id": f"{outline}:m{n:03d}",
        "outline": outline,
        "ordinal": n,
        "heading": f"Module {n}",
        "component": "shared core" if occurrences else "level",
        "bullets": bullets,
        "occurrences": occurrences or [{"outline": outline, "module": n}],
    }


def item(outline, n, b, objectives, occurrences=None, gap=None, reviewed="2026-10-18"):
    """Return one crosswalk item record, reviewed by default."""
    mid = f"{outline}:m{n:03d}"
    return {
        "id": f"{mid}:b{b:02d}",
        "module": mid,
        "ordinal": b,
        "paraphrase": "p",
        "command_verbs": ["calculate"],
        "objectives": objectives,
        "rationale": "r",
        "residual_gap": gap,
        "reviewed": reviewed,
        "occurrences": occurrences or [f"{mid}:b{b:02d}"],
    }


def crosswalk(modules, items):
    """Return a crosswalk whose scope totals match its records."""
    return {
        "schema_version": 1,
        "scope": {"modules": len(modules), "bullets": len(items)},
        "modules": modules,
        "items": items,
    }


class CoverageRepo(Repo):
    """A throwaway repository with coverage records and one valid entry."""

    def __init__(self):
        """Create the repository files."""
        super().__init__()
        self.write("compendium/sec-a/topic.tex", GOOD_ENTRY)
        self.write("notes/pathways/path-x.md", "## Entries\n- `mod:good`\n")
        self.write(
            "notes/entry-evidence.json",
            json.dumps(
                {
                    "mod:good": {
                        "source": "compendium/sec-a/topic.tex",
                        "review": "Checked against p. 3.",
                    }
                }
            ),
        )
        self.write("notes/records.md", "# Records\n")
        self.objectives = copy.deepcopy(OBJECTIVES)
        self.manifest = manifest((OUT_A, HASH_A, 1, 2))
        self.crosswalk = crosswalk(
            [module(OUT_A, 1, 2)],
            [
                item(OUT_A, 1, 1, ["objective:compare-weighted-returns"]),
                item(OUT_A, 1, 2, ["objective:compare-weighted-returns"]),
            ],
        )

    def report(self, verify=False):
        """Run the checker on the repository."""
        for name, doc in (
            ("objectives.json", self.objectives),
            ("outline-manifest.json", self.manifest),
            ("outline-crosswalk.json", self.crosswalk),
        ):
            self.write(f"notes/coverage/{name}", json.dumps(doc))
        return cov.report(self.root, verify=verify)

    def problems(self, verify=False):
        """Return the reported problems as one string."""
        return "\n".join(self.report(verify)["problems"])


class CoverageContract(unittest.TestCase):
    """Structural contract of the coverage records and the outline crosswalk."""

    def setUp(self):
        """Create a repository for each test."""
        self.repo = CoverageRepo()
        self.addCleanup(self.repo.close)

    def obj(self, n=0):
        """Return the n-th objective record."""
        return self.repo.objectives["objectives"][n]

    def test_valid_records_pass_and_many_items_map_to_one_objective(self):
        """Valid records pass and many items map to one objective."""
        r = self.repo.report()
        self.assertEqual(r["problems"], [])
        self.assertEqual(r["objectives"], {"covered": 1, "missing": 1})
        self.assertEqual(r["outline_items"], 2)
        self.assertEqual(r["outline_items_by_component"], {"level": {"covered": 2}})

    def test_unknown_label_source_reference_and_duplicate_id_fail(self):
        """Unknown label source reference and duplicate id fail."""
        self.obj()["entries"] = ["mod:absent"]
        self.repo.crosswalk["items"][0]["objectives"] = ["objective:nowhere"]
        self.repo.crosswalk["modules"][0]["occurrences"][0]["outline"] = "outline:0123456789ab"
        self.repo.objectives["objectives"].append(copy.deepcopy(self.obj(1)))
        problems = self.repo.problems()
        self.assertIn("names `mod:absent`, which is not a typed compendium entry", problems)
        self.assertIn("maps to unknown `objective:nowhere`", problems)
        self.assertIn("occurrence in unknown `outline:0123456789ab`", problems)
        self.assertIn("duplicate id `objective:interpret-real-returns`", problems)

    def test_invalid_status_and_unsupported_owner_fail(self):
        """Invalid status and unsupported owner fail."""
        self.obj(1)["coverage"] = "done"
        self.obj(1)["next_action"] = "someday"
        self.repo.objectives["topics"][0]["section"] = "not-a-section"
        problems = self.repo.problems()
        self.assertIn("invalid coverage 'done'", problems)
        self.assertIn("invalid next action 'someday'", problems)
        self.assertIn("owned by `not-a-section`", problems)

    def test_covered_without_entry_source_or_review_fails(self):
        """Covered without entry source or review fails."""
        self.obj()["entries"] = []
        self.obj()["evidence"] = {"sources": [], "review_record": "notes/missing.md"}
        problems = self.repo.problems()
        self.assertIn("is covered but maps no entry", problems)
        self.assertIn("is covered without a substantive source", problems)
        self.assertIn("is covered without an existing review record", problems)

    def test_covered_entry_needs_entry_evidence(self):
        """Covered entry needs entry evidence."""
        self.repo.write("notes/entry-evidence.json", "{}")
        self.assertIn("maps `mod:good`, which has no nonempty entry evidence", self.repo.problems())

    def test_partial_or_missing_needs_gap_and_next_action(self):
        """Partial or missing needs gap and next action."""
        self.obj(1).update(coverage="partial", missing=None, next_action=None, entries=["mod:good"])
        problems = self.repo.problems()
        self.assertIn("is partial but records no missing requirement", problems)
        self.assertIn("is partial but has no next action", problems)

    def test_source_change_keeps_objective_ids(self):
        """A new outline edition adds source records.

        Objective identities and coverage are unchanged.
        """
        before = [o["id"] for o in self.repo.objectives["objectives"]]
        self.repo.manifest = manifest((OUT_A, HASH_A, 1, 2), (OUT_B, HASH_B, 1, 1))
        self.repo.crosswalk["modules"].append(module(OUT_B, 1, 1))
        self.repo.crosswalk["items"].append(
            item(OUT_B, 1, 1, ["objective:compare-weighted-returns"])
        )
        self.repo.crosswalk["scope"] = {"modules": 2, "bullets": 3}
        r = self.repo.report()
        self.assertEqual(r["problems"], [])
        self.assertEqual([o["id"] for o in self.repo.objectives["objectives"]], before)
        self.assertEqual(r["objectives"], {"covered": 1, "missing": 1})

    def test_shared_core_counted_once_and_identical_wording_kept_separate(self):
        """Shared core counted once and identical wording kept separate."""
        occ = [{"outline": OUT_A, "module": 2}, {"outline": OUT_B, "module": 2}]
        # Outline B prints only the shared core: one module and one item of its own.
        self.repo.manifest = manifest((OUT_A, HASH_A, 2, 3), (OUT_B, HASH_B, 1, 1))
        core = item(
            OUT_A,
            2,
            1,
            ["objective:interpret-real-returns"],
            occurrences=[f"{OUT_A}:m002:b01", f"{OUT_B}:m002:b01"],
        )
        self.repo.crosswalk = crosswalk(
            [module(OUT_A, 1, 2), module(OUT_A, 2, 1, occurrences=occ)],
            self.repo.crosswalk["items"] + [core],
        )
        r = self.repo.report()
        self.assertEqual(r["problems"], [])
        self.assertEqual(r["outline_items"], 3)  # the second copy adds no item
        self.assertEqual(r["outline_items_by_component"]["shared core"], {"missing": 1})
        # The two items in module 1 share wording but remain two source obligations.
        self.assertEqual(r["outline_items_by_component"]["level"], {"covered": 2})

    def test_scope_totals_and_module_counts_must_reconcile(self):
        """Scope totals and module counts must reconcile."""
        self.repo.crosswalk["scope"]["bullets"] = 3
        self.repo.crosswalk["modules"][0]["bullets"] = 1
        problems = self.repo.problems()
        self.assertIn("scope declares 1 modules / 3 bullets, but lists 1 / 2", problems)
        self.assertIn("declares 1 bullets but has 2 items", problems)

    def test_residual_gap_keeps_an_item_partial(self):
        """Residual gap keeps an item partial."""
        self.repo.crosswalk["items"][1]["residual_gap"] = "Second operation not shown."
        r = self.repo.report()
        self.assertEqual(r["outline_items_by_component"], {"level": {"covered": 1, "partial": 1}})

    def test_provider_token_rejected_in_maintained_names_not_provenance(self):
        """Provider token rejected in maintained names not provenance."""
        clean = self.repo.problems()
        self.assertNotIn("provider token", clean)  # provenance filename contains it
        self.obj(1)["id"] = "objective:cfa-real-returns"
        self.repo.write(
            "tools/cfa_helper.py", "def load_cfa_items():\n    cfa_rows = []\n    return cfa_rows\n"
        )
        self.repo.write(
            "compendium/front/sources.tex",
            r"\qfsource{src-key}{A paper}"
            + "\n"
            + r"\qfsource{cfa-curriculum-2027}{Curriculum}"
            + "\n",
        )
        problems = self.repo.problems()
        self.assertIn("`objective:cfa-real-returns` contains the provider token", problems)
        self.assertIn("`tools/cfa_helper.py` contains the provider token", problems)
        self.assertIn("`load_cfa_items` contains the provider token", problems)
        self.assertIn("`cfa_rows` contains the provider token", problems)
        self.assertIn("`cfa-curriculum-2027` contains the provider token", problems)

    # Regressions for the three findings of the 18 October 2026 audit.

    def test_unreviewed_mapping_is_not_covered_by_covered_objectives(self):
        """Unreviewed mapping is not covered by covered objectives."""
        self.repo.crosswalk["items"][0]["reviewed"] = None
        r = self.repo.report()
        self.assertEqual(r["problems"], [])
        self.assertEqual(r["outline_items_by_component"], {"level": {"covered": 1, "partial": 1}})
        self.repo.crosswalk["items"][0]["reviewed"] = "yesterday"
        self.assertIn("malformed review date 'yesterday'", self.repo.problems())

    def test_mapped_label_must_be_a_typed_entry(self):
        """Mapped label must be a typed entry."""
        self.repo.write(
            "compendium/sec-a/topic.tex",
            GOOD_ENTRY + "\\begin{figure}\\label{fig:flow}\\end{figure}\n",
        )
        self.obj(1)["candidate_entries"] = ["fig:flow"]
        self.assertIn(
            "names `fig:flow`, which is not a typed compendium entry", self.repo.problems()
        )

    def test_covered_objective_with_another_entry_and_stale_evidence_fails(self):
        """Covered objective with another entry and stale evidence fails."""
        other = GOOD_ENTRY.replace("mod:good", "mod:other").replace("{src-key}", "{linked-key}")
        self.repo.write("compendium/sec-a/topic.tex", GOOD_ENTRY + other)
        self.repo.write("notes/pathways/path-x.md", "## Entries\n- `mod:good`\n- `mod:other`\n")
        self.obj()["entries"] = ["mod:other"]  # evidence still describes mod:good
        problems = self.repo.problems()
        self.assertIn(
            "entry-evidence references ['mod:good'] do not match its mapped entries ['mod:other']",
            problems,
        )
        self.assertIn("maps `mod:other`, which has no nonempty entry evidence", problems)
        self.assertIn("source `src-key` is cited by none of its mapped entries", problems)

    def test_empty_or_misplaced_entry_evidence_fails(self):
        """Empty or misplaced entry evidence fails."""
        self.repo.write(
            "notes/entry-evidence.json", json.dumps({"mod:good": {"source": "", "review": ""}})
        )
        self.assertIn("maps `mod:good`, which has no nonempty entry evidence", self.repo.problems())
        self.repo.write(
            "notes/entry-evidence.json",
            json.dumps({"mod:good": {"source": "compendium/sec-b/other.tex", "review": "r"}}),
        )
        self.assertIn("whose entry evidence names compendium/sec-b/other.tex", self.repo.problems())

    def test_review_only_source_need_not_be_cited(self):
        """Review only source need not be cited."""
        self.obj()["evidence"]["review_sources"] = [{"key": "linked-key", "locator": "sec. 2"}]
        self.assertEqual(self.repo.report()["problems"], [])

    def test_dropped_item_with_adjusted_counters_fails_against_the_manifest(self):
        """Dropped item with adjusted counters fails against the manifest."""
        self.repo.crosswalk["items"].pop()
        self.repo.crosswalk["modules"][0]["bullets"] = 1
        self.repo.crosswalk["scope"] = {"modules": 1, "bullets": 1}
        self.assertIn(
            f"`{OUT_A}` has 1 module / 1 item occurrences, but the manifest declares 1 / 2",
            self.repo.problems(),
        )

    def test_shared_core_occurrence_counts_in_every_file(self):
        """Shared core occurrence counts in every file."""
        occ = [{"outline": OUT_A, "module": 2}, {"outline": OUT_B, "module": 2}]
        self.repo.manifest = manifest((OUT_A, HASH_A, 2, 3), (OUT_B, HASH_B, 1, 1))
        core = item(
            OUT_A, 2, 1, ["objective:interpret-real-returns"], occurrences=[f"{OUT_A}:m002:b01"]
        )
        self.repo.crosswalk = crosswalk(
            [module(OUT_A, 1, 2), module(OUT_A, 2, 1, occurrences=occ)],
            self.repo.crosswalk["items"] + [core],
        )
        problems = self.repo.problems()
        self.assertIn("occurrences differ from those of its module", problems)
        self.assertIn(
            f"`{OUT_B}` has 1 module / 0 item occurrences, but the manifest declares 1 / 1",
            problems,
        )

    def test_verify_outlines_detects_missing_and_changed_bytes(self):
        """Verify outlines detects missing and changed bytes."""
        path = f"reading_materials/outlines/outline-{HASH_A[:12]}.pdf"
        self.assertIn("local copy", self.repo.problems(verify=True))
        self.assertNotIn("source verification", self.repo.problems(verify=False))
        self.repo.write(path, "outline A")
        self.assertEqual(self.repo.report(verify=True)["problems"], [])
        self.repo.write(path, "outline A, edited")
        self.assertIn("has SHA-256", self.repo.problems(verify=True))


if __name__ == "__main__":
    unittest.main()
