"""Own checks behind the risk-parity passages.

Derivatives and empirical validation (2026-10-17) of Qian's 60/40 variance shares and
two-asset weights and of Maillard, Roncalli and Teiletche's inverse-volatility example. The
checks are in trading_notes.numerical.risk_parity.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.risk_parity
(numpy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.risk_parity import main

if __name__ == "__main__":
    sys.exit(main())
