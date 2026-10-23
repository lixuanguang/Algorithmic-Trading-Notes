"""Own, synthetic illustration behind meth:bitemporal-reference-tables.

Source verification, 2026-10-17. The split history, its actual-time and record-time
conventions and the checks are in trading_notes.numerical.bitemporal.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.bitemporal
(standard library). Exits non-zero on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.bitemporal import main

if __name__ == "__main__":
    sys.exit(main())
