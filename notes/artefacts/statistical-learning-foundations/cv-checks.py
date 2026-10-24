"""Checks behind meth:purged-embargoed-cross-validation.

The checks are in trading_notes.numerical.purged_cv.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.purged_cv (numpy).
Exits non-zero on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.purged_cv import main

if __name__ == "__main__":
    sys.exit(main())
