"""Arithmetic behind USGS aluminium, EIA LNG and Moallemi-Saglam latency figures.

Source verification, 2026-10-17. The sources, the assumed 6.5-hour trading day and the
checks are in trading_notes.numerical.commodity_latency.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.commodity_latency
(standard library). Exits non-zero on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.commodity_latency import main

if __name__ == "__main__":
    sys.exit(main())
