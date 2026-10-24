"""Extreme value tail estimation: Hill, peaks over threshold and GPD fits against known truths.

The checks are in trading_notes.numerical.extreme_value.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.extreme_value
(numpy, scipy). Exits 1 on failure. About 24 seconds: the GPD fits and the Hill bootstrap of the
diagnostics take most of it.
"""

import sys

from trading_notes.numerical.extreme_value import main

if __name__ == "__main__":
    sys.exit(main())
