#!/usr/bin/env python3
"""Check the subject coverage records and reconcile the external outline crosswalk.

Run: uv run python tools/check_coverage.py [--check] [--verify-outlines] [--json] [--root DIR]
(`make check-coverage` and `make verify-outlines` run it with --check).

Reads notes/coverage/objectives.json (topics and neutral learning objectives),
notes/coverage/outline-manifest.json (external outline files) and
notes/coverage/outline-crosswalk.json (outline modules and items mapped to objectives).
It validates their shape, identifiers, references, typed entry labels, section owners
(the sections declared in compendium/compendium.tex), evidence consistency and status
requirements; it reconciles each active outline's item and module occurrences with the
manifest; and it reports objective coverage separately from outline-item coverage. An
outline item counts as covered only after its mapping has been reviewed. --verify-outlines
also checks the local outline copies against their SHA-256.

This is a structural check. It does not judge whether an entry teaches an objective
well enough, and it says nothing about learner mastery.
"""

# standard library imports
import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# project library imports
import check_compendium as compendium

COVERAGE = Path("notes") / "coverage"
COVERAGE_VALUES = ("missing", "partial", "covered")
NEXT_ACTIONS = ("reuse", "extend", "write", "obtain-source", "review")
SLUG = r"[a-z0-9]+(?:-[a-z0-9]+)*"
TOPIC_ID = re.compile(r"^topic:" + SLUG + "$")
OBJECTIVE_ID = re.compile(r"^objective:" + SLUG + "$")
OUTLINE_ID = re.compile(r"^outline:[0-9a-f]{12,64}$")
MODULE_ID = re.compile(r"^(outline:[0-9a-f]{12,64}):m(\d{3})$")
ITEM_ID = re.compile(r"^(outline:[0-9a-f]{12,64}:m\d{3}):b(\d{2})$")
REVIEW_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PROHIBITED = "cfa"  # provider token kept out of maintained names; allowed in provenance values


def load_json(root, name, problems):
    """Load one coverage file, reporting a missing, invalid or unversioned file."""
    path = root / COVERAGE / name
    try:
        data = json.loads(path.read_text())
    except FileNotFoundError:
        problems.append(f"{(COVERAGE / name).as_posix()}: missing")
        return None
    except ValueError as exc:
        problems.append(f"{(COVERAGE / name).as_posix()}: not valid JSON ({exc})")
        return None
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        problems.append(f"{(COVERAGE / name).as_posix()}: expected an object with schema_version 1")
        return None
    return data


def records(data, field, where, problems):
    """Return a list-of-objects field, reporting it if it has another shape."""
    recs = data.get(field) if data else None
    if not isinstance(recs, list) or not all(isinstance(r, dict) for r in recs):
        if data is not None:
            problems.append(f"{where}: `{field}` must be a list of objects")
        return []
    return recs


def unique_ids(recs, pattern, where, problems):
    """Index records by id, reporting malformed and duplicate ids."""
    seen = {}
    for r in recs:
        rid = r.get("id")
        if not isinstance(rid, str) or not pattern.match(rid):
            problems.append(f"{where}: malformed id {rid!r}")
            continue
        if rid in seen:
            problems.append(f"{where}: duplicate id `{rid}`")
        seen[rid] = r
    return seen


def naming_problems(names, where):
    """Report maintained names that contain the prohibited provider token."""
    return [
        f"{where}: maintained name `{n}` contains the provider token"
        for n in names
        if isinstance(n, str) and PROHIBITED in n.lower()
    ]


def maintained_paths(root):
    """Return folders and files under the maintained trees.

    The ignored source copies and the guide submodule are not maintained trees.
    """
    out = []
    for top in ("compendium", "notes", "tools"):
        base = root / top
        if base.exists():
            out += [
                p.relative_to(root).as_posix()
                for p in base.rglob("*")
                if "__pycache__" not in p.parts
            ]
    return out


def python_names(root):
    """Function, class and variable names defined in tools/*.py."""
    # standard library imports
    import ast

    names = []
    for path in sorted((root / "tools").glob("*.py")):
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                names.append(node.name)
            elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                names.append(node.id)
            elif isinstance(node, ast.arg):
                names.append(node.arg)
    return names


def check_evidence(root, oid, o, entries, cite_keys, evidence, where, problems):
    """Structural consistency of a partial or covered objective's entries and evidence.

    Mapped labels must be typed entries; the objective's entry-evidence references must name
    exactly its mapped entries; each must have a nonempty record whose source file is the
    entry's file; every declared source must be known, located and cited by a mapped entry
    (sources read only for review go under review_sources); the review record must exist.
    """
    ev = o.get("evidence")
    if not isinstance(ev, dict):
        problems.append(f"{where}: `{oid}` is {o.get('coverage')} without an evidence record")
        return
    mapped = set(o.get("entries") or [])
    refs = ev.get("entry_evidence")
    if not isinstance(refs, list) or not refs or set(refs) != mapped:
        problems.append(
            f"{where}: `{oid}` entry-evidence references {refs!r} "
            f"do not match its mapped entries {sorted(mapped)}"
        )
    for label in sorted(mapped):
        rec = evidence.get(label)
        if (
            not isinstance(rec, dict)
            or not str(rec.get("source", "")).strip()
            or not str(rec.get("review", "")).strip()
        ):
            problems.append(
                f"{where}: `{oid}` maps `{label}`, which has no nonempty entry evidence"
            )
        elif label in entries and rec["source"] != entries[label]["file"]:
            problems.append(
                f"{where}: `{oid}` maps `{label}`, whose entry evidence names {rec['source']}, "
                f"not {entries[label]['file']}"
            )
    cited = (
        set().union(*(set(entries[lab]["cites"]) for lab in mapped if lab in entries))
        if mapped
        else set()
    )
    sources = ev.get("sources") or []
    if not sources:
        problems.append(f"{where}: `{oid}` is {o.get('coverage')} without a substantive source")
    for field, must_cite in (("sources", True), ("review_sources", False)):
        for src in ev.get(field) or []:
            key = src.get("key") if isinstance(src, dict) else None
            if key not in cite_keys:
                problems.append(f"{where}: `{oid}` {field} names unknown source key `{key}`")
            elif not src.get("locator"):
                problems.append(f"{where}: `{oid}` {field} names `{key}` without a locator")
            elif must_cite and key not in cited:
                problems.append(
                    f"{where}: `{oid}` source `{key}` is cited by none of its mapped entries"
                )
    record = ev.get("review_record") or ""
    if not record or not (root / record.split("#")[0]).exists():
        problems.append(
            f"{where}: `{oid}` is {o.get('coverage')} without an existing review record"
        )
    for note in ev.get("reading_notes") or []:
        if not (root / note).exists():
            problems.append(f"{where}: `{oid}` names missing reading note {note}")


def check_objectives(root, data, entries, cite_keys, evidence, sections, problems):
    """Validate topics and objectives and return them indexed by id."""
    where = (COVERAGE / "objectives.json").as_posix()
    topics = unique_ids(records(data, "topics", where, problems), TOPIC_ID, where, problems)
    objectives = unique_ids(
        records(data, "objectives", where, problems), OBJECTIVE_ID, where, problems
    )
    for tid, t in topics.items():
        if t.get("section") not in sections:
            problems.append(
                f"{where}: `{tid}` is owned by `{t.get('section')}`, "
                "not a section declared in compendium.tex"
            )
        for p in t.get("prerequisites", []):
            if p not in topics:
                problems.append(f"{where}: `{tid}` has unknown prerequisite `{p}`")
    for oid, o in objectives.items():
        if o.get("topic") not in topics:
            problems.append(f"{where}: `{oid}` has unknown topic `{o.get('topic')}`")
        for p in o.get("prerequisites", []):
            if p not in objectives and p not in topics:
                problems.append(f"{where}: `{oid}` has unknown prerequisite `{p}`")
        if o.get("supersedes") is not None and o["supersedes"] not in objectives:
            problems.append(f"{where}: `{oid}` supersedes unknown `{o['supersedes']}`")
        status, action = o.get("coverage"), o.get("next_action")
        if status not in COVERAGE_VALUES:
            problems.append(f"{where}: `{oid}` has invalid coverage {status!r}")
        if action is not None and action not in NEXT_ACTIONS:
            problems.append(f"{where}: `{oid}` has invalid next action {action!r}")
        if not isinstance(o.get("operations"), list) or not o.get("operations"):
            problems.append(f"{where}: `{oid}` lists no operations")
        for field in ("entries", "candidate_entries"):
            for label in o.get(field, []):
                if label not in entries:
                    problems.append(
                        f"{where}: `{oid}` {field} names `{label}`, "
                        "which is not a typed compendium entry"
                    )
        if status in ("missing", "partial"):
            if not o.get("missing"):
                problems.append(f"{where}: `{oid}` is {status} but records no missing requirement")
            if action is None:
                problems.append(f"{where}: `{oid}` is {status} but has no next action")
        if status in ("partial", "covered") and not o.get("entries"):
            problems.append(f"{where}: `{oid}` is {status} but maps no entry")
        if status == "covered" and o.get("missing"):
            problems.append(f"{where}: `{oid}` is covered but still records a missing requirement")
        if status == "covered" or (status == "partial" and o.get("evidence") is not None):
            check_evidence(root, oid, o, entries, cite_keys, evidence, where, problems)
    names = list(topics) + list(objectives)
    for o in objectives.values():
        ev = o.get("evidence") or {}
        names += [
            s.get("key")
            for f in ("sources", "review_sources")
            for s in (ev.get(f) or [])
            if isinstance(s, dict)
        ]
    problems += naming_problems(names, where)
    return topics, objectives


def check_crosswalk(root, manifest, crosswalk, objectives, problems):
    """Validate the manifest and crosswalk and reconcile occurrences with the manifest."""
    mwhere = (COVERAGE / "outline-manifest.json").as_posix()
    cwhere = (COVERAGE / "outline-crosswalk.json").as_posix()
    outlines = unique_ids(
        records(manifest, "outlines", mwhere, problems), OUTLINE_ID, mwhere, problems
    )
    for oid, rec in outlines.items():
        if not re.fullmatch(r"[0-9a-f]{64}", str(rec.get("sha256", ""))) or not rec[
            "sha256"
        ].startswith(oid.split(":")[1]):
            problems.append(
                f"{mwhere}: `{oid}` needs a full SHA-256 that starts with its id digits"
            )
        problems += naming_problems([rec.get("local_path")], mwhere)
    problems += naming_problems(list(outlines), mwhere)
    modules = unique_ids(
        records(crosswalk, "modules", cwhere, problems), MODULE_ID, cwhere, problems
    )
    items = unique_ids(records(crosswalk, "items", cwhere, problems), ITEM_ID, cwhere, problems)
    per_module = Counter()
    for mid, m in modules.items():
        if MODULE_ID.match(mid).group(1) not in outlines:
            problems.append(
                f"{cwhere}: module `{mid}` refers to an outline missing from the manifest"
            )
        for occ in m.get("occurrences", []):
            if occ.get("outline") not in outlines:
                problems.append(
                    f"{cwhere}: module `{mid}` has an occurrence in unknown `{occ.get('outline')}`"
                )
    for iid, it in items.items():
        mid = ITEM_ID.match(iid).group(1)
        if mid not in modules or it.get("module") != mid:
            problems.append(f"{cwhere}: item `{iid}` does not belong to a listed module")
        per_module[mid] += 1
        objs = it.get("objectives")
        if not isinstance(objs, list) or not objs:
            problems.append(f"{cwhere}: item `{iid}` maps to no objective")
            objs = []
        for o in objs:
            if o not in objectives:
                problems.append(f"{cwhere}: item `{iid}` maps to unknown `{o}`")
        if not it.get("command_verbs") or not it.get("paraphrase") or not it.get("rationale"):
            problems.append(
                f"{cwhere}: item `{iid}` needs a paraphrase, command verbs and a rationale"
            )
        for occ in it.get("occurrences", []):
            if (
                ITEM_ID.match(occ) is None
                or MODULE_ID.match(ITEM_ID.match(occ).group(1)).group(1) not in outlines
            ):
                problems.append(
                    f"{cwhere}: item `{iid}` has a malformed or unknown occurrence `{occ}`"
                )
    # Reconcile occurrences in each active source file with the manifest's independent counts:
    # a shared-core item is one crosswalk record but one occurrence in every file that prints it.
    active = {oid for oid, rec in outlines.items() if rec.get("role") == "scope-reference"}
    item_occ, module_occ = Counter(), Counter()
    for mid, m in modules.items():
        occ_outlines = [o.get("outline") for o in m.get("occurrences", [])]
        if MODULE_ID.match(mid).group(1) not in occ_outlines:
            problems.append(
                f"{cwhere}: module `{mid}` does not list its own outline among its occurrences"
            )
        if len(set(occ_outlines)) != len(occ_outlines):
            problems.append(f"{cwhere}: module `{mid}` repeats an occurrence")
        module_occ.update(occ_outlines)
    for iid, it in items.items():
        occ = it.get("occurrences", [])
        occ_outlines = [
            MODULE_ID.match(ITEM_ID.match(x).group(1)).group(1) for x in occ if ITEM_ID.match(x)
        ]
        if iid not in occ:
            problems.append(f"{cwhere}: item `{iid}` does not list itself among its occurrences")
        if len(set(occ_outlines)) != len(occ_outlines):
            problems.append(f"{cwhere}: item `{iid}` repeats an occurrence")
        mod = modules.get(it.get("module"), {})
        if set(occ_outlines) != {o.get("outline") for o in mod.get("occurrences", [])}:
            problems.append(f"{cwhere}: item `{iid}` occurrences differ from those of its module")
        item_occ.update(occ_outlines)
        if it.get("reviewed") is not None and not REVIEW_DATE.match(str(it["reviewed"])):
            problems.append(
                f"{cwhere}: item `{iid}` has a malformed review date {it['reviewed']!r}"
            )
    for oid in sorted(set(item_occ) | set(module_occ)):
        if oid not in active:
            problems.append(
                f"{cwhere}: occurrences name `{oid}`, "
                "which is not an active outline in the manifest"
            )
    for oid in sorted(active):
        rec = outlines[oid]
        if (module_occ[oid], item_occ[oid]) != (rec.get("modules"), rec.get("bullets")):
            problems.append(
                f"{cwhere}: `{oid}` has {module_occ[oid]} module / "
                f"{item_occ[oid]} item occurrences, "
                f"but the manifest declares {rec.get('modules')} / {rec.get('bullets')}"
            )
    for mid, m in modules.items():
        if m.get("bullets") != per_module[mid]:
            problems.append(
                f"{cwhere}: module `{mid}` declares {m.get('bullets')} bullets "
                f"but has {per_module[mid]} items"
            )
    scope = (crosswalk or {}).get("scope", {})
    if crosswalk is not None and (
        scope.get("modules") != len(modules) or scope.get("bullets") != len(items)
    ):
        problems.append(
            f"{cwhere}: scope declares {scope.get('modules')} modules / "
            f"{scope.get('bullets')} bullets, "
            f"but lists {len(modules)} / {len(items)}"
        )
    return outlines, modules, items


def item_status(item, objectives):
    """Return an outline item's coverage: missing, partial or covered.

    An outline item is covered only when its mapping has been reviewed, every mapped objective
    is covered and no residual gap remains. Covered objectives behind an unreviewed mapping give
    `partial`: the content exists, but nobody has checked that it meets this item.
    """
    states = [objectives[o].get("coverage") for o in item.get("objectives", []) if o in objectives]
    if (
        states
        and all(s == "covered" for s in states)
        and not item.get("residual_gap")
        and REVIEW_DATE.match(str(item.get("reviewed") or ""))
    ):
        return "covered"
    if any(s in ("covered", "partial") for s in states):
        return "partial"
    return "missing"


def verify_outlines(root, outlines, problems):
    """Hash each local outline copy and report missing or changed files."""
    for oid, rec in outlines.items():
        path = root / str(rec.get("local_path", ""))
        if not path.is_file():
            problems.append(
                f"source verification: `{oid}` local copy {rec.get('local_path')} is missing"
            )
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != rec.get("sha256"):
            problems.append(
                f"source verification: `{oid}` {rec.get('local_path')} has SHA-256 {digest}, "
                f"expected {rec.get('sha256')}"
            )


def report(root, verify=False):
    """Run every coverage check and return a JSON-serialisable report."""
    problems = []
    sections, _ = compendium.load_routes(root, problems)
    cite_keys = compendium.load_citation_keys(root)
    reached = compendium.reachable_files(root, sections, [])
    entries = {
        e["label"]: e
        for e in compendium.scan_entries(root, sections, cite_keys, [], reached)
        if e["label"]
    }
    evidence_path = root / "notes" / "entry-evidence.json"
    evidence = json.loads(evidence_path.read_text()) if evidence_path.exists() else {}
    obj_data = load_json(root, "objectives.json", problems)
    manifest = load_json(root, "outline-manifest.json", problems)
    crosswalk = load_json(root, "outline-crosswalk.json", problems)
    topics, objectives = check_objectives(
        root, obj_data, entries, cite_keys, evidence, sections, problems
    )
    outlines, modules, items = check_crosswalk(root, manifest, crosswalk, objectives, problems)
    problems += naming_problems(maintained_paths(root), "naming review")
    problems += naming_problems(sorted(set(python_names(root))), "naming review (tools/*.py)")
    problems += naming_problems(
        sorted(
            cite_keys
            - set(
                re.findall(
                    r"\\CatalogueEntry\{([^}]+)\}",
                    (
                        root / "guide" / "institutional_quantitative_finance_reading_list.tex"
                    ).read_text(),
                )
            )
        ),
        "naming review (source keys)",
    )
    problems += naming_problems(sorted(sections), "naming review (section keys)")
    if verify:
        verify_outlines(root, outlines, problems)

    by_section = defaultdict(Counter)
    for o in objectives.values():
        t = topics.get(o.get("topic"))
        by_section[t["section"] if t else "?"][o.get("coverage")] += 1
    component = {mid: m.get("component", "?") for mid, m in modules.items()}
    item_states = defaultdict(Counter)
    for iid, it in items.items():
        item_states[component.get(it.get("module"), "?")][item_status(it, objectives)] += 1
    return {
        "objectives": dict(Counter(o.get("coverage") for o in objectives.values())),
        "objectives_total": len(objectives),
        "topics_total": len(topics),
        "objectives_by_section": {k: dict(v) for k, v in sorted(by_section.items())},
        "next_actions": dict(Counter(str(o.get("next_action")) for o in objectives.values())),
        "outline_modules": len(modules),
        "outline_items": len(items),
        "outline_items_by_component": {k: dict(v) for k, v in sorted(item_states.items())},
        "outline_items_unreviewed": sum(1 for it in items.values() if not it.get("reviewed")),
        "outlines_verified": bool(
            verify and not any(p.startswith("source verification") for p in problems)
        ),
        "problems": problems,
    }


def print_report(r):
    """Print a report in human-readable form."""
    print(
        f"Objectives: {r['objectives_total']} in {r['topics_total']} topics  "
        + ", ".join(f"{k} {r['objectives'].get(k, 0)}" for k in COVERAGE_VALUES)
    )
    for sec, counts in r["objectives_by_section"].items():
        print(f"  {sec}: " + ", ".join(f"{k} {counts.get(k, 0)}" for k in COVERAGE_VALUES))
    print("Next actions: " + ", ".join(f"{k} {v}" for k, v in sorted(r["next_actions"].items())))
    print(
        f"Outline items (separate reconciliation): {r['outline_items']} "
        f"in {r['outline_modules']} modules, "
        f"{r['outline_items_unreviewed']} not yet reviewed"
    )
    for comp, counts in r["outline_items_by_component"].items():
        print(f"  {comp}: " + ", ".join(f"{k} {counts.get(k, 0)}" for k in COVERAGE_VALUES))
    print(f"Problems: {len(r['problems'])}")
    for p in r["problems"]:
        print("  - " + p)
    print(
        "Limits: structure and references only; "
        "not a judgement of teaching depth or of learner mastery."
    )


def main(argv=None):
    """Parse arguments, run the checks and return the process exit status."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    ap.add_argument("--json", action="store_true", help="print the report as JSON")
    ap.add_argument("--check", action="store_true", help="exit 1 when any problem is reported")
    ap.add_argument(
        "--verify-outlines",
        action="store_true",
        help="also hash the local outline copies; a missing or changed file is a problem",
    )
    args = ap.parse_args(argv)
    r = report(args.root.resolve(), verify=args.verify_outlines)
    if args.json:
        json.dump(r, sys.stdout, indent=1)
        print()
    else:
        print_report(r)
    return 1 if args.check and r["problems"] else 0


if __name__ == "__main__":
    sys.exit(main())
