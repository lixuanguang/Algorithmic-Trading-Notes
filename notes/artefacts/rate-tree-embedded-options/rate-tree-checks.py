"""Rate trees and bonds with embedded options: calibration, callable and putable bonds, durations.

The checks are in trading_notes.numerical.rate_tree_embedded_options.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.rate_tree_embedded_options
(numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.rate_tree_embedded_options import main

if __name__ == "__main__":
    sys.exit(main())
