"""The concentrated-position example: sale, zero-cost collar, prepaid forward, exchange fund."""

import math
import sys
from typing import Final

import scipy

from trading_notes.numerical.report import CheckReport
from trading_notes.numerical.wealth_transfer.concentrated_stock import (
    ExchangeFund,
    PrepaidForward,
    StockOptions,
)

NSH: Final = 100_000  # shares held
S0: Final = 50.0
BASIS: Final = 10.0  # per share
TAX: Final = 0.20  # assumed flat rate on the gain
R: Final = 0.04  # continuously compounded
T: Final = 1.0
K1: Final = 45.0  # the collar's put strike
OPTIONS: Final = StockOptions(spot=S0, rate=R, volatility=0.30, maturity=T)
FORWARD: Final = PrepaidForward(shares=NSH, floor=50.0, cap=62.5)
F: Final = FORWARD.floor
C: Final = FORWARD.cap


def check_options(report: CheckReport) -> tuple[float, float]:
    """Check parity, the collar's call strike and the advance; return (K2, advance)."""
    print("== options: parity, zero-cost collar strike, prepaid-forward advance")
    put_direct = OPTIONS.put_direct(K1)
    put = OPTIONS.put
    report.ok(
        "put-call parity (direct BSM put against c - S + K e^{-rT})",
        abs(put_direct - put(K1)) <= 1e-10,
        f"put 45 = {put(K1):.6f}",
    )
    K2 = OPTIONS.zero_cost_call_strike(K1)
    report.ok(
        "zero-cost collar: call at K2 worth the 45 put",
        abs(OPTIONS.call(K2) - put(K1)) <= 1e-10,
        f"K2 = {K2:.4f}",
    )
    adv1 = FORWARD.advance(OPTIONS)
    adv2 = FORWARD.advance_as_loan_and_collar(OPTIONS)
    report.ok(
        "advance by two routes: S0 - c(F) + (F/C) c(C) = F e^{-rT} - p(F) + (F/C) c(C)"
        " (a loan plus a collar)",
        abs(adv1 / adv2 - 1) <= 1e-10,
        f"{adv1:,.2f}, {adv1 / (NSH * S0):.2%} of the 5,000,000 position",
    )
    return K2, adv1


def check_terminal_values(report: CheckReport, K2: float, adv1: float) -> None:
    """Check the sale and the prepaid forward on a grid, and print each strategy's values."""
    print("== terminal values per strategy (before any tax on the hedged positions)")
    sale_cash = NSH * S0 - TAX * NSH * (S0 - BASIS)
    # The gain is 4,000,000, so the tax is 800,000, and 4,200,000 x e^0.04 = 4,371,405.25.
    report.ok(
        "sale: tax 800,000, 4,200,000 reinvested, 4,371,405.25 after a year at 4 percent",
        abs(TAX * NSH * (S0 - BASIS) - 800_000) <= 0.01
        and abs(sale_cash * math.exp(R * T) - 4_371_405.25) <= 0.01,
        f"{sale_cash * math.exp(R * T):,.2f}",
    )
    grid = (30.0, 40.0, 50.0, 60.0, 70.0, 80.0)
    rows: list[tuple[float, float, float, float, float, float]] = []
    exact, decomp, shares_ok = True, True, True
    for ST in grid:
        delivered = FORWARD.delivered(ST)
        delivered_opt = FORWARD.delivered_by_options(ST)
        retained = NSH * ST - delivered
        retained_opt = FORWARD.retained_by_options(ST)
        nshares = delivered / ST
        exact &= retained + delivered == NSH * ST
        decomp &= (
            abs(delivered - delivered_opt) <= 1e-9 * NSH * ST
            and abs(retained - retained_opt) <= 1e-9 * NSH * ST
        )
        shares_ok &= NSH * F / C - 1e-9 <= nshares <= NSH + 1e-9
        collar = NSH * min(max(ST, K1), K2)
        vpf = retained + adv1 * math.exp(R * T)
        rows.append((ST, NSH * ST, collar, vpf, sale_cash * math.exp(R * T), nshares))
    report.ok("prepaid forward: retained plus delivered value equals N S_T on the grid", exact)
    report.ok("prepaid forward: payoffs equal their option decomposition", decomp)
    report.ok(
        "prepaid forward: delivered shares between 0.8 N and N (a variable number)", shares_ok
    )
    print("    S_T   hold          collar        prepaid fwd   sale          shares delivered")
    for ST, hold, col, vpf, sale, ns in rows:
        print(
            f"    {ST:4.0f}  {hold:12,.0f}  {col:12,.0f}  {vpf:12,.0f}  {sale:12,.0f}  {ns:9,.0f}"
        )


def check_exchange_fund(report: CheckReport) -> None:
    """Reproduce Exhibit 15 and print the fee at which the fund's final value equals the sale's."""
    print("== exchange fund against sale (PMiP Exhibit 15) and the break-even fee")
    fund = ExchangeFund(value=1_000_000, basis=100_000, tax=0.25, growth=0.10, years=7)
    b, rate = fund.basis, fund.tax
    inv, s7, fin_s = fund.sale()
    e7, fin_e = fund.fund()
    printed = (775_000, 1_510_256, 1_948_717, 183_814, 462_179, 1_326_442, 1_486_538)
    mine = (inv, s7, e7, rate * (s7 - inv), rate * (e7 - b), fin_s, fin_e)
    report.ok(
        "Exhibit 15 reproduced to the dollar",
        all(abs(a - p) <= 1 for a, p in zip(mine, printed, strict=True)),
        ", ".join(f"{x:,.0f}" for x in mine),
    )

    print(
        "    break-even annual fee (deducted from the 10 percent return):"
        f" {fund.break_even_fee():.4%}"
    )


def main() -> int:
    """Print the versions, then run the three parts with one report.

    The concentrated-position example of meth:complex-client-situations and the zero-cost
    collar of meth:covered-call-protective-put.

    Inputs and acceptance were fixed before the first run.
    Synthetic: 100,000 shares at 50, basis 10 per share, an assumed flat 20 percent tax on the gain
    (illustrative, not a statutory rate), one year, r = 4 percent continuously compounded, q = 0,
    volatility 30 percent, BSM option values.
    Strategies: outright sale (proceeds held riskless, to isolate exposure); a zero-cost collar
    (long 45 put, short call at the strike that makes the premiums equal); a variable prepaid
    forward on terms patterned on the structure in Rev. Rul. 2003-7 (deliver all N shares below
    F = 50, shares worth N F between F and C = 62.5, N F / C shares above), advance = BSM present
    value of the delivery, with no dealer spread. Also: Portfolio Management in Practice, Vol. 1,
    chap. 16, Exhibit 15 (exchange fund against sale) reproduced, and the annual fee that equates
    them (Interpretation).
    Deterministic; no tax treatment is computed except the sale's, and none is implied for the
    collar or forward.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, SciPy {scipy.__version__}")
    report = CheckReport()
    K2, adv1 = check_options(report)
    check_terminal_values(report, K2, adv1)
    check_exchange_fund(report)
    if report.failures:
        print("FAILED:", ", ".join(report.failures))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
