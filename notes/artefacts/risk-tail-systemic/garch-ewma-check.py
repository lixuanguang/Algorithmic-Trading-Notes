"""empirical extensions (2026-10-17): own check behind mod:garch-volatility-forecast.

Christoffersen (2nd ed., chap. 4, PDF p. 81): GARCH(1,1) sigma2_{t+1} = omega + alpha R_t^2 + beta sigma2_t with
long-run variance sigma2 = omega/(1 - alpha - beta) and k-step forecast
E_t[sigma2_{t+k}] - sigma2 = (alpha + beta)^(k-1) (sigma2_{t+1} - sigma2); RiskMetrics (EWMA, lambda = 0.94) is the
case omega = 0, alpha + beta = 1, whose forecast is flat in k. Checked: (1) the k-step formula against simulation;
(2) in a world where GARCH(1,1) is true (synthetic, Gaussian shocks), the out-of-sample mean squared error of the
cumulative 1-day and 20-day variance forecasts of EWMA relative to the true GARCH forecast. This shows only how the
difference grows with the horizon when GARCH is the data-generating process; it is not evidence about market data.
Run: python3 garch-ewma-check.py   (numpy; about 3 s). Exits non-zero on failure.
"""
import sys

import numpy as np

rng = np.random.default_rng(1986)
fails = []


def ok(name, cond, detail=''):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


omega, alpha, beta = 2e-6, 0.08, 0.90
lr = omega / (1 - alpha - beta)
# (1) k-step forecast by Monte Carlo from a high starting variance
s2_next = 4 * lr
k = 10
paths = 200000
s2 = np.full(paths, s2_next)
for _ in range(k - 1):
    R = np.sqrt(s2) * rng.standard_normal(paths)
    s2 = omega + alpha * R ** 2 + beta * s2
mc = s2.mean(); formula = lr + (alpha + beta) ** (k - 1) * (s2_next - lr)
ok('k-step GARCH forecast matches simulation (k = 10)', abs(mc / formula - 1) < 0.01, f'{mc:.3e} vs {formula:.3e}')

# (2) EWMA against the true GARCH forecast, cumulative variance over h days
n = 60000
R = np.empty(n); s2 = np.empty(n); s2[0] = lr
for t in range(n):
    R[t] = np.sqrt(s2[t]) * rng.standard_normal()
    if t + 1 < n:
        s2[t + 1] = omega + alpha * R[t] ** 2 + beta * s2[t]
ew = np.empty(n); ew[0] = lr
for t in range(n - 1):
    ew[t + 1] = 0.94 * ew[t] + 0.06 * R[t] ** 2
out = {}
for h in (1, 20):
    idx = np.arange(1000, n - h)
    real = np.array([np.sum(R[t:t + h] ** 2) for t in idx])
    g = np.array([sum(lr + (alpha + beta) ** j * (s2[t] - lr) for j in range(h)) for t in idx])
    e = h * ew[idx]
    out[h] = (np.mean((real - e) ** 2) / np.mean((real - g) ** 2))
    print(f'     horizon {h:2d}: MSE(EWMA)/MSE(GARCH) = {out[h]:.3f}')
ok('EWMA close to GARCH at one day (within 10 percent MSE)', out[1] < 1.10, f'{out[1]:.3f}')
ok('EWMA relatively worse at 20 days than at 1 day', out[20] > out[1], f'{out[20]:.3f} > {out[1]:.3f}')
if fails:
    print('\nFAILED:', fails)
    sys.exit(1)
print('\nall checks passed')
