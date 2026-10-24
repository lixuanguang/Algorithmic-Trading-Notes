"""Credit portfolios: spread risk and DTS, selection, liquidity and tail risk, CDS and structures.

The checks are in trading_notes.numerical.credit_portfolios.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.credit_portfolios
(numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.credit_portfolios import main

if __name__ == "__main__":
    sys.exit(main())
