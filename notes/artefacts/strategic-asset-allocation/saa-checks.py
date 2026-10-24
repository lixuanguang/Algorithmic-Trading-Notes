"""Strategic asset allocation: the economic balance sheet, mean-variance, rebalancing and goals.

The checks are in trading_notes.numerical.strategic_asset_allocation.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.strategic_asset_allocation
(numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.strategic_asset_allocation import main

if __name__ == "__main__":
    sys.exit(main())
