"""CME Globex allocation steps reproduced on the matching-algorithm page's own examples.

Source verification, 2026-10-17. The source version, the Pro Rata, Leveling, Split and FIFO
rules and the expected allocations are in trading_notes.numerical.cme_allocation.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.cme_allocation
(standard library). Exits non-zero on failure.
"""

import sys

from trading_notes.numerical.cme_allocation import main

if __name__ == "__main__":
    sys.exit(main())
