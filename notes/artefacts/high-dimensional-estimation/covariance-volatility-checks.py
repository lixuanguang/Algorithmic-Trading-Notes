"""derivatives and empirical validation (2026-10-17): own checks behind the covariance, noise and volatility-loss passages.

1. Ledoit and Wolf, "Honey, I Shrunk the Sample Covariance Matrix" (2003 manuscript, App. A-B, eqs. (3)-(5)): target F
   with the sample variances and the average sample correlation r-bar; intensity delta* = max(0, min(kappa/T, 1)),
   kappa = (pi - rho)/gamma, estimated as printed. Check: with N close to T the shrunk matrix has lower Frobenius
   loss than the sample matrix; delta* goes to 1 when the population is constant-correlation (the target is right) and
   lies inside (0, 1) when it is not; the shrunk matrix is invertible when N > T.
2. Laloux et al. (arXiv cond-mat/9810255, eq. (3)): for a T x N matrix of independent unit-variance noise, the
   correlation eigenvalues lie in [(1 - Q^-1/2)^2, (1 + Q^-1/2)^2], Q = T/N. Check by simulation at the paper's
   N = 406, T = 1309 (Q = 3.22); and the paper's sigma^2 = 0.85 equals 1 - lambda_1/N with lambda_1 = 25 lambda_max,
   i.e. the "lambda_max" in "sigma^2 = 1 - lambda_max/N" must be the largest eigenvalue lambda_1 (own reading).
3. Patton (QFRC RP 175, eqs. (5)-(6), (10); Props. 2-3): with a conditionally unbiased but noisy proxy (squared
   return, sigma^2 chi^2_1), MSE and QLIKE rank the true variance first; MAE prefers a forecast near the proxy's
   conditional median (0.455 sigma^2), so it misranks.
4. Corsi (2009, eqs. (4)-(8)): HAR-RV is an AR(22) with coefficients constrained to three steps
   (b_d + b_w/5 + b_m/22 at lag 1, b_w/5 + b_m/22 at lags 2-5, b_m/22 at lags 6-22). Check the mapping numerically.
Run: python3 covariance-volatility-checks.py   (numpy). Exits 1 on failure.
"""
import math
import sys

import numpy as np

rng = np.random.default_rng(20261017)
fails = []


def ok(name, cond, detail=''):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


def lw_constant_correlation(Y):
    T, N = Y.shape
    X = Y - Y.mean(0)
    S = X.T @ X / T
    s = np.sqrt(np.diag(S))
    R = S / np.outer(s, s)
    rbar = (R.sum() - N) / (N * (N - 1))
    F = rbar * np.outer(s, s)
    np.fill_diagonal(F, np.diag(S))
    Z = X[:, :, None] * X[:, None, :] - S                      # T x N x N
    pi_mat = (Z ** 2).mean(0)
    pi = pi_mat.sum()
    D = X ** 2 - np.diag(S)                                    # T x N
    th_ii = np.einsum('ti,tij->ij', D, Z) / T                  # theta_{ii,ij}
    th_jj = np.einsum('tj,tij->ij', D, Z) / T                  # theta_{jj,ij}
    off = (rbar / 2) * (np.sqrt(np.outer(1 / s ** 2, s ** 2)) * th_ii + np.sqrt(np.outer(s ** 2, 1 / s ** 2)) * th_jj)
    np.fill_diagonal(off, 0)
    rho = np.trace(pi_mat) + off.sum()
    gamma = ((F - S) ** 2).sum()
    delta = max(0.0, min((pi - rho) / gamma / T, 1.0))
    return delta * F + (1 - delta) * S, S, delta


print('== 1. Ledoit-Wolf constant-correlation shrinkage')
N, T = 50, 60
vols = rng.uniform(0.1, 0.4, N)
blocks = np.repeat(np.arange(5), 10)
Cb = np.where(blocks[:, None] == blocks[None, :], 0.6, 0.1) + 0.4 * np.eye(N)   # correlations not constant
for label, C in (('constant correlation 0.3', np.full((N, N), 0.3) + 0.7 * np.eye(N)), ('five blocks (0.6 within, 0.1 across)', Cb)):
    Sigma = np.outer(vols, vols) * C
    L = np.linalg.cholesky(Sigma)
    loss_s, loss_f, deltas = [], [], []
    for _ in range(200):
        Y = rng.standard_normal((T, N)) @ L.T
        Sh, S, d = lw_constant_correlation(Y)
        loss_s.append(((S - Sigma) ** 2).sum()); loss_f.append(((Sh - Sigma) ** 2).sum()); deltas.append(d)
    if label.startswith('constant'):
        ok(f'{label}: the target is correct, so the intensity goes to 1', np.median(deltas) > 0.9, f'median delta {np.median(deltas):.3f}')
    else:
        ok(f'{label}: intensity strictly inside (0, 1)', 0 < min(deltas) and max(deltas) < 1, f'median delta {np.median(deltas):.3f}')
    ok(f'{label}: shrinkage lowers mean Frobenius loss', np.mean(loss_f) < np.mean(loss_s), f'{np.mean(loss_f):.5f} vs {np.mean(loss_s):.5f}')
Y = rng.standard_normal((40, 60)) @ np.linalg.cholesky(np.outer(rng.uniform(.1, .4, 60), rng.uniform(.1, .4, 60)) * 0 + np.eye(60) * 0.04 + 0.01).T
Sh, S, d = lw_constant_correlation(Y)
ok('N > T: sample matrix singular, shrunk matrix invertible', np.linalg.matrix_rank(S) < 60 and np.linalg.eigvalsh(Sh).min() > 0,
   f'rank S {np.linalg.matrix_rank(S)}, min eig shrunk {np.linalg.eigvalsh(Sh).min():.2e}, delta {d:.3f}')

print('== 2. Marchenko-Pastur band (Laloux et al.)')
N, T = 406, 1309
Q = T / N
lmin, lmax = (1 - Q ** -0.5) ** 2, (1 + Q ** -0.5) ** 2
X = rng.standard_normal((T, N))
ev = np.linalg.eigvalsh(np.corrcoef(X, rowvar=False))
ok('pure-noise eigenvalues within the band (5% slack at the edges)', ev.min() > 0.95 * lmin and ev.max() < 1.05 * lmax,
   f'band [{lmin:.3f}, {lmax:.3f}], simulated [{ev.min():.3f}, {ev.max():.3f}]')
lam1 = 25 * lmax
ok("sigma^2 = 1 - lambda_1/N with lambda_1 = 25 lambda_max reproduces the paper's 0.85", abs((1 - lam1 / N) - 0.85) < 0.005,
   f'1 - {lam1:.1f}/406 = {1 - lam1 / N:.3f}; 1 - lambda_max/N would be {1 - lmax / N:.4f}')

print('== 3. Robust loss with a noisy variance proxy (Patton)')
n = 400000
sig2 = np.exp(rng.normal(0, 0.5, n))
proxy = sig2 * rng.standard_normal(n) ** 2
cands = {'true': sig2, 'x0.455 (median)': 0.455 * sig2, 'x0.8': 0.8 * sig2, 'x1.25': 1.25 * sig2}
losses = {'MSE': lambda p, h: (p - h) ** 2, 'QLIKE': lambda p, h: np.log(h) + p / h, 'MAE': lambda p, h: np.abs(p - h)}
for name, Lf in losses.items():
    m = {k: Lf(proxy, h).mean() for k, h in cands.items()}
    best = min(m, key=m.get)
    if name == 'MAE':
        ok('MAE prefers the median-scaled forecast, not the truth', best == 'x0.455 (median)', ', '.join(f'{k} {v:.4f}' for k, v in m.items()))
    else:
        ok(f'{name} ranks the true variance first', best == 'true', ', '.join(f'{k} {v:.4f}' for k, v in m.items()))

print('== 4. HAR-RV as a restricted AR(22) (Corsi)')
bd, bw, bm = 0.4, 0.3, 0.2
phi = np.array([bd + bw / 5 + bm / 22] + [bw / 5 + bm / 22] * 4 + [bm / 22] * 17)
rv = np.exp(rng.normal(0, 0.3, 200))
t = 150
har = bd * rv[t] + bw * rv[t - 4:t + 1].mean() + bm * rv[t - 21:t + 1].mean()
ar = phi @ rv[t::-1][:22]
ok('HAR forecast equals the AR(22) with step coefficients', abs(har - ar) < 1e-12, f'{har:.6f} vs {ar:.6f}; persistence {phi.sum():.2f}')

if fails:
    print('\nFAILED:', fails)
    sys.exit(1)
print('\nall checks passed')
