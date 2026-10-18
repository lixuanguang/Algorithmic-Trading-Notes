"""Option strategies (2026-10-19): the worked numbers of meth:option-replication-deltas,
meth:covered-call-protective-put, meth:option-spreads-volatility-strategies and ex:option-strategy-selection-case.

Reproduced: Hull, Options, Futures, and Other Derivatives, 11th Global ed. (2022), chap. 12 (bull spread Example 12.2,
bear spread Example 12.3, the 70-strike straddle) and sec. 17.2 (zero-cost range forward 1.3000 / 1.3414, both 0.0273);
Natenberg, Option Volatility and Pricing, 2nd ed. (2015), chap. 17 (covered writes against stock at 100: the 95 call at
6.50 and the 105 call at 2.00; a protective euro call). Original: payoff identities for synthetic positions, deltas of
hedged positions, a protective put and covered call priced by Black-Scholes with financing of the premium, a buy-call
against sell-put comparison for a short seller, a calendar spread valued at the first expiry, the cost of a collar under
a flat and a skewed volatility curve, and a strategy-selection case for a 10 million holding.

Conventions: profit = payoff at expiry - premium paid, with the premium also shown financed to expiry where stated;
Black-Scholes prices with continuous dividend yield; per share unless stated.

Count convention: one check is one executed ok() call (a call inside a loop counts once per iteration).

Run: uv run python option-strategy-checks.py   (numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import math
import sys

# third party library imports
import numpy as np
import scipy
from scipy.optimize import brentq
from scipy.stats import norm

print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
fails = []


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


def bs(s, k, t, r, sig, q=0.0, kind="c"):
    d1 = (math.log(s / k) + (r - q + sig**2 / 2) * t) / (sig * math.sqrt(t))
    d2 = d1 - sig * math.sqrt(t)
    if kind == "c":
        return s * math.exp(-q * t) * norm.cdf(d1) - k * math.exp(-r * t) * norm.cdf(d2)
    return k * math.exp(-r * t) * norm.cdf(-d2) - s * math.exp(-q * t) * norm.cdf(-d1)


def bs_delta(s, k, t, r, sig, q=0.0, kind="c"):
    d1 = (math.log(s / k) + (r - q + sig**2 / 2) * t) / (sig * math.sqrt(t))
    return math.exp(-q * t) * (norm.cdf(d1) if kind == "c" else norm.cdf(d1) - 1)


def call(st, k):
    return np.maximum(st - k, 0.0)


def put(st, k):
    return np.maximum(k - st, 0.0)


ST = np.linspace(0, 200, 401)

print("== part 1: replicating asset returns with options, and the deltas of hedged positions")
S0, K, T, R, Q, SIG = 100.0, 100.0, 0.5, 0.04, 0.0, 0.20
c, p = bs(S0, K, T, R, SIG), bs(S0, K, T, R, SIG, kind="p")
ok(
    "synthetic long stock: long call + short put + bond paying K has payoff S_T at every price and costs S0",
    np.allclose(call(ST, K) - put(ST, K) + K, ST)
    and close(c - p + K * math.exp(-R * T), S0, 1e-10),
)
ok(
    "synthetic long forward: long call - short put at K = F costs zero (F = 102.0201)",
    abs(bs(S0, S0 * math.exp(R * T), T, R, SIG) - bs(S0, S0 * math.exp(R * T), T, R, SIG, kind="p"))
    < 1e-10,
)
ok(
    "covered call = stock - call = short put + bond (payoff identity) and their costs agree",
    np.allclose(ST - call(ST, K), K - put(ST, K))
    and close(S0 - c, K * math.exp(-R * T) - p, 1e-10),
)
ok(
    "protective put = stock + put = call + bond",
    np.allclose(ST + put(ST, K), call(ST, K) + K)
    and close(S0 + p, c + K * math.exp(-R * T), 1e-10),
)
dc, dp = bs_delta(S0, K, T, R, SIG), bs_delta(S0, K, T, R, SIG, kind="p")
deltas = {
    "long stock": 1.0,
    "short forward": -1.0,
    "synthetic long (call - put)": dc - dp,
    "covered call": 1 - dc,
    "protective put": 1 + dp,
    "short stock + long call": -1 + dc,
}
ok(
    "deltas: stock +1, short forward -1, call - put +1 exactly (no dividend), covered call 1 - 0.5840 = 0.4160,"
    " protective put 1 - 0.4160 = 0.5840, short stock + call = put delta -0.4160",
    close(deltas["synthetic long (call - put)"], 1.0, 1e-12)
    and abs(dc - 0.5840) < 5e-5
    and close(deltas["covered call"], -dp, 1e-12)
    and close(deltas["short stock + long call"], dp, 1e-12),
    " ".join(f"{k_}: {v:+.4f}" for k_, v in deltas.items()),
)
ok(
    "with a 2% dividend yield the synthetic long has delta e^{-qT} = 0.9900, below the stock's 1",
    abs(bs_delta(S0, K, T, R, SIG, 0.02) - bs_delta(S0, K, T, R, SIG, 0.02, "p") - math.exp(-0.01))
    < 1e-12,
)

print("== part 2: covered calls, protective puts and short-position hedges")
ok(
    "Natenberg: stock at 100, sell the 95 call at 6.50 -> break-even 93.50, maximum profit 1.50 (the time premium)",
    95 + 6.5 - 100 == 1.5 and 100 - 6.5 == 93.5,
)
ok(
    "sell the 105 call at 2.00 instead -> break-even 98, maximum profit 7 at or above 105",
    100 - 2 == 98 and 105 + 2 - 100 == 7,
)
cc_profit = np.minimum(ST, 105) + 2 - 100
ok(
    "covered-call profit is the short-put shape: capped at 7, loss 98 - S_T below 98",
    cc_profit.max() == 7 and close(cc_profit[ST == 60][0], -38),
)
pp = bs(S0, 95, T, R, SIG, kind="p")
pp_fin = pp * math.exp(R * T)
pp_profit = ST + put(ST, 95) - 100 - pp
ok(
    "protective put: 95 put costs 2.6786; max loss 100 - 95 + premium = 7.68 (7.73 with the premium financed);"
    " break-even 102.68 (102.73 financed)",
    abs(pp - 2.6786) < 5e-5
    and abs(-pp_profit.min() - 7.68) < 5e-3
    and abs(100 - 95 + pp_fin - 7.73) < 5e-3
    and abs(100 + pp - 102.68) < 5e-3,
    f"{pp:.4f}",
)
ok(
    "Natenberg's euro hedge: buying the 1.40 call on EUR 1m at 0.02 caps the cost at 1.42m all in; at 1.25 the firm"
    " pays 1.27m",
    1.40e6 + 0.02e6 == 1.42e6 and 1.25e6 + 0.02e6 == 1.27e6,
)
# a short seller at 100 hedges with a long 105 call or a short 95 put (both six months)
c105 = bs(S0, 105, T, R, SIG)
p95 = pp
short_call_hedge = (100 - ST) + (call(ST, 105) - c105)
short_put_write = (100 - ST) + (p95 - put(ST, 95))
ok(
    "short stock + long 105 call: loss capped at 5 + 4.3770 = 9.38 however high the stock goes",
    abs(c105 - 4.3770) < 5e-5 and abs(short_call_hedge.min() + 5 + c105) < 1e-9,
    f"{c105:.4f}",
)
ok(
    "short stock + short 95 put: the 2.68 premium only cushions; the loss is unlimited as the stock rises and the gain is"
    " capped at 7.68 below 95",
    short_put_write[-1] < -50 and abs(short_put_write.max() - (5 + p95)) < 1e-9,
)

print("== part 3: spreads, straddles, collars, calendar spreads, and skew")
bull = call(ST, 30) - call(ST, 35) - 2
ok(
    "Hull Example 12.2 bull spread (buy 30 call at 3, sell 35 call at 1): profit -2, S_T - 32, +3",
    bull.min() == -2 and bull.max() == 3,
)
bear = put(ST, 35) - put(ST, 30) - 2
ok(
    "Hull Example 12.3 bear spread (buy 35 put at 3, sell 30 put at 1): profit +3 below 30, -2 above 35",
    bear.max() == 3 and bear.min() == -2,
)
strad = lambda s: max(s - 70, 0) + max(70 - s, 0) - 7
ok(
    "Hull straddle at 70 (call 4, put 3): -6 at 69, -7 at 70, +13 at 90, +8 at 55; break-evens 63 and 77",
    (strad(69), strad(70), strad(90), strad(55), strad(63), strad(77)) == (-6, -7, 13, 8, 0, 0),
)
k1 = 1.30
k2 = brentq(
    lambda k: (
        bs(1.32, k, 0.25, 0.02, 0.14, q=0.02) - bs(1.32, k1, 0.25, 0.02, 0.14, q=0.02, kind="p")
    ),
    1.31,
    1.45,
)
ok(
    "Hull sec. 17.2 zero-cost range forward: a 1.3000 put and a 1.3414 call are both worth 0.0273",
    abs(k2 - 1.3414) < 5e-5
    and abs(bs(1.32, k1, 0.25, 0.02, 0.14, q=0.02, kind="p") - 0.0273) < 5e-5,
)
# calendar spread: sell 3-month 100 call, buy 6-month 100 call; value at the first expiry
c3, c6 = bs(S0, 100, 0.25, R, SIG), bs(S0, 100, 0.5, R, SIG)
cost_cal = c6 - c3
cal = [bs(s, 100, 0.25, R, SIG) - max(s - 100, 0) - cost_cal for s in (80, 95, 100, 105, 120)]
ok(
    "calendar spread (buy 6m, sell 3m 100 calls, cost 2.1418): at the 3-month expiry it profits near 100 and loses"
    " most of its cost far from 100",
    abs(cost_cal - 2.1418) < 5e-4
    and cal[2] > 0
    and cal[0] < 0
    and cal[4] < 0
    and cal[2] == max(cal),
    " ".join(f"{x:+.3f}" for x in cal),
)
ok(
    "a long calendar spread is long vega: a 2-point rise in implied volatility raises its value",
    bs(S0, 100, 0.5, R, 0.22) - bs(S0, 100, 0.25, R, 0.22) > cost_cal,
)


def skew_vol(k, atm=0.20, slope=-0.30):
    """Equity-style skew: implied volatility falls 3 points per 10% of moneyness."""
    return atm + slope * math.log(k / S0)


put90_flat = bs(S0, 90, T, R, 0.20, kind="p")
put90_skew = bs(S0, 90, T, R, skew_vol(90), kind="p")
k_flat = brentq(lambda k: bs(S0, k, T, R, 0.20) - put90_flat, 100, 150)
k_skew = brentq(lambda k: bs(S0, k, T, R, skew_vol(k)) - put90_skew, 100, 150)
ok(
    "zero-cost collar with a 90 put: flat 20% volatility allows a 116.80 call; with the skew the dearer put (23.2%)"
    " forces the call strike down to 110.29",
    abs(k_flat - 116.80) < 0.01
    and abs(k_skew - 110.29) < 0.01
    and abs(skew_vol(90) - 0.2316) < 5e-4,
    f"flat {k_flat:.2f}, skew {k_skew:.2f}",
)

collar_profit = np.minimum(np.maximum(ST, 90), k_flat) - 100
ok(
    "bear spread break-even 33; zero-cost collar (stock 100, 90 put, 116.80 call): max gain 16.80, max loss 10,"
    " break-even 100",
    abs(bear[np.argmin(np.abs(ST - 33))]) < 1e-9
    and abs(collar_profit.max() - (k_flat - 100)) < 1e-9
    and abs(collar_profit.min() + 10) < 1e-9
    and abs(k_flat - 116.80) < 0.005,
)

print("== part 4: strategy selection for a 10 million single-stock holding (100,000 shares at 100)")
n, s0 = 100_000, 100.0
T6 = 0.5
put85 = bs(s0, 85, T6, R, skew_vol(85), kind="p")
call110 = bs(s0, 110, T6, R, skew_vol(110))
call115 = bs(s0, 115, T6, R, skew_vol(115))
k_c = brentq(lambda k: bs(s0, k, T6, R, skew_vol(k)) - put85, 100, 160)
alts = {
    "protective 85 put": (n * put85, 1 + bs_delta(s0, 85, T6, R, skew_vol(85), kind="p")),
    "covered 110 call": (-n * call110, 1 - bs_delta(s0, 110, T6, R, skew_vol(110))),
    "zero-cost 85/k collar": (
        0.0,
        1
        + bs_delta(s0, 85, T6, R, skew_vol(85), kind="p")
        - bs_delta(s0, k_c, T6, R, skew_vol(k_c)),
    ),
}
ok(
    "85 put (24.9% implied) costs 1.24% of the holding (124k); a 110 call (17.1%) raises 2.05%; the zero-cost"
    " collar's call strike is 113.05",
    abs(put85 / s0 - 0.0124) < 5e-4
    and abs(call110 / s0 - 0.0205) < 5e-4
    and abs(k_c - 113.05) < 0.01,
    f"put {put85:.4f}, call110 {call110:.4f}, collar call {k_c:.2f}",
)
ok(
    "deltas per share: protective put 0.870, covered 110 call 0.713, zero-cost collar 0.667 (a third less exposure"
    " for no premium)",
    all(
        abs(alts[a][1] - v) < 0.001
        for a, v in (
            ("protective 85 put", 0.870),
            ("covered 110 call", 0.713),
            ("zero-cost 85/k collar", 0.667),
        )
    ),
    " ".join(f"{a}: {v[1]:.3f}" for a, v in alts.items()),
)
scen = {"-30%": 70.0, "-10%": 90.0, "flat": 100.0, "+10%": 110.0, "+30%": 130.0}
res = {}
for name, st in scen.items():
    stock = st - s0
    res[name] = (
        stock,
        stock + max(85 - st, 0) - put85 * math.exp(R * T6),
        stock - max(st - 110, 0) + call110 * math.exp(R * T6),
        stock + max(85 - st, 0) - max(st - k_c, 0),
    )
ok(
    "in a 30% fall the put and the collar stop the loss near 15 (put -16.27 with financed premium, collar -15.00);"
    " the covered call loses 27.91",
    abs(res["-30%"][1] + 16.27) < 0.01
    and abs(res["-30%"][3] + 15.0) < 1e-9
    and abs(res["-30%"][2] + 27.91) < 0.01,
)
ok(
    "in a 30% rise the stock alone earns 30; put 28.73, covered call 12.09, collar 13.05",
    abs(res["+30%"][1] - 28.73) < 0.01
    and abs(res["+30%"][2] - 12.09) < 0.01
    and abs(res["+30%"][3] - 13.05) < 0.01,
)
d110 = bs_delta(s0, 110, T6, R, skew_vol(110))
d100 = bs_delta(s0, 100, T6, R, 0.20)
ok(
    "to cut exposure to 60% with 110 calls would take 1.39 calls per share, more calls than shares (partly naked);"
    " at-the-money calls need 0.685 per share, fully covered",
    abs(0.4 / d110 - 1.391) < 0.001 and 0.4 / d110 > 1 and abs(0.4 / d100 - 0.685) < 0.001,
)
atm = bs(s0, 100, T6, R, 0.20)
ok(
    "to raise exposure to 125% without buying stock, buy 0.25/0.584 = 0.428 at-the-money calls per share, a premium of"
    " 0.284m (2.8% of the holding) against 2.5m of stock",
    abs(0.25 / d100 - 0.428) < 0.001 and abs(0.25 / d100 * n * atm / 1e6 - 0.284) < 0.001,
)

print()
if fails:
    print(f"{len(fails)} check(s) failed: {fails}")
    sys.exit(1)
print("all checks passed")
