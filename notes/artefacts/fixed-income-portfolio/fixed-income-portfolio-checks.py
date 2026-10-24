"""Fixed-income portfolio management: the worked numbers of seven entries.

The checks are in trading_notes.numerical.fixed_income_portfolio.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.fixed_income_portfolio
(numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.fixed_income_portfolio import main

if __name__ == "__main__":
    sys.exit(main())
