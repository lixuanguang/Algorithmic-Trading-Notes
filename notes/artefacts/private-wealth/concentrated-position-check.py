"""The concentrated-position example and the zero-cost collar.

The checks are in trading_notes.numerical.concentrated_position.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.concentrated_position
(scipy). Exits 1 on failure.
"""

import sys

from trading_notes.numerical.concentrated_position import main

if __name__ == "__main__":
    sys.exit(main())
