"""Slice 34 (2026-10-16): independent checks for the order-instruction, matching, dark-trading and fragmentation entries.

Each block recomputes a source's example or a derived claim from first principles, or gives a counterexample.
Run: /opt/homebrew/bin/python3.10 slice34-checks.py   (numpy, scipy; fixed seeds; a few seconds)
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

# ------------------------------------------------------------------ pro-rata allocation and rounding
head('pro-rata allocation: exact shares and what rounding leaves over')
print('Harris (p. 117): 18 against resting 10 and 20 ->', [Fr(18 * q, 30) for q in (10, 20)])
print('POSIT example (p. 134): sell 3,000 against buys 5,000 and 10,000 ->', [3000 * q // 15000 for q in (5000, 10000)])
Q, rest = 10, [3, 3, 3]
exact = [Fr(Q * q, sum(rest)) for q in rest]
floors = [int(x) for x in exact]
print(f'Q={Q} against {rest}: exact {[str(x) for x in exact]}, floors {floors}, remainder {Q - sum(floors)}'
      ' to be allocated by a venue rule (time, largest fraction, or another); the rule changes who fills')
Q, rest = 7, [1, 1, 100]
exact = [Fr(Q * q, sum(rest)) for q in rest]
print(f'Q={Q} against {rest}: exact {[f"{float(x):.3f}" for x in exact]}, floors {[int(x) for x in exact]}:'
      ' small orders receive nothing without a minimum or remainder rule')

# ------------------------------------------------------------------ market versus limit threshold (derived)
head('posting against crossing: expected relative gain p(S-A) - (1-p)M (derived; legacy proposition)')
for p, S, A, M in [(0.6, 1.0, 0.3, 0.8), (0.6, 1.0, 0.7, 0.8), (0.9, 1.0, 0.3, 2.0)]:
    g = p * (S - A) - (1 - p) * M
    print(f'  p={p}, S={S}, A={A}, M={M}: gain {g:+.2f} -> {"post" if g > 0 else "cross"}')

# ------------------------------------------------------------------ fragmentation metrics
head("ex-fixing market share (Lehalle-Laruelle p. 35): derived (M - m p)/(1 - p) against the printed (1 - m p) M/(1 - p)")
for M_, m_, p_ in [(0.60, 1.0, 0.20), (0.30, 0.0, 0.20), (0.70, 1.0, 0.25)]:
    total, fix_total = 1.0, p_
    venue_total = M_ * total
    venue_fix = m_ * fix_total
    exact = (venue_total - venue_fix) / (total - fix_total)
    printed = (1 - m_ * p_) * M_ / (1 - p_)
    print(f'  M={M_}, m={m_}, p={p_}: ex-fixing share {exact:.4f}; printed formula {printed:.4f}')
print('  (a venue with all the auctions and 60 percent overall has 50 percent of continuous trading, not 60)')

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

# ------------------------------------------------------------------ market-share estimator and its variance
head('venue-share estimator (app. A.8): Bernoulli variance holds only for independent equal-size trades')
p_true, n_tr = 0.3, 2000
iid = rng.binomial(1, p_true, (4000, n_tr)).mean(1)
print(f'  independent trades: sd {iid.std():.4f} against sqrt(p(1-p)/n) {np.sqrt(p_true * (1 - p_true) / n_tr):.4f}')
runs = []
for _ in range(4000):                       # venue choice persists in runs of 20 trades (one child order split...)
    v = rng.binomial(1, p_true, n_tr // 20).repeat(20)
    runs.append(v.mean())
print(f'  venue choice repeated in runs of 20 trades: sd {np.std(runs):.4f}; the binomial interval is too narrow')

# ------------------------------------------------------------------ SOR toy model (app. A.3)
head('SOR toy model (app. A.3): learning rule, market-share update, and the first-order condition')
K, a_sor, gamma = 3, 0.3, 0.002
p_share = np.array([0.95, 0.03, 0.02])
r = np.full(K, 1 / K)
nu = 0.8                                                  # sd proportional to mean liquidity (LL's assumption)
for period in range(400):
    for _ in range(50):
        D = p_share * np.exp(rng.normal(-nu ** 2 / 2, nu, K))     # mean p_k, lognormal
        V = D.sum() * np.exp(rng.normal(-0.02, 0.2))
        hit = (r * V < D).astype(float)                   # venue had more than was sent: allocation was too small
        r = r + gamma * (hit - hit.mean())                 # raise r_k where venue k had more than was sent; LL print
        #   gamma*(mean - hit) in eq. (A.7), which would lower it, against their own text (p. 256)
        r = np.clip(r, 1e-4, None); r /= r.sum()
    p_share = (1 - a_sor) * p_share + a_sor * r
print('  start shares (0.95, 0.03, 0.02), equal initial SOR keys; after 400 periods: shares', p_share.round(3), 'keys', r.round(3))
# first-order condition check with random V: E[V 1{r_k V < D_k}] equal across venues at the optimum
Ds = np.array([0.5, 0.3, 0.2]) * np.exp(rng.normal(-0.32, 0.8, (200_000, 3)))
Vs = Ds.sum(1) * np.exp(rng.normal(0, 0.6, 200_000))
best, bestr = -1, None
for r1 in np.linspace(0.05, 0.9, 86):
    for r2 in np.linspace(0.05, 0.9 - r1, max(2, int((0.9 - r1) / 0.01))):
        rr = np.array([r1, r2, 1 - r1 - r2])
        if rr[2] <= 0:
            continue
        c = np.minimum(rr * Vs[:, None], Ds).sum(1).mean()
        if c > best:
            best, bestr = c, rr
hitw = ((bestr * Vs[:, None] < Ds) * Vs[:, None]).mean(0)
hitu = (bestr * Vs[:, None] < Ds).mean(0)
print(f'  grid optimum r = {bestr.round(3)}: E[V 1(rV<D)] = {hitw.round(4)} (near-equal), E[1(rV<D)] = {hitu.round(4)}'
      ' (LL eq. A.6 drops the V weight; exact only for a fixed order size)')

# ------------------------------------------------------------------ cross-venue no-arbitrage bound (derived)
head('cross-venue bound: a buy at ask a1 and a sale at bid b2 earn b2 - a1 - k per unit')
for a1, b2, k in [(100.00, 100.05, 0.02), (100.00, 100.01, 0.02)]:
    print(f'  a1={a1}, b2={b2}, all-in cost k={k}: profit per unit {b2 - a1 - k:+.2f} -> {"arbitrage" if b2 - a1 > k else "none"}')
