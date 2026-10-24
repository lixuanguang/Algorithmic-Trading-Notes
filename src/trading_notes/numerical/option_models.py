"""Own checks behind the Heston, Merton jump-diffusion and SABR entries.

Derivatives and empirical validation (2026-10-17): own checks behind
mod:heston-stochastic-volatility, mod:merton-jump-diffusion and mod:sabr-smile. Parameters are
invented; nothing here is market data.

1. Heston (1993), eqs. (10), (17)-(18): call = S P1 - K e^{-rT} P2,
   P_j = 1/2 + (1/pi) int_0^inf Re[e^{-i phi ln K} f_j / (i phi)] dphi, with u1 = 1/2,
   u2 = -1/2, a = kappa theta, b1 = kappa - rho sigma, b2 = kappa (lambda = 0).
   Checks: (a) with a tiny vol of vol and v0 = theta it equals Black-Scholes at sqrt(theta);
   (b) it matches an Euler (full truncation) Monte Carlo within three standard errors at
   T = 0.5.
2. Carr and Madan (1999), eqs. (5)-(6), condition (7) E[S_T^{alpha+1}] < inf: FFT of the damped
   call, alpha = 1.5, N = 4096, eta = 0.25, Simpson weights. Checks: Black-Scholes prices
   across strikes; Heston prices against check 1.
3. Merton (Sloan WP 787-75), eqs. (15), (18)-(19): lognormal jumps with E[Y] = 1 (k = 0),
   F = sum_n e^{-lam T}(lam T)^n / n! * BS(S, T; K, sigma^2 + n delta^2 / T, r). Checks:
   lam = 0 gives Black-Scholes; dF/dlam > 0 at lam = 0 (sec. IV); Monte Carlo agreement.
4. SABR (Hagan et al. 2002 as restated by Bianchetti and Carlicchi, Table 5): the lognormal
   implied-volatility expansion. Checks: continuity at the money (z/x(z) -> 1); with nu = 0 and
   beta = 1 it is flat at alpha; against a Monte Carlo of the SABR dynamics at moderate
   parameters, within a stated tolerance of an asymptotic formula.
One generator, seeded 20261017, serves the Heston, Merton and SABR simulations in order.
Run: uv run --frozen --no-editable python -m trading_notes.numerical.option_models (numpy).
Exits 1 on failure.
"""

# standard library imports
import math
import sys
from collections.abc import Callable
from typing import Final

# third party library imports
import numpy as np
from numpy.typing import NDArray

# project library imports
from trading_notes.numerical.report import CheckReport

type Floats = NDArray[np.float64]
type Complexes = NDArray[np.complex128]

SEED: Final = 20261017
S0: Final = 100.0
R: Final = 0.02
MATURITY: Final = 0.5
# Heston parameters of the Monte Carlo and FFT checks.
KAP: Final = 1.5
THETA: Final = 0.04
SIG: Final = 0.5
RHO: Final = -0.7
V0: Final = 0.04
N_PATHS: Final = 200000  # Heston and Merton paths


def ncdf(x: float) -> float:
    """Return the standard normal CDF by erfc."""
    return 0.5 * math.erfc(-x / math.sqrt(2))


def bs(S: float, K: float, T: float, r: float, v: float) -> float:
    """Return the Black-Scholes call at variance v."""
    s = math.sqrt(v * T)
    d1 = (math.log(S / K) + r * T + 0.5 * v * T) / s
    return S * ncdf(d1) - K * math.exp(-r * T) * ncdf(d1 - s)


def heston_f(
    phi: Floats | Complexes,
    j: int,
    x: float,
    v: float,
    T: float,
    r: float,
    kappa: float,
    theta: float,
    sigma: float,
    rho: float,
) -> Complexes:
    """Return Heston's characteristic function f_j at phi."""
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


def heston_call(
    S: float,
    K: float,
    T: float,
    r: float,
    v0: float,
    kappa: float,
    theta: float,
    sigma: float,
    rho: float,
) -> float:
    """Return the Heston call by trapezoidal quadrature of P1 and P2 on [1e-6, 200]."""
    phi = np.linspace(1e-6, 200, 40001)
    P = []
    for j in (1, 2):
        f = heston_f(phi, j, math.log(S), v0, T, r, kappa, theta, sigma, rho)
        integ = np.real(np.exp(-1j * phi * math.log(K)) * f / (1j * phi))
        P.append(0.5 + np.trapezoid(integ, phi) / math.pi)
    call: float = S * P[0] - K * math.exp(-r * T) * P[1]
    return call


def check_heston(report: CheckReport, rng: np.random.Generator) -> None:
    """1. The Heston formula against Black-Scholes and against an Euler Monte Carlo."""
    print("== 1. Heston closed form")
    r, T = R, MATURITY
    th = 0.04
    for K in (90, 100, 110):
        h, b = heston_call(S0, K, T, r, th, 2.0, th, 1e-4, -0.5), bs(S0, K, T, r, th)
        report.ok(
            f"tiny vol of vol equals Black-Scholes to 1e-3 (quadrature on [0, 200]), K = {K}",
            abs(h - b) < 1e-3,
            f"{h:.5f} vs {b:.5f}",
        )
    kap, theta, sig, rho, v0, n = KAP, THETA, SIG, RHO, V0, N_PATHS
    steps = 200
    dt = T / steps
    x = np.full(n, math.log(S0))
    v = np.full(n, v0)
    for _ in range(steps):
        z1 = rng.standard_normal(n)
        z2 = rho * z1 + math.sqrt(1 - rho**2) * rng.standard_normal(n)
        vp = np.maximum(v, 0)
        x += (r - 0.5 * vp) * dt + np.sqrt(vp * dt) * z1
        v += kap * (theta - vp) * dt + sig * np.sqrt(vp * dt) * z2
    ST = np.exp(x)
    for K in (90, 100, 110):
        pay = math.exp(-r * T) * np.maximum(ST - K, 0)
        h = heston_call(S0, K, T, r, v0, kap, theta, sig, rho)
        report.ok(
            f"Heston formula vs Monte Carlo, K = {K}",
            bool(abs(h - pay.mean()) < 3 * pay.std() / math.sqrt(n) + 0.02),
            f"{h:.4f} vs {pay.mean():.4f} (s.e. {pay.std() / math.sqrt(n):.4f})",
        )


def carr_madan(
    cf: Callable[[Complexes], Complexes],
    S: float,
    T: float,
    r: float,
    alpha: float = 1.5,
    N: int = 4096,
    eta: float = 0.25,
) -> tuple[Floats, Floats]:
    """Return strikes and call prices by the FFT of the damped call, with Simpson weights."""
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


def check_carr_madan(report: CheckReport) -> None:
    """2. The FFT against Black-Scholes and against the Heston integral."""
    print("== 2. Carr-Madan FFT")
    r, T = R, MATURITY
    vol = 0.25

    def cf_bs(u: Complexes) -> Complexes:
        c: Complexes = np.exp(
            1j * u * (math.log(S0) + (r - 0.5 * vol**2) * T) - 0.5 * vol**2 * u**2 * T
        )
        return c

    Ks, Cs = carr_madan(cf_bs, S0, T, r)
    err = max(abs(np.interp(K, Ks, Cs) - bs(S0, K, T, r, vol**2)) for K in (80, 90, 100, 110, 120))
    report.ok(
        "FFT reproduces Black-Scholes across strikes 80-120",
        bool(err < 0.01),
        f"max abs error {err:.5f}",
    )

    def cf_h(u: Complexes) -> Complexes:
        return heston_f(u, 2, math.log(S0), V0, T, r, KAP, THETA, SIG, RHO)

    Ks, Cs = carr_madan(cf_h, S0, T, r)
    err = max(
        abs(np.interp(K, Ks, Cs) - heston_call(S0, K, T, r, V0, KAP, THETA, SIG, RHO))
        for K in (90, 100, 110)
    )
    report.ok(
        "FFT with the Heston characteristic function matches the integral",
        bool(err < 0.02),
        f"max abs error {err:.5f}",
    )


def merton(
    S: float, K: float, T: float, r: float, s2: float, lam: float, d2: float, nmax: int = 60
) -> float:
    """Return Merton's series for the call with lognormal jumps, E[Y] = 1, to nmax terms."""
    return sum(
        math.exp(-lam * T) * (lam * T) ** k / math.factorial(k) * bs(S, K, T, r, s2 + k * d2 / T)
        for k in range(nmax)
    )


def check_merton(report: CheckReport, rng: np.random.Generator) -> None:
    """3. Merton's series at lambda = 0, its slope in lambda, and against a Monte Carlo."""
    print("== 3. Merton jump-diffusion (lognormal jumps, E[Y] = 1)")
    r, T, n = R, MATURITY, N_PATHS
    s2, d2 = 0.04, 0.02
    report.ok(
        "lambda = 0 gives Black-Scholes",
        abs(merton(S0, 100, T, r, s2, 0.0, d2) - bs(S0, 100, T, r, s2)) < 1e-12,
    )
    eps = 1e-4
    for K in (80, 100, 120):
        report.ok(
            f"dF/dlambda > 0 at lambda = 0, K = {K}",
            merton(S0, K, T, r, s2, eps, d2) > merton(S0, K, T, r, s2, 0, d2),
        )
    lam = 1.0
    Nj = rng.poisson(lam * T, n)
    # product of n lognormals with E[Y] = 1
    logY = -0.5 * d2 * Nj + math.sqrt(d2) * np.sqrt(Nj) * rng.standard_normal(n)
    ST = S0 * np.exp((r - 0.5 * s2) * T + math.sqrt(s2 * T) * rng.standard_normal(n) + logY)
    for K in (90, 100, 110):
        pay = math.exp(-r * T) * np.maximum(ST - K, 0)
        m = merton(S0, K, T, r, s2, lam, d2)
        report.ok(
            f"Merton series vs Monte Carlo, K = {K}",
            bool(abs(m - pay.mean()) < 3 * pay.std() / math.sqrt(n)),
            f"{m:.4f} vs {pay.mean():.4f}",
        )


def sabr_vol(F: float, K: float, T: float, a: float, b: float, rho: float, nu: float) -> float:
    """Return the SABR lognormal implied-volatility expansion."""
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
    B = (F * K) ** ((1 - b) / 2) * (1 + (1 - b) ** 2 / 24 * lfk**2 + (1 - b) ** 4 / 1920 * lfk**4)
    vol: float = a / B * zx * A
    return vol


def check_sabr(report: CheckReport, rng: np.random.Generator) -> None:
    """4. The expansion's limits, and against a Monte Carlo of the dynamics, by bisection."""
    print("== 4. SABR expansion")
    F, Te = 0.03, 1.0
    a, b, rh, nu = 0.03**0.5 * 0.2, 0.5, -0.3, 0.4
    atm = sabr_vol(F, F, Te, a, b, rh, nu)
    near = sabr_vol(F, F * (1 + 1e-7), Te, a, b, rh, nu)
    report.ok("continuous at the money", abs(atm - near) < 1e-6, f"{atm:.6f} vs {near:.6f}")
    report.ok(
        "nu = 0, beta = 1 gives a flat smile at alpha",
        all(abs(sabr_vol(F, K, Te, 0.2, 1, 0, 0) - 0.2) < 1e-12 for K in (0.02, 0.03, 0.04)),
    )
    m, steps = 100000, 250
    dtt = Te / steps
    f = np.full(m, F)
    al = np.full(m, a)
    for _ in range(steps):
        z1 = rng.standard_normal(m)
        z2 = rh * z1 + math.sqrt(1 - rh * rh) * rng.standard_normal(m)
        f = np.maximum(f + al * np.maximum(f, 0) ** b * math.sqrt(dtt) * z1, 1e-12)
        al = al * np.exp(nu * math.sqrt(dtt) * z2 - 0.5 * nu * nu * dtt)
    for K in (0.025, 0.03, 0.035):
        mc = np.maximum(f - K, 0).mean()
        lo, hi = 1e-4, 2.0
        for _ in range(80):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if bs(F, K, Te, 0.0, mid * mid) < mc else (lo, mid)
        report.ok(
            f"expansion within 2 vol points of Monte Carlo, K = {K}",
            abs(sabr_vol(F, K, Te, a, b, rh, nu) - lo) < 0.02,
            f"formula {sabr_vol(F, K, Te, a, b, rh, nu) * 100:.2f}% vs MC-implied {lo * 100:.2f}%",
        )


def main() -> int:
    """Run the four parts with one report, the simulations drawing from one generator in turn.

    Returns:
        The exit status, 0 or 1.
    """
    rng = np.random.default_rng(SEED)
    report = CheckReport()
    check_heston(report, rng)
    check_carr_madan(report)
    check_merton(report, rng)
    check_sabr(report, rng)
    if report.failures:
        print("\nFAILED:", report.failures)
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
