"""Private wealth: human capital, taxes, planning, retirement, protection and transfers.

The checks are in trading_notes.numerical.private_wealth.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.private_wealth
(numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.private_wealth import main

if __name__ == "__main__":
    sys.exit(main())
