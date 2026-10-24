"""Financial statement analysis: the worked numbers of the statement-analysis entries.

The checks are in trading_notes.numerical.statement_analysis.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.statement_analysis
(numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.statement_analysis import main

if __name__ == "__main__":
    sys.exit(main())
