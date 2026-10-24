"""Offline, synthetic illustration behind mech:order-state-reconciliation.

Source verification, 2026-10-17, with the corrections of the same day. The order, intent and
execution records, the reconciler and the checks are in
trading_notes.numerical.order_reconciliation.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.order_reconciliation
(standard library). Exits non-zero on failure.
"""

import sys

from trading_notes.numerical.order_reconciliation import main

if __name__ == "__main__":
    sys.exit(main())
