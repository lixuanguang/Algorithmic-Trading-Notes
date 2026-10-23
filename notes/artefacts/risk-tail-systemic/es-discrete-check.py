"""Expected shortfall for discrete and historical-simulation distributions.

Empirical extensions (2026-10-17), audit repair, behind meth:var-es-estimation-methods. The
definitions, the audit example and the historical-simulation and normal-law checks are in
trading_notes.numerical.expected_shortfall.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.expected_shortfall
(standard library). Exits non-zero on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.expected_shortfall import main

if __name__ == "__main__":
    sys.exit(main())
