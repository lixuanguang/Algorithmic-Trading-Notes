"""Credit risk, CDS, sovereign debt and securitisation checks.

The checks are in trading_notes.numerical.credit_cds_securitisation.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.credit_cds_securitisation
(numpy, scipy). Exits 1 on failure.
"""

import sys

from trading_notes.numerical.credit_cds_securitisation import main

if __name__ == "__main__":
    sys.exit(main())
