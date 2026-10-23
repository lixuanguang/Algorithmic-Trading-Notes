"""When is the ERC portfolio the maximum-Sharpe portfolio? (meth:equal-risk-contribution).

Derivatives and empirical validation, 2026-10-17. The derivation, the counterexample and the
grid of positive, zero and negative Sharpe ratios are in trading_notes.numerical.erc_sharpe.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.erc_sharpe
(numpy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.erc_sharpe import main

if __name__ == "__main__":
    sys.exit(main())
