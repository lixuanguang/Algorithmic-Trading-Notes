"""Check the subject coverage records and reconcile the external outline crosswalk.

Run from the repository root, or pass --root:
uv run --frozen --no-editable python -m trading_notes.cli.check_coverage
    [--check] [--verify-outlines] [--json] [--root DIR]
It exits 0, or 1 with --check when a problem is reported; a missing or malformed guide file
is reported on stderr with status 1, and argparse usage errors exit 2.
"""

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from trading_notes.structure.compendium import RepositoryInputError
from trading_notes.structure.coverage_check import COVERAGE_VALUES, CoverageReport, build_report

DESCRIPTION = "Check the subject coverage records and reconcile the external outline crosswalk."


def print_report(r: CoverageReport) -> None:
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


def main(argv: Sequence[str] | None = None) -> int:
    """Parse arguments, run the checks and return the process exit status."""
    ap = argparse.ArgumentParser(description=DESCRIPTION)
    ap.add_argument("--root", type=Path, default=Path.cwd())
    ap.add_argument("--json", action="store_true", help="print the report as JSON")
    ap.add_argument("--check", action="store_true", help="exit 1 when any problem is reported")
    ap.add_argument(
        "--verify-outlines",
        action="store_true",
        help="also hash the local outline copies; a missing or changed file is a problem",
    )
    args = ap.parse_args(argv)
    root: Path = args.root
    verify: bool = args.verify_outlines
    try:
        r = build_report(root.resolve(), verify=verify)
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
