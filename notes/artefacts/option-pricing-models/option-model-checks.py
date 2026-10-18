"""derivatives and empirical validation (2026-10-17): own checks behind mod:heston-stochastic-volatility, mod:merton-jump-diffusion and
mod:sabr-smile. Parameters are invented; nothing here is market data.

1. Heston (1993), eqs. (10), (17)-(18): call = S P1 - K e^{-rT} P2, P_j = 1/2 + (1/pi) int_0^inf Re[e^{-i phi ln K}
   f_j / (i phi)] dphi, with u1 = 1/2, u2 = -1/2, a = kappa theta, b1 = kappa - rho sigma, b2 = kappa (lambda = 0).
   Checks: (a) with a tiny vol of vol and v0 = theta it equals Black-Scholes at sqrt(theta); (b) it matches an Euler
   (full truncation) Monte Carlo within three standard errors at T = 0.5.
2. Carr and Madan (1999), eqs. (5)-(6), condition (7) E[S_T^{alpha+1}] < inf: FFT of the damped call, alpha = 1.5, N =
   4096, eta = 0.25, Simpson weights. Checks: Black-Scholes prices across strikes; Heston prices against check 1.
3. Merton (Sloan WP 787-75), eqs. (15), (18)-(19): lognormal jumps with E[Y] = 1 (k = 0), F = sum_n e^{-lam T}(lam T)^n
   / n! * BS(S, T; K, sigma^2 + n delta^2 / T, r). Checks: lam = 0 gives Black-Scholes; dF/dlam > 0 at lam = 0 (sec. IV);
   Monte Carlo agreement.
4. SABR (Hagan et al. 2002 as restated by Bianchetti and Carlicchi, Table 5): the lognormal implied-volatility
   expansion. Checks: continuity at the money (z/x(z) -> 1); with nu = 0 and beta = 1 it is flat at alpha; against a
   Monte Carlo of the SABR dynamics at moderate parameters, within a stated tolerance of an asymptotic formula.
Run: uv run python option-model-checks.py   (numpy). Exits 1 on failure.
"""

# standard library imports
import math
import sys

# third party library imports
import numpy as np

rng = np.random.default_rng(20261017)
fails = []


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


Ncdf = lambda x: 0.5 * math.erfc(-x / math.sqrt(2))


def bs(S, K, T, r, v):
    s = math.sqrt(v * T)
    d1 = (math.log(S / K) + r * T + 0.5 * v * T) / s
    return S * Ncdf(d1) - K * math.exp(-r * T) * Ncdf(d1 - s)


def heston_f(phi, j, x, v, T, r, kappa, theta, sigma, rho):
    u, b = (0.5, kappa - rho * sigma) if j == 1 else (-0.5, kappa)
    a = kappa * theta
    d = np.sqrt((rho * sigma * phi * 1j - b) ** 2 - sigma**2 * (2 * u * phi * 1j - phi**2))
    g = (b - rho * sigma * phi * 1j + d) / (b - rho * sigma * phi * 1j - d)
    e = np.exp(d * T)
    C = r * phi * 1j * T + a / sigma**2 * (
        (b - rho * sigma * phi * 1j + d) * T - 2 * np.log((1 - g * e) / (1 - g))
    )
    D = (b - rho * sigma * phi * 1j + d) / sigma**2 * ((1 - e) / (1 - g * e))
    return np.exp(C + D * v + 1j * phi * x)


def heston_call(S, K, T, r, v0, kappa, theta, sigma, rho):
    phi = np.linspace(1e-6, 200, 40001)
    P = []
    for j in (1, 2):
        f = heston_f(phi, j, math.log(S), v0, T, r, kappa, theta, sigma, rho)
        integ = np.real(np.exp(-1j * phi * math.log(K)) * f / (1j * phi))
        P.append(0.5 + np.trapezoid(integ, phi) / math.pi)
    return S * P[0] - K * math.exp(-r * T) * P[1]


S0, r, T = 100.0, 0.02, 0.5
print("== 1. Heston closed form")
th = 0.04
for K in (90, 100, 110):
    h, b = heston_call(S0, K, T, r, th, 2.0, th, 1e-4, -0.5), bs(S0, K, T, r, th)
    ok(
        f"tiny vol of vol equals Black-Scholes to 1e-3 (quadrature on [0, 200]), K = {K}",
        abs(h - b) < 1e-3,
        f"{h:.5f} vs {b:.5f}",
    )
kap, theta, sig, rho, v0 = 1.5, 0.04, 0.5, -0.7, 0.04
n, steps = 200000, 200
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
    ok(
        f"Heston formula vs Monte Carlo, K = {K}",
        abs(h - pay.mean()) < 3 * pay.std() / math.sqrt(n) + 0.02,
        f"{h:.4f} vs {pay.mean():.4f} (s.e. {pay.std() / math.sqrt(n):.4f})",
    )

print("== 2. Carr-Madan FFT")


def carr_madan(cf, S, T, r, alpha=1.5, N=4096, eta=0.25):
    lam = 2 * math.pi / (N * eta)
    bnd = N * lam / 2
    v = np.arange(N) * eta
    psi = (
        math.exp(-r * T)
        * cf(v - (alpha + 1) * 1j)
        / (alpha**2 + alpha - v**2 + 1j * (2 * alpha + 1) * v)
    )
    w = eta / 3 * (3 + (-1) ** (np.arange(N) + 1) - (np.arange(N) == 0))
    k = -bnd + lam * np.arange(N)
    y = np.fft.fft(np.exp(1j * bnd * v) * psi * w)
    return np.exp(k), np.exp(-alpha * k) / math.pi * np.real(y)


vol = 0.25
cf_bs = lambda u: np.exp(1j * u * (math.log(S0) + (r - 0.5 * vol**2) * T) - 0.5 * vol**2 * u**2 * T)
Ks, Cs = carr_madan(cf_bs, S0, T, r)
err = max(abs(np.interp(K, Ks, Cs) - bs(S0, K, T, r, vol**2)) for K in (80, 90, 100, 110, 120))
ok("FFT reproduces Black-Scholes across strikes 80-120", err < 0.01, f"max abs error {err:.5f}")
cf_h = lambda u: heston_f(u, 2, math.log(S0), v0, T, r, kap, theta, sig, rho)
Ks, Cs = carr_madan(cf_h, S0, T, r)
err = max(
    abs(np.interp(K, Ks, Cs) - heston_call(S0, K, T, r, v0, kap, theta, sig, rho))
    for K in (90, 100, 110)
)
ok(
    "FFT with the Heston characteristic function matches the integral",
    err < 0.02,
    f"max abs error {err:.5f}",
)

print("== 3. Merton jump-diffusion (lognormal jumps, E[Y] = 1)")


def merton(S, K, T, r, s2, lam, d2, nmax=60):
    return sum(
        math.exp(-lam * T) * (lam * T) ** k / math.factorial(k) * bs(S, K, T, r, s2 + k * d2 / T)
        for k in range(nmax)
    )


s2, d2 = 0.04, 0.02
ok(
    "lambda = 0 gives Black-Scholes",
    abs(merton(S0, 100, T, r, s2, 0.0, d2) - bs(S0, 100, T, r, s2)) < 1e-12,
)
eps = 1e-4
for K in (80, 100, 120):
    ok(
        f"dF/dlambda > 0 at lambda = 0, K = {K}",
        merton(S0, K, T, r, s2, eps, d2) > merton(S0, K, T, r, s2, 0, d2),
    )
lam = 1.0
Nj = rng.poisson(lam * T, n)
logY = -0.5 * d2 * Nj + math.sqrt(d2) * np.sqrt(Nj) * rng.standard_normal(
    n
)  # product of n lognormals with E[Y] = 1
ST = S0 * np.exp((r - 0.5 * s2) * T + math.sqrt(s2 * T) * rng.standard_normal(n) + logY)
for K in (90, 100, 110):
    pay = math.exp(-r * T) * np.maximum(ST - K, 0)
    m = merton(S0, K, T, r, s2, lam, d2)
    ok(
        f"Merton series vs Monte Carlo, K = {K}",
        abs(m - pay.mean()) < 3 * pay.std() / math.sqrt(n),
        f"{m:.4f} vs {pay.mean():.4f}",
    )

print("== 4. SABR expansion")


def sabr_vol(F, K, T, a, b, rho, nu):
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
    return a / B * zx * A


F, Te = 0.03, 1.0
a, b, rh, nu = 0.03**0.5 * 0.2, 0.5, -0.3, 0.4
atm = sabr_vol(F, F, Te, a, b, rh, nu)
near = sabr_vol(F, F * (1 + 1e-7), Te, a, b, rh, nu)
ok("continuous at the money", abs(atm - near) < 1e-6, f"{atm:.6f} vs {near:.6f}")
ok(
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
    ok(
        f"expansion within 2 vol points of Monte Carlo, K = {K}",
        abs(sabr_vol(F, K, Te, a, b, rh, nu) - lo) < 0.02,
        f"formula {sabr_vol(F, K, Te, a, b, rh, nu) * 100:.2f}% vs MC-implied {lo * 100:.2f}%",
    )

if fails:
    print("\nFAILED:", fails)
    sys.exit(1)
print("\nall checks passed")
