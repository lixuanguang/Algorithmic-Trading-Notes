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

Corrections pass (2026-10-18, audit of 88bd29e): the discrete-dividend replication is a dated cash-flow ledger (borrow
the full spot, dividends repay the loan); the SOFR futures hedge derives loan interest and futures P&L from SOFR, the
200 bp spread, notional and Hull's quarter-year accrual; the equity swap values the next equity payment as
N(E_t/E_0 - P(t, T_next)) (Hull, p. 778, prints N(E - E_0)/E_0; his Technical Note 19 agrees with the correction), adds
an equity-for-SOFR leg with realised overnight compounding, reset-date limits, and a stochastic-rate simulation.

Correction of 2026-10-19 (audit of 642e29c): the original bond forward is built on a dated coupon calendar (15 May/15 Nov,
actual/actual in period, Sunday coupon paid Monday under 31 CFR 356.30(a), T+1 spot settlement, term repo act/360);
accrued interest, coupon timing, full and quoted prices come from that one schedule, with a two-repo cash ledger and a
carry decomposition of quoted forward minus spot quote as independent checks.

Count convention: one check is one executed ok() call (so a call inside a loop counts once per iteration).

Run: uv run python forward-swap-checks.py   (numpy). Exits 1 on failure.
"""

# standard library imports
import datetime
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
# Replication as a dated cash-flow ledger: at 0 borrow the full S0 and buy the share; each dividend is paid to the
# lender when received; the loan accrues at r between events. The ledger is built event by event, not from (S0 - I)e^rT.
events = sorted({0.0, T, *(tt for tt, _ in divs)})
divs_at = dict(divs)
balance, t_prev, ledger = 0.0, 0.0, []
for tt in events:
    balance *= math.exp(r * (tt - t_prev))
    t_prev = tt
    if tt == 0.0:
        balance += S0  # borrow S0
        ledger.append((tt, S0 - S0))  # loan proceeds less share purchase
    elif tt in divs_at:
        balance -= divs_at[tt]  # dividend applied to the loan
        ledger.append((tt, divs_at[tt] - divs_at[tt]))  # dividend received less repayment
print(
    f"    loan balance at T {balance:.6f}; net cash by date {[(t_, round(c, 12)) for t_, c in ledger]}"
)
ok(
    "ledger: borrowing the full 100 funds the share (net 0 at t=0); each 1.50 dividend repays the loan (net 0)",
    all(close(c, 0, 1e-12) for _, c in ledger) and len(ledger) == 1 + len(divs),
)
ok(
    "ledger: the debt left at T is 101.020320, the forward price, so at T the position is share - F_0 = S_T - F_0",
    abs(balance - 101.020320) < 5e-7 and close(balance, F_div, 1e-10),
)
# Borrowing only S0 - I instead leaves the share purchase unfunded by I at t=0: not self-financing.
ok(
    "borrowing only S0 - I = 97.059257 leaves a funding gap of I = 2.940743 at t=0",
    abs((S0 - (S0 - I0)) - 2.940743) < 5e-7,
)
# Arbitrage: if a dealer quotes 102 for this forward, run the ledger and sell forward: profit 102 - 101.020320 at T.
ok(
    "with the forward quoted at 102, ledger plus short forward earns 0.979680 at T and nothing earlier",
    abs((102 - balance) - 0.979680) < 5e-7,
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
# Hull Example 6.3: borrow 100m for three months at three-month SOFR + 200 bp, hedged by selling 3-month SOFR futures
# at 99.990. Hull accrues both loan and futures on a quarter year (0.25); every amount is derived from rates here.
N_loan, tau_q, spread = 100e6, 0.25, 0.02
contract_face, n_contracts = 1e6, 100
per_bp = contract_face * 1e-4 * tau_q  # $ per basis point per contract
quote0 = 99.990
R_lock = (100 - quote0) / 100  # reference rate implied by the quote


def hedge(settle, tau_loan=tau_q, n=n_contracts):
    R = (100 - settle) / 100
    interest = N_loan * tau_loan * (R + spread)
    fut_pnl = (
        n * per_bp * (quote0 - settle) * 100
    )  # short futures gain when the quote falls (in bp)
    return R, interest, fut_pnl, interest - fut_pnl


ok(
    "contract value per bp: 1m x 0.0001 x 0.25 = $25; 100 contracts match 100m of quarter-year accrual",
    close(per_bp, 25.0, 1e-12) and close(n_contracts * contract_face, N_loan, 1e-6),
)
ok(
    "quote 99.990 implies a reference rate of 0.01%; adding the 200 bp spread locks 2.01%",
    close(R_lock, 0.0001, 1e-12) and close(R_lock + spread, 0.0201, 1e-12),
)
R_up, int_up, pnl_up, net_up = hedge(99.200)
ok(
    "settles 99.200 (SOFR 0.80%): loan pays 2.80% = 700,000; futures gain 79 bp = 197,500; net 502,500 = 2.01%",
    close(R_up, 0.008, 1e-12)
    and close(int_up, 700000, 1e-6)
    and close(pnl_up, 197500, 1e-6)
    and close(net_up, 502500, 1e-6)
    and close(net_up / (N_loan * tau_q), 0.0201, 1e-12),
)
R_dn, int_dn, pnl_dn, net_dn = hedge(100.400)
ok(
    "settles 100.400 (SOFR -0.40%): loan pays 1.60% = 400,000; futures lose 41 bp = 102,500; net 502,500 again",
    close(R_dn, -0.004, 1e-12)
    and close(int_dn, 400000, 1e-6)
    and close(pnl_dn, -102500, 1e-6)
    and close(net_dn, 502500, 1e-6),
)
ok(
    "Hull's printed 197,000 and 102,250 differ from the derived 197,500 and 102,500; printed total 502,250 is a slip",
    not close(pnl_up, 197000, 1) and not close(-pnl_dn, 102250, 1) and not close(net_dn, 502250, 1),
)
sweep = [hedge(s)[3] for s in np.linspace(97.0, 101.5, 19)]
ok(
    "for any settlement between 97.0 and 101.5 the net cost is 502,500: N x 0.25 x (0.01% + 2%)",
    np.allclose(sweep, N_loan * tau_q * (R_lock + spread), atol=1e-6),
)
# With a loan accrual different from the futures' fixed 0.25 (e.g. a 92-day act/360 period), 100 contracts leave a
# residual that moves with SOFR; scaling to 100 x (92/360)/0.25 = 102.2 contracts restores the lock.
t92 = 92 / 360
res = [hedge(s, t92)[3] for s in (99.2, 100.4)]
res_scaled = [hedge(s, t92, n_contracts * t92 / tau_q)[3] for s in (99.2, 100.4)]
ok(
    "92-day loan: 100 contracts leave the net cost rate-dependent; 102.2 contracts make it constant again",
    abs(res[0] - res[1]) > 1000 and close(res_scaled[0], res_scaled[1], 1e-6),
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
# Original bond forward on a dated schedule (correction of 2026-10-19: the earlier inputs, accrued 0.90 now and 0.375
# at delivery with a coupon in 0.35 years, fitted no regular semiannual calendar). 5% note, coupons 15 May and 15
# November, actual/actual in period on the scheduled dates (Hull sec. 6.1, pp. 152-153); a coupon date on a weekend is
# paid the next business day without additional interest (31 CFR 356.30(a)). Spot trade Fri 16 Oct 2026, T+1
# settlement Mon 19 Oct 2026; forward delivery Mon 19 Apr 2027; term repo 4.20% simple act/360, flat.
C_b, repo = 2.5, 0.042
settle, deliver, trade = (
    datetime.date(2026, 10, 19),
    datetime.date(2027, 4, 19),
    datetime.date(2026, 10, 16),
)


def coupon_schedule(maturity, first_needed):
    """Scheduled coupon dates stepped back six months from maturity (independent of the hand-entered dates)."""
    dates, y, m = [], maturity.year, maturity.month
    while True:
        d = datetime.date(y, m, maturity.day)
        if d < first_needed:
            return sorted([*dates, d])
        dates.append(d)
        m -= 6
        if m <= 0:
            m, y = m + 12, y - 1


def paid_on(d):
    """Next business day for a weekend date (no holiday falls on these dates)."""
    while d.weekday() >= 5:
        d += datetime.timedelta(days=1)
    return d


sched = coupon_schedule(datetime.date(2031, 11, 15), datetime.date(2026, 1, 1))


def accrued(on):
    prev = max(d for d in sched if d <= on)
    nxt = min(d for d in sched if d > on)
    return C_b * (on - prev).days / (nxt - prev).days, prev, nxt


def df_repo(d):
    return 1 / (1 + repo * (d - settle).days / 360)


ai_0, prev_0, next_0 = accrued(settle)
ai_T, prev_T, next_T = accrued(deliver)
pay_c = paid_on(next_0)
ok(
    "schedule: settlement in 15 May-15 Nov 2026 (157 of 184 days), delivery in 15 Nov 2026-15 May 2027 (155 of 181);"
    " the Sunday 15 Nov 2026 coupon is paid Monday 16 Nov, 28 days after settlement; trade T+1 is Monday 19 Oct",
    (prev_0, next_0, prev_T, next_T)
    == (
        datetime.date(2026, 5, 15),
        datetime.date(2026, 11, 15),
        datetime.date(2026, 11, 15),
        datetime.date(2027, 5, 15),
    )
    and (
        (settle - prev_0).days,
        (next_0 - prev_0).days,
        (deliver - prev_T).days,
        (next_T - prev_T).days,
    )
    == (157, 184, 155, 181)
    and next_0.weekday() == 6
    and pay_c == datetime.date(2026, 11, 16)
    and (pay_c - settle).days == 28
    and paid_on(trade + datetime.timedelta(days=1)) == settle,
)
ok(
    "accrual is continuous: it reaches the full coupon at the scheduled date and restarts at zero (not on the paid date)",
    close(C_b * (next_0 - prev_0).days / (next_0 - prev_0).days, C_b)
    and close(accrued(next_0)[0], 0.0)
    and accrued(pay_c)[0] > 0,
)
clean_0 = 101.20
B0_b = clean_0 + ai_0
I_b = C_b * df_repo(pay_c)
F_full = (B0_b - I_b) / df_repo(deliver)
F_clean = F_full - ai_T
ok(
    "accrued 2.133152 and 2.140884; full spot 103.333152; coupon PV 2.491860; forward full 102.982489; quoted 100.841605",
    all(
        abs(a - b) < 5e-7
        for a, b in [
            (ai_0, 2.133152),
            (ai_T, 2.140884),
            (B0_b, 103.333152),
            (I_b, 2.491860),
            (F_full, 102.982489),
            (F_clean, 100.841605),
        ]
    ),
    f"{ai_0:.6f} {ai_T:.6f} {B0_b:.6f} {I_b:.6f} {F_full:.6f} {F_clean:.6f}",
)
# Independent check 1: dated ledger of the replication (two term repos), net cash zero before delivery
loan_T, loan_c = B0_b - I_b, I_b
ledger = {
    settle: -B0_b + loan_T + loan_c,
    pay_c: C_b - loan_c * (1 + repo * (pay_c - settle).days / 360),
    deliver: -loan_T * (1 + repo * (deliver - settle).days / 360),
}
ok(
    "replication ledger: buy the bond with repo to delivery (B0 - I) and to the coupon date (I); the coupon repays the"
    " short repo; at delivery the bond is held against a debt equal to the forward full price",
    close(ledger[settle], 0, 1e-12)
    and close(ledger[pay_c], 0, 1e-12)
    and close(-ledger[deliver], F_full, 1e-9),
)
# Independent check 2: clean-to-full at both dates and the carry decomposition of quoted forward minus spot quote
fin = B0_b * repo * (deliver - settle).days / 360
coupon_income = C_b - ai_0 + ai_T
reinvest = C_b * (df_repo(pay_c) / df_repo(deliver) - 1)
ok(
    "quoted forward - spot quote = financing 2.194107 - coupon income 2.507732 - interest on the paid coupon 0.044770"
    " = -0.358395 (positive carry: forward quoted below spot)",
    close(F_clean - clean_0, fin - coupon_income - reinvest, 1e-12)
    and abs(fin - 2.194107) < 5e-7
    and abs(coupon_income - 2.507732) < 5e-7
    and abs(reinvest - 0.044770) < 5e-7
    and F_clean < clean_0,
)
ok(
    "conventions matter: discounting the coupon from the Sunday instead of the Monday moves the forward by -0.000296;"
    " reinvesting it at the 154-day term rate instead of the curve's forward moves it by -0.000146",
    abs((B0_b - C_b / (1 + repo * 27 / 360)) / df_repo(deliver) - F_full + 0.000296) < 5e-7
    and abs(
        B0_b / df_repo(deliver)
        - C_b * (1 + repo * (deliver - pay_c).days / 360)
        - F_full
        + 0.000146
    )
    < 5e-7,
)
later = datetime.date(2027, 1, 18)
ok(
    "if the forward full price rises 0.40 on 18 Jan 2027 (91 days left), a long agreed at 102.982489 is worth +0.395798",
    (deliver - later).days == 91 and abs(0.40 / (1 + repo * 91 / 360) - 0.395798) < 5e-7,
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
# The next equity payment N(E_next/E_reset - 1) is replicated by holding N E_t/E_reset of the total-return index and
# owing N at the payment date: PV = N(E_t/E_reset - P(t, T_next)). Later payments, each N(E_k/E_(k-1) - 1), are worth
# N(P_(k-1) - P_k) and telescope to N(P_next - P_n); the whole leg is N(E_t/E_reset - P_n).
P_next = df_t[0]
next_eq = 100e6 * (E_rel - P_next)
later_eq = 100e6 * (P_next - df_t[-1])
hull_778 = 100e6 * (E_rel - 1)  # the printed expression L(E - E0)/E0
ok(
    "next equity payment PV 100m x (1.06 - e^(-0.02)) = 7.980133m; later payments 11.084044m; sum = equity leg",
    abs(next_eq / 1e6 - 7.980133) < 5e-7
    and abs(later_eq / 1e6 - 11.084044) < 5e-7
    and close(next_eq + later_eq, eq_val, 1e-6),
)
ok(
    "N(E/E0 - 1) = 6.000m undervalues the next payment by N(1 - P) = 1.980m; it is right only as t -> T_next",
    close(next_eq - hull_778, 100e6 * (1 - P_next), 1e-6)
    and abs((next_eq - hull_778) / 1e6 - 1.980133) < 5e-7,
)
# Payment-date limits: as t -> T_next, P -> 1 and the PV becomes the payment itself; just after a reset, E = E_reset
# and the next payment is worth N(1 - P), not zero.


def next_eq_pv(e_rel, tau_next, rate=0.04):
    return 100e6 * (e_rel - math.exp(-rate * tau_next))


ok(
    "limits: one second before payment the PV is the payment N(E/E0 - 1); just after a reset (E = E0, a year to\n"
    "      go) the next equity payment is worth N(1 - e^-0.04) = 3.921056m, not zero",
    abs(next_eq_pv(E_rel, 1 / 31_536_000) - hull_778) < 1.0
    and abs(next_eq_pv(1.0, 1.0) / 1e6 - 3.921056) < 5e-7,
)
# Equity-for-SOFR: the floating payment compounds overnight SOFR over the period; A_t = 1.019 is the realised
# compounded return since the reset (1.900%). Investing A_t N in overnight deposits until T_next and owing N
# replicates it, so its PV is N(A_t - P); later floating payments are worth N(P_(k-1) - P_k), the same as the later
# equity payments.
A_t = 1.019
next_fl = 100e6 * (A_t - P_next)
fl_leg = next_fl + 100e6 * (P_next - df_t[-1])
ok(
    "equity-for-SOFR: next floating payment 3.880133m, floating leg 14.964176m, receive-equity value 4.100m",
    abs(next_fl / 1e6 - 3.880133) < 5e-7
    and abs(fl_leg / 1e6 - 14.964176) < 5e-7
    and close(eq_val - fl_leg, 100e6 * (E_rel - A_t), 1e-6)
    and abs((eq_val - fl_leg) / 1e6 - 4.100) < 1e-9,
)


def legs(e_rel, a_on, dfs):
    """Equity and compounded-overnight floating legs, per unit notional, from payment-date discount factors."""
    later = sum(dfs[k - 1] - dfs[k] for k in range(1, len(dfs)))
    return (e_rel - dfs[0]) + later, (a_on - dfs[0]) + later


at_reset = [legs(1.0, 1.0, d_) for d_ in (df, df_t, np.exp(-0.06 * np.arange(1, 5)))]
ok(
    "immediately after a reset (E/E_reset = 1, A = 1) the equity-for-SOFR swap is worth zero on three curves,\n"
    "      although each leg alone is worth 1 - P_n",
    all(close(e_ - f_, 0, 1e-15) and e_ > 0 for e_, f_ in at_reset),
)
# Independent check by simulation, not replication: Vasicek short rate (kappa 0.5, theta 4%, sigma 1%, r_t 4%) and a
# total-return index with 20% volatility correlated 0.3 with rates, daily steps over the half year to T_next. The
# simulated PV of the next equity payment and of the compounded-overnight floating payment should match the formulas
# with the model's own P(t, T_next), whatever the rate dynamics.
rng_eq = np.random.default_rng(20261018)
n_paths, n_steps, h_t = 40000, 126, 0.5
dt_e = h_t / n_steps
kap, th, sg_r, sg_e, rho = 0.5, 0.04, 0.01, 0.20, 0.3
r_path = np.full(n_paths, 0.04)
log_E = np.zeros(n_paths)
int_r = np.zeros(n_paths)
growth_on = np.ones(n_paths)  # overnight compounding, simple daily interest
for _ in range(n_steps):
    z1 = rng_eq.standard_normal(n_paths)
    z2 = rho * z1 + math.sqrt(1 - rho**2) * rng_eq.standard_normal(n_paths)
    int_r += r_path * dt_e
    growth_on *= 1 + r_path * dt_e
    log_E += (r_path - 0.5 * sg_e**2) * dt_e + sg_e * math.sqrt(dt_e) * z2
    r_path = r_path + kap * (th - r_path) * dt_e + sg_r * math.sqrt(dt_e) * z1
disc = np.exp(-int_r)
B_v = (1 - math.exp(-kap * h_t)) / kap
P_vas = math.exp(
    (th - sg_r**2 / (2 * kap**2)) * (B_v - h_t) - sg_r**2 * B_v**2 / (4 * kap) - B_v * 0.04
)
pay_eq = disc * (E_rel * np.exp(log_E) - 1.0)
pay_fl = disc * (A_t * growth_on - 1.0)
se_eq = pay_eq.std() / math.sqrt(n_paths)
print(
    f"    simulated next equity PV {pay_eq.mean():.6f} (se {se_eq:.6f}); formula {E_rel - P_vas:.6f}; "
    f"N(E/E0-1) form {E_rel - 1:.6f}; floating {pay_fl.mean():.6f} vs {A_t - P_vas:.6f}"
)
ok(
    "simulation: next equity payment PV matches E/E0 - P(t,T) within 4 standard errors and rejects E/E0 - 1",
    abs(pay_eq.mean() - (E_rel - P_vas)) < 4 * se_eq
    and abs(pay_eq.mean() - (E_rel - 1)) > 20 * se_eq,
)
se_fl = pay_fl.std() / math.sqrt(n_paths)
ok(
    "simulation: compounded-overnight floating payment PV matches A_t - P(t,T) within 4 standard errors",
    abs(pay_fl.mean() - (A_t - P_vas)) < 4 * se_fl + 5e-6,
)

print()
if fails:
    print(f"{len(fails)} check(s) failed: {fails}")
    sys.exit(1)
print("all checks passed")
