"""Heston, Merton jump-diffusion and SABR option models, and Carr-Madan FFT pricing."""

import math
from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]
type Complexes = NDArray[np.complex128]


def normal_cdf(x: float) -> float:
    """Return the standard normal CDF by erfc."""
    return 0.5 * math.erfc(-x / math.sqrt(2))


def variance_call(S: float, K: float, T: float, r: float, v: float) -> float:
    """Return the Black-Scholes call at variance rate v (volatility squared), no dividends."""
    s = math.sqrt(v * T)
    d1 = (math.log(S / K) + r * T + 0.5 * v * T) / s
    return S * normal_cdf(d1) - K * math.exp(-r * T) * normal_cdf(d1 - s)


class HestonModel(Record):
    """Heston's (1993) stochastic variance, dv = kappa (theta - v) dt + sigma sqrt(v) dW.

    The market price of volatility risk is zero (lambda = 0).

    Attributes:
        kappa: Speed of mean reversion of the variance.
        theta: Long-run variance.
        sigma: Volatility of the variance.
        rho: Correlation of the variance and stock shocks.
        v0: Initial variance.
    """

    kappa: float
    theta: float
    sigma: float
    rho: float
    v0: float

    def characteristic(
        self, phi: Floats | Complexes, j: int, x: float, T: float, r: float
    ) -> Complexes:
        """Return Heston's characteristic function f_j (eqs. 17-18) at phi.

        Args:
            phi: Transform arguments, real or complex.
            j: 1 or 2, giving u_1 = 1/2, b_1 = kappa - rho sigma or u_2 = -1/2, b_2 = kappa.
            x: Log of the stock price.
            T: Time to expiry in years.
            r: Continuously compounded rate.
        """
        kappa, theta, sigma, rho, v = self.kappa, self.theta, self.sigma, self.rho, self.v0
        u, b = (0.5, kappa - rho * sigma) if j == 1 else (-0.5, kappa)
        a = kappa * theta
        d = np.sqrt((rho * sigma * phi * 1j - b) ** 2 - sigma**2 * (2 * u * phi * 1j - phi**2))
        g = (b - rho * sigma * phi * 1j + d) / (b - rho * sigma * phi * 1j - d)
        e = np.exp(d * T)
        C = r * phi * 1j * T + a / sigma**2 * (
            (b - rho * sigma * phi * 1j + d) * T - 2 * np.log((1 - g * e) / (1 - g))
        )
        D = (b - rho * sigma * phi * 1j + d) / sigma**2 * ((1 - e) / (1 - g * e))
        f: Complexes = np.exp(C + D * v + 1j * phi * x)
        return f

    def call(self, S: float, K: float, T: float, r: float) -> float:
        """Return the call S P1 - K e^(-rT) P2, by trapezoidal quadrature on [1e-6, 200]."""
        phi = np.linspace(1e-6, 200, 40001)
        P = []
        for j in (1, 2):
            f = self.characteristic(phi, j, math.log(S), T, r)
            integ = np.real(np.exp(-1j * phi * math.log(K)) * f / (1j * phi))
            P.append(0.5 + np.trapezoid(integ, phi) / math.pi)
        call: float = S * P[0] - K * math.exp(-r * T) * P[1]
        return call


def carr_madan(
    cf: Callable[[Complexes], Complexes],
    S: float,
    T: float,
    r: float,
    alpha: float = 1.5,
    N: int = 4096,
    eta: float = 0.25,
) -> tuple[Floats, Floats]:
    """Return strikes and call prices by the FFT of the damped call, with Simpson weights.

    Args:
        cf: Characteristic function of the log terminal price.
        S: Stock price; the strike grid is centred on log-strike 0.
        T: Time to expiry in years.
        r: Continuously compounded rate.
        alpha: Damping exponent; E[S_T^(alpha + 1)] must be finite.
        N: Number of FFT points.
        eta: Spacing of the transform grid.
    """
    lam = 2 * math.pi / (N * eta)
    bnd = N * lam / 2
    v = np.arange(N) * eta
    # The damped call's transform is evaluated at v - (alpha + 1) i, a complex128 array.
    u = np.asarray(v - (alpha + 1) * 1j, dtype=np.complex128)
    psi = math.exp(-r * T) * cf(u) / (alpha**2 + alpha - v**2 + 1j * (2 * alpha + 1) * v)
    w = eta / 3 * (3 + (-1) ** (np.arange(N) + 1) - (np.arange(N) == 0))
    k = -bnd + lam * np.arange(N)
    y = np.fft.fft(np.exp(1j * bnd * v) * psi * w)
    return np.exp(k), np.exp(-alpha * k) / math.pi * np.real(y)


class MertonJumpDiffusion(Record):
    """Merton's (1976) diffusion with Poisson lognormal jumps of mean one (k = 0).

    Attributes:
        variance: Diffusion variance rate sigma^2.
        intensity: Jump intensity lambda a year.
        jump_variance: Variance delta^2 of the log jump size.
    """

    variance: float
    intensity: float
    jump_variance: float

    def call(self, S: float, K: float, T: float, r: float, nmax: int = 60) -> float:
        """Return the call by Merton's series of Black-Scholes prices, to nmax terms."""
        lam, s2, d2 = self.intensity, self.variance, self.jump_variance
        return sum(
            math.exp(-lam * T)
            * (lam * T) ** k
            / math.factorial(k)
            * variance_call(S, K, T, r, s2 + k * d2 / T)
            for k in range(nmax)
        )


class SabrModel(Record):
    """SABR dynamics dF = a F^b dW1, da = nu a dW2, corr rho (Hagan et al., 2002).

    Attributes:
        alpha: Initial volatility a.
        beta: CEV exponent b.
        rho: Correlation of the two shocks.
        nu: Volatility of volatility.
    """

    alpha: float
    beta: float
    rho: float
    nu: float

    def implied_vol(self, F: float, K: float, T: float) -> float:
        """Return the lognormal implied-volatility expansion at forward F and strike K."""
        a, b, rho, nu = self.alpha, self.beta, self.rho, self.nu
        if abs(F - K) < 1e-12:
            zx = 1.0
            lfk = 0.0
        else:
            lfk = math.log(F / K)
            z = nu / a * (F * K) ** ((1 - b) / 2) * lfk
            zx = (
                z / math.log((math.sqrt(1 - 2 * rho * z + z * z) + z - rho) / (1 - rho))
                if nu > 0
                else 1.0
            )
        A = (
            1
            + (
                (1 - b) ** 2 * a * a / (24 * (F * K) ** (1 - b))
                + a * b * nu * rho / (4 * (F * K) ** ((1 - b) / 2))
                + nu * nu * (2 - 3 * rho * rho) / 24
            )
            * T
        )
        B = (F * K) ** ((1 - b) / 2) * (
            1 + (1 - b) ** 2 / 24 * lfk**2 + (1 - b) ** 4 / 1920 * lfk**4
        )
        vol: float = a / B * zx * A
        return vol
