"""Global macro in equity down months, January 2014 to July 2026, from the index workbook."""

import sys
from collections.abc import Sequence
from pathlib import Path
from typing import ClassVar, Final

from trading_notes.data_folders import DataFolder
from trading_notes.research.global_macro.index_returns import (
    IndexMonths,
    IndexWorkbook,
    french_factors,
)
from trading_notes.research.workflow import WorkflowArguments

START: Final = (2014, 1)
END: Final = (2026, 7)
RECENT: Final = (2022, 1)
# The workbook retrieved from BarclayHedge's public Excel form on 2026-10-17 07:58 UTC.
WORKBOOK_SHA256: Final = "ead890c4274a7cdd7f92e3da23d15dbd0359dd239bf6a3841cddf437853d1097"


def report(label: str, data: IndexMonths) -> None:
    """Print one window's statistics and its verdict under the pre-set rule."""
    print(f"{label}: window {data.span()}, T = {len(data.months)} months")
    print(f"  all months: {data.all_months()}")
    print("  " + data.down().describe("down", 4))
    print("  " + data.up().describe("up", 4))
    print("  " + data.worst("stable"))
    print(f"  verdict (pre-set rule): {data.verdict()}")


class Arguments(WorkflowArguments):
    """The 2014 down-months test's arguments.

    Attributes:
        workbook: The Barclay Global Macro Index workbook (.xls).
        factors: Ken French's factors CSV.
        page_months: A generated global_macro_monthly.csv, or a run folder holding one, to read
            instead of the retained file.
    """

    folder: ClassVar[DataFolder] = DataFolder(subsection="global_macro")
    workbook: Path
    factors: Path
    page_months: Path | None = None


def main(argv: Sequence[str] | None = None) -> int:
    """Print the protocol window and the recent comparison; write global_macro_monthly_2014.csv.

    The protocol for ev:global-macro-returns-after-2013 on its own window, January 2014 to
    July 2026 inclusive, on the index workbook from BarclayHedge's public Excel form; months
    marked as estimated (cells with '*' notes) are excluded and none may fall in the window.
    Statistics and the pre-set verdict are those of `down_months`, the index-page workflow.
    Diagnostics, not part of the verdict: the same statistics on 2022-01..2026-07 from the
    workbook, and a comparison with the index page's values (the retained
    global_macro_monthly.csv unless --page-months names a generated one) to detect revisions.
    Every figure is as of the retrieval time: constituents and past values change.

    Returns:
        0.

    Raises:
        ValueError: If a window month is estimated or missing from the inputs.
    """
    parser = Arguments.parser(__doc__ or "")
    parser.add_argument("workbook", type=Path, help="the index workbook (.xls)")
    parser.add_argument("factors", type=Path, help="Ken French's factors CSV")
    parser.add_argument(
        "--page-months", type=Path, default=None, help="a generated page table or run folder"
    )
    args = Arguments.parse(parser, argv)
    page_months = args.upstream(args.page_months, args.folder.results / "global_macro_monthly.csv")
    book = IndexWorkbook.read(args.workbook)
    matches = "matches" if book.sha256 == WORKBOOK_SHA256 else "DIFFERS FROM"
    print(f"workbook SHA-256 {book.sha256} ({matches} the recorded snapshot)")
    print(
        f"estimated months excluded: {', '.join(f'{y}-{m:02d}' for y, m in sorted(book.estimated))}"
    )
    data = book.window(french_factors(args.factors), START, END)
    data.write(args.output_folder / "global_macro_monthly_2014.csv")
    report("Protocol window (Barclay Global Macro Index workbook, net; French Mkt-RF)", data)
    report("Recent-period comparison from the workbook", data.since(RECENT))
    page = IndexMonths.read(page_months).returns_by_month()
    diffs = book.revisions(page)
    print(
        f"revision check against the index page's values of 2026-10-17 ({len(page)} months, 4"
        f" decimals): {len(diffs)} months differ"
        + (
            ": " + "; ".join(f"{m[0]}-{m[1]:02d} {a:+.4f} -> {b:+.4f}" for m, a, b in diffs)
            if diffs
            else ""
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
