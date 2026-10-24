"""Intercorporate investments, FX reporting and financial institutions: the worked numbers.

The checks are in trading_notes.numerical.intercorporate_fx_institutions.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.intercorporate_fx_institutions
(numpy). Exits 1 on failure.
"""

import sys

from trading_notes.numerical.intercorporate_fx_institutions import main

if __name__ == "__main__":
    sys.exit(main())
