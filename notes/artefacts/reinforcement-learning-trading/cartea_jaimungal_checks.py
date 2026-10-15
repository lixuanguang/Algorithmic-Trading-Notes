"""Numerical checks for mod:cartea-jaimungal-execution (migration slice 16, 2026-10-15).

Checks Lehalle and Laruelle, app. A.7.3, pp. 281-284: the reduction of the HJB equation with the
inventory term -nu*dqH, the Riccati solution for h2 against direct integration (the printed closed
form gives h2(T) = A - b), the Feynman-Kac form of h1 (the boxed formula omits the factor b), the
Almgren-Chriss limit (mu = 0, A -> infinity) and the inventory paths behind the parameter intuition.
Illustrative parameters in consistent units; standard library only.  Run: python3 cartea_jaimungal_checks.py

Follow-up to slice 16 (2026-10-15), in followup_checks(): the pathwise wealth identity behind the
corrected terminal payoff Q_T(S_T - psi/2 - A Q_T); a direct discretised optimisation compared with the
feedback policies for the corrected payoff (decomposition h = H - x - q(S - psi/2)) and for the printed
payoff (decomposition g = H - x - qS); the infinite-value counterexample nu = -M; and the variance of
b * int Q mu dt for Q_t = 1 - t, mu_t = B_t (b^2/20).
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
    followup_checks()


def wealth_sim(nu, mu, Q0, S0, b, kappa, psi, phi, A, T, printed=False):
    """Euler simulation of the dynamics with sigma = 0; returns the realised reward."""
    n = len(nu); dt = T / n; S, Q, X, run = S0, Q0, 0.0, 0.0
    for i in range(n):
        X += (S - psi / 2 - kappa * nu[i]) * nu[i] * dt
        run += phi * Q * Q * dt
        S += b * (mu[i] - nu[i]) * dt
        Q -= nu[i] * dt
    term = Q * (S - A * Q) if printed else Q * (S - psi / 2 - A * Q)
    return X + term - run, Q


def wealth_identity(nu, mu, Q0, S0, b, kappa, psi, phi, A, T):
    """Q0 S0 - psi Q0/2 - b Q0^2/2 + b int Q mu - kappa int nu^2 - phi int Q^2 - (A - b/2) Q_T^2."""
    n = len(nu); dt = T / n; Q, Imu, Inu, IQ = Q0, 0.0, 0.0, 0.0
    for i in range(n):
        Imu += Q * mu[i] * dt; Inu += nu[i] ** 2 * dt; IQ += Q * Q * dt
        Q -= nu[i] * dt
    return Q0 * S0 - psi * Q0 / 2 - b * Q0 ** 2 / 2 + b * Imu - kappa * Inu - phi * IQ - (A - b / 2) * Q * Q


def direct_optimum(Q0, kappa, phi, A, b, psi, T, n, printed):
    """Maximise -kappa sum nu^2 dt - phi sum Q_k^2 dt - (A - b/2) Q_n^2 [+ psi/2 Q_n if printed] over Q_1..Q_n
    (mu = sigma = 0): a concave quadratic when kappa > 0, phi >= 0 and A > b/2; tridiagonal first-order conditions."""
    dt = T / n; c = kappa / dt
    a_, d_, u_, r_ = [0.0] * n, [0.0] * n, [0.0] * n, [0.0] * n
    for k in range(1, n + 1):  # d/dQ_k of the objective = 0
        i = k - 1
        if k < n:
            d_[i] = 2 * c + phi * dt; u_[i] = -c
        else:
            d_[i] = c + phi * dt + (A - b / 2); r_[i] = psi / 4 if printed else 0.0
        a_[i] = -c if k > 1 else 0.0
        if k == 1:
            r_[i] += c * Q0
    for i in range(1, n):  # Thomas algorithm, system d Q_k + a Q_{k-1} + u Q_{k+1} = r (scaled by 1/2)
        w = a_[i] / d_[i - 1]; d_[i] -= w * u_[i - 1]; r_[i] -= w * r_[i - 1]
    Q = [0.0] * n; Q[-1] = r_[-1] / d_[-1]
    for i in range(n - 2, -1, -1):
        Q[i] = (r_[i] - u_[i] * Q[i + 1]) / d_[i]
    return Q


def feedback_path(Q0, kappa, phi, A, b, psi, T, n, printed):
    """mu = 0: nu* = xi q / kappa (corrected payoff, h = H - x - q(S - psi/2));
    printed payoff (g = H - x - qS): nu = xi q / kappa - psi/(4 kappa) exp(-(1/kappa) int_t^T xi)."""
    dt = T / n; tail = [0.0] * (n + 1)
    for i in range(n - 1, -1, -1):
        tail[i] = tail[i + 1] + xi((i + 0.5) * dt, T, kappa, phi, A, b) * dt
    Q, out = Q0, []
    for i in range(n):
        t = i * dt; nu = xi(t, T, kappa, phi, A, b) / kappa * Q
        if printed:
            nu -= psi / (4 * kappa) * math.exp(-tail[i] / kappa)
        Q -= nu * dt; out.append(Q)
    return out


def followup_checks():
    print('--- follow-up checks (2026-10-15)')
    random.seed(1)
    T, n, Q0, S0 = 1.0, 4000, 1.0, 10.0
    b, kappa, psi, phi, A = 0.1, 0.01, 0.02, 0.001, 0.08
    nu = [random.uniform(-2, 3) for _ in range(n)]; mu = [random.uniform(-1, 1) for _ in range(n)]
    print('wealth identity: simulated %.6f, identity %.6f'
          % (wealth_sim(nu, mu, Q0, S0, b, kappa, psi, phi, A, T)[0],
             wealth_identity(nu, mu, Q0, S0, b, kappa, psi, phi, A, T)))
    kappa, phi, A, b, psi, n = 0.01, 0.001, 0.05, 0.02, 0.01, 2000
    for printed in (False, True):
        d = direct_optimum(Q0, kappa, phi, A, b, psi, T, n, printed)
        f = feedback_path(Q0, kappa, phi, A, b, psi, T, n, printed)
        print('%s payoff: Q(T/2) direct %.4f feedback %.4f; Q(T) direct %.4f feedback %.4f'
              % ('printed  ' if printed else 'corrected', d[n // 2 - 1], f[n // 2 - 1], d[-1], f[-1]))
    # counterexample: T = Q0 = 1, mu = sigma = psi = 0, b = 0.1, kappa = A = 0.01, phi = 0.001, nu = -M
    b, kappa, A, phi, psi = 0.1, 0.01, 0.01, 0.001, 0.0
    coef = b / 2 - kappa - A - phi / 3
    print('nu = -M: M^2 coefficient b/2 - kappa - A - phi/3 = %.6f' % coef)
    for M in (10, 100, 1000):
        r, _ = wealth_sim([-M] * 4000, [0.0] * 4000, 1.0, S0, b, kappa, psi, phi, A, 1.0)
        print('  M=%5d reward %.4e, reward/M^2 %.6f' % (M, r, r / M ** 2))
    A = 0.06  # sufficient regime A > b/2
    r, _ = wealth_sim([-1000] * 4000, [0.0] * 4000, 1.0, S0, b, kappa, psi, phi, A, 1.0)
    print('  A=0.06 > b/2: M=1000 reward/M^2 %.6f (b/2 - kappa - A - phi/3 = %.6f)'
          % (r / 1e6, b / 2 - kappa - A - phi / 3))
    # variance of int_0^1 (1 - t) B_t dt: exact 1/20
    m = 400; dt = 1.0 / m
    exact = sum((1 - (i + .5) * dt) * (1 - (j + .5) * dt) * min(i + .5, j + .5) * dt
                for i in range(m) for j in range(m)) * dt * dt
    paths, acc, acc2 = 20000, 0.0, 0.0
    for _ in range(paths):
        B, I = 0.0, 0.0
        for i in range(200):
            B += random.gauss(0, math.sqrt(1 / 200)); I += (1 - (i + 1) / 200) * B / 200
        acc += I; acc2 += I * I
    print('Var int (1-t) B_t dt: quadrature %.5f, Monte Carlo %.5f, 1/20 = %.5f'
          % (exact, acc2 / paths - (acc / paths) ** 2, 1 / 20))


if __name__ == '__main__':
    main()
