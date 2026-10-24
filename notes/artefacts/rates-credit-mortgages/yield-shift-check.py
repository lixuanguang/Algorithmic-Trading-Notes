"""Yield change against a parallel zero-curve shift.

The demonstration is in trading_notes.numerical.yield_shift.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.yield_shift (numpy, scipy).
"""

import sys

from trading_notes.numerical.yield_shift import main

if __name__ == "__main__":
    sys.exit(main())
