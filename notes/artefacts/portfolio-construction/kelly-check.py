"""Kelly growth: the optimal fraction, half Kelly, daily rebalancing and estimation error.

The checks are in trading_notes.numerical.kelly_growth.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.kelly_growth
(numpy, scipy). Exits 1 on failure. About 5 seconds.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.kelly_growth import main

if __name__ == "__main__":
    sys.exit(main())
