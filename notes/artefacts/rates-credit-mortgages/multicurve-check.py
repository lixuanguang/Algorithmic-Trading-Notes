"""Own checks behind mod:multi-curve-fra-swap-valuation.

Empirical extensions, 2026-10-17. The checks, their sources and assumptions are in
trading_notes.numerical.multicurve.

Run: uv run python multicurve-check.py   (standard library). Exits non-zero on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.multicurve import main

if __name__ == "__main__":
    sys.exit(main())
