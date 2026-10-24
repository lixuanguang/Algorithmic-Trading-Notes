"""Order flow: spreads, imbalance, trade signing, noise, Epps, Hawkes and waiting times.

The checks are in trading_notes.numerical.order_flow.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.order_flow
(numpy, scipy; fixed seeds; about 20 s). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.order_flow import main

if __name__ == "__main__":
    sys.exit(main())
