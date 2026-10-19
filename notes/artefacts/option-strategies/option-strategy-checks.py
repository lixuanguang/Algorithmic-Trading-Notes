"""Option strategies (2026-10-19): the worked numbers of meth:option-replication-deltas,
meth:covered-call-protective-put, meth:option-spreads-volatility-strategies and ex:option-strategy-selection-case.

Reproduced: Hull, Options, Futures, and Other Derivatives, 11th Global ed. (2022), chap. 12 (bull spread Example 12.2,
bear spread Example 12.3, the 70-strike straddle) and sec. 17.2 (zero-cost range forward 1.3000 / 1.3414, both 0.0273);
Natenberg, Option Volatility and Pricing, 2nd ed. (2015), chap. 17 (covered writes against stock at 100: the 95 call at
6.50 and the 105 call at 2.00; a protective euro call). Original: value, terminal cash-flow and delta identities for synthetic positions with zero, continuous and discrete
dividends, including the -e^(-qT) spot delta of a fixed-strike short forward (added 2026-10-19, PR #25 pass), a protective put and covered call priced by Black-Scholes with financing of the premium, a buy-call
against sell-put comparison for a short seller, a calendar spread valued at the first expiry (value and
profit reported separately since the PR #25 pass), the cost of a collar under
a flat and a skewed volatility curve, and a strategy-selection case for a 10 million holding.

Conventions: value = what the position is worth on the valuation date; profit = value (or payoff at expiry) - premium
paid, with the premium also shown financed to expiry where stated;
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
    "synthetic long forward: long call - short put at K = F costs zero (F = 102.0201, no dividend)",
    abs(bs(S0, S0 * math.exp(R * T), T, R, SIG) - bs(S0, S0 * math.exp(R * T), T, R, SIG, kind="p"))
    < 1e-10,
)
ok(
    "terminal payoffs (any dividend policy): call - put + K pays S_T; stock - call pays K - (K - S_T)+; stock + put"
    " pays (S_T - K)+ + K. Dividends are extra cash to the stockholder only",
    np.allclose(call(ST, K) - put(ST, K) + K, ST)
    and np.allclose(ST - call(ST, K), K - put(ST, K))
    and np.allclose(ST + put(ST, K), call(ST, K) + K),
)
for q_ in (0.0, 0.02):
    c_q, p_q = bs(S0, K, T, R, SIG, q_), bs(S0, K, T, R, SIG, q_, "p")
    pv_div = S0 * (1 - math.exp(-q_ * T))  # PV of the yield paid over the life
    ok(
        f"q = {q_:.0%}: values. Synthetic stock costs S0 e^(-qT) = {S0 * math.exp(-q_ * T):.4f}; stock = synthetic +"
        f" PV(dividends) {pv_div:.4f}; covered call = short put + bond + PV(div); protective put = call + bond +"
        " PV(div)",
        close(c_q - p_q + K * math.exp(-R * T), S0 * math.exp(-q_ * T), 1e-10)
        and close(S0 - c_q, K * math.exp(-R * T) - p_q + pv_div, 1e-10)
        and close(S0 + p_q, c_q + K * math.exp(-R * T) + pv_div, 1e-10),
    )
# discrete dividend: 1.00 paid at three months; options priced on the escrowed price S0 - D (Hull sec. 15.12)
d_amt, t_d = 1.00, 0.25
D = d_amt * math.exp(-R * t_d)
c_d, p_d = bs(S0 - D, K, T, R, SIG), bs(S0 - D, K, T, R, SIG, kind="p")
st_paths = np.array([70.0, 100.0, 130.0])
stock_cash = st_paths + d_amt * math.exp(R * (T - t_d))  # dividend reinvested at r to expiry
synth_cash = call(st_paths, K) - put(st_paths, K) + K
ok(
    "discrete dividend 1.00 at 3 months: p + S0 = c + Ke^(-rT) + D with D = 0.9900; at expiry the stock (dividend"
    " reinvested) exceeds the synthetic by 1.0101 in every state, whose present value is D",
    close(p_d + S0, c_d + K * math.exp(-R * T) + D, 1e-10)
    and np.allclose(stock_cash - synth_cash, d_amt * math.exp(R * (T - t_d)))
    and close(d_amt * math.exp(R * (T - t_d)) * math.exp(-R * T), D, 1e-12),
)


def fd_delta(f, s, h=1e-4):
    return (f(s + h) - f(s - h)) / (2 * h)


for q_ in (0.0, 0.02):
    dc, dp = bs_delta(S0, K, T, R, SIG, q_), bs_delta(S0, K, T, R, SIG, q_, "p")
    fwd_short = fd_delta(lambda s, q_=q_: -(s * math.exp(-q_ * T) - K * math.exp(-R * T)), S0)
    fd_c = fd_delta(lambda s, q_=q_: bs(s, K, T, R, SIG, q_), S0)
    fd_p = fd_delta(lambda s, q_=q_: bs(s, K, T, R, SIG, q_, "p"), S0)
    gap = (-1 + dc) - dp
    ok(
        f"q = {q_:.0%}: spot deltas by finite difference match BSM; a fixed-strike short forward has delta"
        f" -e^(-qT) = {fwd_short:.7f}; call - put = e^(-qT); short stock + call - put delta = {gap:+.7f}"
        " (zero only without dividends)",
        abs(fd_c - dc) < 1e-7
        and abs(fd_p - dp) < 1e-7
        and abs(fwd_short + math.exp(-q_ * T)) < 1e-9
        and abs(dc - dp - math.exp(-q_ * T)) < 1e-12
        and abs(gap - (math.exp(-q_ * T) - 1)) < 1e-12,
        f"call {dc:.4f}, put {dp:.4f}, covered call {1 - dc:.4f}, protective put {1 + dp:.4f}",
    )


def share_plus_forwards(s, n_fwd, q_=0.02):
    """Value of one share (held, dividends to be received) plus n_fwd short fixed-strike forwards."""
    return s - n_fwd * (s * math.exp(-q_ * T) - K * math.exp(-R * T))


ok(
    "at q = 2%, T = 0.5 (finite differences): one share plus one short forward keeps delta +0.00995, although the"
    " forward's payoff slope at expiry is -1; e^(qT) = 1.01005 short forwards per share are needed for delta zero",
    abs(fd_delta(lambda s: share_plus_forwards(s, 1.0), S0) - (1 - math.exp(-0.01))) < 1e-8
    and abs(fd_delta(lambda s: share_plus_forwards(s, 1.0), S0) - 0.00995) < 5e-6
    and abs(fd_delta(lambda s: share_plus_forwards(s, math.exp(0.01)), S0)) < 1e-8,
)
dc, dp = bs_delta(S0, K, T, R, SIG), bs_delta(S0, K, T, R, SIG, kind="p")
ok(
    "no dividend: call delta 0.5840, covered call 0.4160, protective put 0.5840, short stock + call -0.4160",
    abs(dc - 0.5840) < 5e-5 and abs((1 + dp) - 0.5840) < 5e-5 and abs((-1 + dc) + 0.4160) < 5e-5,
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
# calendar spread: sell 3-month 100 call, buy 6-month 100 call. Valuation date: the 3-month expiry, with 0.25 years
# left on the long call and the BSM inputs unchanged. Value = long call - payoff of the expiring short call;
# profit = value - initial cost (premium paid at inception, not financed); the financed profit subtracts the cost
# grown at r for the three months.
c3, c6 = bs(S0, 100, 0.25, R, SIG), bs(S0, 100, 0.5, R, SIG)
cost_cal = c6 - c3
grid_s = (80, 95, 100, 105, 120)
cal_value = [bs(s, 100, 0.25, R, SIG) - max(s - 100, 0) for s in grid_s]
cal_profit = [v - cost_cal for v in cal_value]
cal_profit_fin = [v - cost_cal * math.exp(R * 0.25) for v in cal_value]
ok(
    "calendar spread (buy 6m, sell 3m 100 calls, cost 2.141842): at the 3-month expiry its value is 0.052704,"
    " 2.190593, 4.485236, 2.747684 and 1.108320 at 80-120; profits after the cost are -2.089, +0.049, +2.343,"
    " +0.606 and -1.034, peaking at the strike",
    abs(cost_cal - 2.141842) < 5e-7
    and np.allclose(cal_value, [0.052704, 2.190593, 4.485236, 2.747684, 1.108320], atol=5e-7)
    and min(cal_value) > 0
    and cal_profit[2] == max(cal_profit)
    and cal_profit[0] < 0 < cal_profit[2],
    "value "
    + " ".join(f"{x:.6f}" for x in cal_value)
    + "; profit "
    + " ".join(f"{x:+.3f}" for x in cal_profit),
)
ok(
    "value never falls below zero (the long call is worth at least the expiring call's payoff), so the maximum loss"
    " is the 2.141842 cost; financing the cost at 4% for three months lowers every profit by 0.021526",
    all(v >= 0 for v in cal_value)
    and np.allclose(
        np.subtract(cal_profit, cal_profit_fin), cost_cal * (math.exp(R * 0.25) - 1), atol=1e-12
    )
    and abs(cost_cal * (math.exp(R * 0.25) - 1) - 0.021526) < 5e-7,
)
ok(
    "a long calendar spread is long vega: at inception, a 2-point rise in implied volatility raises its value",
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
