"""Capital market expectations: the worked numbers of six CME entries.

The checks are in trading_notes.numerical.capital_market_expectations.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.capital_market_expectations
(numpy, scipy). Exits 1 on failure.
"""

import sys

from trading_notes.numerical.capital_market_expectations import main

if __name__ == "__main__":
    sys.exit(main())
