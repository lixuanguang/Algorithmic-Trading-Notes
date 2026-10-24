"""Institutional portfolios: pension risk, endowment law, sovereign funds, liquidity and ESG.

The checks are in trading_notes.numerical.institutional_portfolios.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.institutional_portfolios
(numpy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.institutional_portfolios import main

if __name__ == "__main__":
    sys.exit(main())
