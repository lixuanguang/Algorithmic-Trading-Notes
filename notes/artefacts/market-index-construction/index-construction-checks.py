"""Index values and returns: the worked examples of two index entries.

The checks are in trading_notes.numerical.index_construction.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.index_construction
(numpy). Exits 1 on failure.
"""

import sys

from trading_notes.numerical.index_construction import main

if __name__ == "__main__":
    sys.exit(main())
