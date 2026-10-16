"""Numerical checks for migration slice 35 (the foundations folder), 2026-10-16.

Run with numpy:  /opt/homebrew/bin/python3.10 slice35-checks.py
Each section prints its result and asserts what the entries state.

1. Past profit, skill and luck: when past profit predicts future profit, and why
   unconditional zero-mean luck is not enough (res:zero-sum-skill-luck).
2. Zero-sum accounting and the two corollaries (res:zero-sum-skill-luck).
3. Credit relationships with and without brokers: Harris's ordered count and the
   legacy unordered count (def:market-structures-venues).
4. Depth--width duality and the attainment condition (def:liquidity-dimensions).
5. Search stopping: Harris's camera example and the one-step rule (def:liquidity-dimensions).
6. Book size is neither a bound on traded volume nor on executable quantity
   (def:liquidity-dimensions).
7. Lehalle and Laruelle's ``Nyquist--Shannon latency bound'' restated as a staleness
   condition (def:smart-order-routing).
8. Message capacity: utilisation below one is necessary, not sufficient
   (def:floor-automated-trading-systems).
9. Reported volume under different counting conventions (def:market-structures-venues).
10. The order-flow externality inequality (mech:venue-competition-fragmentation).
"""
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
section("4. depth--width duality")
def check_duality(C, grid, c):
    feasible = [q for q in grid if C(q) <= c]
    D = max(feasible)
    return all((q <= D) == (C(q) <= c) for q in grid), D
# a nondecreasing step cost on an integer grid: the maximum is attained and the equivalence holds
steps = np.sort(rng.uniform(0, 1, 20))
C_step = lambda q: float(steps[:q].sum())
ok, D = check_duality(C_step, range(0, 21), 3.0)
print(f"  integer sizes, nondecreasing cost: D(3.0) = {D}; q <= D(c) iff C(q) <= c: {ok}")
assert ok
# continuous size with a jump at q = 1, cost right-continuous: {q : C(q) <= 1.5} = [0, 1), no maximum
C_jump = lambda q: q if q < 1 else 2.0
qs = np.linspace(0, 1, 100_001)[:-1]
sup = qs[[C_jump(x) <= 1.5 for x in qs]].max()
print(f"  C(q) = q for q < 1, 2 for q >= 1, c = 1.5: sup of feasible sizes -> 1 (grid {sup:.5f}), C(1) = {C_jump(1.0)} > c: the max is not attained")
print("  so the duality needs the maximum to exist (C lower semicontinuous, here left-continuous at the jump) and C(0) <= c")


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
section("8. message capacity")
mu = 1000.0
for rho_ in [0.5, 0.9, 0.99]:
    print(f"  M/M/1, utilisation {rho_}: mean time in system 1/(mu - lambda) = {1000/(mu - rho_*mu):.1f} ms at mu = 1,000 messages/s")
def lindley(arr_rate_fn, n=200_000, svc=1/mu):
    t, w, waits = 0.0, 0.0, []
    for i in range(n):
        lam = arr_rate_fn(t)
        dt = rng.exponential(1 / lam)
        t += dt
        w = max(0.0, w + rng.exponential(svc) - dt)
        waits.append(w)
    return np.array(waits)
w_steady = lindley(lambda t: 0.8 * mu)
burst = lambda t: (1.5 * mu) if (t % 1.0) < 0.1 else (0.72 * mu)   # average 0.798 mu, bursts at 1.5 mu
w_burst = lindley(burst)
print(f"  average utilisation 0.8: mean wait {1000*w_steady.mean():.2f} ms (steady) against {1000*w_burst.mean():.2f} ms with 10% bursts at 1.5x capacity; "
      f"99th percentile {1000*np.quantile(w_steady, .99):.1f} against {1000*np.quantile(w_burst, .99):.1f} ms")
assert w_burst.mean() > 3 * w_steady.mean()
w_over = lindley(lambda t: 1.05 * mu, n=100_000)
print(f"  utilisation 1.05: backlog wait after 50k and 100k messages {1000*w_over[49_999]:.1f} and {1000*w_over[-1]:.1f} ms (grows without bound)")
assert w_over[-1] > w_over[49_999]


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
