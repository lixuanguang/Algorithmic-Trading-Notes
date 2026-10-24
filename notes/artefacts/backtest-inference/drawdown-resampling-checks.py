"""Own synthetic check behind meth:backtest-evaluation-diagnostics (drawdowns).

Source verification (2026-10-17): shuffled against stationary-type block bootstrap drawdowns on
an AR(1) model; a synthetic illustration, not a reading of Politis and Romano, whose paper was
not obtained. The comparison is in trading_notes.numerical.drawdown_resampling.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.drawdown_resampling
(numpy). Exits non-zero on failure.
"""

import sys

from trading_notes.numerical.drawdown_resampling import main

if __name__ == "__main__":
    sys.exit(main())
