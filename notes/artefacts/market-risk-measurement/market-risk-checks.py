"""Market risk measurement and limits: VaR, sensitivities, scenarios and capital.

The checks are in trading_notes.numerical.market_risk_measurement.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.market_risk_measurement
(numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.market_risk_measurement import main

if __name__ == "__main__":
    sys.exit(main())
