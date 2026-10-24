"""Numerical checks for the closed forms in model-derivations.tex.

The checks are in trading_notes.numerical.lob_model_derivations.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.lob_model_derivations
(numpy and scipy). Exits non-zero on failure, with no summary line.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.lob_model_derivations import main

if __name__ == "__main__":
    sys.exit(main())
