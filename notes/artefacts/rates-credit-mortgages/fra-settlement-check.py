"""Settlement conventions behind mod:multi-curve-fra-swap-valuation.

Derivatives and empirical validation, 2026-10-17. The checks, their derivation and sources
are in trading_notes.numerical.fra_settlement.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.fra_settlement
(standard library; exits 1 on failure).
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.fra_settlement import main

if __name__ == "__main__":
    sys.exit(main())
