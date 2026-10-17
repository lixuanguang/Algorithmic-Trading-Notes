"""order matching and fragmentation review (2026-10-16): independent checks for the order-instruction, matching, dark-trading and fragmentation entries.

Each block recomputes a source's example or a derived claim from first principles, or gives a counterexample.
Run: /opt/homebrew/bin/python3.10 order-routing-fragmentation-checks.py   (numpy, scipy; fixed seeds; a few seconds)
"""
from fractions import Fraction as Fr

import numpy as np
from scipy import stats

rng = np.random.default_rng(34)


def head(t):
    print('\n== ' + t)


# ------------------------------------------------------------------ single-price auction on Harris's Table 6-1
head("single-price auction on Harris's Table 6-1 orders (chap. 6, pp. 118-125): clearing price, volume, surplus")
INF = 10**6
buys = [('Bea', 3, Fr('20.0')), ('Ben', 2, Fr('20.0')), ('Bif', 4, None), ('Bob', 2, Fr('20.1')), ('Bud', 7, Fr('19.8'))]
sells = [('Sam', 2, Fr('20.1')), ('Sol', 1, Fr('19.8')), ('Stu', 5, Fr('20.2')), ('Sue', 6, Fr('20.0'))]
prices = sorted({p for *_, p in buys + sells if p is not None})


def demand(p):
    return sum(q for _, q, lim in buys if lim is None or lim >= p)


def supply(p):
    return sum(q for _, q, lim in sells if lim <= p)


rows = [(p, demand(p), supply(p), min(demand(p), supply(p)), demand(p) - supply(p)) for p in prices]
for p, d, s_, m, e in rows:
    print(f'  p={float(p):5.1f}: demand {d:2d} supply {s_:2d} matched {m:2d} excess demand {e:+d}')
mx = max(r[3] for r in rows)
cands = [r for r in rows if r[3] == mx]
surplus_min = min(abs(r[4]) for r in cands)
cands = [r for r in cands if abs(r[4]) == surplus_min]
print('rule 1 (maximum volume) and rule 2 (minimum surplus) leave', [float(r[0]) for r in cands], 'with volume', mx)
assert [float(r[0]) for r in cands] == [20.0] and mx == 7

# surplus: valuations = limit prices, market buyer valued at 20.3 (Harris's assumption)
val = {n: (lim if lim is not None else Fr('20.3')) for n, _, lim in buys + sells}
p_star = Fr('20.0')
uniform_trades = [('Sol', 'Bif', 1), ('Sue', 'Bif', 3), ('Sue', 'Bob', 2), ('Sue', 'Bea', 1)]
s_uniform = sum((val[b] - val[s]) * q for s, b, q in uniform_trades)
cont_trades = [('Sol', 'Bea', Fr('20.0'), 1), ('Sam', 'Bif', Fr('20.1'), 2), ('Stu', 'Bif', Fr('20.2'), 2),
               ('Sue', 'Bob', Fr('20.1'), 2), ('Sue', 'Bea', Fr('20.0'), 2), ('Sue', 'Ben', Fr('20.0'), 2)]
s_cont = sum((val[b] - val[s]) * q for s, b, _, q in cont_trades)
print(f'total surplus: single price {float(s_uniform):.1f} on 7 units; continuous {float(s_cont):.1f} on 11 units'
      ' (Harris Tables 6-7 and 6-9: 1.6 and 1.0); the surplus of a trade does not depend on its price')
assert s_uniform == Fr('1.6') and s_cont == Fr('1.0')
bif_cont = (Fr('20.1') * 2 + Fr('20.2') * 2) / 4
print(f"Bif's average price: discriminatory {float(bif_cont):.2f} against 20.2 if his order alone set a uniform price"
      " (Harris p. 128); Sue's average 20.033 against 20.0")

# ------------------------------------------------------------------ pro-rata allocation: capacity, rounding, residual
head('pro-rata allocation (corrected 2026-10-16): capacity first, then proportional shares, rounding remainder, incoming residual')


def pro_rata(Q, resting):
    """Executable quantity is capped by eligible resting liquidity; shares are proportional to size; floors leave a
    rounding remainder for a venue rule; any excess of Q over the liquidity is the incoming order's residual."""
    E = min(Q, sum(resting))
    exact = [Fr(E * q, sum(resting)) for q in resting]
    floors = [int(x) for x in exact]
    rounding = E - sum(floors)
    residual = Q - E
    assert all(f <= q for f, q in zip(floors, resting)), 'no order fills beyond its size'
    assert sum(floors) + rounding + residual == Q, 'quantity conserved'
    assert sum(floors) + rounding <= sum(resting), 'capacity respected'
    return E, exact, floors, rounding, residual


cases = [('Harris p. 117', 18, [10, 20]), ('undersubscribed, fractional', 10, [4, 4, 4]),
         ('equal', 12, [4, 4, 4]), ('oversubscribed', 10, [3, 3, 3]), ('small orders', 7, [1, 1, 100])]
for name, Q, rest in cases:
    E, exact, floors, rounding, residual = pro_rata(Q, rest)
    print(f'  {name:28} Q={Q:2d} vs {rest}: executable {E}, exact {[str(x) for x in exact]}, floors {floors},'
          f' rounding remainder {rounding} (venue rule), unexecuted incoming residual {residual}')
assert pro_rata(10, [3, 3, 3])[1:] == ([3, 3, 3], [3, 3, 3], 0, 1)
assert pro_rata(10, [4, 4, 4])[3:] == (1, 0)
print('POSIT example (p. 134): sell 3,000 against buys 5,000 and 10,000 ->', pro_rata(3000, [5000, 10000])[2])

# ------------------------------------------------------------------ posting against crossing: explicit cash flows
head('posting against crossing (corrected 2026-10-16): equal target quantity, common terminal mark, pathwise cash flows')


def outcomes(ask0, bid0, filled, chase_price, mark):
    """Buy one unit by the horizon. Crossing pays ask0 now. Posting pays bid0 if filled, otherwise buys at the horizon
    at chase_price. Both end long one unit, marked at the same terminal price."""
    cross = mark - ask0
    post = mark - (bid0 if filled else chase_price)
    return cross, post, post - cross


c, p_, g = outcomes(100, 99, True, None, 97)
print(f'  fill at 99 vs buy at 100, mark 97: crossing {c:+}, posting {p_:+}, posting gain {g:+} (= the spread saved;'
      ' the fall to 97 hits both)')
assert g == 1
c, p_, g = outcomes(100, 99, False, 101.5, 103)
print(f'  miss, chase at 101.5, mark 103: crossing {c:+}, posting {p_:+}, posting gain {g:+} (= ask0 - chase price)')
assert g == -1.5
# pathwise check on a random-walk midprice with a fill rule; the identity gain = p*S - (1-p)*M holds by construction
rng_p = np.random.default_rng(341)
n, steps, half = 200_000, 50, 0.5
mid0 = 100.0
z = rng_p.standard_normal((n, steps)).cumsum(1) * 0.2
mins, last = z.min(1), z[:, -1]
filled = mins <= -2 * half             # the bid at mid0 - half is reached if the mid falls one full spread below it
chase = mid0 + last + half               # buy at the horizon ask if missed
mark = mid0 + last
cross = mark - (mid0 + half)
post = np.where(filled, mark - (mid0 - half), mark - chase)
gain = post - cross
p_fill = filled.mean(); S = 2 * half; M = (chase - (mid0 + half))[~filled].mean()
print(f'  random walk: P(fill) {p_fill:.3f}; mean pathwise gain {gain.mean():+.4f}; p*S - (1-p)*M = {p_fill * S - (1 - p_fill) * M:+.4f}')
assert abs(gain.mean() - (p_fill * S - (1 - p_fill) * M)) < 1e-9
A = (mid0 - half - mark)[filled].mean()  # the post-fill fall, the old formula's 'A'
print(f'  the old formula subtracts A = E[fill price - mark | fill] = {A:+.3f} from the posting branch only; the same fall'
      f' hits the crossing position, so p(S-A)-(1-p)M = {p_fill * (S - A) - (1 - p_fill) * M:+.4f} misstates the gain')

# ------------------------------------------------------------------ ex-fixing share
head('ex-fixing market share: (M - m p)/(1 - p) against the printed (1 - m p) M/(1 - p); equal iff m p (1 - M) = 0')


def ex_fixing(M, m, p):
    assert 0 <= p < 1 and 0 <= m <= 1 and m * p <= M <= m * p + (1 - p), 'shares must be feasible'
    return (M - m * p) / (1 - p)


for M_, m_, p_ in [(0.60, 1.0, 0.20), (0.30, 0.0, 0.20), (0.70, 1.0, 0.25), (1.0, 1.0, 0.2), (0.4, 0.5, 0.0)]:
    exact = ex_fixing(M_, m_, p_)
    printed = (1 - m_ * p_) * M_ / (1 - p_)
    agree = abs(exact - printed) < 1e-12
    assert agree == (abs(m_ * p_ * (1 - M_)) < 1e-12)
    print(f'  M={M_}, m={m_}, p={p_}: ex-fixing {exact:.4f}; printed {printed:.4f}; agree {agree} (m p (1-M) = {m_ * p_ * (1 - M_):.3f})')
print('  a monopolist (M = m = 1) has share 1 ex-fixing under both; p = 1 (all volume in auctions) leaves it undefined')

head('FEI = entropy / log N (app. A.1) and an empty venue added')
q = np.array([0.6, 0.25, 0.15])
H = -(q * np.log(q)).sum()
F3 = H / np.log(3)
F4 = H / np.log(4)
print(f'q={q}: F(N=3) = {F3:.4f}; with an empty fourth venue F = {F4:.4f} = log3/log4 x F(N=3) = {np.log(3) / np.log(4) * F3:.4f}')
print('uniform -> F =', round(float(-(np.full(4, .25) * np.log(np.full(4, .25))).sum() / np.log(4)), 6), '; one venue -> 0')

head('Gini from the Lorenz curve, G = 1 - 2 int L (app. A.9.1)')


def gini(x):
    x = np.sort(np.asarray(x, float))
    L = np.concatenate([[0], np.cumsum(x) / x.sum()])
    u = np.linspace(0, 1, len(L))
    return 1 - 2 * np.trapz(L, u)


def gini_mean_diff(x):
    x = np.asarray(x, float)
    return np.abs(x[:, None] - x[None, :]).sum() / (2 * len(x) ** 2 * x.mean())


x = rng.lognormal(0, 1.2, 101)
print(f'  lognormal turnover of 101 stocks: Lorenz Gini {gini(x):.4f}; half relative mean difference {gini_mean_diff(x):.4f}')
print('  equal turnover ->', round(gini(np.ones(50)), 6), '; LL Table A.3: B = 0.18 -> G = 1 - 2B =', 1 - 2 * 0.18)
srt = np.sort(x)[::-1]
cov80 = (np.searchsorted(np.cumsum(srt) / srt.sum(), 0.8) + 1) / len(srt)
print(f'  coverage (share of stocks needed for 80 percent of turnover): {cov80:.2f}; 0.80 for equal turnover')

head('two-sample KS: failure to reject is not equality of distributions')
fails = 0
for _ in range(1000):
    a = rng.normal(0, 1, 30)
    b = rng.normal(0.3, 1.2, 30)          # different distributions
    fails += stats.ks_2samp(a, b).pvalue > 0.05
print(f'  N(0,1) against N(0.3,1.2^2), 30 observations each: not rejected at 5 percent in {fails / 10:.1f} percent of 1,000 trials')
n, m = 120, 120
print(f'  LL Table A.4 statistics for SBF 120 (n=m=120 assumed here): critical D at 5 percent ~'
      f' {1.358 * np.sqrt((n + m) / (n * m)):.3f}; observed 0.1207 (2010) and 0.0833 (2012) fail to reject, nothing more')

# ------------------------------------------------------------------ market-share estimators and their variance
head('venue-share estimators (corrected 2026-10-16): count and value shares, and the fixed-weight index estimator')
rng_v = np.random.default_rng(342)
p_true, n_tr = 0.3, 2000
iid = rng_v.binomial(1, p_true, (4000, n_tr)).mean(1)
print(f'  count share, independent trades: sd {iid.std():.4f} against sqrt(p(1-p)/n) {np.sqrt(p_true * (1 - p_true) / n_tr):.4f}')
vals = rng_v.lognormal(0, 1.5, n_tr)            # fixed trade values
X = rng_v.binomial(1, p_true, (4000, n_tr))
vshare = (X * vals).sum(1) / vals.sum()
n_eff = vals.sum() ** 2 / (vals ** 2).sum()
print(f'  value share, fixed trade values, independent venues: sd {vshare.std():.4f} against sqrt(p(1-p)/n_eff)'
      f' {np.sqrt(p_true * (1 - p_true) / n_eff):.4f} with n_eff = {n_eff:.0f} of {n_tr} trades')
runs = np.array([rng_v.binomial(1, p_true, n_tr // 20).repeat(20).mean() for _ in range(4000)])
print(f'  count share with venue choices repeated in runs of 20: sd {runs.std():.4f}; binomial {np.sqrt(p_true * (1 - p_true) / n_tr):.4f}')


def var_diff(w, sig2, k, cov=None):
    a = -np.asarray(w, float); a[k] += 1.0                  # p_hat_k - sum_j w_j p_hat_j
    C = np.diag(sig2) if cov is None else np.asarray(cov)
    return float(a @ C @ a)


w, p_, n_ = np.array([0.9, 0.1]), np.array([0.5, 0.5]), np.array([100, 100])
s2 = p_ * (1 - p_) / n_
correct = var_diff(w, s2, 0)
book = (1 - 2 * w[0]) * s2[0] + 0.5 * 0.5 / n_.sum()
print(f'  w=(0.9,0.1), p=(0.5,0.5), n=(100,100): Var(p_1 - p_hat) = (1-w1)^2 s1 + w2^2 s2 = {correct:.5f};'
      f' the printed formula with pooled n = 200 gives {book:+.5f}')
assert abs(correct - 0.00005) < 1e-12 and abs(book + 0.00075) < 1e-12
sims = rng_v.binomial(n_, p_, (400_000, 2)) / n_
diff = sims[:, 0] - sims @ w
print(f'  simulated variance {diff.var():.6f}')

# ------------------------------------------------------------------ SOR objective, gradient and a consistent learner
head('SOR objective (corrected 2026-10-16): E[sum_k min(r_k V, D_k)]; marginal value E[V 1{r_k V < D_k}]')
scen = [(1.0, np.array([0.4, 0.6])), (10.0, np.array([6.0, 4.0]))]   # equally likely


def capture(r):
    return np.mean([np.minimum(r * V, D).sum() for V, D in scen])


def ind(r, weighted):
    return np.mean([(V if weighted else 1.0) * (r * V < D) for V, D in scen], axis=0)


for r in [np.array([0.5, 0.5]), np.array([0.6, 0.4])]:
    print(f'  r={r}: expected capture {capture(r):.2f}; E[1(rV<D)] {ind(r, False)}; E[V 1(rV<D)] {ind(r, True)}')
assert abs(capture(np.array([0.5, 0.5])) - 4.95) < 1e-12 and abs(capture(np.array([0.6, 0.4])) - 5.4) < 1e-12
grid = np.linspace(0, 1, 1001)
caps = [capture(np.array([x, 1 - x])) for x in grid]
print(f'  grid optimum r1 = {grid[int(np.argmax(caps))]:.3f} with capture {max(caps):.3f}: equal unweighted indicators do'
      ' not identify the optimum; the size-weighted condition does (interior: equal for all r_k > 0; boundary r_k = 0: no larger)')

head('a learner consistent with that objective, with D independent of V and E[D_k / sum D] = p_k (Lehalle-Laruelle eq. A.10)')
rng_s = np.random.default_rng(343)
K, nu = 3, 0.8


def draw_D(mu, size):
    return mu * np.exp(rng_s.normal(-nu ** 2 / 2, nu, (size, K)))   # sd proportional to the mean (common nu)


def calibrate(p_target, iters=60, size=40_000):
    mu = p_target.copy()
    Z = rng_s.normal(-nu ** 2 / 2, nu, (size, K))
    for _ in range(iters):
        D = mu * np.exp(Z)
        share = (D / D.sum(1, keepdims=True)).mean(0)
        mu = mu * p_target / share
        mu = mu / mu.sum()
    return mu, (D / D.sum(1, keepdims=True)).mean(0)


def project_simplex(v):
    u = np.sort(v)[::-1]; css = np.cumsum(u)
    rho = np.nonzero(u * np.arange(1, len(v) + 1) > (css - 1))[0][-1]
    return np.maximum(v - (css[rho] - 1) / (rho + 1), 0)


mu, achieved = calibrate(np.array([0.95, 0.03, 0.02]))
print(f'  calibrated means {mu.round(4)} give E[D_k/sum D] = {achieved.round(4)} (target 0.95, 0.03, 0.02)')


def learn(r, mu, n_draws, gamma0=0.02, tau=300):
    """Projected stochastic gradient ascent on E[sum min(r_k V, D_k)] with decreasing steps; returns the average key."""
    D = draw_D(mu, n_draws)
    V = np.exp(rng_s.normal(-0.02, 0.2, n_draws)) * mu.sum()           # independent of D, E[V] ~ sum E[D]
    acc = np.zeros(K)
    for i, (d, v) in enumerate(zip(D, V)):
        g = v * (r * v < d) / mu.sum()                                   # stochastic gradient, scaled by order size
        r = project_simplex(r + gamma0 / (1 + i / tau) * (g - g.mean()))
        if i >= n_draws // 2:
            acc += r
    return r, acc / (n_draws - n_draws // 2)


def optimum(mu, n=100_000):
    """Exact KKT solution on a sample: each r_k solves h_k(r_k) = E[V 1{r_k V < D_k}] = lam (h_k decreasing in r_k),
    r_k = 0 if h_k(0) <= lam, and lam is set by bisection so that the keys sum to one."""
    D = draw_D(mu, n); V = np.exp(rng_s.normal(-0.02, 0.2, n)) * mu.sum()
    ratio = D / V[:, None]                                               # r_k V < D_k  <=>  r_k < D_k / V

    def key(k, lam):
        order = np.argsort(ratio[:, k]); rk = ratio[order, k]; vk = V[order]
        tail = np.cumsum(vk[::-1])[::-1] / n                             # h_k just below each breakpoint
        idx = np.searchsorted(-tail, -lam, side='right')                # first breakpoint where h_k <= lam
        return 0.0 if idx == 0 else rk[min(idx, n) - 1]

    lo, hi = 0.0, V.mean()
    for _ in range(80):
        lam = (lo + hi) / 2
        tot = sum(key(k, lam) for k in range(K))
        lo, hi = (lam, hi) if tot > 1 else (lo, lam)
    r = np.array([key(k, lam) for k in range(K)]); r = r / r.sum()
    g = (V[:, None] * (r * V[:, None] < D)).mean(0)
    return r, g, np.minimum(r * V[:, None], D).sum(1).mean(), lam


p_share, r, a_sor = np.array([0.95, 0.03, 0.02]), np.full(K, 1 / K), 0.3
for period in range(60):
    mu, _ = calibrate(p_share, iters=25, size=8_000)
    r, r_avg = learn(r, mu, 3000)
    p_share = (1 - a_sor) * p_share + a_sor * r_avg
r_opt, g_opt, c_opt, lam = optimum(mu)
print(f'  illustrative coupled run, 60 periods (a = 0.3, nu = {nu}): shares {p_share.round(3)}, averaged keys {r_avg.round(3)}')
print(f'  exact KKT optimum at the final liquidity: keys {r_opt.round(5)}, E[V 1(rV<D)] {g_opt.round(4)}, lambda {lam:.4f}'
      ' (all keys positive and the marginal values equal: an interior solution)')
assert np.all(r_opt > 0) and np.ptp(g_opt) < 0.01 * lam + 1e-3
print(f'  the learner averaged keys {r_avg.round(4)} against the exact optimum {r_opt.round(4)}')
assert np.abs(r_avg - r_opt).max() < 0.01
r_mid, g_mid, c_mid, lam_mid = optimum(np.array([0.6, 0.25, 0.15]))
print(f'  same solver with liquidity means (0.6, 0.25, 0.15): keys {r_mid.round(3)}, E[V 1(rV<D)] {g_mid.round(4)}')
assert np.ptp(g_mid[r_mid > 0]) < 0.01 * lam_mid + 1e-3
print('  with D_k = mu_k X_k, X_k i.i.d. and V independent, the optimal keys are mu_k / sum mu (scale invariance), and the'
      ' constraint E[D_k/sum D] = p_k makes mu_1/sum mu > p_1 for the largest venue, so p drifts towards it: this variant'
      ' concentrates and does not reproduce Lehalle-Laruelle\'s 50/25/25 path (their nu is unreported and their update'
      ' as printed differs)')

# ------------------------------------------------------------------ cross-venue no-arbitrage bound (derived)
head('cross-venue bound: a buy at ask a1 and a sale at bid b2 earn b2 - a1 - k per unit')
for a1, b2, k in [(100.00, 100.05, 0.02), (100.00, 100.01, 0.02)]:
    print(f'  a1={a1}, b2={b2}, all-in cost k={k}: profit per unit {b2 - a1 - k:+.2f} -> {"arbitrage" if b2 - a1 > k else "none"}')
