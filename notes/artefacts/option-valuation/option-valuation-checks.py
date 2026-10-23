"""Option valuation (2026-10-19): the worked numbers of def:option-value-drivers, res:put-call-forward-parity,
meth:one-period-binomial-valuation, meth:multi-period-binomial-valuation, meth:black-model-rates-currencies and
meth:greeks-delta-gamma-hedging.

Reproduced from Hull, Options, Futures, and Other Derivatives, 11th Global ed. (2022): call 7.116 and put 4.677 (sec.
11.1), the lower-bound example 3.71 (sec. 11.3), put-call parity arbitrage profits 1.02 and 0.27 and the American
bounds 1.68-2.50 (sec. 11.4, Example 11.3), the one-step tree 0.545 (sec. 13.1), the two-step European put 4.1923 and
American put 5.0894 (secs. 13.4-13.5), currency option implied volatility 14.1% (Example 17.2), the futures-option
parity put 1.04 (Example 18.5), Black's model 1.12 and 88.37 (Examples 18.6-18.7), a caplet 0.00519 million (Example
29.3), a swaption 2.19 million (Example 29.4), delta 0.522 and the delta-hedging performance measures of Table 19.4, and
the gamma-neutral example of sec. 19.6. Original checks: sign tests of each value driver, parity against Black-Scholes
prices and a forward, a one-period replication with arbitrage cash flows, a two-period caplet on the rate tree of
Handbook chap. 36, the call as a leveraged stock position, and the gamma-theta P&L of a delta-neutral book against full
revaluation and with realised volatility above implied.

Count convention: one check is one executed ok() call (a call inside a loop counts once per iteration).

Run: uv run --frozen --no-editable python option-valuation-checks.py   (numpy, scipy). Exits 1 on failure.
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


def black(f, k, t, r, sig, kind="c"):
    return bs(f, k, t, r, sig, q=r, kind=kind)


def delta_c(s, k, t, r, sig, q=0.0):
    return math.exp(-q * t) * norm.cdf(
        (math.log(s / k) + (r - q + sig**2 / 2) * t) / (sig * math.sqrt(t))
    )


def gamma(s, k, t, r, sig, q=0.0):
    d1 = (math.log(s / k) + (r - q + sig**2 / 2) * t) / (sig * math.sqrt(t))
    return math.exp(-q * t) * norm.pdf(d1) / (s * sig * math.sqrt(t))


print(
    "== part 1: exercise value, moneyness, time value and the factors that drive option value (Hull chap. 11)"
)
c0, p0 = bs(50, 50, 1, 0.05, 0.30), bs(50, 50, 1, 0.05, 0.30, kind="p")
ok(
    "Hull sec. 11.1 base case (S = K = 50, r = 5%, sigma = 30%, T = 1): call 7.116, put 4.677",
    abs(c0 - 7.116) < 5e-4 and abs(p0 - 4.677) < 5e-4,
    f"{c0:.4f} {p0:.4f}",
)
bump = {
    "S": (51, 50, 1, 0.05, 0.30),
    "K": (50, 51, 1, 0.05, 0.30),
    "T": (50, 50, 1.1, 0.05, 0.30),
    "sigma": (50, 50, 1, 0.05, 0.31),
    "r": (50, 50, 1, 0.06, 0.30),
}
signs = {k: (np.sign(bs(*v) - c0), np.sign(bs(*v, kind="p") - p0)) for k, v in bump.items()}
ok(
    "Table 11.1 signs for European options without dividends: call +S -K +T +sigma +r; put -S +K +T +sigma -r",
    signs == {"S": (1, -1), "K": (-1, 1), "T": (1, 1), "sigma": (1, 1), "r": (1, -1)},
    str(signs),
)
cd = bs(50 - 2 * math.exp(-0.05 * 0.5), 50, 1, 0.05, 0.30)
pd_ = bs(50 - 2 * math.exp(-0.05 * 0.5), 50, 1, 0.05, 0.30, kind="p")
ok(
    "a dividend of 2 in six months lowers the call (7.116 -> lower) and raises the put",
    cd < c0 and pd_ > p0,
    f"{cd:.3f} {pd_:.3f}",
)
ok(
    "at the money the whole premium is time value: call 7.116 and put 4.677 have zero intrinsic value",
    max(50 - 50, 0) == 0 and c0 > 0 and p0 > 0,
)
deep_p = bs(30, 50, 1, 0.05, 0.30, kind="p")
ok(
    "a deep in-the-money European put can be worth less than its exercise value (time value negative): K=50, S=30",
    deep_p < 50 - 30,
    f"{deep_p:.4f} < 20",
)
lb = 20 - 18 * math.exp(-0.1)
ok(
    "Hull sec. 11.3: lower bound S0 - K e^{-rT} for S0 = 20, K = 18, r = 10%, T = 1 is 3.71; a call at 3.00 earns 1.79",
    abs(lb - 3.71) < 5e-3 and abs(17 * math.exp(0.1) - 18 - 0.79) < 5e-3,
)
ok(
    "a call is worth at least its lower bound and at most the stock: 0 <= max(S - K e^{-rT}, 0) <= c <= S",
    all(
        max(s - 50 * math.exp(-0.05), 0) <= bs(s, 50, 1, 0.05, 0.30) <= s
        for s in (20, 40, 50, 60, 90)
    ),
)

print("== part 2: put-call parity and put-call-forward parity")
lhs = 3 + 30 * math.exp(-0.1 * 0.25)
ok(
    "Hull: c + K e^{-rT} = 32.26 against p + S0 = 33.25; buy the call, short put and stock, invest 30.25 -> 31.02,"
    " profit 1.02",
    abs(lhs - 32.26) < 5e-3
    and abs(30.25 * math.exp(0.025) - 31.02) < 5e-3
    and abs(30.25 * math.exp(0.025) - 30 - 1.02) < 5e-3,
)
ok(
    "with the put at 1: short call, buy put and stock for 29 financed -> 29.73, profit 0.27",
    abs(30 - 29 * math.exp(0.025) - 0.27) < 5e-3,
)
ok(
    "Hull Example 11.3 American bounds: 19 - 20 <= C - P <= 19 - 20e^{-0.1x5/12}, so P lies between 1.68 and 2.50",
    abs(1.50 + 1.0 - 2.50) < 1e-12 and abs(1.50 + 20 * math.exp(-0.1 * 5 / 12) - 19 - 1.68) < 5e-3,
)
s0, k, t, r, q, sig = 100.0, 95.0, 0.5, 0.04, 0.015, 0.25
f0 = s0 * math.exp((r - q) * t)
c, p = bs(s0, k, t, r, sig, q), bs(s0, k, t, r, sig, q, "p")
ok(
    "original: c - p = S0 e^{-qT} - K e^{-rT} = (F - K) e^{-rT} with S0 100, K 95, r 4%, q 1.5%, T 0.5",
    close(c - p, s0 * math.exp(-q * t) - k * math.exp(-r * t), 1e-10)
    and close(c - p, (f0 - k) * math.exp(-r * t), 1e-10),
    f"F {f0:.4f}, c-p {c - p:.4f}",
)
ok(
    "Hull Example 18.5: put = 0.56 + 8.50e^{-0.05} - 8.00e^{-0.05} = 1.04 from put-call-futures parity",
    abs(0.56 + (8.5 - 8.0) * math.exp(-0.05) - 1.04) < 5e-3,
)
syn_call = p + s0 * math.exp(-q * t) - k * math.exp(-r * t)
ok(
    "synthetic call = put + stock (net of dividends) - bond; synthetic forward at K = long call + short put",
    close(syn_call, c, 1e-10) and close(c - p, (f0 - k) * math.exp(-r * t), 1e-10),
)

print("== part 3: one-period binomial valuation and risk neutrality (Hull secs. 13.1-13.2)")
s_u, s_d, kk, rr, tt = 22.0, 18.0, 21.0, 0.04, 0.25
delta = (1 - 0) / (s_u - s_d)
f_noarb = 20 * delta - 4.5 * math.exp(-rr * tt)
pr = (math.exp(rr * tt) - 0.9) / (1.1 - 0.9)
f_rn = math.exp(-rr * tt) * (pr * 1 + (1 - pr) * 0)
ok(
    "Hull: delta 0.25 makes 22 x 0.25 - 1 = 18 x 0.25 = 4.5 riskless; the call is worth 0.545 = e^{-rT}(p x 1)"
    " with p = 0.5503",
    delta == 0.25
    and abs(f_noarb - 0.545) < 5e-4
    and close(f_noarb, f_rn, 1e-12)
    and abs(pr - 0.5503) < 5e-5,
)
q_real = 0.7
exp_stock_ret = (q_real * s_u + (1 - q_real) * s_d) / 20 - 1
ok(
    "with a real-world up probability of 0.7 the stock is expected to earn 4% a quarter, yet the call is still 0.545;"
    " discounting the real-world expected payoff at the risk-free rate would give 0.693, which replication shows is wrong",
    abs(exp_stock_ret - 0.04) < 1e-12
    and abs(math.exp(-rr * tt) * q_real - 0.693) < 5e-4
    and close(20 * delta - delta * s_d * math.exp(-rr * tt), f_noarb, 1e-12),
)
borrow = (delta * s_d - 0) * math.exp(-rr * tt)
ok(
    "replication: buy 0.25 shares and borrow 4.455 (= PV of 4.5) costs 0.545 and pays 1 or 0",
    close(delta * 20 - borrow, f_noarb, 1e-12)
    and close(delta * s_u - borrow * math.exp(rr * tt), 1, 1e-12)
    and close(delta * s_d - borrow * math.exp(rr * tt), 0, 1e-12),
)
quote = 0.60
ok(
    "original arbitrage: if the call is quoted at 0.60, write 400 calls (240) and buy 100 shares (2,000) with"
    " 1,782.09 borrowed: 22.09 profit today, and the position is worth 0 in both states",
    abs(400 * borrow - 1782.09) < 0.005
    and abs(400 * quote - (100 * 20 - 400 * borrow) - 22.09) < 0.005
    and close(100 * s_u - 400 * 1 - 400 * borrow * math.exp(rr * tt), 0, 1e-9)
    and close(100 * s_d - 0 - 400 * borrow * math.exp(rr * tt), 0, 1e-9),
)

print("== part 4: two-period European, American and interest-rate options (Hull secs. 13.4-13.5)")
u, d, rate = 1.2, 0.8, 0.05
p2 = (math.exp(rate) - d) / (u - d)
eu = math.exp(-2 * rate) * (p2**2 * 0 + 2 * p2 * (1 - p2) * 4 + (1 - p2) ** 2 * 20)
node_b = math.exp(-rate) * (p2 * 0 + (1 - p2) * 4)
node_c_cont = math.exp(-rate) * (p2 * 4 + (1 - p2) * 20)
am = math.exp(-rate) * (p2 * node_b + (1 - p2) * max(52 - 40, node_c_cont))
ok(
    "European two-year put (S 50, K 52, u 1.2, d 0.8, r 5%): p = 0.6282, value 4.1927 (Hull 4.1923 with p rounded)",
    abs(p2 - 0.6282) < 5e-5 and abs(eu - 4.1927) < 5e-5,
    f"{eu:.4f}",
)
ok(
    "American put: early exercise at node C (12 > 9.4639; Hull 9.4636) lifts the value to 5.0896 (Hull 5.0894)",
    abs(node_c_cont - 9.4639) < 5e-5 and abs(am - 5.0896) < 1e-4 and am > eu,
    f"{am:.4f}",
)
ok(
    "option arbitrage: an American put quoted at 4.80 is cheap by 0.29; buy it and sell the replicating portfolio",
    abs(am - 4.80 - 0.2896) < 1e-3,
)
# two-period caplet on the Handbook's calibrated tree: 1m notional, strike 5%, set at year 2 on the one-year rate,
# paid at year 3; rates from chap. 36 (year 1: 4.4448 / 5.4289; year 2: 4.6958 / 5.7354 / 7.0053; root 3.5)
r1 = [0.044448, 0.054289]
r2 = [0.046958, 0.057354, 0.070053]
pay = [1e6 * max(x - 0.05, 0.0) for x in r2]
v2 = [pay[i] / (1 + r2[i]) for i in range(3)]
v1 = [0.5 * (v2[i] + v2[i + 1]) / (1 + r1[i]) for i in range(2)]
v0 = 0.5 * (v1[0] + v1[1]) / 1.035
ok(
    "caplet on the Handbook tree (1m, 5%, set at year 2, paid at year 3): payoffs 0 / 7,354 / 20,053; value 7,495",
    abs(pay[1] - 7354) < 1 and abs(pay[2] - 20053) < 1 and abs(v0 - 7495.47) < 0.01,
    f"{v0:.2f}",
)
ok(
    "the caplet's value is the risk-neutral average of its discounted payoffs over the four two-year paths",
    close(
        sum(
            0.25 * pay[i + j] / ((1 + r2[i + j]) * (1 + r1[i]) * 1.035)
            for i in (0, 1)
            for j in (0, 1)
        ),
        v0,
        1e-9,
    ),
)

print(
    "== part 5: Black-Scholes-Merton components and Black's model for currencies, futures and rates"
)
c156, p156 = bs(42, 40, 0.5, 0.10, 0.20), bs(42, 40, 0.5, 0.10, 0.20, kind="p")
ok("Hull Example 15.6: c = 4.76, p = 0.81", abs(c156 - 4.76) < 5e-3 and abs(p156 - 0.81) < 5e-3)
d1 = (math.log(42 / 40) + (0.10 + 0.02) * 0.5) / (0.2 * math.sqrt(0.5))
shares, debt = norm.cdf(d1), 40 * math.exp(-0.05) * norm.cdf(d1 - 0.2 * math.sqrt(0.5))
ok(
    "the call is a leveraged stock position: N(d1) = 0.7791 shares (32.72) financed by borrowing 27.96",
    abs(shares - 0.7791) < 5e-5 and close(shares * 42 - debt, c156, 1e-10),
    f"{shares * 42:.3f} - {debt:.3f}",
)
ok(
    "its elasticity Delta S / c = 6.88: a 1% stock move changes the call by about 6.9%",
    abs(shares * 42 / c156 - 6.88) < 5e-3,
)
iv = brentq(lambda v: bs(1.6, 1.6, 1 / 3, 0.08, v, q=0.11) - 0.043, 0.01, 1.0)
ok(
    "Hull Example 17.2: a 4-month GBP call at 4.3 cents implies 14.1% volatility (Garman-Kohlhagen, q = foreign rate)",
    abs(iv - 0.141) < 5e-4,
    f"{iv:.4f}",
)
fx_f = 1.6 * math.exp((0.08 - 0.11) / 3)
ok(
    "the same option by Black's model on the forward rate equals the Garman-Kohlhagen value",
    close(black(fx_f, 1.6, 1 / 3, 0.08, iv), bs(1.6, 1.6, 1 / 3, 0.08, iv, q=0.11), 1e-12),
)
ok(
    "Hull Example 18.6: four-month futures put, F = K = 20, r 9%, vol 25%: 1.12",
    abs(black(20, 20, 4 / 12, 0.09, 0.25, "p") - 1.12) < 5e-3,
)
ok(
    "Hull Example 18.7: six-month gold call, F 1,240, K 1,200, r 5%, vol 20%: 88.37",
    abs(black(1240, 1200, 0.5, 0.05, 0.20) - 88.37) < 5e-3,
)
df125 = math.exp(-0.065 * 1.25)
caplet = (
    0.25
    * 10
    * df125
    * (
        0.07 * norm.cdf((math.log(0.07 / 0.08) + 0.02) / 0.2)
        - 0.08 * norm.cdf((math.log(0.07 / 0.08) - 0.02) / 0.2)
    )
)
ok(
    "Hull Example 29.3 caplet (10m, 8% cap, forward 7%, vol 20%, 1-year fixing): 0.00519 million",
    abs(caplet - 0.00519) < 5e-6,
    f"{caplet:.6f}",
)
ann = 0.5 * sum(math.exp(-0.06 * t_) for t_ in (5.5, 6, 6.5, 7, 7.5, 8))
sf, sk_, ts = 2 * (math.exp(0.061 / 2) - 1), 0.062, 5.0
d1s = (math.log(sf / sk_) + 0.02 * ts) / (0.2 * math.sqrt(ts))
swpt = 100 * ann * (sf * norm.cdf(d1s) - sk_ * norm.cdf(d1s - 0.2 * math.sqrt(ts)))
ok(
    "Hull Example 29.4 payer swaption (5 x 3, 6.2% strike, forward 6.194% s.a., vol 20%): annuity 2.0035, 2.19 million",
    abs(ann - 2.0035) < 1e-4 and abs(sf - 0.06194) < 5e-6 and abs(swpt - 2.19) < 5e-3,
    f"{swpt:.4f}",
)
floorlet = (
    0.25
    * 10
    * df125
    * (
        0.08 * norm.cdf(-(math.log(0.07 / 0.08) - 0.02) / 0.2)
        - 0.07 * norm.cdf(-(math.log(0.07 / 0.08) + 0.02) / 0.2)
    )
)
ok(
    "cap-floor parity for one period: caplet - floorlet = PV of (F - K) on the accrual (a forward-starting swaplet)",
    close(caplet - floorlet, 0.25 * 10 * df125 * (0.07 - 0.08), 1e-12),
)

print("== part 6: Greeks, delta hedging, gamma and implied volatility (Hull chap. 19)")
s, k, r, sig, T = 49.0, 50.0, 0.05, 0.20, 20 / 52
ok(
    "Hull Example 19.1: delta 0.522; the BSM price of 100,000 calls is about 240,000",
    abs(delta_c(s, k, T, r, sig) - 0.522) < 5e-4
    and abs(1e5 * bs(s, k, T, r, sig) - 240_000) < 1_000,
)
rng = np.random.default_rng(20261019)


def hedge_cost_ratio(step_weeks, n_paths=20_000, mu=0.13):
    """Std of the PV cost of writing 1 call and delta hedging it, over the BSM price (Hull Table 19.4 measure)."""
    n = round(20 / step_weeks)
    dt = T / n
    st = np.full(n_paths, s)
    dlt = np.array([delta_c(s, k, T, r, sig)] * n_paths)
    cost = dlt * st
    for i in range(1, n + 1):
        z = rng.standard_normal(n_paths)
        st = st * np.exp((mu - sig**2 / 2) * dt + sig * math.sqrt(dt) * z)
        cost = cost * math.exp(r * dt)
        if i < n:
            tau = T - i * dt
            d1v = (np.log(st / k) + (r + sig**2 / 2) * tau) / (sig * math.sqrt(tau))
            new = norm.cdf(d1v)
        else:
            new = (st > k).astype(float)
        cost += (new - dlt) * st
        dlt = new
    cost -= np.where(st > k, k, 0.0)
    pv = cost * math.exp(-r * T)
    return pv.std() / bs(s, k, T, r, sig), pv.mean()


hull_t194 = {5: 0.42, 4: 0.38, 2: 0.28, 1: 0.21, 0.5: 0.16, 0.25: 0.13}
sim = {w: hedge_cost_ratio(w) for w in hull_t194}
ok(
    "simulated delta-hedging performance (20,000 paths, mu 13%) matches Hull Table 19.4 within 0.03 for rebalancing"
    " every 1 to 5 weeks",
    all(abs(sim[w][0] - hull_t194[w]) < 0.03 for w in (5, 4, 2, 1)),
    " ".join(f"{w}w {sim[w][0]:.3f}" for w in sim),
)
ok(
    "at 0.5 and 0.25 weeks the simulation keeps falling as the square root of the interval (ratio ~1.41 per halving),"
    " below Hull's 0.16 and 0.13, whose ratios are 1.31 and 1.23",
    all(abs(sim[a][0] / sim[b][0] - math.sqrt(2)) < 0.08 for a, b in ((1, 0.5), (0.5, 0.25)))
    and sim[0.25][0] < hull_t194[0.25] - 0.02,
)
ok(
    "and the mean hedging cost is close to the BSM price (2.40) at weekly rebalancing",
    abs(sim[1][1] - bs(s, k, T, r, sig)) < 0.05,
    f"{sim[1][1]:.4f}",
)
ok(
    "Hull sec. 19.6: portfolio gamma -3,000 and a call with delta 0.62 and gamma 1.50 -> buy 2,000 calls and sell"
    " 1,240 shares to stay delta neutral",
    3000 / 1.5 == 2000 and abs(2000 * 0.62 - 1240) < 1e-9,
)
ok(
    "Hull: a delta-neutral book with gamma -10,000 loses about 20,000 on a move of 2 (0.5 x 10,000 x 2^2)",
    0.5 * 10_000 * 2**2 == 20_000,
)
# delta-neutral short call: dPi ~ Theta dt + 0.5 Gamma dS^2 against full revaluation
dt_ = 1 / 252
g = gamma(s, k, T, r, sig)
theta = (bs(s, k, T - dt_, r, sig) - bs(s, k, T, r, sig)) / dt_
for ds in (-2.0, -0.5, 0.5, 2.0):
    full = -(bs(s + ds, k, T - dt_, r, sig) - bs(s, k, T, r, sig)) + delta_c(s, k, T, r, sig) * ds
    approx = -(theta * dt_ + 0.5 * g * ds**2)
    ok(
        f"short call + delta shares, move {ds:+.1f} in one day: Theta dt + Gamma dS^2/2 is within 0.02 of revaluation",
        abs(full - approx) < 0.02,
        f"full {full:.4f}, approx {approx:.4f}",
    )
# implied versus realised: a long call bought at 20% implied and delta hedged daily (deltas at 20%) while the stock's
# realised volatility is 25%; P&L accrues interest on the hedge account
n_p, n_d = 4_000, 98
dtd = T / n_d
st = np.full(n_p, s)
c_old = np.full(n_p, bs(s, k, T, r, 0.20))
dl = np.full(n_p, delta_c(s, k, T, r, 0.20))
pnl = np.zeros(n_p)
for i in range(n_d):
    z = rng.standard_normal(n_p)
    st_new = st * np.exp((r - 0.25**2 / 2) * dtd + 0.25 * math.sqrt(dtd) * z)
    tau2 = T - (i + 1) * dtd
    if tau2 > 1e-12:
        d1v = (np.log(st_new / k) + (r + 0.20**2 / 2) * tau2) / (0.20 * math.sqrt(tau2))
        c_new = st_new * norm.cdf(d1v) - k * math.exp(-r * tau2) * norm.cdf(
            d1v - 0.20 * math.sqrt(tau2)
        )
        dl_new = norm.cdf(d1v)
    else:
        c_new = np.maximum(st_new - k, 0.0)
        dl_new = np.zeros(n_p)
    pnl = (
        pnl * math.exp(r * dtd)
        + (c_new - c_old)
        - dl * (st_new - st)
        - (math.exp(r * dtd) - 1) * (c_old - dl * st)
    )
    st, c_old, dl = st_new, c_new, dl_new
ok(
    "buying options at 20% implied and delta hedging when realised volatility is 25% earns a positive average P&L",
    pnl.mean() > 3 * pnl.std(ddof=1) / math.sqrt(n_p),
    f"mean {pnl.mean():.4f}, se {pnl.std(ddof=1) / math.sqrt(n_p):.4f}",
)
vega = 49 * math.sqrt(T) * norm.pdf((math.log(49 / 50) + (0.05 + 0.02) * T) / (0.2 * math.sqrt(T)))
ok(
    "vega 12.1 per unit volatility: one point of implied volatility moves the call by about 0.121",
    abs(vega - 12.1) < 0.1
    and abs(bs(s, k, T, r, 0.21) - bs(s, k, T, r, 0.20) - vega * 0.01) < 0.002,
    f"{vega:.3f}",
)

print()
if fails:
    print(f"{len(fails)} check(s) failed: {fails}")
    sys.exit(1)
print("all checks passed")
