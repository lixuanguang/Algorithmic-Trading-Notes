"""Own checks behind the covariance, noise and volatility-loss passages.

The checks are in trading_notes.numerical.covariance_volatility.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.covariance_volatility
(numpy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.covariance_volatility import main

if __name__ == "__main__":
    sys.exit(main())
