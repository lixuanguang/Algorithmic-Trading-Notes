"""Delta hedging at the wrong volatility, and the vanna and volga formulas.

The checks are in trading_notes.numerical.volatility_mismatch_hedging.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.volatility_mismatch_hedging
(numpy, scipy). Exits 1 on failure. About 10 seconds.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.volatility_mismatch_hedging import main

if __name__ == "__main__":
    sys.exit(main())
