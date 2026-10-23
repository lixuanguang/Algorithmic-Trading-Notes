"""Worked examples of def:return-measures, meth:instrument-present-value and related entries.

Batch 2 foundations, 2026-10-18, with the unit review and correction pass of 2026-10-23.
The checks, their conventions and the bisection contract are in
trading_notes.numerical.time_value_returns.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.time_value_returns
(standard library). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.time_value_returns import main

if __name__ == "__main__":
    sys.exit(main())
