"""Derivative overlays for portfolio exposures: the worked numbers of four overlay entries.

The checks are in trading_notes.numerical.derivative_overlays.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.derivative_overlays
(numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.derivative_overlays import main

if __name__ == "__main__":
    sys.exit(main())
