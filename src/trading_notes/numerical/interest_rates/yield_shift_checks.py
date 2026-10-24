"""Yield change against a parallel zero-curve shift, for coupon and zero-coupon bonds."""

import sys

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.interest_rates.continuous_cash_flows import CashFlows


def yield_change(flows: CashFlows, z: NDArray[np.float64], shift: float) -> float:
    """Return the change in yield when every zero rate rises by shift."""
    return flows.yield_to_maturity(z + shift) - flows.yield_to_maturity(z)


def main() -> int:
    """Print the yield changes for four bonds and curves, and the two durations.

    A demonstration: it prints the yield changes and durations and asserts nothing. Rates are
    continuously compounded.

    Returns:
        The exit status, always 0.
    """
    t = np.array([0.5, 1, 1.5, 2])
    z = np.array([0.05, 0.058, 0.064, 0.068])
    coupon = CashFlows(amounts=np.array([3, 3, 3, 103.0]), times=t)
    for D in [1e-4, 0.01, 0.02]:
        print("coupon, Hull 4.2 curve, shift", D, "dy", yield_change(coupon, z, D))
    zero = CashFlows(amounts=np.array([0, 0, 0, 100.0]), times=t)
    for D in [1e-4, 0.02]:
        print(
            "zero-coupon, same curve, shift",
            D,
            "dy",
            yield_change(zero, z, D),
            "y=R(T)?",
            zero.yield_to_maturity(z),
            z[-1],
        )
    # steep curve, long coupon bond
    t2 = np.arange(1, 11.0)
    z2 = 0.01 + 0.004 * t2
    c2 = np.full(10, 5.0)
    c2[-1] += 100
    long_bond = CashFlows(amounts=c2, times=t2)
    for D in [1e-4, 0.02]:
        print("10y 5% coupon, steep curve, shift", D, "dy/D", yield_change(long_bond, z2, D) / D)
    y = long_bond.yield_to_maturity(z2)
    dBdy = long_bond.price_derivative(y)
    dBdD = long_bond.price_derivative(z2)
    print(
        "yield duration",
        -dBdy / long_bond.price(z2),
        "zero-curve duration",
        -dBdD / long_bond.price(z2),
    )
    # a curve flat at the payment dates only: elsewhere it does not matter
    flat_at_dates = CashFlows(amounts=np.array([5, 105.0]), times=np.array([1, 2.0]))
    z3 = np.array([0.05, 0.05])
    print("flat at payment dates, shift .02 dy", yield_change(flat_at_dates, z3, 0.02))
    return 0


if __name__ == "__main__":
    sys.exit(main())
