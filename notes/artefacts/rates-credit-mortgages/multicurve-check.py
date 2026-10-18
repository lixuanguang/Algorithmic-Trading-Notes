"""empirical extensions (2026-10-17): own checks behind mod:multi-curve-fra-swap-valuation.

Hull, Options, Futures, and Other Derivatives, 11th Global ed., sec. 7.6, pp. 183-185: value a swap as a portfolio of
FRAs by (1) computing forward rates for the unknown floating rates, (2) taking cash flows at those forwards and (3)
discounting at the risk-free (OIS/SOFR) rate; for a SOFR swap the first rate blends the overnight rates already
observed with the zero rate for the rest of the period. Example 7.1 (pay 3% semiannual, receive six-month SOFR on
$100m, payments at 0.2, 0.7 and 1.2 years; zero rates 2.8, 3.2, 3.4%; 2.3% observed over the last 0.3 years) gives
+0.292 million. Checks: (1) Example 7.1 reproduced; (2) daily compounding of overnight rates implied by a smooth
curve equals the simple forward from discount-factor ratios (the backward-looking SOFR period rate, in expectation
under the forward measure, ignoring convexity and day counts); (3) a two-curve FRA: projecting a term reference rate
(a LIBOR-like curve 30 bp above OIS) and discounting at OIS against projecting and discounting on the single term
curve. Own illustration with invented curves; not market data.
Run: uv run python multicurve-check.py   (standard library). Exits non-zero on failure.
"""

# standard library imports
import math
import sys

fails = []


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


print("== Hull Example 7.1")
z = {0.2: 0.028, 0.7: 0.032, 1.2: 0.034}
first = 0.6 * 0.023 + 0.4 * 0.028
f2 = (z[0.7] * 0.7 - z[0.2] * 0.2) / 0.5
f3 = (z[1.2] * 1.2 - z[0.7] * 0.7) / 0.5
cont = [first, f2, f3]
semi = [2 * (math.exp(r / 2) - 1) for r in cont]
ok(
    "floating rates 2.50, 3.36, 3.68% continuous",
    [round(r * 100, 2) for r in cont] == [2.50, 3.36, 3.68],
)
ok(
    "semiannual 2.516, 3.388, 3.714%",
    [round(r * 100, 3) for r in semi] == [2.516, 3.388, 3.714],
    ", ".join(f"{r * 100:.3f}" for r in semi),
)
pv = sum((0.5 * r * 100 - 1.5) * math.exp(-z[t] * t) for r, t in zip(semi, (0.2, 0.7, 1.2)))
ok("swap value +0.292 million", round(pv, 3) == 0.292, f"{pv:.4f}")

print("== compounded overnight rate over a period equals the forward from discount factors")
P = lambda t: math.exp(-(0.03 + 0.004 * t) * t)  # an invented smooth OIS curve
t1, t2, n = 0.5, 1.0, 126
dt = (t2 - t1) / n
growth = 1.0
for i in range(n):
    a, b = t1 + i * dt, t1 + (i + 1) * dt
    on = (P(a) / P(b) - 1) / dt  # overnight forward rate for each day
    growth *= 1 + on * dt
ok(
    "product of (1 + r_i d_i) = P(t1)/P(t2)",
    abs(growth - P(t1) / P(t2)) < 1e-12,
    f"{growth:.10f} vs {P(t1) / P(t2):.10f}",
)

print("== two curves: term reference rate projected on its own curve, cash flow discounted at OIS")
Pois = lambda t: math.exp(-0.030 * t)
Pref = lambda t: math.exp(-0.033 * t)  # a term-rate curve 30 bp above OIS (invented)
T1, T2, K, N = 1.0, 1.25, 0.034, 100e6
tau = T2 - T1
F_ref = (Pref(T1) / Pref(T2) - 1) / tau
F_ois = (Pois(T1) / Pois(T2) - 1) / tau
v_two = N * tau * (F_ref - K) * Pois(T2)
v_single = N * tau * (F_ref - K) * Pref(T2)
v_wrong = N * tau * (F_ois - K) * Pois(T2)
print(f"     forward on reference curve {F_ref * 100:.4f}%, on OIS {F_ois * 100:.4f}%")
print(
    f"     receive-floating FRA value: two-curve {v_two:,.0f}; single (term) curve {v_single:,.0f}; OIS-projected {v_wrong:,.0f}"
)
ok("discounting choice changes the value", abs(v_two - v_single) > 1)
ok(
    "projection choice changes the value far more than discounting",
    abs(v_two - v_wrong) > 10 * abs(v_two - v_single),
)
if fails:
    print("\nFAILED:", fails)
    sys.exit(1)
print("\nall checks passed")
