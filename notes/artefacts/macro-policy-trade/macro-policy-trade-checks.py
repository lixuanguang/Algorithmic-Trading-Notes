"""Business cycles, policy, trade and geopolitical risk: the worked numbers of eight entries.

The checks are in trading_notes.numerical.macro_policy_trade.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.macro_policy_trade
(numpy, scipy). Exits 1 on failure.
"""

import sys

from trading_notes.numerical.macro_policy_trade import main

if __name__ == "__main__":
    sys.exit(main())
