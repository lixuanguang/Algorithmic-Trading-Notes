"""Allocating to alternatives: roles, risk mitigation, opportunity sets, pacing and liquidity.

The checks are in trading_notes.numerical.alternatives_allocation.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.alternatives_allocation
(numpy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.alternatives_allocation import main

if __name__ == "__main__":
    sys.exit(main())
