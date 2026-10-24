"""Inference and simulation: intervals, tests, bootstrap and Monte Carlo against closed forms.

The checks are in trading_notes.numerical.inference_simulation.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.inference_simulation
(numpy, scipy). Exits 1 on failure.
"""

import sys

from trading_notes.numerical.inference_simulation import main

if __name__ == "__main__":
    sys.exit(main())
