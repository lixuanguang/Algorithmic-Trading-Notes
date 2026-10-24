"""Performance presentation standards: the worked GIPS examples.

The checks are in trading_notes.numerical.gips.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.gips (numpy). Exits 1 on
failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.gips import main

if __name__ == "__main__":
    sys.exit(main())
