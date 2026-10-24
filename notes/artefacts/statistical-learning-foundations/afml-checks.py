"""Financial data and labels: toy calculations behind the AFML data-cluster entries.

The calculations are in trading_notes.numerical.afml.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.afml (numpy, statsmodels).
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.afml import main

if __name__ == "__main__":
    sys.exit(main())
