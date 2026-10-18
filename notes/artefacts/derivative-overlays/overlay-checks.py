"""Derivative overlays for portfolio exposures (2026-10-19): the worked numbers of meth:forward-commitment-risk-overlays,
meth:volatility-derivative-applications, meth:derivative-overlay-allocation and ex:endowment-derivative-overlay-case.

Reproduced from Hull, Options, Futures, and Other Derivatives, 11th Global ed. (2022): the duration-based hedge of
Example 6.5 (79 contracts), changing a portfolio's beta with index futures (sec. 3.5: 30, 15 and long 10 contracts),
the VIX futures gain of Example 15.8 ($800), and the variance and volatility swaps of Examples 26.4-26.5 (1.69 and 1.82
million, with E(V) = 0.0621 from the strip of option prices). From Managing Investment Portfolios (2007), chap. 6: the
interest-rate parity forward (EUR 0.7880 per dollar) and the hedged-return comparison of Japanese and Canadian bonds.
Original: a receive-fixed swap that lengthens a bond portfolio, an equity swap that turns cash into index exposure, a
currency-hedged return, variance-swap P&L in vega and variance units, a VIX futures roll in contango, a synthetic shift
from 60/40 to 50/50, implied probabilities from a call spread and from a meeting-dated OIS, and an endowment's choice
between cash and futures for rebalancing and a tactical tilt (illustrative costs and prices, not quotes).

Count convention: one check is one executed ok() call (a call inside a loop counts once per iteration).

Run: uv run python overlay-checks.py   (numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import math
import sys

# third party library imports
import numpy as np
import scipy
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


print("== part 1: rates, currencies and equities: swaps, forwards and futures that modify risk")
n_dur = 10_000_000 * 6.80 / (93_062.50 * 9.20)
ok(
    "Hull Example 6.5: hedging 10m of bonds (duration 6.80) with T-bond futures at 93-02 (duration 9.20): 79 contracts",
    abs(n_dur - 79.42) < 0.005 and round(n_dur) == 79,
    f"{n_dur:.2f}",
)
# lengthen duration: 200m portfolio, duration 5.0 -> 6.5 with 10-year futures (DV01 per contract 75) or a 10-year swap
port, d_now, d_tgt = 200e6, 5.0, 6.5
dv01_gap = port * (d_tgt - d_now) * 1e-4
fut_dv01 = 75.0
ok(
    "raising a 200m portfolio from duration 5.0 to 6.5 needs 30,000 of DV01: 400 futures at 75 each",
    close(dv01_gap, 30_000, 1e-6) and close(dv01_gap / fut_dv01, 400, 1e-9),
)
swap_dv01_per_m = (
    0.0001 * sum(math.exp(-0.04 * t) for t in range(1, 11)) * 1e6
)  # annual receive-fixed, 4% flat curve
notional_m = dv01_gap / swap_dv01_per_m  # millions of notional
ok(
    "or a 10-year annual receive-fixed swap (DV01 807.8 per million on a flat 4% continuous curve): 37.14m notional",
    abs(swap_dv01_per_m - 807.8) < 0.05 and abs(notional_m - 37.14) < 0.005,
    f"{swap_dv01_per_m:.2f}, {notional_m:.3f}m",
)
# currency: interest-rate parity and hedged returns (MIP chap. 6)
f_irp = 0.8000 * (1 + 0.030) / (1 + 0.045)
ok(
    "MIP: eurozone 3.0% and US 4.5%, spot EUR 0.8000 per dollar -> forward about 0.7880 (forward discount -1.5%)",
    abs(f_irp - 0.7885) < 5e-4 and abs(0.8000 * (1 - 0.015) - 0.7880) < 1e-12,
    f"{f_irp:.4f}",
)
ok(
    "MIP: for a UK investor, hedged returns differ by local risk premia: Japan 2.16 - 1.25 = 0.91%, Canada 3.40 - 1.54"
    " = 1.86%; prefer Canada when fully hedged",
    close(2.16 - 1.25, 0.91, 1e-9) and close(3.40 - 1.54, 1.86, 1e-9),
)
r_local, fx_ret, fwd_prem = 0.031, -0.062, -0.012
ok(
    "a US investor's unhedged return on a euro bond is about 3.1% - 6.2% = -3.1%; hedged it is 3.1% - 1.2% = 1.9%",
    close(r_local + fx_ret, -0.031, 1e-12) and close(r_local + fwd_prem, 0.019, 1e-12),
)
# equity: beta change with index futures (Hull sec. 3.5)
va, vf, beta = 5_050_000.0, 250 * 1010.0, 1.5
ok(
    "Hull sec. 3.5: portfolio 5.05m, beta 1.5, futures 252,500: 30 to hedge fully, 15 short for beta 0.75, 10 long for 2.0",
    close(beta * va / vf, 30, 1e-9)
    and close((beta - 0.75) * va / vf, 15, 1e-9)
    and close((2.0 - beta) * va / vf, 10, 1e-9),
)
# equity swap: receive index total return, pay SOFR + 30 bp on 50m held in cash earning SOFR
cash_ret, idx_tr, sofr, spread = 0.042, 0.11, 0.042, 0.003
ok(
    "50m in cash plus an equity swap receiving index total return and paying SOFR + 30 bp earns index - 30 bp"
    " (10.70% when the index returns 11%)",
    close(cash_ret + idx_tr - (sofr + spread), 0.107, 1e-12),
)

print("== part 2: volatility derivatives and variance swaps (Hull sec. 26.16; Example 15.8)")
ok(
    "Hull Example 15.8: one VIX future bought at 18.5 and sold at 19.3 gains $800 (1,000 x 0.8)",
    close(1000 * (19.3 - 18.5), 800, 1e-9),
)
# Hull Example 26.4: replicate expected variance from option prices
S0, r, q, T, Lvar, VK = 1020.0, 0.04, 0.01, 0.25, 100.0, 0.045
strikes = np.arange(800, 1201, 50, dtype=float)
vols = np.array([0.29, 0.28, 0.27, 0.26, 0.25, 0.24, 0.23, 0.22, 0.21])
F0 = S0 * math.exp((r - q) * T)
s_star = 1000.0
Q = []
for k, v in zip(strikes, vols, strict=True):
    c, p = bs(S0, k, T, r, v, q), bs(S0, k, T, r, v, q, "p")
    Q.append(p if k < s_star else c if k > s_star else 0.5 * (c + p))
Q = np.array(Q)
ok(
    "Hull: F0 = 1,027.68 and the strip Q(K) = 2.22, 5.22, 11.05, 21.27, 51.21, 38.94, 20.69, 9.44, 3.57",
    abs(F0 - 1027.68) < 5e-3
    and np.allclose(Q, [2.22, 5.22, 11.05, 21.27, 51.21, 38.94, 20.69, 9.44, 3.57], atol=6e-3),
    " ".join(f"{x:.2f}" for x in Q),
)
ev = (
    2 / T * math.log(F0 / s_star)
    - 2 / T * (F0 / s_star - 1)
    + 2 / T * math.exp(r * T) * np.sum(50 * Q / strikes**2)
)
val_var = Lvar * (ev - VK) * math.exp(-r * T)
ok(
    "expected variance 0.0621 (24.9% volatility) and a receive-variance swap at 0.045 worth 1.69 million",
    abs(ev - 0.0621) < 5e-5 and abs(val_var - 1.69) < 5e-3,
    f"E(V) {ev:.5f}, value {val_var:.4f}m",
)
e_vol = math.sqrt(ev) * (1 - 0.0001 / (8 * ev**2))
ok(
    "Hull Example 26.5: receive realised volatility against 23% on 100m, sd of realised variance 0.01: 1.82 million",
    abs(100 * (e_vol - 0.23) * math.exp(-r * T) - 1.82) < 5e-3,
    f"{100 * (e_vol - 0.23) * math.exp(-r * T):.4f}m",
)
# variance-swap P&L: vega notional 100,000 per vol point, strike 24
vega_n, k_vol = 100_000.0, 24.0
var_units = vega_n / (2 * k_vol)
pnl = {rv: var_units * (rv**2 - k_vol**2) for rv in (16.0, 24.0, 32.0)}
ok(
    "vega notional 100,000 at strike 24 is 2,083.3 variance units: realised 16 loses 666,667, 32 gains 933,333",
    abs(var_units - 2083.33) < 0.01
    and abs(pnl[16.0] + 666_666.67) < 0.01
    and abs(pnl[32.0] - 933_333.33) < 0.01,
)
ok(
    "the payoff is convex in volatility: an 8-point rise gains more than an 8-point fall loses (an equity-crash hedge)",
    pnl[32.0] > -pnl[16.0] and pnl[24.0] == 0,
)
# tail hedge: VIX future at 20 in contango with spot 18; if spot stays at 18 the future converges and loses
ok(
    "a long one-month VIX future at 20 with spot steady at 18 loses 2,000 per contract at expiry (the roll cost of the"
    " hedge in calm markets)",
    close(1000 * (18 - 20), -2000, 1e-9),
)

print(
    "== part 3: targeting equity and rate exposure, rebalancing with futures, and inferring expectations"
)
fund = 1_000_000_000.0
eq_fut = 50 * 6000.0  # notional per equity index contract (multiplier 50, index 6,000)
bond_dv01 = 80.0  # per bond futures contract
eq_beta, bond_dur = 1.0, 6.0
n_eq = -0.10 * fund * eq_beta / eq_fut
n_bd = 0.10 * fund * bond_dur * 1e-4 / bond_dv01
ok(
    "synthetic 60/40 -> 50/50 on 1bn: sell 333 equity futures (300,000 notional each) and buy 750 bond futures"
    " (DV01 80; 100m at duration 6.0)",
    abs(n_eq + 333.33) < 0.01 and abs(n_bd - 750) < 1e-9,
)
# implied probability from a call spread: P(S_T > K) ~ e^{rT} [C(K - h) - C(K + h)] / (2h)
S, K, TT, rr, sig = 6000.0, 6000.0, 0.25, 0.04, 0.18
h = 25.0
p_spread = math.exp(rr * TT) * (bs(S, K - h, TT, rr, sig) - bs(S, K + h, TT, rr, sig)) / (2 * h)
d2 = (math.log(S / K) + (rr - sig**2 / 2) * TT) / (sig * math.sqrt(TT))
ok(
    "risk-neutral probability that the index ends above 6,000 in three months: 0.5264 from a 5,975/6,025 call spread,"
    " matching N(d2) = 0.5264",
    abs(p_spread - norm.cdf(d2)) < 2e-4 and abs(norm.cdf(d2) - 0.5264) < 5e-4,
    f"{p_spread:.4f}",
)
ok(
    "a meeting-dated OIS 18 bp below the policy rate with only a 25 bp cut possible implies a 72% cut probability",
    close(0.18 / 0.25, 0.72, 1e-12),
)

print(
    "== part 4: endowment case: cash against futures for rebalancing and a tactical tilt (illustrative)"
)
endow = 2_000_000_000.0
eq_w, target = 0.66, 0.60
trade = (eq_w - target) * endow
cash_cost = trade * (0.0025 + 0.0010)  # sell equities 25 bp one-way, buy bonds 10 bp
fut_cost = trade * (0.0002 + 0.0002)  # futures 2 bp each side
ok(
    "drift to 66% equity on 2bn: moving 120m back costs about 420,000 in cash markets and 48,000 with futures",
    close(trade, 120e6, 1e-6) and close(cash_cost, 420_000, 1e-6) and close(fut_cost, 48_000, 1e-6),
)
roll_q = 0.0010 * trade  # roll cost or benefit relative to fair value, 10 bp a quarter
ok(
    "holding the overlay for a year adds four rolls at 10 bp of mispricing: 480,000, more than the cash trade",
    close(4 * roll_q, 480_000, 1e-6) and 4 * roll_q + fut_cost > cash_cost,
)
im = 0.06 * trade
vm_stress = 0.10 * trade
ok(
    "initial margin of 6% (7.2m) and a 10% adverse move (12m variation margin) must be met from liquid assets",
    close(im, 7.2e6, 1e-6) and close(vm_stress, 12e6, 1e-6),
)
# tactical tilt: +5% equity for three months via futures; scenarios for equity relative to bonds
tilt = 0.05 * endow
for rel, exp_pnl in ((-0.08, -8e6), (0.0, 0.0), (0.06, 6e6)):
    ok(
        f"tactical +5% equity tilt (100m notional): equity {rel:+.0%} relative to bonds -> {exp_pnl / 1e6:+.0f}m",
        close(tilt * rel, exp_pnl, 1e-6),
    )
ok(
    "the tilt adds tracking risk of about 0.75% a year if the equity-bond spread has 15% volatility",
    close(0.05 * 0.15, 0.0075, 1e-12),
)

print()
if fails:
    print(f"{len(fails)} check(s) failed: {fails}")
    sys.exit(1)
print("all checks passed")
