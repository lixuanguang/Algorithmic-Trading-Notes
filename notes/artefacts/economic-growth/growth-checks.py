"""Economic growth: the worked numbers of four growth entries.

The checks are in trading_notes.numerical.economic_growth.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.economic_growth
(numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.economic_growth import main

if __name__ == "__main__":
    sys.exit(main())
