"""Numerical demonstration for mod:cartea-jaimungal-execution.

Execution control, source review, optimal execution and high-frequency strategies reviews.
Lehalle and Laruelle, app. A.7.3, pp. 281-284: the reduction of the HJB equation with the
inventory term -nu*dqH, the Riccati solution for h2 against direct integration (the printed
closed form gives h2(T) = A - b), the Feynman-Kac form of h1 (the boxed formula omits the factor
b), the Almgren-Chriss limit (mu = 0, A -> infinity) and the inventory paths behind the parameter
intuition. Illustrative parameters in consistent units; standard library only.

Follow-up to the execution control review (2026-10-15), in
check_wealth_identity_and_feedback(): the pathwise wealth identity behind the corrected terminal
payoff Q_T(S_T - psi/2 - A Q_T); a direct discretised optimisation compared with the feedback
policies for the corrected payoff (decomposition h = H - x - q(S - psi/2)) and for the printed
payoff (decomposition g = H - x - qS); the infinite-value counterexample nu = -M; and the variance
of b * int Q mu dt for Q_t = 1 - t, mu_t = B_t (b^2/20).

This is a demonstration, not a checker: it prints its values for comparison by eye, asserts
nothing and exits 0. Each section draws from its own seeded generator, never the shared one.
Run: uv run --frozen --no-editable python -m trading_notes.numerical.cartea_jaimungal
"""

import math
import random
import sys
from collections.abc import Sequence


def xi(
    t: float, T: float, k: float, phi: float, A: float, b: float, printed: bool = False
) -> float:
    """Return the Riccati feedback coefficient at time t, corrected or as printed.

    Args:
        t: Time.
        T: Horizon.
        k: Temporary impact kappa.
        phi: Running inventory penalty.
        A: Terminal liquidation penalty.
        b: Permanent impact.
        printed: Use the printed closed form, with zeta inverted and exponent +2 gamma (T - t).
    """
    g, r, s = math.sqrt(phi / k), A - b / 2, math.sqrt(k * phi)
    if printed:
        z = (r + s) / (r - s)
        E = z * math.exp(2 * g * (T - t))
    else:
        z = (r - s) / (r + s)
        E = z * math.exp(-2 * g * (T - t))
    return s * (1 + E) / (1 - E)


def path(
    k: float, phi: float, A: float, b: float = 0.0, T: float = 1.0, n: int = 20000
) -> list[float]:
    """Return the inventory Q at T/4, T/2 and T under the corrected feedback, to 4 decimals.

    Q starts at 1 and is stepped forward by Euler with n steps.
    """
    Q, dt, out = 1.0, T / n, []
    for i in range(n):
        Q -= dt * xi(i * dt, T, k, phi, A, b) / k * Q
        if i + 1 in (n // 4, n // 2):
            out.append(round(Q, 4))
    return [*out, round(Q, 4)]


def show_hjb_reduction(rng: random.Random) -> None:
    """Print the full minus the reduced HJB expression at three random points."""
    for _ in range(3):
        S, psi, mu, q, nu, dqh, k, b = [rng.uniform(-2, 2) for _ in range(8)]
        full = nu * (S - psi / 2 - k * nu) + b * (mu - nu) * q - nu * (S - psi / 2 + dqh)
        reduced = -k * nu**2 - (b * q + dqh) * nu + b * mu * q
        print(f"HJB reduction difference {full - reduced:.1e}")


def show_riccati_and_feynman_kac() -> None:
    """Print h2(0) and h1(0) by direct integration beside their closed forms."""
    k, phi, A, b, T = 0.01, 0.001, 0.5, 0.002, 1.0
    # h2 integrated backward from h2(T) = -A by Euler.
    n, h = 200000, -A
    for _ in range(n):
        h -= (T / n) * (phi - (b + 2 * h) ** 2 / (4 * k))
    print(
        f"h2(0): ODE {h:.6f}, corrected form {-xi(0, T, k, phi, A, b) - b / 2:.6f}, "
        f"printed form {-xi(0, T, k, phi, A, b, True) - b / 2:.6f}"
    )
    print(
        f"h2(T) printed form {-xi(T, T, k, phi, A, b, True) - b / 2:.4f} (should be -A = {-A:.4f})"
    )
    m, n, h1 = 0.3, 100000, 0.0  # constant flow, so L^mu h1 = 0
    dt = T / n
    for i in range(n, 0, -1):
        h1 -= dt * (-b * m + xi(i * dt, T, k, phi, A, b) * h1 / k)
    # The Feynman-Kac integral, accumulated forward on its own.
    tot, integral = 0.0, 0.0
    for i in range(n):
        tot += math.exp(-integral / k) * m * dt
        integral += xi(i * dt, T, k, phi, A, b) * dt
    print(f"h1(0): ODE {h1:.6f}, b*FK {b * tot:.6f}, boxed without b {tot:.6f}")


def show_inventory_paths() -> None:
    """Print the inventory paths for the base case, each parameter scaled and the A-C limit."""
    print("Q at t = 0.25, 0.5, 1")
    print("  base kappa=0.01 phi=0.001 A=0.5", path(0.01, 0.001, 0.5))
    print("  phi x10                       ", path(0.01, 0.01, 0.5))
    print("  A x10                         ", path(0.01, 0.001, 5.0))
    print("  kappa x10                     ", path(0.1, 0.001, 0.5))
    g = math.sqrt(0.001 / 0.01)
    print(
        "  A=1e6                         ",
        path(0.01, 0.001, 1e6),
        "Almgren-Chriss sinh",
        [round(math.sinh(g * (1 - t)) / math.sinh(g), 4) for t in (0.25, 0.5)],
    )


def main() -> int:
    """Print the demonstration and return the exit status, always 0."""
    show_hjb_reduction(random.Random(0))
    show_riccati_and_feynman_kac()
    show_inventory_paths()
    check_wealth_identity_and_feedback()
    return 0


def wealth_sim(
    nu: Sequence[float],
    mu: Sequence[float],
    Q0: float,
    S0: float,
    b: float,
    kappa: float,
    psi: float,
    phi: float,
    A: float,
    T: float,
    printed: bool = False,
) -> tuple[float, float]:
    """Simulate the dynamics with sigma = 0 by Euler; return the realised reward and Q_T.

    Args:
        nu: Trading rate in each of the n steps.
        mu: Order flow in each step.
        Q0: Initial inventory.
        S0: Initial price.
        b: Permanent impact.
        kappa: Temporary impact.
        psi: Spread; half of it is paid on each trade.
        phi: Running inventory penalty.
        A: Terminal liquidation penalty.
        T: Horizon.
        printed: Use the printed terminal payoff Q_T(S_T - A Q_T) instead of the corrected
            Q_T(S_T - psi/2 - A Q_T).
    """
    n = len(nu)
    dt = T / n
    S, Q, X, run = S0, Q0, 0.0, 0.0
    for i in range(n):
        X += (S - psi / 2 - kappa * nu[i]) * nu[i] * dt
        run += phi * Q * Q * dt
        S += b * (mu[i] - nu[i]) * dt
        Q -= nu[i] * dt
    term = Q * (S - A * Q) if printed else Q * (S - psi / 2 - A * Q)
    return X + term - run, Q


def wealth_identity(
    nu: Sequence[float],
    mu: Sequence[float],
    Q0: float,
    S0: float,
    b: float,
    kappa: float,
    psi: float,
    phi: float,
    A: float,
    T: float,
) -> float:
    """Return the identity for the corrected reward, from the integrals alone.

    Q0 S0 - psi Q0/2 - b Q0^2/2 + b int Q mu - kappa int nu^2 - phi int Q^2 - (A - b/2) Q_T^2.
    The arguments are those of wealth_sim; no price path is simulated.
    """
    n = len(nu)
    dt = T / n
    Q, Imu, Inu, IQ = Q0, 0.0, 0.0, 0.0
    for i in range(n):
        Imu += Q * mu[i] * dt
        Inu += nu[i] ** 2 * dt
        IQ += Q * Q * dt
        Q -= nu[i] * dt
    return (
        Q0 * S0
        - psi * Q0 / 2
        - b * Q0**2 / 2
        + b * Imu
        - kappa * Inu
        - phi * IQ
        - (A - b / 2) * Q * Q
    )


def direct_optimum(
    Q0: float,
    kappa: float,
    phi: float,
    A: float,
    b: float,
    psi: float,
    T: float,
    n: int,
    printed: bool,
) -> list[float]:
    """Return the inventories Q_1..Q_n that maximise the discretised objective directly.

    The objective is -kappa sum nu^2 dt - phi sum Q_k^2 dt - (A - b/2) Q_n^2 [+ psi/2 Q_n if
    printed] (mu = sigma = 0): a concave quadratic when kappa > 0, phi >= 0 and A > b/2, with
    tridiagonal first-order conditions. It uses no closed form, so it is independent of xi.
    """
    dt = T / n
    c = kappa / dt
    a_, d_, u_, r_ = [0.0] * n, [0.0] * n, [0.0] * n, [0.0] * n
    for k in range(1, n + 1):  # d/dQ_k of the objective = 0
        i = k - 1
        if k < n:
            d_[i] = 2 * c + phi * dt
            u_[i] = -c
        else:
            d_[i] = c + phi * dt + (A - b / 2)
            r_[i] = psi / 4 if printed else 0.0
        a_[i] = -c if k > 1 else 0.0
        if k == 1:
            r_[i] += c * Q0
    # Thomas algorithm, system d Q_k + a Q_{k-1} + u Q_{k+1} = r (scaled by 1/2)
    for i in range(1, n):
        w = a_[i] / d_[i - 1]
        d_[i] -= w * u_[i - 1]
        r_[i] -= w * r_[i - 1]
    Q = [0.0] * n
    Q[-1] = r_[-1] / d_[-1]
    for i in range(n - 2, -1, -1):
        Q[i] = (r_[i] - u_[i] * Q[i + 1]) / d_[i]
    return Q


def feedback_path(
    Q0: float,
    kappa: float,
    phi: float,
    A: float,
    b: float,
    psi: float,
    T: float,
    n: int,
    printed: bool,
) -> list[float]:
    """Return the inventories Q_1..Q_n under the feedback policy, with mu = 0.

    Corrected payoff (h = H - x - q(S - psi/2)): nu* = xi q / kappa. Printed payoff
    (g = H - x - qS): nu = xi q / kappa - psi/(4 kappa) exp(-(1/kappa) int_t^T xi).
    """
    dt = T / n
    tail = [0.0] * (n + 1)
    for i in range(n - 1, -1, -1):
        tail[i] = tail[i + 1] + xi((i + 0.5) * dt, T, kappa, phi, A, b) * dt
    Q, out = Q0, []
    for i in range(n):
        t = i * dt
        nu = xi(t, T, kappa, phi, A, b) / kappa * Q
        if printed:
            nu -= psi / (4 * kappa) * math.exp(-tail[i] / kappa)
        Q -= nu * dt
        out.append(Q)
    return out


def quadrature_variance(m: int = 400) -> float:
    """Return Var int_0^1 (1 - t) B_t dt, exactly 1/20, by the midpoint rule on its covariance.

    The double integral of (1 - s)(1 - t) min(s, t) over the unit square, on an m x m grid.
    """
    dt = 1.0 / m
    return (
        sum(
            (1 - (i + 0.5) * dt) * (1 - (j + 0.5) * dt) * min(i + 0.5, j + 0.5) * dt
            for i in range(m)
            for j in range(m)
        )
        * dt
        * dt
    )


def monte_carlo_variance(rng: random.Random, paths: int = 20000, steps: int = 200) -> float:
    """Return the sample variance of int_0^1 (1 - t) B_t dt over simulated Brownian paths.

    Args:
        rng: The generator to draw the Gaussian increments from, in path order.
        paths: Number of paths.
        steps: Euler steps per path.
    """
    acc, acc2 = 0.0, 0.0
    for _ in range(paths):
        B, integral = 0.0, 0.0
        for i in range(steps):
            B += rng.gauss(0, math.sqrt(1 / steps))
            integral += (1 - (i + 1) / steps) * B / steps
        acc += integral
        acc2 += integral * integral
    return acc2 / paths - (acc / paths) ** 2


def check_wealth_identity_and_feedback() -> None:
    """Print the follow-up comparisons of 2026-10-15.

    One generator seeded with 1 supplies, in order, the trading rates, the order flow and then
    the Monte Carlo increments, so the Monte Carlo continues the same sequence.
    """
    print("--- follow-up checks (2026-10-15)")
    rng = random.Random(1)
    T, n, Q0, S0 = 1.0, 4000, 1.0, 10.0
    b, kappa, psi, phi, A = 0.1, 0.01, 0.02, 0.001, 0.08
    nu = [rng.uniform(-2, 3) for _ in range(n)]
    mu = [rng.uniform(-1, 1) for _ in range(n)]
    simulated = wealth_sim(nu, mu, Q0, S0, b, kappa, psi, phi, A, T)[0]
    identity = wealth_identity(nu, mu, Q0, S0, b, kappa, psi, phi, A, T)
    print(f"wealth identity: simulated {simulated:.6f}, identity {identity:.6f}")
    kappa, phi, A, b, psi, n = 0.01, 0.001, 0.05, 0.02, 0.01, 2000
    for printed in (False, True):
        d = direct_optimum(Q0, kappa, phi, A, b, psi, T, n, printed)
        f = feedback_path(Q0, kappa, phi, A, b, psi, T, n, printed)
        label = "printed  " if printed else "corrected"
        print(
            f"{label} payoff: Q(T/2) direct {d[n // 2 - 1]:.4f} feedback {f[n // 2 - 1]:.4f}; "
            f"Q(T) direct {d[-1]:.4f} feedback {f[-1]:.4f}"
        )
    # counterexample: T = Q0 = 1, mu = sigma = psi = 0, b = 0.1, kappa = A = 0.01, phi = 0.001,
    # nu = -M
    b, kappa, A, phi, psi = 0.1, 0.01, 0.01, 0.001, 0.0
    coef = b / 2 - kappa - A - phi / 3
    print(f"nu = -M: M^2 coefficient b/2 - kappa - A - phi/3 = {coef:.6f}")
    for M in (10, 100, 1000):
        r, _ = wealth_sim([-M] * 4000, [0.0] * 4000, 1.0, S0, b, kappa, psi, phi, A, 1.0)
        print(f"  M={M:5d} reward {r:.4e}, reward/M^2 {r / M**2:.6f}")
    A = 0.06  # sufficient regime A > b/2
    r, _ = wealth_sim([-1000] * 4000, [0.0] * 4000, 1.0, S0, b, kappa, psi, phi, A, 1.0)
    print(
        f"  A=0.06 > b/2: M=1000 reward/M^2 {r / 1e6:.6f} "
        f"(b/2 - kappa - A - phi/3 = {b / 2 - kappa - A - phi / 3:.6f})"
    )
    # variance of int_0^1 (1 - t) B_t dt: exact 1/20
    exact = quadrature_variance()
    simulated = monte_carlo_variance(rng)
    print(
        f"Var int (1-t) B_t dt: quadrature {exact:.5f}, Monte Carlo {simulated:.5f}, "
        f"1/20 = {1 / 20:.5f}"
    )


if __name__ == "__main__":
    sys.exit(main())
