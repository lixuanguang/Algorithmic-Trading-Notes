"""A put on a lognormal asset: finite-difference grids, a CRR tree and simulated price paths."""

import math
from collections.abc import Container

import numpy as np
from numpy.typing import NDArray
from scipy.linalg import solve_banded

from trading_notes.numerical.option_pricing.black_scholes import BlackScholes
from trading_notes.records import Record

type Floats = NDArray[np.float64]


class PutOption(Record):
    """A put on an asset following geometric Brownian motion under the pricing measure.

    Attributes:
        strike: K.
        rate: Continuously compounded risk-free rate r.
        dividend_yield: Continuous dividend yield q.
        vol: Volatility sigma.
        maturity: T in years.
        spot: The price at which the value is read.
    """

    strike: float
    rate: float
    dividend_yield: float
    vol: float
    maturity: float
    spot: float

    def black_scholes(self) -> float:
        """Return the European value by Black-Scholes-Merton."""
        return BlackScholes(
            spot=self.spot,
            strike=self.strike,
            maturity=self.maturity,
            rate=self.rate,
            vol=self.vol,
            dividend_yield=self.dividend_yield,
        ).put()

    def crr_value(self, n: int, american: bool = True, every: int | None = None) -> float:
        """Return the value on a CRR binomial tree of n steps.

        Args:
            n: Time steps.
            american: Whether exercise is allowed after every step.
            every: For a Bermudan put, exercise only after every `every`-th step from the start.
        """
        K, S0 = self.strike, self.spot
        dt = self.maturity / n
        u = math.exp(self.vol * math.sqrt(dt))
        d = 1 / u
        p = (math.exp((self.rate - self.dividend_yield) * dt) - d) / (u - d)
        disc = math.exp(-self.rate * dt)
        j = np.arange(n + 1)
        V = np.maximum(K - S0 * u ** (n - 2 * j), 0.0)
        for step in range(n - 1, -1, -1):
            V = disc * (p * V[:-1] + (1 - p) * V[1:])
            if step > 0 and (american or (every is not None and step % every == 0)):
                j = np.arange(step + 1)
                V = np.maximum(V, K - S0 * u ** (step - 2 * j))
        return float(V[0])

    def price_paths(self, rng: np.random.Generator, n_paths: int, dates: int) -> Floats:
        """Return prices on `dates` equal steps to maturity, one row per path, exact in log."""
        dt = self.maturity / dates
        z = rng.standard_normal((n_paths, dates))
        drift = (self.rate - self.dividend_yield - self.vol**2 / 2) * dt
        prices: Floats = self.spot * np.exp(np.cumsum(drift + self.vol * math.sqrt(dt) * z, axis=1))
        return prices


class GridValues(Record):
    """Option values on a uniform price grid.

    Attributes:
        values: The value at each node.
        prices: The node prices, 0 to S_max.
    """

    values: Floats
    prices: Floats

    def at(self, s: float) -> float:
        """Return the value at the grid node nearest s."""
        return float(self.values[round(s / (self.prices[1] - self.prices[0]))])


class FiniteDifferenceGrid(Record):
    """Finite-difference schemes for a put on M + 1 price nodes over [0, S_max], in time to expiry.

    Attributes:
        option: The put.
        s_max: The upper boundary of the price grid.
    """

    option: PutOption
    s_max: float

    def coefficients(self, M: int) -> tuple[Floats, Floats, Floats, NDArray[np.bool_]]:
        """Return the coefficients on M space steps of the spatial operator.

        Spatial operator L V_i = a_i V_{i-1} + b_i V_i + c_i V_{i+1} for V_tau = L V (central).
        Where sigma^2 i < |r - q| the first derivative is upwinded (forward difference for
        r - q > 0), so that every off-diagonal coefficient is non-negative.

        Returns:
            a, b, c for the interior nodes i = 1..M-1, and which of them are upwinded.
        """
        r, q, sg = self.option.rate, self.option.dividend_yield, self.option.vol
        i = np.arange(1, M, dtype=float)
        a = 0.5 * (sg**2 * i**2 - (r - q) * i)
        b = -(sg**2 * i**2 + r)
        c = 0.5 * (sg**2 * i**2 + (r - q) * i)
        up = sg**2 * i < abs(r - q)
        if r - q > 0:
            a[up] = 0.5 * sg**2 * i[up] ** 2
            b[up] = -(sg**2 * i[up] ** 2 + (r - q) * i[up] + r)
            c[up] = 0.5 * sg**2 * i[up] ** 2 + (r - q) * i[up]
        return a, b, c, up

    def boundaries(self, tau: float, american: bool) -> tuple[float, float]:
        """Return the values at S = 0 and S = S_max with time tau to maturity."""
        K = self.option.strike
        return (K if american else K * math.exp(-self.option.rate * tau)), 0.0

    def payoff(self, M: int) -> GridValues:
        """Return the exercise value max(K - S, 0) on M space steps."""
        S = np.arange(M + 1, dtype=np.float64) * (self.s_max / M)
        return GridValues(values=np.maximum(self.option.strike - S, 0.0), prices=S)

    def explicit(
        self, M: int, N: int, american: bool = False
    ) -> tuple[GridValues, tuple[Floats, Floats, Floats]]:
        """Explicit scheme V^{n+1}_i = A_i V^n_{i-1} + B_i V^n_i + C_i V^n_{i+1}.

        Returns:
            The values at time 0, and the coefficients (A, B, C).
        """
        dt = self.option.maturity / N
        start = self.payoff(M)
        a, b, c, _ = self.coefficients(M)
        A, B, C = dt * a, 1 + dt * b, dt * c
        V = start.values
        pay = V.copy()
        for n in range(N):
            new = V.copy()
            new[1:-1] = A * V[:-2] + B * V[1:-1] + C * V[2:]
            new[0], new[-1] = self.boundaries((n + 1) * dt, american)
            V = np.maximum(new, pay) if american else new
        return GridValues(values=V, prices=start.prices), (A, B, C)

    def crank_nicolson(
        self, M: int, N: int, american: bool = False, exercise_steps: Container[int] | None = None
    ) -> GridValues:
        """Crank-Nicolson with a Rannacher start (four implicit half-steps replace the first two).

        Args:
            M: Space steps on [0, S_max].
            N: Time steps.
            american: Whether to solve the full LCP by projected SOR at every step.
            exercise_steps: If given, the step indices n (1..N, in time to maturity) after which
                exercise is allowed by projection (a Bermudan option).

        Returns:
            The values at time 0.
        """
        dt = self.option.maturity / N
        start = self.payoff(M)
        a, b, c, _ = self.coefficients(M)
        pay = start.values
        V = pay.copy()
        tau = 0.0
        for n in range(1, N + 1):
            if n <= 2:
                for _ in range(2):
                    tau += dt / 2
                    V = self._theta_step(V, dt / 2, 1.0, (a, b, c), tau, american, pay)
            else:
                tau += dt
                V = self._theta_step(V, dt, 0.5, (a, b, c), tau, american, pay)
            if exercise_steps is not None and n in exercise_steps:
                V = np.maximum(V, pay)
        return GridValues(values=V, prices=start.prices)

    def _theta_step(
        self,
        V: Floats,
        dt: float,
        theta: float,
        operator: tuple[Floats, Floats, Floats],
        tau_new: float,
        american: bool,
        pay: Floats,
        omega: float = 1.5,
        tol: float = 1e-9,
    ) -> Floats:
        """One theta-scheme step: (I - theta dt L) V_new = (I + (1 - theta) dt L) V_old.

        The boundary values enter the first and last equations. An American step solves the
        linear complementarity problem by projected SOR (relaxation omega, stopping when no
        value moves by tol, at most 100,000 sweeps), started from the previous values.
        """
        a, b, c = operator
        m = len(a)
        rhs = V[1:-1] + (1 - theta) * dt * (a * V[:-2] + b * V[1:-1] + c * V[2:])
        lo, hi = self.boundaries(tau_new, american)
        rhs[0] += theta * dt * a[0] * lo
        rhs[-1] += theta * dt * c[-1] * hi
        sub, diag, sup = -theta * dt * a, 1 - theta * dt * b, -theta * dt * c
        if not american:
            ab = np.zeros((3, m))
            ab[0, 1:], ab[1], ab[2, :-1] = sup[:-1], diag, sub[1:]
            x = solve_banded((1, 1), ab, rhs)
        else:
            x = np.maximum(V[1:-1].copy(), pay[1:-1])
            g = pay[1:-1]
            for _ in range(100_000):
                change = 0.0
                for j in range(m):
                    left = sub[j] * x[j - 1] if j > 0 else 0.0
                    right = sup[j] * x[j + 1] if j < m - 1 else 0.0
                    y = (rhs[j] - left - right) / diag[j]
                    xn = max(x[j] + omega * (y - x[j]), g[j])
                    change = max(change, abs(xn - x[j]))
                    x[j] = xn
                if change < tol:
                    break
        out = np.empty_like(V)
        out[1:-1], out[0], out[-1] = x, lo, hi
        return out
