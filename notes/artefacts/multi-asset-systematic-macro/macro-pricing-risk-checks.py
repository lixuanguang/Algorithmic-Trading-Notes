"""Macro pricing risk: regimes, transmission maps, rates and carry, and practitioner frameworks.

The checks are in trading_notes.numerical.macro_pricing_risk.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.macro_pricing_risk
(numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.macro_pricing_risk import main

if __name__ == "__main__":
    sys.exit(main())
