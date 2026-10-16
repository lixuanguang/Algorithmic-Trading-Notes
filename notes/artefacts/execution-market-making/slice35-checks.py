"""Numerical checks for migration slice 35 (the foundations folder), 2026-10-16.

Run with numpy:  /opt/homebrew/bin/python3.10 slice35-checks.py
Each section prints its result and asserts what the entries state.

1. Past profit, skill and luck: when past profit predicts future profit, and why
   unconditional zero-mean luck is not enough (res:zero-sum-skill-luck).
2. Zero-sum accounting and the two corollaries (res:zero-sum-skill-luck).
3. Credit relationships with and without brokers: Harris's ordered count and the
   legacy unordered count (def:market-structures-venues).
4. Depth--width duality per unit, against a cash budget, and the attainment conditions
   (def:liquidity-dimensions; corrected in the slice-35 follow-up).
5. Search stopping: Harris's camera example and the one-step rule (def:liquidity-dimensions).
6. Book size is neither a bound on traded volume nor on executable quantity
   (def:liquidity-dimensions).
7. Lehalle and Laruelle's ``Nyquist--Shannon latency bound'' restated as a staleness
   condition (def:smart-order-routing).
8. Message capacity: for M/M/1, utilisation below one is necessary and sufficient for
   stability; delay, deadlines, bursts and buffers are separate questions
   (def:floor-automated-trading-systems; corrected in the slice-35 follow-up).
9. Reported volume under different counting conventions (def:market-structures-venues).
10. The order-flow externality inequality (mech:venue-competition-fragmentation).
"""
import collections

import numpy as np

rng = np.random.default_rng(35)


def section(title):
    print("\n== " + title)


# 1. Skill and luck ---------------------------------------------------------------
section("1. past profit, skill and luck")
M, T = 200_000, 2
# (a) skill unknown to the evaluator, luck i.i.d. and independent of skill
tau, sigma = 0.5, 1.0
S = rng.normal(0.0, tau, M)
P = S[:, None] + rng.normal(0.0, sigma, (M, T))
slope_a = np.cov(P[:, 0], P[:, 1])[0, 1] / np.var(P[:, 0])
theory_a = tau**2 / (tau**2 + sigma**2)
print(f"  unknown skill, i.i.d. luck: slope of profit(t+1) on profit(t) {slope_a:.3f}; tau^2/(tau^2+sigma^2) = {theory_a:.3f}")
assert abs(slope_a - theory_a) < 0.01
# (b) no skill at all, luck i.i.d.: past profit has no predictive value
P0 = rng.normal(0.0, sigma, (M, T))
slope_b = np.cov(P0[:, 0], P0[:, 1])[0, 1] / np.var(P0[:, 0])
print(f"  no skill, i.i.d. luck: slope {slope_b:.4f} (0 expected)")
assert abs(slope_b) < 0.01
# (c) no skill, luck with unconditional mean zero but persistent (AR(1), rho = 0.5)
rho = 0.5
L0 = rng.normal(0.0, sigma, M)
L1 = rho * L0 + np.sqrt(1 - rho**2) * rng.normal(0.0, sigma, M)
slope_c = np.cov(L0, L1)[0, 1] / np.var(L0)
print(f"  no skill, luck AR(1) rho=0.5, E[L]=0 unconditionally: slope {slope_c:.3f}; past profit predicts luck, not skill")
assert abs(slope_c - rho) < 0.01 and abs(L1.mean()) < 0.01
# (d) skill known to the evaluator (in F_t) and luck with E[L_{t+1} | F_t, Pi_t] = 0:
#     regressing Pi_{t+1} - S on Pi_t gives zero, i.e. no incremental value
resid = P[:, 1] - S
slope_d = np.cov(P[:, 0], resid)[0, 1] / np.var(P[:, 0])
print(f"  skill in the information set, luck conditionally mean zero: incremental slope {slope_d:.4f}")
assert abs(slope_d) < 0.01


# 2. Zero-sum accounting and corollaries --------------------------------------------
section("2. zero-sum accounting")
V, Ptrade, q = 103.0, 100.0, 5
buyer, seller = q * (V - Ptrade), q * (Ptrade - V)
print(f"  buyer gain {buyer}, seller gain {seller}, sum {buyer + seller} at a common terminal value")
assert buyer + seller == 0
# closed group of profit-motivated traders: random bilateral trades, all marked at V
n, k = 10, 2_000
pos, cash = np.zeros(n), np.zeros(n)
fees = np.zeros(n)
for _ in range(k):
    i, j = rng.choice(n, 2, replace=False)
    price = V + rng.normal(0, 1)
    size = rng.integers(1, 10)
    pos[i] += size; cash[i] -= size * price
    pos[j] -= size; cash[j] += size * price
    fees[i] += 0.01 * size; fees[j] += 0.01 * size
gross = cash + pos * V
print(f"  closed group: sum of gross gains {gross.sum():.2e}; net = -total costs {(gross - fees).sum():.2f} = {-fees.sum():.2f}")
assert abs(gross.sum()) < 1e-6 and abs((gross - fees).sum() + fees.sum()) < 1e-6
# active management arithmetic: holdings that aggregate to the market portfolio
N, m = 50, 8
mkt_w = rng.dirichlet(np.ones(N))
r = rng.normal(0.01, 0.05, N)
R_M = mkt_w @ r
# managers' weights as deviations that sum (value-weighted) to the market
aum = rng.dirichlet(np.ones(m))
dev = rng.normal(0, 0.02, (m, N))
dev -= dev.mean(axis=1, keepdims=True)        # each deviation is self-financing
dev -= (aum @ dev) / aum.sum()                # value-weighted deviations cancel
W = mkt_w + dev
assert np.allclose(aum @ W, mkt_w)
a = W @ r - R_M
c = rng.uniform(0.001, 0.01, m)
print(f"  value-weighted active return {aum @ a:.2e}; net {aum @ (a - c):.5f} = -sum w c {-(aum @ c):.5f}")
assert abs(aum @ a) < 1e-12 and abs(aum @ (a - c) + aum @ c) < 1e-12
# if the actives do not aggregate to the market (e.g. other holders own a different portfolio),
# their aggregate active return need not be zero
W2 = W.copy(); W2[:, 0] += 0.05; W2 /= W2.sum(axis=1, keepdims=True)
print(f"  actives not aggregating to the market: value-weighted active return {aum @ (W2 @ r - R_M):.5f} (not 0 in general)")


# 3. Credit relationships -----------------------------------------------------------
section("3. credit relationships with and without brokers")
n_traders, B = 1_000_000, 100
ordered_direct = n_traders * (n_traders - 1)
ordered_brokered = 2 * n_traders + B * (B - 1)
print(f"  Harris (ordered checks): direct {ordered_direct:,}; brokered {ordered_brokered:,}; ratio {ordered_direct / ordered_brokered:,.0f} ('500,000 times smaller')")
assert ordered_direct == 999_999_000_000 and ordered_brokered == 2_009_900
unordered_direct = n_traders * (n_traders - 1) // 2
unordered_brokered = n_traders + B * (B - 1) // 2
print(f"  legacy (unordered pairs): direct {unordered_direct:,}; brokered n + B(B-1)/2 = {unordered_brokered:,}; ratio {unordered_direct / unordered_brokered:,.0f}")
# brute force on a small network: each client attached to exactly one broker, brokers fully linked
n_s, B_s = 12, 3
broker_of = np.arange(n_s) % B_s
edges = set()
for cl in range(n_s):
    edges.add(("c", cl, "b", int(broker_of[cl])))
for b1 in range(B_s):
    for b2 in range(b1 + 1, B_s):
        edges.add(("b", b1, "b", b2))
assert len(edges) == n_s + B_s * (B_s - 1) // 2
print(f"  brute force n={n_s}, B={B_s}: {len(edges)} undirected relationships = n + B(B-1)/2")
# a client with two brokers adds one relationship: the formula assumes one broker each
print("  assumptions: one broker per client, brokers guarantee their clients, every broker pair may trade, n counts clients only")


# 4. Depth--width duality --------------------------------------------------------------
# Corrected in the slice-35 follow-up (2026-10-16). Harris (pp. 398--399) states width as
# "the cost per unit of liquidity" and depth in "units available at a given price of
# liquidity": both are per-unit quantities. The slice-35 version inverted a cumulative
# (total) cost, which answers a cash-budget question instead.
section("4. depth--width duality (per-unit cost, not a cash budget)")
def book_costs(levels, mid, q, fee=0.0):
    """Buying q shares by sweeping (price, size) ask levels from the midpoint `mid`, with a
    fixed fee per order: returns (total cost in currency, average per-unit cost, marginal
    per-unit cost of the last share). Sizes beyond the book are infeasible (None)."""
    left, total, last = q, 0.0, None
    for price, size in levels:
        take = min(left, size)
        if take > 0:
            total += take * (price - mid)
            last = price - mid
            left -= take
        if left == 0:
            break
    if left > 0:
        return None
    total += fee
    return total, total / q, last
# (a) Harris-style counterexample: midpoint 99, 100 shares offered at 100
book1 = [(100.0, 100)]
w = lambda q: book_costs(book1, 99.0, q)[1]
C = lambda q: book_costs(book1, 99.0, q)[0]
dom = range(1, 101)
depth_per_unit = max(q for q in dom if w(q) <= 1.0)
budget_size = max(q for q in dom if C(q) <= 1.0)
print(f"  midpoint 99, 100 offered at 100: per-unit cost w(q) = {w(1):.0f} for q <= 100; depth at per-unit cost 1 = {depth_per_unit} shares;")
print(f"  total cost C(q) = q, so a cash budget of 1 buys {budget_size} share: two different questions")
assert depth_per_unit == 100 and budget_size == 1
# (b) average against marginal per-unit cost: 100 at 100 and 100 at 101
book2 = [(100.0, 100), (101.0, 100)]
dom2 = range(1, 201)
d_avg = max(q for q in dom2 if book_costs(book2, 99.0, q)[1] <= 1.5 + 1e-12)
d_marg = max(q for q in dom2 if book_costs(book2, 99.0, q)[2] <= 1.5 + 1e-12)
print(f"  adding 100 at 101: depth at average per-unit cost 1.5 = {d_avg} shares; at marginal cost 1.5 = {d_marg} shares")
assert d_avg == 200 and d_marg == 100
# (c) with a nondecreasing per-unit cost on a finite lot grid the equivalence holds;
#     the 20 uniform draws keep the random stream of later sections unchanged
gaps = np.sort(rng.uniform(0, 1, 20))
book3 = [(99.0 + 0.01 + g, 10) for g in gaps]          # 20 levels of 10 shares above mid 99
dom3 = range(1, 201)
w3 = {q: book_costs(book3, 99.0, q)[1] for q in dom3}
assert all(w3[q] <= w3[q + 1] + 1e-12 for q in range(1, 200))   # sweeping: nondecreasing
ok = True
for wbar in np.linspace(0.05, 1.0, 40):
    feas = [q for q in dom3 if w3[q] <= wbar]
    if feas:
        D = max(feas)
        ok &= all((q <= D) == (w3[q] <= wbar) for q in dom3)
print(f"  random 20-level book, lots 1..200, nondecreasing average cost: q <= D(wbar) iff w(q) <= wbar for 40 levels: {ok}")
assert ok
# (d) a fixed fee per order makes the average per-unit cost fall with size: not monotone
F = 50.0
wf = {q: book_costs(book2, 99.0, q, fee=F)[1] for q in dom2}
feas = [q for q in dom2 if wf[q] <= 1.5 + 1e-12]
print(f"  fee {F:.0f} per order: w(1) = {wf[1]:.1f}, w(50) = {wf[50]:.1f}, w(100) = {wf[100]:.2f}, w(150) = {wf[150]:.3f}; feasible set at 1.5 = {feas}")
assert feas == [100] and wf[50] > 1.5          # q = 50 <= D = 100 but w(50) > 1.5: the equivalence fails
# (e) attainment on an interval domain [q_min, qbar]
qs = np.linspace(0.01, 3.0, 299_001)
def sup_and_attained(wfun, wbar):
    feas = qs[np.array([wfun(x) <= wbar for x in qs])]
    s = feas.max()
    return s, wfun(s) <= wbar
w_rc = lambda q: q if q < 1 else 2.0                      # right-continuous jump at 1: not LSC
s, _ = sup_and_attained(w_rc, 1.5)
print(f"  w(q) = q below 1 and 2 from 1 on, wbar 1.5: feasible [q_min, 1), grid sup {s:.5f}, w(1) = {w_rc(1.0)} > 1.5: no maximum")
assert w_rc(1.0) > 1.5 and s < 1.0
w_nlsc = lambda q: q if q <= 1 else (2.0 if q < 2 else 5.0)  # jumps up at 2, w(2) = 5 > liminf 2: not LSC at 2
s, att = sup_and_attained(w_nlsc, 1.5)
print(f"  w(q) = q on [q_min,1], 2 on (1,2), 5 on [2,3] (not lower semicontinuous at 2), wbar 1.5: max {s:.3f} attained = {att}")
assert att and abs(s - 1.0) < 1e-9
print("  lower semicontinuity with a compact domain is sufficient, not necessary; on [q_min, inf) a constant w < wbar")
print("  is continuous and has no maximal feasible size, so boundedness is needed as well")
# second slice-35 follow-up: units. w in currency per share gives C = q w; w in basis points of
# the midpoint m gives C = q m w_bp / 10,000
q_, m_, w_bp = 100, 100.0, 10.0
C_cash = q_ * m_ * w_bp / 10_000
print(f"  units: {q_} shares at midpoint {m_:.0f} and {w_bp:.0f} bp cost C = q m w_bp/10,000 = {C_cash:.0f} (currency); "
      f"the same cost as w = {m_*w_bp/10_000:.2f} per share")
assert abs(C_cash - 10.0) < 1e-12 and abs(q_ * (m_ * w_bp / 10_000) - C_cash) < 1e-12


# 5. Search stopping ---------------------------------------------------------------------
section("5. search stopping")
gain = 10 * 0.25
cost = 30 * 5 / 60
print(f"  Harris's camera: expected gain from one more search < {gain:.2f}; cost > {cost:.2f}; stop (p. 395)")
assert gain <= cost
# one-step rule with recall and i.i.d. offers equals the reservation-value rule: stop when
# E[(X - best)^+] <= c; for X ~ U(0,1), (1 - r)^2 / 2 = c gives r.
cst = 0.02
r_star = 1 - np.sqrt(2 * cst)
def run(policy, n_runs=100_000):
    tot = 0.0
    for _ in range(n_runs // 1000):
        X = rng.uniform(0, 1, (1000, 200))
        best = np.maximum.accumulate(X, axis=1)
        stop = np.argmax(policy(best), axis=1)
        tot += (best[np.arange(1000), stop] - cst * (stop + 1)).sum()
    return tot / n_runs
v_res = run(lambda best: best >= r_star)
v_lo = run(lambda best: best >= r_star - 0.1)
v_hi = run(lambda best: best >= min(r_star + 0.05, 0.999))
print(f"  U(0,1) offers, cost 0.02: reservation {r_star:.3f}; net value {v_res:.4f} against {v_lo:.4f} (stop earlier) and {v_hi:.4f} (later)")
assert v_res > v_lo and v_res > v_hi
# without recall (the best match may disappear), the expected loss L enters the comparison
print("  bilateral search: if the best match disappears with probability p, add L = p x (its value over the fallback) to the cost side")


# 6. Book size --------------------------------------------------------------------------
section("6. book size against traded and executable quantity")
print(f"  replenishment (Lehalle and Laruelle, p. 144): best bid 20 throughout, 100 trades of 19 -> {100 * 19} traded in 5 min, far above the displayed size")
assert 100 * 19 == 1900
print("  a sweep through several limits trades 2,000 against 10 displayed at the best bid; hidden or iceberg orders add executable size;")
print("  cancellations before arrival remove it, so displayed size bounds neither traded nor executable quantity in general")


# 7. Latency and book staleness ------------------------------------------------------------
section("7. the 'Nyquist--Shannon latency bound' as a staleness condition")
for one_way_ms, f_hz in [(2, 250), (2, 500), (4, 125)]:
    T = 2 * one_way_ms / 1000            # round trip, decision time ignored
    print(f"  one-way {one_way_ms} ms, round trip {1000*T:.0f} ms, update rate {f_hz} Hz: f*T = {f_hz*T:.2f}; "
          f"Poisson P(no update during round trip) = {np.exp(-f_hz*T):.3f}; periodic updates: {max(0.0, 1 - f_hz*T):.3f}")
f_thr = 1 / (2 * 0.002)
assert abs(f_thr - 250) < 1e-9 and abs(1 / (2 * 0.004) - 125) < 1e-9
print("  LL's threshold f = 1/(2 x one-way latency) = 1/(round trip): the 2 is the round trip, not a sampling-theorem factor;")
print("  with random updates the book is unchanged over the round trip with probability exp(-fT) = 0.368 at the threshold, so there is no sharp boundary")
assert abs(np.exp(-1) - 0.3679) < 1e-4


# 8. Capacity ----------------------------------------------------------------------------
# Corrected in the slice-35 follow-up (2026-10-16). (i) For the stated M/M/1 queue (Poisson
# arrivals at total rate lam = N x lambda, exponential service at rate mu, one server, unlimited
# buffer, FIFO), lam < mu is necessary and sufficient for stability; stability says nothing
# about delay. (ii) The slice-35 burst simulation drew each inter-arrival gap from the rate in
# force at the previous arrival, so a gap that crossed a rate boundary kept the old rate; its
# average rate was not the one stated. Arrivals are now sampled by thinning, which is exact for
# a piecewise-constant rate. (iii) Waiting time in queue W and time in system T = W + S are
# reported separately. Section 8 has its own generator so that no other section changes.
section("8. message capacity: stability, delay and bursts")
rq = np.random.default_rng(3508)
mu = 1000.0                                   # messages per second
for rho_ in [0.5, 0.9, 0.99]:
    lam = rho_ * mu
    print(f"  M/M/1, utilisation {rho_}: mean wait in queue rho/(mu - lam) = {1000*rho_/(mu - lam):.1f} ms, "
          f"mean time in system 1/(mu - lam) = {1000/(mu - lam):.1f} ms")

def thinning(rate_fn, rate_max, horizon):
    """Exact non-homogeneous Poisson arrival times on [0, horizon) for rate_fn <= rate_max."""
    n = rq.poisson(rate_max * horizon)
    cand = np.sort(rq.uniform(0.0, horizon, n))
    keep = rq.uniform(0.0, 1.0, n) < rate_fn(cand) / rate_max
    return cand[keep]

def fifo(arrivals):
    """Single exponential server, FIFO, unlimited buffer: Lindley recursion.
    Returns waits in queue W and service times S (time in system T = W + S)."""
    S = rq.exponential(1.0 / mu, arrivals.size)
    W = np.empty(arrivals.size)
    w, prev = 0.0, arrivals[0]
    for i, a in enumerate(arrivals):
        if i:
            w = max(0.0, w + S[i - 1] - (a - prev))
        W[i] = w
        prev = a
    return W, S

H = 400.0                                     # seconds simulated; first 20 s discarded as warm-up
# (a) constant rate 0.8 mu against the M/M/1 formulas
lam = 0.8 * mu
arr = thinning(lambda t: np.full_like(t, lam), lam, H)
W, S = fifo(arr)
m = arr >= 20.0
T = W + S
th_W, th_T = 0.8 / (mu - lam), 1.0 / (mu - lam)
th_W99 = np.log(0.8 / 0.01) / (mu - lam)      # P(W > x) = rho exp(-(mu - lam) x)
th_T99 = np.log(100.0) / (mu - lam)           # T ~ Exp(mu - lam)
d = 0.010
print(f"  constant rate: realised rate {arr.size / H:.1f}/s (target {lam:.0f}); mean wait {1000*W[m].mean():.2f} ms "
      f"(theory {1000*th_W:.2f}); mean time in system {1000*T[m].mean():.2f} ms (theory {1000*th_T:.2f})")
print(f"    99th percentiles: wait {1000*np.quantile(W[m], .99):.1f} ms (theory {1000*th_W99:.1f}); "
      f"time in system {1000*np.quantile(T[m], .99):.1f} ms (theory {1000*th_T99:.1f}); "
      f"P(T > {1000*d:.0f} ms) = {np.mean(T[m] > d):.3f} (theory {np.exp(-(mu - lam)*d):.3f})")
assert abs(arr.size / H - lam) / lam < 0.01
assert abs(W[m].mean() - th_W) / th_W < 0.05 and abs(T[m].mean() - th_T) / th_T < 0.05
assert abs(np.quantile(T[m], .99) - th_T99) / th_T99 < 0.08
assert abs(np.mean(T[m] > d) - np.exp(-(mu - lam) * d)) < 0.01

# (b) periodic bursts: 1.5 mu for the first 10% of each second, a lower rate otherwise, with the
#     low rate set so that the average is exactly 0.8 mu
hi, frac, avg = 1.5 * mu, 0.1, 0.8 * mu
lo = (avg - frac * hi) / (1 - frac)
rate = lambda t: np.where((t % 1.0) < frac, hi, lo)
arr_b = thinning(rate, hi, H)
Wb, Sb = fifo(arr_b)
mb = arr_b >= 20.0
Tb = Wb + Sb
print(f"  bursts: 1.5 mu for 0.1 s of every second, {lo/mu:.4f} mu otherwise; realised average rate "
      f"{arr_b.size / H:.1f}/s (target {avg:.0f}); in-burst rate {np.mean((arr_b % 1.0) < frac) * arr_b.size / (frac*H):.0f}/s")
assert abs(arr_b.size / H - avg) / avg < 0.01
print(f"    mean wait {1000*Wb[mb].mean():.2f} ms against {1000*W[m].mean():.2f} ms at a constant rate with the same average; "
      f"mean time in system {1000*Tb[mb].mean():.2f} against {1000*T[m].mean():.2f} ms")
print(f"    99th percentile time in system {1000*np.quantile(Tb[mb], .99):.1f} against {1000*np.quantile(T[m], .99):.1f} ms; "
      f"P(T > 10 ms) {np.mean(Tb[mb] > d):.3f} against {np.mean(T[m] > d):.3f}")
# fluid approximation of the burst: backlog grows at hi - mu for 0.1 s and drains at mu - lo
peak = (hi - mu) * frac
drain = peak / (mu - lo)
phase = arr_b % 1.0
end_burst = mb & (phase > 0.095) & (phase < 0.1)
print(f"    fluid view: backlog peaks near (hi - mu) x 0.1 s = {peak:.0f} messages, about {1000*peak/mu:.0f} ms of work, "
      f"and drains in {drain:.2f} s; simulated mean wait at the end of a burst {1000*Wb[end_burst].mean():.1f} ms")
assert Wb[mb].mean() > W[m].mean() and abs(Wb[end_burst].mean() - peak / mu) < 0.02
# (c) the same peak rate in shorter bursts with the same average: delay depends on duration
for frac2 in [0.1, 0.02, 0.005]:
    a2 = thinning(lambda t, f=frac2: np.where((t % 1.0) < f, hi, (avg - f * hi) / (1 - f)), hi, H)
    W2, S2 = fifo(a2)
    m2 = a2 >= 20.0
    print(f"    burst of {1000*frac2:.0f} ms at 1.5 mu once a second (average 0.8 mu): mean wait {1000*W2[m2].mean():.2f} ms, "
          f"99th percentile time in system {1000*np.quantile((W2 + S2)[m2], .99):.1f} ms, P(T > 10 ms) {np.mean((W2 + S2)[m2] > d):.3f}")
# (d) a finite buffer: messages arriving when K are already in the system are rejected
def fifo_buffer(arrivals, K):
    S = rq.exponential(1.0 / mu, arrivals.size)
    rejected = 0
    q = collections.deque()                   # departure times of messages in the system
    for a, s in zip(arrivals, S):
        while q and q[0] <= a:
            q.popleft()
        if len(q) >= K:
            rejected += 1
            continue
        start = max(a, q[-1] if q else a)
        q.append(start + s)
    return rejected / arrivals.size
for K in [20, 100]:
    print(f"    buffer of {K} messages: rejected share {fifo_buffer(arr_b, K):.4f} with bursts against "
          f"{fifo_buffer(arr, K):.5f} at a constant rate (M/M/1/{K} theory {(1-0.8)*0.8**K/(1-0.8**(K+1)):.5f})")
# (e) overload: utilisation above one, backlog grows without bound
over = thinning(lambda t: np.full_like(t, 1.05 * mu), 1.05 * mu, 100.0)
Wo, So = fifo(over)
print(f"  utilisation 1.05: wait at 50 s and 100 s {1000*Wo[over < 50].max():.0f} and {1000*Wo[-1]:.0f} ms "
      f"(fluid growth 0.05 s of work per second: {50*0.05*1000:.0f} and {100*0.05*1000:.0f} ms)")
assert Wo[-1] > Wo[over < 50].max()


# (f) the slice-35 sampler, kept for the record: each gap drawn from the rate in force at the
#     previous arrival, with a low rate of 0.72 mu (stated average 0.798 mu)
def old_sampler(n, hi_=1.5 * mu, lo_=0.72 * mu):
    t, out = 0.0, np.empty(n)
    for i in range(n):
        t += rq.exponential(1.0 / (hi_ if (t % 1.0) < 0.1 else lo_))
        out[i] = t
    return out
old = old_sampler(200_000)
print(f"  slice-35 sampler: stated average 0.798 mu = 798/s; realised {old.size / old[-1]:.1f}/s over {old[-1]:.0f} s "
      f"(in-burst share of arrivals {np.mean((old % 1.0) < 0.1):.4f} against 0.1 x 1.5 / 0.798 = {0.15/0.798:.4f})")


# 9. Volume counting -----------------------------------------------------------------------
section("9. reported volume")
for label, legs in [("public buyer to public seller", 1), ("one dealer in between", 2), ("two dealers", 3)]:
    print(f"  {label}: a 100-share public trade reports {100*legs} shares (Harris, p. 48)")


# 10. Order-flow externality ------------------------------------------------------------------
section("10. order-flow externality")
s_m, c_m, s_e, c_e = 1.0, 0.30, 1.2, 0.25
ell = lambda F: np.log(F)
F_m, F_e = 1000.0, 50.0
U_m, U_e = s_m - c_m + ell(F_m), s_e - c_e + ell(F_e)
print(f"  entrant better on service net of cost by {(s_e-c_e)-(s_m-c_m):.2f}; liquidity gap ell(F_m) - ell(F_e) = {ell(F_m)-ell(F_e):.2f}; "
      f"U_m = {U_m:.2f} > U_e = {U_e:.2f}: the trader stays")
assert U_m > U_e and (ell(F_m) - ell(F_e)) > (s_e - c_e) - (s_m - c_m)

print("\nall checks passed")
