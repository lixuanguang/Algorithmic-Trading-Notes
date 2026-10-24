"""Investment planning case: the return requirement, allocations, a concentrated stock and biases.

The checks are in trading_notes.numerical.investment_planning.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.investment_planning
(numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.investment_planning import main

if __name__ == "__main__":
    sys.exit(main())
