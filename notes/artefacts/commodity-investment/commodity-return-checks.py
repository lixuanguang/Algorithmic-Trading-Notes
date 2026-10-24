"""Commodity investment: return components, roll yield, diversification return, swaps, indices.

The checks are in trading_notes.numerical.commodity_returns.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.commodity_returns (numpy).
Exits 1 on failure.
"""

import sys

from trading_notes.numerical.commodity_returns import main

if __name__ == "__main__":
    sys.exit(main())
