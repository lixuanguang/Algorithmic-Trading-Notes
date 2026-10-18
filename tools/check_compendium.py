#!/usr/bin/env python3
r"""Check compendium entries, citation keys, labels and pathway links.

Run: uv run python tools/check_compendium.py [--check] [--json] [--root DIR]
(`make check-compendium` runs it with --check).

Printed entries require a title, a type-appropriate label, a Statement, and
known citations with locators. Source-review provenance belongs in
notes/entry-evidence.json; it is not a required printed field. Pathway notes
list entry labels under Entries and proposed entries under Entry backlog.
The ordered \qfsections list in compendium/compendium.tex is the single declaration
of compendium sections: chapter folders and section-overview notes must use one of
its keys, and every typed entry must be reachable from the master through a
section wrapper's \input chain. Specialist pathway notes may also use the pinned
guide's specialist pathway keys.

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
SECTIONS_DECL = re.compile(r"\\qfsections\{([^}]*)\}")
INPUT = re.compile(r"\\input\{([^}]+)\}")


def tex_text(path):
    """Return a LaTeX file's text with comments removed."""
    return "\n".join(strip_comment(text_line) for text_line in path.read_text().splitlines())


def load_sections(root, problems):
    r"""Return ordered section keys from the single \qfsections declaration in the master.

    A missing master, a missing or repeated declaration, a malformed key or a
    repeated key is reported; there is no fallback to another registry.
    """
    master = root / MASTER
    if not master.exists():
        problems.append(f"{MASTER.as_posix()}: missing, so no compendium sections are declared")
        return []
    decls = SECTIONS_DECL.findall(tex_text(master))
    if len(decls) != 1:
        problems.append(
            f"{MASTER.as_posix()}: expected exactly one \\qfsections declaration, "
            f"found {len(decls)}"
        )
        return []
    keys, seen = [], set()
    for key in (k.strip() for k in decls[0].split(",")):
        if not SECTION_KEY.match(key):
            problems.append(f"{MASTER.as_posix()}: malformed section key {key!r}")
        elif key in seen:
            problems.append(f"{MASTER.as_posix()}: section `{key}` is declared twice")
        else:
            seen.add(key)
            keys.append(key)
    return keys


def load_specialist_pathways(root):
    """Return the pinned guide's specialist pathway keys, used only to name pathway notes."""
    data = json.loads((root / "guide" / "learning_routes.json").read_text())
    return {r["id"] for r in data["specialist_routes"]}


def load_routes(root, problems):
    """Return declared sections and the keys a pathway note may use.

    A pathway note may use a declared section key or a guide specialist pathway key.
    """
    sections = set(load_sections(root, problems))
    specialist = load_specialist_pathways(root)
    for key in sorted(sections & specialist):
        problems.append(
            f"{MASTER.as_posix()}: section `{key}` collides with a guide specialist pathway key"
        )
    return sections, sections | specialist


def reachable_files(root, sections, problems):
    r"""Return topic files reached from the master.

    Starts from <key>/section.tex for each declared key and follows its \input chain.
    """
    compendium = root / "compendium"
    reached, queue = set(), []
    for key in sorted(sections):
        wrapper = compendium / key / "section.tex"
        if wrapper.exists():
            queue.append(wrapper)
    while queue:
        path = queue.pop()
        if path in reached:
            continue
        reached.add(path)
        for target in INPUT.findall(tex_text(path)):
            child = compendium / (target if Path(target).suffix else target + ".tex")
            if child.exists():
                queue.append(child)
            else:
                problems.append(
                    f"{path.relative_to(root).as_posix()}: \\input{{{target}}} names no file"
                )
    return reached


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
    """Return typed entries with their structural gaps, appending problems as found."""
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
        if reached is not None and path not in reached and ENTRY.search(text):
            problems.append(f"{rel}: has typed entries but is not reachable from compendium.tex")
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
    sections, pathways = load_routes(root, problems)
    reached = reachable_files(root, sections, problems)
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
