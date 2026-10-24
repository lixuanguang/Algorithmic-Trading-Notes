"""Distributed-ledger mechanics and digital-asset investment arithmetic (2026-10-20).

The checks are in trading_notes.numerical.digital_assets.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.digital_assets (numpy).
Exits 1 on failure.
"""

import sys

from trading_notes.numerical.digital_assets import main

if __name__ == "__main__":
    sys.exit(main())
