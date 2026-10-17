"""derivatives and empirical validation (2026-10-17): when is the ERC portfolio the maximum-Sharpe portfolio? (meth:equal-risk-contribution)

Maillard, Roncalli and Teiletche (sec. 3.5, p. 9) say ERC "is optimal" with a constant correlation matrix and equal
individual Sharpe ratios, by checking the first-order condition mu - r = SR(x) Sigma x / sigma(x). That condition is
met for ANY common Sharpe ratio s, so it locates a stationary point, not necessarily a maximum. Own derivation: with
Sigma = D C D (vols D > 0; C constant correlation rho, -1/(n-1) < rho < 1, so Sigma is positive definite) and
mu - r = s * vols, the Sharpe ratio of long-only, fully invested weights x is SR(x) = s * DR(x), where
DR(x) = sum x_i sigma_i / sigma(x) >= 1 is the diversification ratio, maximised by inverse volatility (= ERC here).
  s > 0: ERC maximises SR (it is also the tangency portfolio Sigma^-1 (mu - r), normalised);
  s = 0: every portfolio has SR 0;
  s < 0: ERC MINIMISES SR among long-only portfolios; the maximum is at a single asset (DR = 1), SR = s.
Counterexample: two uncorrelated unit-volatility assets, each with expected excess return -1: ERC (1/2, 1/2) has
Sharpe -sqrt(2), either asset alone -1.
Run: python3 erc-sharpe-check.py   (numpy). Exits 1 on failure.
"""
import itertools
import math
import sys

import numpy as np

fails = []


def ok(name, cond, detail=''):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


def sharpe(x, ex, S):
    return float(x @ ex / math.sqrt(x @ S @ x))


print('== counterexample: two uncorrelated unit-volatility assets, excess return -1 each')
S = np.eye(2); ex = np.array([-1.0, -1.0]); erc = np.array([0.5, 0.5])
ok('ERC Sharpe = -sqrt(2)', abs(sharpe(erc, ex, S) + math.sqrt(2)) < 1e-12, f'{sharpe(erc, ex, S):+.6f}')
ok('single asset Sharpe = -1', abs(sharpe(np.array([1.0, 0.0]), ex, S) + 1) < 1e-12)
ok('ERC is not the maximum', sharpe(erc, ex, S) < sharpe(np.array([1.0, 0.0]), ex, S))

print('== four assets, vols 10/20/30/40%, constant correlation 0.3; long-only grid of step 1/20')
vols = np.array([0.1, 0.2, 0.3, 0.4]); C = np.full((4, 4), 0.3) + 0.7 * np.eye(4); S = np.outer(vols, vols) * C
iv = (1 / vols) / (1 / vols).sum()
grid = [np.array(w) / 20 for w in itertools.product(range(21), repeat=4) if sum(w) == 20]
for s in (0.4, 0.0, -0.4):
    ex = s * vols
    srs = np.array([sharpe(x, ex, S) for x in grid])
    e = sharpe(iv, ex, S)
    if s > 0:
        tan = np.linalg.solve(S, ex); tan /= tan.sum()
        ok(f's = {s:+.1f}: ERC is the grid maximum and the tangency portfolio', e >= srs.max() - 1e-12 and np.allclose(tan, iv),
           f'ERC {e:+.4f}, grid max {srs.max():+.4f}')
    elif s == 0:
        ok('s = 0: all Sharpe ratios are zero', np.abs(srs).max() < 1e-12 and abs(e) < 1e-12)
    else:
        ok(f's = {s:+.1f}: ERC is the grid MINIMUM; maximum = s at a single asset', e <= srs.min() + 1e-12 and abs(srs.max() - s) < 1e-12,
           f'ERC {e:+.4f}, grid min {srs.min():+.4f}, grid max {srs.max():+.4f}')

print('== unequal correlations break it even for s > 0')
C2 = np.array([[1, 0.8, 0.1, 0.0], [0.8, 1, 0.2, 0.1], [0.1, 0.2, 1, -0.3], [0.0, 0.1, -0.3, 1.0]])
S2 = np.outer(vols, vols) * C2
y = np.ones(4)
for _ in range(20000):
    y = np.sqrt(y / (S2 @ y))
erc2 = y / y.sum()
ex = 0.4 * vols
tan = np.linalg.solve(S2, ex); tan /= tan.sum()
ok('ERC below the tangency Sharpe', sharpe(erc2, ex, S2) < sharpe(tan, ex, S2) - 1e-6,
   f'ERC {sharpe(erc2, ex, S2):+.4f} vs tangency {sharpe(tan, ex, S2):+.4f}')
if fails:
    print('\nFAILED:', fails)
    sys.exit(1)
print('\nall checks passed')
