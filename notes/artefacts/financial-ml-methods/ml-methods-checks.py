"""Financial machine learning methods: supervised, unsupervised, leakage, text and evaluation.

The checks are in trading_notes.numerical.financial_ml_methods.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.financial_ml_methods
(numpy, scipy). Exits 1 on failure.
"""

import sys

from trading_notes.numerical.financial_ml_methods import main

if __name__ == "__main__":
    sys.exit(main())
