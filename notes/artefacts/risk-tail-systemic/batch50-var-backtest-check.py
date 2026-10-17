"""Batch of 17 October 2026: own synthetic check behind meth:var-es-estimation-methods.

Christoffersen (Elements of Financial Risk Management, 2nd ed., 2012): Historical Simulation (HS) VaR, Filtered
Historical Simulation (FHS: a GARCH variance with the empirical distribution of standardized returns), and the
unconditional coverage test LR_uc = -2 ln[(1-p)^T0 p^T1 / ((1-T1/T)^T0 (T1/T)^T1)] ~ chi2(1), critical value 2.7055
at 10 percent. Checked: (1) 2.7055 is the 90th percentile of chi2(1); (2) on returns simulated from a GARCH(1,1) with
Student-t(6) shocks, 1 percent HS VaR (250-day window) and FHS VaR (true GARCH filter, empirical residual quantile
from the same window) are backtested over 20 000 days: HS's violations cluster (probability of a violation the day
after a violation far above 1 percent) while FHS's do not, the dynamic-updating claim in a setting where the model is
right. This does not test either method on market data.
Run: python3 batch50-var-backtest-check.py   (numpy, scipy; about 5 s). Exits non-zero on failure.
"""
import math
import sys

import numpy as np
from scipy.stats import chi2

rng = np.random.default_rng(1996)
fails = []


def ok(name, cond, detail):
    print(f"  {'ok ' if cond else 'BAD'} {name}: {detail}")
    if not cond:
        fails.append(name)


ok('chi2(1) 90th percentile', abs(chi2.ppf(0.9, 1) - 2.7055) < 5e-4, f'{chi2.ppf(0.9, 1):.4f}')


def lr_uc(hits, p):
    T1 = int(hits.sum()); T0 = len(hits) - T1; pi = T1 / len(hits)
    return -2 * (T0 * math.log(1 - p) + T1 * math.log(p) - T0 * math.log(1 - pi) - T1 * math.log(pi))


omega, a, b, nu, n, win, p = 1e-6, 0.08, 0.90, 6, 20250, 250, 0.01
z = rng.standard_t(nu, n) / math.sqrt(nu / (nu - 2))
s2 = np.empty(n); r = np.empty(n)
s2[0] = omega / (1 - a - b)
for t in range(n):
    r[t] = math.sqrt(s2[t]) * z[t]
    if t + 1 < n:
        s2[t + 1] = omega + a * r[t] ** 2 + b * s2[t]
hs, fhs = [], []
for t in range(win, n):
    past = r[t - win:t]
    var_hs = -np.quantile(past, p)
    zq = np.quantile(past / np.sqrt(s2[t - win:t]), p)
    var_fhs = -math.sqrt(s2[t]) * zq
    hs.append(r[t] < -var_hs); fhs.append(r[t] < -var_fhs)
hs, fhs = np.array(hs), np.array(fhs)
for name, h in (('HS', hs), ('FHS', fhs)):
    after = h[1:][h[:-1]].mean()
    print(f'     {name}: violation rate {h.mean()*100:.2f}%, LR_uc {lr_uc(h, p):.2f}, P(violation | violation yesterday) {after*100:.1f}%')
ok('HS violations cluster', hs[1:][hs[:-1]].mean() > 0.04, 'conditional rate above 4 percent')
ok('FHS violations do not cluster as much', fhs[1:][fhs[:-1]].mean() < hs[1:][hs[:-1]].mean() / 2, 'conditional rate under half of HS')
if fails:
    sys.exit(1)
print('all checks passed')
