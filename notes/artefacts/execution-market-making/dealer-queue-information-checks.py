"""Dealer queue information: quotes, arbitrage, queue values, inference and information review.

The checks are in trading_notes.numerical.dealer_queue_information.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.dealer_queue_information
(numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.dealer_queue_information import main

if __name__ == "__main__":
    sys.exit(main())
