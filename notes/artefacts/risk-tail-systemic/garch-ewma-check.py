"""Own check behind mod:garch-volatility-forecast.

Empirical extensions (2026-10-17): the GARCH(1,1) k-step forecast against simulation, and EWMA
against the true GARCH forecast. The checks are in trading_notes.numerical.garch_ewma.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.garch_ewma
(numpy). Exits non-zero on failure.
"""

import sys

from trading_notes.numerical.garch_ewma import main

if __name__ == "__main__":
    sys.exit(main())
