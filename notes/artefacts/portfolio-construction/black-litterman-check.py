"""Checks behind mod:black-litterman (Black and Litterman 1991, Appendix, points 6-8).

Source verification, 2026-10-17. The precision-form posterior, its independent Gaussian
conditioning reference and the three-asset example are in trading_notes.numerical.black_litterman.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.black_litterman
(numpy). Exits non-zero on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.black_litterman import main

if __name__ == "__main__":
    sys.exit(main())
