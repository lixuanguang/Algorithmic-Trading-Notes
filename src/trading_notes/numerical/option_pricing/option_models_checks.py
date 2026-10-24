"""Heston, Carr-Madan FFT, Merton jump-diffusion and SABR formulas against limits and simulation."""

import math
import sys
from typing import Final

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.option_pricing.stochastic_models import (
    HestonModel,
    MertonJumpDiffusion,
    SabrModel,
    carr_madan,
    variance_call,
)
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


def check_heston(report: CheckReport, rng: np.random.Generator) -> None:
    """Check The Heston formula against Black-Scholes and against an Euler Monte Carlo."""
    print("== 1. Heston closed form")
    r, T = R, MATURITY
    th = 0.04
    for K in (90, 100, 110):
        h, b = (
            HestonModel(kappa=2.0, theta=th, sigma=1e-4, rho=-0.5, v0=th).call(S0, K, T, r),
            variance_call(S0, K, T, r, th),
        )
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
        h = HestonModel(kappa=kap, theta=theta, sigma=sig, rho=rho, v0=v0).call(S0, K, T, r)
        report.ok(
            f"Heston formula vs Monte Carlo, K = {K}",
            bool(abs(h - pay.mean()) < 3 * pay.std() / math.sqrt(n) + 0.02),
            f"{h:.4f} vs {pay.mean():.4f} (s.e. {pay.std() / math.sqrt(n):.4f})",
        )


def check_carr_madan(report: CheckReport) -> None:
    """Check The FFT against Black-Scholes and against the Heston integral."""
    print("== 2. Carr-Madan FFT")
    r, T = R, MATURITY
    vol = 0.25

    def cf_bs(u: Complexes) -> Complexes:
        c: Complexes = np.exp(
            1j * u * (math.log(S0) + (r - 0.5 * vol**2) * T) - 0.5 * vol**2 * u**2 * T
        )
        return c

    Ks, Cs = carr_madan(cf_bs, S0, T, r)
    err = max(
        abs(np.interp(K, Ks, Cs) - variance_call(S0, K, T, r, vol**2))
        for K in (80, 90, 100, 110, 120)
    )
    report.ok(
        "FFT reproduces Black-Scholes across strikes 80-120",
        bool(err < 0.01),
        f"max abs error {err:.5f}",
    )

    def cf_h(u: Complexes) -> Complexes:
        return HestonModel(kappa=KAP, theta=THETA, sigma=SIG, rho=RHO, v0=V0).characteristic(
            u, 2, math.log(S0), T, r
        )

    Ks, Cs = carr_madan(cf_h, S0, T, r)
    err = max(
        abs(
            np.interp(K, Ks, Cs)
            - HestonModel(kappa=KAP, theta=THETA, sigma=SIG, rho=RHO, v0=V0).call(S0, K, T, r)
        )
        for K in (90, 100, 110)
    )
    report.ok(
        "FFT with the Heston characteristic function matches the integral",
        bool(err < 0.02),
        f"max abs error {err:.5f}",
    )


def check_merton(report: CheckReport, rng: np.random.Generator) -> None:
    """Check Merton's series at lambda = 0, its slope in lambda, and against a Monte Carlo."""
    print("== 3. Merton jump-diffusion (lognormal jumps, E[Y] = 1)")
    r, T, n = R, MATURITY, N_PATHS
    s2, d2 = 0.04, 0.02
    report.ok(
        "lambda = 0 gives Black-Scholes",
        abs(
            MertonJumpDiffusion(variance=s2, intensity=0.0, jump_variance=d2).call(S0, 100, T, r)
            - variance_call(S0, 100, T, r, s2)
        )
        < 1e-12,
    )
    eps = 1e-4
    for K in (80, 100, 120):
        report.ok(
            f"dF/dlambda > 0 at lambda = 0, K = {K}",
            MertonJumpDiffusion(variance=s2, intensity=eps, jump_variance=d2).call(S0, K, T, r)
            > MertonJumpDiffusion(variance=s2, intensity=0, jump_variance=d2).call(S0, K, T, r),
        )
    lam = 1.0
    Nj = rng.poisson(lam * T, n)
    # product of n lognormals with E[Y] = 1
    logY = -0.5 * d2 * Nj + math.sqrt(d2) * np.sqrt(Nj) * rng.standard_normal(n)
    ST = S0 * np.exp((r - 0.5 * s2) * T + math.sqrt(s2 * T) * rng.standard_normal(n) + logY)
    for K in (90, 100, 110):
        pay = math.exp(-r * T) * np.maximum(ST - K, 0)
        m = MertonJumpDiffusion(variance=s2, intensity=lam, jump_variance=d2).call(S0, K, T, r)
        report.ok(
            f"Merton series vs Monte Carlo, K = {K}",
            bool(abs(m - pay.mean()) < 3 * pay.std() / math.sqrt(n)),
            f"{m:.4f} vs {pay.mean():.4f}",
        )


def check_sabr(report: CheckReport, rng: np.random.Generator) -> None:
    """Check the expansion's limits, and against a Monte Carlo of the dynamics, by bisection."""
    print("== 4. SABR expansion")
    F, Te = 0.03, 1.0
    a, b, rh, nu = 0.03**0.5 * 0.2, 0.5, -0.3, 0.4
    sabr = SabrModel(alpha=a, beta=b, rho=rh, nu=nu)
    atm = sabr.implied_vol(F, F, Te)
    near = sabr.implied_vol(F, F * (1 + 1e-7), Te)
    report.ok("continuous at the money", abs(atm - near) < 1e-6, f"{atm:.6f} vs {near:.6f}")
    report.ok(
        "nu = 0, beta = 1 gives a flat smile at alpha",
        all(
            abs(SabrModel(alpha=0.2, beta=1, rho=0, nu=0).implied_vol(F, K, Te) - 0.2) < 1e-12
            for K in (0.02, 0.03, 0.04)
        ),
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
            lo, hi = (mid, hi) if variance_call(F, K, Te, 0.0, mid * mid) < mc else (lo, mid)
        report.ok(
            f"expansion within 2 vol points of Monte Carlo, K = {K}",
            abs(sabr.implied_vol(F, K, Te) - lo) < 0.02,
            f"formula {sabr.implied_vol(F, K, Te) * 100:.2f}% vs MC-implied {lo * 100:.2f}%",
        )


def main() -> int:
    """Run the four parts with one report, the simulations drawing from one generator in turn.

    Parameters are invented; nothing here is market data.

    1. Heston (1993), eqs. (10), (17)-(18): with a tiny vol of vol and v0 = theta it equals
       Black-Scholes at sqrt(theta), and it matches an Euler (full truncation) Monte Carlo within
       three standard errors at T = 0.5.
    2. Carr and Madan (1999), eqs. (5)-(7): the FFT of the damped call (alpha = 1.5, N = 4096,
       eta = 0.25, Simpson weights) against Black-Scholes and Heston prices.
    3. Merton (Sloan WP 787-75), eqs. (15), (18)-(19): lambda = 0 gives Black-Scholes,
       dF/dlambda > 0 at 0, and Monte Carlo agreement.
    4. SABR (Hagan et al. 2002, as restated by Bianchetti and Carlicchi, Table 5): continuity at
       the money, a flat smile at alpha with nu = 0 and beta = 1, and a Monte Carlo of the
       dynamics within a stated tolerance of the asymptotic formula.

    One generator, seeded 20261017, serves the simulations in order.

    Returns:
        The exit status, 0 or 1.
    """
    rng = np.random.default_rng(SEED)
    report = CheckReport()
    check_heston(report, rng)
    check_carr_madan(report)
    check_merton(report, rng)
    check_sabr(report, rng)
    return report.summarise()


if __name__ == "__main__":
    sys.exit(main())
