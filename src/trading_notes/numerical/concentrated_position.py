"""The concentrated-position example and the zero-cost collar.

Library gap-filling Batch L6, package L6-b (2026-10-21): the concentrated-position example of
meth:complex-client-situations and the zero-cost collar of meth:covered-call-protective-put.

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

Run: uv run --frozen --no-editable python -m trading_notes.numerical.concentrated_position
(scipy). Exits 1 on failure.
"""

# standard library imports
import math
import sys
from typing import Final

# third party library imports
import scipy
from scipy import stats

# project library imports
from trading_notes.numerical.report import CheckReport

NSH: Final = 100_000  # shares held
S0: Final = 50.0
BASIS: Final = 10.0  # per share
TAX: Final = 0.20  # assumed flat rate on the gain
R: Final = 0.04  # continuously compounded
SIG: Final = 0.30
T: Final = 1.0
K1: Final = 45.0  # the collar's put strike
F: Final = 50.0  # the prepaid forward's floor
C: Final = 62.5  # the prepaid forward's cap
N = stats.norm.cdf


def call(K: float) -> float:
    """Return the BSM call on the shares struck at K."""
    d1 = (math.log(S0 / K) + (R + SIG**2 / 2) * T) / (SIG * math.sqrt(T))
    return S0 * N(d1) - K * math.exp(-R * T) * N(d1 - SIG * math.sqrt(T))


def put(K: float) -> float:
    """Return the put struck at K by put-call parity."""
    return call(K) - S0 + K * math.exp(-R * T)


def check_options(report: CheckReport) -> tuple[float, float]:
    """Check parity, the collar's call strike and the advance; return (K2, advance)."""
    print("== options: parity, zero-cost collar strike, prepaid-forward advance")
    d1 = (math.log(S0 / K1) + (R + SIG**2 / 2) * T) / (SIG * math.sqrt(T))
    put_direct = K1 * math.exp(-R * T) * N(-d1 + SIG * math.sqrt(T)) - S0 * N(-d1)
    report.ok(
        "put-call parity (direct BSM put against c - S + K e^{-rT})",
        abs(put_direct - put(K1)) <= 1e-10,
        f"put 45 = {put(K1):.6f}",
    )
    lo, hi = S0, 3 * S0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if call(mid) > put(K1) else (lo, mid)
    K2 = 0.5 * (lo + hi)
    report.ok(
        "zero-cost collar: call at K2 worth the 45 put",
        abs(call(K2) - put(K1)) <= 1e-10,
        f"K2 = {K2:.4f}",
    )
    adv1 = NSH * (S0 - call(F) + F / C * call(C))
    adv2 = NSH * (F * math.exp(-R * T) - put(F) + F / C * call(C))
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
    # First run (recorded): the frozen hand values (tax 900,000; 4,267,328.43) were wrong; the
    # gain is 4,000,000, so the tax is 800,000 and 4,200,000 x e^0.04 = 4,371,405.25 (hand:
    # e^0.04 = 1.0408107742). Literals corrected; tolerance unchanged.
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
        delivered = NSH * ST if ST < F else (NSH * F if ST <= C else NSH * F / C * ST)
        delivered_opt = NSH * (ST - max(ST - F, 0) + F / C * max(ST - C, 0))
        retained = NSH * ST - delivered
        retained_opt = NSH * (max(ST - F, 0) - F / C * max(ST - C, 0))
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
    mv, b, rate, g, yrs = 1_000_000, 100_000, 0.25, 0.10, 7
    inv = mv - rate * (mv - b)
    s7 = inv * (1 + g) ** yrs
    e7 = mv * (1 + g) ** yrs
    fin_s = s7 - rate * (s7 - inv)
    fin_e = e7 - rate * (e7 - b)
    printed = (775_000, 1_510_256, 1_948_717, 183_814, 462_179, 1_326_442, 1_486_538)
    mine = (inv, s7, e7, rate * (s7 - inv), rate * (e7 - b), fin_s, fin_e)
    report.ok(
        "Exhibit 15 reproduced to the dollar",
        all(abs(a - p) <= 1 for a, p in zip(mine, printed, strict=True)),
        ", ".join(f"{x:,.0f}" for x in mine),
    )

    def fund_final(fee: float) -> float:
        v = mv * (1 + g - fee) ** yrs
        return v - rate * (v - b)

    lo, hi = 0.0, g
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if fund_final(mid) > fin_s else (lo, mid)
    print(f"    break-even annual fee (deducted from the 10 percent return): {0.5 * (lo + hi):.4%}")


def main() -> int:
    """Print the versions, then run the three parts with one report.

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
