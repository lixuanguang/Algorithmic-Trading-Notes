"""The worked examples of meth:transaction-cost-hedging.

The checks are in trading_notes.numerical.transaction_cost_hedging.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.transaction_cost_hedging
(numpy, scipy). Exits 1 on failure. About 20 seconds.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.transaction_cost_hedging import main

if __name__ == "__main__":
    sys.exit(main())
