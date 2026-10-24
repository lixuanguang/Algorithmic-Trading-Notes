"""Finite-difference option pricing and least-squares Monte Carlo, checked on BSM.

The checks are in trading_notes.numerical.numerical_pricing.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.numerical_pricing
(numpy, scipy). Exits 1 on failure. About 30 seconds.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.numerical_pricing import main

if __name__ == "__main__":
    sys.exit(main())
