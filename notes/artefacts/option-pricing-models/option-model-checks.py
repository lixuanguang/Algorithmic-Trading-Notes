"""Own checks behind the Heston, Merton jump-diffusion and SABR entries.

The checks are in trading_notes.numerical.option_models.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.option_models (numpy).
Exits 1 on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.option_models import main

if __name__ == "__main__":
    sys.exit(main())
