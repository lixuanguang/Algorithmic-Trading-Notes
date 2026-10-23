"""Library gap-filling Batch L1, package P2 (2026-10-21): the worked examples of
meth:finite-difference-option-pricing and meth:least-squares-monte-carlo.

Inputs: K = 100, r = 5 percent, q = 0, sigma = 20 percent, T = 1, value
read at S = 100, a grid node; S_max = 3K. Acceptance ranges, seeds (20261021, 20261022) and path counts were
fixed before any run and are not tuned. Synthetic model data only: the checks show that the
schemes are implemented correctly under Black-Scholes-Merton; they are not evidence about markets.

Run: uv run --frozen --no-editable python numerical-pricing-checks.py   Exits 1 on failure. About 30 seconds.
"""

# standard library imports
import math
import sys

# third party library imports
import numpy as np
import scipy
from scipy import stats
from scipy.linalg import solve_banded

print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
fails = []


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


K, r, q, sg, T, S0 = 100.0, 0.05, 0.0, 0.20, 1.0, 100.0
SMAX = 3 * K


def bsm_put(S, tau):
    d1 = (math.log(S / K) + (r - q + sg**2 / 2) * tau) / (sg * math.sqrt(tau))
    d2 = d1 - sg * math.sqrt(tau)
    return K * math.exp(-r * tau) * stats.norm.cdf(-d2) - S * math.exp(-q * tau) * stats.norm.cdf(
        -d1
    )


def coefficients(I):
    """Spatial operator L V_i = a_i V_{i-1} + b_i V_i + c_i V_{i+1} for V_tau = L V (central differences).

    Where sigma^2 i < |r - q| the first derivative is upwinded (forward difference for r - q > 0), so that
    every off-diagonal coefficient is non-negative.
    """
    i = np.arange(1, I, dtype=float)
    a = 0.5 * (sg**2 * i**2 - (r - q) * i)
    b = -(sg**2 * i**2 + r)
    c = 0.5 * (sg**2 * i**2 + (r - q) * i)
    up = sg**2 * i < abs(r - q)
    if r - q > 0:
        a[up] = 0.5 * sg**2 * i[up] ** 2
        b[up] = -(sg**2 * i[up] ** 2 + (r - q) * i[up] + r)
        c[up] = 0.5 * sg**2 * i[up] ** 2 + (r - q) * i[up]
    return a, b, c, up


def boundaries(tau, american, call=False):
    if call:
        return 0.0, SMAX * math.exp(-q * tau) - K * math.exp(-r * tau)
    return (K if american else K * math.exp(-r * tau)), 0.0


def explicit(I, N, american=False):
    """Explicit scheme V^{n+1}_i = A_i V^n_{i-1} + B_i V^n_i + C_i V^n_{i+1} in time to maturity."""
    dS, dt = SMAX / I, T / N
    S = np.arange(I + 1) * dS
    a, b, c, _ = coefficients(I)
    A, B, C = dt * a, 1 + dt * b, dt * c
    V = np.maximum(K - S, 0.0)
    pay = V.copy()
    for n in range(N):
        new = V.copy()
        new[1:-1] = A * V[:-2] + B * V[1:-1] + C * V[2:]
        new[0], new[-1] = boundaries((n + 1) * dt, american)
        V = np.maximum(new, pay) if american else new
    return V, S, (A, B, C)


def theta_step(V, dt, theta, a, b, c, tau_new, american, pay, omega=1.5, tol=1e-9):
    """One theta-scheme step: (I - theta dt L) V_new = (I + (1 - theta) dt L) V_old, with boundaries."""
    m = len(a)
    rhs = V[1:-1] + (1 - theta) * dt * (a * V[:-2] + b * V[1:-1] + c * V[2:])
    lo, hi = boundaries(tau_new, american)
    rhs[0] += theta * dt * a[0] * lo
    rhs[-1] += theta * dt * c[-1] * hi
    sub, diag, sup = -theta * dt * a, 1 - theta * dt * b, -theta * dt * c
    if not american:
        ab = np.zeros((3, m))
        ab[0, 1:], ab[1], ab[2, :-1] = sup[:-1], diag, sub[1:]
        x = solve_banded((1, 1), ab, rhs)
    else:
        # Projected SOR on the linear complementarity problem, started from the previous values.
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


def crank_nicolson(I, N, american=False, exercise_steps=None):
    """Crank-Nicolson with a Rannacher start (four implicit half-steps replace the first two steps).

    exercise_steps: if given, the set of step indices n (1..N, in time to maturity) after which exercise is
    allowed by projection (a Bermudan option); american=True instead solves the full LCP by projected SOR.
    """
    dS, dt = SMAX / I, T / N
    S = np.arange(I + 1) * dS
    a, b, c, _ = coefficients(I)
    pay = np.maximum(K - S, 0.0)
    V = pay.copy()
    tau = 0.0
    for n in range(1, N + 1):
        if n <= 2:
            for _ in range(2):
                tau += dt / 2
                V = theta_step(V, dt / 2, 1.0, a, b, c, tau, american, pay)
        else:
            tau += dt
            V = theta_step(V, dt, 0.5, a, b, c, tau, american, pay)
        if exercise_steps is not None and n in exercise_steps:
            V = np.maximum(V, pay)
    return V, S


def value_at(V, S, s=S0):
    return float(V[round(s / (S[1] - S[0]))])


print("== European put by finite differences")
ref = bsm_put(S0, T)
ok("BSM put 5.5735", abs(ref - 5.573526) < 1e-6, f"{ref:.6f}")
cn = {I: value_at(*crank_nicolson(I, I // 2)) for I in (150, 300)}
e150, e300 = abs(cn[150] - ref), abs(cn[300] - ref)
ok(
    "Crank-Nicolson (150, 75) and (300, 150): error ratio in [3, 5] (second order)",
    3 <= e150 / e300 <= 5,
    f"errors {e150:.2e}, {e300:.2e}, ratio {e150 / e300:.2f}",
)
ex = {}
for I in (150, 300):
    bound = 1 / (sg**2 * I**2 + r)
    N = math.ceil(T / bound)
    V, S, (A, B, C) = explicit(I, N)
    ex[I] = value_at(V, S)
    ok(
        f"explicit at I = {I}, N = {N} (dt just inside 1/(sigma^2 I^2 + r)): all coefficients >= 0",
        min(A.min(), B.min(), C.min()) >= 0 and T / N <= bound,
    )
_, _, _, up = coefficients(150)
ok("sigma^2 < r here, so node i = 1 alone is upwinded", list(np.where(up)[0] + 1) == [1])
x150, x300 = abs(ex[150] - ref), abs(ex[300] - ref)
ok(
    "explicit error ratio in [3, 5] with dt proportional to dS^2",
    3 <= x150 / x300 <= 5,
    f"errors {x150:.2e}, {x300:.2e}, ratio {x150 / x300:.2f}",
)
Vbad, Sbad, (A, B, C) = explicit(150, 200)
ok(
    "explicit at I = 150, N = 200 (dt = 4.5 times the bound): B < 0 and |V| > 1e6",
    B.min() < 0 and np.abs(Vbad).max() > 1e6,
    f"max |V| {np.abs(Vbad).max():.2e}",
)

print("== American put")


def crr_put(n, american=True, every=None):
    """CRR binomial put; every=m allows exercise only after every m-th step from the start (Bermudan)."""
    dt = T / n
    u = math.exp(sg * math.sqrt(dt))
    d = 1 / u
    p = (math.exp((r - q) * dt) - d) / (u - d)
    disc = math.exp(-r * dt)
    j = np.arange(n + 1)
    V = np.maximum(K - S0 * u ** (n - 2 * j), 0.0)
    for step in range(n - 1, -1, -1):
        V = disc * (p * V[:-1] + (1 - p) * V[1:])
        if step > 0 and (american or (every is not None and step % every == 0)):
            j = np.arange(step + 1)
            V = np.maximum(V, K - S0 * u ** (step - 2 * j))
    return float(V[0])


t8000, t8001 = crr_put(8000), crr_put(8001)
amer = 0.5 * (t8000 + t8001)
ok(
    "reference 6.0904: mean of CRR trees with 8,000 and 8,001 steps",
    abs(amer - 6.0904) < 5e-5,
    f"{t8000:.5f}, {t8001:.5f}, mean {amer:.5f}",
)
am = {I: value_at(*crank_nicolson(I, I // 2, american=True)) for I in (150, 300)}
a150, a300 = abs(am[150] - amer), abs(am[300] - amer)
ok(
    "Crank-Nicolson with projected SOR (omega 1.5, tol 1e-9) at I = 300 within 4e-3 of the reference",
    a300 <= 4e-3,
    f"{am[150]:.4f} at I = 150, {am[300]:.4f} at I = 300",
)
ok("error ratio from I = 150 to I = 300 in [3, 5]", 3 <= a150 / a300 <= 5, f"{a150 / a300:.2f}")
Vexa, Sexa, _ = explicit(150, 901, american=True)
ok(
    "explicit with projection (I = 150, N = 901) is also close (within 0.02)",
    abs(value_at(Vexa, Sexa) - amer) < 0.02,
    f"{value_at(Vexa, Sexa):.4f}",
)
ok("early-exercise premium over the European put is about 0.52", 0.50 < amer - ref < 0.54)

print("== Least-squares Monte Carlo: Hull's eight paths (Table 27.4)")
paths = np.array(
    [
        [1.09, 1.08, 1.34],
        [1.16, 1.26, 1.54],
        [1.22, 1.07, 1.03],
        [0.93, 0.97, 0.92],
        [1.11, 1.56, 1.52],
        [0.76, 0.77, 0.90],
        [0.92, 0.84, 1.01],
        [0.88, 1.22, 1.34],
    ]
)


def lsm(Sp, strike, rate, dt, basis, coefs=None):
    """Longstaff-Schwartz on paths Sp (rows paths, columns exercise dates dt, 2 dt, ...).

    With coefs None the regressions are fitted on Sp and returned; otherwise the given policy is applied.
    Returns the discounted cash flow per path and the coefficients.
    """
    n_paths, n_dates = Sp.shape
    cash = np.maximum(strike - Sp[:, -1], 0.0)
    when = np.full(n_paths, n_dates - 1)
    fitted = {}
    for t in range(n_dates - 2, -1, -1):
        itm = strike - Sp[:, t] > 0
        if not itm.any():
            continue
        X = basis(Sp[itm, t])
        y = cash[itm] * np.exp(-rate * dt * (when[itm] - t))
        beta = np.linalg.lstsq(X, y, rcond=None)[0] if coefs is None else coefs[t]
        fitted[t] = beta
        ex_now = strike - Sp[itm, t] >= X @ beta
        idx = np.where(itm)[0][ex_now]
        cash[idx], when[idx] = strike - Sp[idx, t], t
    disc = cash * np.exp(-rate * dt * (when + 1))
    return disc, fitted


quad = lambda s: np.column_stack([np.ones_like(s), s, s**2])
hull_disc, hull_beta = lsm(paths, 1.10, 0.06, 1.0, quad)
ok(
    "value 0.1144 (Hull p. 663)",
    abs(hull_disc.mean() - 0.1144) < 5e-5,
    f"{hull_disc.mean():.5f}",
)
# Hull prints c = -1.813 at year 2; the least-squares value is -1.81358, so the printed figure is truncated
# rather than rounded. The comparison therefore allows one unit in the third decimal.
ok(
    "regressions -1.070 + 2.983 S - 1.813 S^2 at year 2, 2.038 - 3.335 S + 1.356 S^2 at year 1 (to 1e-3)",
    np.allclose(hull_beta[1], [-1.070, 2.983, -1.813], atol=1e-3)
    and np.allclose(hull_beta[0], [2.038, -3.335, 1.356], atol=1e-3),
    f"year 2 c = {hull_beta[1][2]:.5f}",
)

print("== Least-squares Monte Carlo: Bermudan put with 50 exercise dates")
n_ex = 50
tree5000, tree5050 = crr_put(5000, False, 100), crr_put(5050, False, 101)
berm = 0.5 * (tree5000 + tree5050)
ok(
    "tree reference: CRR 5,000 and 5,050 steps, exercise only at t_j = j/50",
    abs(tree5000 - tree5050) < 2e-3,
    f"{tree5000:.5f}, {tree5050:.5f}, mean {berm:.5f}",
)
Vb, Sb = crank_nicolson(600, 1000, exercise_steps=set(range(20, 1001, 20)))
cn_berm = value_at(Vb, Sb)
ok(
    "Crank-Nicolson (600, 1,000) with projection only at the 50 dates within 5e-3 of the trees",
    abs(cn_berm - berm) <= 5e-3,
    f"{cn_berm:.5f}",
)
ok("Bermudan lies between the European and American values", ref < berm < amer)


def gbm_on_dates(seed, n_paths):
    rng = np.random.default_rng(seed)
    dt = T / n_ex
    z = rng.standard_normal((n_paths, n_ex))
    return S0 * np.exp(np.cumsum((r - q - sg**2 / 2) * dt + sg * math.sqrt(dt) * z, axis=1))


basis = lambda s: np.column_stack([np.ones_like(s), s / K, (s / K) ** 2])
fit_paths = gbm_on_dates(20261021, 100_000)
in_sample, policy = lsm(fit_paths, K, r, T / n_ex, basis)
val_paths = gbm_on_dates(20261022, 100_000)
out_sample, _ = lsm(val_paths, K, r, T / n_ex, basis, coefs=policy)
est, se = out_sample.mean(), out_sample.std(ddof=1) / math.sqrt(len(out_sample))
ok(
    "policy fitted on 100,000 paths (seed 20261021), valued on 100,000 fresh paths (seed 20261022): "
    "reference - 0.05 <= estimate <= reference + 3 s.e.",
    berm - 0.05 <= est <= berm + 3 * se,
    f"{est:.4f} (s.e. {se:.4f}) against {berm:.4f}",
)
print(f"  in-sample estimate on the fitting paths {in_sample.mean():.4f} (reported, not tested)")

if fails:
    print("FAILED:", ", ".join(fails))
    sys.exit(1)
print("all checks passed")
