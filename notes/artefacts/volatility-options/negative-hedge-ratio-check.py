"""A negative minimum-variance hedge ratio reduces variance (mod:minimum-variance-hedge-ratio).

Financial data and labels review follow-up check (2026-10-16). The analytical, covariance and
grid-search calculations are in trading_notes.numerical.negative_hedge_ratio.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.negative_hedge_ratio
(numpy). Prints its values and exits 0; it asserts nothing.
"""

import sys

from trading_notes.numerical.negative_hedge_ratio import main

if __name__ == "__main__":
    sys.exit(main())
