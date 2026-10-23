"""Deadline arithmetic behind data:holdings-insider-filing-lags.

Source verification, 2026-10-17. The rules cited, the business-day calendar and the checks
are in trading_notes.numerical.filing_deadlines.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.filing_deadlines
(standard library). Exits non-zero on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.filing_deadlines import main

if __name__ == "__main__":
    sys.exit(main())
