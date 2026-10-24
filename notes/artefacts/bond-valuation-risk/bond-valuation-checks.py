"""Bond valuation and interest-rate risk: the worked numbers of eight bond-measure entries.

The checks are in trading_notes.numerical.bond_valuation_risk.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.bond_valuation_risk
(numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.bond_valuation_risk import main

if __name__ == "__main__":
    sys.exit(main())
