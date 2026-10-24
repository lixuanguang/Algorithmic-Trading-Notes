"""Extreme value tail estimation: Hill, peaks over threshold and GPD fits against known truths.

Library gap-filling Batch L2, package P9 (2026-10-21): the worked examples of
meth:extreme-value-tail-estimation.

Estimators fixed before the first run: upper tail of the loss; threshold at the empirical 95th
percentile with k = n/20 exceedances; Hill H_k = (1/k) sum_{i=1..k} ln X_(n-i+1) - ln X_(n-k), the
threshold being the (k+1)-th largest observation; the GPD fitted by maximum likelihood to the k
excesses; VaR and ES at 99 and 99.5 percent by the peaks-over-threshold formulas (Hull, RMFI 6th
ed., eqs. (12.9)-(12.10); McNeil, Frey and Embrechts, QRM 2005, eqs. (7.18)-(7.19)).

Pass or fail (known-truth benchmarks): exact Pareto data (Renyi: H_k ~ xi Gamma(k, 1)/k); Student t4
at n = 1e6 against the finite-threshold Hill functional; GPD score and likelihood checks; exact POT
formulas for a Pareto tail; RMFI's published example. Diagnostics (no pass threshold):
maximum-likelihood shape bias over 500 GPD samples (moved here at the L2 freeze), finite-threshold
bias at n = 5,000, bootstrap coverage, threshold sensitivity, and the two-step (GARCH then GPD)
method on the GARCH(1,1)-t generator of var-backtest-check.py (omega 1e-6, alpha 0.08, beta 0.90, nu
6).

Seeds, fixed before the first run: 20261091 Pareto replications; 20261092 t4 with n = 1e6; 20261093
the GPD score sample; 20261094 the 500-sample shape diagnostic; 20261095 the n = 5,000 t4 sample;
20261100 + i samples and 20261300 + i resamples for bootstrap coverage (i = 0..199); 20261097 the
GPD bootstrap; 20261098 the GARCH path. The L2 freeze reproduction of the shape diagnostic used
NumPy default_rng(20261021); that seed was examined during planning and is reported only as such.
Synthetic data only: no empirical claim. Each part makes its own generators from the seeds above, so
no generator is shared between parts.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.extreme_value
(numpy, scipy). Exits 1 on failure. About 24 seconds: the GPD fits and the Hill bootstrap of the
diagnostics take most of it.
"""

# standard library imports
import math
import sys
from typing import Final

# third party library imports
import numpy as np
import scipy
from numpy.typing import NDArray
from scipy import integrate, optimize, stats

# project library imports
from trading_notes.numerical.report import CheckReport

type Floats = NDArray[np.float64]

N_SAMPLE: Final = 5_000  # the n = 5,000 sample of the known-truth and diagnostic parts
K_TOP: Final = 250  # its k = n/20 exceedances
NU: Final = 4  # Student t degrees of freedom
XI0: Final = 0.25  # the GPD shape of the exact Pareto and GPD samples


def hill(x: Floats, k: int) -> float:
    """H_k with the (k+1)-th largest observation as threshold."""
    top = np.sort(np.partition(x, -(k + 1))[-(k + 1) :])
    return float(np.mean(np.log(top[1:])) - math.log(top[0]))


def gpd_nll(params: Floats | tuple[float, float], y: Floats) -> float:
    """Return the negative GPD log-likelihood of the excesses y at (xi, beta); inf off support."""
    xi, beta = params
    if beta <= 0 or np.any(1 + xi * y / beta <= 0):
        return np.inf
    return len(y) * math.log(beta) + (1 + 1 / xi) * float(np.sum(np.log1p(xi * y / beta)))


def gpd_score(xi: float, beta: float, y: Floats) -> Floats:
    """Gradient of the GPD log-likelihood (QRM eq. (7.14)) with respect to (xi, beta)."""
    z = 1 + xi * y / beta
    d_xi = float(np.sum(np.log(z) / xi**2 - (1 + 1 / xi) * (y / beta) / z))
    d_beta = float(-len(y) / beta + (1 + 1 / xi) * np.sum(xi * y / beta**2 / z))
    return np.array([d_xi, d_beta])


def gpd_fit(y: Floats, start: tuple[float, float | None] = (0.2, None)) -> Floats:
    """Maximum likelihood by Nelder-Mead, polished by Newton steps on the analytic score."""
    b0 = start[1] or float(np.mean(y))
    res = optimize.minimize(
        gpd_nll,
        x0=[start[0], b0],
        args=(y,),
        method="Nelder-Mead",
        options={"xatol": 1e-12, "fatol": 1e-12, "maxiter": 20_000},
    )
    p: Floats = res.x.copy()
    for _ in range(50):
        g = gpd_score(p[0], p[1], y)
        h = 1e-6 * np.maximum(np.abs(p), 1e-3)
        H = np.empty((2, 2))
        for j in range(2):
            e = np.zeros(2)
            e[j] = h[j]
            pe, pm = p + e, p - e
            H[:, j] = (gpd_score(pe[0], pe[1], y) - gpd_score(pm[0], pm[1], y)) / (2 * h[j])
        step = np.linalg.solve(H, g)
        p = p - step
        if np.max(np.abs(step)) < 1e-14:
            break
    return p


def pot_var(u: float, xi: float, beta: float, tail_frac: float, q: float) -> float:
    """Peaks-over-threshold VaR at level q, for threshold u and tail fraction tail_frac."""
    var: float = u + beta / xi * (((1 - q) / tail_frac) ** (-xi) - 1)
    return var


def pot_es(var: float, u: float, xi: float, beta: float) -> float:
    """Peaks-over-threshold expected shortfall, given the VaR at the same level."""
    es: float = (var + beta - xi * u) / (1 - xi)
    return es


def kl_best_gpd(u: float, nu: int) -> Floats:
    """GPD parameters maximising the expected log-likelihood of the true t excesses over u."""
    sf_u = stats.t.sf(u, nu)

    def neg(p: Floats) -> float:
        xi, beta = p
        if beta <= 0:
            return np.inf

        def f(yy: float) -> float:
            density: float = (
                (math.log(beta) + (1 + 1 / xi) * math.log1p(xi * yy / beta))
                * stats.t.pdf(u + yy, nu)
                / sf_u
            )
            return density

        return integrate.quad(f, 0, np.inf, epsabs=1e-12, limit=200)[0]

    return optimize.minimize(
        neg, x0=[0.2, 0.5], method="Nelder-Mead", options={"xatol": 1e-10, "fatol": 1e-13}
    ).x


def t_es(q: float, nu: int) -> float:
    """Expected shortfall of the Student t distribution at level q."""
    x = stats.t.ppf(q, nu)
    return (nu + x**2) / (nu - 1) * stats.t.pdf(x, nu) / (1 - q)


def garch_nll(p: Floats, x: Floats) -> float:
    """Return the negative Gaussian GARCH(1,1) log-likelihood of x at (omega, alpha, beta)."""
    w, aa, bb = p
    if w <= 0 or aa < 0 or bb < 0 or aa + bb >= 1:
        return np.inf
    v = np.empty(x.size)
    v[0] = x.var()
    for t in range(1, x.size):
        v[t] = w + aa * x[t - 1] ** 2 + bb * v[t - 1]
    return 0.5 * float(np.sum(np.log(v) + x**2 / v))


# ---------------------------------------------------------------------------------------------
def check_rmfi(report: CheckReport) -> None:
    """Part A: RMFI's published EVT example (u = 160, n_u = 25, n = 500).

    Args:
        report: The run's report.
    """
    print("== RMFI sec. 12.6: the published EVT example (u = 160, n_u = 25, n = 500)")
    # RMFI prints beta = 110.46 and xi = 0.354, but its exponent reads -1/0.3545 (p. 274) and its
    # VaRs need the unrounded Solver estimate: with xi = 0.354 exactly, the 99.9% VaR is 1,094.31,
    # not the printed 1,094.6. The check therefore infers xi from the printed 99.9% VaR (beta
    # 110.46) and requires that one value to reproduce the other printed figures.
    u0, nu0, n0, b0 = 160.0, 25, 500, 110.46
    x0 = optimize.brentq(
        lambda x: pot_var(u0, x, b0, nu0 / n0, 0.999) - 1094.6, 0.30, 0.40, xtol=1e-12
    )

    def tp(x: float) -> float:
        tail: float = nu0 / n0 * (1 + x0 * (x - u0) / b0) ** (-1 / x0)
        return tail

    v99, v9997 = (pot_var(u0, x0, b0, nu0 / n0, q) for q in (0.99, 0.9997))
    v999 = 1094.6
    report.ok(
        "xi implied by the printed 99.9% VaR rounds to 0.354 and reproduces 0.0176, 0.0062, 399.6,"
        " 1,757.4, 702.0, 1,778.1",
        round(x0, 3) == 0.354
        and round(tp(300), 4) == 0.0176
        and round(tp(500), 4) == 0.0062
        and round(v99, 1) == 399.6
        and abs(v9997 - 1757.4) <= 0.06
        and round(pot_es(v99, u0, x0, b0), 1) == 702.0
        and abs(pot_es(v999, u0, x0, b0) - 1778.1) <= 0.06,
        f"xi {x0:.5f}; {tp(300):.5f}, {tp(500):.5f}; {v99:.2f}, {v9997:.2f};"
        f" {pot_es(v99, u0, x0, b0):.2f}, {pot_es(v999, u0, x0, b0):.2f}",
    )


# ---------------------------------------------------------------------------------------------
def check_known_truth(report: CheckReport) -> tuple[float, float]:
    """Part B: known-truth benchmarks for Hill, the GPD fit and the POT formulas.

    Args:
        report: The run's report.

    Returns:
        The 95th percentile of the t4 distribution and its population Hill functional.
    """
    print("== Known-truth benchmarks")
    n, k, xi0 = N_SAMPLE, K_TOP, XI0
    rng = np.random.default_rng(20261091)
    H = np.array([hill(rng.random(n) ** (-xi0), k) for _ in range(2_000)])
    se = H.std(ddof=1) / math.sqrt(H.size)
    report.ok(
        "exact Pareto (xi = 0.25): mean of H_k over 2,000 samples within 3 s.e. of 0.25",
        abs(H.mean() - xi0) <= 3 * se,
        f"{H.mean():.5f} (s.e. {se:.5f})",
    )
    report.ok(
        "and its standard deviation within 5 percent of xi / sqrt(k) = 0.015811",
        abs(H.std(ddof=1) / (xi0 / math.sqrt(k)) - 1) <= 0.05,
        f"{H.std(ddof=1):.6f}",
    )

    nu = NU
    u95 = stats.t.ppf(0.95, nu)
    hill_pop = (
        integrate.quad(lambda x: stats.t.sf(x, nu) / x, u95, np.inf, epsabs=1e-13, epsrel=1e-12)[0]
        / 0.05
    )
    report.ok(
        "population Hill functional of t4 at its 95th percentile is 0.348898",
        abs(hill_pop - 0.348898) < 5e-7,
        f"{hill_pop:.7f}",
    )
    rng = np.random.default_rng(20261092)
    big = rng.standard_t(nu, 1_000_000)
    kb = 50_000
    top = np.sort(np.partition(big, -(kb + 1))[-(kb + 1) :])
    logs = np.log(top[1:]) - math.log(top[0])
    hb, seb = float(logs.mean()), float(logs.std(ddof=1) / math.sqrt(kb))
    report.ok(
        "t4 with n = 1e6, k = 50,000: H_k within 3 s.e. of the functional 0.348898 (not of the"
        " asymptotic 0.25)",
        abs(hb - hill_pop) <= 3 * seb,
        f"{hb:.5f} (s.e. {seb:.5f})",
    )

    rng = np.random.default_rng(20261093)
    y = stats.genpareto.rvs(c=0.25, scale=1.0, size=250, random_state=rng)
    xi_hat, beta_hat = gpd_fit(y)
    sc = gpd_score(xi_hat, beta_hat, y)
    report.ok(
        "exact GPD (xi 0.25, beta 1), k = 250: score below 1e-6 in each component at the fit",
        bool(np.all(np.abs(sc) < 1e-6)),
        f"xi {xi_hat:.5f}, beta {beta_hat:.5f}, score {sc[0]:.1e}, {sc[1]:.1e}",
    )
    c_sp, _, s_sp = stats.genpareto.fit(y, floc=0)
    ll_own, ll_sp = -gpd_nll((xi_hat, beta_hat), y), -gpd_nll((c_sp, s_sp), y)
    report.ok(
        "its log-likelihood is no lower than scipy.stats.genpareto.fit (location 0) less 1e-8",
        bool(ll_own >= ll_sp - 1e-8),
        f"{ll_own:.10f} against {ll_sp:.10f}",
    )

    alpha_t = 4.0
    u_p = 0.05 ** (-1 / alpha_t)
    errs = []
    for q in (0.99, 0.995):
        var_true = (1 - q) ** (-1 / alpha_t)
        es_true = var_true * alpha_t / (alpha_t - 1)
        v = pot_var(u_p, 1 / alpha_t, u_p / alpha_t, 0.05, q)
        errs += [abs(v - var_true), abs(pot_es(v, u_p, 1 / alpha_t, u_p / alpha_t) - es_true)]
    report.ok(
        "Pareto tail (alpha 4): POT VaR and ES at 99 and 99.5% with the true GPD of the excesses"
        " reproduce the closed forms to 1e-10",
        max(errs) < 1e-10,
        f"largest error {max(errs):.1e}",
    )
    return u95, hill_pop


# ---------------------------------------------------------------------------------------------
def report_diagnostics(u95: float, hill_pop: float) -> None:
    """Part C: the reported diagnostics, with no pass threshold.

    Args:
        u95: The 95th percentile of the t4 distribution, from part B.
        hill_pop: The population Hill functional of t4 at u95, from part B.
    """
    print("== Diagnostics (reported, no pass threshold)")
    n, k, nu = N_SAMPLE, K_TOP, NU
    rng = np.random.default_rng(20261094)
    shapes = np.array(
        [
            gpd_fit(stats.genpareto.rvs(c=0.25, scale=1.0, size=250, random_state=rng))[0]
            for _ in range(500)
        ]
    )
    print(
        f"  ML shape over 500 exact-GPD samples of 250 (seed 20261094): mean {shapes.mean():.6f},"
        f" s.e. {shapes.std(ddof=1) / math.sqrt(500):.6f},"
        f" mean - 0.25 = {shapes.mean() - 0.25:+.6f} (finite-sample ML bias; the freeze"
        " reproduction"
        " with the planning seed 20261021 gave 0.237276)"
    )

    pop95 = kl_best_gpd(u95, nu)
    print(
        f"  population GPD fit to t4 excesses over the 95th percentile: xi {pop95[0]:.4f}, beta"
        f" {pop95[1]:.4f}"
    )
    rng = np.random.default_rng(20261095)
    xs = rng.standard_t(nu, n)
    h5 = hill(xs, k)
    srt = np.sort(xs)
    u_s = srt[-(k + 1)]
    ys = srt[-k:] - u_s
    g5 = gpd_fit(ys)
    print(
        f"  n = 5,000 t4 sample: Hill {h5:.4f} and GPD shape {g5[0]:.4f}, against 0.25 and the"
        f" population values {hill_pop:.4f} and {pop95[0]:.4f}"
    )
    for q in (0.99, 0.995):
        v_hat = pot_var(u_s, g5[0], g5[1], k / n, q)
        v_pop = pot_var(u95, pop95[0], pop95[1], 0.05, q)
        print(
            f"    {100 * q:.1f}%: VaR {v_hat:.4f} (true {stats.t.ppf(q, nu):.4f}, population GPD"
            f" {v_pop:.4f}); ES {pot_es(v_hat, u_s, *g5):.4f} (true {t_es(q, nu):.4f}, population"
            " GPD"
            f" {pot_es(v_pop, u95, *pop95):.4f})"
        )
    cover = {"pop": 0, "asym": 0}
    widths = []
    for i in range(200):
        xi_s = np.random.default_rng(20261100 + i).standard_t(nu, n)
        rb = np.random.default_rng(20261300 + i)
        hs = np.empty(1_000)
        for j in range(1_000):
            hs[j] = hill(xi_s[rb.integers(0, n, n)], k)
        lo, hi = np.quantile(hs, [0.025, 0.975])
        cover["pop"] += lo <= hill_pop <= hi
        cover["asym"] += lo <= 0.25 <= hi
        widths.append(hi - lo)
    print(
        f"  Hill 95% percentile bootstrap (1,000 resamples) over 200 samples: covers 0.348898 in"
        f" {cover['pop']} and 0.25 in {cover['asym']} of 200; mean width {np.mean(widths):.4f}"
    )
    rb = np.random.default_rng(20261097)
    boot_shapes = []
    for _ in range(1_000):
        s_b = np.sort(xs[rb.integers(0, n, n)])
        boot_shapes.append(gpd_fit(s_b[-k:] - s_b[-(k + 1)], start=(g5[0], g5[1]))[0])
    blo, bhi = np.quantile(boot_shapes, [0.025, 0.975])
    print(
        f"  GPD shape, single-sample 95% bootstrap interval (1,000 resamples): [{blo:.4f},"
        f" {bhi:.4f}]"
    )
    print(
        "  threshold sensitivity on the n = 5,000 sample (estimate / population value at that"
        " threshold):"
    )
    for qth in (0.90, 0.95, 0.975, 0.99):
        kk = round(n * (1 - qth))
        uq = stats.t.ppf(qth, nu)
        hp = integrate.quad(lambda x: stats.t.sf(x, nu) / x, uq, np.inf, epsabs=1e-13)[0] / (
            1 - qth
        )
        gp = kl_best_gpd(uq, nu)
        gq = gpd_fit(srt[-kk:] - srt[-(kk + 1)])
        print(
            f"    {100 * qth:5.1f}% (k = {kk:3d}): Hill {hill(xs, kk):.4f} / {hp:.4f}; GPD shape"
            f" {gq[0]:.4f} / {gp[0]:.4f}"
        )


# ---------------------------------------------------------------------------------------------
def report_garch() -> None:
    """Part D, reported: the two-step method, GARCH(1,1) filtering then a GPD on the residuals."""
    print("== Diagnostic: the two-step (GARCH then GPD) method on GARCH(1,1)-t returns")
    k = K_TOP
    omega, a_g, b_g, nu_g, n_g, burn = 1e-6, 0.08, 0.90, 6, 5_000, 1_000
    rng = np.random.default_rng(20261098)
    zt = rng.standard_t(nu_g, n_g + burn + 1) / math.sqrt(nu_g / (nu_g - 2))
    s2 = np.empty(n_g + burn + 1)
    r = np.empty(n_g + burn)
    s2[0] = omega / (1 - a_g - b_g)
    for t in range(n_g + burn):
        r[t] = math.sqrt(s2[t]) * zt[t]
        s2[t + 1] = omega + a_g * r[t] ** 2 + b_g * s2[t]
    r, s2_next = r[burn:], s2[-1]

    fit = optimize.minimize(
        garch_nll,
        x0=[2e-6, 0.05, 0.9],
        args=(r,),
        method="Nelder-Mead",
        options={"xatol": 1e-10, "fatol": 1e-10, "maxiter": 4_000},
    ).x
    v = np.empty(r.size)
    v[0] = r.var()
    for t in range(1, r.size):
        v[t] = fit[0] + fit[1] * r[t - 1] ** 2 + fit[2] * v[t - 1]
    sig_next = math.sqrt(fit[0] + fit[1] * r[-1] ** 2 + fit[2] * v[-1])
    res_loss = np.sort(-r / np.sqrt(v))
    u_r = res_loss[-(k + 1)]
    gr = gpd_fit(res_loss[-k:] - u_r)
    scale_t = math.sqrt((nu_g - 2) / nu_g)
    for q in (0.99, 0.995):
        vz = pot_var(u_r, gr[0], gr[1], k / n_g, q)
        true_q = stats.t.ppf(q, nu_g) * scale_t
        print(
            f"  {100 * q:.1f}%: one-day conditional VaR {sig_next * vz:.5f} (true"
            f" {math.sqrt(s2_next) * true_q:.5f}); ES {sig_next * pot_es(vz, u_r, *gr):.5f} (true"
            f" {math.sqrt(s2_next) * scale_t * t_es(q, nu_g):.5f})"
        )
    print(
        f"  fitted GARCH (omega, alpha, beta) {fit[0]:.2e}, {fit[1]:.4f}, {fit[2]:.4f}; residual"
        " GPD"
        f" shape {gr[0]:.4f} (t6 asymptotic 1/6 = 0.1667)"
    )


def main() -> int:
    """Print the versions, then run the four parts with one report.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
    report = CheckReport()
    check_rmfi(report)
    u95, hill_pop = check_known_truth(report)
    report_diagnostics(u95, hill_pop)
    report_garch()
    if report.failures:
        print("FAILED:", ", ".join(report.failures))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
