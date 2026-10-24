"""CAPM, market model and factor models: the worked examples of seven asset-pricing entries.

The checks are in trading_notes.numerical.asset_pricing_factor_models; this entrypoint passes
the compendium figure's location, so it runs from any directory.

Run: uv run --frozen --no-editable python asset-pricing-checks.py   (numpy, statsmodels).
Exits 1 on failure.
"""

# standard library imports
import sys
from pathlib import Path

# project library imports
from trading_notes.numerical.asset_pricing_factor_models import main

if __name__ == "__main__":
    ROOT = Path(__file__).resolve().parents[3]
    sys.exit(main(ROOT / "compendium" / "asset-pricing" / "figures" / "security-market-line.tikz"))
