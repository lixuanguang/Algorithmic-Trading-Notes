"""Currency management: the worked numbers of four currency entries.

The checks are in trading_notes.numerical.currency_management.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.currency_management
(numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.currency_management import main

if __name__ == "__main__":
    sys.exit(main())
