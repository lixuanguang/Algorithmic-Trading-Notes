"""Batch of 17 October 2026: own simulation behind meth:portfolio-covariance-estimation.

Ledoit and Wolf's review (UZH WP 323, version of February 2020, eqs. (2.4)-(2.7), pp. 5-6) gives the oracle linear
shrinkage Sigma* = gamma* mu I + (1 - gamma*) S, gamma* = beta^2 / delta^2, mu = <Sigma, I>, with the scaled Frobenius
norm ||A||^2 = Tr(A'A)/N, beta^2 = E||S - Sigma||^2, delta^2 = E||S - mu I||^2 = alpha^2 + beta^2. Checked here, with
the population known (so the oracle is computable): N = 100 assets, T = 120 i.i.d. normal observations, a true
covariance with a one-factor structure. (1) the identity alpha^2 + beta^2 = delta^2 holds by simulation; (2) the
oracle has lower Frobenius loss than S; (3) the global minimum-variance portfolio built from Sigma* has a lower true
variance than the one built from S. Synthetic data only; the feasible estimator of the paper is not reproduced.
Run: python3 batch50-shrinkage-check.py   (numpy; about 5 s). Exits non-zero on failure.
"""
import sys

import numpy as np

rng = np.random.default_rng(2020)
N, T, R = 100, 120, 300
beta = rng.normal(1.0, 0.3, N)
Sigma = 0.04 * np.outer(beta, beta) + np.diag(rng.uniform(0.01, 0.09, N))
L = np.linalg.cholesky(Sigma)
frob = lambda A: np.trace(A.T @ A) / N
mu = np.trace(Sigma) / N
I = np.eye(N)
alpha2 = frob(Sigma - mu * I)
Ss = []
for _ in range(R):
    X = rng.standard_normal((T, N)) @ L.T
    Ss.append(X.T @ X / T)  # mean-zero data, as in the paper's Section 2
beta2 = np.mean([frob(S - Sigma) for S in Ss])
delta2 = np.mean([frob(S - mu * I) for S in Ss])
g = beta2 / delta2
loss_S = beta2
loss_star = np.mean([frob(g * mu * I + (1 - g) * S - Sigma) for S in Ss])


def gmv_var(C):
    w = np.linalg.solve(C, np.ones(N))
    w /= w.sum()
    return w @ Sigma @ w


v_S = np.mean([gmv_var(S) for S in Ss])
v_star = np.mean([gmv_var(g * mu * I + (1 - g) * S) for S in Ss])
v_true = gmv_var(Sigma)
print(f'alpha^2 + beta^2 = {alpha2 + beta2:.6f}, delta^2 = {delta2:.6f}; oracle intensity gamma* = {g:.3f}')
print(f'Frobenius loss: sample {loss_S:.6f}, oracle shrinkage {loss_star:.6f}')
print(f'true variance of GMV portfolio: from S {v_S:.6f}, from Sigma* {v_star:.6f}, true optimum {v_true:.6f}')
fails = []
if abs(alpha2 + beta2 - delta2) > 0.02 * delta2:
    fails.append('identity')
if not loss_star < loss_S:
    fails.append('Frobenius')
if not v_star < v_S:
    fails.append('GMV variance')
for f in fails:
    print('BAD', f)
if fails:
    sys.exit(1)
print('all checks passed')
