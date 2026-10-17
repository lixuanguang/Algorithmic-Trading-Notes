"""source verification (2026-10-17) (audit repair): conditions behind meth:sharpe-ratio-standard-error.

Independent numerical checks, not reproductions of the entry's formulas from the same code path:
1. General IID asymptotic variance of the Sharpe-ratio estimator, V = 1 - g3*SR + (g4 - 1)/4 * SR^2
   (g3 skewness, g4 kurtosis, not excess), against Monte Carlo for a skewed two-point distribution, where the
   normal-moment value 1 + SR^2/2 is wrong. The normal case is checked too.
2. A counterexample to "finite mean and variance suffice": IID Student-t returns with 3 degrees of freedom
   (finite variance, infinite fourth moment) and SR != 0. T * Var(SR_hat) keeps growing with T instead of settling
   at a finite V; a robust spread measure (interquartile range * sqrt(T)) is printed alongside.
3. Time aggregation of ADDITIVE returns: SR(q) = sqrt(q) * SR needs only constant mean and variance with zero
   autocovariances, not independence. Checked exactly (by construction of the variance) and by simulation for the
   dependent but uncorrelated process e_t = z_t * z_{t-1}.
4. Compounded simple returns: for IID lognormal one-period gross returns, the Sharpe ratio of the compounded
   q-period simple return (excess over a compounded constant benchmark) differs from sqrt(q) times the one-period
   ratio; the exact moments are computed in closed form.
Run: python3 sharpe-conditions-checks.py   (numpy; about 2 s). Exits non-zero on failure.
"""
import math
import sys

import numpy as np

rng = np.random.default_rng(20261017)
fails = []


def check(name, ok, detail):
    print(f"  {'ok ' if ok else 'BAD'} {name}: {detail}")
    if not ok:
        fails.append(name)


def sr_hat(x):
    return x.mean(axis=-1) / x.std(axis=-1, ddof=0)


print('== 1. General IID variance against Monte Carlo')
# two-point returns: value a with prob p, b with prob 1-p
p, a, b = 0.1, -0.30, 0.06
mu = p * a + (1 - p) * b
var = p * (a - mu) ** 2 + (1 - p) * (b - mu) ** 2
sd = math.sqrt(var)
g3 = (p * (a - mu) ** 3 + (1 - p) * (b - mu) ** 3) / sd ** 3
g4 = (p * (a - mu) ** 4 + (1 - p) * (b - mu) ** 4) / sd ** 4
SR = mu / sd
V_gen = 1 - g3 * SR + (g4 - 1) / 4 * SR ** 2
V_norm = 1 + SR ** 2 / 2
T, R = 2000, 20000
x = np.where(rng.random((R, T)) < p, a, b)
V_mc = T * sr_hat(x).var()
se_mc = V_mc * math.sqrt(2 / (R - 1))
print(f'     two-point: SR {SR:.3f}, skewness {g3:.3f}, kurtosis {g4:.3f}; V general {V_gen:.4f}, normal-moment {V_norm:.4f}, MC {V_mc:.4f} (+/- {se_mc:.4f})')
check('MC matches the general formula (within 4 MC s.e.)', abs(V_mc - V_gen) < 4 * se_mc, f'|{V_mc:.4f} - {V_gen:.4f}|')
check('MC rejects 1 + SR^2/2 (more than 10 MC s.e. away)', abs(V_mc - V_norm) > 10 * se_mc, f'|{V_mc:.4f} - {V_norm:.4f}|')
SRn = 0.4
xn = SRn + rng.standard_normal((R, T))
V_mc_n = T * sr_hat(xn).var()
check('normal returns: MC matches 1 + SR^2/2', abs(V_mc_n - (1 + SRn ** 2 / 2)) < 4 * V_mc_n * math.sqrt(2 / (R - 1)),
      f'{V_mc_n:.4f} against {1 + SRn ** 2 / 2:.4f}')

print('\n== 2. Finite variance is not enough: Student-t(3), SR = 0.5')
nu = 3
scale = math.sqrt((nu - 2) / nu)  # unit variance
out = []
for T in (250, 2000, 16000):
    Rr = 4000 if T < 16000 else 1500
    s = np.empty(Rr)
    for i in range(0, Rr, 500):
        y = 0.5 + scale * rng.standard_t(nu, size=(min(500, Rr - i), T))
        s[i:i + len(y)] = sr_hat(y)
    tv = T * s.var()
    iqr = (np.quantile(s, 0.75) - np.quantile(s, 0.25)) * math.sqrt(T)
    out.append(tv)
    print(f'     T {T:6d}: T*Var(SR_hat) = {tv:.3f}   sqrt(T)*IQR = {iqr:.3f}')
print(f'     normal-moment formula would give {1 + 0.25 / 2:.3f}')
check('T*Var(SR_hat) grows with T (no finite V under infinite kurtosis)', out[2] > out[0] * 1.3, f'{out[0]:.3f} -> {out[2]:.3f}')

print('\n== 3. Zero autocovariance suffices for sqrt(q) scaling of additive returns')
q = 12
mu1 = 0.05
z = rng.standard_normal(600001)
e = z[1:] * z[:-1]  # uncorrelated, not independent (e_t^2 and e_{t-1}^2 are correlated)
r = mu1 + e
ac1 = np.corrcoef(r[1:], r[:-1])[0, 1]
ac_sq = np.corrcoef(e[1:] ** 2, e[:-1] ** 2)[0, 1]
n = len(r) // q
rq = r[:n * q].reshape(n, q).sum(axis=1)
sr1 = r.mean() / r.std()
srq = rq.mean() / rq.std()
check('process is uncorrelated but dependent', abs(ac1) < 0.01 and ac_sq > 0.1, f'corr(r_t, r_t-1) {ac1:+.4f}, corr(e_t^2, e_t-1^2) {ac_sq:+.3f}')
check('SR(12) = sqrt(12) SR(1) within sampling error', abs(srq / (math.sqrt(q) * sr1) - 1) < 0.08, f'ratio {srq / (math.sqrt(q) * sr1):.4f}')

print('\n== 4. Compounded simple returns do not scale exactly by sqrt(q)')
m, s1, rf = 0.008, 0.045, 0.002  # monthly log-return mean and sd, monthly simple benchmark
E1 = math.exp(m + s1 ** 2 / 2)
V1 = math.exp(2 * m + s1 ** 2) * (math.exp(s1 ** 2) - 1)
SR1 = (E1 - 1 - rf) / math.sqrt(V1)
Eq = math.exp(q * m + q * s1 ** 2 / 2)
Vq = math.exp(2 * q * m + q * s1 ** 2) * (math.exp(q * s1 ** 2) - 1)
SRq = (Eq - (1 + rf) ** q) / math.sqrt(Vq)
print(f'     monthly SR {SR1:.4f}; sqrt(12)*SR {math.sqrt(q) * SR1:.4f}; compounded 12-month SR {SRq:.4f}')
check('compounded annual SR differs from sqrt(12) x monthly by more than 1 percent',
      abs(SRq / (math.sqrt(q) * SR1) - 1) > 0.01, f'ratio {SRq / (math.sqrt(q) * SR1):.4f}')
# with additive (summed) log excess returns and an additive benchmark the scaling is exact
lr = math.log(1 + rf)
SR1l = (m - lr) / s1
SRql = (q * m - q * lr) / (math.sqrt(q) * s1)
check('summed log returns over a summed log benchmark scale exactly', abs(SRql - math.sqrt(q) * SR1l) < 1e-12, f'{SRql:.6f}')

if fails:
    print('\nFAILED:', fails)
    sys.exit(1)
print('\nall checks passed')
