"""Slice-32 follow-up check (2026-10-16): a negative minimum-variance hedge ratio reduces variance.

Position convention as in mod:minimum-variance-hedge-ratio: hedged change V(h) = dS - h dF, so h > 0 is a short
futures position against a long exposure and h < 0 a long one.
Run: python3 negative-hedge-ratio-check.py   (numpy only)
"""
import numpy as np

sS, sF, rho = 1.0, 1.0, -0.6
var = lambda h: sS**2 - 2 * h * rho * sS * sF + h**2 * sF**2
hstar = rho * sS / sF
print('analytic: h* =', hstar, ' Var(h*) =', var(hstar), ' Var(0) =', var(0.0), ' Var(+0.6) =', var(0.6))

rng = np.random.default_rng(7)
n = 200_000
z1, z2 = rng.standard_normal(n), rng.standard_normal(n)
dF = sF * z1
dS = sS * (rho * z1 + np.sqrt(1 - rho**2) * z2)
h_ols = np.cov(dS, dF)[0, 1] / dF.var(ddof=1)
grid = np.linspace(-1.5, 1.5, 3001)
h_grid = grid[np.argmin([np.var(dS - h * dF) for h in grid])]
print(f'simulated: Cov/Var = {h_ols:.4f}, grid minimiser = {h_grid:.4f}')
for h in [0.0, h_ols, -h_ols]:
    print(f'  h = {h:+.4f}: Var(dS - h dF) = {np.var(dS - h * dF):.4f}')
print('a long futures position (h < 0) against a long exposure removes', f'{1 - np.var(dS - h_ols * dF) / np.var(dS):.3f}',
      'of the variance (rho^2 =', rho**2, '); the same size short adds variance')
