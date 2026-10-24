"""The worked numbers of meth:cross-currency-basis-swaps.

The checks are in trading_notes.numerical.cross_currency_basis.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.cross_currency_basis
(numpy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.cross_currency_basis import main

if __name__ == "__main__":
    sys.exit(main())
