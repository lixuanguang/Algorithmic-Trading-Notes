"""Country-risk example of meth:cost-of-debt-equity-estimation.

Library gap-filling Batch L6, package L6-a, 2026-10-21. The checks, their sources and the
first-run record are in trading_notes.numerical.country_risk_premium.

Run: uv run python country-risk-premium-check.py   Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.country_risk_premium import main

if __name__ == "__main__":
    sys.exit(main())
