"""Checks behind meth:forecast-scaling-ic.

The checks are in trading_notes.numerical.forecast_scaling.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.forecast_scaling
(numpy, scipy). Exits non-zero on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.forecast_scaling import main

if __name__ == "__main__":
    sys.exit(main())
