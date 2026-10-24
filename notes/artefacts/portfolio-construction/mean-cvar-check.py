"""Mean-CVaR optimisation: the LP, Rockafellar and Uryasev's benchmark and the normal equivalence.

The checks are in trading_notes.numerical.mean_cvar.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.mean_cvar
(numpy, scipy). Exits 1 on failure. About 110 seconds: the LPs of part 3 on 100,000 scenarios take
nearly all of it.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.mean_cvar import main

if __name__ == "__main__":
    sys.exit(main())
