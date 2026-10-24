"""Equity portfolio management: indexing, active strategies, active risk and capacity.

The checks are in trading_notes.numerical.equity_portfolio_management.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.equity_portfolio_management
(numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.equity_portfolio_management import main

if __name__ == "__main__":
    sys.exit(main())
