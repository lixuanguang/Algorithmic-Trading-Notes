"""Option valuation: value drivers, parity, binomial trees, Black's model, Greeks and hedging.

The checks are in trading_notes.numerical.option_valuation.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.option_valuation
(numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.option_valuation import main

if __name__ == "__main__":
    sys.exit(main())
