"""Coverage pilot: the worked example of meth:statement-linked-cash-flows.

Dated 2026-10-18, with the cash-tax correction of the second audit. The statements, the
three derivations of the cash-flow statement and their sources are in
trading_notes.numerical.cash_flow_linkage.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.cash_flow_linkage
(standard library). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.cash_flow_linkage import main

if __name__ == "__main__":
    sys.exit(main())
