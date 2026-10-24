"""The worked examples of meth:correlation-independence-tests.

The checks are in trading_notes.numerical.correlation_independence.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.correlation_independence
(numpy, scipy). Exits 1 on failure.
"""

import sys

from trading_notes.numerical.correlation_independence import main

if __name__ == "__main__":
    sys.exit(main())
