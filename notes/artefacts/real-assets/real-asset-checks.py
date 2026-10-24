"""Real assets: the worked numbers of the real-asset investor entries.

The checks are in trading_notes.numerical.real_assets.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.real_assets
(numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.real_assets import main

if __name__ == "__main__":
    sys.exit(main())
