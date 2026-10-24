"""Portfolio return moments and diversification: the worked examples of two entries.

The checks are in trading_notes.numerical.portfolio_moments.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.portfolio_moments
(numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.portfolio_moments import main

if __name__ == "__main__":
    sys.exit(main())
