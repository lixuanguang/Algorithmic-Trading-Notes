"""Library gap-filling Batch L2, package P11c (2026-10-21): the worked examples of meth:margin-purchase-leverage.

Deterministic, original inputs. Percentages from the rule texts read on 2026-10-21: Regulation T (12 CFR 220.12, eCFR
up to date as of 19 October 2026) sets initial margin at 50 percent of market value for a long margin equity security
and 150 percent for a short sale; FINRA Rule 4210(c) (version from 4 June 2026) sets maintenance at 25 percent of
market value for long margin securities and, for a short stock at $5 or above, the greater of $5 a share or 30 percent.
Brokers may set higher house requirements (Rule 4210(d)).

Margin-call prices (assumptions as corrected after the L2 audit): the static formulas P* = P0 (1 - m0)/(1 - mm) (long)
and P0 (1 + m0)/(1 + mm) (short) assume the loan or the credit balance is unchanged since the trade. With interest,
fees, dividends or other flows, the call price is computed from the balance at the date: P* = L_t / (N (1 - mm)) for a
long position and K_t / (N (1 + mm)) for a short one. Each formula is checked against a numerical root of the
equity-to-value condition, and the balances are rebuilt from a dated cash-flow ledger (actual/360 simple interest).

Run: uv run python margin-purchase-check.py   (scipy). Exits 1 on failure.
"""

# standard library imports
import sys
from datetime import date

# third party library imports
import scipy
from scipy import optimize

print(f"Python {sys.version.split()[0]}, SciPy {scipy.__version__}")
fails = []


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


def long_ratio(P, N, loan):
    return (N * P - loan) / (N * P)


def short_ratio(P, N, credit):
    return (credit - N * P) / (N * P)


def root(f, lo, hi):
    return optimize.brentq(f, lo, hi, xtol=1e-14, rtol=1e-15, maxiter=500)


N, P0, m0 = 1_000, 40.0, 0.50
mm_long, mm_short = 0.25, 0.30
print("== Static case (no interest, fees or income since the trade)")
print(
    f"  leverage ratio 1/m0 = {1 / m0:.1f}; long loan {N * P0 * (1 - m0):,.2f}; short credit balance {N * P0 * (1 + m0):,.2f}"
)
p_long = P0 * (1 - m0) / (1 - mm_long)
p_long_root = root(lambda P: long_ratio(P, N, N * P0 * (1 - m0)) - mm_long, 1.0, P0)
ok(
    "long margin-call price P0(1 - m0)/(1 - mm) equals the root of equity/value = mm to 1e-12",
    abs(p_long - p_long_root) < 1e-12,
    f"{p_long:.10f}",
)
p_short = P0 * (1 + m0) / (1 + mm_short)
p_short_root = root(lambda P: short_ratio(P, N, N * P0 * (1 + m0)) - mm_short, P0, 10 * P0)
ok(
    "short margin-call price P0(1 + m0)/(1 + mm) equals the root to 1e-12",
    abs(p_short - p_short_root) < 1e-12,
    f"{p_short:.10f}",
)
ok(
    "at P* the short's maintenance requirement is 30% of value, above $5 a share, so the 30% leg binds",
    mm_short * p_short >= 5.0 and p_short >= 5.0,
    f"{mm_short * p_short:.4f} a share",
)


def act360(d1, d2):
    return (d2 - d1).days / 360


print("== Long position with financing, a commission and a dividend (ledger)")
t0, t_div, t_eval = date(2026, 1, 5), date(2026, 4, 15), date(2026, 6, 30)
rate, commission, div = 0.065, 15.0, 0.40
ledger = []
loan = N * P0 * (1 - m0)  # the commission is paid in cash with the deposit
ledger.append((t0, "buy 1,000 at 40.00; 50% initial margin; commission paid in cash", loan))
interest_1 = loan * rate * act360(t0, t_div)
loan += interest_1
ledger.append((t_div, f"interest {interest_1:.2f} added to the loan", loan))
loan -= N * div
ledger.append((t_div, f"dividend {N * div:.2f} credited against the loan", loan))
interest_2 = loan * rate * act360(t_div, t_eval)
loan += interest_2
ledger.append((t_eval, f"interest {interest_2:.2f} added to the loan", loan))
for d, what, bal in ledger:
    print(f"  {d}  {what:<62} loan {bal:,.4f}")
loan_closed = N * P0 * (1 - m0) * (1 + rate * act360(t0, t_div)) - N * div
loan_closed *= 1 + rate * act360(t_div, t_eval)
ok(
    "the ledger balance equals the closed-form accrual to 1e-9",
    abs(loan - loan_closed) < 1e-9,
    f"{loan:,.4f}",
)
p_long_t = loan / (N * (1 - mm_long))
ok(
    "balance-based call price L_t/(N(1 - mm)) equals the root of the equity condition at L_t to 1e-12",
    abs(p_long_t - root(lambda P: long_ratio(P, N, loan) - mm_long, 1.0, P0)) < 1e-12,
    f"{p_long_t:.6f} against the static {p_long:.6f} (difference {p_long_t - p_long:+.6f})",
)

print("== Short position with a rebate, a borrow fee, a commission and a dividend owed (ledger)")
rebate, fee, comm_s = 0.02, 0.005, 15.0
credit = N * P0 * (1 + m0) - comm_s
ledger = [(t0, "sell short 1,000 at 40.00; 50% margin deposited; commission debited", credit)]
reb_1 = N * P0 * rebate * act360(t0, t_div)
fee_1 = N * P0 * fee * act360(t0, t_div)
credit += reb_1 - fee_1
ledger.append((t_div, f"rebate {reb_1:.2f} on proceeds less borrow fee {fee_1:.2f}", credit))
credit -= N * div
ledger.append((t_div, f"dividend {N * div:.2f} owed to the lender debited", credit))
reb_2 = N * P0 * rebate * act360(t_div, t_eval)
fee_2 = N * P0 * fee * act360(t_div, t_eval)
credit += reb_2 - fee_2
ledger.append((t_eval, f"rebate {reb_2:.2f} less borrow fee {fee_2:.2f}", credit))
for d, what, bal in ledger:
    print(f"  {d}  {what:<62} credit {bal:,.4f}")
p_short_t = credit / (N * (1 + mm_short))
ok(
    "balance-based call price K_t/(N(1 + mm)) equals the root of the equity condition at K_t to 1e-12",
    abs(p_short_t - root(lambda P: short_ratio(P, N, credit) - mm_short, P0 / 2, 10 * P0)) < 1e-12,
    f"{p_short_t:.6f} against the static {p_short:.6f} (difference {p_short_t - p_short:+.6f})",
)

print("== Levered return on equity: identity against the cash flows")
P1, comm_sell = 46.0, 15.0
E0 = N * P0 * m0 + commission
interest = N * P0 * (1 - m0) * rate * act360(t0, t_eval)
cash_end = (
    N * P1 - N * P0 * (1 - m0) - interest + N * div - comm_sell
)  # sell, repay loan and interest; dividend kept as cash
r_cash = cash_end / E0 - 1
r_asset = (P1 - P0 + div) / P0
i_period = rate * act360(t0, t_eval)
r_formula = (
    (r_asset / m0 - i_period * (1 / m0 - 1) - (commission + comm_sell) / (N * P0 * m0))
    * (N * P0 * m0)
    / E0
)
ok(
    "levered return [r_asset/m0 - i(1/m0 - 1) - commissions/E] x (N P0 m0)/E0 equals the cash-flow return to 1e-12",
    abs(r_cash - r_formula) < 1e-12,
    f"asset total return {100 * r_asset:.4f}%, levered return on equity {100 * r_cash:.4f}%",
)
P1_down = 34.0
cash_down = N * P1_down - N * P0 * (1 - m0) - interest + N * div - comm_sell
print(
    f"  at {P1_down:.2f} the asset returns {100 * (P1_down - P0 + div) / P0:.2f}% and the equity"
    f" {100 * (cash_down / E0 - 1):.2f}%"
)

if fails:
    print("FAILED:", ", ".join(fails))
    sys.exit(1)
print("all checks passed")
