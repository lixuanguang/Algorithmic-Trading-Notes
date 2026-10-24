"""Numerical checks for res:synthetic-short-put-call.

Review follow-up, 2026-10-15. The terminal cash flows, the quadrature and closed-form
parity routes and the daily cash accounts are in trading_notes.numerical.synthetic_short.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.synthetic_short
(standard library). Exits non-zero if a check fails.
"""

import sys

from trading_notes.numerical.synthetic_short import main

if __name__ == "__main__":
    sys.exit(main())
