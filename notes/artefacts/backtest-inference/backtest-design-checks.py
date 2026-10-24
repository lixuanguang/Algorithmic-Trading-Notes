"""Backtest design: how survivorship, look-ahead, costs and search make performance from noise.

The checks are in trading_notes.numerical.backtest_design.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.backtest_design
(numpy). Exits 1 on failure.
"""

import sys

from trading_notes.numerical.backtest_design import main

if __name__ == "__main__":
    sys.exit(main())
