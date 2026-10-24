"""Conditions behind meth:sharpe-ratio-standard-error.

The checks are in trading_notes.numerical.sharpe_conditions.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.sharpe_conditions
(numpy; about 2 s). Exits non-zero on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.sharpe_conditions import main

if __name__ == "__main__":
    sys.exit(main())
