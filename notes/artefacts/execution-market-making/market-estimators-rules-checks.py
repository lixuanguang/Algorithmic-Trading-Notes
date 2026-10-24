"""Market estimators and rules: refresh time, batch auctions, Model I, tick tables and platinum.

The checks are in trading_notes.numerical.market_estimators_rules.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.market_estimators_rules
(numpy; fixed seeds; a few seconds). Exits 1 on failure.
"""

import sys

from trading_notes.numerical.market_estimators_rules import main

if __name__ == "__main__":
    sys.exit(main())
