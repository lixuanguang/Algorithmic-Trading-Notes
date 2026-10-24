"""Checks behind the market-making model statements.

The checks are in trading_notes.numerical.lob_models.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.lob_models
(numpy and scipy). Exits non-zero on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.lob_models import main

if __name__ == "__main__":
    sys.exit(main())
