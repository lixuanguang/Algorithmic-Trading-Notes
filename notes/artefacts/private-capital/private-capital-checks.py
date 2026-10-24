"""Private capital: the worked numbers of the private-capital allocator entries.

The checks are in trading_notes.numerical.private_capital.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.private_capital
(numpy, scipy). Exits 1 on failure.
"""

import sys

from trading_notes.numerical.private_capital import main

if __name__ == "__main__":
    sys.exit(main())
