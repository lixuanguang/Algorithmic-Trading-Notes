"""The worked examples of meth:margin-purchase-leverage.

Library gap-filling Batch L2, package P11c (2026-10-21).

Deterministic, original inputs. Percentages from the rule texts read on 2026-10-21:
Regulation T (12 CFR 220.12, eCFR up to date as of 19 October 2026) sets initial margin at 50
percent of market value for a long margin equity security and 150 percent for an unhedged short
sale of a nonexempted equity security (220.12(c)(1); the exceptions in (c)(2) and (d) do not
apply to these examples); FINRA Rule 4210(c) (version from 4 June 2026) sets maintenance at 25
percent of market value for long margin securities and, for a short stock at $5 or above, the
greater of $5 a share or 30 percent. Brokers may set higher house requirements (Rule 4210(d)).

Margin-call prices (assumptions as corrected after the L2 audit): the static formulas
P* = P0 (1 - m0)/(1 - mm) (long) and P0 (1 + m0)/(1 + mm) (short) assume the loan or the
credit balance is unchanged since the trade. With interest, fees, dividends or other flows,
the call price is computed from the balance at the date: P* = L_t / (N (1 - mm)) for a long
position and K_t / (N (1 + mm)) for a short one. Each formula is checked against a numerical
root of the equity-to-value condition, and the balances are rebuilt from a dated cash-flow
ledger (actual/360 simple interest).

Run: uv run --frozen --no-editable python -m trading_notes.numerical.margin_purchase
(scipy). Exits 1 on failure.
"""

import sys
from collections.abc import Callable
from datetime import date
from typing import Final

import scipy
from scipy import optimize

from trading_notes.numerical.report import CheckReport

N: Final = 1_000  # shares
P0: Final = 40.0  # trade price
M0: Final = 0.50  # initial margin
MM_LONG: Final = 0.25  # maintenance margin, long
MM_SHORT: Final = 0.30  # maintenance margin, short
T0: Final = date(2026, 1, 5)  # trade date
T_DIV: Final = date(2026, 4, 15)  # dividend date
T_EVAL: Final = date(2026, 6, 30)  # valuation date
RATE: Final = 0.065  # margin loan rate
COMMISSION: Final = 15.0  # on the purchase
DIV: Final = 0.40  # dividend per share

type Ledger = list[tuple[date, str, float]]


def long_ratio(P: float, N: float, loan: float) -> float:
    """Return a long position's equity over its value at price P."""
    return (N * P - loan) / (N * P)


def short_ratio(P: float, N: float, credit: float) -> float:
    """Return a short position's equity over its value at price P."""
    return (credit - N * P) / (N * P)


def root(f: Callable[[float], float], lo: float, hi: float) -> float:
    """Return brentq's root of f in [lo, hi] at tight tolerances."""
    return optimize.brentq(f, lo, hi, xtol=1e-14, rtol=1e-15, maxiter=500)


def act360(d1: date, d2: date) -> float:
    """Return the actual/360 year fraction from d1 to d2."""
    return (d2 - d1).days / 360


def check_static(report: CheckReport) -> tuple[float, float]:
    """Check the static call prices against roots; return the (long, short) prices."""
    m0 = M0
    print("== Static case (no interest, fees or income since the trade)")
    print(
        f"  leverage ratio 1/m0 = {1 / m0:.1f}; long loan {N * P0 * (1 - m0):,.2f}; short credit"
        f" balance {N * P0 * (1 + m0):,.2f}"
    )
    p_long = P0 * (1 - m0) / (1 - MM_LONG)
    p_long_root = root(lambda P: long_ratio(P, N, N * P0 * (1 - m0)) - MM_LONG, 1.0, P0)
    report.ok(
        "long margin-call price P0(1 - m0)/(1 - mm) equals the root of equity/value = mm to 1e-12",
        abs(p_long - p_long_root) < 1e-12,
        f"{p_long:.10f}",
    )
    p_short = P0 * (1 + m0) / (1 + MM_SHORT)
    p_short_root = root(lambda P: short_ratio(P, N, N * P0 * (1 + m0)) - MM_SHORT, P0, 10 * P0)
    report.ok(
        "short margin-call price P0(1 + m0)/(1 + mm) equals the root to 1e-12",
        abs(p_short - p_short_root) < 1e-12,
        f"{p_short:.10f}",
    )
    report.ok(
        "at P* the short's maintenance requirement is 30% of value, above $5 a share, so the 30%"
        " leg binds",
        MM_SHORT * p_short >= 5.0 and p_short >= 5.0,
        f"{MM_SHORT * p_short:.4f} a share",
    )
    return p_long, p_short


def check_long_ledger(report: CheckReport, p_long: float) -> None:
    """Rebuild the long loan from its ledger and check the balance-based call price."""
    m0, rate, div = M0, RATE, DIV
    print("== Long position with financing, a commission and a dividend (ledger)")
    ledger: Ledger = []
    loan = N * P0 * (1 - m0)  # the commission is paid in cash with the deposit
    ledger.append((T0, "buy 1,000 at 40.00; 50% initial margin; commission paid in cash", loan))
    interest_1 = loan * rate * act360(T0, T_DIV)
    loan += interest_1
    ledger.append((T_DIV, f"interest {interest_1:.2f} added to the loan", loan))
    loan -= N * div
    ledger.append((T_DIV, f"dividend {N * div:.2f} credited against the loan", loan))
    interest_2 = loan * rate * act360(T_DIV, T_EVAL)
    loan += interest_2
    ledger.append((T_EVAL, f"interest {interest_2:.2f} added to the loan", loan))
    for d, what, bal in ledger:
        print(f"  {d}  {what:<62} loan {bal:,.4f}")
    loan_closed = N * P0 * (1 - m0) * (1 + rate * act360(T0, T_DIV)) - N * div
    loan_closed *= 1 + rate * act360(T_DIV, T_EVAL)
    report.ok(
        "the ledger balance equals the closed-form accrual to 1e-9",
        abs(loan - loan_closed) < 1e-9,
        f"{loan:,.4f}",
    )
    p_long_t = loan / (N * (1 - MM_LONG))
    report.ok(
        "balance-based call price L_t/(N(1 - mm)) equals the root of the equity condition at L_t"
        " to 1e-12",
        abs(p_long_t - root(lambda P: long_ratio(P, N, loan) - MM_LONG, 1.0, P0)) < 1e-12,
        f"{p_long_t:.6f} against the static {p_long:.6f} (difference {p_long_t - p_long:+.6f})",
    )


def check_short_ledger(report: CheckReport, p_short: float) -> None:
    """Rebuild the short credit balance from its ledger and check the call price."""
    m0, div = M0, DIV
    print(
        "== Short position with a rebate, a borrow fee, a commission and a dividend owed (ledger)"
    )
    rebate, fee, comm_s = 0.02, 0.005, 15.0
    credit = N * P0 * (1 + m0) - comm_s
    ledger: Ledger = [
        (T0, "sell short 1,000 at 40.00; 50% margin deposited; commission debited", credit)
    ]
    reb_1 = N * P0 * rebate * act360(T0, T_DIV)
    fee_1 = N * P0 * fee * act360(T0, T_DIV)
    credit += reb_1 - fee_1
    ledger.append((T_DIV, f"rebate {reb_1:.2f} on proceeds less borrow fee {fee_1:.2f}", credit))
    credit -= N * div
    ledger.append((T_DIV, f"dividend {N * div:.2f} owed to the lender debited", credit))
    reb_2 = N * P0 * rebate * act360(T_DIV, T_EVAL)
    fee_2 = N * P0 * fee * act360(T_DIV, T_EVAL)
    credit += reb_2 - fee_2
    ledger.append((T_EVAL, f"rebate {reb_2:.2f} less borrow fee {fee_2:.2f}", credit))
    for d, what, bal in ledger:
        print(f"  {d}  {what:<62} credit {bal:,.4f}")
    p_short_t = credit / (N * (1 + MM_SHORT))
    report.ok(
        "balance-based call price K_t/(N(1 + mm)) equals the root of the equity condition at K_t"
        " to 1e-12",
        abs(p_short_t - root(lambda P: short_ratio(P, N, credit) - MM_SHORT, P0 / 2, 10 * P0))
        < 1e-12,
        f"{p_short_t:.6f} against the static {p_short:.6f} (difference {p_short_t - p_short:+.6f})",
    )


def check_levered_return(report: CheckReport) -> None:
    """Check the levered-return identity against the cash flows, and print a falling case."""
    m0, rate, div, commission = M0, RATE, DIV, COMMISSION
    print("== Levered return on equity: identity against the cash flows")
    P1, comm_sell = 46.0, 15.0
    E0 = N * P0 * m0 + commission
    interest = N * P0 * (1 - m0) * rate * act360(T0, T_EVAL)
    # sell, repay loan and interest; dividend kept as cash
    cash_end = N * P1 - N * P0 * (1 - m0) - interest + N * div - comm_sell
    r_cash = cash_end / E0 - 1
    r_asset = (P1 - P0 + div) / P0
    i_period = rate * act360(T0, T_EVAL)
    r_formula = (
        (r_asset / m0 - i_period * (1 / m0 - 1) - (commission + comm_sell) / (N * P0 * m0))
        * (N * P0 * m0)
        / E0
    )
    report.ok(
        "levered return [r_asset/m0 - i(1/m0 - 1) - commissions/E] x (N P0 m0)/E0 equals the"
        " cash-flow return to 1e-12",
        abs(r_cash - r_formula) < 1e-12,
        f"asset total return {100 * r_asset:.4f}%, levered return on equity {100 * r_cash:.4f}%",
    )
    P1_down = 34.0
    cash_down = N * P1_down - N * P0 * (1 - m0) - interest + N * div - comm_sell
    print(
        f"  at {P1_down:.2f} the asset returns {100 * (P1_down - P0 + div) / P0:.2f}% and the"
        f" equity {100 * (cash_down / E0 - 1):.2f}%"
    )


def main() -> int:
    """Print the versions, then run the four parts with one report.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, SciPy {scipy.__version__}")
    report = CheckReport()
    p_long, p_short = check_static(report)
    check_long_ledger(report, p_long)
    check_short_ledger(report, p_short)
    check_levered_return(report)
    if report.failures:
        print("FAILED:", ", ".join(report.failures))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
