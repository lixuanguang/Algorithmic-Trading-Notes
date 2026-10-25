"""The regime map's deflation or disinflation row, tested on the quarterly CPI vintages."""

import sys
from collections.abc import Sequence
from typing import Final

from trading_notes.research.macro_regimes_data.regime_inputs import (
    QUARTERLY_CPI,
    RealTimeVintage,
    RowArguments,
)
from trading_notes.research.macro_regimes_data.vintage_signals import VintageQuarters

THRESHOLD: Final = -1.0  # a fall of the 12-month inflation rate over 12 months, in points
HEADER: Final = (
    "\nresponse   role          signal mean   other mean   difference   Welch t   NW t (4 lags)"
)


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
    args = RowArguments.parse(RowArguments.parser(__doc__ or ""), argv)
    responses = args.responses()
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
