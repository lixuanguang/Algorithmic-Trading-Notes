"""Cross-currency basis swaps: cash flows, the forward they imply and the basis on either leg."""

import sys
from typing import Final

import numpy as np

from trading_notes.numerical.forward_commitment_valuation.cross_currency import CrossCurrencySwap
from trading_notes.numerical.report import CheckReport, print_versions

S: Final = 1.10  # USD per EUR
N_EUR: Final = 100e6
N_USD: Final = S * N_EUR
R_USD: Final = 0.040
R_EUR: Final = 0.025
KAPPA: Final = -0.0020  # spread on the euro leg
TOL_CCY: Final = 1e-6
TOL_REL: Final = 1e-12
SWAP: Final = CrossCurrencySwap(spot=S, usd_rate=R_USD, eur_rate=R_EUR)


def rel(a: float, b: float) -> float:
    """Return |a - b| / |b|."""
    return abs(a - b) / abs(b)


def check_cash_flows(report: CheckReport) -> None:
    """1. Party A's flows by date, and the direction and size of the exchanges."""
    N_eur, N_usd, r_usd, r_eur, kappa = N_EUR, N_USD, R_USD, R_EUR, KAPPA
    print("== 1. cash flows by date and party (three annual periods, assumed fixings)")
    periods, tau = 3, 1.0
    # (date, party A's EUR flow, party A's USD flow); party B is the negative
    rows: list[tuple[str, float, float]] = []
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
    report.ok(
        "initial exchange opposite to the interest flows in each currency",
        bool(np.sign(init_e) == -np.sign(int_e) and np.sign(init_u) == -np.sign(int_u)),
    )
    report.ok(
        "final exchange in the same direction as the interest flows",
        bool(np.sign(fin_e) == np.sign(int_e) and np.sign(fin_u) == np.sign(int_u)),
    )
    report.ok(
        "same principals and spot at both exchanges; A repays the dollars it received",
        abs(fin_u + init_u) <= TOL_CCY
        and abs(fin_e + init_e) <= TOL_CCY
        and rel(-init_u / init_e, S) <= TOL_REL,
    )
    print(
        f"  euro coupon received by A: {int_e:,.0f} (ESTR 2.5% less 20 bp on EUR 100m); dollar"
        f" coupon paid {-int_u:,.0f}"
    )


def check_parity(report: CheckReport) -> None:
    """2. The one-period relation, its mapping to the dollar-leg basis and annualisation."""
    N_eur, N_usd, r_usd, r_eur, kappa = N_EUR, N_USD, R_USD, R_EUR, KAPPA
    print("== 2. one-period relation, convention mapping and annualisation")
    for t in (1.0, 0.25):
        usd_out = N_usd * (1 + r_usd * t)
        eur_in = N_eur * (1 + (r_eur + kappa) * t)
        F = SWAP.forward(t, kappa)
        report.ok(
            f"tau {t:g}: legs at assumed fixings give the forward",
            rel(usd_out / eur_in, F) <= TOL_REL,
            f"F = {F:.6f}",
        )
        F0 = SWAP.forward(t, 0.0)
        report.ok(
            f"tau {t:g}: kappa = 0 reproduces covered parity",
            rel(F0, S * (1 + r_usd * t) / (1 + r_eur * t)) <= TOL_REL,
            f"F_CIP = {F0:.6f}",
        )
        b = SWAP.dollar_basis(F, t)
        F_b = S * (1 + (r_usd + b) * t) / (1 + r_eur * t)
        report.ok(
            f"tau {t:g}: F/S = [1 + (r_usd + b) tau]/[1 + r_f tau] returns the same forward",
            rel(F_b, F) <= TOL_REL,
        )
        b_closed = -kappa * (1 + r_usd * t) / (1 + (r_eur + kappa) * t)
        report.ok(
            f"tau {t:g}: b = -kappa (1 + r_usd tau)/(1 + (r_f + kappa) tau)",
            rel(b, b_closed) <= TOL_REL,
            f"b = {b * 1e4:.4f} bp a year",
        )
        syn = ((F / S) * (1 + r_eur * t) - 1) / t
        report.ok(
            f"tau {t:g}: synthetic dollar rate = r_usd + b > r_usd when kappa < 0",
            rel(syn, r_usd + b) <= TOL_REL and syn > r_usd,
            f"{syn * 100:.4f}% against {r_usd * 100:.1f}%",
        )
        b_period = (F / S) * (1 + r_eur * t) - (1 + r_usd * t)
        print(
            f"  tau {t:g}: period amount b tau = {b_period * 1e4:.4f} bp; annualised b ="
            f" {b * 1e4:.4f} bp"
        )
    b_q = SWAP.dollar_basis(SWAP.forward(0.25, kappa), 0.25)
    b_q_unscaled = b_q * 0.25
    report.ok(
        "tau 0.25: the unannualised amount is a quarter of the spread, not the spread",
        rel(b_q_unscaled * 4, b_q) <= TOL_REL and abs(b_q_unscaled - b_q) > 1e-4,
    )


def check_quote_direction(report: CheckReport) -> None:
    """3. The inverted quote gives the reciprocal forward; the misread quote does not."""
    r_usd, r_eur, kappa = R_USD, R_EUR, KAPPA
    print("== 3. quote direction")
    Q = 1 / S  # euros per dollar
    F = SWAP.forward(1.0, kappa)
    F_Q = Q * (1 + (r_eur + kappa)) / (1 + r_usd)
    report.ok(
        "inverted quote (EUR per USD) gives the reciprocal forward",
        rel(F_Q, 1 / F) <= TOL_REL,
        f"{F_Q:.6f} = 1/{F:.6f}",
    )
    wrong = Q * (1 + r_usd) / (1 + (r_eur + kappa))
    print(
        f"  reported: the EUR-per-USD quote entered as if USD per EUR gives {wrong:.6f}, not"
        f" {F_Q:.6f} or {F:.6f}"
    )


def check_final_exchange(report: CheckReport) -> None:
    """4. The final exchange's value against the fixed-for-fixed swap's."""
    N_eur, N_usd = N_EUR, N_USD
    print("== 4. principal exchange at maturity against the fixed-for-fixed swap")
    for S_T in (1.10, 1.14):
        v_A = N_eur * S_T - N_usd
        print(
            f"  spot {S_T:.2f}: final exchange worth {v_A + 0.0:+,.0f} USD to A,"
            f" {0.0 - v_A:+,.0f} to B"
        )
    v_move = (N_eur * 1.14 - N_usd) - (N_eur * 1.10 - N_usd)
    # meth:swap-valuation-replication: EUR 100m at 1.08, euro to 1.12, party paying euros
    ffx = 108e6 - 1.12 * 100e6
    report.ok(
        "a 0.04 rise in USD per EUR is worth +4.0m to A (receives euros), as the fixed-for-fixed"
        " swap's -4.0m to the euro payer",
        abs(v_move - 4.0e6) <= TOL_CCY and abs(ffx + 4.0e6) <= TOL_CCY,
        f"{v_move:,.0f} and {ffx:,.0f}",
    )


def main() -> int:
    """Print the versions, then run the four parts with one report.

    EUR/USD at S = 1.10 dollars per euro; notionals EUR 100m and USD 110m exchanged at T0 and
    re-exchanged at the same spot at Tn. Party A receives compounded ESTR + kappa on the euro
    notional and pays compounded SOFR on the dollar notional (Hull sec. 7.10; Ding, Liu and
    Rutkowski, Definition 2.4, spread on the non-dollar leg), kappa = -20 bp, assumed fixings 4.0
    and 2.5 percent, accrual exactly tau (ACT/360 compounding in arrears is not modelled). The
    annualised dollar-leg basis (BIS Box A) is b = [(F/S)(1 + r_f tau) - (1 + r_usd tau)] / tau;
    with the foreign-leg kappa, b = -kappa (1 + r_usd tau) / (1 + (r_f + kappa) tau) exactly.
    Tolerances: relative 1e-12 or 1e-6 currency on 100 million. Synthetic inputs.

    Returns:
        The exit status, 0 or 1.
    """
    print_versions(np)
    report = CheckReport()
    check_cash_flows(report)
    check_parity(report)
    check_quote_direction(report)
    check_final_exchange(report)
    return report.summarise()


if __name__ == "__main__":
    sys.exit(main())
