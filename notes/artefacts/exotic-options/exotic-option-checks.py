"""Exotic options: digital, barrier and Asian option closed forms against Monte Carlo.

The checks are in trading_notes.numerical.exotic_options.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.exotic_options
(numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.exotic_options import main

if __name__ == "__main__":
    sys.exit(main())
