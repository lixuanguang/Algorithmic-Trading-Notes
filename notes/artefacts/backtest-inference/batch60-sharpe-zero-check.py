"""Third batch of 17 October 2026 (audit repair): what the finite-fourth-moment condition of
meth:sharpe-ratio-standard-error is, and is not, needed for.

Derivation (own, not Lo's). With IID returns, mean mu, variance sigma^2 > 0 and SR = (mu - Rf)/sigma:
  * SR = 0 (mu = Rf). Then sqrt(T) * SR_hat = sqrt(T) (mu_hat - mu) / sigma_hat. The classical CLT gives
    sqrt(T)(mu_hat - mu)/sigma -> N(0,1) with a finite variance alone; the weak law of large numbers gives
    sigma_hat -> sigma (finite variance suffices); Slutsky's lemma gives sqrt(T) SR_hat -> N(0,1). No fourth moment
    is needed, so a finite fourth moment is not necessary for every normal limit of the Sharpe-ratio estimator.
  * SR != 0. The joint delta method on (mu_hat, sigma2_hat) uses sqrt(T)(sigma2_hat - sigma^2) -> N(0, nu4 - sigma^4),
    which needs a finite fourth moment. That is the sufficient condition used for the general variance
    V = 1 - g3 SR + (g4 - 1) SR^2 / 4.
  * "Normal moments, and only then". V = 1 + SR^2/2 iff SR = 0 or g4 = 3 + 4 g3 / SR. So normal third and fourth
    moments are sufficient, not necessary: a symmetric non-normal law with kurtosis 3 gives the same V.
Checks (Monte Carlo):
  1. centred IID Student-t3 (finite variance, infinite fourth moment), SR = 0: Var(sqrt(T) SR_hat) near 1 and
     tail frequencies near the normal ones at T = 10 000;
  2. the three-point law {-sqrt(3), 0, +sqrt(3)} with probabilities {1/6, 2/3, 1/6} (variance 1, skewness 0,
     kurtosis 3, not normal), shifted to SR = 0.5: T Var(SR_hat) near 1 + 0.5^2/2 = 1.125.
Run: python3 batch60-sharpe-zero-check.py   (numpy; about 10 s). Exits non-zero on failure.
"""
import math
import sys

import numpy as np

rng = np.random.default_rng(31)
fails = []


def check(name, ok, detail):
    print(f"  {'ok ' if ok else 'BAD'} {name}: {detail}")
    if not ok:
        fails.append(name)


def root_t_sr(draw, T, reps, sr_true=0.0, chunk=250):
    out = []
    for _ in range(reps // chunk):
        x = draw((chunk, T))
        s = x.mean(axis=1) / x.std(axis=1, ddof=0)
        out.append(math.sqrt(T) * (s - sr_true))
    return np.concatenate(out)


print('== 1. centred Student-t3, SR = 0')
T, reps = 10000, 4000
z = root_t_sr(lambda size: rng.standard_t(3, size), T, reps)
v = z.var()
tail = np.mean(np.abs(z) > 1.96)
check('Var(sqrt(T) SR_hat) within 0.08 of 1', abs(v - 1) < 0.08, f'{v:.3f}')
check('P(|sqrt(T) SR_hat| > 1.96) within 0.012 of 0.05', abs(tail - 0.05) < 0.012, f'{tail:.4f}')

print('== 2. a non-normal law with skewness 0 and kurtosis 3 gives 1 + SR^2/2')
vals = np.array([-math.sqrt(3), 0.0, math.sqrt(3)])
probs = np.array([1 / 6, 2 / 3, 1 / 6])
m2 = float((probs * vals ** 2).sum()); m4 = float((probs * vals ** 4).sum())
check('kurtosis of the three-point law is 3', abs(m4 / m2 ** 2 - 3) < 1e-12, f'{m4 / m2 ** 2:.3f}')
sr = 0.5
T2, reps2 = 2000, 8000
y = root_t_sr(lambda size: vals[rng.choice(3, size=size, p=probs)] + sr, T2, reps2, sr_true=sr)
v2 = y.var()
check('T Var(SR_hat) within 0.06 of 1.125', abs(v2 - 1.125) < 0.06, f'{v2:.3f}')
if fails:
    print('\nFAILED:', fails)
    sys.exit(1)
print('\nall checks passed')
