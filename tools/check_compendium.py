#!/usr/bin/env python3
r"""Check compendium entries, citation keys, labels and pathway links.

Run: uv run python tools/check_compendium.py [--check] [--json] [--root DIR]
(`make check-compendium` runs it with --check).

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

This is a structural check, not a claim or source-verification check.
"""

# standard library imports
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

PREFIX = {
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
LABEL_RE = r"(?:" + "|".join(sorted(set(PREFIX.values()))) + r"):[a-z0-9-]+"

ENTRY = re.compile(
    r"\\begin\{qf(" + "|".join(PREFIX) + r")\}(?:\[(.*?)\])?(.*?)\\end\{qf\1\}", re.S
)
LABEL = re.compile(r"\\label\{([^}]+)\}")
CITEP = re.compile(r"\\citep(\[[^\]]*\])?(\[[^\]]*\])?\{([^}]+)\}")
FIELD = re.compile(r"\\qffield\{([^}]+)\}")


def strip_comment(line):
    """Drop a LaTeX comment, keeping escaped percent signs."""
    return re.sub(r"(?<!\\)%.*", "", line)


def keys_from(text):
    """Split a comma-separated key list, dropping blanks."""
    return [k.strip() for k in text.split(",") if k.strip()]


MASTER = Path("compendium") / "compendium.tex"
SECTION_KEY = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PART_DECL = re.compile(r"\\qfpart\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}")
OLD_DECL = re.compile(r"\\qfsections\{")
INPUT = re.compile(r"\\input\{([^}]+)\}")
HEADING = re.compile(r"\\(chapter|section|subsection|subsubsection)\*?\{")
LEVEL = {"chapter": 0, "section": 1, "subsection": 2, "subsubsection": 3}


def tex_text(path):
    """Return a LaTeX file's text with comments removed."""
    return "\n".join(strip_comment(text_line) for text_line in path.read_text().splitlines())


def input_target(compendium, target):
    r"""Return the file an \input names, resolved so that equivalent paths are one file.

    LaTeX resolves \input paths from compendium/, so `a/topic` and `a/../a/topic` name the
    same file; resolving also removes symbolic-link aliases.
    """
    return (compendium / (target if Path(target).suffix else target + ".tex")).resolve()


def load_parts(root, problems):
    r"""Return the ordered Parts declared by \qfpart in the master: (key, title, [sections]).

    A missing master, no declaration, a leftover \qfsections list, a malformed key or a
    repeated Part or section key is reported; there is no fallback to another registry.
    """
    master = root / MASTER
    if not master.exists():
        problems.append(f"{MASTER.as_posix()}: missing, so no compendium sections are declared")
        return []
    text = tex_text(master)
    if OLD_DECL.search(text):
        problems.append(
            f"{MASTER.as_posix()}: \\qfsections is retired; declare sections in \\qfpart"
        )
    decls = PART_DECL.findall(text)
    if not decls:
        problems.append(f"{MASTER.as_posix()}: no \\qfpart declaration")
        return []
    parts, seen_parts, seen = [], set(), set()
    for pkey, title, body in decls:
        pkey, title = pkey.strip(), " ".join(title.split())
        if not SECTION_KEY.match(pkey) or pkey in seen_parts:
            problems.append(f"{MASTER.as_posix()}: malformed or repeated Part key {pkey!r}")
            continue
        seen_parts.add(pkey)
        keys = []
        for key in (k.strip() for k in body.split(",")):
            if not SECTION_KEY.match(key):
                problems.append(f"{MASTER.as_posix()}: malformed section key {key!r}")
            elif key in seen:
                problems.append(f"{MASTER.as_posix()}: section `{key}` is declared twice")
            else:
                seen.add(key)
                keys.append(key)
        parts.append((pkey, title, keys))
    return parts


def load_sections(root, problems):
    """Return the declared section keys in reading order, flattened across Parts."""
    return [key for _, _, keys in load_parts(root, problems) for key in keys]


def load_guide(root):
    """Return the pinned guide's learning routes."""
    return json.loads((root / "guide" / "learning_routes.json").read_text())


def load_specialist_pathways(root):
    """Return the pinned guide's specialist pathway keys, used only to name pathway notes."""
    return {r["id"] for r in load_guide(root)["specialist_routes"]}


def load_retired_overviews(root):
    """Return the guide's retired overview keys with their successor sections."""
    return {r["id"]: list(r["successors"]) for r in load_guide(root).get("retired_overviews", [])}


def check_guide_alignment(parts, guide, problems):
    """Compare the declared Parts and sections with the guide's learning_parts directly."""
    where = MASTER.as_posix()
    expected = [
        (p["id"], " ".join(p["title"].split()), list(p["routes"])) for p in guide["learning_parts"]
    ]
    if [p[0] for p in parts] != [p[0] for p in expected]:
        problems.append(
            f"{where}: Parts {[p[0] for p in parts]} differ from the guide's "
            f"{[p[0] for p in expected]}"
        )
    declared = {key: pkey for pkey, _, keys in parts for key in keys}
    guide_part = {key: pkey for pkey, _, keys in expected for key in keys}
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
    by_key = {p[0]: p for p in parts}
    for pkey, title, keys in expected:
        if pkey not in by_key:
            continue
        if by_key[pkey][1] != title:
            problems.append(
                f"{where}: Part `{pkey}` is titled {by_key[pkey][1]!r}, the guide {title!r}"
            )
        shared = [k for k in by_key[pkey][2] if k in keys]
        if shared != [k for k in keys if k in shared]:
            problems.append(
                f"{where}: Part `{pkey}` orders its sections {shared}, the guide {keys}"
            )


def load_routes(root, problems):
    """Return declared sections and the keys a pathway note may use.

    The declaration is checked against the guide. A pathway note may use a declared
    section key, a guide specialist pathway key or a retired guide overview key.
    """
    parts = load_parts(root, problems)
    sections = {key for _, _, keys in parts for key in keys}
    if parts:
        check_guide_alignment(parts, load_guide(root), problems)
    specialist = load_specialist_pathways(root)
    retired = set(load_retired_overviews(root))
    for key in sorted(sections & specialist):
        problems.append(
            f"{MASTER.as_posix()}: section `{key}` collides with a guide specialist pathway key"
        )
    for key in sorted(sections & retired):
        problems.append(
            f"{MASTER.as_posix()}: section `{key}` is a retired guide overview; "
            "declare its successor sections instead"
        )
    return sections, sections | specialist | retired


def input_order(root, sections, problems):
    r"""Return topic files in compiled order, reporting repeated inputs, cycles and missing files.

    Starts from <key>/section.tex for each declared key in order and follows each \input
    depth first. A file reached twice is reported, as is an \input back into a file that is
    still open (a cycle); neither is followed again. Files are identified by their resolved
    paths, so an aliased path cannot hide a repeat or a cycle.
    """
    root = root.resolve()
    compendium = root / "compendium"
    order, count, stack = [], defaultdict(int), []

    def visit(path, parent):
        rel = path.relative_to(root).as_posix()
        if path in stack:
            chain = " -> ".join(p.relative_to(root).as_posix() for p in [*stack, path])
            problems.append(f"input cycle: {chain}")
            return
        count[path] += 1
        if count[path] > 1:
            problems.append(f"{rel}: input {count[path]} times (again from {parent})")
            return
        order.append(path)
        stack.append(path)
        for target in INPUT.findall(tex_text(path)):
            child = input_target(compendium, target)
            if not child.is_relative_to(compendium):
                problems.append(f"{rel}: \\input{{{target}}} names a file outside compendium/")
            elif child.exists():
                visit(child, rel)
            else:
                problems.append(f"{rel}: \\input{{{target}}} names no file")
        stack.pop()

    for key in sections:
        wrapper = compendium / key / "section.tex"
        if wrapper.exists():
            visit(wrapper.resolve(), MASTER.as_posix())
    return order


def reachable_files(root, sections, problems):
    """Return the set of files reached from the master (see input_order)."""
    return set(input_order(root, sorted(sections), problems))


def heading_levels(root, sections, problems):
    r"""Report a wrapper without exactly one chapter heading, or a heading that skips a level.

    Headings are read in compiled order: a wrapper's own headings interleave with the
    files it inputs. Each chapter starts at level 0 (\chapter) and may descend one level
    at a time (\section, \subsection, \subsubsection). Files are identified as in input_order.
    """
    root = root.resolve()
    compendium = root / "compendium"
    token = re.compile(HEADING.pattern + "|" + INPUT.pattern)
    state = {"depth": None}
    seen = set()

    def walk(path):
        if path in seen:
            return
        seen.add(path)
        rel = path.relative_to(root).as_posix()
        text = tex_text(path)
        for m in token.finditer(text):
            if m.group(1) is None:
                child = input_target(compendium, m.group(2))
                if child.is_relative_to(compendium) and child.exists():
                    walk(child)
                continue
            level = LEVEL[m.group(1)]
            if level and (state["depth"] is None or level > state["depth"] + 1):
                line = text.count("\n", 0, m.start()) + 1
                problems.append(f"{rel}:{line}: \\{m.group(1)} skips a heading level")
            state["depth"] = level

    for key in sections:
        wrapper = compendium / key / "section.tex"
        if wrapper.exists():
            if len(re.findall(r"\\chapter\*?\{", tex_text(wrapper))) != 1:
                problems.append(
                    f"{wrapper.relative_to(root).as_posix()}: a section wrapper needs "
                    "exactly one \\chapter heading"
                )
            state["depth"] = None
            walk(wrapper.resolve())


def load_citation_keys(root):
    """Return catalogue keys from the guide plus keys registered in front/sources.tex."""
    keys = set(
        re.findall(
            r"\\CatalogueEntry\{([^}]+)\}",
            (root / "guide" / "institutional_quantitative_finance_reading_list.tex").read_text(),
        )
    )
    sources = root / "compendium" / "front" / "sources.tex"
    if sources.exists():
        keys |= set(re.findall(r"\\qfsource(?:\[[^]]*\])?\{([^}]+)\}", sources.read_text()))
    return keys


def scan_entries(root, sections, cite_keys, problems, reached=None):
    """Return typed entries with their structural gaps, appending problems as found.

    With `reached`, every non-empty .tex file in a section folder must be in it, whether it
    holds typed entries or only headings and prose. Front matter (compendium/front/) and the
    shared files at the top of compendium/ (master, house style, preamble) are not topic files.
    """
    root = root.resolve()
    entries = []
    compendium = root / "compendium"
    for path in sorted(compendium.rglob("*.tex")):
        parts = path.relative_to(compendium).parts
        if len(parts) < 2 or parts[0] == "front":
            continue
        rel = path.relative_to(root).as_posix()
        if parts[0] not in sections:
            problems.append(
                f"{rel}: folder `{parts[0]}` is not a section declared in compendium.tex"
            )
        text = tex_text(path)
        if reached is not None and path.resolve() not in reached and text.strip():
            what = "has typed entries" if ENTRY.search(text) else "is a topic file"
            problems.append(f"{rel}: {what} but is not reachable from compendium.tex")
        for m in ENTRY.finditer(text):
            etype, title, body = m.group(1), m.group(2), m.group(3)
            line = text.count("\n", 0, m.start()) + 1
            labels = LABEL.findall(body)
            head = body.split("\\qffield", 1)[0]
            label = next(
                (lab for lab in LABEL.findall(head) if not lab.startswith(("fig:", "eq:"))), None
            )
            gaps = []
            if not title:
                gaps.append("title")
            if not label:
                gaps.append("label")
            elif not label.startswith(PREFIX[etype] + ":"):
                gaps.append(f"label prefix (expected {PREFIX[etype]}:)")
            fields = FIELD.findall(body)
            if "Statement" not in fields:
                gaps.append("Statement field")
            claims = (
                body.split("\\qffield{Further reading}")[0] if "Further reading" in fields else body
            )
            cites = CITEP.findall(body)
            if not CITEP.search(claims):
                gaps.append("citation")
            for opt1, opt2, key in CITEP.findall(claims):
                if not opt1:
                    gaps.append(f"locator for {key}")
            for _, _, key in cites:
                if key not in cite_keys:
                    gaps.append(f"unknown citation key {key}")
            entries.append(
                {
                    "file": rel,
                    "line": line,
                    "section": parts[0],
                    "type": etype,
                    "label": label,
                    "labels": labels,
                    "gaps": sorted(set(gaps)),
                    "cites": sorted({key for _, _, key in cites}),
                }
            )
            for g in sorted(set(gaps)):
                problems.append(f"{rel}:{line}: entry {label or title!r} missing {g}")
    return entries


def duplicate_labels(root, problems):
    """Report labels defined more than once and return the set of all labels."""
    seen = defaultdict(list)
    for path in sorted((root / "compendium").rglob("*.tex")):
        if path.name == "house.tex":
            continue
        for n, line in enumerate(path.read_text().splitlines(), 1):
            for lab in LABEL.findall(strip_comment(line)):
                seen[lab].append(f"{path.relative_to(root).as_posix()}:{n}")
    for label, where in seen.items():
        if len(where) > 1:
            problems.append(f"label `{label}` defined {len(where)} times: {', '.join(where)}")
    return set(seen)


def pathway_notes(root, pathways, problems):
    """Return entry labels each pathway note lists under `Entries`, and its backlog stubs."""
    listed, stubs = {}, {}
    for path in sorted((root / "notes" / "pathways").glob("*.md")):
        key = path.stem
        if key not in pathways:
            problems.append(
                f"notes/pathways/{path.name}: `{key}` is not a declared section "
                "or guide pathway key"
            )
        heading, labels, n_stubs = "", set(), 0
        for line in path.read_text().splitlines():
            if line.startswith("#"):
                heading = line.lstrip("#").strip().lower()
            elif heading.startswith("entries"):
                labels |= set(re.findall(LABEL_RE, line))
            elif heading == "entry backlog" and re.match(r"-\s*" + LABEL_RE + ":", line.strip()):
                n_stubs += 1
        listed[key], stubs[key] = labels, n_stubs
    return listed, stubs


def report(root):
    """Run every structural check and return a JSON-serialisable report."""
    problems = []
    root = root.resolve()
    sections, pathways = load_routes(root, problems)
    ordered = [key for key in load_sections(root, []) if key in sections]
    reached = set(input_order(root, ordered, problems))
    heading_levels(root, ordered, problems)
    populated = [key for key in ordered if (root / "compendium" / key / "section.tex").exists()]
    notes_dir = root / "notes" / "pathways"
    for key in populated:
        if not (notes_dir / f"{key}.md").exists():
            problems.append(
                f"section `{key}` is populated but has no overview note notes/pathways/{key}.md"
            )
    for key, successors in sorted(load_retired_overviews(root).items()):
        note = notes_dir / f"{key}.md"
        if note.exists():
            text = note.read_text()
            for succ in successors:
                if f"`{succ}`" not in text:
                    problems.append(
                        f"notes/pathways/{key}.md: bridge for a retired guide overview "
                        f"does not name its successor section `{succ}`"
                    )
    entries = scan_entries(root, sections, load_citation_keys(root), problems, reached)
    all_labels = duplicate_labels(root, problems)
    listed, stubs = pathway_notes(root, pathways, problems)
    entry_labels = {e["label"] for e in entries if e["label"]}
    for key, labels in listed.items():
        for lab in sorted(labels - all_labels):
            problems.append(
                f"notes/pathways/{key}.md lists `{lab}`, which no compendium label defines"
            )
    in_notes = set().union(*listed.values()) if listed else set()
    for lab in sorted(entry_labels - in_notes):
        problems.append(f"entry `{lab}` is listed in no pathway note")
    return {
        "pathways": {
            k: {
                "backlog_stubs": stubs.get(k, 0),
                "entries_listed": sorted(listed.get(k, set()) & entry_labels),
            }
            for k in sorted(listed)
        },
        "parts": [
            {"key": pkey, "sections": keys, "populated": [k for k in keys if k in populated]}
            for pkey, _, keys in load_parts(root, [])
        ],
        "entries": len(entries),
        "entries_by_section": dict(Counter(e["section"] for e in entries)),
        "entries_by_type": dict(Counter(e["type"] for e in entries)),
        "entries_with_gaps": [e["label"] or e["file"] for e in entries if e["gaps"]],
        "problems": problems,
    }


def print_report(r):
    """Print a report in human-readable form."""
    print(
        f"Entries: {r['entries']}  "
        + ", ".join(f"{k} {v}" for k, v in sorted(r["entries_by_type"].items()))
    )
    print(
        f"Parts: {len(r['parts'])}  sections declared "
        + "/".join(str(len(p["sections"])) for p in r["parts"])
        + ", populated "
        + "/".join(str(len(p["populated"])) for p in r["parts"])
    )
    print(f"Pathway notes: {len(r['pathways'])}")
    print(f"Problems: {len(r['problems'])}")
    for problem in r["problems"]:
        print("  - " + problem)
    print("Limits: this checks structure and references, not the truth of claims.")


def main(argv=None):
    """Parse arguments, run the checks and return the process exit status."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    ap.add_argument("--json", action="store_true", help="print the report as JSON")
    ap.add_argument("--check", action="store_true", help="exit 1 when any problem is reported")
    args = ap.parse_args(argv)
    r = report(args.root.resolve())
    if args.json:
        json.dump(r, sys.stdout, indent=1)
        print()
    else:
        print_report(r)
    return 1 if args.check and r["problems"] else 0


if __name__ == "__main__":
    sys.exit(main())
