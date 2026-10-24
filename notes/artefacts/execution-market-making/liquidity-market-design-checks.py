"""Liquidity and market design: skill and luck, depth and width, search, capacity and externalities.

The checks are in trading_notes.numerical.liquidity_market_design.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.liquidity_market_design
(numpy). Exits 1 on failure.
"""

import sys

from trading_notes.numerical.liquidity_market_design import main

if __name__ == "__main__":
    sys.exit(main())
