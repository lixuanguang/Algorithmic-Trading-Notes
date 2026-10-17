"""Checks for the second macro markets and pricing review follow-up (2026-10-16). Standard library only; exits non-zero on failure.

1. FX carry with separate accrual fractions (macro-fx.tex, mod:fx-carry-trade): covered parity, exact funded P&L,
   carry, first-order forms and the continuously compounded log excess return, for 90 days at 5% ACT/360
   against 2% ACT/365.
2. Zero carry of the DV01-hedged convexity position (interest-rates.tex, Practice): long 100 face of a 10-year
   4% annual-coupon bond at par, short k times the face of a 4% 2-year bond at par, flat 4% curve, financing
   and rebate both at 4%: carry 4 - 4k + 4(k - 1) = 0 for any k, with k = 4.30 from the DV01 ratio.
3. Interest rate swaps within the BIS OTC interest rate derivatives (monetary-policy-curves.tex, swaps entry):
   bis-otc-ird-instruments.csv is an extract of the BIS bulk file WS_OTC_DERIV2_csv_flat.zip (data.bis.org,
   retrieved 2026-10-16, sha256 49e5b5c5...a67e923): half-yearly notional outstanding, all reporting countries,
   all counterparties, all currencies and maturities, net-net basis, USD millions.
4. Peak years of the 15-64 and 35-69 populations (macro-regimes-data.tex, Gliner's Table 12.2 countries):
   wpp2024-working-prime-age.csv sums five-year age groups of the UN World Population Prospects 2024, medium
   variant, file WPP2024_PopulationByAge5GroupSex_Medium.csv.gz (population.un.org, retrieved 2026-10-16,
   sha256 a04d7d14...2487cd), 1 July populations 1950-2100 (estimates to 2023, projections after). Peaks are
   taken over 1950-2100 and, for comparison with Gliner's table, which stops at 2050, over 1950-2050.
5. Best-quote flow when a price moves away (order-books.tex, def:order-flow-imbalance): Cont, Kukanov and
   Stoikov's e_n uses the old size, Cont, Cucuringu and Zhang's printed OF^{m,b} the new one.
6. Foucault, Kadan and Kandel's Proposition 4 (high-frequency-trading.tex, mod:make-take-fee-speed-race) against
   Lehalle and Laruelle's (A.4), with s*Delta = Delta_FKK/2, Gamma = L and r = gamma/beta.
"""
import csv
import math
import os
import sys

fails = []


def check(name, got, want, tol):
    ok = abs(got - want) <= tol
    print(f"  {'ok ' if ok else 'BAD'} {name}: {got:.8f} (want {want}, tol {tol})")
    if not ok:
        fails.append(name)


print("1. FX carry, unequal day-count bases")
days, i_d, i_f = 90, 0.05, 0.02
tau_d, tau_f = days / 360, days / 365
S0 = 1.0
F = S0 * (1 + i_d * tau_d) / (1 + i_f * tau_f)
check("tau_f", tau_f, 0.246575, 5e-7)
check("F/S0", F / S0, 1.0075314, 5e-8)


def pnl(ST):
    """Arithmetic funded P&L per unit of domestic currency borrowed: buy foreign, invest, convert back, repay."""
    return ST / S0 * (1 + i_f * tau_f) - (1 + i_d * tau_d)


carry = pnl(S0)
check("carry = i_f tau_f - i_d tau_d (%)", 100 * carry, -0.75685, 5e-6)
check("carry identity", carry, i_f * tau_f - i_d * tau_d, 1e-15)
check("common-basis carry would be (%)", 100 * (i_f - i_d) * tau_d, -0.75, 1e-12)
check("hedged at F gives zero", F / S0 * (1 + i_f * tau_f) - (1 + i_d * tau_d), 0.0, 1e-15)
s = 0.01
P = pnl(S0 * (1 + s))
check("Pi(+1%) exact (%)", 100 * P, 0.24808, 5e-6)
check("Pi = carry + s + s i_f tau_f", P, carry + s + s * i_f * tau_f, 1e-15)
check("first order carry + s (%)", 100 * (carry + s), 0.24315, 5e-6)
x = math.log(1 + s) + math.log(1 + i_f * tau_f) - math.log(1 + i_d * tau_d)
check("log excess x (%)", 100 * x, 0.24472, 5e-6)
check("e^x - 1 = Pi/(1 + i_d tau_d)", math.exp(x) - 1, P / (1 + i_d * tau_d), 1e-15)
r_d, r_f = math.log(1 + i_d * tau_d) / tau_d, math.log(1 + i_f * tau_f) / tau_d
check("x with cc rates on common tau", math.log(1 + s) + (r_f - r_d) * tau_d, x, 1e-15)
check("forward premium exact", (F - S0) / S0, (i_d * tau_d - i_f * tau_f) / (1 + i_f * tau_f), 1e-15)

print("2. Convexity hedge carry on a flat 4% curve")


def price(c, y, n):
    return sum(c / (1 + y) ** t for t in range(1, n + 1)) + 100 / (1 + y) ** n


def dv01(c, y, n):
    return (price(c, y - 1e-4, n) - price(c, y + 1e-4, n)) / 2


k = dv01(4, 0.04, 10) / dv01(4, 0.04, 2)
check("hedge ratio k", k, 4.30, 0.005)
check("10y at par", price(4, 0.04, 10), 100.0, 1e-9)
check("2y at par", price(4, 0.04, 2), 100.0, 1e-9)
# Per 100 of 10y face, one year: receive the 10y coupon 4, pay the short 2y coupons 4k; the short's proceeds
# 100k earn the 4% rebate and the long's 100 is financed at 4%, a net 4k - 4 = 4(k - 1).
coupon_long, fin_long, coupons_short, rebate = 4.0, 4.0, 4.0 * k, 4.0 * k
carry_conv = coupon_long - coupons_short + (rebate - fin_long)
check("carry 4 - 4k + 4(k-1)", carry_conv, 4 - 4 * k + 4 * (k - 1), 1e-12)
check("carry is zero", carry_conv, 0.0, 1e-12)
for kk in (1.0, 2.5, 7.0):
    check(f"zero for k={kk}", 4 - 4 * kk + 4 * (kk - 1), 0.0, 1e-12)
for dy in (0.01, -0.01):
    g = (price(4, 0.04 + dy, 10) - 100) - k * (price(4, 0.04 + dy, 2) - 100)
    check(f"hedged P&L for {dy:+.2f}", g, 0.274 if dy > 0 else 0.302, 0.0015)

print("3. BIS interest rate derivatives by instrument")
bis = {}
for r in csv.DictReader(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bis-otc-ird-instruments.csv"))):
    bis[(r["period"], r["risk"], r["instrument"])] = float(r["notional_usd_millions"]) / 1e6   # USD trillions
for per in ("2024-S1", "2025-S2"):
    ird = bis[(per, "D", "A")]
    parts = sum(bis[(per, "D", i)] for i in "MNRZ")
    check(f"{per} instruments sum to IRD total", parts, ird, 0.01)
    print(f"  {per}: all OTC {bis[(per, 'A', 'A')]:.1f}tn, IRD {ird:.1f}tn ({100 * ird / bis[(per, 'A', 'A')]:.1f}%), "
          f"swaps {bis[(per, 'D', 'N')]:.1f}tn ({100 * bis[(per, 'D', 'N')] / ird:.1f}% of IRD), "
          f"FRAs {100 * bis[(per, 'D', 'M')] / ird:.1f}%, options {100 * bis[(per, 'D', 'R')] / ird:.1f}%")
check("2024-S1 IRD matches the release's $579tn", bis[("2024-S1", "D", "A")], 579, 0.5)
check("2025-S2 swap share of IRD (%)", 100 * bis[("2025-S2", "D", "N")] / bis[("2025-S2", "D", "A")], 81.4, 0.05)

print("4. UN WPP 2024 peak years")
pop = {}
for r in csv.DictReader(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "wpp2024-working-prime-age.csv"))):
    pop.setdefault(r["country"], {})[int(r["year"])] = (float(r["pop_15_64_thousands"]), float(r["pop_35_69_thousands"]))
gliner = {"Germany": (2006, 1986), "Japan": (2016, 1992), "Netherlands": (2012, 1989), "United Kingdom": (2012, 2009),
          "United States": (2016, 2007), "China": (2032, 2011), "Korea": (2023, 2015), "Russia": (2025, 2011),
          "Spain": (2022, 2004), "India": (2050, 2027), "Indonesia": (2050, 2023), "Nigeria": (2050, 2050),
          "Philippines": (2050, 2037)}   # (35-69 peak, 15-64 peak), Table 12.2, macro-pricing-risk-checks.py section 15
peaks = {}
for c, (g_prime, g_work) in gliner.items():
    ys = pop[c]
    assert sorted(ys) == list(range(1950, 2101)), c
    pk = lambda idx, hi: max((y for y in ys if y <= hi), key=lambda y: ys[y][idx])
    peaks[c] = (pk(0, 2100), pk(1, 2100), pk(0, 2050), pk(1, 2050))
    print(f"  {c:15} 15-64 peak {peaks[c][0]} (to 2050: {peaks[c][2]}; Gliner {g_work});"
          f"  35-69 peak {peaks[c][1]} (to 2050: {peaks[c][3]}; Gliner {g_prime})")
check("Japan 15-64 peak", peaks["Japan"][0], 1995, 0)
check("Germany 35-69 peak", peaks["Germany"][1], 2024, 0)
check("United States 15-64 still rising in 2100", peaks["United States"][0], 2100, 0)
check("China 15-64 peak", peaks["China"][0], 2015, 0)

print("5. OFI conventions on one bid move")


def e_cks(pb0, qb0, pb1, qb1, pa0, qa0, pa1, qa1):
    return ((pb1 >= pb0) * qb1 - (pb1 <= pb0) * qb0 - (pa1 <= pa0) * qa1 + (pa1 >= pa0) * qa0)


def of_ccz(p0, q0, p1, q1, side):
    if side == "b":
        return q1 if p1 > p0 else (q1 - q0 if p1 == p0 else -q1)
    return -q1 if p1 > p0 else (q1 - q0 if p1 == p0 else q1)


# bid falls from 100.00 x 300 to 99.99 x 500; ask unchanged at 100.01 x 400
cks = e_cks(100.00, 300, 99.99, 500, 100.01, 400, 100.01, 400)
ccz = of_ccz(100.00, 300, 99.99, 500, "b") - of_ccz(100.01, 400, 100.01, 400, "a")
check("CKS: bid falls, minus the old size", cks, -300, 0)
check("CCZ: bid falls, minus the new size", ccz, -500, 0)
# unchanged prices: both give the size changes
check("same when prices unchanged", e_cks(100, 300, 100, 350, 101, 400, 101, 380),
      of_ccz(100, 300, 100, 350, "b") - of_ccz(101, 400, 101, 380, "a"), 0)

print("6. FKK Proposition 4 and Lehalle-Laruelle (A.4)")
for (D, L, cbar, M, N, beta, gamma) in [(0.01, 0.05, 0.003, 50, 100, 1.0, 2.0), (0.02, 0.03, 0.001, 200, 20, 3.0, 0.5)]:
    q, r = M / N, gamma / beta
    cm_fkk = 0.5 * (D - 2 * (L - cbar) / (1 + (q * r) ** (1 / 3)))
    pim, pit = (L - cbar) / (1 + (q * r) ** (1 / 3)), (L - cbar) / (1 + (q * r) ** (-1 / 3))
    cm_ll = D / 2 - (L - cbar) / (1 + (M / N * gamma / beta) ** (1 / 3))
    check(f"c_m FKK = LL (Delta={D}, M/N={q})", cm_fkk, cm_ll, 1e-15)
    check("pi_m + pi_t = L - cbar", pim + pit, L - cbar, 1e-15)
    check("pi_m = Delta/2 - c_m", pim, D / 2 - cm_fkk, 1e-15)

print("FAILURES:", fails if fails else "none")
sys.exit(1 if fails else 0)
