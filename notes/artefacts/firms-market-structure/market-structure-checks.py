"""Firms and market structure: cost and output decisions, oligopoly outcomes and concentration.

The checks are in trading_notes.numerical.market_structure.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.market_structure
(numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.market_structure import main

if __name__ == "__main__":
    sys.exit(main())
