r"""Check compendium entries, citation keys, labels and pathway links.

Printed entries require a title, a type-appropriate label, a Statement, and
known citations with locators. Source-review provenance belongs in
notes/entry-evidence.json; it is not a required printed field. Pathway notes
list entry labels under Entries and proposed entries under Entry backlog.

The ordered \qfpart declarations in compendium/compendium.tex are the single
declaration of compendium Parts and sections. Their keys, titles, order and
membership must equal the pinned guide's learning_parts. Chapter folders and
section-overview notes must use a declared section key, and every populated section
needs its overview note. Specialist pathway notes may also use the guide's
specialist pathway keys, and a note for one of the guide's retired overviews is a
compatibility bridge that must name each successor section. Every non-empty topic
file, including one with only headings or prose, is input exactly once, in declared
order, from a section wrapper's \input chain, without cycles; equivalent paths name
one file. Headings below a chapter must not skip a level.

A chapter's title is its guide section's name. Below it, each \section is a guide specialist
pathway opened by \qfpathway{pathway-key}{Name} in the wrapper: the key must be one of that
section's pathways in the guide's specialist_order, the name the guide's, each pathway at most
once and in the guide's relative order, and each with at least one typed entry. A pathway
without local material is omitted. Every topic file, and so every typed entry, is input
under a pathway; a chapter may open with brief prose in its wrapper. Topic files hold the
lower headings (\subsection, \subsubsection) only.

This is a structural check, not a claim or source-verification check.
"""

import re
from collections import Counter, defaultdict
from collections.abc import Collection, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Final, TypedDict

from trading_notes.structure.compendium import (
    ENTRY,
    INPUT,
    LABEL,
    LABEL_PREFIX,
    Compendium,
)

PATHWAY_NOTES: Final = Path("notes") / "pathways"
LABEL_RE: Final = r"(?:" + "|".join(sorted(set(LABEL_PREFIX.values()))) + r"):[a-z0-9-]+"
HEADING: Final = re.compile(r"\\(chapter|section|subsection|subsubsection|qfpathway)\*?\{")
LEVEL: Final = {
    "chapter": 0,
    "section": 1,
    "qfpathway": 1,
    "subsection": 2,
    "subsubsection": 3,
}
PATHWAY: Final = re.compile(r"\\qfpathway\{([^}]*)\}\{([^}]*)\}")
CHAPTER: Final = re.compile(r"\\chapter\*?\{([^}]*)\}")


class PathwaySummary(TypedDict):
    """A pathway note's listing in the report."""

    backlog_stubs: int
    entries_listed: list[str]


class PartSummary(TypedDict):
    """A declared Part in the report."""

    key: str
    sections: list[str]
    populated: list[str]


class CompendiumReport(TypedDict):
    """The JSON report printed by trading_notes.cli.check_compendium --json."""

    pathways: dict[str, PathwaySummary]
    parts: list[PartSummary]
    pathways_rendered: dict[str, list[str]]
    entries: int
    entries_by_section: dict[str, int]
    entries_by_type: dict[str, int]
    entries_with_gaps: list[str]
    problems: list[str]


@dataclass(frozen=True)
class NoteListing:
    """What a pathway note lists.

    Attributes:
        labels: Entry labels named under a heading that starts with "Entries".
        backlog_stubs: Proposed entries, as `- <label>:` lines under "Entry backlog".
    """

    labels: frozenset[str]
    backlog_stubs: int


def check_heading_levels(
    compendium: Compendium, sections: Sequence[str], problems: list[str]
) -> None:
    r"""Report a wrapper without exactly one chapter heading, or a heading that skips a level.

    Headings are read in compiled order: a wrapper's own headings interleave with the
    files it inputs. Each chapter starts at level 0 (\chapter) and may descend one level
    at a time (\section, \subsection, \subsubsection). Files are identified as in
    `Compendium.input_order`, and each is read once across all chapters.

    Args:
        compendium: The run's sources.
        sections: Declared section keys in reading order.
        problems: Receives the problems found, in order; it is appended to.
    """
    token = re.compile(HEADING.pattern + "|" + INPUT.pattern)
    seen: set[Path] = set()
    depth: int | None = None

    def walk(path: Path) -> None:
        nonlocal depth
        if path in seen:
            return
        seen.add(path)
        text = compendium.text(path)
        for m in token.finditer(text):
            if m.group(1) is None:
                child = compendium.input_target(m.group(2))
                if child.is_relative_to(compendium.directory) and child.exists():
                    walk(child)
                continue
            level = LEVEL[m.group(1)]
            if level and (depth is None or level > depth + 1):
                line = text.count("\n", 0, m.start()) + 1
                problems.append(
                    f"{compendium.relative(path)}:{line}: \\{m.group(1)} skips a heading level"
                )
            depth = level

    for key in sections:
        wrapper = compendium.wrapper(key)
        if wrapper.exists():
            if len(re.findall(r"\\chapter\*?\{", compendium.text(wrapper))) != 1:
                problems.append(
                    f"{compendium.relative(wrapper)}: a section wrapper needs "
                    "exactly one \\chapter heading"
                )
            depth = None
            walk(wrapper.resolve())


def check_pathways(
    compendium: Compendium, sections: Sequence[str], problems: list[str]
) -> dict[str, list[str]]:
    r"""Compare each populated chapter's title and \qfpathway headings with the guide.

    The chapter title must be the section's guide name. In the wrapper every \input follows
    a \qfpathway, so no topic file, and no typed entry, sits outside a numbered pathway; a
    chapter may open with brief introductory prose in the wrapper itself. Each pathway key
    belongs to this section's specialist_order, carries the guide's name, appears once, in the
    guide's relative order, and has at least one typed entry among the files input under it.
    Peer headings other than \qfpathway are reported: a bare or starred \section or an
    unnumbered overview command in a wrapper, and \chapter, \section, \qfpathway or an
    overview command in a topic file.

    Args:
        compendium: The run's sources.
        sections: Declared section keys in reading order.
        problems: Receives the problems found, in order; it is appended to.

    Returns:
        The pathway keys each populated section opens, in wrapper order.
    """
    guide = compendium.guide
    owner = {pid: sec for sec, pids in guide.section_pathways.items() for pid in pids}
    token = re.compile(
        PATHWAY.pattern + "|" + INPUT.pattern + r"|(\\section\*?\{|\\qfoverview[a-z]*)"
    )
    rendered: dict[str, list[str]] = {}

    def entries_under(path: Path, seen: set[Path]) -> int:
        if path in seen or not path.exists():
            return 0
        seen.add(path)
        text = compendium.text(path)
        found = len(ENTRY.findall(text))
        for target in INPUT.findall(text):
            child = compendium.input_target(target)
            if child.is_relative_to(compendium.directory):
                found += entries_under(child, seen)
        return found

    for key in sections:
        wrapper = compendium.wrapper(key)
        if not wrapper.exists():
            continue
        where = compendium.relative(wrapper)
        text = compendium.text(wrapper)
        titles = CHAPTER.findall(text)
        name = guide.section_names.get(key)
        if titles and name is not None and " ".join(titles[0].split()) != name:
            problems.append(f"{where}: chapter is titled {titles[0]!r}, the guide {name!r}")
        order = guide.section_pathways.get(key, ())
        current: str | None = None
        counts: dict[str, int] = {}
        keys: list[str] = []
        for m in token.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            if m.group(1) is not None:
                pid, title = m.group(1).strip(), " ".join(m.group(2).split())
                current = pid
                if pid in counts:
                    problems.append(f"{where}:{line}: pathway `{pid}` is opened twice")
                    continue
                counts[pid] = 0
                keys.append(pid)
                if pid not in guide.pathway_names:
                    problems.append(f"{where}:{line}: `{pid}` is not a guide specialist pathway")
                elif owner.get(pid) != key:
                    problems.append(
                        f"{where}:{line}: pathway `{pid}` belongs to section "
                        f"`{owner.get(pid)}`, not `{key}`"
                    )
                elif title != guide.pathway_names[pid]:
                    problems.append(
                        f"{where}:{line}: pathway `{pid}` is titled {title!r}, "
                        f"the guide {guide.pathway_names[pid]!r}"
                    )
            elif m.group(3) is not None:
                if current is None:
                    problems.append(
                        f"{where}:{line}: \\input{{{m.group(3)}}} sits outside any numbered "
                        "pathway; open the guide pathway it serves with \\qfpathway first"
                    )
                    continue
                child = compendium.input_target(m.group(3))
                if child.is_relative_to(compendium.directory):
                    counts[current] += entries_under(child, set())
            else:
                problems.append(
                    f"{where}:{line}: {m.group(4).rstrip('{')} is not a guide pathway heading; "
                    "use \\qfpathway"
                )
        listed = [pid for pid in keys if owner.get(pid) == key]
        if listed != [pid for pid in order if pid in listed]:
            problems.append(
                f"{where}: pathways {listed} are not in the guide's order {list(order)}"
            )
        for pid in keys:
            if counts[pid] == 0:
                problems.append(f"{where}: pathway `{pid}` has no typed entry")
        rendered[key] = keys
    for path in compendium.tex_files:
        folders = path.relative_to(compendium.directory).parts
        if len(folders) < 2 or folders[0] == "front" or path.name == "section.tex":
            continue
        text = compendium.text(path)
        for m in re.finditer(r"\\(qfpathway|qfoverview[a-z]*|chapter|section)(?![a-z])\*?", text):
            line = text.count("\n", 0, m.start()) + 1
            problems.append(
                f"{compendium.relative(path)}:{line}: \\{m.group(1)} in a topic file; "
                "pathways open in the wrapper and topics use \\subsection"
            )
    return rendered


def check_duplicate_labels(compendium: Compendium, problems: list[str]) -> set[str]:
    """Report labels defined more than once and return every label defined.

    Every .tex file under compendium/ counts except house.tex, whose label macros are
    definitions of commands rather than labels.

    Args:
        compendium: The run's sources.
        problems: Receives one problem per repeated label; it is appended to.
    """
    seen: defaultdict[str, list[str]] = defaultdict(list)
    for path in compendium.tex_files:
        if path.name == "house.tex":
            continue
        for n, line in enumerate(compendium.text(path).splitlines(), 1):
            for label in LABEL.findall(line):
                seen[label].append(f"{compendium.relative(path)}:{n}")
    for label, where in seen.items():
        if len(where) > 1:
            problems.append(f"label `{label}` defined {len(where)} times: {', '.join(where)}")
    return set(seen)


def read_pathway_notes(root: Path) -> dict[str, str]:
    """Return the text of each notes/pathways/<key>.md, keyed by file stem, sorted by path."""
    paths = sorted((root / PATHWAY_NOTES).glob("*.md"))
    return {path.stem: path.read_text(encoding="utf-8") for path in paths}


def list_note_entries(
    notes: dict[str, str], note_keys: Collection[str], problems: list[str]
) -> dict[str, NoteListing]:
    """Return what each pathway note lists, reporting a note named after an unknown key.

    Args:
        notes: Note text by key, from `read_pathway_notes`.
        note_keys: Keys a note may be named after (see `Declaration.note_keys`).
        problems: Receives one problem per unknown note key; it is appended to.
    """
    listings: dict[str, NoteListing] = {}
    for key, text in notes.items():
        if key not in note_keys:
            problems.append(
                f"{PATHWAY_NOTES.as_posix()}/{key}.md: `{key}` is not a declared section "
                "or guide pathway key"
            )
        heading, labels, stubs = "", set[str](), 0
        for line in text.splitlines():
            if line.startswith("#"):
                heading = line.lstrip("#").strip().lower()
            elif heading.startswith("entries"):
                labels |= set(re.findall(LABEL_RE, line))
            elif heading == "entry backlog" and re.match(r"-\s*" + LABEL_RE + ":", line.strip()):
                stubs += 1
        listings[key] = NoteListing(frozenset(labels), stubs)
    return listings


def build_report(root: Path) -> CompendiumReport:
    """Run every structural check on the repository at root and return the report.

    Raises:
        RepositoryInputError: The pinned guide or its catalogue is missing or malformed.
    """
    problems: list[str] = []
    compendium = Compendium.load(root)
    declaration = compendium.read_declaration(problems)
    sections = declaration.sections
    reached = set(compendium.input_order(sections, problems))
    check_heading_levels(compendium, sections, problems)
    rendered = check_pathways(compendium, sections, problems)
    populated = [key for key in sections if compendium.wrapper(key).exists()]
    notes = read_pathway_notes(compendium.root)
    for key in populated:
        if key not in notes:
            problems.append(
                f"section `{key}` is populated but has no overview note "
                f"{PATHWAY_NOTES.as_posix()}/{key}.md"
            )
    for key, successors in sorted(compendium.guide.retired_overviews.items()):
        text = notes.get(key)
        if text is None:
            continue
        for successor in successors:
            if f"`{successor}`" not in text:
                problems.append(
                    f"{PATHWAY_NOTES.as_posix()}/{key}.md: bridge for a retired guide overview "
                    f"does not name its successor section `{successor}`"
                )
    entries = compendium.scan_entries(set(sections), reached, problems)
    all_labels = check_duplicate_labels(compendium, problems)
    listings = list_note_entries(notes, declaration.note_keys, problems)
    entry_labels = {e.label for e in entries if e.label}
    for key, listing in listings.items():
        for label in sorted(listing.labels - all_labels):
            problems.append(
                f"{PATHWAY_NOTES.as_posix()}/{key}.md lists `{label}`, "
                "which no compendium label defines"
            )
    in_notes = set[str]().union(*(listing.labels for listing in listings.values()))
    for label in sorted(entry_labels - in_notes):
        problems.append(f"entry `{label}` is listed in no pathway note")
    return {
        "pathways": {
            key: {
                "backlog_stubs": listings[key].backlog_stubs,
                "entries_listed": sorted(listings[key].labels & entry_labels),
            }
            for key in sorted(listings)
        },
        "parts": [
            {
                "key": part.key,
                "sections": list(part.sections),
                "populated": [key for key in part.sections if key in populated],
            }
            for part in declaration.parts
        ],
        "pathways_rendered": rendered,
        "entries": len(entries),
        "entries_by_section": dict(Counter(e.section for e in entries)),
        "entries_by_type": dict(Counter(e.kind for e in entries)),
        "entries_with_gaps": [e.label or e.file for e in entries if e.gaps],
        "problems": problems,
    }
