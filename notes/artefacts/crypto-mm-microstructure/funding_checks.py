"""Numerical checks for mech:perpetual-funding.

The Deribit funding formula, the independent piecewise rule, the worked examples of the
Funding Specifications page (edited 27 July 2026) and their units are in
trading_notes.numerical.perpetual_funding.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.perpetual_funding
(standard library). Exits non-zero if a check fails.
"""

import sys

from trading_notes.numerical.perpetual_funding import main

if __name__ == "__main__":
    sys.exit(main())
