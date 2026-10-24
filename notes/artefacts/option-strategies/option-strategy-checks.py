"""Option strategies: replication, covered calls, spreads, collars, skew and selection.

The checks are in trading_notes.numerical.option_strategies.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.option_strategies
(numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.option_strategies import main

if __name__ == "__main__":
    sys.exit(main())
