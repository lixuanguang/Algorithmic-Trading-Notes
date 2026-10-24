"""The worked example of meth:monte-carlo-greeks.

The checks are in trading_notes.numerical.monte_carlo_greeks.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.monte_carlo_greeks
(numpy, scipy). Exits 1 on failure. About one second.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.monte_carlo_greeks import main

if __name__ == "__main__":
    sys.exit(main())
