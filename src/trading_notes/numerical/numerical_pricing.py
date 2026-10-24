"""Finite-difference option pricing and least-squares Monte Carlo, checked on BSM.

Library gap-filling Batch L1, package P2 (2026-10-21): the worked examples of
meth:finite-difference-option-pricing and meth:least-squares-monte-carlo.

Inputs: K = 100, r = 5 percent, q = 0, sigma = 20 percent, T = 1, value read at S = 100, a grid
node; S_max = 3K. Acceptance ranges, seeds (20261021, 20261022) and path counts were fixed before
any run and are not tuned. Synthetic model data only: the checks show that the schemes are
implemented correctly under Black-Scholes-Merton; they are not evidence about markets.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.numerical_pricing
(numpy, scipy). Exits 1 on failure. About 30 seconds.
"""

import math
import sys
from collections.abc import Callable, Container
from typing import Final

import numpy as np
import scipy
from numpy.typing import NDArray
from scipy import stats
from scipy.linalg import solve_banded

from trading_notes.numerical.report import CheckReport

type Floats = NDArray[np.float64]
type Basis = Callable[[Floats], Floats]

K: Final = 100.0
R: Final = 0.05
Q: Final = 0.0
SG: Final = 0.20
T: Final = 1.0
S0: Final = 100.0
SMAX: Final = 3 * K
SEED_FIT: Final = 20261021  # paths that fit the exercise policy
SEED_VALUE: Final = 20261022  # fresh paths that value it
N_EX: Final = 50  # Bermudan exercise dates


def bsm_put(S: float, tau: float) -> float:
    """Return the BSM put."""
    d1 = (math.log(S / K) + (R - Q + SG**2 / 2) * tau) / (SG * math.sqrt(tau))
    d2 = d1 - SG * math.sqrt(tau)
    return K * math.exp(-R * tau) * stats.norm.cdf(-d2) - S * math.exp(-Q * tau) * stats.norm.cdf(
        -d1
    )


def coefficients(M: int) -> tuple[Floats, Floats, Floats, NDArray[np.bool_]]:
    """Return the coefficients on M space steps of the spatial operator.

    Spatial operator L V_i = a_i V_{i-1} + b_i V_i + c_i V_{i+1} for V_tau = L V (central).

    Where sigma^2 i < |r - q| the first derivative is upwinded (forward difference for
    r - q > 0), so that every off-diagonal coefficient is non-negative.

    Returns:
        a, b, c for the interior nodes i = 1..M-1, and which of them are upwinded.
    """
    r, q, sg = R, Q, SG
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


def boundaries(tau: float, american: bool, call: bool = False) -> tuple[float, float]:
    """Return the values at S = 0 and S = S_max with time tau to maturity."""
    if call:
        return 0.0, SMAX * math.exp(-Q * tau) - K * math.exp(-R * tau)
    return (K if american else K * math.exp(-R * tau)), 0.0


def explicit(
    M: int, N: int, american: bool = False
) -> tuple[Floats, Floats, tuple[Floats, Floats, Floats]]:
    """Explicit scheme V^{n+1}_i = A_i V^n_{i-1} + B_i V^n_i + C_i V^n_{i+1} in time to maturity.

    Returns:
        The values and the grid at maturity, and the coefficients (A, B, C).
    """
    dS, dt = SMAX / M, T / N
    S = np.arange(M + 1, dtype=np.float64) * dS
    a, b, c, _ = coefficients(M)
    A, B, C = dt * a, 1 + dt * b, dt * c
    V = np.maximum(K - S, 0.0)
    pay = V.copy()
    for n in range(N):
        new = V.copy()
        new[1:-1] = A * V[:-2] + B * V[1:-1] + C * V[2:]
        new[0], new[-1] = boundaries((n + 1) * dt, american)
        V = np.maximum(new, pay) if american else new
    return V, S, (A, B, C)


def theta_step(
    V: Floats,
    dt: float,
    theta: float,
    a: Floats,
    b: Floats,
    c: Floats,
    tau_new: float,
    american: bool,
    pay: Floats,
    omega: float = 1.5,
    tol: float = 1e-9,
) -> Floats:
    """One theta-scheme step: (I - theta dt L) V_new = (I + (1 - theta) dt L) V_old.

    The boundary values enter the first and last equations. An American step solves the linear
    complementarity problem by projected SOR (relaxation omega, stopping when no value moves by
    tol, at most 100,000 sweeps).
    """
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


def crank_nicolson(
    M: int, N: int, american: bool = False, exercise_steps: Container[int] | None = None
) -> tuple[Floats, Floats]:
    """Crank-Nicolson with a Rannacher start (four implicit half-steps replace the first two).

    Args:
        M: Space steps on [0, S_max].
        N: Time steps.
        american: Whether to solve the full LCP by projected SOR at every step.
        exercise_steps: If given, the step indices n (1..N, in time to maturity) after which
            exercise is allowed by projection (a Bermudan option).

    Returns:
        The values and the grid at time 0.
    """
    dS, dt = SMAX / M, T / N
    S = np.arange(M + 1, dtype=np.float64) * dS
    a, b, c, _ = coefficients(M)
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


def value_at(V: Floats, S: Floats, s: float = S0) -> float:
    """Return the value at the grid node nearest s."""
    return float(V[round(s / (S[1] - S[0]))])


def crr_put(n: int, american: bool = True, every: int | None = None) -> float:
    """CRR binomial put; every=m allows exercise only after every m-th step from the start."""
    dt = T / n
    u = math.exp(SG * math.sqrt(dt))
    d = 1 / u
    p = (math.exp((R - Q) * dt) - d) / (u - d)
    disc = math.exp(-R * dt)
    j = np.arange(n + 1)
    V = np.maximum(K - S0 * u ** (n - 2 * j), 0.0)
    for step in range(n - 1, -1, -1):
        V = disc * (p * V[:-1] + (1 - p) * V[1:])
        if step > 0 and (american or (every is not None and step % every == 0)):
            j = np.arange(step + 1)
            V = np.maximum(V, K - S0 * u ** (step - 2 * j))
    return float(V[0])


def lsm(
    Sp: Floats,
    strike: float,
    rate: float,
    dt: float,
    basis: Basis,
    coefs: dict[int, Floats] | None = None,
) -> tuple[Floats, dict[int, Floats]]:
    """Longstaff-Schwartz on paths Sp (rows paths, columns exercise dates dt, 2 dt, ...).

    With coefs None the regressions are fitted on Sp and returned; otherwise the given policy is
    applied.

    Returns:
        The discounted cash flow per path, and the coefficients by date index.
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


def gbm_on_dates(rng: np.random.Generator, n_paths: int) -> Floats:
    """Return GBM prices at the N_EX exercise dates, one row per path, exact in log."""
    dt = T / N_EX
    z = rng.standard_normal((n_paths, N_EX))
    prices: Floats = S0 * np.exp(
        np.cumsum((R - Q - SG**2 / 2) * dt + SG * math.sqrt(dt) * z, axis=1)
    )
    return prices


def check_european(report: CheckReport) -> float:
    """The European put: Crank-Nicolson's order, and the explicit scheme's stability bound."""
    sg, r = SG, R
    print("== European put by finite differences")
    ref = bsm_put(S0, T)
    report.ok("BSM put 5.5735", abs(ref - 5.573526) < 1e-6, f"{ref:.6f}")
    cn = {M: value_at(*crank_nicolson(M, M // 2)) for M in (150, 300)}
    e150, e300 = abs(cn[150] - ref), abs(cn[300] - ref)
    report.ok(
        "Crank-Nicolson (150, 75) and (300, 150): error ratio in [3, 5] (second order)",
        3 <= e150 / e300 <= 5,
        f"errors {e150:.2e}, {e300:.2e}, ratio {e150 / e300:.2f}",
    )
    ex = {}
    for M in (150, 300):
        bound = 1 / (sg**2 * M**2 + r)
        N = math.ceil(T / bound)
        V, S, (A, B, C) = explicit(M, N)
        ex[M] = value_at(V, S)
        report.ok(
            f"explicit at I = {M}, N = {N} (dt just inside 1/(sigma^2 I^2 + r)): all coefficients"
            " >= 0",
            bool(min(A.min(), B.min(), C.min()) >= 0 and T / N <= bound),
        )
    _, _, _, up = coefficients(150)
    report.ok("sigma^2 < r here, so node i = 1 alone is upwinded", list(np.where(up)[0] + 1) == [1])
    x150, x300 = abs(ex[150] - ref), abs(ex[300] - ref)
    report.ok(
        "explicit error ratio in [3, 5] with dt proportional to dS^2",
        3 <= x150 / x300 <= 5,
        f"errors {x150:.2e}, {x300:.2e}, ratio {x150 / x300:.2f}",
    )
    Vbad, _Sbad, (A, B, C) = explicit(150, 200)
    report.ok(
        "explicit at I = 150, N = 200 (dt = 4.5 times the bound): B < 0 and |V| > 1e6",
        bool(B.min() < 0 and np.abs(Vbad).max() > 1e6),
        f"max |V| {np.abs(Vbad).max():.2e}",
    )
    return ref


def check_american(report: CheckReport, ref: float) -> float:
    """The American put: CRR reference, Crank-Nicolson with PSOR, and projected explicit."""
    print("== American put")
    t8000, t8001 = crr_put(8000), crr_put(8001)
    amer = 0.5 * (t8000 + t8001)
    report.ok(
        "reference 6.0904: mean of CRR trees with 8,000 and 8,001 steps",
        abs(amer - 6.0904) < 5e-5,
        f"{t8000:.5f}, {t8001:.5f}, mean {amer:.5f}",
    )
    am = {M: value_at(*crank_nicolson(M, M // 2, american=True)) for M in (150, 300)}
    a150, a300 = abs(am[150] - amer), abs(am[300] - amer)
    report.ok(
        "Crank-Nicolson with projected SOR (omega 1.5, tol 1e-9) at I = 300 within 4e-3 of the"
        " reference",
        a300 <= 4e-3,
        f"{am[150]:.4f} at I = 150, {am[300]:.4f} at I = 300",
    )
    report.ok(
        "error ratio from I = 150 to I = 300 in [3, 5]", 3 <= a150 / a300 <= 5, f"{a150 / a300:.2f}"
    )
    Vexa, Sexa, _ = explicit(150, 901, american=True)
    report.ok(
        "explicit with projection (I = 150, N = 901) is also close (within 0.02)",
        abs(value_at(Vexa, Sexa) - amer) < 0.02,
        f"{value_at(Vexa, Sexa):.4f}",
    )
    report.ok(
        "early-exercise premium over the European put is about 0.52", 0.50 < amer - ref < 0.54
    )
    return amer


def quad(s: Floats) -> Floats:
    """Return the basis 1, S, S^2 of Hull's example."""
    return np.column_stack([np.ones_like(s), s, s**2])


def basis_scaled(s: Floats) -> Floats:
    """Return the basis 1, S/K, (S/K)^2 of the Bermudan example."""
    return np.column_stack([np.ones_like(s), s / K, (s / K) ** 2])


def check_hull_paths(report: CheckReport) -> None:
    """Least-squares Monte Carlo on Hull's eight paths (Table 27.4)."""
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
    hull_disc, hull_beta = lsm(paths, 1.10, 0.06, 1.0, quad)
    report.ok(
        "value 0.1144 (Hull p. 663)",
        bool(abs(hull_disc.mean() - 0.1144) < 5e-5),
        f"{hull_disc.mean():.5f}",
    )
    # Hull prints c = -1.813 at year 2; the least-squares value is -1.81358, so the printed figure
    # is truncated rather than rounded. The comparison therefore allows one unit in the third
    # decimal.
    report.ok(
        "regressions -1.070 + 2.983 S - 1.813 S^2 at year 2, 2.038 - 3.335 S + 1.356 S^2 at year 1"
        " (to 1e-3)",
        np.allclose(hull_beta[1], [-1.070, 2.983, -1.813], atol=1e-3)
        and np.allclose(hull_beta[0], [2.038, -3.335, 1.356], atol=1e-3),
        f"year 2 c = {hull_beta[1][2]:.5f}",
    )


def check_bermudan(report: CheckReport, ref: float, amer: float) -> None:
    """The Bermudan put by trees, Crank-Nicolson and LSM fitted and valued on separate paths."""
    print("== Least-squares Monte Carlo: Bermudan put with 50 exercise dates")
    tree5000, tree5050 = crr_put(5000, False, 100), crr_put(5050, False, 101)
    berm = 0.5 * (tree5000 + tree5050)
    report.ok(
        "tree reference: CRR 5,000 and 5,050 steps, exercise only at t_j = j/50",
        abs(tree5000 - tree5050) < 2e-3,
        f"{tree5000:.5f}, {tree5050:.5f}, mean {berm:.5f}",
    )
    Vb, Sb = crank_nicolson(600, 1000, exercise_steps=set(range(20, 1001, 20)))
    cn_berm = value_at(Vb, Sb)
    report.ok(
        "Crank-Nicolson (600, 1,000) with projection only at the 50 dates within 5e-3 of the trees",
        abs(cn_berm - berm) <= 5e-3,
        f"{cn_berm:.5f}",
    )
    report.ok("Bermudan lies between the European and American values", ref < berm < amer)
    fit_paths = gbm_on_dates(np.random.default_rng(SEED_FIT), 100_000)
    in_sample, policy = lsm(fit_paths, K, R, T / N_EX, basis_scaled)
    val_paths = gbm_on_dates(np.random.default_rng(SEED_VALUE), 100_000)
    out_sample, _ = lsm(val_paths, K, R, T / N_EX, basis_scaled, coefs=policy)
    est, se = out_sample.mean(), out_sample.std(ddof=1) / math.sqrt(len(out_sample))
    report.ok(
        "policy fitted on 100,000 paths (seed 20261021), valued on 100,000 fresh paths (seed"
        " 20261022): "
        "reference - 0.05 <= estimate <= reference + 3 s.e.",
        bool(berm - 0.05 <= est <= berm + 3 * se),
        f"{est:.4f} (s.e. {se:.4f}) against {berm:.4f}",
    )
    print(
        f"  in-sample estimate on the fitting paths {in_sample.mean():.4f} (reported, not tested)"
    )


def main() -> int:
    """Print the versions, then run the four parts with one report.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
    report = CheckReport()
    ref = check_european(report)
    amer = check_american(report, ref)
    check_hull_paths(report)
    check_bermudan(report, ref, amer)
    if report.failures:
        print("FAILED:", ", ".join(report.failures))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
