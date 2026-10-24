"""Gaussian copula default correlation: tranche losses, base correlations and compound correlations.

The checks are in trading_notes.numerical.default_correlation.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.default_correlation
(numpy, scipy). Exits 1 on failure. About 30 seconds: the base-correlation solves of part 3 take
nearly all of it.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.default_correlation import main

if __name__ == "__main__":
    sys.exit(main())
