"""Brownian motion, Ito's lemma and risk-neutral pricing, checked on model-generated data.

The checks are in trading_notes.numerical.stochastic_calculus.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.stochastic_calculus
(numpy, scipy). Exits 1 on failure.
"""

import sys

from trading_notes.numerical.stochastic_calculus import main

if __name__ == "__main__":
    sys.exit(main())
