"""Own synthetic check behind meth:var-es-estimation-methods.

Source verification (2026-10-17): the chi2(1) critical value of Christoffersen's LR_uc, and HS
against FHS VaR backtested on a simulated GARCH(1,1)-t(6) path. The checks are in
trading_notes.numerical.var_backtest.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.var_backtest
(numpy, scipy). Exits non-zero on failure.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.var_backtest import main

if __name__ == "__main__":
    sys.exit(main())
