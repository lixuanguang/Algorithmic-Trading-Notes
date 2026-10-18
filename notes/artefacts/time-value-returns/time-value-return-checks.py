"""Batch 2 foundations (2026-10-18): the worked examples of def:return-measures (holding-period, price and total
returns; arithmetic and geometric means), def:required-return-components, meth:instrument-present-value and
res:cash-flow-additivity.

Each closed-form result is checked against an independent route: explicit cash-flow summation, a ledger of the
replicating trades, root finding by bisection, or the alternative formula. Annual compounding and end-of-year cash
flows throughout unless stated. Corrections of 2026-10-18 (plan sec. 10.2): dated forward-lending cash flows, uncertain inflation, yield quotation.
Inputs are invented; they illustrate the mechanics, not any security.
Run: uv run python time-value-return-checks.py   (standard library). Exits 1 on failure.
"""

# standard library imports
import math
import sys

fails = []


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


def close(a, b, tol=5e-5):
    return abs(a - b) <= tol


def bisect(f, lo, hi, n=200):
    flo = f(lo)
    for _ in range(n):
        mid = (lo + hi) / 2
        if (f(mid) > 0) == (flo > 0):
            lo, flo = mid, f(mid)
        else:
            hi = mid
    return (lo + hi) / 2


print("== holding-period, price and total return of a share")
p0, p1, div = 50.00, 54.00, 1.20
price_ret = p1 / p0 - 1
income_ret = div / p0
total_ret = (p1 + div) / p0 - 1
ok("price return 8.0%", close(price_ret, 0.08))
ok("income return 2.4%", close(income_ret, 0.024))
ok(
    "total = price + income return (one period, income at the end)",
    close(total_ret, price_ret + income_ret) and close(total_ret, 0.104),
)

gross_end, fee = 1000 * 1.08, 0.01 * 1000
ok("net of a 1% fee on opening assets: 7.0%", close((gross_end - fee) / 1000 - 1, 0.07))

print("== price index against total-return index, dividend reinvested at the ex-date close")
# Two periods of one share: prices 100 -> 102 (ex-dividend 2 paid in period 1) -> 105.
prices, divs = [100.0, 102.0, 105.0], [0.0, 2.0, 0.0]
pr_index, tr_index = [100.0], [100.0]
for t in (1, 2):
    pr_index.append(pr_index[-1] * prices[t] / prices[t - 1])
    tr_index.append(tr_index[-1] * (prices[t] + divs[t]) / prices[t - 1])
# Independent route: hold one share, reinvest the dividend in shares at 102.
shares = 1 + divs[1] / prices[1]
ledger_value = shares * prices[2]
ok("price index 105.00", close(pr_index[-1], 105.0))
ok(
    "total-return index equals the reinvested holding",
    close(tr_index[-1], ledger_value),
    f"{tr_index[-1]:.4f}",
)
ok("total return 7.0588%", close(tr_index[-1] / 100 - 1, 0.070588))

print("== arithmetic against geometric mean")
rets = [0.20, -0.10, 0.05]
arith = sum(rets) / len(rets)
growth = math.prod(1 + r for r in rets)
geo = growth ** (1 / len(rets)) - 1
ok("arithmetic mean 5.0000%", close(arith, 0.05))
ok("geometric mean 4.2808%", close(geo, 0.042808, 2e-6), f"{geo:.6f}")
ok(
    "geometric compounds to the realised wealth",
    close((1 + geo) ** 3, growth) and close(growth, 1.134),
)
ok("geometric below arithmetic for unequal returns", geo < arith)
var = sum((r - arith) ** 2 for r in rets) / len(rets)
ok(
    "approximation geo ~ arith - var/2 (population variance) gives 4.25%",
    close(arith - var / 2, 0.0425, 1e-12),
    f"{arith - var / 2:.6f}",
)
ok("equal returns: the means coincide", close((1.05**3) ** (1 / 3) - 1, 0.05, 1e-12))

print("== required-return components (Fisher exact and approximate; additive premia)")
real, infl = 0.015, 0.025
nominal = (1 + real) * (1 + infl) - 1
ok("exact Fisher nominal 4.0375%", close(nominal, 0.040375))
ok(
    "additive approximation error = real * inflation",
    close(nominal - (real + infl), real * infl, 1e-12),
)
ok(
    "real from nominal: (1.08/1.03) - 1 = 4.8544% (the existing entry)",
    close(1.08 / 1.03 - 1, 0.048544),
)
ok(
    "high inflation: 10% nominal, 20% inflation -> exact real -8.3333%, approximation -10%",
    close(1.10 / 1.20 - 1, -0.083333, 1e-6) and close(0.10 - 0.20, -0.10, 1e-12),
)
ok(
    "uncertain inflation: deflating by mean inflation gives 0%, mean realised real return 0.8333%",
    close(1.10 / (1 + (0.0 + 0.20) / 2) - 1, 0.0, 1e-12)
    and close(sum(1.10 / (1 + h) - 1 for h in (0.0, 0.20)) / 2, 0.0083333, 1e-6),
)
ok(
    "realised real return is convex in inflation (Jensen): mean exceeds value at the mean",
    sum(1.10 / (1 + h) - 1 for h in (0.0, 0.20)) / 2 > 1.10 / 1.10 - 1,
)
ok(
    "continuously compounded rates add exactly",
    close(math.log(1 + nominal), math.log(1 + real) + math.log(1 + infl), 1e-12),
)
irp, credit, liquidity, erp = 0.003, 0.012, 0.003, 0.050
nominal_rf_yield = nominal + irp
ok("nominal risk-free yield with inflation risk premium 4.3375%", close(nominal_rf_yield, 0.043375))
ok("corporate bond required yield 5.8375%", close(nominal_rf_yield + credit + liquidity, 0.058375))
ok("equity required return 9.3375%", close(nominal_rf_yield + erp, 0.093375))

print(
    "== present values: zero, coupon bond (single yield and spot rates), preferred, constant and two-stage growth"
)
zero = 1000 / 1.04**3
ok("zero-coupon 888.9964", close(zero, 888.996359, 1e-4), f"{zero:.6f}")
cf = [5, 5, 105]
price_y = sum(c / 1.04**t for t, c in enumerate(cf, 1))
annuity = 5 * (1 - 1.04**-3) / 0.04 + 100 / 1.04**3
ok(
    "coupon bond at 4% = 102.7751 by summation and annuity formula",
    close(price_y, annuity, 1e-9) and close(price_y, 102.775091, 1e-4),
    f"{price_y:.6f}",
)
spots = [0.030, 0.038, 0.041]
price_s = sum(c / (1 + z) ** t for (t, c), z in zip(enumerate(cf, 1), spots))
ok("coupon bond at spot rates 102.5709", close(price_s, 102.570853, 1e-5), f"{price_s:.6f}")
ytm_s = bisect(lambda y: sum(c / (1 + y) ** t for t, c in enumerate(cf, 1)) - price_s, 0.0, 0.2)
ok(
    "its yield 4.0723% lies between the spot rates and nearest the 3-year rate",
    close(ytm_s, 0.040723, 2e-6) and spots[0] < ytm_s < spots[2],
    f"{ytm_s:.6f}",
)
pref = 6 / 0.075
pref_sum = sum(6 / 1.075**t for t in range(1, 3001))
ok(
    "preferred perpetuity 80.00 (truncated sum agrees)",
    close(pref, 80.0) and close(pref_sum, 80.0, 1e-6),
)
d0, g, r = 2.00, 0.04, 0.09
d1 = d0 * (1 + g)
gordon = d1 / (r - g)
gordon_sum = sum(d0 * (1 + g) ** t / (1 + r) ** t for t in range(1, 3001))
ok(
    "constant growth 41.60 (truncated sum agrees)",
    close(gordon, 41.60) and close(gordon_sum, 41.60, 1e-4),
)
# Two stage: 10% growth for years 1-2, 4% thereafter, r = 9%.
d_1, d_2 = d0 * 1.10, d0 * 1.10**2
terminal = d_2 * 1.04 / (0.09 - 0.04)  # value at year 2 of dividends from year 3
two_stage = d_1 / 1.09 + (d_2 + terminal) / 1.09**2
two_sum = d_1 / 1.09 + d_2 / 1.09**2 + sum(d_2 * 1.04**k / 1.09 ** (2 + k) for k in range(1, 4000))
ok(
    "two-stage 46.4220 (truncated sum agrees)",
    close(two_stage, 46.422018, 1e-5) and close(two_sum, two_stage, 1e-4),
    f"{two_stage:.6f}",
)
ok("terminal value 50.3360 at year 2", close(terminal, 50.336, 1e-6))

print("== semiannual cash flows: effective against nominal (bond-equivalent) annual yields")
half_eff = 1.10**0.5 - 1
pv_eff = 5 / (1 + half_eff) + 105 / (1 + half_eff) ** 2
y_nom = 2 * half_eff
pv_nom = 5 / (1 + y_nom / 2) + 105 / (1 + y_nom / 2) ** 2
ok(
    "10% effective annual: half-year rate 4.8809%, value 100.2218584",
    close(half_eff, 0.048809, 1e-6) and close(pv_eff, 100.2218584, 1e-7),
)
ok(
    "equivalent nominal 9.7618% compounded semiannually gives the same value",
    close(y_nom, 0.097618, 1e-6) and close(pv_nom, pv_eff, 1e-10),
)
ok("halving the effective rate misprices: 100.00", close(5 / 1.05 + 105 / 1.05**2, 100.0, 1e-10))

print("== implied returns and growth")
ytm = bisect(lambda y: sum(c / (1 + y) ** t for t, c in enumerate(cf, 1)) - 98.00, 0.0, 0.2)
ok("yield of the 5% 3-year bond priced 98.00 is 5.7447%", close(ytm, 0.057447, 2e-6), f"{ytm:.6f}")
ok(
    "repricing at that yield returns 98.00",
    close(sum(c / (1 + ytm) ** t for t, c in enumerate(cf, 1)), 98.00, 1e-8),
)
ok("implied required return D1/P0 + g = 9%", close(d1 / 41.60 + g, 0.09))
g_impl = (0.09 * 52 - d0) / (52 + d0)
ok("implied growth at price 52: 4.9630%", close(g_impl, 0.049630, 2e-6), f"{g_impl:.6f}")
ok(
    "Gordon value at the implied growth returns 52",
    close(d0 * (1 + g_impl) / (0.09 - g_impl), 52.0, 1e-9),
)
g_bis = bisect(lambda gg: d0 * (1 + gg) / (0.09 - gg) - 52, 0.0, 0.0899)
ok("bisection agrees with the closed form", close(g_bis, g_impl, 1e-9))

print("== cash-flow additivity: forward rate, forward FX, option by replication and parity")
z1, z2 = 0.030, 0.038
f12 = (1 + z2) ** 2 / (1 + z1) - 1
ok("1-year rate one year forward 4.6062%", close(f12, 0.046062, 2e-6), f"{f12:.6f}")
# Ledger: buy a 2-year zero paying 1,000; finance it by a 1-year borrowing; at year 1 refinance at the forward.
cost = 1000 / (1 + z2) ** 2
repay_y1 = cost * (1 + z1)
ok("two-year zero paying 1,000 costs 928.1225", close(cost, 928.122482, 1e-5))
# Correction of 2026-10-18 (plan sec. 10.2): check the dated cash flows of the trades themselves; no future rate assumed.
# Buy the 2-year zero, borrow its cost for 1 year: flows (t0, t1, t2) = (0, -repay, +1000).
flows_lend = (-cost + cost, -repay_y1, 1000.0)
ok(
    "forward lending: flows 0, -955.9662, +1000",
    close(flows_lend[0], 0, 1e-12)
    and close(flows_lend[1], -955.966157, 1e-5)
    and flows_lend[2] == 1000.0,
)
ok(
    "rate earned from year 1 to year 2 equals the implied forward",
    close(flows_lend[2] / -flows_lend[1] - 1, f12, 1e-12),
)
# Reverse: short the 2-year zero, lend the proceeds for 1 year: (0, +955.9662, -1000), forward borrowing.
flows_borrow = tuple(-x for x in flows_lend)
ok(
    "forward borrowing: flows 0, +955.9662, -1000",
    close(flows_borrow[1], 955.966157, 1e-5) and flows_borrow[2] == -1000.0,
)
# Rolling the year-1 debt into a new loan at an unknown future rate is not a lock-in: at 8% it costs 1,032.4434.
ok(
    "refinancing at a later 8% spot costs 1,032.4434, not 1,000",
    close(repay_y1 * 1.08, 1032.443449, 1e-5),
)
f12_c = (2 * math.log(1 + z2) - math.log(1 + z1)) / 1
ok(
    "continuous version (Hull eq. 4.5) agrees after conversion",
    close(math.exp(f12_c) - 1, f12, 1e-12),
)

spot, i_usd, i_eur = 1.1000, 0.040, 0.025  # USD per EUR; one year, annual compounding
fwd = spot * (1 + i_usd) / (1 + i_eur)
ok("forward 1.116098 USD per EUR", close(fwd, 1.116098, 1e-6), f"{fwd:.6f}")
# Ledger: borrow USD 1,100, buy EUR 1,000, deposit at 2.5%, sell EUR 1,025 forward; repay USD 1,144.
ok(
    "covered position nets zero at the forward",
    close(1000 * (1 + i_eur) * fwd - 1100 * (1 + i_usd), 0.0, 1e-9),
)
ok("forward points +160.98 (pips of 0.0001)", close((fwd - spot) * 1e4, 160.98, 0.01))

s0, su, sd, k, rf = 50.0, 60.0, 40.0, 50.0, 0.05  # one period; rf simple for the period
cu, cd = max(su - k, 0), max(sd - k, 0)
delta = (cu - cd) / (su - sd)
bond_pv = (cd - delta * sd) / (1 + rf)
call = delta * s0 + bond_pv
ok(
    "call replication: 0.5 share and borrowing 19.0476 -> 5.9524",
    close(delta, 0.5) and close(bond_pv, -19.047619, 1e-6) and close(call, 5.952381, 1e-6),
)
ok(
    "replicating portfolio pays the call in both states",
    close(delta * su + bond_pv * (1 + rf), cu, 1e-12)
    and close(delta * sd + bond_pv * (1 + rf), cd, 1e-12),
)
q = ((1 + rf) * s0 - sd) / (su - sd)
ok(
    "risk-neutral expectation gives the same value",
    close((q * cu + (1 - q) * cd) / (1 + rf), call, 1e-12),
)
pu, pd = max(k - su, 0), max(k - sd, 0)
put_rep = (pu - pd) / (su - sd) * s0 + (pd - (pu - pd) / (su - sd) * sd) / (1 + rf)
put_parity = call + k / (1 + rf) - s0
ok(
    "put by replication equals put by parity 3.5714",
    close(put_rep, put_parity, 1e-12) and close(put_parity, 3.571429, 1e-6),
)
ok(
    "parity holds state by state: call - put = share - K",
    all(close(max(s - k, 0) - max(k - s, 0), s - k, 1e-12) for s in (su, sd, 47.3)),
)

if fails:
    print("FAILED:", ", ".join(fails))
    sys.exit(1)
print("all checks passed")
