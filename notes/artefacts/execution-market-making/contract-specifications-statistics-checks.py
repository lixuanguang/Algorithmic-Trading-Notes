"""Arithmetic behind contract tick values, end-use shares, OPEC shares and ISM release dates.

Source follow-up, 2026-10-16, extended 2026-10-17. The rulebook chapters, data releases,
the 2026 business-day calendar and its stated exceptions are in
trading_notes.numerical.contract_statistics.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.contract_statistics
(standard library only). Exits non-zero on failure.
"""

import sys

from trading_notes.numerical.contract_statistics import main

if __name__ == "__main__":
    sys.exit(main())
