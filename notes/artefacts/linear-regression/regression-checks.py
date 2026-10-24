"""Simple regression: estimation, diagnostics, ANOVA, prediction and functional form.

The checks are in trading_notes.numerical.linear_regression.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.linear_regression
(numpy, scipy, statsmodels). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.linear_regression import main

if __name__ == "__main__":
    sys.exit(main())
