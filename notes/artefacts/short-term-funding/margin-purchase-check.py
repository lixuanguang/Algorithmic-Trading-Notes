"""The worked examples of meth:margin-purchase-leverage.

The checks are in trading_notes.numerical.margin_purchase.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.margin_purchase
(scipy). Exits 1 on failure.
"""

import sys

from trading_notes.numerical.margin_purchase import main

if __name__ == "__main__":
    sys.exit(main())
