"""Own checks behind meth:equal-risk-contribution (Maillard, Roncalli and Teiletche).

Empirical extensions, 2026-10-17. The ERC iteration, the projected-gradient minimum-variance
portfolio and the two covariance cases are in trading_notes.numerical.equal_risk_contribution.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.equal_risk_contribution
(numpy). Exits non-zero on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.equal_risk_contribution import main

if __name__ == "__main__":
    sys.exit(main())
