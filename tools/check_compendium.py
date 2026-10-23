#!/usr/bin/env python3
"""Check compendium entries, citation keys, labels and pathway links.

Run: uv run python tools/check_compendium.py [--check] [--json] [--root DIR]
(`make check-compendium` runs it with --check).

The checks are trading_notes.structure.compendium_check; this script parses arguments,
prints the report and sets the exit status: 0, or 1 with --check when a problem is
reported. A missing or malformed required guide file is reported on stderr with exit
status 1 whether or not --check is given; argparse usage errors exit 2.
"""

# standard library imports
import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

# project library imports
from trading_notes.structure.compendium import RepositoryInputError
from trading_notes.structure.compendium_check import CompendiumReport, build_report

DESCRIPTION = "Check compendium entries, citation keys, labels and pathway links."


def print_report(r: CompendiumReport) -> None:
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
    print(
        f"Pathways rendered: {sum(len(v) for v in r['pathways_rendered'].values())}  "
        f"pathway notes: {len(r['pathways'])}"
    )
    print(f"Problems: {len(r['problems'])}")
    for problem in r["problems"]:
        print("  - " + problem)
    print("Limits: this checks structure and references, not the truth of claims.")


def main(argv: Sequence[str] | None = None) -> int:
    """Parse arguments, run the checks and return the process exit status."""
    ap = argparse.ArgumentParser(description=DESCRIPTION)
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    ap.add_argument("--json", action="store_true", help="print the report as JSON")
    ap.add_argument("--check", action="store_true", help="exit 1 when any problem is reported")
    args = ap.parse_args(argv)
    root: Path = args.root
    try:
        r = build_report(root.resolve())
    except RepositoryInputError as exc:
        print(f"{ap.prog}: error: {exc}", file=sys.stderr)
        return 1
    if args.json:
        json.dump(r, sys.stdout, indent=1)
        print()
    else:
        print_report(r)
    return 1 if args.check and r["problems"] else 0


if __name__ == "__main__":
    sys.exit(main())
