"""Own simulation behind meth:portfolio-covariance-estimation.

Source verification (2026-10-17) of Ledoit and Wolf's oracle linear shrinkage. The simulation
and its three conditions are in trading_notes.numerical.covariance_shrinkage.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.covariance_shrinkage
(numpy). Exits non-zero on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.covariance_shrinkage import main

if __name__ == "__main__":
    sys.exit(main())
