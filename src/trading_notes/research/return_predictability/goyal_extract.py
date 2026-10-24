"""Extract the annual and monthly S&P 500 series of the return-predictability checks."""

import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Final

from trading_notes.research.return_predictability.goyal_workbook import GoyalArguments

# Index level, trailing 12-month dividends, the risk-free return over the period and the CRSP
# value-weighted S&P 500 return (from 1926), as printed in the workbook.
KEEP: Final = ["Index", "D12", "Rfree", "CRSP_SPvw"]


def main(argv: Sequence[str] | None = None) -> int:
    """Write goyal-annual-1871-2025.csv and goyal-monthly-1871-2025.csv; exit 1 on a hash mismatch.

    The checks derive returns, the dividend-price ratio and excess returns from these
    columns. Despite its label, the workbook runs to December 2025: it is the 2026 vintage
    of the series, not the file behind Welch and Goyal's 2008 tables.

    Returns:
        0, or 1 when the workbook is not the recorded download.
    """
    parser = GoyalArguments.parser(__doc__ or "")
    parser.add_argument("workbook", type=Path, help="PredictorData2005_original.xlsx")
    args = GoyalArguments.parse(parser, argv)
    return args.extract(
        [
            ("goyal-annual-1871-2025.csv", "Annual", "yyyy"),
            ("goyal-monthly-1871-2025.csv", "Monthly", "yyyymm"),
        ],
        KEEP,
    )


if __name__ == "__main__":
    sys.exit(main())
