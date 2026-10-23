"""Illustration behind mod:margin-liquidity-spiral (Brunnermeier and Pedersen, Proposition 5).

Source verification, 2026-10-17. The closed form, the independent loop series and the
illustrative inputs are in trading_notes.numerical.margin_spiral.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.margin_spiral
(standard library). Exits non-zero on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.margin_spiral import main

if __name__ == "__main__":
    sys.exit(main())
