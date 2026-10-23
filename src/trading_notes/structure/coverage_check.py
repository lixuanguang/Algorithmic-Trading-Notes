"""Check the subject coverage records and reconcile the external outline crosswalk.

Reads notes/coverage/objectives.json (topics and neutral learning objectives),
notes/coverage/outline-manifest.json (external outline files) and
notes/coverage/outline-crosswalk.json (outline modules and items mapped to objectives).
It validates their shape, identifiers, references, typed entry labels, section owners
(the sections declared in compendium/compendium.tex), evidence consistency and status
requirements; it reconciles each active outline's item and module occurrences with the
manifest; and it reports objective coverage separately from outline-item coverage. An
outline item counts as covered only after its mapping has been reviewed. Verification
also checks the local outline copies against their SHA-256.

A field of the wrong JSON type is reported and then read as absent, so a malformed record
gives problems rather than a traceback.

This is a structural check. It does not judge whether an entry teaches an objective
well enough, and it says nothing about learner mastery.
"""

# standard library imports
import ast
import hashlib
import json
import re
from collections import Counter, defaultdict
from collections.abc import Container, Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Literal, Self, TypedDict

# project library imports
from trading_notes.structure.compendium import Compendium, Entry
from trading_notes.structure.json_fields import JsonObject, JsonRecord, as_object

type Coverage = Literal["missing", "partial", "covered"]
type NextAction = Literal["reuse", "extend", "write", "obtain-source", "review"]

COVERAGE: Final = Path("notes") / "coverage"
ENTRY_EVIDENCE: Final = Path("notes") / "entry-evidence.json"
COVERAGE_VALUES: Final[tuple[Coverage, ...]] = ("missing", "partial", "covered")
NEXT_ACTIONS: Final[tuple[NextAction, ...]] = (
    "reuse",
    "extend",
    "write",
    "obtain-source",
    "review",
)
SLUG: Final = r"[a-z0-9]+(?:-[a-z0-9]+)*"
TOPIC_ID: Final = re.compile(r"^topic:" + SLUG + "$")
OBJECTIVE_ID: Final = re.compile(r"^objective:" + SLUG + "$")
OUTLINE_ID: Final = re.compile(r"^outline:[0-9a-f]{12,64}$")
MODULE_ID: Final = re.compile(r"^(outline:[0-9a-f]{12,64}):m(\d{3})$")
ITEM_ID: Final = re.compile(r"^(outline:[0-9a-f]{12,64}:m\d{3}):b(\d{2})$")
REVIEW_DATE: Final = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PROHIBITED: Final = "cfa"  # provider token kept out of maintained names; allowed in provenance
# Trees whose folder and file names are maintained here; the ignored source copies and the
# vendored guide are not.
MAINTAINED_TREES: Final = ("compendium", "notes", "tools", "src", "tests")
# Python sources whose defined names are reviewed: the entrypoints, the package and tests.
PYTHON_SOURCES: Final = (("tools", "*.py"), ("src", "**/*.py"), ("tests", "**/*.py"))


class CoverageReport(TypedDict):
    """The JSON report printed by tools/check_coverage.py --json.

    Objective counts are keyed by coverage value, "invalid" counting a missing or unknown
    one; next actions by value, "None" counting objectives without one.
    """

    objectives: dict[str, int]
    objectives_total: int
    topics_total: int
    objectives_by_section: dict[str, dict[str, int]]
    next_actions: dict[str, int]
    outline_modules: int
    outline_items: int
    outline_items_by_component: dict[str, dict[str, int]]
    outline_items_unreviewed: int
    outlines_verified: bool
    problems: list[str]


def choice[T: str](value: object, options: tuple[T, ...]) -> T | None:
    """Return the option equal to value, or None when value is none of them."""
    for option in options:
        if value == option:
            return option
    return None


def module_outline(module_id: str) -> str:
    """Return the outline id of a well-formed module id (see MODULE_ID)."""
    return module_id.rsplit(":", 1)[0]


def item_module(item_id: str) -> str:
    """Return the module id of a well-formed item id (see ITEM_ID)."""
    return item_id.rsplit(":", 1)[0]


def item_outline(item_id: str) -> str | None:
    """Return the outline id an item id names, or None when the id is malformed."""
    return module_outline(item_module(item_id)) if ITEM_ID.match(item_id) else None


@dataclass(frozen=True)
class SourceRef:
    """A source an objective's evidence names, with its locator."""

    key: str | None
    locator: str | None


@dataclass(frozen=True)
class Evidence:
    """A partial or covered objective's evidence record.

    Attributes:
        sources: Substantive sources; each must be cited by a mapped entry.
        review_sources: Sources read only for the review; they need not be cited.
        entry_evidence: Labels whose entry-evidence records support the objective.
        review_record: Repository path of the review record, optionally with a #fragment.
        reading_notes: Repository paths of reading notes.
    """

    sources: tuple[SourceRef, ...]
    review_sources: tuple[SourceRef, ...]
    entry_evidence: tuple[str, ...]
    review_record: str
    reading_notes: tuple[str, ...]

    @classmethod
    def read(cls, record: JsonRecord) -> Self:
        """Read an evidence object; its lists may be null."""

        def refs(field: str) -> tuple[SourceRef, ...]:
            sources = (record.child(raw) for raw in record.objects(field, nullable=True))
            return tuple(SourceRef(src.text("key"), src.text("locator")) for src in sources)

        return cls(
            sources=refs("sources"),
            review_sources=refs("review_sources"),
            entry_evidence=record.texts("entry_evidence", nullable=True),
            review_record=record.text("review_record") or "",
            reading_notes=record.texts("reading_notes", nullable=True),
        )


@dataclass(frozen=True)
class Topic:
    """A canonical topic, owned by one compendium section."""

    id: str
    section: str | None
    prerequisites: tuple[str, ...]

    @classmethod
    def read(cls, record: JsonRecord) -> Self:
        """Read a topic whose id has been validated."""
        return cls(record.name, record.text("section"), record.texts("prerequisites"))


@dataclass(frozen=True)
class Objective:
    """A learning objective and its coverage status.

    Attributes:
        id: Validated objective id.
        topic: The owning topic id.
        prerequisites: Prerequisite objective or topic ids.
        supersedes: An objective id this one replaces.
        coverage: Coverage status; None when missing or invalid.
        next_action: Next editorial action; None when absent or invalid.
        operations: The operations the objective requires.
        entries: Labels of entries mapped as teaching the objective.
        candidate_entries: Labels found by subject search but not yet reviewed.
        missing: The requirement still missing, if any.
        evidence: Evidence record, if any.
    """

    id: str
    topic: str | None
    prerequisites: tuple[str, ...]
    supersedes: str | None
    coverage: Coverage | None
    next_action: NextAction | None
    operations: tuple[str, ...]
    entries: tuple[str, ...]
    candidate_entries: tuple[str, ...]
    missing: str | None
    evidence: Evidence | None

    @classmethod
    def read(cls, record: JsonRecord) -> Self:
        """Read an objective whose id has been validated.

        An invalid coverage or next action reads as None; `check_objectives` reports it.
        """
        evidence = record.nested("evidence")
        return cls(
            id=record.name,
            topic=record.text("topic"),
            prerequisites=record.texts("prerequisites"),
            supersedes=record.text("supersedes"),
            coverage=choice(record.get("coverage"), COVERAGE_VALUES),
            next_action=choice(record.get("next_action"), NEXT_ACTIONS),
            operations=record.texts("operations"),
            entries=record.texts("entries"),
            candidate_entries=record.texts("candidate_entries"),
            missing=record.text("missing"),
            evidence=Evidence.read(evidence) if evidence is not None else None,
        )


@dataclass(frozen=True)
class Outline:
    """An external outline file listed in the manifest.

    Attributes:
        id: Validated outline id, `outline:` and the leading SHA-256 digits.
        sha256: Full SHA-256 of the file.
        local_path: Repository path of the git-ignored local copy.
        role: "scope-reference" for an active outline.
        modules: The file's own module count.
        bullets: The file's own item count.
    """

    id: str
    sha256: str | None
    local_path: str | None
    role: str | None
    modules: int | None
    bullets: int | None

    @classmethod
    def read(cls, record: JsonRecord) -> Self:
        """Read a manifest outline whose id has been validated."""
        return cls(
            id=record.name,
            sha256=record.text("sha256"),
            local_path=record.text("local_path"),
            role=record.text("role"),
            modules=record.integer("modules"),
            bullets=record.integer("bullets"),
        )


@dataclass(frozen=True)
class Module:
    """A crosswalk module.

    Attributes:
        id: Validated module id.
        component: Outline component, such as "shared core".
        bullets: Declared item count.
        occurrences: Outline id of each occurrence; None where an occurrence names none.
    """

    id: str
    component: str | None
    bullets: int | None
    occurrences: tuple[str | None, ...]

    @classmethod
    def read(cls, record: JsonRecord) -> Self:
        """Read a crosswalk module whose id has been validated."""
        occurrences = (record.child(raw) for raw in record.objects("occurrences"))
        return cls(
            id=record.name,
            component=record.text("component"),
            bullets=record.integer("bullets"),
            occurrences=tuple(occurrence.text("outline") for occurrence in occurrences),
        )


@dataclass(frozen=True)
class Item:
    """A crosswalk item: one outline bullet mapped to objectives.

    Attributes:
        id: Validated item id.
        module: The module id the record names.
        objectives: Mapped objective ids; null maps none.
        command_verbs: The outline's command verbs; null lists none.
        paraphrase: The item paraphrased in our own words.
        rationale: Why the item maps to its objectives.
        residual_gap: What the mapped objectives leave uncovered; null or empty for nothing.
        reviewed: Review date of the mapping, YYYY-MM-DD when well formed.
        occurrences: Item ids of every printed copy, its own included.
    """

    id: str
    module: str | None
    objectives: tuple[str, ...]
    command_verbs: tuple[str, ...]
    paraphrase: str | None
    rationale: str | None
    residual_gap: str | None
    reviewed: str | None
    occurrences: tuple[str, ...]

    @classmethod
    def read(cls, record: JsonRecord) -> Self:
        """Read a crosswalk item whose id has been validated."""
        return cls(
            id=record.name,
            module=record.text("module"),
            objectives=record.texts("objectives", nullable=True),
            command_verbs=record.texts("command_verbs", nullable=True),
            paraphrase=record.text("paraphrase"),
            rationale=record.text("rationale"),
            residual_gap=record.text("residual_gap"),
            reviewed=record.text("reviewed"),
            occurrences=record.texts("occurrences"),
        )


@dataclass(frozen=True)
class CompendiumIndex:
    """What the coverage records are checked against, from one run's compendium.

    Attributes:
        root: Resolved repository root, against which record paths are resolved.
        sections: Declared section keys.
        entries: Typed entries by label.
        cite_keys: Every known citation key.
        entry_sources: Source file of each label with a nonempty entry-evidence record.
    """

    root: Path
    sections: frozenset[str]
    entries: dict[str, Entry]
    cite_keys: frozenset[str]
    entry_sources: dict[str, str]


def load_coverage_file(root: Path, name: str, problems: list[str]) -> JsonObject | None:
    """Load one coverage file, reporting a missing, invalid or unversioned file.

    Returns:
        The file's top-level object, or None when it was reported.
    """
    where = (COVERAGE / name).as_posix()
    try:
        data: object = json.loads((root / COVERAGE / name).read_text(encoding="utf-8"))
    except FileNotFoundError:
        problems.append(f"{where}: missing")
        return None
    except ValueError as exc:  # JSON or UTF-8 decoding
        problems.append(f"{where}: not valid JSON ({exc})")
        return None
    fields = as_object(data)
    if fields is None or fields.get("schema_version") != 1:
        problems.append(f"{where}: expected an object with schema_version 1")
        return None
    return fields


def load_entry_sources(root: Path, problems: list[str]) -> dict[str, str]:
    """Return the source file named by each label's nonempty entry-evidence record.

    A missing notes/entry-evidence.json means no evidence. A record whose source or review
    is blank or not a string is left out, so an objective mapping its label is reported.
    """
    path, where = root / ENTRY_EVIDENCE, ENTRY_EVIDENCE.as_posix()
    if not path.exists():
        return {}
    try:
        data: object = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:  # JSON or UTF-8 decoding
        problems.append(f"{where}: not valid JSON ({exc})")
        return {}
    records = as_object(data)
    if records is None:
        problems.append(f"{where}: expected an object of entry-evidence records by label")
        return {}
    sources = {}
    for label, value in records.items():
        record = as_object(value) or {}
        source, review = record.get("source"), record.get("review")
        if (
            isinstance(source, str)
            and source.strip()
            and isinstance(review, str)
            and review.strip()
        ):
            sources[label] = source
    return sources


def object_list(
    data: JsonObject | None, field: str, where: str, problems: list[str]
) -> list[JsonObject]:
    """Return a file's list-of-objects field, reporting another shape; [] for no file."""
    if data is None:
        return []
    return JsonRecord(data, where, "", problems).objects(field, required=True)


def index_by_id(
    records: Iterable[JsonObject], pattern: re.Pattern[str], where: str, problems: list[str]
) -> dict[str, JsonObject]:
    """Index records by id, reporting malformed and duplicate ids; a later duplicate wins."""
    seen: dict[str, JsonObject] = {}
    for record in records:
        rid = record.get("id")
        if not isinstance(rid, str) or not pattern.match(rid):
            problems.append(f"{where}: malformed id {rid!r}")
            continue
        if rid in seen:
            problems.append(f"{where}: duplicate id `{rid}`")
        seen[rid] = record
    return seen


def naming_problems(names: Iterable[str | None], where: str) -> list[str]:
    """Report maintained names that contain the prohibited provider token."""
    return [
        f"{where}: maintained name `{n}` contains the provider token"
        for n in names
        if n is not None and PROHIBITED in n.lower()
    ]


def maintained_paths(root: Path) -> list[str]:
    """Return the repository-relative folders and files under the maintained trees."""
    paths = []
    for top in MAINTAINED_TREES:
        base = root / top
        if base.exists():
            paths += [
                p.relative_to(root).as_posix()
                for p in base.rglob("*")
                if "__pycache__" not in p.parts
            ]
    return paths


def python_names(root: Path) -> list[str]:
    """Return the function, class, argument and assigned names defined in the Python sources."""
    names = []
    for base, pattern in PYTHON_SOURCES:
        for path in sorted((root / base).glob(pattern)):
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                    names.append(node.name)
                elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                    names.append(node.id)
                elif isinstance(node, ast.arg):
                    names.append(node.arg)
    return names


def check_evidence(o: Objective, index: CompendiumIndex, where: str, problems: list[str]) -> None:
    """Check a partial or covered objective's entries and evidence for consistency.

    Mapped labels must be typed entries; the objective's entry-evidence references must name
    exactly its mapped entries; each must have a nonempty record whose source file is the
    entry's file; every declared source must be known, located and cited by a mapped entry
    (sources read only for review go under review_sources); the review record must exist.
    """
    ev = o.evidence
    if ev is None:
        problems.append(f"{where}: `{o.id}` is {o.coverage} without an evidence record")
        return
    mapped = set(o.entries)
    if not ev.entry_evidence or set(ev.entry_evidence) != mapped:
        problems.append(
            f"{where}: `{o.id}` entry-evidence references {list(ev.entry_evidence)!r} "
            f"do not match its mapped entries {sorted(mapped)}"
        )
    for label in sorted(mapped):
        source = index.entry_sources.get(label)
        if source is None:
            problems.append(
                f"{where}: `{o.id}` maps `{label}`, which has no nonempty entry evidence"
            )
        elif label in index.entries and source != index.entries[label].file:
            problems.append(
                f"{where}: `{o.id}` maps `{label}`, whose entry evidence names {source}, "
                f"not {index.entries[label].file}"
            )
    cited = {
        key for label in mapped if label in index.entries for key in index.entries[label].cites
    }
    if not ev.sources:
        problems.append(f"{where}: `{o.id}` is {o.coverage} without a substantive source")
    for field, refs, must_cite in (
        ("sources", ev.sources, True),
        ("review_sources", ev.review_sources, False),
    ):
        for src in refs:
            if src.key is None or src.key not in index.cite_keys:
                problems.append(f"{where}: `{o.id}` {field} names unknown source key `{src.key}`")
            elif not src.locator:
                problems.append(f"{where}: `{o.id}` {field} names `{src.key}` without a locator")
            elif must_cite and src.key not in cited:
                problems.append(
                    f"{where}: `{o.id}` source `{src.key}` is cited by none of its mapped entries"
                )
    record = ev.review_record
    if not record or not (index.root / record.split("#")[0]).exists():
        problems.append(f"{where}: `{o.id}` is {o.coverage} without an existing review record")
    for note in ev.reading_notes:
        if not (index.root / note).exists():
            problems.append(f"{where}: `{o.id}` names missing reading note {note}")


def check_objectives(
    data: JsonObject | None, index: CompendiumIndex, problems: list[str]
) -> tuple[dict[str, Topic], dict[str, Objective]]:
    """Validate topics and objectives and return them indexed by id.

    Args:
        data: objectives.json, or None when it was reported missing or invalid.
        index: The compendium the records refer to.
        problems: Receives the problems found, in order; it is appended to.
    """
    where = (COVERAGE / "objectives.json").as_posix()
    raw_topics = index_by_id(
        object_list(data, "topics", where, problems), TOPIC_ID, where, problems
    )
    raw_objectives = index_by_id(
        object_list(data, "objectives", where, problems), OBJECTIVE_ID, where, problems
    )
    topics: dict[str, Topic] = {}
    for tid, raw in raw_topics.items():
        t = topics[tid] = Topic.read(JsonRecord(raw, where, tid, problems))
        if t.section is None or t.section not in index.sections:
            problems.append(
                f"{where}: `{tid}` is owned by `{t.section}`, "
                "not a section declared in compendium.tex"
            )
        for p in t.prerequisites:
            if p not in raw_topics:
                problems.append(f"{where}: `{tid}` has unknown prerequisite `{p}`")
    objectives: dict[str, Objective] = {}
    for oid, raw in raw_objectives.items():
        o = objectives[oid] = Objective.read(JsonRecord(raw, where, oid, problems))
        if o.topic is None or o.topic not in raw_topics:
            problems.append(f"{where}: `{oid}` has unknown topic `{o.topic}`")
        for p in o.prerequisites:
            if p not in raw_objectives and p not in raw_topics:
                problems.append(f"{where}: `{oid}` has unknown prerequisite `{p}`")
        if o.supersedes is not None and o.supersedes not in raw_objectives:
            problems.append(f"{where}: `{oid}` supersedes unknown `{o.supersedes}`")
        if o.coverage is None:
            problems.append(f"{where}: `{oid}` has invalid coverage {raw.get('coverage')!r}")
        if o.next_action is None and raw.get("next_action") is not None:
            problems.append(f"{where}: `{oid}` has invalid next action {raw.get('next_action')!r}")
        if not o.operations:
            problems.append(f"{where}: `{oid}` lists no operations")
        for field, labels in (("entries", o.entries), ("candidate_entries", o.candidate_entries)):
            for label in labels:
                if label not in index.entries:
                    problems.append(
                        f"{where}: `{oid}` {field} names `{label}`, "
                        "which is not a typed compendium entry"
                    )
        status = o.coverage
        if status in ("missing", "partial"):
            if not o.missing:
                problems.append(f"{where}: `{oid}` is {status} but records no missing requirement")
            if o.next_action is None:
                problems.append(f"{where}: `{oid}` is {status} but has no next action")
        if status in ("partial", "covered") and not o.entries:
            problems.append(f"{where}: `{oid}` is {status} but maps no entry")
        if status == "covered" and o.missing:
            problems.append(f"{where}: `{oid}` is covered but still records a missing requirement")
        if status == "covered" or (status == "partial" and o.evidence is not None):
            check_evidence(o, index, where, problems)
    names: list[str | None] = [*topics, *objectives]
    for o in objectives.values():
        if o.evidence is not None:
            names += [src.key for src in (*o.evidence.sources, *o.evidence.review_sources)]
    problems += naming_problems(names, where)
    return topics, objectives


def check_crosswalk(
    manifest: JsonObject | None,
    crosswalk: JsonObject | None,
    objectives: Container[str],
    problems: list[str],
) -> tuple[dict[str, Outline], dict[str, Module], dict[str, Item]]:
    """Validate the manifest and crosswalk and reconcile occurrences with the manifest.

    Args:
        manifest: outline-manifest.json, or None when it was reported.
        crosswalk: outline-crosswalk.json, or None when it was reported.
        objectives: Known objective ids.
        problems: Receives the problems found, in order; it is appended to.

    Returns:
        Outlines, modules and items, each indexed by id.
    """
    mwhere = (COVERAGE / "outline-manifest.json").as_posix()
    cwhere = (COVERAGE / "outline-crosswalk.json").as_posix()
    raw_outlines = index_by_id(
        object_list(manifest, "outlines", mwhere, problems), OUTLINE_ID, mwhere, problems
    )
    outlines: dict[str, Outline] = {}
    for oid, raw in raw_outlines.items():
        rec = outlines[oid] = Outline.read(JsonRecord(raw, mwhere, oid, problems))
        if (
            rec.sha256 is None
            or not re.fullmatch(r"[0-9a-f]{64}", rec.sha256)
            or not rec.sha256.startswith(oid.split(":")[1])
        ):
            problems.append(
                f"{mwhere}: `{oid}` needs a full SHA-256 that starts with its id digits"
            )
        problems += naming_problems([rec.local_path], mwhere)
    problems += naming_problems(list(outlines), mwhere)
    raw_modules = index_by_id(
        object_list(crosswalk, "modules", cwhere, problems), MODULE_ID, cwhere, problems
    )
    raw_items = index_by_id(
        object_list(crosswalk, "items", cwhere, problems), ITEM_ID, cwhere, problems
    )
    per_module: Counter[str] = Counter()
    modules: dict[str, Module] = {}
    for mid, raw in raw_modules.items():
        m = modules[mid] = Module.read(JsonRecord(raw, cwhere, mid, problems))
        if module_outline(mid) not in outlines:
            problems.append(
                f"{cwhere}: module `{mid}` refers to an outline missing from the manifest"
            )
        for occ_outline in m.occurrences:
            if occ_outline is None or occ_outline not in outlines:
                problems.append(
                    f"{cwhere}: module `{mid}` has an occurrence in unknown `{occ_outline}`"
                )
    items: dict[str, Item] = {}
    for iid, raw in raw_items.items():
        it = items[iid] = Item.read(JsonRecord(raw, cwhere, iid, problems))
        mid = item_module(iid)
        if mid not in raw_modules or it.module != mid:
            problems.append(f"{cwhere}: item `{iid}` does not belong to a listed module")
        per_module[mid] += 1
        if not it.objectives:
            problems.append(f"{cwhere}: item `{iid}` maps to no objective")
        for o in it.objectives:
            if o not in objectives:
                problems.append(f"{cwhere}: item `{iid}` maps to unknown `{o}`")
        if not it.command_verbs or not it.paraphrase or not it.rationale:
            problems.append(
                f"{cwhere}: item `{iid}` needs a paraphrase, command verbs and a rationale"
            )
        for occ in it.occurrences:
            occ_outline = item_outline(occ)
            if occ_outline is None or occ_outline not in outlines:
                problems.append(
                    f"{cwhere}: item `{iid}` has a malformed or unknown occurrence `{occ}`"
                )
    # Reconcile occurrences in each active source file with the manifest's independent counts:
    # a shared-core item is one crosswalk record but one occurrence in every file that prints it.
    active = {oid for oid, rec in outlines.items() if rec.role == "scope-reference"}
    item_occ: Counter[str] = Counter()
    module_occ: Counter[str] = Counter()
    for mid, m in modules.items():
        if module_outline(mid) not in m.occurrences:
            problems.append(
                f"{cwhere}: module `{mid}` does not list its own outline among its occurrences"
            )
        if len(set(m.occurrences)) != len(m.occurrences):
            problems.append(f"{cwhere}: module `{mid}` repeats an occurrence")
        # An occurrence naming no outline was reported above and names no file to count.
        module_occ.update(occ for occ in m.occurrences if occ is not None)
    for iid, it in items.items():
        occ_outlines = [o for o in map(item_outline, it.occurrences) if o is not None]
        if iid not in it.occurrences:
            problems.append(f"{cwhere}: item `{iid}` does not list itself among its occurrences")
        if len(set(occ_outlines)) != len(occ_outlines):
            problems.append(f"{cwhere}: item `{iid}` repeats an occurrence")
        module = modules.get(it.module) if it.module is not None else None
        if set(occ_outlines) != set(module.occurrences if module is not None else ()):
            problems.append(f"{cwhere}: item `{iid}` occurrences differ from those of its module")
        item_occ.update(occ_outlines)
        if it.reviewed is not None and not REVIEW_DATE.match(it.reviewed):
            problems.append(f"{cwhere}: item `{iid}` has a malformed review date {it.reviewed!r}")
    for oid in sorted(set(item_occ) | set(module_occ)):
        if oid not in active:
            problems.append(
                f"{cwhere}: occurrences name `{oid}`, "
                "which is not an active outline in the manifest"
            )
    for oid in sorted(active):
        rec = outlines[oid]
        if (module_occ[oid], item_occ[oid]) != (rec.modules, rec.bullets):
            problems.append(
                f"{cwhere}: `{oid}` has {module_occ[oid]} module / "
                f"{item_occ[oid]} item occurrences, "
                f"but the manifest declares {rec.modules} / {rec.bullets}"
            )
    for mid, m in modules.items():
        if m.bullets != per_module[mid]:
            problems.append(
                f"{cwhere}: module `{mid}` declares {m.bullets} bullets "
                f"but has {per_module[mid]} items"
            )
    if crosswalk is not None:
        scope = JsonRecord(crosswalk, cwhere, "", problems).nested("scope")
        declared = (scope.integer("modules"), scope.integer("bullets")) if scope else (None, None)
        if declared != (len(modules), len(items)):
            problems.append(
                f"{cwhere}: scope declares {declared[0]} modules / {declared[1]} bullets, "
                f"but lists {len(modules)} / {len(items)}"
            )
    return outlines, modules, items


def item_status(item: Item, objectives: dict[str, Objective]) -> Coverage:
    """Return an outline item's coverage.

    An outline item is covered only when its mapping has been reviewed, every mapped objective
    is covered and no residual gap remains. Covered objectives behind an unreviewed mapping give
    `partial`: the content exists, but nobody has checked that it meets this item.
    """
    states = [objectives[o].coverage for o in item.objectives if o in objectives]
    if (
        states
        and all(s == "covered" for s in states)
        and not item.residual_gap
        and REVIEW_DATE.match(item.reviewed or "")
    ):
        return "covered"
    if any(s in ("covered", "partial") for s in states):
        return "partial"
    return "missing"


def verify_outlines(root: Path, outlines: dict[str, Outline], problems: list[str]) -> None:
    """Hash each local outline copy and report missing or changed files."""
    for oid, rec in outlines.items():
        path = root / (rec.local_path or "")
        if not path.is_file():
            problems.append(f"source verification: `{oid}` local copy {rec.local_path} is missing")
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != rec.sha256:
            problems.append(
                f"source verification: `{oid}` {rec.local_path} has SHA-256 {digest}, "
                f"expected {rec.sha256}"
            )


def build_report(root: Path, verify: bool = False) -> CoverageReport:
    """Run every coverage check on the repository at root and return the report.

    Args:
        root: Repository root.
        verify: Also hash the local outline copies; a missing or changed file is a problem.

    Raises:
        RepositoryInputError: The pinned guide or its catalogue is missing or malformed.
    """
    problems: list[str] = []
    compendium = Compendium.load(root)
    root = compendium.root
    # Only the declaration's problems belong to this report; the entry and input problems
    # are the compendium check's, so they are collected and discarded here.
    declaration = compendium.read_declaration(problems)
    sections = declaration.sections
    reached = set(compendium.input_order(sections, []))
    entries = compendium.scan_entries(set(sections), reached, [])
    index = CompendiumIndex(
        root=root,
        sections=frozenset(sections),
        entries={e.label: e for e in entries if e.label},
        cite_keys=compendium.citations.known,
        entry_sources=load_entry_sources(root, problems),
    )
    obj_data = load_coverage_file(root, "objectives.json", problems)
    manifest = load_coverage_file(root, "outline-manifest.json", problems)
    crosswalk = load_coverage_file(root, "outline-crosswalk.json", problems)
    topics, objectives = check_objectives(obj_data, index, problems)
    outlines, modules, items = check_crosswalk(manifest, crosswalk, objectives, problems)
    citations = compendium.citations
    problems += naming_problems(maintained_paths(root), "naming review")
    problems += naming_problems(sorted(set(python_names(root))), "naming review (Python sources)")
    problems += naming_problems(
        sorted(citations.registered - citations.catalogue), "naming review (source keys)"
    )
    problems += naming_problems(sorted(sections), "naming review (section keys)")
    if verify:
        verify_outlines(root, outlines, problems)

    by_section: defaultdict[str, Counter[str]] = defaultdict(Counter)
    for o in objectives.values():
        topic = topics.get(o.topic) if o.topic is not None else None
        section = topic.section if topic is not None and topic.section is not None else "?"
        by_section[section][o.coverage or "invalid"] += 1
    component = {mid: m.component if m.component is not None else "?" for mid, m in modules.items()}
    item_states: defaultdict[str, Counter[str]] = defaultdict(Counter)
    for it in items.values():
        item_states[component.get(it.module or "", "?")][item_status(it, objectives)] += 1
    return {
        "objectives": dict(Counter(o.coverage or "invalid" for o in objectives.values())),
        "objectives_total": len(objectives),
        "topics_total": len(topics),
        "objectives_by_section": {k: dict(v) for k, v in sorted(by_section.items())},
        "next_actions": dict(Counter(str(o.next_action) for o in objectives.values())),
        "outline_modules": len(modules),
        "outline_items": len(items),
        "outline_items_by_component": {k: dict(v) for k, v in sorted(item_states.items())},
        "outline_items_unreviewed": sum(1 for it in items.values() if not it.reviewed),
        "outlines_verified": verify
        and not any(p.startswith("source verification") for p in problems),
        "problems": problems,
    }
