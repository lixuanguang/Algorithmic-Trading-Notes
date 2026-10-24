"""Short-term funding and repurchase agreements: the worked numbers of def:short-term-funding-repo.

Dated 2026-10-19. The checks, their sources and conventions are in
trading_notes.numerical.funding_repo.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.funding_repo
(standard library only). Exits 1 on failure.
"""

import sys

from trading_notes.numerical.funding_repo import main

if __name__ == "__main__":
    sys.exit(main())
