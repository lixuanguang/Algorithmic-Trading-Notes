"""Third batch of 17 October 2026: own check behind meth:equal-risk-contribution.

Maillard, Roncalli and Teiletche (authors' version of May 2009 of "The properties of equally weighted risk
contribution portfolios"): risk contributions sigma_i(x) = x_i (Sigma x)_i / sigma(x) sum to sigma(x) (sec. 2.1); the
long-only ERC portfolio equalises them (eqs. (1)-(2)); with a constant correlation it is the inverse-volatility
portfolio (eq. (3)); in general x_i is proportional to 1/beta_i (eq. (5)); and sigma_mv <= sigma_erc <= sigma_1/n
(sec. 3.4, appendix A.3). Checked on two covariance matrices (one constant-correlation, one not); the ERC weights are
found by a simple fixed-point iteration on y_i = 1/(Sigma y)_i (own algorithm, not the paper's SQP), and the
long-only minimum-variance portfolio by projected gradient descent.
Run: python3 batch60-erc-check.py   (numpy). Exits non-zero on failure.
"""
import sys

import numpy as np

fails = []


def ok(name, cond, detail=''):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


def erc(S, iters=20000):
    y = np.ones(len(S))
    for _ in range(iters):
        y = np.sqrt(y * (1 / (S @ y)))  # geometric step toward y_i (Sigma y)_i = 1
    return y / y.sum()


def minvar_long_only(S, iters=200000, lr=0.5):
    n = len(S); x = np.ones(n) / n
    for _ in range(iters):
        x = x - lr * (S @ x)
        # project onto the simplex
        u = np.sort(x)[::-1]; css = np.cumsum(u); rho = np.nonzero(u * np.arange(1, n + 1) > (css - 1))[0][-1]
        x = np.maximum(x - (css[rho] - 1) / (rho + 1), 0)
    return x


def rc(x, S):
    s = np.sqrt(x @ S @ x)
    return x * (S @ x) / s, s


vols = np.array([0.10, 0.20, 0.30, 0.15])
for label, C in (('constant correlation 0.3', np.full((4, 4), 0.3) + 0.7 * np.eye(4)),
                 ('unequal correlations', np.array([[1, 0.8, 0.1, 0.0], [0.8, 1, 0.2, 0.1], [0.1, 0.2, 1, -0.3], [0.0, 0.1, -0.3, 1.0]]))):
    print(f'== {label}')
    S = np.outer(vols, vols) * C
    x = erc(S)
    r, s = rc(x, S)
    ok('risk contributions sum to portfolio volatility', abs(r.sum() - s) < 1e-12, f'{r.sum():.6f} vs {s:.6f}')
    ok('ERC contributions equal', np.ptp(r) < 1e-10, ', '.join(f'{v:.5f}' for v in r))
    iv = (1 / vols) / (1 / vols).sum()
    beta = (S @ x) / (x @ S @ x)
    ok('x_i = (1/beta_i)/n (eq. (5))', np.allclose(x, 1 / beta / len(x), atol=1e-10))
    same = np.allclose(x, iv, atol=1e-8)
    if label.startswith('constant'):
        ok('constant correlation: ERC equals inverse volatility (eq. (3))', same, ', '.join(f'{v:.4f}' for v in x))
    else:
        ok('unequal correlations: ERC differs from inverse volatility', not same,
           'ERC ' + ', '.join(f'{v:.4f}' for v in x) + ' | 1/vol ' + ', '.join(f'{v:.4f}' for v in iv))
        r_iv, _ = rc(iv, S)
        print('     inverse-volatility risk shares: ' + ', '.join(f'{v / r_iv.sum() * 100:.1f}%' for v in r_iv))
    mv = minvar_long_only(S)
    s_mv, s_erc, s_eq = np.sqrt(mv @ S @ mv), s, np.sqrt(np.ones(4) @ S @ np.ones(4)) / 4
    ok('sigma_mv <= sigma_erc <= sigma_1/n', s_mv <= s_erc + 1e-12 <= s_eq + 2e-12, f'{s_mv:.5f} <= {s_erc:.5f} <= {s_eq:.5f}')
if fails:
    print('\nFAILED:', fails)
    sys.exit(1)
print('\nall checks passed')
