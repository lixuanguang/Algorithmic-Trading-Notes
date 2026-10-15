"""Numerical checks for mod:cartea-jaimungal-execution (migration slice 16, 2026-10-15).

Checks Lehalle and Laruelle, app. A.7.3, pp. 281-284: the reduction of the HJB equation with the
inventory term -nu*dqH, the Riccati solution for h2 against direct integration (the printed closed
form gives h2(T) = A - b), the Feynman-Kac form of h1 (the boxed formula omits the factor b), the
Almgren-Chriss limit (mu = 0, A -> infinity) and the inventory paths behind the parameter intuition.
Illustrative parameters in consistent units; standard library only.  Run: python3 cartea_jaimungal_checks.py
"""
import math
import random


def xi(t, T, k, phi, A, b, printed=False):
    g, r, s = math.sqrt(phi / k), A - b / 2, math.sqrt(k * phi)
    if printed:  # as printed: zeta inverted, exponent +2 gamma (T - t)
        z = (r + s) / (r - s); E = z * math.exp(2 * g * (T - t))
    else:
        z = (r - s) / (r + s); E = z * math.exp(-2 * g * (T - t))
    return s * (1 + E) / (1 - E)


def path(k, phi, A, b=0.0, T=1.0, n=20000):
    Q, dt, out = 1.0, T / n, []
    for i in range(n):
        Q -= dt * xi(i * dt, T, k, phi, A, b) / k * Q
        if i + 1 in (n // 4, n // 2):
            out.append(round(Q, 4))
    return out + [round(Q, 4)]


def main():
    random.seed(0)
    for _ in range(3):
        S, psi, mu, q, nu, dqh, k, b = [random.uniform(-2, 2) for _ in range(8)]
        full = nu * (S - psi / 2 - k * nu) + b * (mu - nu) * q - nu * (S - psi / 2 + dqh)
        reduced = -k * nu ** 2 - (b * q + dqh) * nu + b * mu * q
        print('HJB reduction difference %.1e' % (full - reduced))
    k, phi, A, b, T = 0.01, 0.001, 0.5, 0.002, 1.0
    n, h = 200000, -A
    for _ in range(n):
        h -= (T / n) * (phi - (b + 2 * h) ** 2 / (4 * k))
    print('h2(0): ODE %.6f, corrected form %.6f, printed form %.6f'
          % (h, -xi(0, T, k, phi, A, b) - b / 2, -xi(0, T, k, phi, A, b, True) - b / 2))
    print('h2(T) printed form %.4f (should be -A = %.4f)' % (-xi(T, T, k, phi, A, b, True) - b / 2, -A))
    m, n, h1 = 0.3, 100000, 0.0  # constant flow, so L^mu h1 = 0
    dt = T / n
    for i in range(n, 0, -1):
        h1 -= dt * (-b * m + xi(i * dt, T, k, phi, A, b) * h1 / k)
    tot, I = 0.0, 0.0
    for i in range(n):
        tot += math.exp(-I / k) * m * dt; I += xi(i * dt, T, k, phi, A, b) * dt
    print('h1(0): ODE %.6f, b*FK %.6f, boxed without b %.6f' % (h1, b * tot, tot))
    print('Q at t = 0.25, 0.5, 1')
    print('  base kappa=0.01 phi=0.001 A=0.5', path(0.01, 0.001, 0.5))
    print('  phi x10                       ', path(0.01, 0.01, 0.5))
    print('  A x10                         ', path(0.01, 0.001, 5.0))
    print('  kappa x10                     ', path(0.1, 0.001, 0.5))
    g = math.sqrt(0.001 / 0.01)
    print('  A=1e6                         ', path(0.01, 0.001, 1e6),
          'Almgren-Chriss sinh', [round(math.sinh(g * (1 - t)) / math.sinh(g), 4) for t in (0.25, 0.5)])


if __name__ == '__main__':
    main()
