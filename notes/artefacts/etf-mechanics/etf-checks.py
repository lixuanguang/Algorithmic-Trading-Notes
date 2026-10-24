"""ETFs: market-maker quotes, premiums and discounts, the 6c-11 spread, tracking and costs.

The checks are in trading_notes.numerical.etf_mechanics.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.etf_mechanics (numpy).
Exits 1 on failure.
"""

import sys

from trading_notes.numerical.etf_mechanics import main

if __name__ == "__main__":
    sys.exit(main())
