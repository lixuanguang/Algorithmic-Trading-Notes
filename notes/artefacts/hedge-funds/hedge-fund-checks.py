"""Hedge funds: exposures, fee layers, strategy arithmetic and the effect of an allocation.

The checks are in trading_notes.numerical.hedge_funds.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.hedge_funds (numpy).
Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.hedge_funds import main

if __name__ == "__main__":
    sys.exit(main())
