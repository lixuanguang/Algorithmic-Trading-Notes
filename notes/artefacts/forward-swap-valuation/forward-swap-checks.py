"""Forward and swap valuation: the worked numbers of six entries, from payoffs to swaps.

The checks are in trading_notes.numerical.forward_swap_valuation.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.forward_swap_valuation
(numpy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.forward_swap_valuation import main

if __name__ == "__main__":
    sys.exit(main())
