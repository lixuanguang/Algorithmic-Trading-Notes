"""source verification (2026-10-17): checks behind meth:forecast-scaling-ic (Grinold and Kahn, Active Portfolio Management,
2nd ed., chap. 10, pp. 264-271).

1. Binary model: IC = Cov/(Std r Std g) = 3/(9*4) = 0.0833; refined forecast = 9 * IC * score = 0.75 * score;
   normal scores: |0.75 z| <= 0.75 with probability ~2/3 and |0.75 z| > 1.50 with probability ~1/20.
2. Two forecasts: Var g = 16, Var g' = 25, Cov(g, g') = 5, Cov(r, g) = 3, Cov(r, g') = 4, Var r = 81:
   regression weights Sigma^-1 c = (0.1467, 0.1307); IC of g' = 4/(9*5) = 0.089; combined IC sqrt(c' Sigma^-1 c)/9 = 0.1090.
3. Table 10.1: alpha = residual volatility * 0.09 * score, to within the rounding of the printed two-decimal scores.
Run: python3 forecast-checks.py   (numpy, scipy). Exits non-zero on failure.
"""
import sys

import numpy as np
from scipy.stats import norm

fails = []


def check(name, got, want, tol):
    ok = abs(got - want) <= tol
    print(f"  {'ok ' if ok else 'BAD'} {name}: {got:.5f} (want {want}, tol {tol})")
    if not ok:
        fails.append(name)


print('== 1. One forecast')
ic = 3 / (9 * 4)
check('IC', ic, 0.0833, 5e-5)
check('multiplier volatility * IC', 9 * ic, 0.75, 1e-12)
check('P(|z| <= 1)', 2 * norm.cdf(1) - 1, 2 / 3, 0.02)
check('P(|z| > 2)', 2 * (1 - norm.cdf(2)), 1 / 20, 0.005)

print('\n== 2. Two forecasts')
Sig = np.array([[16.0, 5.0], [5.0, 25.0]])
c = np.array([3.0, 4.0])
w = np.linalg.solve(Sig, c)
check('weight on g', w[0], 0.1467, 5e-5)
check("weight on g'", w[1], 0.1307, 5e-5)
check("IC of g'", 4 / 45, 0.089, 5e-4)
check('combined IC', np.sqrt(c @ w) / 9, 0.1090, 5e-5)

print('\n== 3. Table 10.1 (IC 0.09)')
rows = {'American Express': (23.26, 0.35, 0.73), 'AT&T': (15.89, 0.71, 1.01), 'DuPont': (17.29, 1.58, 2.47),
        'General Motors': (23.46, 1.98, 4.17), 'IBM': (30.32, -0.67, -1.84), 'Johnson & Johnson': (18.97, -1.77, -3.02),
        'Procter & Gamble': (16.29, -2.32, -3.40), 'Exxon': (21.13, 0.00, -0.01)}
for name, (vol, score, alpha) in rows.items():
    check(name, vol * 0.09 * score, alpha, vol * 0.09 * 0.005 + 0.005)

if fails:
    print('\nFAILED:', fails)
    sys.exit(1)
print('\nall checks passed')
