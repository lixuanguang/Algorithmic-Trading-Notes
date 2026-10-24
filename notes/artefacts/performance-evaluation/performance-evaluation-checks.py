"""Performance evaluation: risk-adjusted measures, attribution, benchmark quality and skill.

The checks are in trading_notes.numerical.performance_evaluation.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.performance_evaluation
(numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.performance_evaluation import main

if __name__ == "__main__":
    sys.exit(main())
