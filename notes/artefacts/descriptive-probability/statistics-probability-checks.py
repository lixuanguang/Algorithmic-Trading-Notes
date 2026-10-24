"""Return statistics, conditional moments, distributions and Bayesian updating, by two routes.

The checks are in trading_notes.numerical.statistics_probability.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.statistics_probability
(numpy, scipy). Exits 1 on failure.
"""

import sys

from trading_notes.numerical.statistics_probability import main

if __name__ == "__main__":
    sys.exit(main())
