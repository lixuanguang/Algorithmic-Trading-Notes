"""Cartea and Jaimungal's optimal liquidation: the Riccati feedback and its discretised checks."""

import math
import random
from collections.abc import Sequence

from trading_notes.records import Record


class LiquidationModel(Record):
    """Liquidation with temporary and permanent impact, a running and a terminal penalty.

    Lehalle and Laruelle, app. A.7.3, pp. 281-284. Parameters are in consistent units.

    Attributes:
        kappa: Temporary impact.
        phi: Running inventory penalty.
        terminal: A, the terminal liquidation penalty.
        permanent: b, the permanent impact.
        horizon: T.
        spread: psi; half of it is paid on each trade.
    """

    kappa: float
    phi: float
    terminal: float
    permanent: float = 0.0
    horizon: float = 1.0
    spread: float = 0.0

    def xi(self, t: float, printed: bool = False) -> float:
        """Return the Riccati feedback coefficient at time t, corrected or as printed.

        Args:
            t: Time.
            printed: Use the printed closed form, with zeta inverted and exponent
                +2 gamma (T - t).
        """
        k, phi, T = self.kappa, self.phi, self.horizon
        g, r, s = math.sqrt(phi / k), self.terminal - self.permanent / 2, math.sqrt(k * phi)
        if printed:
            z = (r + s) / (r - s)
            E = z * math.exp(2 * g * (T - t))
        else:
            z = (r - s) / (r + s)
            E = z * math.exp(-2 * g * (T - t))
        return s * (1 + E) / (1 - E)

    def inventory(self, n: int = 20000) -> list[float]:
        """Return the inventory Q at T/4, T/2 and T under the corrected feedback, to 4 decimals.

        Q starts at 1 and is stepped forward by Euler with n steps.
        """
        Q, dt, out = 1.0, self.horizon / n, []
        for i in range(n):
            Q -= dt * self.xi(i * dt) / self.kappa * Q
            if i + 1 in (n // 4, n // 2):
                out.append(round(Q, 4))
        return [*out, round(Q, 4)]

    def wealth(
        self,
        nu: Sequence[float],
        mu: Sequence[float],
        Q0: float,
        S0: float,
        printed: bool = False,
    ) -> tuple[float, float]:
        """Simulate the dynamics with sigma = 0 by Euler; return the realised reward and Q_T.

        Args:
            nu: Trading rate in each of the n steps.
            mu: Order flow in each step.
            Q0: Initial inventory.
            S0: Initial price.
            printed: Use the printed terminal payoff Q_T(S_T - A Q_T) instead of the corrected
                Q_T(S_T - psi/2 - A Q_T).
        """
        b, kappa, psi, phi, A = self.permanent, self.kappa, self.spread, self.phi, self.terminal
        n = len(nu)
        dt = self.horizon / n
        S, Q, X, run = S0, Q0, 0.0, 0.0
        for i in range(n):
            X += (S - psi / 2 - kappa * nu[i]) * nu[i] * dt
            run += phi * Q * Q * dt
            S += b * (mu[i] - nu[i]) * dt
            Q -= nu[i] * dt
        term = Q * (S - A * Q) if printed else Q * (S - psi / 2 - A * Q)
        return X + term - run, Q

    def wealth_identity(
        self, nu: Sequence[float], mu: Sequence[float], Q0: float, S0: float
    ) -> float:
        """Return the identity for the corrected reward, from the integrals alone.

        Q0 S0 - psi Q0/2 - b Q0^2/2 + b int Q mu - kappa int nu^2 - phi int Q^2 - (A - b/2)
        Q_T^2. The arguments are those of `wealth`; no price path is simulated.
        """
        b, kappa, psi, phi, A = self.permanent, self.kappa, self.spread, self.phi, self.terminal
        n = len(nu)
        dt = self.horizon / n
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

    def direct_optimum(self, Q0: float, n: int, printed: bool) -> list[float]:
        """Return the inventories Q_1..Q_n that maximise the discretised objective directly.

        The objective is -kappa sum nu^2 dt - phi sum Q_k^2 dt - (A - b/2) Q_n^2 [+ psi/2 Q_n
        if printed] (mu = sigma = 0): a concave quadratic when kappa > 0, phi >= 0 and A > b/2,
        with tridiagonal first-order conditions. It uses no closed form, so it is independent
        of xi.
        """
        kappa, phi, A, b, psi = self.kappa, self.phi, self.terminal, self.permanent, self.spread
        dt = self.horizon / n
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

    def feedback_path(self, Q0: float, n: int, printed: bool) -> list[float]:
        """Return the inventories Q_1..Q_n under the feedback policy, with mu = 0.

        Corrected payoff (h = H - x - q(S - psi/2)): nu* = xi q / kappa. Printed payoff
        (g = H - x - qS): nu = xi q / kappa - psi/(4 kappa) exp(-(1/kappa) int_t^T xi).
        """
        kappa, psi = self.kappa, self.spread
        dt = self.horizon / n
        tail = [0.0] * (n + 1)
        for i in range(n - 1, -1, -1):
            tail[i] = tail[i + 1] + self.xi((i + 0.5) * dt) * dt
        Q, out = Q0, []
        for i in range(n):
            t = i * dt
            nu = self.xi(t) / kappa * Q
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
