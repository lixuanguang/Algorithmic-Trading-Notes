"""Derivative payoffs and forward-commitment valuation (2026-10-18): the worked numbers of
meth:option-payoff-profit, meth:arbitrage-replication-carry, meth:forward-price-value-lifecycle,
res:forward-futures-price-difference, def:swaps-as-forward-strips, meth:equity-forward-futures-valuation,
meth:rate-bond-forward-valuation and meth:swap-valuation-replication.

Reproduced from Hull, Options, Futures, and Other Derivatives (11th Global ed., 2022): option profit examples (sec.
10.1), forward prices and values (Examples in secs. 5.4-5.7, 5.10-5.11), conversion factors and the cheapest-to-deliver
example (sec. 6.2, Example 6.1), the bond futures price (Example 6.2), the SOFR futures hedge (Example 6.3) and the
currency swap valued by forwards and by bonds (Examples 7.2-7.3). Original examples use invented inputs and continuous
compounding unless stated; money-market periods use act/360. Single-curve examples are labelled; the separate
projection and discounting curves of mod:multi-curve-fra-swap-valuation are not repeated here.

Run: uv run python forward-swap-checks.py   (numpy). Exits 1 on failure.
"""

# standard library imports
import math
import sys

# third party library imports
import numpy as np

print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}")
fails = []


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


print("== part 1: option value at expiration and profit")
ST = np.array([60.0, 80, 95, 100, 105, 115, 120])


def call_pay(s, k):
    return np.maximum(s - k, 0.0)


def put_pay(s, k):
    return np.maximum(k - s, 0.0)


Kc, prem_c, Kp, prem_p = 100.0, 5.0, 70.0, 7.0
long_call = call_pay(ST, Kc) - prem_c
short_call = -call_pay(ST, Kc) + prem_c
long_put = put_pay(ST, Kp) - prem_p
short_put = -put_pay(ST, Kp) + prem_p
ok(
    "long and short positions sum to zero at every terminal price (zero-sum before costs)",
    np.allclose(long_call + short_call, 0) and np.allclose(long_put + short_put, 0),
)
ok(
    "Hull: call 100 strike for 5 -> profit 1,000 per 100-share contract at 115; loss 300 at 102",
    close(100 * (call_pay(115.0, Kc) - prem_c), 1000)
    and close(100 * (call_pay(102.0, Kc) - prem_c), -300),
)
ok(
    "Hull: put 70 strike for 7 -> profit 800 per contract at 55; loss 700 above 70",
    close(100 * (put_pay(55.0, Kp) - prem_p), 800)
    and close(100 * (put_pay(80.0, Kp) - prem_p), -700),
)
ok(
    "break-evens: call K + premium = 105; put K - premium = 63",
    close(call_pay(105.0, Kc) - prem_c, 0) and close(put_pay(63.0, Kp) - prem_p, 0),
)
ok(
    "long call loss is capped at the premium; short call loss grows without limit",
    long_call.min() == -prem_c and short_call[-1] < short_call[-2] < 0,
)
# Financing the premium: 3-month option, premium paid now, financed at 4% (continuous) to expiry.
r, T = 0.04, 0.25
fin = prem_c * math.exp(r * T)
ok(
    "with the premium financed at 4% for 3 months, the call break-even moves from 105 to 105.0503",
    abs(Kc + fin - 105.0503) < 5e-5,
)
ok(
    "payoff (value at expiration) never negative for the holder; profit can be",
    call_pay(ST, Kc).min() == 0 and long_call.min() < 0,
)

print("== part 2: arbitrage, replication and the cost of carry")
S0, r, T = 100.0, 0.04, 1.0
F0 = S0 * math.exp(r * T)
ok("no-income asset: F0 = 100 e^0.04 = 104.0811", abs(F0 - 104.0811) < 5e-5)
# Cash-and-carry when the quoted forward is 106; reverse when 102 (borrow costs ignored)
ok(
    "forward quoted at 106: buy spot on borrowed money and sell forward -> locked profit 1.9189 at T",
    abs((106 - S0 * math.exp(r * T)) - 1.9189) < 5e-5,
)
ok(
    "forward quoted at 102: short spot, lend proceeds, buy forward -> locked profit 2.0811 at T",
    abs((S0 * math.exp(r * T) - 102) - 2.0811) < 5e-5,
)
mu = 0.08
ok(
    "an 8% expected growth gives E[S_T] = 108.33 > F0: the forward is not the expected price unless risk is unpriced",
    abs(S0 * math.exp(mu * T) - 108.3287) < 5e-5 and S0 * math.exp(mu * T) > F0,
)
# Hull's examples
ok("Hull: 40 e^(0.05 x 0.25) = 40.50", abs(40 * math.exp(0.05 * 0.25) - 40.50) < 0.005)
ok(
    "Hull: (900 - 40 e^(-0.03/3)) e^(0.04 x 0.75) = 886.60",
    abs((900 - 40 * math.exp(-0.03 / 3)) * math.exp(0.03) - 886.60) < 0.005,
)
ok(
    "Hull: (50 - 2.162) e^(0.08 x 10/12) = 51.14",
    abs((50 - 2.162) * math.exp(0.08 * 10 / 12) - 51.14) < 0.005,
)
ok(
    "Hull: q = 2 ln 1.02 = 3.96%; 25 e^((0.10-0.0396) 0.5) = 25.77",
    abs(25 * math.exp((0.10 - 2 * math.log(1.02)) * 0.5) - 25.77) < 0.005,
)
ok(
    "Hull: value of an old forward (26.28 - 24) e^-0.05 = 2.17",
    abs((26.28 - 24) * math.exp(-0.05) - 2.17) < 0.005,
)
ok(
    "Hull: AUD forward 0.7500 e^((0.01-0.03) 2) = 0.7206 USD per AUD",
    abs(0.75 * math.exp(-0.04) - 0.7206) < 5e-5,
)
ok(
    "Hull: commodity with storage (450 + 2 e^-0.07) e^0.07 = 484.63",
    abs((450 + 2 * math.exp(-0.07)) * math.exp(0.07) - 484.63) < 0.005,
)

print("== part 3: price and value of a forward over its life (equity, with and without dividends)")
K = F0  # contract written at the then forward price
ok(
    "at initiation the forward is worth zero to both sides",
    close(S0 - K * math.exp(-r * T), 0, 1e-12),
)
t, St = 0.5, 108.0
Ft = St * math.exp(r * (T - t))
val_long = St - K * math.exp(-r * (T - t))
ok(
    "six months later, S = 108: value to the long 5.9799 = S - K e^(-r(T-t)) = (F_t - K) e^(-r(T-t))",
    abs(val_long - 5.9799) < 5e-5 and close(val_long, (Ft - K) * math.exp(-r * (T - t)), 1e-12),
)
ok(
    "the short holds exactly the negative; at expiry with S_T = 110 the long receives 5.9189",
    close(-val_long + val_long, 0) and abs(110 - K - 5.9189) < 5e-5,
)
# Discrete dividends 1.50 at 0.25 and 0.75 years
divs = [(0.25, 1.5), (0.75, 1.5)]
I0 = sum(d * math.exp(-r * tt) for tt, d in divs)
F_div = (S0 - I0) * math.exp(r * T)
ok(
    "dividends 1.50 at 3 and 9 months: PV 2.9407; forward 101.0203",
    abs(I0 - 2.9407) < 5e-5 and abs(F_div - 101.0203) < 5e-5,
)
# Replication: buy the share, borrow S0 - I0, repay with dividends and the loan; at T own the share and owe F_div.
loan = S0 - I0
owed_T = loan * math.exp(r * T)
ok(
    "replicating portfolio: share + loan of S0 - I costs nothing net of dividends and owes exactly F at T",
    close(owed_T, F_div, 1e-10),
)
I_t = 1.5 * math.exp(-r * (0.75 - t))
val_div = St - I_t - F_div * math.exp(-r * (T - t))
ok(
    "value at 6 months (S = 108, one dividend left): S - PV(div) - K e^(-r(T-t)) = 7.4949",
    abs(val_div - 7.4949) < 5e-5,
)
q = 0.02
ok(
    "continuous yield 2%: F = 100 e^(0.04-0.02) = 102.0201; replication holds e^(-qT) shares",
    abs(S0 * math.exp((r - q) * T) - 102.0201) < 5e-5
    and close(
        math.exp(-q * T) * S0 * math.exp(r * T) * math.exp(-r * T) * math.exp(q * T), S0, 1e-12
    ),
)
# Index futures quoted as points: 4,000 index, 2% yield, 4% rate, 3 months -> fair futures price
ok(
    "index futures: 4,000 e^((0.04-0.02) 0.25) = 4,020.05",
    abs(4000 * math.exp(0.02 * 0.25) - 4020.05) < 0.005,
)

print("== part 4: forward and futures prices")
rng = np.random.default_rng(7)
steps = 250
dt = T / steps
rt = 0.03 + 0.02 * np.linspace(0, 1, steps + 1)  # deterministic, time-varying short rate
growth = np.exp(np.cumsum(rt[:-1] * dt))
disc_T = np.exp(-np.r_[0, np.cumsum(rt[:-1] * dt)] + np.sum(rt[:-1] * dt))  # e^{int_t^T r}
S = S0 * np.exp(np.cumsum(np.r_[0, rng.normal(0, 0.2 * math.sqrt(dt), steps)]))
F_det = (
    S * disc_T
)  # with deterministic rates, the futures price equals the forward price S_t e^{int_t^T r}
gains = 0.0
for i in range(steps):
    h_i = 1 / disc_T[i + 1]  # tail: hold e^{-int_{t+1}^T r} contracts
    gains += h_i * (F_det[i + 1] - F_det[i]) * disc_T[i + 1]  # settle daily, invest to T
ok(
    "deterministic rates: a tailed futures position ends with S_T - F0, the forward payoff, on a simulated path",
    close(gains, S[-1] - F_det[0], 1e-9),
)
# Stochastic rates: two periods; the short rate and the asset move together (positive correlation).
r0 = 0.04
r1 = {"u": 0.06, "d": 0.02}
S1 = {"u": 110.0, "d": 92.0}
S0b = 0.5 * (S1["u"] + S1["d"]) / (1 + r0)  # risk-neutral pricing, no income
fut1 = {k: S1[k] * (1 + r1[k]) for k in S1}  # one period before expiry futures = forward = S(1+r)
fut0 = 0.5 * (fut1["u"] + fut1["d"])
P02 = 0.5 * (1 / (1 + r1["u"]) + 1 / (1 + r1["d"])) / (1 + r0)
fwd0 = S0b / P02
print(f"    S0 {S0b:.4f}, futures {fut0:.4f}, forward {fwd0:.4f}")
ok(
    "positive asset-rate correlation: futures 105.2200 above forward 105.0012",
    abs(fut0 - 105.22) < 5e-5 and abs(fwd0 - 105.0012) < 5e-5 and fut0 > fwd0,
)
S1n = {"u": 92.0, "d": 110.0}
S0n = 0.5 * (S1n["u"] + S1n["d"]) / (1 + r0)
fut0n = 0.5 * (S1n["u"] * (1 + r1["u"]) + S1n["d"] * (1 + r1["d"]))
fwd0n = S0n / P02
ok(
    "negative correlation reverses it: futures 104.8600 below the same forward 105.0012",
    abs(fut0n - 104.86) < 5e-5 and fut0n < fwd0n,
)

print("== part 5: interest-rate and bond forwards and futures")
# FRA on simple act/360 rates from a single curve (labelled single-curve): DF(91d), DF(182d)
d1, d2 = 0.990, 0.979
tau = 91 / 360
fra = (d1 / d2 - 1) / tau
ok("3x6 FRA from discount factors 0.990 and 0.979: 4.4450% (act/360)", abs(fra - 0.044450) < 5e-6)
N = 10e6
K_fra = 0.0420
val_payfix = N * tau * (fra - K_fra) * d2
ok(
    "existing FRA paying 4.20% fixed on 10m: worth +6,063 to the fixed payer, -6,063 to the receiver",
    abs(val_payfix - 6062.83) < 0.01,
)
# Hull Example 6.3: 3-month SOFR futures hedge on 100m (100 contracts, $25 per bp)
gain = 100 * 25 * (99.990 - 99.200) * 100
ok(
    "Hull Ex. 6.3: futures fall 79 bp -> gain 197,500 (Hull's text subtracts 197,000, a slip); net 502,500 = 2.01%",
    close(gain, 197500, 1e-6)
    and close(700000 - gain, 502500, 1e-6)
    and close(0.25 * 1e8 * 0.0201, 502500, 1e-6),
)
loss = 100 * 25 * (100.400 - 99.990) * 100
ok(
    "Hull's negative-rate case: 41 bp loss is 102,500 (printed 102,250); 400,000 + 102,500 = 502,500 again",
    close(loss, 102500, 1e-6) and close(400000 + loss, 502500, 1e-6),
)
# Conversion factors (6% s.a., maturities rounded to quarters)
cf1 = (sum(5 / 1.03**i for i in range(1, 41)) + 100 / 1.03**40) / 100
v_q = sum(4 / 1.03**i for i in range(1, 37)) + 100 / 1.03**36 + 4
cf2 = (v_q / math.sqrt(1.03) - 2) / 100
ok(
    "Hull conversion factors: 10% bond, 20 years -> 1.4623; 8% bond, 18 years 3 months -> 1.2199",
    abs(cf1 - 1.4623) < 5e-5 and abs(cf2 - 1.2199) < 5e-5,
)
costs = [99.50 - 93.25 * 1.0382, 143.50 - 93.25 * 1.5188, 119.75 - 93.25 * 1.2615]
ok(
    "Hull Ex. 6.1: delivery costs 2.69, 1.87, 2.12 -> bond 2 is cheapest to deliver",
    np.allclose(costs, [2.69, 1.87, 2.12], atol=0.005) and int(np.argmin(costs)) == 1,
)
# Hull Example 6.2: futures price from the cheapest-to-deliver 12% bond
cash = 115 + 60 / (60 + 122) * 6
I_c = 6 * math.exp(-0.1 * 122 / 365)
F_cash = (cash - I_c) * math.exp(0.1 * 270 / 365)
F_quoted_bond = F_cash - 6 * 148 / (148 + 35)
F_fut = F_quoted_bond / 1.6
ok(
    "Hull Ex. 6.2: cash 116.978, coupon PV 5.803, cash forward 119.711, quoted 114.859, futures 71.79",
    abs(cash - 116.978) < 5e-4
    and abs(I_c - 5.803) < 5e-4
    and abs(F_cash - 119.711) < 5e-4
    and abs(F_quoted_bond - 114.859) < 5e-4
    and abs(F_fut - 71.79) < 0.005,
)
# Original bond forward: 5% s.a. bond, clean 101.20, accrued 0.90 now; coupon 2.50 in 0.35 years; forward for
# delivery in 0.5 years when accrued will be 0.375; repo 4.2% (continuous)
full_now = 101.20 + 0.90
I_b = 2.5 * math.exp(-0.042 * 0.35)
F_full = (full_now - I_b) * math.exp(0.042 * 0.5)
F_clean = F_full - 0.375
ok(
    "bond forward: full 102.10, coupon PV 2.4635, forward full 101.7510, forward clean (quoted) 101.3760",
    abs(I_b - 2.4635) < 5e-5 and abs(F_full - 101.7510) < 5e-5 and abs(F_clean - 101.3760) < 5e-5,
)
F_new = F_full + 0.40
ok(
    "if the forward full price later rises by 0.40 with 0.25 years left, a long agreed at 101.7510 is worth +0.3958",
    abs(0.40 * math.exp(-0.042 * 0.25) - 0.3958) < 5e-5 and F_new > F_full,
)

print("== part 6: swaps as strips of forwards; interest-rate, currency and equity swaps")
# Annual single-curve discount factors from par swap rates (OIS, invented)
par = np.array([0.0360, 0.0350, 0.0355, 0.0365, 0.0375])
df = []
for c in par:
    df.append((1 - c * sum(df)) / (1 + c))
df = np.array(df)
fwd = np.r_[1 / df[0], df[:-1] / df[1:]] - 1
s5 = (1 - df[-1]) / df.sum()
ok("5-year par swap rate (1 - DF5)/sum(DF) recovers the 3.75% input", close(s5, 0.0375, 1e-12))
exch = (fwd - s5) * df  # value of each annual exchange to the floating receiver, per unit notional
ok(
    "each exchange is an off-market forward with non-zero value; together they are worth zero",
    np.all(np.abs(exch) > 1e-4) and close(exch.sum(), 0, 1e-12),
)
ok(
    "on this curve the receive-floating side is negative early and positive late (forwards cross the swap rate)",
    exch[0] < 0 and exch[1] < 0 and exch[-1] > 0,
)
# One year later the curve has shifted up 50 bp in par terms; value of a receive-fixed 3.75% swap with 4 years left
par_new = np.array([0.0410, 0.0405, 0.0415, 0.0425])
df_n = []
for c in par_new:
    df_n.append((1 - c * sum(df_n)) / (1 + c))
df_n = np.array(df_n)
fixed_bond = 0.0375 * df_n.sum() + df_n[-1]
float_bond = 1.0  # a floater is worth par on a reset date (single curve)
v_bonds = (fixed_bond - float_bond) * 100e6
fwd_n = np.r_[1 / df_n[0], df_n[:-1] / df_n[1:]] - 1
v_fras = float(((0.0375 - fwd_n) * df_n).sum() * 100e6)
s4_new = (1 - df_n[-1]) / df_n.sum()
ok(
    "receive-fixed 3.75% on 100m with 4 years left after rates rise: -1.8079m, equal by bonds and by FRAs",
    abs(v_bonds - v_fras) < 1e-6 and abs(v_bonds / 1e6 + 1.80785) < 5e-5,
)
ok(
    "its value is the annuity times the rate change: (3.75% - new 4.25% swap rate) x sum DF x notional",
    close(v_bonds, (0.0375 - s4_new) * df_n.sum() * 100e6, 1e-6) and abs(s4_new - 0.0425) < 1e-12,
)
# Hull Examples 7.2 and 7.3: currency swap, receive yen 3% on 1,200m, pay dollars 4% on 10m, 3 years, flat 2.5% / 1.5%
times = np.array([1, 2, 3.0])
usd_cf = np.array([0.4, 0.4, 10.4])
jpy_cf = np.array([36, 36, 1236.0])
spot = 1 / 110
fwds = spot * np.exp((0.025 - 0.015) * times)
v_fwd = float(np.sum((jpy_cf * fwds - usd_cf) * np.exp(-0.025 * times)))
B_D = float(usd_cf @ np.exp(-0.025 * times))
B_F = float(jpy_cf @ np.exp(-0.015 * times))
v_bond = B_F * spot - B_D
ok(
    "Hull Ex. 7.2/7.3: 0.9628m by forward contracts and by bonds (B_D 10.4191, B_F 1,252.01 yen); Hull prints 0.9629,\n"
    "      but his own present values -0.0677, -0.0629, +1.0934 and his bond values 1,252.01/110 - 10.4191 give 0.9628",
    abs(v_fwd - 0.96279) < 5e-6
    and abs(v_bond - v_fwd) < 1e-10
    and abs(B_D - 10.4191) < 5e-5
    and abs(B_F - 1252.01) < 0.005
    and abs((-0.0677 - 0.0629 + 1.0934) - 0.9628) < 1e-9
    and abs(1252.01 / 110 - 10.4191 - 0.9628) < 5e-5,
)
# Original fixed-for-fixed EUR/USD: notionals EUR 100m and USD 108m at spot 1.08 USD per EUR; 3 years annual;
# flat annual-compounded rates USD 4.00%, EUR 2.50%; fixed rates set at par in each currency -> zero value.
s_usd, s_eur = 0.04, 0.025
dfu = np.array([1.04**-k for k in (1, 2, 3)])
dfe = np.array([1.025**-k for k in (1, 2, 3)])
B_usd = 108e6 * (s_usd * dfu.sum() + dfu[-1])
B_eur = 100e6 * (s_eur * dfe.sum() + dfe[-1])
ok(
    "at initiation with par coupons each bond is worth its notional and the swap is worth zero at 1.08",
    abs(B_usd - 108e6) < 1e-3 and abs(B_eur - 100e6) < 1e-3 and abs(B_usd - 1.08 * B_eur) < 1e-3,
)
v_after = (
    B_usd - 1.12 * B_eur
)  # receive USD, pay EUR, after EUR strengthens to 1.12 USD per EUR (rates unchanged)
ok(
    "EUR rises to 1.12 USD: the party paying EUR loses 4.0m USD (100m x 0.04)",
    abs(v_after + 4.0e6) < 1e-3,
)
wrong = B_usd - B_eur / 1.12  # mistakenly treating 1.12 as EUR per USD
ok(
    "using the inverted quote (EUR per USD) by mistake would show a 18.7m gain instead",
    abs(wrong - 18.714e6) < 1e3,
    f"{wrong / 1e6:.3f}m",
)
# Equity swap: receive the index total return, pay fixed s on 100m, annual resets, 5 years on the OIS curve above
eq_leg = 1 - df[-1]  # replication: invest N each period, return N(E_k/E_(k-1)), repay N at k
s_eq = eq_leg / df.sum()
ok(
    "equity-for-fixed swap: the equity leg is worth N(1 - DF_n), so the fair fixed rate equals the par swap rate 3.75%",
    close(s_eq, s5, 1e-12),
)
# Value 0.5 years into the second period: index up 6% since the last reset, curve shifted to flat 4% continuous
tau_r = 0.5  # time to next reset
E_rel = 1.06
df_t = np.exp(-0.04 * (tau_r + np.arange(4)))  # to the next reset and the three after it
eq_val = 100e6 * (E_rel - df_t[-1])
fix_val = 100e6 * s_eq * df_t.sum()
v_eq = eq_val - fix_val
ok(
    "mid-period: equity leg 100m(E/E_reset - DF_n) = 19.064m, fixed leg 13.861m; receive-equity side +5.204m",
    abs(eq_val / 1e6 - 19.0642) < 5e-4
    and abs(fix_val / 1e6 - 13.8606) < 5e-4
    and abs(v_eq / 1e6 - 5.2036) < 5e-4,
)
ok(
    "immediately after a reset (E/E_reset = 1) on an unchanged curve, the equity-for-floating version is worth zero",
    close(100e6 * (1 - df[0]) - 100e6 * (fwd[0]) * df[0], 0, 1e-6),
)

print()
if fails:
    print(f"{len(fails)} check(s) failed: {fails}")
    sys.exit(1)
print("all checks passed")
