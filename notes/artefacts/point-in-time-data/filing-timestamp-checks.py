"""The separate timestamps of an EDGAR filing, behind data:holdings-insider-filing-lags.

Source verification (audit repair), 2026-10-17, corrected the same day. The rules cited, the
availability and lower-bound conventions and the checks are in
trading_notes.numerical.filing_timestamps.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.filing_timestamps
(standard library). Exits non-zero on failure.
"""

import sys

from trading_notes.numerical.filing_timestamps import main

if __name__ == "__main__":
    sys.exit(main())
