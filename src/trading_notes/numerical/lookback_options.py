"""Lookback options: Hull's and Wilmott's closed forms, seasoned simulation and monitoring bias.

Library gap-filling Batch L5, package L5-a (2026-10-21): the worked examples of
meth:lookback-option-valuation.

Inputs and acceptance were frozen before the first run. Model: GBM with constant r, q and sigma,
r != q. Hull's floating formulas (OFOD 11th Global ed., sec. 26.11, pp. 623-624) are evaluated with
T read as the remaining time tau and S_min/S_max the extreme recorded to date; Wilmott's sec. 26.6
forms (PWOQF 2nd ed., pp. 450-452) are an independent transcription.

Part 1, deterministic: Hull's Example 26.2 to its printed rounding (put 7.79, call 8.04) and
intermediates; the two sources against each other for floating and fixed-strike options; the
pricing-equation residual; the boundary condition dV/dM = 0 on S = M; deep-seasoned limits and
monotonicity in the recorded extreme.
Part 2, seasoned Monte Carlo: exact one-step simulation of the terminal price and the continuous
extreme of the remaining life (Brownian-bridge extreme, inverse of the barrier entry's crossing
probability), default_rng(20261022), 400,000 paths, against the closed forms within 4 standard
errors.
Part 3, monitoring: new issue, default_rng(20261021), 100,000 paths of 1,008 log-exact steps in 20
blocks of 5,000 (per block: normals, then uniforms for the minimum, then uniforms for the maximum).
Nested grids m = 7, 21, 63, 252, 1,008, each including S_0 and S_T; the continuous extreme on the
same paths from exact bridge extremes on every step. Sampling error (continuous estimate against
the closed form) is separated from monitoring bias (paired gap).

Synthetic model data only.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.lookback_options
(numpy, scipy). Exits 1 on failure. About 15 seconds.
"""

# standard library imports
import itertools
import math
import sys
from collections.abc import Callable
from typing import Final, Literal, overload

# third party library imports
import numpy as np
import scipy
from numpy.typing import NDArray
from scipy import stats

# project library imports
from trading_notes.numerical.report import CheckReport

type Floats = NDArray[np.float64]
# A floating-strike formula: (S, recorded extreme, tau, r, q, sigma) -> value.
type Floating = Callable[[float, float, float, float, float, float], float]

N = stats.norm.cdf
S0: Final = 50.0  # Hull Example 26.2
SIG: Final = 0.4
R: Final = 0.10
Q: Final = 0.0
T: Final = 0.25
X0: Final = math.log(S0)
DISC: Final = math.exp(-R * T)


# ---------------------------------------------------------------- formulas
def hull_floating_call(S: float, smin: float, tau: float, r: float, q: float, sig: float) -> float:
    """Hull eq. for c_fl with the minimum to date; tau is the remaining time."""
    st = sig * math.sqrt(tau)
    a1 = (math.log(S / smin) + (r - q + sig**2 / 2) * tau) / st
    a2 = a1 - st
    a3 = (math.log(S / smin) + (-r + q + sig**2 / 2) * tau) / st
    Y1 = -2 * (r - q - sig**2 / 2) * math.log(S / smin) / sig**2
    w = sig**2 / (2 * (r - q))
    return (
        S * math.exp(-q * tau) * N(a1)
        - S * math.exp(-q * tau) * w * N(-a1)
        - smin * math.exp(-r * tau) * (N(a2) - w * math.exp(Y1) * N(-a3))
    )


@overload
def hull_floating_put(
    S: float, smax: float, tau: float, r: float, q: float, sig: float, parts: Literal[False] = ...
) -> float: ...
@overload
def hull_floating_put(
    S: float, smax: float, tau: float, r: float, q: float, sig: float, parts: Literal[True]
) -> tuple[float, float, float, float, float]: ...
def hull_floating_put(
    S: float, smax: float, tau: float, r: float, q: float, sig: float, parts: bool = False
) -> float | tuple[float, float, float, float, float]:
    """Hull eq. for p_fl with the maximum to date; tau is the remaining time.

    With `parts`, also return the intermediates b1, b2, b3 and Y2.
    """
    st = sig * math.sqrt(tau)
    b1 = (math.log(smax / S) + (-r + q + sig**2 / 2) * tau) / st
    b2 = b1 - st
    b3 = (math.log(smax / S) + (r - q - sig**2 / 2) * tau) / st
    Y2 = 2 * (r - q - sig**2 / 2) * math.log(smax / S) / sig**2
    w = sig**2 / (2 * (r - q))
    value = (
        smax * math.exp(-r * tau) * (N(b1) - w * math.exp(Y2) * N(-b3))
        + S * math.exp(-q * tau) * w * N(-b2)
        - S * math.exp(-q * tau) * N(b2)
    )
    return (value, b1, b2, b3, Y2) if parts else value


def _wd(
    S: float, M: float, tau: float, r: float, D: float, sig: float
) -> tuple[float, float, float, float, float]:
    st = sig * math.sqrt(tau)
    d1 = (math.log(S / M) + (r - D + sig**2 / 2) * tau) / st
    return (
        d1,
        d1 - st,
        sig**2 / (2 * (r - D)),
        (S / M) ** (-2 * (r - D) / sig**2),
        2 * (r - D) * math.sqrt(tau) / sig,
    )


def wilmott_floating_call(S: float, M: float, tau: float, r: float, D: float, sig: float) -> float:
    """Wilmott's floating-strike call on the minimum M to date (sec. 26.6)."""
    d1, d2, w, pw, sh = _wd(S, M, tau, r, D, sig)
    return (
        S * math.exp(-D * tau) * N(d1)
        - M * math.exp(-r * tau) * N(d2)
        + S * math.exp(-r * tau) * w * (pw * N(-d1 + sh) - math.exp((r - D) * tau) * N(-d1))
    )


def wilmott_floating_put(S: float, M: float, tau: float, r: float, D: float, sig: float) -> float:
    """Wilmott's floating-strike put on the maximum M to date (sec. 26.6)."""
    d1, d2, w, pw, sh = _wd(S, M, tau, r, D, sig)
    return (
        M * math.exp(-r * tau) * N(-d2)
        - S * math.exp(-D * tau) * N(-d1)
        + S * math.exp(-r * tau) * w * (-pw * N(d1 - sh) + math.exp((r - D) * tau) * N(d1))
    )


def wilmott_fixed_call(
    S: float, M: float, E: float, tau: float, r: float, D: float, sig: float
) -> float:
    """Fixed-strike call on the maximum M to date (sec. 26.6, both cases)."""
    if E > M:
        d1, d2, w, pw, sh = _wd(S, E, tau, r, D, sig)
        return (
            S * math.exp(-D * tau) * N(d1)
            - E * math.exp(-r * tau) * N(d2)
            + S * math.exp(-r * tau) * w * (-pw * N(d1 - sh) + math.exp((r - D) * tau) * N(d1))
        )
    d1, d2, w, pw, sh = _wd(S, M, tau, r, D, sig)
    return (
        (M - E) * math.exp(-r * tau)
        + S * math.exp(-D * tau) * N(d1)
        - M * math.exp(-r * tau) * N(d2)
        + S * math.exp(-r * tau) * w * (-pw * N(d1 - sh) + math.exp((r - D) * tau) * N(d1))
    )


def wilmott_fixed_put(
    S: float, M: float, E: float, tau: float, r: float, D: float, sig: float
) -> float:
    """Fixed-strike put on the minimum M to date (sec. 26.6, both cases)."""
    if E < M:
        d1, d2, w, pw, sh = _wd(S, E, tau, r, D, sig)
        return (
            E * math.exp(-r * tau) * N(-d2)
            - S * math.exp(-D * tau) * N(-d1)
            + S * math.exp(-r * tau) * w * (pw * N(-d1 + sh) - math.exp((r - D) * tau) * N(-d1))
        )
    d1, d2, w, pw, sh = _wd(S, M, tau, r, D, sig)
    return (
        (E - M) * math.exp(-r * tau)
        - S * math.exp(-D * tau) * N(-d1)
        + M * math.exp(-r * tau) * N(-d2)
        + S * math.exp(-r * tau) * w * (pw * N(-d1 + sh) - math.exp((r - D) * tau) * N(-d1))
    )


def hull_fixed_call(
    S: float, smax: float, K: float, tau: float, r: float, q: float, sig: float
) -> float:
    """c_fix = p*_fl + S e^{-q tau} - K e^{-r tau} with S*_max = max(S_max, K) (p. 625)."""
    return (
        hull_floating_put(S, max(smax, K), tau, r, q, sig)
        + S * math.exp(-q * tau)
        - K * math.exp(-r * tau)
    )


def hull_fixed_put(
    S: float, smin: float, K: float, tau: float, r: float, q: float, sig: float
) -> float:
    """p_fix = c*_fl + K e^{-r tau} - S e^{-q tau} with S*_min = min(S_min, K) (p. 625)."""
    return (
        hull_floating_call(S, min(smin, K), tau, r, q, sig)
        + K * math.exp(-r * tau)
        - S * math.exp(-q * tau)
    )


def pde_residual(
    f: Floating,
    S: float,
    M: float,
    tau: float,
    rr: float,
    qq: float,
    ss: float,
    hS: float = 0.01,
    ht: float = 1e-5,
) -> float:
    """Return the pricing-equation residual of f at (S, M, tau) by central differences."""
    v = f(S, M, tau, rr, qq, ss)
    vS = (f(S + hS, M, tau, rr, qq, ss) - f(S - hS, M, tau, rr, qq, ss)) / (2 * hS)
    vSS = (f(S + hS, M, tau, rr, qq, ss) - 2 * v + f(S - hS, M, tau, rr, qq, ss)) / hS**2
    vtau = (f(S, M, tau + ht, rr, qq, ss) - f(S, M, tau - ht, rr, qq, ss)) / (2 * ht)
    return -vtau + 0.5 * ss**2 * S**2 * vSS + (rr - qq) * S * vS - rr * v


# ---------------------------------------------------------------- part 1
def check_closed_forms(report: CheckReport) -> tuple[float, float]:
    """Part 1: Example 26.2, the two sources, the pricing equation and the boundary condition.

    Returns:
        The new-issue floating call and put of Example 26.2.
    """
    print("== part 1: Example 26.2, two sources, pricing equation, boundary condition, history")
    put0, b1, b2, b3, Y2 = hull_floating_put(S0, S0, T, R, Q, SIG, parts=True)
    call0 = hull_floating_call(S0, S0, T, R, Q, SIG)
    report.ok(
        "Example 26.2 new-issue put rounds to 7.79 (S_max = S_0) and call to 8.04 (S_min = S_0)",
        round(put0, 2) == 7.79 and round(call0, 2) == 8.04,
        f"put {put0:.6f}, call {call0:.6f}",
    )
    report.ok(
        "printed intermediates b1 = -0.025, b2 = -0.225, b3 = 0.025 and Y2 = 0",
        abs(b1 + 0.025) <= 5e-4
        and abs(b2 + 0.225) <= 5e-4
        and abs(b3 - 0.025) <= 5e-4
        and abs(Y2) <= 1e-15,
        f"{b1:.6f}, {b2:.6f}, {b3:.6f}, {Y2:.1e}",
    )

    points = [
        (50.0, 0.25, 0.10, 0.00, 0.40),
        (50.0, 0.25, 0.10, 0.02, 0.40),
        (100.0, 1.00, 0.05, 0.02, 0.25),
    ]
    worst = 0.0
    for S, tau, rr, qq, ss in points:
        for smin, smax in ((S, S), (0.9 * S, 1.12 * S)):
            pairs = [
                (
                    hull_floating_call(S, smin, tau, rr, qq, ss),
                    wilmott_floating_call(S, smin, tau, rr, qq, ss),
                ),
                (
                    hull_floating_put(S, smax, tau, rr, qq, ss),
                    wilmott_floating_put(S, smax, tau, rr, qq, ss),
                ),
            ]
            for K in (0.95 * smax, 1.1 * smax):
                pairs.append(
                    (
                        hull_fixed_call(S, smax, K, tau, rr, qq, ss),
                        wilmott_fixed_call(S, smax, K, tau, rr, qq, ss),
                    )
                )
            for K in (0.9 * smin, 1.05 * smin):
                pairs.append(
                    (
                        hull_fixed_put(S, smin, K, tau, rr, qq, ss),
                        wilmott_fixed_put(S, smin, K, tau, rr, qq, ss),
                    )
                )
            worst = max(worst, max(abs(a - b) / abs(b) for a, b in pairs))
    report.ok(
        "Hull and Wilmott agree: floating call and put, fixed call and put in both strike cases"
        " (6 points, q = 0 and 0.02)",
        worst <= 1e-12,
        f"largest relative difference {worst:.1e}",
    )

    # Harness correction after the first run (recorded in the L5 review record): the frozen
    # steps hS = 0.01, ht = 1e-5 left a truncation error of up to 3.6e-6 near the running
    # extreme (it falls as hS^2: -3.5e-4, -3.2e-5, -3.6e-6, -3.3e-7 at hS = 0.1, 0.03, 0.01,
    # 0.003 for S = 50, S_min = 48, tau = 0.1). The frozen 1e-6 tolerance is kept and applied to
    # the Richardson-extrapolated residual (4 R(0.01) - R(0.02)) / 3, which removes the hS^2 term.
    pts: list[tuple[Floating, float, float, float, float, float, float]] = [
        (hull_floating_call, 52.0, 45.0, 0.25, 0.10, 0.02, 0.40),
        (hull_floating_call, 50.0, 48.0, 0.10, 0.10, 0.00, 0.40),
        (hull_floating_put, 50.0, 56.0, 0.25, 0.10, 0.02, 0.40),
        (hull_floating_put, 95.0, 110.0, 1.00, 0.05, 0.02, 0.25),
    ]
    raw = [pde_residual(*p) for p in pts]
    res = [(4 * pde_residual(*p, hS=0.01) - pde_residual(*p, hS=0.02)) / 3 for p in pts]
    print(f"    raw residuals at hS = 0.01: {', '.join(f'{x:.1e}' for x in raw)}")
    report.ok(
        "pricing-equation residual at interior points (S strictly inside the extreme), extrapolated"
        " in hS, <= 1e-6",
        max(abs(x) for x in res) <= 1e-6,
        f"largest {max(abs(x) for x in res):.1e}",
    )

    interior = (
        hull_floating_call(50, 45 + 1e-3, T, R, Q, SIG)
        - hull_floating_call(50, 45 - 1e-3, T, R, Q, SIG)
    ) / 2e-3
    fd = {h: (call0 - hull_floating_call(S0, S0 - h, T, R, Q, SIG)) / h for h in (1e-2, 1e-3)}
    report.ok(
        "dV/dS_min = 0 on S = S_min: one-sided difference small against the interior derivative"
        " and linear in h",
        abs(fd[1e-3]) <= 1e-2 * abs(interior) and 5 <= fd[1e-2] / fd[1e-3] <= 20,
        f"interior dc/dS_min {interior:.5f}; at S = S_min {fd[1e-2]:.2e} (h = 0.01), "
        f"{fd[1e-3]:.2e} (h = 0.001)",
    )

    deep_c = hull_floating_call(S0, 20.0, T, R, Q, SIG) - (
        S0 * math.exp(-Q * T) - 20.0 * math.exp(-R * T)
    )
    deep_p = hull_floating_put(S0, 120.0, T, R, Q, SIG) - (
        120.0 * math.exp(-R * T) - S0 * math.exp(-Q * T)
    )
    report.ok(
        "deep-seasoned limits: S_min = 20 gives S e^{-q tau} - 20 e^{-r tau}, S_max = 120 gives"
        " 120 e^{-r tau} - S e^{-q tau}",
        0 <= deep_c <= 1e-4 and 0 <= deep_p <= 1e-4,
        f"excess {deep_c:.1e} and {deep_p:.1e}; values "
        f"{hull_floating_call(S0, 20.0, T, R, Q, SIG):.4f} and "
        f"{hull_floating_put(S0, 120.0, T, R, Q, SIG):.4f} against new issue {call0:.4f} and "
        f"{put0:.4f}",
    )
    cgrid = [hull_floating_call(S0, m, T, R, Q, SIG) for m in np.arange(20.0, 50.01, 2.5)]
    pgrid = [hull_floating_put(S0, m, T, R, Q, SIG) for m in np.arange(50.0, 120.01, 5.0)]
    report.ok(
        "c_fl strictly decreasing in S_min (20 to 50) and p_fl strictly increasing in S_max"
        " (50 to 120)",
        all(a > b for a, b in itertools.pairwise(cgrid))
        and all(a < b for a, b in itertools.pairwise(pgrid)),
    )
    return call0, put0


# ---------------------------------------------------------------- part 2
def check_seasoned(
    report: CheckReport, rng: np.random.Generator, call0: float, put0: float
) -> None:
    """Part 2: seasoned contracts by exact simulation of the remaining life."""
    print(
        "== part 2: seasoned contracts by exact simulation of the remaining life"
        " (tau = 0.25, S = 50)"
    )
    n2 = 400_000
    z = rng.standard_normal(n2)
    u_min = 1.0 - rng.random(n2)
    u_max = 1.0 - rng.random(n2)
    x1 = X0 + (R - Q - SIG**2 / 2) * T + SIG * math.sqrt(T) * z
    spread = (x1 - X0) ** 2
    m_fut = np.exp(0.5 * (X0 + x1 - np.sqrt(spread - 2 * SIG**2 * T * np.log(u_min))))
    M_fut = np.exp(0.5 * (X0 + x1 + np.sqrt(spread - 2 * SIG**2 * T * np.log(u_max))))
    ST = np.exp(x1)
    cases = [
        (
            "floating call, S_min = 45",
            DISC * (ST - np.minimum(45.0, m_fut)),
            hull_floating_call(S0, 45.0, T, R, Q, SIG),
        ),
        (
            "floating put, S_max = 56",
            DISC * (np.maximum(56.0, M_fut) - ST),
            hull_floating_put(S0, 56.0, T, R, Q, SIG),
        ),
        (
            "fixed call K = 52, S_max = 56",
            DISC * np.maximum(np.maximum(56.0, M_fut) - 52.0, 0),
            hull_fixed_call(S0, 56.0, 52.0, T, R, Q, SIG),
        ),
        (
            "fixed call K = 60, S_max = 56",
            DISC * np.maximum(np.maximum(56.0, M_fut) - 60.0, 0),
            hull_fixed_call(S0, 56.0, 60.0, T, R, Q, SIG),
        ),
    ]
    se_seasoned = {}
    for name, x, cf in cases:
        m, se = x.mean(), x.std(ddof=1) / math.sqrt(n2)
        se_seasoned[name] = se
        report.ok(
            f"{name}: simulation within 4 s.e. of the closed form",
            abs(m - cf) <= 4 * se,
            f"{m:.4f} (s.e. {se:.4f}) against {cf:.4f}, z = {(m - cf) / se:+.2f}",
        )
    gap_c = hull_floating_call(S0, 45.0, T, R, Q, SIG) - call0
    gap_p = hull_floating_put(S0, 56.0, T, R, Q, SIG) - put0
    report.ok(
        "power: seasoned and new-issue closed forms differ by more than 20 s.e."
        " (ignoring history would fail)",
        abs(gap_c) > 20 * se_seasoned["floating call, S_min = 45"]
        and abs(gap_p) > 20 * se_seasoned["floating put, S_max = 56"],
        f"call +{gap_c:.4f} ({gap_c / se_seasoned['floating call, S_min = 45']:.0f} s.e.), "
        f"put +{gap_p:.4f} ({gap_p / se_seasoned['floating put, S_max = 56']:.0f} s.e.)",
    )


# ---------------------------------------------------------------- part 3
def check_monitoring(
    report: CheckReport, rng: np.random.Generator, call0: float, put0: float
) -> None:
    """Part 3: discrete against continuous monitoring on coupled nested grids (new issue)."""
    print("== part 3: discrete against continuous monitoring on coupled nested grids (new issue)")
    n_paths, n_steps, block = 100_000, 1008, 5000
    grids = (7, 21, 63, 252, 1008)
    dt = T / n_steps
    keys: list[tuple[str, str | int]] = [("call", "cont"), ("put", "cont")] + [
        (k, m) for k in ("call", "put") for m in grids
    ]
    acc = {k: [0.0, 0.0] for k in keys}  # sums and sums of squares of discounted payoffs
    gacc = {(k, m): [0.0, 0.0] for k in ("call", "put") for m in grids}  # paired gaps
    ordered = True
    for _ in range(n_paths // block):
        z = rng.standard_normal((block, n_steps))
        um = 1.0 - rng.random((block, n_steps))
        uM = 1.0 - rng.random((block, n_steps))
        x = np.empty((block, n_steps + 1))
        x[:, 0] = X0
        np.cumsum((R - Q - SIG**2 / 2) * dt + SIG * math.sqrt(dt) * z, axis=1, out=x[:, 1:])
        x[:, 1:] += X0
        a, b = x[:, :-1], x[:, 1:]
        d2 = (b - a) ** 2
        mc = np.exp(0.5 * (a + b - np.sqrt(d2 - 2 * SIG**2 * dt * np.log(um))).min(axis=1))
        Mc = np.exp(0.5 * (a + b + np.sqrt(d2 - 2 * SIG**2 * dt * np.log(uM))).max(axis=1))
        ST = np.exp(x[:, -1])
        pay: dict[tuple[str, str | int], Floats] = {
            ("call", "cont"): DISC * (ST - mc),
            ("put", "cont"): DISC * (Mc - ST),
        }
        for m in grids:
            sub = x[:, :: n_steps // m]
            pay[("call", m)] = DISC * (ST - np.exp(sub.min(axis=1)))
            pay[("put", m)] = DISC * (np.exp(sub.max(axis=1)) - ST)
        for k in ("call", "put"):
            chain = [pay[(k, "cont")]] + [pay[(k, m)] for m in reversed(grids)]
            ordered &= all(bool((hi >= lo - 1e-12).all()) for hi, lo in itertools.pairwise(chain))
        for key, v in pay.items():
            acc[key][0] += v.sum()
            acc[key][1] += (v**2).sum()
        for k in ("call", "put"):
            for m in grids:
                g = pay[(k, "cont")] - pay[(k, m)]
                gacc[(k, m)][0] += g.sum()
                gacc[(k, m)][1] += (g**2).sum()

    def mean_se(s: list[float]) -> tuple[float, float]:
        m = s[0] / n_paths
        return m, math.sqrt((s[1] / n_paths - m**2) / (n_paths - 1))

    report.ok(
        "pathwise: continuous >= m = 1,008 >= 252 >= 63 >= 21 >= 7 payoff on every path"
        " (call and put)",
        ordered,
    )
    for k, cf in (("call", call0), ("put", put0)):
        est, se = mean_se(acc[(k, "cont")])
        report.ok(
            f"{k}: continuous (bridge) estimate within 4 s.e. of the closed form",
            abs(est - cf) <= 4 * se,
            f"{est:.4f} (s.e. {se:.4f}) against {cf:.4f}, z = {(est - cf) / se:+.2f}",
        )
        gaps = {}
        for mm in grids:
            gap, gse = mean_se(gacc[(k, mm)])
            gaps[mm] = (gap, gse)
            print(
                f"    m = {mm:5d}: value {mean_se(acc[(k, mm)])[0]:.4f}, "
                f"gap {gap:.4f} (paired s.e. {gse:.5f}), gap*sqrt(m) {gap * math.sqrt(mm):.3f}"
            )
        report.ok(
            f"{k}: every monitoring gap positive by more than 4 paired s.e.",
            all(gap > 4 * s for gap, s in gaps.values()),
        )
        report.ok(
            f"{k}: convergence, gap at m = 1,008 at most half the gap at m = 63",
            gaps[1008][0] <= 0.5 * gaps[63][0],
            f"{gaps[1008][0]:.4f} against {gaps[63][0]:.4f} "
            f"(ratio {gaps[1008][0] / gaps[63][0]:.3f})",
        )


def main() -> int:
    """Print the versions, then run the three parts with one report.

    Parts 2 and 3 each draw from their own seeded generator.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
    report = CheckReport()
    call0, put0 = check_closed_forms(report)
    check_seasoned(report, np.random.default_rng(20261022), call0, put0)
    check_monitoring(report, np.random.default_rng(20261021), call0, put0)
    if report.failures:
        print("FAILED:", ", ".join(report.failures))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
