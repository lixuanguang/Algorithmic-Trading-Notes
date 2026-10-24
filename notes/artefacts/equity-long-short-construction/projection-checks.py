"""Best linear projection against conditional expectation, behind meth:forecast-scaling-ic.

Source verification (2026-10-17) (audit repair): a zero-IC example with predictive information,
orthogonality without mean independence, and projection equal to the conditional mean under
joint normality. The checks are in trading_notes.numerical.linear_projection.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.linear_projection
(numpy). Exits non-zero on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.linear_projection import main

if __name__ == "__main__":
    sys.exit(main())
