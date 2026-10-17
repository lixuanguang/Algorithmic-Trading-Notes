"""source verification (2026-10-17): an own synthetic check behind meth:backtest-evaluation-diagnostics (drawdowns).

Claim checked: shuffling single returns (Narang's remedy) destroys the serial dependence that drives drawdown depth,
so with positively autocorrelated returns it understates drawdown risk, while resampling blocks of random
(geometric) length keeps short-range dependence. This is an illustration on an AR(1) model chosen here, not a
reading: Politis and Romano's stationary bootstrap paper was not obtained, and the resampler below is the commonly
described form (block starts uniform, lengths geometric with mean L, wrapping around the sample).
Design: monthly returns r_t = 0.005 + 0.3 (r_{t-1} - 0.005) + e_t, e_t ~ N(0, 0.04^2), T = 120. The model's own
distribution of the maximum drawdown is the reference; for 200 independent sample paths each method's bootstrap
95th percentile is compared with the reference 95th percentile.
Run: python3 drawdown-resampling-checks.py   (numpy; about 10 s). Exits non-zero on failure.
"""
import sys

import numpy as np

rng = np.random.default_rng(1710)
T, phi, mu, sd = 120, 0.3, 0.005, 0.04


def ar1(n_paths):
    e = rng.normal(0, sd, (n_paths, T + 50))
    r = np.empty_like(e)
    r[:, 0] = mu + e[:, 0]
    for t in range(1, T + 50):
        r[:, t] = mu + phi * (r[:, t - 1] - mu) + e[:, t]
    return r[:, 50:]


def max_dd(r):
    w = np.cumsum(np.log1p(r), axis=-1)
    peak = np.maximum.accumulate(np.concatenate([np.zeros(w.shape[:-1] + (1,)), w], axis=-1), axis=-1)[..., 1:]
    return np.max(peak - w, axis=-1)


def shuffle_boot(x, B):
    return np.array([rng.permutation(x) for _ in range(B)])


def stationary_boot(x, B, L=12):
    n = len(x)
    out = np.empty((B, n))
    for b in range(B):
        i, k = rng.integers(n), 0
        while k < n:
            out[b, k] = x[i % n]
            k += 1
            i = rng.integers(n) if rng.random() < 1 / L else i + 1
    return out


ref = np.quantile(max_dd(ar1(20000)), 0.95)
q_sh, q_st = [], []
for _ in range(200):
    x = ar1(1)[0]
    q_sh.append(np.quantile(max_dd(shuffle_boot(x, 400)), 0.95))
    q_st.append(np.quantile(max_dd(stationary_boot(x, 400)), 0.95))
q_sh, q_st = np.median(q_sh), np.median(q_st)
print(f'reference 95th percentile of max drawdown (log units): {ref:.3f}')
print(f'median bootstrap 95th percentile: shuffle {q_sh:.3f}, stationary-type blocks (L=12) {q_st:.3f}')
fails = []
if not q_sh < 0.85 * ref:
    fails.append('shuffle does not understate')
if not abs(q_st - ref) < abs(q_sh - ref):
    fails.append('blocks not closer than shuffle')
for f in fails:
    print('BAD', f)
if fails:
    sys.exit(1)
print('ok  shuffling understates the drawdown tail under positive autocorrelation; blocks come closer\nall checks passed')
