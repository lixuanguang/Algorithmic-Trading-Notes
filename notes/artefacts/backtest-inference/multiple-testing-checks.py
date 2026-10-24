"""Own Monte Carlo behind meth:multiple-testing-control.

Source verification (2026-10-17): Bonferroni, Holm, single-step max and StepM on equicorrelated
normal statistics, after Romano and Wolf (UPF working paper 712). The Monte Carlo is in
trading_notes.numerical.multiple_testing.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.multiple_testing
(numpy, scipy). Exits non-zero on failure.
"""

import sys

from trading_notes.numerical.multiple_testing import main

if __name__ == "__main__":
    sys.exit(main())
