"""The worked example of rule:counterparty-credit-cva-capital.

The checks are in trading_notes.numerical.counterparty_capital.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.counterparty_capital
(scipy). Exits 1 on failure.
"""

import sys

from trading_notes.numerical.counterparty_capital import main

if __name__ == "__main__":
    sys.exit(main())
