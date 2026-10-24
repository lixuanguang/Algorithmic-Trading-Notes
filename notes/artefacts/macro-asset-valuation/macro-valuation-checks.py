"""The economy and asset values: worked numbers of three macro valuation entries.

The checks are in trading_notes.numerical.macro_valuation.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.macro_valuation
(numpy, scipy). Exits 1 on failure.
"""

import sys

from trading_notes.numerical.macro_valuation import main

if __name__ == "__main__":
    sys.exit(main())
