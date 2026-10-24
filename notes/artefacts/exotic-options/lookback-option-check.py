"""Lookback options: Hull's and Wilmott's closed forms, seasoned simulation and monitoring bias.

The checks are in trading_notes.numerical.lookback_options.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.lookback_options
(numpy, scipy). Exits 1 on failure. About 15 seconds.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.lookback_options import main

if __name__ == "__main__":
    sys.exit(main())
