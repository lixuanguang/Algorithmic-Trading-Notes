"""order books and order flow review (2026-10-16): independent checks for the order-book, order-flow and point-process entries.

Each block recomputes a claim from first principles or gives a counterexample; nothing here is fitted to real data.
Run: python3 order-flow-checks.py   (numpy, scipy; fixed seeds; about 20 s)
"""
from decimal import Decimal

import numpy as np
from scipy import integrate, stats

rng = np.random.default_rng(33)


def head(t):
    print('\n== ' + t)


# ------------------------------------------------------------------ Harris model: tick counterfactual units
head('Harris discretised spread: E(Psi | delta) = sum_k (k/delta) f_delta(k), k in new ticks (Lehalle-Laruelle app. A.6)')
shape = 4.0


def latent_pdf(x, mean):                       # latent continuous spread in OLD ticks, gamma with the given mean
    return stats.gamma.pdf(x, a=shape, scale=mean / shape)


def expected_discrete(mean, delta, kmax=400):
    """Expected observed spread in OLD ticks after rounding on a grid of old_tick/delta."""
    tot = 0.0
    p1 = integrate.quad(latent_pdf, 0, 1.5 / delta, args=(mean,))[0]
    tot += (1 / delta) * p1
    for k in range(2, kmax):
        pk = integrate.quad(latent_pdf, (k - 0.5) / delta, (k + 0.5) / delta, args=(mean,))[0]
        tot += (k / delta) * pk
        if (k - 0.5) / delta > mean * 10:
            break
    return tot


for mean in [0.6, 1.2, 3.0, 8.0]:
    e1, e5 = expected_discrete(mean, 1), expected_discrete(mean, 5)
    print(f'latent mean {mean:4.1f} old ticks: E(Psi|delta=1) = {e1:.3f}, E(Psi|delta=5) = {e5:.3f} old ticks,'
          f' change {e5 - e1:+.3f} ({(e5 - e1) / e1:+.1%})')
print('units: an observed spread of k old ticks is k*delta NEW ticks (3 old ticks = 15 new ticks at delta = 5);'
      ' it is a count of k NEW ticks that equals k/delta old ticks. The legacy "k-tick spread becomes k/delta old-tick units" mixes the two.')
print('the counterfactual re-rounds the latent spread on the finer grid; it does not rescale observed spreads:'
      f' mean 8.0 changes by {expected_discrete(8.0, 5) - expected_discrete(8.0, 1):+.3f} old ticks, not 8.0/5 - 8.0 = {8 / 5 - 8:+.1f}')


# ------------------------------------------------------------------ queue imbalance: two normalisations
head('queue imbalance: QI = (B - A)/(B + A) = 2I - 1 with I = B/(B + A) (Bouchaud et al. eq. 7.1)')
B, A = rng.integers(1, 500, 5), rng.integers(1, 500, 5)
I = B / (B + A)
QI = (B - A) / (B + A)
print('max |QI - (2I - 1)| =', float(np.abs(QI - (2 * I - 1)).max()), '; I in (0,1), QI in (-1,1); both scale-invariant:',
      bool(np.allclose((3 * B - 3 * A) / (3 * B + 3 * A), QI)))


# ------------------------------------------------------------------ OFI (Cont-Kukanov-Stoikov) against trade imbalance
head('event-based order-flow imbalance e_n (Cont, Kukanov and Stoikov, p. 4) against signed trade volume')


def e_n(prev, cur):
    pb0, qb0, pa0, qa0 = prev
    pb1, qb1, pa1, qa1 = cur
    return ((pb1 >= pb0) * qb1 - (pb1 <= pb0) * qb0 - (pa1 <= pa0) * qa1 + (pa1 >= pa0) * qa0)


# best-quote states (bid price, bid size, ask price, ask size) and any trade (signed volume) between them
seq = [((10.00, 500, 10.01, 400), 0),
       ((10.00, 300, 10.01, 400), -200),      # market sell of 200 hits the bid
       ((10.00, 500, 10.01, 400), 0),         # 200 replenished at the bid
       ((10.00, 500, 10.01, 100), 0),         # 300 cancelled at the ask (no trade)
       ((10.00, 500, 10.02, 600), +100),      # market buy of 100 empties the ask; new ask level 10.02 with 600
       ]
ofi, ti = 0.0, 0.0
for (prev, _), (cur, tr) in zip(seq[:-1], seq[1:]):
    e = e_n(prev, cur)
    ofi += e
    ti += tr
    print(f'  {prev} -> {cur}: e_n = {e:+5.0f}, signed trade = {tr:+5d}')
print(f'OFI = {ofi:+.0f}, trade imbalance = {ti:+.0f}: the cancellation at the ask (+300) and the replenished bid (+200) move OFI'
      ' but not the trade imbalance; the two measures can even differ in sign')


# ------------------------------------------------------------------ trade signing
head('trade signing: quote rule, then tick rule at the midpoint (Lee-Ready as described by Harris and Hasbrouck)')


def tick_sign(prices):
    """Sign of the last non-zero price change before the current trade (0 if none): the tick test, zero ticks skipped."""
    for k in range(len(prices) - 1, 0, -1):
        d = prices[k] - prices[k - 1]
        if d != 0:
            return 1 if d > 0 else -1
    return 0


def lee_ready(price, bid, ask, prior_prices):
    """Quote rule against the midpoint, tick test (last non-zero change) for trades exactly at the midpoint.
    Prices are Decimal values built from strings, so a half-tick midpoint such as 10.005 compares exactly."""
    mid = (bid + ask) / 2
    if price > mid:
        return +1
    if price < mid:
        return -1
    return tick_sign(list(prior_prices) + [price])


D = Decimal
cases = [  # (trade, bid, ask, earlier trade prices, expected sign, what it tests)
    (D('10.005'), D('10.00'), D('10.01'), [D('10.00')], +1, 'half-tick midpoint after an uptick'),
    (D('10.005'), D('10.00'), D('10.01'), [D('10.01')], -1, 'half-tick midpoint after a downtick'),
    (D('10.01'), D('10.00'), D('10.02'), [D('10.02')], -1, 'whole-tick midpoint after a downtick'),
    (D('10.01'), D('10.00'), D('10.02'), [D('10.00'), D('10.01')], +1, 'midpoint, zero tick, last non-zero change up (zero uptick)'),
    (D('10.01'), D('10.00'), D('10.02'), [D('10.02'), D('10.01')], -1, 'midpoint, zero tick, last non-zero change down (zero downtick)'),
    (D('10.01'), D('10.00'), D('10.02'), [D('10.01')], 0, 'midpoint, no earlier non-zero change: unclassified'),
    (D('10.006'), D('10.00'), D('10.01'), [D('10.01')], +1, 'just above a half-tick midpoint, after a downtick'),
    (D('10.004'), D('10.00'), D('10.01'), [D('10.00')], -1, 'just below a half-tick midpoint, after an uptick'),
    (D('10.00'), D('10.00'), D('10.02'), [D('9.98')], -1, 'at the bid after an uptick'),
    (D('10.02'), D('10.00'), D('10.02'), [D('10.04')], +1, 'at the ask after a downtick'),
]
for p, b, a, prior, want, what in cases:
    got = lee_ready(p, b, a, prior)
    assert got == want, (what, got, want)
    print(f'  {what:62}: trade {p} in [{b}, {a}] after {[str(x) for x in prior]} -> {got:+d}')
print('all', len(cases), 'assertions hold')
print('binary floating point: (10.00 + 10.01)/2 =', repr((10.00 + 10.01) / 2), '< 10.005 ->',
      'a float implementation calls the downtick midpoint case a buy;', 'Decimal gives', (D('10.00') + D('10.01')) / 2)
print('a trade at the bid is a sell under the quote rule whatever the previous tick; a passive buyer who pegs the bid'
      ' is never classified as the buyer (Harris, p. 423)')


# ------------------------------------------------------------------ signature plot and microstructure noise
head('realised variance with i.i.d. noise: E[RV(Delta)] = IV + 2 n sigma_eta^2, n = T/Delta (Lehalle-Laruelle app. A.13 model)')
T, N = 1.0, 23_400
sigma, s_eta = 0.01, 0.0002
dW = rng.standard_normal(N) * sigma * np.sqrt(T / N)
M = np.concatenate([[0.0], np.cumsum(dW)])
X = M + rng.standard_normal(N + 1) * s_eta
for step in [1, 5, 30, 300, 1800]:
    rv = np.sum(np.diff(X[::step]) ** 2)
    n = N // step
    print(f'  step {step:5d} ({n:5d} returns): RV = {rv:.3e}, IV + 2 n s_eta^2 = {sigma ** 2 + 2 * n * s_eta ** 2:.3e}')

head('jumps: realised variance converges to quadratic variation, not to the integrated diffusion variance')
rng_j = np.random.default_rng(35)
lam_j, Tj = 5.0, 1.0
jt = np.sort(rng_j.uniform(0, Tj, rng_j.poisson(lam_j * Tj)))     # unit-jump Poisson path: sigma = 0
for n_steps in [10, 100, 10_000, 1_000_000]:
    grid = np.linspace(0, Tj, n_steps + 1)
    Ng = np.searchsorted(jt, grid, side='right')                     # N at grid times
    print(f'  {n_steps:9d} steps: RV = {np.sum(np.diff(Ng) ** 2):3d}; jump count N_T = {len(jt)}; integrated diffusion variance 0')
co = np.sort(rng_j.uniform(0, 1, 3))
X1 = lambda t: np.searchsorted(co, t, side='right') * 1.0               # three common jumps of +1 ...
X2 = lambda t: -np.searchsorted(co, t, side='right') * 0.5             # ... and -0.5 in the second asset
g = np.linspace(0, 1, 100_001)
print('  co-jumps: realised covariance', float(np.sum(np.diff(X1(g)) * np.diff(X2(g)))), '= sum of jump products 3 x (1)(-0.5)')


head('Epps effect from asynchronous observation alone: true correlation 0.6, previous-tick sampling of Poisson trade times')
rho, N, reps = 0.6, 23_400, 40


def prev_tick(P, obs, grid):
    idx = np.searchsorted(obs, grid, side='right') - 1
    return P[obs[np.clip(idx, 0, len(obs) - 1)]]


steps = [5, 30, 120, 600, 1800]
corr = {s: [] for s in steps}
for _ in range(reps):
    z1, z2 = rng.standard_normal(N), rng.standard_normal(N)
    P1 = np.cumsum(z1)
    P2 = np.cumsum(rho * z1 + np.sqrt(1 - rho ** 2) * z2)
    obs1 = np.sort(rng.choice(N, 2000, replace=False))   # about one trade every 12 time units
    obs2 = np.sort(rng.choice(N, 2000, replace=False))
    for step in steps:
        grid = np.arange(max(obs1[0], obs2[0]), N, step)
        r1, r2 = np.diff(prev_tick(P1, obs1, grid)), np.diff(prev_tick(P2, obs2, grid))
        corr[step].append(np.corrcoef(r1, r2)[0, 1])
for step in steps:
    print(f'  step {step:5d}: mean sample correlation over {reps} paths {np.mean(corr[step]):.3f} (sd {np.std(corr[step]):.3f})')


# ------------------------------------------------------------------ deseasonalisation
head('multiplicative deseasonalisation with a centred moving average of length p (Lehalle-Laruelle app. A.11)')
p, n = 13, 60                                          # 13 slots a day, 60 days
S_true = 1 + 0.6 * np.cos(np.linspace(0, 2 * np.pi, p, endpoint=False)) ** 2
S_true /= S_true.mean()
trend = np.linspace(100, 140, p * n)
X = trend * np.tile(S_true, n) + rng.standard_normal(p * n) * 2.0
k = p // 2
MA = np.full(X.size, np.nan)
for t in range(k, X.size - k):
    MA[t] = X[t - k:t + k + 1].mean()                  # odd length 2k+1 = p
ratio = (X / MA).reshape(n, p)
S_hat = np.nanmean(ratio, axis=0)
S_hat /= S_hat.mean()
print('max |S_hat - S| =', round(float(np.abs(S_hat - S_true).max()), 4))
X2 = X.copy()
X2[200 + 3] += 50.0                                    # a later observation changes
MA2 = np.array([X2[t - k:t + k + 1].mean() if k <= t < X.size - k else np.nan for t in range(X.size)])
print('a shock at t = 203 changes the centred MA at t = 197..202 (before it):', bool(np.all(MA2[197:203] != MA[197:203])),
      '-> a two-sided trend estimate is not available at decision time; the last k values are undefined')


# ------------------------------------------------------------------ point processes and Hawkes
head('homogeneous Poisson: exponential durations; time change of a Hawkes compensator to unit-rate Poisson')


def sim_hawkes_exp(mu, alpha, beta, T, rng):
    """Ogata thinning for lambda(t) = mu + sum alpha * exp(-beta (t - t_i)); alpha/beta is the branching ratio."""
    t, ev, excite = 0.0, [], 0.0
    while True:
        lam_bar = mu + excite
        w = rng.exponential(1 / lam_bar)
        t_new = t + w
        excite *= np.exp(-beta * w)
        if t_new > T:
            return np.array(ev)
        if rng.uniform() * lam_bar <= mu + excite:
            ev.append(t_new)
            excite += alpha
        t = t_new


mu, alpha, beta, T = 1.0, 0.6, 1.0, 20_000.0
ev = sim_hawkes_exp(mu, alpha, beta, T, rng)
print(f'exponential kernel, branching ratio alpha/beta = {alpha / beta}: mean rate {len(ev) / T:.3f}'
      f' against mu/(1 - alpha/beta) = {mu / (1 - alpha / beta):.3f}')
counts = np.histogram(ev, bins=np.arange(0, T + 1, 50.0))[0]
print(f'clustering ratio Var/E of counts in windows of 50: {counts.var() / counts.mean():.2f}'
      f' (Poisson 1; Hawkes long-window limit 1/(1-g)^2 = {1 / (1 - alpha / beta) ** 2:.2f})')
# compensator between events
Lam = []
excite_at = 0.0
for i in range(1, len(ev)):
    dt = ev[i] - ev[i - 1]
    excite_after = excite_at + alpha                   # just after event i-1
    Lam.append(mu * dt + excite_after / beta * (1 - np.exp(-beta * dt)))
    excite_at = excite_after * np.exp(-beta * dt)
Lam = np.array(Lam)
print(f'time-rescaled durations: mean {Lam.mean():.3f}, KS p-value against Exp(1) {stats.kstest(Lam, "expon").pvalue:.2f};'
      f' raw durations against Exp(mean): p = {stats.kstest(np.diff(ev) / np.diff(ev).mean(), "expon").pvalue:.1e}')

head('inhibition: a negative kernel in a linear Hawkes intensity can go negative; a non-negative link keeps it valid')
mu, a_neg, beta = 0.5, -0.8, 2.0
lin = mu + a_neg * np.exp(-beta * 0.0)
print(f'linear intensity just after one event: mu + a = {lin:+.2f} < 0 (not an intensity)')


def sim_nonlinear(mu, a, beta, T, rng):
    """lambda = (mu + sum a exp(-beta (t - t_i)))^+ ; thinning with bound mu (valid because a < 0)."""
    t, ev, ex = 0.0, [], 0.0
    while True:
        w = rng.exponential(1 / mu)
        t += w
        ex *= np.exp(-beta * w)
        if t > T:
            return np.array(ev)
        if rng.uniform() * mu <= max(mu + ex, 0.0):
            ev.append(t)
            ex += a


ev_in = sim_nonlinear(mu, a_neg, beta, 20_000.0, rng)
c = np.histogram(ev_in, bins=np.arange(0, 20_001, 50.0))[0]
print(f'(.)^+ link: rate {len(ev_in) / 20_000:.3f} < mu = {mu}; clustering ratio {c.var() / c.mean():.2f} < 1 (events repel)')

head('queue arrival/departure ratio: birth-death queue with insertion rate L and departure rate D (cancellations plus trades)')
for L, D in [(1.2, 1.0), (0.8, 1.0)]:
    q, path = 20, []
    for _ in range(20_000):
        if q == 0:
            q = 1
        q += 1 if rng.uniform() < L / (L + D) else -1
        path.append(q)
    print(f'  A/D ratio {L / D:.1f}: queue after 20,000 events {path[-1]}, mean drift per event {(L - D) / (L + D):+.3f}')
print('the drift sign follows the ratio only when both rates are constant in the queue size; with state-dependent rates'
      ' (Huang-Lehalle-Rosenbaum) the ratio must be read at each size')

head('waiting-time estimator of 1/lambda depends on where the clock starts (Lehalle-Laruelle p. 221, n. 12)')
starts_uniform = rng.uniform(0, ev[-1], 5000)
idx = np.searchsorted(ev, starts_uniform)
ok = idx < len(ev)
wait_uniform = (ev[idx[ok]] - starts_uniform[ok]).mean()
wait_after_event = np.diff(ev).mean()
print(f'Hawkes sample: mean wait from uniform start times {wait_uniform:.3f}, mean inter-event time {wait_after_event:.3f}')
print('renewal theory: for an equilibrium renewal process with finite E[X^2], the mean wait from an arbitrary time is'
      ' E[X^2]/(2 E[X]); it equals E[X] iff E[X^2] = 2 E[X]^2, i.e. CV = 1, which does not imply exponential gaps')
xs, ps = np.array([0.5, 3.0]), np.array([0.8, 0.2])
EX, EX2 = float((xs * ps).sum()), float((xs ** 2 * ps).sum())
assert abs(EX - 1) < 1e-12 and abs(EX2 - 2) < 1e-12
print(f'two-point gaps P(X=0.5)=0.8, P(X=3)=0.2: E[X] = {EX}, E[X^2] = {EX2}, CV = {np.sqrt(EX2 - EX ** 2) / EX:.3f},'
      f' E[X^2]/(2E[X]) = {EX2 / (2 * EX)}')
rng2 = np.random.default_rng(34)
gaps = rng2.choice(xs, size=400_000, p=ps)
times = np.cumsum(gaps)
st = rng2.uniform(times[1000], times[-1000], 200_000)
w = times[np.searchsorted(times, st)] - st
print(f'simulated: mean wait from uniform times {w.mean():.4f} against mean gap {gaps.mean():.4f}; equal although not Poisson')
g_exp = rng2.exponential(1.0, 400_000); t_exp = np.cumsum(g_exp)
st = rng2.uniform(t_exp[1000], t_exp[-1000], 200_000)
print(f'exponential gaps (mean 1): mean wait {(t_exp[np.searchsorted(t_exp, st)] - st).mean():.4f}')
hg = np.diff(ev)
print(f'Hawkes gaps: CV = {hg.std() / hg.mean():.3f}; E[X^2]/(2E[X]) = {(hg ** 2).mean() / (2 * hg.mean()):.3f}'
      f' against the mean wait {wait_uniform:.3f} from uniform start times (the stationary inversion formula, Palm moments)')
