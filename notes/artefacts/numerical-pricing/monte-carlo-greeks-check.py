"""Library gap-filling Batch L4, package L4-a (2026-10-21): the worked example of meth:monte-carlo-greeks.

Model (implementation_plan_v2.md, "Batch L4 freeze corrections and frozen specification"): risk-neutral GBM,
S0 = 100, r = 3 percent, q = 0, sigma = 20 percent, T = 1 (the inputs of meth:monte-carlo-simulation). A European
call struck at 105 and a unit cash-or-nothing call struck at 105. Estimators after Broadie and Glasserman (1996):
pathwise (eqs. (5)-(9)) and likelihood ratio (eqs. (14)-(16), scores rewritten in the standard normal Z), and
resimulation with common random numbers for the digital (reported only).

Frozen before the first run: NumPy default_rng(20261021), one vector of 100,000 standard normals shared by every
estimator; deterministic checks to relative 1e-6 (finite differences) or 1e-12 (identities); each stochastic
estimate within 4 standard errors of its closed form. Synthetic inputs only: not evidence about markets.

Run: uv run python monte-carlo-greeks-check.py   Exits 1 on failure. About one second.
"""

# standard library imports
import sys

# third party library imports
import numpy as np
import scipy
from scipy import stats

print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
fails = []


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


def rel(a, b):
    return abs(a - b) / abs(b)


S0, K, sig, r, T = 100.0, 105.0, 0.20, 0.03, 1.0
M, SEED, ZMAX = 100_000, 20261021, 4.0
disc = np.exp(-r * T)
sqT = np.sqrt(T)

# closed forms (BSM, q = 0)
d1 = (np.log(S0 / K) + (r + sig**2 / 2) * T) / (sig * sqT)
d2 = d1 - sig * sqT
call = S0 * stats.norm.cdf(d1) - K * disc * stats.norm.cdf(d2)
call_delta = stats.norm.cdf(d1)
call_vega = S0 * sqT * stats.norm.pdf(d1)
call_gamma = stats.norm.pdf(d1) / (S0 * sig * sqT)
call_dK = -disc * stats.norm.cdf(d2)
dig_delta = disc * stats.norm.pdf(d2) / (S0 * sig * sqT)
dig_dK = -disc * stats.norm.pdf(d2) / (K * sig * sqT)
print(
    f"closed forms: call {call:.4f}, delta {call_delta:.5f}, vega {call_vega:.4f}, gamma {call_gamma:.6f}"
)
print(f"  dC/dK {call_dK:.5f}; digital delta {dig_delta:.6f}, digital dD/dK {dig_dK:.6f}")


def path(s0, vol, z):
    """Terminal price as a function of the parameters on fixed normals z (Broadie-Glasserman eq. (4))."""
    return s0 * np.exp((r - vol**2 / 2) * T + vol * sqT * z)


def log_density(x, s0, vol):
    """Log of the lognormal density of S_T (eqs. (10)-(11))."""
    d = (np.log(x / s0) - (r - vol**2 / 2) * T) / (vol * sqT)
    return stats.norm.logpdf(d) - np.log(x * vol * sqT)


def z_of(x, s0, vol):
    return (np.log(x / s0) - (r - vol**2 / 2) * T) / (vol * sqT)


print("== 1. deterministic: path derivatives, scores and the gamma boundary term")
zs = np.array([-2.0, -0.5, 0.0, 0.7, 2.3])
h = 1e-5
dS_dS0_fd = (path(S0 + h, sig, zs) - path(S0 - h, sig, zs)) / (2 * h)
dS_dsig_fd = (path(S0, sig + h * 1e-2, zs) - path(S0, sig - h * 1e-2, zs)) / (2 * h * 1e-2)
ST_z = path(S0, sig, zs)
err1 = max(rel(a, b) for a, b in zip(dS_dS0_fd, ST_z / S0, strict=True))
err2 = max(rel(a, b) for a, b in zip(dS_dsig_fd, ST_z * (-sig * T + sqT * zs), strict=True))
ok("dS_T/dS0 = S_T/S0 (eq. (9))", err1 <= 1e-6, f"max rel err {err1:.1e}")
ok("dS_T/dsigma = S_T(-sigma T + sqrt(T) Z) (eq. (5))", err2 <= 1e-6, f"max rel err {err2:.1e}")
worst_s, worst_v = 0.0, 0.0
for x in (80.0, 105.0, 130.0):
    z = z_of(x, S0, sig)
    fd_s = (log_density(x, S0 + 1e-4, sig) - log_density(x, S0 - 1e-4, sig)) / 2e-4
    fd_v = (log_density(x, S0, sig + 1e-6) - log_density(x, S0, sig - 1e-6)) / 2e-6
    worst_s = max(worst_s, rel(fd_s, z / (S0 * sig * sqT)))
    worst_v = max(worst_v, rel(fd_v, (z * z - 1) / sig - sqT * z))
ok("S0 score = Z/(S0 sigma sqrt T) (eq. (16) in Z)", worst_s <= 1e-6, f"max rel err {worst_s:.1e}")
ok(
    "sigma score = (Z^2 - 1)/sigma - sqrt(T) Z (eq. (15) in Z)",
    worst_v <= 1e-6,
    f"max rel err {worst_v:.1e}",
)
# the per-path pathwise delta depends on S0 only through the indicator: S_T/S0 is unchanged by a bump
ratio_err = float(np.max(np.abs(path(S0 + 1.0, sig, zs) / (S0 + 1.0) - ST_z / S0) / (ST_z / S0)))
ok(
    "S_T/S0 does not depend on S0 (naive pathwise gamma is 0 a.s.)",
    ratio_err <= 1e-12,
    f"{ratio_err:.1e}",
)
g_K = np.exp(log_density(K, S0, sig))
gamma_eq18 = disc * (K / S0) ** 2 * g_K
ok(
    "eq. (18) boundary term e^{-rT}(K/S0)^2 g(K) = BSM gamma",
    rel(gamma_eq18, call_gamma) <= 1e-12,
    f"{gamma_eq18:.10f} vs {call_gamma:.10f}",
)

print(f"== 2. estimators on {M:,} draws, seed {SEED}")
rng = np.random.default_rng(SEED)
Z = rng.standard_normal(M)
ST = path(S0, sig, Z)
itm = ST > K
pay = disc * np.maximum(ST - K, 0.0)
score_S0 = Z / (S0 * sig * sqT)
score_sig = (Z * Z - 1) / sig - sqT * Z


def mean_se(x):
    return float(x.mean()), float(x.std(ddof=1) / np.sqrt(x.size))


est = {
    "call pathwise delta": (disc * itm * ST / S0, call_delta),
    "call LR delta": (pay * score_S0, call_delta),
    "call pathwise vega": (disc * itm * ST * (-sig * T + sqT * Z), call_vega),
    "call LR vega": (pay * score_sig, call_vega),
    "call pathwise dC/dK": (-disc * itm.astype(float), call_dK),
}
res = {}
for name, (x, exact) in est.items():
    m, se = mean_se(x)
    res[name] = (m, se)
    zsc = (m - exact) / se
    ok(
        f"{name} within {ZMAX:g} s.e.",
        abs(zsc) <= ZMAX,
        f"{m:.5f} (s.e. {se:.5f}) vs {exact:.5f}, z {zsc:+.2f}",
    )
print(f"  call by simulation {mean_se(pay)[0]:.4f} (s.e. {mean_se(pay)[1]:.4f}) vs {call:.4f}")

dig = disc * itm.astype(float)
# pathwise: the per-path derivative of e^{-rT} 1{S_T > K}, taken on the fixed draws by a central difference
# far smaller than any path's distance from the strike, is zero on every path
eps = 1e-9
gap = float(np.min(np.abs(ST - K)))
dig_pw_delta = (
    disc * ((path(S0 + eps, sig, Z) > K).astype(float) - (path(S0 - eps, sig, Z) > K)) / (2 * eps)
)
dig_pw_dK = disc * ((ST > K + eps).astype(float) - (ST > K - eps)) / (2 * eps)
ok(
    "digital pathwise delta is 0 on every path",
    gap > 1e3 * eps and not np.any(dig_pw_delta),
    f"mean 0 vs exact {dig_delta:.6f} (closest path {gap:.1e} from K)",
)
ok(
    "digital pathwise dD/dK is 0 on every path",
    not np.any(dig_pw_dK),
    f"mean 0 vs exact {dig_dK:.6f}",
)
m, se = mean_se(dig * score_S0)
zsc = (m - dig_delta) / se
ok(
    f"digital LR delta within {ZMAX:g} s.e.",
    abs(zsc) <= ZMAX,
    f"{m:.6f} (s.e. {se:.6f}) vs {dig_delta:.6f}, z {zsc:+.2f}",
)
dig_lr = (m, se)

print("== 3. reported, not binding")
for g in ("delta", "vega"):
    ratio = res[f"call LR {g}"][1] / res[f"call pathwise {g}"][1]
    print(f"  call {g}: LR / pathwise standard error = {ratio:.2f}")
for hh in (1.0, 0.01):
    fd = disc * ((path(S0 + hh, sig, Z) > K).astype(float) - itm) / hh
    m, se = mean_se(fd)
    print(
        f"  digital resimulation delta, h = {hh:g}: {m:.6f} (s.e. {se:.6f}), minus exact {m - dig_delta:+.6f}"
    )
print(f"  digital LR delta for comparison: {dig_lr[0]:.6f} (s.e. {dig_lr[1]:.6f})")

print("FAILED: " + ", ".join(fails) if fails else "all checks passed")
sys.exit(1 if fails else 0)
