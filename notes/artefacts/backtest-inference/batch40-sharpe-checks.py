"""Batch of 17 October 2026: checks behind meth:sharpe-ratio-standard-error and meth:deflated-sharpe-ratio.

1. Lo (2002), FAJ 58(4), eq. (9), p. 38: SE(SR) = sqrt((1 + SR^2/2)/T) under IID returns; his examples for T = 60
   (0.188 at SR 1.50, 0.303 at SR 3.00).
2. Lo, eqs. (20) and (22), pp. 40-41: eta(q) = q / sqrt(q + 2 sum_{k=1}^{q-1} (q-k) rho_k), and for AR(1) returns
   (rho_k = rho^k) the closed form (22); against Table 2 (p. 41) at q = 12: 4.17 (rho = -0.2), 3.46 (0), 2.88 (0.2),
   and a sample of other cells. A Monte Carlo AR(1) check of the IID standard error's understatement is not claimed.
3. Bailey and Lopez de Prado, author version of 31 July 2014, eqs. (1)-(2), pp. 7-8, and the numerical example,
   pp. 9-10: SR0 = 0.1132 (non-annualised, 250 observations a year) and DSR = 0.9004 for N = 100, V = 1/2 annualised,
   T = 1250, skewness -3, kurtosis 10, SR = 2.5 annualised; DSR = 0.9505 at N = 46; and with normal returns
   (skewness 0, kurtosis 3) DSR = 0.9505 "after N = 88".
Run: python3 batch40-sharpe-checks.py   (scipy). Exits non-zero on failure.
"""
import math
import sys

from scipy.stats import norm

fails = []


def check(name, got, want, tol):
    ok = abs(got - want) <= tol
    print(f"  {'ok ' if ok else 'BAD'} {name}: {got:.6f} (want {want}, tol {tol})")
    if not ok:
        fails.append(name)


print('== 1. Lo eq. (9)')
se = lambda sr, T: math.sqrt((1 + 0.5 * sr * sr) / T)
check('SE at SR 1.50, T 60', se(1.5, 60), 0.188, 5e-4)
check('SE at SR 3.00, T 60', se(3.0, 60), 0.303, 5e-4)
check('SE/SR limit sqrt(1/(2T)) at T 60, SR 1e4', se(1e4, 60) / 1e4, math.sqrt(1 / 120), 1e-6)

print('\n== 2. Lo eqs. (20) and (22), Table 2')


def eta_sum(q, rho):
    return q / math.sqrt(q + 2 * sum((q - k) * rho ** k for k in range(1, q)))


def eta_22(q, rho):
    if rho == 0:
        return math.sqrt(q)
    return math.sqrt(q) * (1 + 2 * rho / (1 - rho) * (1 - (1 - rho ** q) / (q * (1 - rho)))) ** -0.5


table = {(12, -0.2): 4.17, (12, 0.0): 3.46, (12, 0.2): 2.88, (2, 0.9): 1.03, (250, -0.9): 67.65,
         (24, 0.5): 2.91, (48, -0.5): 11.84, (6, 0.1): 2.25}
for (q, rho), want in table.items():
    check(f'eta({q}, rho={rho}) by eq. (22) against Table 2', eta_22(q, rho), want, 0.006)
    check(f'eta({q}, rho={rho}) eq. (20) = eq. (22)', eta_sum(q, rho), eta_22(q, rho), 1e-9)

print('\n== 3. Deflated Sharpe ratio, eqs. (1)-(2) and the example')
g = 0.5772156649015329  # Euler-Mascheroni


def sr0(N, V):
    return math.sqrt(V) * ((1 - g) * norm.ppf(1 - 1 / N) + g * norm.ppf(1 - 1 / (N * math.e)))


def dsr(sr, s0, T, g3, g4):
    return norm.cdf((sr - s0) * math.sqrt(T - 1) / math.sqrt(1 - g3 * sr + (g4 - 1) / 4 * sr * sr))


V = 0.5 / 250
sr = 2.5 / math.sqrt(250)
check('SR0 at N = 100 (non-annualised)', sr0(100, V), 0.1132, 5e-5)
check('DSR at N = 100, skew -3, kurtosis 10', dsr(sr, sr0(100, V), 1250, -3, 10), 0.9004, 5e-5)
check('DSR at N = 46', dsr(sr, sr0(46, V), 1250, -3, 10), 0.9505, 5e-5)
check('DSR at N = 88 with normal returns', dsr(sr, sr0(88, V), 1250, 0, 3), 0.9505, 5e-4)
print(f'     normal returns: DSR at N = 87, 88, 89: '
      f'{dsr(sr, sr0(87, V), 1250, 0, 3):.4f}, {dsr(sr, sr0(88, V), 1250, 0, 3):.4f}, {dsr(sr, sr0(89, V), 1250, 0, 3):.4f}')

if fails:
    print('\nFAILED:', fails)
    sys.exit(1)
print('\nall checks passed')
