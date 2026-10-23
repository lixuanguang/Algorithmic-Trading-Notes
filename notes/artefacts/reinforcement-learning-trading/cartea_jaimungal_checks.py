"""Numerical demonstration for mod:cartea-jaimungal-execution.

Lehalle and Laruelle, app. A.7.3, pp. 281-284, with the follow-up of 2026-10-15. The HJB,
Riccati, Feynman-Kac, inventory-path and wealth-identity computations are in
trading_notes.numerical.cartea_jaimungal.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.cartea_jaimungal
(standard library). Prints its values and exits 0; it asserts nothing.
"""

# standard library imports
import sys

# project library imports
from trading_notes.numerical.cartea_jaimungal import main

if __name__ == "__main__":
    sys.exit(main())
