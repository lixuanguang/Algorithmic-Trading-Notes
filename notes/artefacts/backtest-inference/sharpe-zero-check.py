"""When the finite-fourth-moment condition of meth:sharpe-ratio-standard-error is needed.

Empirical extensions (2026-10-17), audit repair. The derivation and the Student-t3 and
three-point Monte Carlo checks are in trading_notes.numerical.sharpe_zero.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.sharpe_zero
(numpy). Exits non-zero on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.sharpe_zero import main

if __name__ == "__main__":
    sys.exit(main())
