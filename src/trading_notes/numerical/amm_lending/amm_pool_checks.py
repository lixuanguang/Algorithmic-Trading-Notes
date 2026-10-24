"""Constant-product swaps, impermanent loss and concentrated liquidity of Uniswap pools."""

import math
import sys
from typing import Final

from trading_notes.numerical.amm_lending.liquidity_pools import (
    ConcentratedPosition,
    ConstantProductPool,
)
from trading_notes.numerical.report import CheckReport

# The v2 pool before the trade: 1,000 ETH and 2,000,000 USDC.
POOL: Final = ConstantProductPool(x=1000.0, y=2_000_000.0, fee=0.003)


def check_v2_swap(report: CheckReport) -> None:
    """Sell 10 ETH into the v2 pool with the 0.30% fee."""
    print("== v2 swap with the 0.30% fee")
    x, y, dx, fee = POOL.x, POOL.y, 10.0, POOL.fee  # sell 10 ETH
    g = 1 - fee
    dy = POOL.swap_output(dx)
    after = POOL.after_swap(dx)
    x1, y1 = after.x, after.y
    lhs = (x1 - fee * dx) * (y1 - 0)
    report.ok(
        "output satisfies eq. (10) with equality",
        abs(lhs - x * y) / (x * y) < 1e-12,
        f"dy = {dy:.4f}",
    )
    report.ok(
        "k rises after the trade (fee retained in the pool)",
        x1 * y1 > x * y,
        f"{x1 * y1:.1f} > {x * y:.1f}",
    )
    p0, exec_p, p1 = POOL.price, dy / dx, after.price
    print(f"     pool price {p0:.2f}, execution price {exec_p:.2f}, new pool price {p1:.2f}")
    report.ok("execution price lies between pool prices before and after", p1 < exec_p < p0)
    report.ok(
        "fee-free execution shortfall (p0 - exec/g)/p0 = g dx/(x + g dx)",
        abs((p0 - exec_p / g) / p0 - g * dx / (x + g * dx)) < 1e-12,
        f"{(p0 - exec_p / g) / p0 * 100:.3f}% for a trade of {dx / x * 100:.1f}% of the reserve",
    )


def check_impermanent_loss(report: CheckReport) -> None:
    """Value a full-range position in the v2 pool against holding, without fees."""
    print("== impermanent loss of a full-range position (no fees)")
    x, y = POOL.x, POOL.y
    p0 = POOL.price
    for r in (0.5, 1.0, 1.5, 2.0, 4.0):
        p = p0 * r
        moved = POOL.arbitraged(p)
        v_pool, v_hold = moved.x * p + moved.y, x * p + y
        il = v_pool / v_hold - 1
        report.ok(
            f"r = {r}: IL = 2 sqrt(r)/(1+r) - 1",
            abs(il - (2 * math.sqrt(r) / (1 + r) - 1)) < 1e-12,
            f"{il * 100:+.2f}%",
        )


def check_concentrated_position(report: CheckReport) -> None:
    """Check the real reserves and capital of a v3 position on [p_a, p_b]."""
    print("== v3 concentrated position")
    position = ConcentratedPosition(liquidity=10_000.0, lower=1600.0, upper=2500.0)
    pa, pb, pc, L = position.lower, position.upper, 2000.0, position.liquidity
    xr, yr = position.reserves(pc)
    report.ok(
        "real reserves satisfy eq. (2.2)",
        abs((xr + L / math.sqrt(pb)) * (yr + L * math.sqrt(pa)) - L * L) / L**2 < 1e-12,
        f"x_real = {xr:.4f}, y_real = {yr:.2f}",
    )
    full_x, full_y = L / math.sqrt(pc), L * math.sqrt(pc)  # same L over (0, inf)
    eff = (full_x * pc + full_y) / (xr * pc + yr)
    print(
        f"     capital for the same L: full range {full_x * pc + full_y:,.0f} against"
        f" {xr * pc + yr:,.0f} in [{pa:.0f}, {pb:.0f}], ratio {eff:.2f}"
    )
    report.ok("concentration needs less capital for the same liquidity", eff > 1)
    xa, yb = position.all_x(), position.all_y()
    report.ok(
        "below p_a the position is all X, above p_b all Y",
        xa > 0 and yb > 0,
        f"all-X {xa:.4f}, all-Y {yb:.2f}",
    )


def main() -> int:
    """Run every check with a fresh report, print the summary and return the exit status.

    Own checks behind def:amm-pool-mechanics. Uniswap v2 Core (March 2020): constant product
    x*y = k, a 30-basis-point fee to liquidity providers (sec. 1), enforced as
    (x1 - 0.003 x_in)(y1 - 0.003 y_in) >= x0 y0 (sec. 3.2.1, eq. (10)); Uniswap v3 Core (March
    2021): fee tiers 0.05%, 0.30%, 1% (sec. 1), liquidity L = sqrt(k), and a position on
    [p_a, p_b] whose real reserves satisfy (x + L/sqrt(p_b))(y + L sqrt(p_a)) = L^2 (sec. 2, eq.
    (2.2), read from the page image). Own derivations checked numerically: the swap output,
    execution price against the pool price, the value of a full-range position against holding
    (impermanent loss 2 sqrt(r)/(1+r) - 1 for a price ratio r, before fees), and the real
    reserves of a concentrated position.

    Returns:
        The exit status, 0 or 1.
    """
    report = CheckReport()
    check_v2_swap(report)
    check_impermanent_loss(report)
    check_concentrated_position(report)
    if report.failures:
        print("\nFAILED:", report.failures)
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
