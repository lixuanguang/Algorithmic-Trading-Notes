"""Trading costs and trade execution: worked numbers of five execution entries.

The checks are in trading_notes.numerical.trade_execution.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.trade_execution
(numpy, scipy). Exits 1 on failure.
"""

import sys

from trading_notes.numerical.trade_execution import main

if __name__ == "__main__":
    sys.exit(main())
