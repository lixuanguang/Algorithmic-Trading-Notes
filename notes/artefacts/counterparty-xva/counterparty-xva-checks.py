"""Counterparty credit risk: exposures, CVA, wrong-way risk, collateral and rate-tree CVA.

The checks are in trading_notes.numerical.counterparty_xva.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.counterparty_xva
(numpy, scipy). Exits 1 on failure.
"""

import sys

from trading_notes.numerical.counterparty_xva import main

if __name__ == "__main__":
    sys.exit(main())
