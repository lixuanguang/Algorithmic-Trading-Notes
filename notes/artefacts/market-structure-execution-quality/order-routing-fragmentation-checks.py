"""Order routing and fragmentation: auctions, pro-rata fills, posting, venue shares, SOR learning.

The checks are in trading_notes.numerical.order_routing_fragmentation.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.order_routing_fragmentation
(numpy, scipy; fixed seeds; a few seconds). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.order_routing_fragmentation import main

if __name__ == "__main__":
    sys.exit(main())
