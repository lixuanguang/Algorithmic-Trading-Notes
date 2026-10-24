r"""Shared representation of the compendium sources and the pinned learning guide."""

import json
import re
from collections import Counter
from collections.abc import Container, Iterable, Set
from functools import cached_property
from pathlib import Path
from typing import Final

from trading_notes.records import Record
from trading_notes.structure.json_fields import JsonRecord, as_object

MASTER: Final = Path("compendium") / "compendium.tex"
GUIDE_ROUTES: Final = Path("guide") / "learning_routes.json"
CATALOGUE: Final = Path("guide") / "institutional_quantitative_finance_reading_list.tex"
SOURCES: Final = Path("compendium") / "front" / "sources.tex"

LABEL_PREFIX: Final = {
    "definition": "def",
    "convention": "conv",
    "result": "res",
    "model": "mod",
    "method": "meth",
    "mechanism": "mech",
    "evidence": "ev",
    "data": "data",
    "rule": "rule",
    "pitfall": "pit",
    "example": "ex",
}

ENTRY: Final = re.compile(
    r"\\begin\{qf(" + "|".join(LABEL_PREFIX) + r")\}(?:\[(.*?)\])?(.*?)\\end\{qf\1\}", re.S
)
LABEL: Final = re.compile(r"\\label\{([^}]+)\}")
CITEP: Final = re.compile(r"\\citep(\[[^\]]*\])?(\[[^\]]*\])?\{([^}]+)\}")
FIELD: Final = re.compile(r"\\qffield\{([^}]+)\}")
INPUT: Final = re.compile(r"\\input\{([^}]+)\}")
SECTION_KEY: Final = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PART_DECL: Final = re.compile(r"\\qfpart\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}")
OLD_DECL: Final = re.compile(r"\\qfsections\{")


class RepositoryInputError(Exception):
    """A required pinned input is missing or malformed, so the checks cannot run."""


def strip_comment(line: str) -> str:
    """Drop a LaTeX comment, keeping escaped percent signs."""
    return re.sub(r"(?<!\\)%.*", "", line)


def collapse(text: str) -> str:
    """Return text with each whitespace run collapsed to one space, as titles are compared."""
    return " ".join(text.split())


class Part(Record):
    """A Part of the reading order.

    Attributes:
        key: Part key.
        title: Display title with whitespace collapsed.
        sections: Section keys in reading order.
    """

    key: str
    title: str
    sections: tuple[str, ...]


class Guide(Record):
    """The parts of the pinned guide's learning_routes.json that the checks compare against.

    Names and titles have their whitespace collapsed.

    Attributes:
        parts: The guide's learning_parts in order.
        section_names: Name of each section (guide route) key.
        section_pathways: Specialist pathway keys of each section, in the guide's order.
        pathway_names: Name of each specialist pathway key.
        retired_overviews: Successor section keys of each retired overview key.
    """

    parts: tuple[Part, ...]
    section_names: dict[str, str]
    section_pathways: dict[str, tuple[str, ...]]
    pathway_names: dict[str, str]
    retired_overviews: dict[str, tuple[str, ...]]

    @classmethod
    def load(cls, root: Path) -> Guide:
        """Read and validate the guide under a repository root.

        Raises:
            RepositoryInputError: The file is missing, is not JSON or lacks a required field.
        """
        where = GUIDE_ROUTES.as_posix()
        try:
            data: object = json.loads((root / GUIDE_ROUTES).read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:  # ValueError covers JSON and UTF-8 decoding
            raise RepositoryInputError(f"{where}: cannot be read as JSON ({exc})") from exc
        return cls.parse(data, where)

    @classmethod
    def parse(cls, data: object, where: str) -> Guide:
        """Validate parsed guide JSON.

        Args:
            data: The parsed file.
            where: File name for error messages.

        Raises:
            RepositoryInputError: A required field is missing or has the wrong type.
        """
        problems: list[str] = []
        fields = as_object(data)
        if fields is None:
            raise RepositoryInputError(f"{where}: expected a JSON object")
        guide = JsonRecord(fields, where, "", problems)

        def records(field: str, required: bool) -> list[JsonRecord]:
            return [
                JsonRecord(raw, where, f"{field}[{i}]", problems)
                for i, raw in enumerate(guide.objects(field, required=required))
            ]

        parts = []
        for part in records("learning_parts", required=True):
            key, title = part.text("id", required=True), part.text("title", required=True)
            sections = part.texts("routes", required=True)
            if key is not None and title is not None:
                parts.append(Part(key=key, title=collapse(title), sections=sections))
        section_names, section_pathways = {}, {}
        for route in records("routes", required=True):
            if (key := route.text("id", required=True)) is not None:
                section_names[key] = collapse(route.text("name") or "")
                section_pathways[key] = route.texts("specialist_order")
        pathway_names = {}
        for route in records("specialist_routes", required=True):
            if (key := route.text("id", required=True)) is not None:
                pathway_names[key] = collapse(route.text("name") or "")
        retired = {}
        for overview in records("retired_overviews", required=False):
            if (key := overview.text("id", required=True)) is not None:
                retired[key] = overview.texts("successors", required=True)
        if problems:
            raise RepositoryInputError("\n".join(problems))
        return cls(
            parts=tuple(parts),
            section_names=section_names,
            section_pathways=section_pathways,
            pathway_names=pathway_names,
            retired_overviews=retired,
        )


class CitationKeys(Record):
    r"""The citation keys an entry may cite.

    Attributes:
        catalogue: Keys of the guide's reading-list catalogue.
        registered: Keys registered with \qfsource in compendium/front/sources.tex.
    """

    catalogue: frozenset[str]
    registered: frozenset[str]

    @property
    def known(self) -> frozenset[str]:
        """Return every key an entry may cite."""
        return self.catalogue | self.registered

    @classmethod
    def load(cls, root: Path) -> CitationKeys:
        """Read both registries; front/sources.tex is optional.

        Raises:
            RepositoryInputError: The guide catalogue cannot be read.
        """
        try:
            catalogue = (root / CATALOGUE).read_text(encoding="utf-8")
        except (OSError, ValueError) as exc:  # ValueError covers UTF-8 decoding
            raise RepositoryInputError(f"{CATALOGUE.as_posix()}: cannot be read ({exc})") from exc
        sources = root / SOURCES
        registered = sources.read_text(encoding="utf-8") if sources.exists() else ""
        return cls(
            catalogue=frozenset(re.findall(r"\\CatalogueEntry\{([^}]+)\}", catalogue)),
            registered=frozenset(re.findall(r"\\qfsource(?:\[[^]]*\])?\{([^}]+)\}", registered)),
        )


class Declaration(Record):
    r"""The master's \qfpart declaration of Parts and sections.

    Attributes:
        parts: Declared Parts with their well-formed, first-declared section keys, in order;
            malformed or repeated Part keys are left out.
        note_keys: Keys a pathway note may be named after: declared sections, guide
            specialist pathways and retired guide overviews.
    """

    parts: tuple[Part, ...]
    note_keys: frozenset[str]

    @property
    def sections(self) -> tuple[str, ...]:
        """Return the declared section keys in reading order, flattened across Parts."""
        return tuple(key for part in self.parts for key in part.sections)


class Entry(Record):
    """A typed entry in a section folder.

    Attributes:
        file: Repository-relative POSIX path of the file holding the entry.
        section: The section folder of that file.
        kind: Entry type, a key of LABEL_PREFIX.
        label: The entry's own label, or None when it has none.
        gaps: Sorted structural gaps; empty for a complete entry.
        cites: Sorted citation keys cited anywhere in the entry.
    """

    file: str
    section: str
    kind: str
    label: str | None
    gaps: tuple[str, ...]
    cites: tuple[str, ...]


class Compendium:
    r"""One run's view of a repository: its TeX sources, pinned guide and citation keys.

    Both structural checkers read the master's \qfpart declaration, the guide, the citation-key
    registries and the typed entries through this module. A `Compendium` belongs to one run: it
    reads each TeX file at most once and is discarded with the run, so successive runs on a modified
    repository never see stale text.

    Typed entries are environments `qf<type>` with an optional bracketed title. Entry labels carry a
    type prefix (`mod:` for a model, and so on). LaTeX resolves `\input` paths from compendium/, so
    files are identified by resolved paths: `a/topic` and `a/../a/topic`, or a symbolic link, name
    one file.

    TeX files are read on first use and then kept, comment-stripped, for the life of the
    instance. Create one instance per run so that edits between runs are seen.

    Attributes:
        root: Resolved repository root.
        directory: The compendium/ folder, from which LaTeX resolves \input paths.
        guide: The validated pinned guide.
        citations: Known citation keys.
    """

    def __init__(self, root: Path, guide: Guide, citations: CitationKeys) -> None:
        """Hold the inputs of one run; TeX files are read later, when first needed."""
        self.root = root.resolve()
        self.directory = self.root / "compendium"
        self.guide = guide
        self.citations = citations
        self._texts: dict[Path, str] = {}

    @classmethod
    def load(cls, root: Path) -> Compendium:
        """Read the guide and citation registries of the repository at root.

        Raises:
            RepositoryInputError: A required guide file is missing or malformed.
        """
        root = root.resolve()
        return cls(root, Guide.load(root), CitationKeys.load(root))

    @cached_property
    def tex_files(self) -> tuple[Path, ...]:
        """Return every .tex file under compendium/, sorted, as found on first use."""
        return tuple(sorted(self.directory.rglob("*.tex")))

    def text(self, path: Path) -> str:
        """Return a TeX file's text with comments removed, line breaks kept.

        Raises:
            OSError: The file cannot be read; callers check existence first.
        """
        key = path.resolve()
        if key not in self._texts:
            lines = key.read_text(encoding="utf-8").splitlines()
            self._texts[key] = "\n".join(strip_comment(line) for line in lines)
        return self._texts[key]

    def relative(self, path: Path) -> str:
        """Return a path under the root as a repository-relative POSIX path."""
        return path.relative_to(self.root).as_posix()

    def wrapper(self, section: str) -> Path:
        """Return the path of a section's wrapper, compendium/<key>/section.tex."""
        return self.directory / section / "section.tex"

    def input_target(self, target: str) -> Path:
        r"""Return the resolved file an \input names, adding .tex when it has no suffix."""
        return (self.directory / (target if Path(target).suffix else target + ".tex")).resolve()

    def read_declaration(self, problems: list[str]) -> Declaration:
        r"""Read the master's \qfpart declarations and compare them with the guide.

        A missing master, no declaration, a leftover \qfsections list, a malformed key or a
        repeated Part or section key is reported; there is no fallback to another registry.
        Declared sections must not collide with guide specialist pathway or retired
        overview keys.

        Args:
            problems: Receives the problems found, in order; it is appended to.
        """
        where = MASTER.as_posix()
        parts = self._declared_parts(where, problems)
        if parts:
            self._check_guide_alignment(parts, where, problems)
        sections = {key for part in parts for key in part.sections}
        specialist, retired = set(self.guide.pathway_names), set(self.guide.retired_overviews)
        for key in sorted(sections & specialist):
            problems.append(
                f"{where}: section `{key}` collides with a guide specialist pathway key"
            )
        for key in sorted(sections & retired):
            problems.append(
                f"{where}: section `{key}` is a retired guide overview; "
                "declare its successor sections instead"
            )
        return Declaration(parts=tuple(parts), note_keys=frozenset(sections | specialist | retired))

    def _declared_parts(self, where: str, problems: list[str]) -> list[Part]:
        r"""Return the master's well-formed Parts in order, reporting malformed declarations."""
        master = self.root / MASTER
        if not master.exists():
            problems.append(f"{where}: missing, so no compendium sections are declared")
            return []
        text = self.text(master)
        if OLD_DECL.search(text):
            problems.append(f"{where}: \\qfsections is retired; declare sections in \\qfpart")
        declarations = PART_DECL.findall(text)
        if not declarations:
            problems.append(f"{where}: no \\qfpart declaration")
            return []
        parts: list[Part] = []
        seen_parts: set[str] = set()
        seen: set[str] = set()
        for raw_key, raw_title, body in declarations:
            part_key = raw_key.strip()
            if not SECTION_KEY.match(part_key) or part_key in seen_parts:
                problems.append(f"{where}: malformed or repeated Part key {part_key!r}")
                continue
            seen_parts.add(part_key)
            keys: list[str] = []
            for key in (k.strip() for k in body.split(",")):
                if not SECTION_KEY.match(key):
                    problems.append(f"{where}: malformed section key {key!r}")
                elif key in seen:
                    problems.append(f"{where}: section `{key}` is declared twice")
                else:
                    seen.add(key)
                    keys.append(key)
            parts.append(Part(key=part_key, title=collapse(raw_title), sections=tuple(keys)))
        return parts

    def _check_guide_alignment(self, parts: list[Part], where: str, problems: list[str]) -> None:
        """Compare the declared Parts and sections with the guide's learning_parts directly."""
        expected = self.guide.parts
        if [p.key for p in parts] != [p.key for p in expected]:
            problems.append(
                f"{where}: Parts {[p.key for p in parts]} differ from the guide's "
                f"{[p.key for p in expected]}"
            )
        declared = {key: part.key for part in parts for key in part.sections}
        guide_part = {key: part.key for part in expected for key in part.sections}
        for key in sorted(set(guide_part) - set(declared)):
            problems.append(f"{where}: guide section `{key}` is not declared")
        for key in sorted(set(declared) - set(guide_part)):
            problems.append(f"{where}: section `{key}` is not a section of the pinned guide")
        for key in sorted(set(declared) & set(guide_part)):
            if declared[key] != guide_part[key]:
                problems.append(
                    f"{where}: section `{key}` is declared in Part `{declared[key]}`, "
                    f"the guide places it in `{guide_part[key]}`"
                )
        by_key = {part.key: part for part in parts}
        for part in expected:
            if part.key not in by_key:
                continue
            ours = by_key[part.key]
            if ours.title != part.title:
                problems.append(
                    f"{where}: Part `{part.key}` is titled {ours.title!r}, the guide {part.title!r}"
                )
            shared = [k for k in ours.sections if k in part.sections]
            if shared != [k for k in part.sections if k in shared]:
                problems.append(
                    f"{where}: Part `{part.key}` orders its sections {shared}, "
                    f"the guide {list(part.sections)}"
                )

    def input_order(self, sections: Iterable[str], problems: list[str]) -> list[Path]:
        r"""Return topic files in compiled order, reporting repeated inputs, cycles and gaps.

        Starts from each section's wrapper, in the order given, and follows each \input
        depth first. A file reached twice is reported, as is an \input back into a file that
        is still open (a cycle); neither is followed again. Files are identified by resolved
        paths, so an aliased path cannot hide a repeat or a cycle.

        Args:
            sections: Section keys whose wrappers start the traversal.
            problems: Receives the problems found, in order; it is appended to.

        Returns:
            Resolved paths of the wrappers and every file they reach, in compiled order.
        """
        order: list[Path] = []
        count: Counter[Path] = Counter()
        stack: list[Path] = []

        def visit(path: Path, parent: str) -> None:
            rel = self.relative(path)
            if path in stack:
                chain = " -> ".join(self.relative(p) for p in [*stack, path])
                problems.append(f"input cycle: {chain}")
                return
            count[path] += 1
            if count[path] > 1:
                problems.append(f"{rel}: input {count[path]} times (again from {parent})")
                return
            order.append(path)
            stack.append(path)
            for target in INPUT.findall(self.text(path)):
                child = self.input_target(target)
                if not child.is_relative_to(self.directory):
                    problems.append(f"{rel}: \\input{{{target}}} names a file outside compendium/")
                elif child.exists():
                    visit(child, rel)
                else:
                    problems.append(f"{rel}: \\input{{{target}}} names no file")
            stack.pop()

        for key in sections:
            wrapper = self.wrapper(key)
            if wrapper.exists():
                visit(wrapper.resolve(), MASTER.as_posix())
        return order

    def scan_entries(
        self, sections: Container[str], reached: Set[Path], problems: list[str]
    ) -> list[Entry]:
        """Return the typed entries of every section folder, reporting their structural gaps.

        Every non-empty .tex file in a section folder must be reached, whether it holds
        typed entries or only headings and prose. Front matter (compendium/front/) and the
        shared files at the top of compendium/ (master, house style, preamble) are not
        topic files. An entry needs a title, a label with its type's prefix, a Statement
        field and a citation with a locator before any Further reading; every citation
        key must be known.

        Args:
            sections: Declared section keys; any other folder is reported.
            reached: Resolved paths reached from the master (see `input_order`).
            problems: Receives the problems found, in order; it is appended to.
        """
        known = self.citations.known
        entries: list[Entry] = []
        for path in self.tex_files:
            folders = path.relative_to(self.directory).parts
            if len(folders) < 2 or folders[0] == "front":
                continue
            rel = self.relative(path)
            if folders[0] not in sections:
                problems.append(
                    f"{rel}: folder `{folders[0]}` is not a section declared in compendium.tex"
                )
            text = self.text(path)
            if path.resolve() not in reached and text.strip():
                what = "has typed entries" if ENTRY.search(text) else "is a topic file"
                problems.append(f"{rel}: {what} but is not reachable from compendium.tex")
            for m in ENTRY.finditer(text):
                kind, title, body = m.group(1), m.group(2), m.group(3)
                line = text.count("\n", 0, m.start()) + 1
                # The entry's own label precedes its first field; figure and equation labels
                # inside the statement are not entry labels.
                head = body.split("\\qffield", 1)[0]
                label = next(
                    (lab for lab in LABEL.findall(head) if not lab.startswith(("fig:", "eq:"))),
                    None,
                )
                gaps = []
                if not title:
                    gaps.append("title")
                if not label:
                    gaps.append("label")
                elif not label.startswith(LABEL_PREFIX[kind] + ":"):
                    gaps.append(f"label prefix (expected {LABEL_PREFIX[kind]}:)")
                fields = FIELD.findall(body)
                if "Statement" not in fields:
                    gaps.append("Statement field")
                # Claims need located citations; Further reading may cite without a locator.
                claims = (
                    body.split("\\qffield{Further reading}")[0]
                    if "Further reading" in fields
                    else body
                )
                cites = CITEP.findall(body)
                if not CITEP.search(claims):
                    gaps.append("citation")
                for locator, _, key in CITEP.findall(claims):
                    if not locator:
                        gaps.append(f"locator for {key}")
                for _, _, key in cites:
                    if key not in known:
                        gaps.append(f"unknown citation key {key}")
                unique_gaps = tuple(sorted(set(gaps)))
                entries.append(
                    Entry(
                        file=rel,
                        section=folders[0],
                        kind=kind,
                        label=label,
                        gaps=unique_gaps,
                        cites=tuple(sorted({key for _, _, key in cites})),
                    )
                )
                for gap in unique_gaps:
                    problems.append(f"{rel}:{line}: entry {label or title!r} missing {gap}")
        return entries
