"""Manager selection: the worked numbers of three manager-selection entries.

The checks are in trading_notes.numerical.manager_selection.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.manager_selection
(numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.manager_selection import main

if __name__ == "__main__":
    sys.exit(main())
