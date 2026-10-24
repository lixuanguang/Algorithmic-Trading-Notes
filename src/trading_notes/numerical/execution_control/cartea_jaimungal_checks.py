"""Numerical demonstration for mod:cartea-jaimungal-execution."""

import math
import random
import sys

from trading_notes.numerical.execution_control.optimal_liquidation import (
    LiquidationModel,
    monte_carlo_variance,
    quadrature_variance,
)


def show_hjb_reduction(rng: random.Random) -> None:
    """Print the full minus the reduced HJB expression at three random points."""
    for _ in range(3):
        S, psi, mu, q, nu, dqh, k, b = [rng.uniform(-2, 2) for _ in range(8)]
        full = nu * (S - psi / 2 - k * nu) + b * (mu - nu) * q - nu * (S - psi / 2 + dqh)
        reduced = -k * nu**2 - (b * q + dqh) * nu + b * mu * q
        print(f"HJB reduction difference {full - reduced:.1e}")


def show_riccati_and_feynman_kac() -> None:
    """Print h2(0) and h1(0) by direct integration beside their closed forms."""
    model = LiquidationModel(kappa=0.01, phi=0.001, terminal=0.5, permanent=0.002, horizon=1.0)
    k, phi, A, b, T = model.kappa, model.phi, model.terminal, model.permanent, model.horizon
    # h2 integrated backward from h2(T) = -A by Euler.
    n, h = 200000, -A
    for _ in range(n):
        h -= (T / n) * (phi - (b + 2 * h) ** 2 / (4 * k))
    print(
        f"h2(0): ODE {h:.6f}, corrected form {-model.xi(0) - b / 2:.6f}, "
        f"printed form {-model.xi(0, True) - b / 2:.6f}"
    )
    print(f"h2(T) printed form {-model.xi(T, True) - b / 2:.4f} (should be -A = {-A:.4f})")
    m, n, h1 = 0.3, 100000, 0.0  # constant flow, so L^mu h1 = 0
    dt = T / n
    for i in range(n, 0, -1):
        h1 -= dt * (-b * m + model.xi(i * dt) * h1 / k)
    # The Feynman-Kac integral, accumulated forward on its own.
    tot, integral = 0.0, 0.0
    for i in range(n):
        tot += math.exp(-integral / k) * m * dt
        integral += model.xi(i * dt) * dt
    print(f"h1(0): ODE {h1:.6f}, b*FK {b * tot:.6f}, boxed without b {tot:.6f}")


def show_inventory_paths() -> None:
    """Print the inventory paths for the base case, each parameter scaled and the A-C limit."""

    def path(k: float, phi: float, A: float) -> list[float]:
        return LiquidationModel(kappa=k, phi=phi, terminal=A).inventory()

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


def show_wealth_identity_and_feedback() -> None:
    """Print the wealth identity, the two feedback policies and the counterexample.

    One generator seeded with 1 supplies, in order, the trading rates, the order flow and then
    the Monte Carlo increments, so the Monte Carlo continues the same sequence.
    """
    print("--- wealth identity, feedback policies and the unbounded counterexample")
    rng = random.Random(1)
    n, Q0, S0 = 4000, 1.0, 10.0
    model = LiquidationModel(kappa=0.01, phi=0.001, terminal=0.08, permanent=0.1, spread=0.02)
    nu = [rng.uniform(-2, 3) for _ in range(n)]
    mu = [rng.uniform(-1, 1) for _ in range(n)]
    simulated = model.wealth(nu, mu, Q0, S0)[0]
    identity = model.wealth_identity(nu, mu, Q0, S0)
    print(f"wealth identity: simulated {simulated:.6f}, identity {identity:.6f}")
    model = LiquidationModel(kappa=0.01, phi=0.001, terminal=0.05, permanent=0.02, spread=0.01)
    n = 2000
    for printed in (False, True):
        d = model.direct_optimum(Q0, n, printed)
        f = model.feedback_path(Q0, n, printed)
        label = "printed  " if printed else "corrected"
        print(
            f"{label} payoff: Q(T/2) direct {d[n // 2 - 1]:.4f} feedback {f[n // 2 - 1]:.4f}; "
            f"Q(T) direct {d[-1]:.4f} feedback {f[-1]:.4f}"
        )
    # counterexample: T = Q0 = 1, mu = sigma = psi = 0, b = 0.1, kappa = A = 0.01, phi = 0.001,
    # nu = -M
    model = LiquidationModel(kappa=0.01, phi=0.001, terminal=0.01, permanent=0.1, spread=0.0)
    b, kappa, A, phi = model.permanent, model.kappa, model.terminal, model.phi
    coef = b / 2 - kappa - A - phi / 3
    print(f"nu = -M: M^2 coefficient b/2 - kappa - A - phi/3 = {coef:.6f}")
    for M in (10, 100, 1000):
        r, _ = model.wealth([-M] * 4000, [0.0] * 4000, 1.0, S0)
        print(f"  M={M:5d} reward {r:.4e}, reward/M^2 {r / M**2:.6f}")
    model = model.model_copy(update={"terminal": 0.06})  # sufficient regime A > b/2
    A = model.terminal
    r, _ = model.wealth([-1000] * 4000, [0.0] * 4000, 1.0, S0)
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


def main() -> int:
    """Print the demonstration and return the exit status, always 0.

    Lehalle and Laruelle, app. A.7.3, pp. 281-284: the reduction of the HJB equation with the
    inventory term -nu*dqH, the Riccati solution for h2 against direct integration (the printed
    closed form gives h2(T) = A - b), the Feynman-Kac form of h1 (the boxed formula omits the
    factor b), the Almgren-Chriss limit (mu = 0, A -> infinity) and the inventory paths behind
    the parameter intuition. Then the pathwise wealth identity behind the terminal payoff
    Q_T(S_T - psi/2 - A Q_T); a direct discretised optimisation compared with the feedback
    policies for that payoff (decomposition h = H - x - q(S - psi/2)) and for the printed
    payoff (decomposition g = H - x - qS); the infinite-value counterexample nu = -M; and the
    variance of b * int Q mu dt for Q_t = 1 - t, mu_t = B_t (b^2/20).

    A demonstration, not a checker: it prints its values for comparison by eye and asserts
    nothing. Each section draws from its own seeded generator, never the shared one; standard
    library only.
    """
    show_hjb_reduction(random.Random(0))
    show_riccati_and_feynman_kac()
    show_inventory_paths()
    show_wealth_identity_and_feedback()
    return 0


if __name__ == "__main__":
    sys.exit(main())
