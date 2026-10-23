"""Own checks behind def:amm-pool-mechanics.

Empirical extensions, 2026-10-17. The checks, their sources and derivations are in
trading_notes.numerical.amm_pool.

Run: uv run python amm-checks.py (standard library). Exits non-zero on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.amm_pool import main

if __name__ == "__main__":
    sys.exit(main())
