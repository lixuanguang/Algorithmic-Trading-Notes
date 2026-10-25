"""The regime map's inflation-shock row, classified on the middle-month monthly CPI vintages."""

import sys
from collections.abc import Sequence
from typing import Final

from trading_notes.research.macro_regimes_data.regime_inputs import (
    MONTHLY_CPI,
    RealTimeVintage,
    RowArguments,
)
from trading_notes.research.macro_regimes_data.vintage_signals import (
    ResponseDifference,
    VintageQuarters,
)

THRESHOLD: Final = 1.0  # a rise of the 12-month inflation rate over 12 months, in points
HEADER: Final = (
    "\nresponse   hypothesis   signal mean   other mean   difference   Welch t   NW t (4 lags)"
)
HYPOTHESES: Final = (("dy10", "> 0"), ("dslope", "> 0"), ("oil", "> 0"))


def print_verdict(diffs: dict[str, ResponseDifference]) -> None:
    """Print the verdict on each response: supported if positive with Welch |t| > 2."""
    supported = {k: d.difference > 0 and abs(d.welch_t) > 2 for k, d in diffs.items()}
    print(
        "\nVerdict (Welch |t| > 2, hypothesised sign): "
        + "; ".join(f"{k} {'supported' if v else 'not supported'}" for k, v in supported.items())
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Print the inflation row's results and write inflation_monthly_vintage_quarters.csv.

    The test of ev:regime-asset-responses-tested under inflation-row-protocol.md, on the
    Philadelphia Fed's monthly CPI vintages (pcpiMvMd.xlsx), the middle-month vintage of each
    quarter standing for the quarterly one: with L the last month reported, the signal is
    pi(L) - pi(L - 12) >= 1.0 point; responses over m + 1..m + 3 are dy10, dslope (GS10 less
    the 3-month bill) and oil (Cushing WTI spot), each supported if positive with Welch
    |t| > 2. Kept as a timing sensitivity to the quarterly-vintage test.

    Returns:
        0.
    """
    args = RowArguments.parse(RowArguments.parser(__doc__ or ""), argv)
    responses = args.responses()
    vintages = list(RealTimeVintage.read_all(args.materials / MONTHLY_CPI, "pcpi", "PCPI", False))
    quarters = VintageQuarters.of(vintages, responses, THRESHOLD, deflation=False, incomplete="")
    quarters.write(args.output_folder / "inflation_monthly_vintage_quarters.csv")
    print(f"{quarters.used()}; skipped: {', '.join(quarters.skipped) or 'none'}")
    print(quarters.signal_summary())
    print_verdict(quarters.print_responses(HEADER, HYPOTHESES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
