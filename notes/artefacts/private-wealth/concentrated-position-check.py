"""Library gap-filling Batch L6, package L6-b (2026-10-21): the concentrated-position example of
meth:complex-client-situations and the zero-cost collar of meth:covered-call-protective-put.

Inputs and acceptance were fixed before the first run.
Synthetic: 100,000 shares at 50, basis 10 per share, an assumed flat 20 percent tax on the gain (illustrative, not a
statutory rate), one year, r = 4 percent continuously compounded, q = 0, volatility 30 percent, BSM option values.
Strategies: outright sale (proceeds held riskless, to isolate exposure); a zero-cost collar (long 45 put, short call
at the strike that makes the premiums equal); a variable prepaid forward on terms patterned on the structure in
Rev. Rul. 2003-7 (deliver all N shares below F = 50, shares worth N F between F and C = 62.5, N F / C shares above),
advance = BSM present value of the delivery, with no dealer spread. Also: Portfolio Management in Practice, Vol. 1,
chap. 16, Exhibit 15 (exchange fund against sale) reproduced, and the annual fee that equates them (Interpretation).
Deterministic; no tax treatment is computed except the sale's, and none is implied for the collar or forward.

Run: uv run python concentrated-position-check.py   Exits 1 on failure.
"""

# standard library imports
import math
import sys

# third party library imports
import scipy
from scipy import stats

print(f"Python {sys.version.split()[0]}, SciPy {scipy.__version__}")
fails = []


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


Nsh, S0, basis, tax, r, sig, T = 100_000, 50.0, 10.0, 0.20, 0.04, 0.30, 1.0
K1, F, C = 45.0, 50.0, 62.5
N = stats.norm.cdf


def call(K):
    d1 = (math.log(S0 / K) + (r + sig**2 / 2) * T) / (sig * math.sqrt(T))
    return S0 * N(d1) - K * math.exp(-r * T) * N(d1 - sig * math.sqrt(T))


def put(K):
    return call(K) - S0 + K * math.exp(-r * T)


print("== options: parity, zero-cost collar strike, prepaid-forward advance")
d1 = (math.log(S0 / K1) + (r + sig**2 / 2) * T) / (sig * math.sqrt(T))
put_direct = K1 * math.exp(-r * T) * N(-d1 + sig * math.sqrt(T)) - S0 * N(-d1)
ok(
    "put-call parity (direct BSM put against c - S + K e^{-rT})",
    abs(put_direct - put(K1)) <= 1e-10,
    f"put 45 = {put(K1):.6f}",
)
lo, hi = S0, 3 * S0
for _ in range(200):
    mid = 0.5 * (lo + hi)
    lo, hi = (mid, hi) if call(mid) > put(K1) else (lo, mid)
K2 = 0.5 * (lo + hi)
ok(
    "zero-cost collar: call at K2 worth the 45 put",
    abs(call(K2) - put(K1)) <= 1e-10,
    f"K2 = {K2:.4f}",
)
adv1 = Nsh * (S0 - call(F) + F / C * call(C))
adv2 = Nsh * (F * math.exp(-r * T) - put(F) + F / C * call(C))
ok(
    "advance by two routes: S0 - c(F) + (F/C) c(C) = F e^{-rT} - p(F) + (F/C) c(C) (a loan plus a collar)",
    abs(adv1 / adv2 - 1) <= 1e-10,
    f"{adv1:,.2f}, {adv1 / (Nsh * S0):.2%} of the 5,000,000 position",
)

print("== terminal values per strategy (before any tax on the hedged positions)")
sale_cash = Nsh * S0 - tax * Nsh * (S0 - basis)
# First run (recorded): the frozen hand values (tax 900,000; 4,267,328.43) were wrong; the gain is 4,000,000, so the tax
# is 800,000 and 4,200,000 x e^0.04 = 4,371,405.25 (hand: e^0.04 = 1.0408107742). Literals corrected; tolerance unchanged.
ok(
    "sale: tax 800,000, 4,200,000 reinvested, 4,371,405.25 after a year at 4 percent",
    abs(tax * Nsh * (S0 - basis) - 800_000) <= 0.01
    and abs(sale_cash * math.exp(r * T) - 4_371_405.25) <= 0.01,
    f"{sale_cash * math.exp(r * T):,.2f}",
)
grid = (30.0, 40.0, 50.0, 60.0, 70.0, 80.0)
rows, exact, decomp, shares_ok = [], True, True, True
for ST in grid:
    delivered = Nsh * ST if ST < F else (Nsh * F if ST <= C else Nsh * F / C * ST)
    delivered_opt = Nsh * (ST - max(ST - F, 0) + F / C * max(ST - C, 0))
    retained = Nsh * ST - delivered
    retained_opt = Nsh * (max(ST - F, 0) - F / C * max(ST - C, 0))
    nshares = delivered / ST
    exact &= retained + delivered == Nsh * ST
    decomp &= (
        abs(delivered - delivered_opt) <= 1e-9 * Nsh * ST
        and abs(retained - retained_opt) <= 1e-9 * Nsh * ST
    )
    shares_ok &= Nsh * F / C - 1e-9 <= nshares <= Nsh + 1e-9
    collar = Nsh * min(max(ST, K1), K2)
    vpf = retained + adv1 * math.exp(r * T)
    rows.append((ST, Nsh * ST, collar, vpf, sale_cash * math.exp(r * T), nshares))
ok("prepaid forward: retained plus delivered value equals N S_T on the grid", exact)
ok("prepaid forward: payoffs equal their option decomposition", decomp)
ok("prepaid forward: delivered shares between 0.8 N and N (a variable number)", shares_ok)
print("    S_T   hold          collar        prepaid fwd   sale          shares delivered")
for ST, hold, col, vpf, sale, ns in rows:
    print(f"    {ST:4.0f}  {hold:12,.0f}  {col:12,.0f}  {vpf:12,.0f}  {sale:12,.0f}  {ns:9,.0f}")

print("== exchange fund against sale (PMiP Exhibit 15) and the break-even fee")
mv, b, rate, g, yrs = 1_000_000, 100_000, 0.25, 0.10, 7
inv = mv - rate * (mv - b)
s7 = inv * (1 + g) ** yrs
e7 = mv * (1 + g) ** yrs
fin_s = s7 - rate * (s7 - inv)
fin_e = e7 - rate * (e7 - b)
printed = (775_000, 1_510_256, 1_948_717, 183_814, 462_179, 1_326_442, 1_486_538)
mine = (inv, s7, e7, rate * (s7 - inv), rate * (e7 - b), fin_s, fin_e)
ok(
    "Exhibit 15 reproduced to the dollar",
    all(abs(a - p) <= 1 for a, p in zip(mine, printed, strict=True)),
    ", ".join(f"{x:,.0f}" for x in mine),
)


def fund_final(fee):
    v = mv * (1 + g - fee) ** yrs
    return v - rate * (v - b)


lo, hi = 0.0, g
for _ in range(200):
    mid = 0.5 * (lo + hi)
    lo, hi = (mid, hi) if fund_final(mid) > fin_s else (lo, mid)
print(f"    break-even annual fee (deducted from the 10 percent return): {0.5 * (lo + hi):.4%}")

if fails:
    print("FAILED:", ", ".join(fails))
    sys.exit(1)
print("all checks passed")
