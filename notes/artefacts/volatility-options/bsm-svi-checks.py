"""Own checks behind mod:black-scholes-merton and def:implied-volatility-surface.

Empirical extensions, 2026-10-17. The checks, their sources and the finding on the density
in Gatheral and Jacquier's Lemma 2.2 are in trading_notes.numerical.bsm_svi.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.bsm_svi
(standard library). Exits non-zero on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.bsm_svi import main

if __name__ == "__main__":
    sys.exit(main())
