"""Exchange-rate mechanics and determination: the worked numbers of nine FX entries.

The checks are in trading_notes.numerical.fx_mechanics.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.fx_mechanics
(numpy, scipy). Exits 1 on failure.
"""

import sys

from trading_notes.numerical.fx_mechanics import main

if __name__ == "__main__":
    sys.exit(main())
