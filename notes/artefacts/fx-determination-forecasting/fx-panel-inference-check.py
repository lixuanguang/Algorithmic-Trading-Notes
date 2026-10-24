"""Pooled Clark-West inference: calendar-month lags and cross-currency dependence.

The checks are in trading_notes.numerical.fx_panel_inference.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.fx_panel_inference
(numpy only; exits 1 on failure).
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.fx_panel_inference import main

if __name__ == "__main__":
    sys.exit(main())
