"""Checks behind meth:sharpe-ratio-standard-error and meth:deflated-sharpe-ratio.

Source verification (2026-10-17): Lo's (2002) standard error and annualisation factor, and
Bailey and Lopez de Prado's deflated Sharpe ratio example. The checks are in
trading_notes.numerical.sharpe_statistics.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.sharpe_statistics
(scipy). Exits non-zero on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.sharpe_statistics import main

if __name__ == "__main__":
    sys.exit(main())
