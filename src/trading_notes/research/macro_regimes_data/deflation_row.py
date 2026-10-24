"""The regime map's deflation or disinflation row, tested on the quarterly CPI vintages."""

import sys
from collections.abc import Sequence
from pathlib import Path
from typing import ClassVar, Final

from trading_notes.research.macro_regimes_data.regime_inputs import (
    QUARTERLY_CPI,
    MonthlyResponses,
    RealTimeVintage,
)
from trading_notes.research.macro_regimes_data.vintage_signals import VintageQuarters
from trading_notes.research.workflow import WorkflowArguments

THRESHOLD: Final = -1.0  # a fall of the 12-month inflation rate over 12 months, in points
HEADER: Final = (
    "\nresponse   role          signal mean   other mean   difference   Welch t   NW t (4 lags)"
)


class Arguments(WorkflowArguments):
    """The deflation row's arguments.

    Attributes:
        materials: The reading-materials root that holds the vintage, GS10 and oil files.
    """

    folder: ClassVar[str] = "macro-regimes-stock-bond"
    materials: Path


def main(argv: Sequence[str] | None = None) -> int:
    """Print the deflation row's results and write deflation_quarters.csv.

    The test of ev:regime-asset-responses-tested under deflation-row-protocol.md: in the
    vintage dated in the quarter's middle month m, the signal is pi(L) - pi(L - 12) <= -1.0
    point; the hypothesis dy10 = GS10(m + 3) - GS10(m) < 0, supported if the signal-minus-other
    difference is negative with Welch |t| > 2. Alongside: a Newey-West t (4 lags), the
    episodes, and the slope and WTI responses of the inflation row.

    Returns:
        0.
    """
    parser = Arguments.parser(__doc__ or "")
    parser.add_argument("materials", type=Path, help="the reading-materials root")
    args = Arguments.parse(parser, argv)
    responses = MonthlyResponses.read(args.materials, args.root)
    vintages = list(RealTimeVintage.read_all(args.materials / QUARTERLY_CPI, "cpi", "CPI", True))
    quarters = VintageQuarters.of(vintages, responses, THRESHOLD, deflation=True)
    quarters.write(args.output_folder / "deflation_quarters.csv")
    print("Deflation / disinflation row, quarterly CPI vintages (cpiQvMd.xlsx)")
    print(f"{quarters.used()}; skipped: {len(quarters.skipped)}")
    print(quarters.signal_summary())
    dy10 = quarters.print_responses(
        HEADER, (("dy10", "H: < 0"), ("dslope", "alongside"), ("oil", "alongside"))
    )["dy10"]
    verdict = dy10.difference < 0 and abs(dy10.welch_t) > 2
    print(f"\nVerdict (dy10 < 0 with Welch |t| > 2): {'supported' if verdict else 'not supported'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
