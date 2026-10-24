"""Global macro in equity down months, January 2022 to July 2026, from BarclayHedge's index page."""

import sys
from collections.abc import Sequence
from pathlib import Path
from typing import ClassVar, Final

from trading_notes.research.global_macro.index_returns import (
    IndexMonths,
    barclay_page,
    french_factors,
)
from trading_notes.research.workflow import WorkflowArguments

# The last complete month with French data; August and September 2026 are estimates.
LAST_MONTH: Final = (2026, 7)


class Arguments(WorkflowArguments):
    """The down-months test's arguments.

    Attributes:
        page: The saved BarclayHedge index page (HTML).
        factors: Ken French's factors CSV.
    """

    folder: ClassVar[str] = "multi-asset-systematic-macro"
    page: Path
    factors: Path


def main(argv: Sequence[str] | None = None) -> int:
    """Print the down- and up-month statistics and write global_macro_monthly.csv.

    The bounded run of the protocol for ev:global-macro-returns-after-2013: does a named macro
    hedge-fund index show positive returns and low or negative co-movement with equities in
    equity down months? Series: the Barclay Global Macro Index's monthly net returns as shown
    on BarclayHedge's public page on 2026-10-17 (January 2022 onward), estimated months
    excluded; benchmark Ken French's Mkt-RF, down months those below zero; index excess
    return = index - RF, Sharpe with Lo's IID standard error; correlation intervals by
    Fisher z, beta and means by OLS and t (independence assumed); the ten lowest Mkt-RF
    months. Crisis protection only if the down-month mean is positive with t > 2. This window
    is not the protocol's 2014-2026 one.

    Returns:
        0.
    """
    parser = Arguments.parser(__doc__ or "")
    parser.add_argument("page", type=Path, help="the BarclayHedge index page (HTML)")
    parser.add_argument("factors", type=Path, help="Ken French's factors CSV")
    args = Arguments.parse(parser, argv)
    idx, ff = barclay_page(args.page), french_factors(args.factors)
    data = IndexMonths.of(sorted(m for m in idx if m in ff and m <= LAST_MONTH), idx, ff)
    data.write(args.output_folder / "global_macro_monthly.csv")
    print(
        f"Window {data.months[0]} to {data.months[-1]}, T = {len(data.months)} months (Barclay"
        " Global Macro Index, net; French Mkt-RF)"
    )
    print(f"All months: {data.all_months()}")
    print(data.down().describe("down", 2))
    print(data.up().describe("up", 2))
    print(data.worst("quicksort"))
    print(f"Verdict (pre-set rule): {data.verdict()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
