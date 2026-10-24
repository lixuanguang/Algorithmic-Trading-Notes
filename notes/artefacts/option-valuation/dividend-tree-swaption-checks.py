"""Known dividends in a binomial tree, and the receiver swaption behind a callable bond.

The checks are in trading_notes.numerical.dividend_tree_swaption.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.dividend_tree_swaption
(numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.dividend_tree_swaption import main

if __name__ == "__main__":
    sys.exit(main())
