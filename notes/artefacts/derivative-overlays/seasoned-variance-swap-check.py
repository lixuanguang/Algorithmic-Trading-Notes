"""The seasoned variance swap added to meth:volatility-derivative-applications.

The checks are in trading_notes.numerical.seasoned_variance_swap.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.seasoned_variance_swap
(numpy, scipy). Exits 1 on failure. About two seconds.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.seasoned_variance_swap import main

if __name__ == "__main__":
    sys.exit(main())
