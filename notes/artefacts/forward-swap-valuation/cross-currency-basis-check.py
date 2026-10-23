"""Library gap-filling Batch L4, package L4-c (2026-10-21): the worked numbers of meth:cross-currency-basis-swaps.

Conventions: EUR/USD quoted as
S = 1.10 dollars per euro; constant notionals EUR 100m and USD 110m exchanged at T0 and re-exchanged at the same spot at
Tn. Party A pays euros and receives dollars at T0, then receives compounded ESTR + kappa on the euro notional and pays
compounded SOFR on the dollar notional each period, and at Tn pays the dollars back and receives the euros (Hull sec.
7.10; Ding, Liu and Rutkowski, arXiv v3, Definition 2.4, spread on the non-dollar leg). kappa = -20 bp. Assumed
fixings 4.0 percent (SOFR) and 2.5 percent (ESTR) per year, accrual exactly tau (real contracts accrue ACT/360 on
rates compounded in arrears; not modelled). Three annual periods for the cash-flow table; one period at tau = 1 and
tau = 0.25 for the parity relation.

Annualised dollar-leg basis (BIS Box A, written with tau): b = [(F/S)(1 + r_f tau) - (1 + r_usd tau)] / tau, so that
F/S = [1 + (r_usd + b) tau] / [1 + r_f tau]; with the foreign-leg kappa, F/S = (1 + r_usd tau) / (1 + (r_f + kappa) tau)
and exactly b = -kappa (1 + r_usd tau) / (1 + (r_f + kappa) tau). The period amount is b tau.

All checks deterministic, fixed before the first run: relative 1e-12, or 1e-6 currency on 100 million. Synthetic
inputs; not evidence about the size of the basis in any market.

Run: uv run --frozen --no-editable python cross-currency-basis-check.py   Exits 1 on failure.
"""

# standard library imports
import sys

# third party library imports
import numpy as np

print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}")
fails = []


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


def rel(a, b):
    return abs(a - b) / abs(b)


S, N_eur = 1.10, 100e6
N_usd = S * N_eur
r_usd, r_eur, kappa = 0.040, 0.025, -0.0020
TOL_CCY, TOL_REL = 1e-6, 1e-12

print("== 1. cash flows by date and party (three annual periods, assumed fixings)")
periods, tau = 3, 1.0
rows = []  # (date, party A's EUR flow, party A's USD flow); party B is the negative
rows.append(("T0", -N_eur, +N_usd))
for j in range(1, periods + 1):
    eur = N_eur * (r_eur + kappa) * tau
    usd = -N_usd * r_usd * tau
    if j == periods:
        eur, usd = eur + N_eur, usd - N_usd
    rows.append((f"T{j}", eur, usd))
print(f"  {'date':4} {'A: EUR':>16} {'A: USD':>16} {'B: EUR':>16} {'B: USD':>16}")
for d, e, u in rows:
    print(f"  {d:4} {e:16,.0f} {u:16,.0f} {-e:16,.0f} {-u:16,.0f}")
init_e, init_u = rows[0][1], rows[0][2]
int_e = N_eur * (r_eur + kappa) * tau
int_u = -N_usd * r_usd * tau
fin_e, fin_u = rows[-1][1] - int_e, rows[-1][2] - int_u
ok(
    "initial exchange opposite to the interest flows in each currency",
    np.sign(init_e) == -np.sign(int_e) and np.sign(init_u) == -np.sign(int_u),
)
ok(
    "final exchange in the same direction as the interest flows",
    np.sign(fin_e) == np.sign(int_e) and np.sign(fin_u) == np.sign(int_u),
)
ok(
    "same principals and spot at both exchanges; A repays the dollars it received",
    abs(fin_u + init_u) <= TOL_CCY
    and abs(fin_e + init_e) <= TOL_CCY
    and rel(-init_u / init_e, S) <= TOL_REL,
)
print(
    f"  euro coupon received by A: {int_e:,.0f} (ESTR 2.5% less 20 bp on EUR 100m); dollar coupon paid {-int_u:,.0f}"
)


def forward_from_kappa(t, k):
    """One-period forward implied by the swap legs at assumed fixings: USD paid per EUR received at the end."""
    return S * (1 + r_usd * t) / (1 + (r_eur + k) * t)


def b_from_forward(F, t):
    return ((F / S) * (1 + r_eur * t) - (1 + r_usd * t)) / t


print("== 2. one-period relation, convention mapping and annualisation")
for t in (1.0, 0.25):
    usd_out = N_usd * (1 + r_usd * t)
    eur_in = N_eur * (1 + (r_eur + kappa) * t)
    F = forward_from_kappa(t, kappa)
    ok(
        f"tau {t:g}: legs at assumed fixings give the forward",
        rel(usd_out / eur_in, F) <= TOL_REL,
        f"F = {F:.6f}",
    )
    F0 = forward_from_kappa(t, 0.0)
    ok(
        f"tau {t:g}: kappa = 0 reproduces covered parity",
        rel(F0, S * (1 + r_usd * t) / (1 + r_eur * t)) <= TOL_REL,
        f"F_CIP = {F0:.6f}",
    )
    b = b_from_forward(F, t)
    F_b = S * (1 + (r_usd + b) * t) / (1 + r_eur * t)
    ok(
        f"tau {t:g}: F/S = [1 + (r_usd + b) tau]/[1 + r_f tau] returns the same forward",
        rel(F_b, F) <= TOL_REL,
    )
    b_closed = -kappa * (1 + r_usd * t) / (1 + (r_eur + kappa) * t)
    ok(
        f"tau {t:g}: b = -kappa (1 + r_usd tau)/(1 + (r_f + kappa) tau)",
        rel(b, b_closed) <= TOL_REL,
        f"b = {b * 1e4:.4f} bp a year",
    )
    syn = ((F / S) * (1 + r_eur * t) - 1) / t
    ok(
        f"tau {t:g}: synthetic dollar rate = r_usd + b > r_usd when kappa < 0",
        rel(syn, r_usd + b) <= TOL_REL and syn > r_usd,
        f"{syn * 100:.4f}% against {r_usd * 100:.1f}%",
    )
    b_period = (F / S) * (1 + r_eur * t) - (1 + r_usd * t)
    print(
        f"  tau {t:g}: period amount b tau = {b_period * 1e4:.4f} bp; annualised b = {b * 1e4:.4f} bp"
    )
b_q = b_from_forward(forward_from_kappa(0.25, kappa), 0.25)
b_q_unscaled = b_q * 0.25
ok(
    "tau 0.25: the unannualised amount is a quarter of the spread, not the spread",
    rel(b_q_unscaled * 4, b_q) <= TOL_REL and abs(b_q_unscaled - b_q) > 1e-4,
)

print("== 3. quote direction")
Q = 1 / S  # euros per dollar
F = forward_from_kappa(1.0, kappa)
F_Q = Q * (1 + (r_eur + kappa)) / (1 + r_usd)
ok(
    "inverted quote (EUR per USD) gives the reciprocal forward",
    rel(F_Q, 1 / F) <= TOL_REL,
    f"{F_Q:.6f} = 1/{F:.6f}",
)
wrong = Q * (1 + r_usd) / (1 + (r_eur + kappa))
print(
    f"  reported: the EUR-per-USD quote entered as if USD per EUR gives {wrong:.6f}, not {F_Q:.6f} or {F:.6f}"
)

print("== 4. principal exchange at maturity against the fixed-for-fixed swap")
for S_T in (1.10, 1.14):
    v_A = N_eur * S_T - N_usd
    print(
        f"  spot {S_T:.2f}: final exchange worth {v_A + 0.0:+,.0f} USD to A, {0.0 - v_A:+,.0f} to B"
    )
v_move = (N_eur * 1.14 - N_usd) - (N_eur * 1.10 - N_usd)
ffx = (
    108e6 - 1.12 * 100e6
)  # meth:swap-valuation-replication: EUR 100m at 1.08, euro to 1.12, party paying euros
ok(
    "a 0.04 rise in USD per EUR is worth +4.0m to A (receives euros), as the fixed-for-fixed swap's -4.0m to the euro payer",
    abs(v_move - 4.0e6) <= TOL_CCY and abs(ffx + 4.0e6) <= TOL_CCY,
    f"{v_move:,.0f} and {ffx:,.0f}",
)

print("FAILED: " + ", ".join(fails) if fails else "all checks passed")
sys.exit(1 if fails else 0)
