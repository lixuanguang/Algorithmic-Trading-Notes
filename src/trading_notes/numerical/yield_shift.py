"""Yield change against a parallel zero-curve shift.

Derivatives and hedging review follow-up check (2026-10-16). Continuous compounding. A
demonstration: it prints the yield changes and durations and asserts nothing.
Run: uv run --frozen --no-editable python -m trading_notes.numerical.yield_shift (numpy, scipy).
"""

import sys

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import brentq

type Floats = NDArray[np.float64]


def price(c: Floats, t: Floats, z: Floats) -> np.float64:
    """Return the price of cash flows c at times t discounted at continuous zero rates z."""
    return np.sum(c * np.exp(-z * t))


def yld(c: Floats, t: Floats, z: Floats) -> float:
    """Return the continuous yield that reprices the cash flows, bracketed in [-1, 1]."""
    B = price(c, t, z)

    def gap(y: float) -> np.float64:
        return np.sum(c * np.exp(-y * t)) - B

    return brentq(gap, -1, 1)


def main() -> int:
    """Print the yield changes for four bonds and curves, and the two durations.

    Returns:
        The exit status, always 0.
    """
    t = np.array([0.5, 1, 1.5, 2])
    z = np.array([0.05, 0.058, 0.064, 0.068])
    c = np.array([3, 3, 3, 103.0])
    for D in [1e-4, 0.01, 0.02]:
        print("coupon, Hull 4.2 curve, shift", D, "dy", yld(c, t, z + D) - yld(c, t, z))
    cz = np.array([0, 0, 0, 100.0])
    for D in [1e-4, 0.02]:
        print(
            "zero-coupon, same curve, shift",
            D,
            "dy",
            yld(cz, t, z + D) - yld(cz, t, z),
            "y=R(T)?",
            yld(cz, t, z),
            z[-1],
        )
    # steep curve, long coupon bond
    t2 = np.arange(1, 11.0)
    z2 = 0.01 + 0.004 * t2
    c2 = np.full(10, 5.0)
    c2[-1] += 100
    for D in [1e-4, 0.02]:
        print(
            "10y 5% coupon, steep curve, shift",
            D,
            "dy/D",
            (yld(c2, t2, z2 + D) - yld(c2, t2, z2)) / D,
        )
    y = yld(c2, t2, z2)
    dBdy = -(t2 * c2 * np.exp(-y * t2)).sum()
    dBdD = -(t2 * c2 * np.exp(-z2 * t2)).sum()
    print(
        "yield duration",
        -dBdy / price(c2, t2, z2),
        "zero-curve duration",
        -dBdD / price(c2, t2, z2),
    )
    # nonflat curve flat at the payment dates only: z at 1,2 equal; curve elsewhere irrelevant
    t3 = np.array([1, 2.0])
    z3 = np.array([0.05, 0.05])
    c3 = np.array([5, 105.0])
    print("flat at payment dates, shift .02 dy", yld(c3, t3, z3 + 0.02) - yld(c3, t3, z3))
    return 0


if __name__ == "__main__":
    sys.exit(main())
