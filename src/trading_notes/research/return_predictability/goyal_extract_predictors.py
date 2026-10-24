"""Extract the annual predictor columns of the forecast-combination and conditional checks."""

import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Final

from trading_notes.research.return_predictability.goyal_workbook import GoyalArguments

# Index level, trailing 12-month dividends and earnings, the 3-month bill, Moody's AAA and BAA
# yields, the long-term government yield, the risk-free return and the CRSP return.
KEEP: Final = ["Index", "D12", "E12", "tbl", "AAA", "BAA", "lty", "Rfree", "CRSP_SPvw"]


def main(argv: Sequence[str] | None = None) -> int:
    """Write goyal-annual-predictors-1871-2025.csv; exit 1 on a hash mismatch.

    The checks derive the log equity premium and the four predictors from these columns of
    the Annual sheet.

    Returns:
        0, or 1 when the workbook is not the recorded download.
    """
    parser = GoyalArguments.parser(__doc__ or "")
    parser.add_argument("workbook", type=Path, help="PredictorData2005_original.xlsx")
    args = GoyalArguments.parse(parser, argv)
    return args.extract([("goyal-annual-predictors-1871-2025.csv", "Annual", "yyyy")], KEEP)


if __name__ == "__main__":
    sys.exit(main())
