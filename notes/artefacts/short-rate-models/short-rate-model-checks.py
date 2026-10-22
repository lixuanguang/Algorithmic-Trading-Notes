"""Library gap-filling Batch L2, package P6 (2026-10-21): the worked examples of
mod:affine-short-rate-models, mod:hjm-forward-rate-models and the curve-fitting extension of
mod:term-structure-models-simulation.

Curve. The Federal Reserve Board's Gurkaynak-Sack-Wright Svensson parameters for 30 September 2026, from
feds200628.csv (source fed-gsw-data; the file is kept outside Git, SHA-256 7286435090933f0d...0bb89335c). The six
parameters are written below so that the script runs without the file; when the file is present at
reading_materials/derivatives-validation/empirical/feds200628.csv the script reads the row again and also checks the
published zero yields. The curve is a fitted off-the-run nominal Treasury zero curve, not SOFR or OIS. The
mean-reversion and volatility parameters (a = 0.1, sigma = 1 percent) are illustrative and not calibrated: calibration
needs cap or swaption volatilities, which are not held.

Seeds and criteria were fixed before the first run: 20261061 Hull-White
paths, 20261062 CIR exact paths, 20261063 the CIR Euler and exact comparison, 20261064 the forward-market caplet. A
failed statistical check is diagnosed, not rerun with another seed. Every check except the curve shows that a model is
implemented correctly under its own assumptions; none is evidence about markets.

Run: uv run python short-rate-model-checks.py   (numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import csv
import itertools
import math
import sys
from pathlib import Path

# third party library imports
import numpy as np
import scipy
from scipy import integrate, stats

print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
fails = []


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


# GSW Svensson parameters, 2026-09-30 (percent; tau in years).
GSW = {
    "BETA0": 2.220637762132e-14,
    "BETA1": 3.9277698129101,
    "BETA2": 5.27031980138786,
    "BETA3": 17.0928160768659,
    "TAU1": 1.86454967884118,
    "TAU2": 15.7025187144884,
}
GSW_FILE = Path(__file__).resolve().parents[3] / (
    "reading_materials/derivatives-validation/empirical/feds200628.csv"
)

print("== The GSW curve of 30 September 2026")
published = None
if GSW_FILE.exists():
    with GSW_FILE.open() as fh:
        rows = list(csv.reader(fh))
    header = next(r for r in rows if r and r[0] == "Date")
    row = dict(zip(header, next(r for r in rows if r and r[0] == "2026-09-30"), strict=True))
    ok(
        "the six parameters written in this script equal the file's row for 2026-09-30",
        all(float(row[k]) == v for k, v in GSW.items()),
    )
    published = {n: float(row[f"SVENY{n:02d}"]) for n in range(1, 31)}
else:
    print("  (feds200628.csv not present: the published-yield comparison is skipped)")

b0, b1, b2, b3, t1, t2 = (GSW[k] / 100 if k.startswith("BETA") else GSW[k] for k in GSW)


def fwd(t):
    """Instantaneous forward rate f(0, t), continuously compounded (Svensson)."""
    e1, e2 = math.exp(-t / t1), math.exp(-t / t2)
    return b0 + b1 * e1 + b2 * (t / t1) * e1 + b3 * (t / t2) * e2


def fwd_slope(t):
    """Analytic derivative of f(0, t) with respect to t."""
    e1, e2 = math.exp(-t / t1), math.exp(-t / t2)
    return -b1 / t1 * e1 + b2 / t1 * e1 * (1 - t / t1) + b3 / t2 * e2 * (1 - t / t2)


def zero_yield(t):
    """Continuously compounded zero yield y(0, t), the average of f(0, u) on [0, t]."""
    x1, x2 = t / t1, t / t2
    g1 = (1 - math.exp(-x1)) / x1
    g2 = (1 - math.exp(-x2)) / x2
    return b0 + b1 * g1 + b2 * (g1 - math.exp(-x1)) + b3 * (g2 - math.exp(-x2))


def discount(t):
    return math.exp(-zero_yield(t) * t) if t > 0 else 1.0


mats = np.arange(1, 31)
P_gsw = np.array([discount(T) for T in mats])
ok(
    "the zero yield is the average of the forward curve (quadrature) to 1e-12 at 1-30 years",
    max(
        abs(integrate.quad(fwd, 0, T, epsabs=1e-14, epsrel=1e-12)[0] - zero_yield(T) * T)
        for T in mats
    )
    < 1e-12,
)
if published is not None:
    gap = max(abs(100 * zero_yield(n) - published[n]) for n in range(1, 31))
    ok(
        "the zero yields reproduce the published SVENY01-SVENY30 (4 decimals) to 5e-5 percentage points",
        gap <= 5e-5 + 1e-9,
        f"largest gap {gap:.2e}",
    )
h = 1e-4
ok(
    "the analytic forward slope matches a central difference to 1e-8",
    max(abs(fwd_slope(t) - (fwd(t + h) - fwd(t - h)) / (2 * h)) for t in (0.5, 2, 7, 15, 29))
    < 1e-8,
)
print(
    f"  f(0,0) = {100 * fwd(0):.4f}%, y(1) = {100 * zero_yield(1):.4f}%, y(10) = {100 * zero_yield(10):.4f}%,"
    f" y(30) = {100 * zero_yield(30):.4f}%; P(0,10) = {discount(10):.6f}, P(0,30) = {discount(30):.6f}"
)

print("== Vasicek (reused) and CIR closed forms")
a_v, b_v, s_v, r_v = 0.1, 0.05, 0.01, 0.04
B4 = (1 - math.exp(-a_v * 4)) / a_v
A4 = math.exp((B4 - 4) * (a_v**2 * b_v - s_v**2 / 2) / a_v**2 - s_v**2 * B4**2 / (4 * a_v))
ok(
    "Vasicek four-year zero (Hull eqs. 31.6-31.8) is the existing 0.846849",
    abs(A4 * math.exp(-B4 * r_v) - 0.846849) < 5e-7,
    f"{A4 * math.exp(-B4 * r_v):.6f}",
)


def cir_price(r, tau, a, b, s):
    g = math.sqrt(a * a + 2 * s * s)
    den = (g + a) * (math.exp(g * tau) - 1) + 2 * g
    B = 2 * (math.exp(g * tau) - 1) / den
    A = (2 * g * math.exp((a + g) * tau / 2) / den) ** (2 * a * b / s**2)
    return A * math.exp(-B * r)


a_c, b_c, s_c, r_c, T_c = 0.5, 0.04, 0.10, 0.03, 5.0
P_cir = cir_price(r_c, T_c, a_c, b_c, s_c)
ok("Feller condition 2ab >= sigma^2 holds (0.04 >= 0.01)", 2 * a_c * b_c >= s_c**2)


# The bond price must solve P_t + a(b - r) P_r + 0.5 sigma^2 r P_rr = r P (Hull eq. 31.5).
def cir_pde_residual(r, tau, hr=1e-4, ht=1e-5):
    p = cir_price(r, tau, a_c, b_c, s_c)
    p_r = (cir_price(r + hr, tau, a_c, b_c, s_c) - cir_price(r - hr, tau, a_c, b_c, s_c)) / (2 * hr)
    p_rr = (
        cir_price(r + hr, tau, a_c, b_c, s_c) - 2 * p + cir_price(r - hr, tau, a_c, b_c, s_c)
    ) / hr**2
    p_t = -(cir_price(r, tau + ht, a_c, b_c, s_c) - cir_price(r, tau - ht, a_c, b_c, s_c)) / (
        2 * ht
    )
    return p_t + a_c * (b_c - r) * p_r + 0.5 * s_c**2 * r * p_rr - r * p


res = max(abs(cir_pde_residual(r, tau)) for r in (0.01, 0.03, 0.08) for tau in (0.5, 5.0))
ok("the CIR closed form solves the bond-pricing PDE (residual < 1e-6)", res < 1e-6, f"{res:.1e}")
print(f"  CIR five-year zero, closed form: {P_cir:.6f}")

print("== CIR by exact non-central chi-square transitions (200,000 paths)")
n_cir, h_min = 200_000, 1 / 128
steps = round(T_c / h_min)
c_fac = s_c**2 * (1 - math.exp(-a_c * h_min)) / (4 * a_c)
dof = 4 * a_c * b_c / s_c**2
rng = np.random.default_rng(20261062)
r_path = np.full(n_cir, r_c)
min_cir = r_c
# Trapezoid sums of the exact rate samples on grids h = 1/4, 1/8, ..., 1/128, all on the same paths.
levels = [32, 16, 8, 4, 2, 1]  # stride in units of h_min
trap = {k: np.zeros(n_cir) for k in levels}
prev = {k: r_path.copy() for k in levels}
for i in range(1, steps + 1):
    r_path = c_fac * rng.noncentral_chisquare(dof, r_path * math.exp(-a_c * h_min) / c_fac)
    min_cir = min(min_cir, float(r_path.min()))
    for k in levels:
        if i % k == 0:
            trap[k] += 0.5 * (prev[k] + r_path) * k * h_min
            prev[k] = r_path.copy()
ok("exact CIR samples are never negative", min_cir >= 0, f"minimum {min_cir:.2e}")
est = {}
for k in levels:
    df = np.exp(-trap[k])
    est[k] = (float(df.mean()), float(df.std(ddof=1) / math.sqrt(n_cir)))
chosen = None
for coarse, fine in itertools.pairwise(levels):
    change = abs(est[fine][0] - est[coarse][0])
    print(
        f"  h = 1/{round(1 / (fine * h_min))}: {est[fine][0]:.6f} (s.e. {est[fine][1]:.6f}),"
        f" change from 1/{round(1 / (coarse * h_min))} {change:.2e}"
    )
    if change < 0.1 * est[fine][1]:
        chosen = fine
        break
ok(
    "halving the integration grid changes the price by less than 0.1 s.e. at some h >= 1/128",
    chosen is not None,
)
if chosen is not None:
    m, se = est[chosen]
    ok(
        "CIR closed-form five-year zero lies within 3 s.e. of the exact-transition Monte Carlo",
        abs(m - P_cir) <= 3 * se,
        f"{m:.6f} (s.e. {se:.6f}) against {P_cir:.6f}, z = {(m - P_cir) / se:+.2f}",
    )

print("== CIR with sigma = 25 percent (Feller fails): Euler against exact sampling (10,000 paths)")
s_hi, n_e, dt_e = 0.25, 10_000, 1 / 12
rng = np.random.default_rng(20261063)
r_eu = np.full(n_e, r_c)
r_ex = np.full(n_e, r_c)
neg_eu = np.zeros(n_e, dtype=bool)
min_ex = np.inf
c_hi = s_hi**2 * (1 - math.exp(-a_c * dt_e)) / (4 * a_c)
for _ in range(round(T_c / dt_e)):
    z = rng.standard_normal(n_e)
    live = ~neg_eu
    r_eu[live] = (
        r_eu[live] + a_c * (b_c - r_eu[live]) * dt_e + s_hi * np.sqrt(r_eu[live] * dt_e) * z[live]
    )
    neg_eu |= r_eu < 0  # an untruncated Euler step cannot continue past a negative rate
    r_ex = c_hi * rng.noncentral_chisquare(
        4 * a_c * b_c / s_hi**2, r_ex * math.exp(-a_c * dt_e) / c_hi
    )
    min_ex = min(min_ex, float(r_ex.min()))
ok(
    "untruncated monthly Euler produces negative rates on some paths; exact sampling never does",
    neg_eu.sum() > 0 and min_ex >= 0,
    f"Euler negative on {neg_eu.sum()} of {n_e} paths; exact minimum {min_ex:.2e}",
)

print("== Hull-White fitted to the GSW curve (a = 0.1, sigma = 1 percent, illustrative)")
a, sg = 0.1, 0.01
r0 = fwd(0.0)


def theta(t):
    """Hull eq. (32.5): F_t(0,t) + a F(0,t) + sigma^2 (1 - exp(-2at)) / (2a)."""
    return fwd_slope(t) + a * fwd(t) + sg**2 / (2 * a) * (1 - math.exp(-2 * a * t))


def bfun(tau):
    return (1 - math.exp(-a * tau)) / a


def var_int(tau):
    """Variance of the integral of the Ornstein-Uhlenbeck part over [0, tau] started at 0."""
    return sg**2 / a**2 * (tau - 2 * bfun(tau) + (1 - math.exp(-2 * a * tau)) / (2 * a))


def int_alpha(T):
    """Integral over [0, T] of the deterministic part alpha, by quadrature of theta: r0 B(0,T) + int theta B."""
    q = integrate.quad(
        lambda s: theta(s) * bfun(T - s), 0, T, epsabs=1e-14, epsrel=1e-12, limit=200
    )[0]
    return r0 * bfun(T) + q


# Wilmott eq. (31.2) with Hull's theta: ln P(0,T) = -int theta B - r0 B + (sigma^2/2a^2)[T - 2B + (1-e^{-2aT})/2a].
P_hw = np.array([math.exp(-int_alpha(T) + 0.5 * var_int(T)) for T in mats])
gap = float(np.max(np.abs(P_hw - P_gsw)))
ok(
    "analytic Hull-White zero prices equal the GSW discount factors at 1-30 years to 1e-10",
    gap < 1e-10,
    f"{gap:.1e}",
)


def alpha_closed(t):
    return fwd(t) + sg**2 / (2 * a**2) * (1 - math.exp(-a * t)) ** 2


def alpha_quad(t):
    q = integrate.quad(
        lambda s: math.exp(-a * (t - s)) * theta(s), 0, t, epsabs=1e-14, epsrel=1e-12
    )[0]
    return r0 * math.exp(-a * t) + q


ok(
    "the mean short rate implied by theta equals F(0,t) + sigma^2 (1 - e^{-at})^2 / (2a^2) to 1e-10",
    max(abs(alpha_quad(t) - alpha_closed(t)) for t in (0.5, 1, 5, 10, 20, 30)) < 1e-10,
)
print(
    f"  theta/a at t = 0, 5, 20 years: {theta(0) / a:.4f}, {theta(5) / a:.4f}, {theta(20) / a:.4f};"
    f" forward premium alpha - F at 30 years {1e4 * (alpha_closed(30) - fwd(30)):.1f} bp"
)

print("== Hull-White Monte Carlo: exact joint sampling of (x, integral of x), 100,000 paths")
n_hw, sub = 100_000, 24  # half-monthly steps; monthly results by aggregation on the same paths
dt = 1 / sub
e1 = math.exp(-a * dt)
var_x = sg**2 * (1 - e1**2) / (2 * a)
var_i = var_int(dt)
cov = sg**2 / (2 * a**2) * (1 - e1) ** 2
L = np.linalg.cholesky(np.array([[var_x, cov], [cov, var_i]]))
rng = np.random.default_rng(20261061)
x = np.zeros(n_hw)
I = np.zeros(n_hw)
trap_m = np.zeros(n_hw)
trap_h = np.zeros(n_hw)
x_prev_m = np.zeros(n_hw)
I_at = {}
trap_m_at, trap_h_at = {}, {}
for k in range(1, 30 * sub + 1):
    t_prev, t_now = (k - 1) * dt, k * dt
    z = rng.standard_normal((2, n_hw))
    eps = L @ z
    x_new = x * e1 + eps[0]
    I += x * bfun(dt) + eps[1]
    # trapezoid on the exact short-rate samples r = x + alpha, half-monthly and monthly
    trap_h += 0.5 * dt * ((x + alpha_closed(t_prev)) + (x_new + alpha_closed(t_now)))
    x = x_new
    if k % 2 == 0:
        trap_m += (
            0.5 * (2 * dt) * ((x_prev_m + alpha_closed(t_now - 2 * dt)) + (x + alpha_closed(t_now)))
        )
        x_prev_m = x.copy()
    if k % sub == 0:
        T = k // sub
        I_at[T] = I.copy()
        trap_m_at[T], trap_h_at[T] = trap_m.copy(), trap_h.copy()
z_scores = []
for T, P in zip(mats, P_gsw, strict=True):
    df = math.exp(-int_alpha(T)) * np.exp(-I_at[T])
    m, se = float(df.mean()), float(df.std(ddof=1) / math.sqrt(n_hw))
    z_scores.append((m - P) / se)
zs = np.array(z_scores)
ok(
    "simulated discount factors lie within 4 s.e. of the GSW discount factors at all 30 maturities",
    bool(np.all(np.abs(zs) <= 4)),
    f"largest |z| {np.abs(zs).max():.2f} at {int(mats[np.abs(zs).argmax()])} years",
)
print(
    "  z at 1, 5, 10, 20, 30 years: " + ", ".join(f"{zs[T - 1]:+.2f}" for T in (1, 5, 10, 20, 30))
)
df_m = np.exp(-trap_m_at[30])
df_h = np.exp(-trap_h_at[30])
se30 = float(df_h.std(ddof=1) / math.sqrt(n_hw))
change = abs(float(df_h.mean()) - float(df_m.mean()))
verdict = "usable" if change < 0.1 * se30 else "biased (reported, not used)"
print(
    f"  diagnostic: trapezoid 30-year discount factor {df_m.mean():.6f} monthly, {df_h.mean():.6f} half-monthly"
    f" (change {change:.2e}, 0.1 s.e. {0.1 * se30:.2e}): {verdict}; GSW {P_gsw[-1]:.6f}"
)
neg_share = float(np.mean(x + alpha_closed(30.0) < 0))
print(f"  share of paths with a negative short rate at 30 years: {neg_share:.4f}")

print("== HJM drift condition on the GSW curve")


def hjm_short_rate_det(t, vol):
    """Deterministic part of r(t) = F(t,t): F(0,t) + int_0^t m(s,t) ds with m(s,T) = v(s,T) int_s^T v(s,u) du."""

    def m(s):
        return vol(s, t) * integrate.quad(lambda u: vol(s, u), s, t, epsabs=1e-14, epsrel=1e-12)[0]

    return fwd(t) + integrate.quad(m, 0, t, epsabs=1e-14, epsrel=1e-12)[0]


def richardson_slope(f, t, h=1e-2):
    d1 = (f(t + h) - f(t - h)) / (2 * h)
    d2 = (f(t + h / 2) - f(t - h / 2)) / h
    return (4 * d2 - d1) / 3


s_h = 0.01
const = lambda s, u: s_h
for t in (1.0, 5.0, 12.0):
    slope = richardson_slope(lambda u: hjm_short_rate_det(u, const), t)
    ok(
        f"constant volatility: the short-rate drift at t = {t:g} equals dF(0,t)/dt + sigma^2 t (Ho-Lee) to 1e-10",
        abs(slope - (fwd_slope(t) + s_h**2 * t)) < 1e-10,
        f"{slope:.12f}",
    )
expo = lambda s, u: sg * math.exp(-a * (u - s))
for t in (1.0, 5.0, 12.0):
    det = hjm_short_rate_det(t, expo)
    slope = richardson_slope(lambda u: hjm_short_rate_det(u, expo), t)
    ok(
        f"sigma e^(-a(T-t)): drift at t = {t:g} plus a times the deterministic rate equals Hull's theta (32.5) to 1e-10",
        abs(slope + a * det - theta(t)) < 1e-10,
    )

print("== Forward market model: a caplet under the rolling spot measure (100,000 paths)")
lam, n_fm, sub_fm, k_cap = (
    0.20,
    100_000,
    12,
    5,
)  # caplet on the year-5 to year-6 forward, annual accrual
Pk = np.array([discount(t) for t in range(0, k_cap + 2)])
F0 = Pk[:-1] / Pk[1:] - 1  # annual forwards F_0..F_{k_cap}, actual/actual with delta = 1
K = float(F0[k_cap])  # at the money
rng = np.random.default_rng(20261064)
logF = np.tile(np.log(F0), (n_fm, 1))
disc = 1 / (1 + F0[0]) * np.ones(n_fm)
d = 1 / sub_fm
for j in range(k_cap):  # periods (t_j, t_{j+1}]; forwards j+1..k_cap are alive
    for _ in range(sub_fm):
        z = rng.standard_normal(n_fm)
        F = np.exp(logF[:, j + 1 :])
        w = F * lam / (1 + F)  # delta_i F_i Lambda / (1 + delta_i F_i), Hull eq. (33.10)
        drift = lam * np.cumsum(w, axis=1) - 0.5 * lam**2
        logF[:, j + 1 :] += drift * d + lam * math.sqrt(d) * z[:, None]
    disc /= 1 + np.exp(logF[:, j + 1])  # roll the numeraire at t_{j+1} at the rate just set
payoff = np.maximum(np.exp(logF[:, k_cap]) - K, 0.0) * disc
mc, se = float(payoff.mean()), float(payoff.std(ddof=1) / math.sqrt(n_fm))
sd = lam * math.sqrt(k_cap)
d1 = (math.log(F0[k_cap] / K) + sd**2 / 2) / sd
black = Pk[k_cap + 1] * (F0[k_cap] * stats.norm.cdf(d1) - K * stats.norm.cdf(d1 - sd))
ok(
    "the simulated caplet agrees with Black's formula (Hull eq. 29.7) within 3 s.e.",
    abs(mc - black) <= 3 * se,
    f"{1e4 * mc:.3f} bp (s.e. {1e4 * se:.3f}) against {1e4 * black:.3f} bp per unit notional, z = {(mc - black) / se:+.2f}",
)
zc = (float(disc.mean()) - Pk[k_cap + 1]) / float(disc.std(ddof=1) / math.sqrt(n_fm))
ok(
    "the rolled numeraire reprices the six-year zero within 3 s.e. (the curve is an input)",
    abs(zc) <= 3,
    f"z = {zc:+.2f}",
)

if fails:
    print("FAILED:", ", ".join(fails))
    sys.exit(1)
print("all checks passed")
