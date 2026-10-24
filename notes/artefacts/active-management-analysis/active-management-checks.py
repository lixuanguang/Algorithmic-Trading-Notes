"""Active management: the worked examples of three active-management entries.

The checks are in trading_notes.numerical.active_management.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.active_management
(numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.active_management import main

if __name__ == "__main__":
    sys.exit(main())
