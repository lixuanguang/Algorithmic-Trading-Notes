"""Return predictability: the present-value identity, nested forecasts and restricted forecasts."""

import sys
from collections.abc import Iterator, Sequence
from typing import Final

import numpy as np
import pandas as pd
from numpy.typing import NDArray

from trading_notes.data_folders import DataFolder
from trading_notes.numerical.report import CheckReport, print_versions
from trading_notes.numerical.repository import repository_root
from trading_notes.numerical.return_predictability.forecast_evaluation import (
    NestedComparison,
    RecursiveForecasts,
    lstsq_forecasts,
    mean_t,
    ols_slope,
)
from trading_notes.numerical.return_predictability.labelled_table import LabelledTable, lagged
from trading_notes.numerical.return_predictability.present_value import (
    Linearisation,
    ReturnPanel,
    log1pexp,
)
from trading_notes.records import Record

type Floats = NDArray[np.float64]

DATA: Final = DataFolder(subsection="return_predictability").inputs
GAMMA, W_MAX = 3.0, 1.5
REPS, R0 = 5000, 120
REPS_X, PS_X = 20000, (120, 240, 720)


def adj_r2(r2: float, t: int, k: int = 2) -> float:
    """Return the adjusted R^2 of a regression with k coefficients on t observations."""
    return 1 - (1 - r2) * (t - 1) / (t - k)


def var1(x: Floats) -> float:
    """Return the sample variance with divisor n - 1."""
    return float(np.var(x, ddof=1))


class Annual(Record):
    """The annual panel with the columns parts A and B use.

    Attributes:
        panel: Returns and ratios, CRSP returns where they exist.
        r_A: log(1 + R_A), R_A built from Index and D12 in every year.
        eqp: The log equity premium, log(1 + R) - log(1 + Rfree).
        crsp: CRSP's simple return (NaN before 1926).
    """

    panel: ReturnPanel
    r_A: Floats
    eqp: Floats
    crsp: Floats


def check_linearisation_points(report: CheckReport) -> None:
    """A0: the two linearisation points on hand examples."""
    print("\n== A0. linearisation points: hand checks")
    R3, dd3 = np.array([0.5, -0.3, 0.1]), np.array([0.02, 0.04, 0.0])
    rho3 = Linearisation.working_paper(R3, dd3).rho
    rho3_meanlog = np.exp(-(np.mean(np.log1p(R3)) - dd3.mean()))
    report.ok(
        "working-paper rho uses log(1 + mean R): R = 0.5, -0.3, 0.1 and dd = 0.02, 0.04, 0 give"
        " exp(0.02)/1.1",
        bool(abs(rho3 - np.exp(0.02) / 1.1) < 1e-15 and abs(rho3 - rho3_meanlog) > 0.04),
        f"{rho3:.6f}; the mean log return would give {rho3_meanlog:.6f}",
    )
    PD, g_ss = (
        25.0,
        0.02,
    )  # steady state: constant price-dividend ratio and growth, so R is constant
    R_ss = (PD + 1) / PD * np.exp(g_ss) - 1
    rho_ss_wp = Linearisation.working_paper(np.full(5, R_ss), np.full(5, g_ss)).rho
    report.ok(
        "steady state: the working-paper rho equals PD/(1 + PD), the mean-pd rho",
        abs(rho_ss_wp - PD / (1 + PD)) < 1e-12
        and abs(Linearisation(point=float(np.log(PD))).rho - PD / (1 + PD)) < 1e-15,
        f"{rho_ss_wp:.12f} against {PD / (1 + PD):.12f}",
    )


def check_exact_identity(report: CheckReport, ann: Annual) -> None:
    """A1: the exact identity on annual S&P 500 data, the return built from Index and D12."""
    print(
        "\n== A1. exact identity, annual S&P 500 data, return built from Index and D12 in every"
        " year"
    )
    p = ann.panel
    exact = p.dd - lagged(p.pd) + log1pexp(p.pd)
    rows = p.rows(1872, 2025)
    gap = np.max(np.abs((ann.r_A - exact)[rows]))
    report.ok(
        "A1 exact identity r_t = dd_t - pd_{t-1} + log(1 + e^{pd_t}) for every year 1872-2025",
        bool(gap < 1e-12),
        f"max gap {gap:.1e}",
    )
    crsp_rows = p.rows(1926, 2025)
    mis = (np.log1p(ann.crsp) - ann.r_A)[crsp_rows]
    largest = p.labels[crsp_rows][np.argmax(np.abs(mis))]
    corr = np.corrcoef(np.log1p(ann.crsp[crsp_rows]), ann.r_A[crsp_rows])[0, 1]
    print(
        "     reported separately: CRSP log return less the Index-and-D12 log return, 1926-2025:"
        f" mean {mis.mean():+.5f}, sd {np.std(mis, ddof=1):.4f}, largest {np.abs(mis).max():.4f}"
        f" ({largest}), correlation of the two returns {corr:.4f}"
    )


def check_taylor_remainder(
    report: CheckReport, ann: Annual
) -> dict[tuple[int, int, str], tuple[float, float, float]]:
    """A2: the first-order approximation's remainder at two expansion points.

    Returns:
        (rho, variance ratio, correlation) for each sample and point.
    """
    print("\n== A2. first-order approximation: the pure Taylor remainder at two expansion points")
    p = ann.panel
    results = {}
    for lo, hi in ((1872, 1986), (1872, 2025)):
        a, w = p.rows(lo - 1, hi), p.rows(lo, hi)
        points = {
            # over lo - 1, ..., hi, the pd values the identity uses
            "mean pd": Linearisation(point=float(np.mean(p.pd[a]))),
            "working paper": Linearisation.working_paper(p.index_return[w], p.dd[w]),
        }
        for name, lin in points.items():
            pdbar, rho = lin.point, lin.rho
            approx = lin.approximation(p.pd, p.dd)[w]
            r_w = ann.r_A[w]
            rem = r_w - approx
            taylor = log1pexp(p.pd[w]) - log1pexp(pdbar) - rho * (p.pd[w] - pdbar)
            vr, corr = var1(rem) / var1(r_w), float(np.corrcoef(r_w, approx)[0, 1])
            results[(lo, hi, name)] = (rho, vr, corr)
            extra = ""
            if name == "working paper":
                extra = (
                    f"; log(1 + mean R) {np.log1p(np.mean(p.index_return[w])):.4f}, mean dd"
                    f" {np.mean(p.dd[w]):.4f}"
                )
            print(
                f"     {lo}-{hi}, {name} point: pd-bar {pdbar:.4f}, rho {rho:.4f}{extra}\n"
                f"       remainder: mean {rem.mean():.5f}, min {rem.min():.1e}, max"
                f" {rem.max():.4f}, variance ratio {vr:.5f}, corr(r, approximation) {corr:.5f}"
            )
            report.ok(
                f"A2 {lo}-{hi}, {name}: the remainder is log(1+e^pd) less its tangent at pd-bar, in"
                " [0, (pd - pd-bar)^2/8]",
                bool(
                    np.abs(rem - taylor).max() < 1e-12
                    and rem.min() >= -1e-12
                    and (rem <= (p.pd[w] - pdbar) ** 2 / 8 + 1e-12).all()
                ),
                f"max |remainder - tangent gap| {np.abs(rem - taylor).max():.1e}",
            )
            if name == "mean pd":  # the protocol's gate applies to its linearisation constant
                report.ok(
                    f"A2 {lo}-{hi}: error variance below 0.5% of var(r) and correlation above 0.99",
                    vr < 0.005 and corr > 0.99,
                )
        approx_m = points["mean pd"].approximation(p.pd, p.dd)
        r_crsp = p.r[w]  # the first run's return: CRSP from 1926
        e_crsp = r_crsp - approx_m[w]
        print(
            f"     {lo}-{hi}, mean pd point, with CRSP returns from 1926 as in the first run"
            f" (remainder plus mismatch): variance ratio {var1(e_crsp) / var1(r_crsp):.5f}"
        )
    print(
        "     nominal data: Campbell and Shiller's Table 1a (0.0008, 0.9996) is for PPI-deflated"
        " returns at the working-paper\n"
        "     point; these rows illustrate the approximation on nominal data and do not reproduce"
        " that table"
    )
    return results


def check_forward_solution(report: CheckReport, ann: Annual) -> None:
    """A3: iterating the identity forward rebuilds pd_t, 1872-2025, at the mean pd point."""
    print("\n== A3. forward solution, 1872-2025, mean pd point")
    p = ann.panel
    a = p.rows(1871, 2025)
    lin = Linearisation(point=float(np.mean(p.pd[a])))
    rho, k = lin.rho, lin.k
    eps = (ann.r_A - lin.approximation(p.pd, p.dd))[a]
    pd_, dd, rr = p.pd[a], p.dd[a], ann.r_A[a]
    for J in (1, 5, 10, 20):
        worst = 0.0
        for t in range(0, len(pd_) - J):
            js = np.arange(1, J + 1)
            rebuilt = (
                np.sum(rho ** (js - 1) * (k + dd[t + js] - rr[t + js] + eps[t + js]))
                + rho**J * pd_[t + J]
            )
            worst = max(worst, abs(rebuilt - pd_[t]))
        report.ok(
            f"A3 iterating {J} years forward rebuilds pd_t with remainders and terminal term kept",
            worst < 1e-10,
            f"max gap {worst:.1e}; terminal weight rho^J = {rho**J:.3f}",
        )


def check_coefficient_restriction(
    report: CheckReport, ann: Annual
) -> dict[tuple[int, int], tuple[float, float, float, float, float]]:
    """A4: b_r - b_d + rho phi = 1 + b_eps at each sample's mean pd point.

    Returns:
        (b_r, b_d, phi, rho, b_eps) for each sample.
    """
    print("\n== A4. coefficient restriction, mean pd point of each sample")
    p = ann.panel
    a4 = {}
    for lo, hi in ((1927, 2004), (1872, 2025)):
        s, w = p.rows(lo - 1, hi), p.rows(lo, hi)
        lin = Linearisation(point=float(np.mean(p.pd[s])))
        rho_s = lin.rho
        eps = ann.r_A - lin.approximation(p.pd, p.dd)
        mis = np.log1p(p.R) - ann.r_A  # CRSP less constructed (zero before 1926)
        x = p.dp_lag[w]
        b_r, b_d = ols_slope(x, ann.r_A[w]), ols_slope(x, p.dd[w])
        phi, b_e = ols_slope(x, p.dp[w]), ols_slope(x, eps[w])
        lhs = b_r - b_d + rho_s * phi
        a4[(lo, hi)] = (b_r, b_d, phi, rho_s, b_e)
        report.ok(
            f"A4 {lo}-{hi}: b_r - b_d + rho*phi = 1 + b_eps",
            abs(lhs - (1 + b_e)) < 1e-10,
            f"b_r {b_r:.3f}, b_d {b_d:.3f}, phi {phi:.3f}, rho {rho_s:.4f}, b_eps {b_e:.4f}, b_r -"
            f" b_d + rho*phi = {lhs:.4f}",
        )
        blr = b_r / (1 - rho_s * phi)
        print(
            f"     long-run return coefficient b_r/(1 - rho*phi) = {blr:.2f}, dividend-growth share"
            f" -b_d/(1 - rho*phi) = {-b_d / (1 - rho_s * phi):.2f}; reported separately: slope of"
            f" CRSP log returns {ols_slope(x, np.log1p(p.R[w])):.3f} (= b_r + slope of the"
            f" mismatch, {ols_slope(x, mis[w]):+.3f})"
        )
    return a4


def check_hand_example(report: CheckReport) -> None:
    """B1: recursive forecasts and the statistics' algebra on eight observations."""
    print("\n== B1. hand example: recursive forecasts and the statistics' algebra")
    x8 = np.array([3.0, 3.4, 2.9, 3.8, 3.1, 3.6, 4.0, 3.3])
    y8 = np.array([0.4, 1.2, -0.3, 2.0, 0.1, 1.5, 0.9, -0.6])
    first8 = 4
    forecast = RecursiveForecasts.of(x8, y8, first8)
    fa, fn = forecast.regression, forecast.mean
    report.ok(
        "recursive OLS by running sums equals lstsq refitted at each origin",
        np.allclose(fa, lstsq_forecasts(x8, y8, first8), atol=1e-12, rtol=0),
    )
    report.ok(
        "historical-mean forecast equals the mean of earlier outcomes",
        np.allclose(fn, [y8[:i].mean() for i in range(first8, 8)], atol=1e-14, rtol=0),
    )
    st = NestedComparison.of(y8[first8:], fa, fn)
    e_a, e_n = y8[first8:] - fa, y8[first8:] - fn
    report.ok(
        "Clark-West: mean f = MSE_N - (MSE_A - adj)",
        abs(st.CW_mean - (st.mse_n - (st.mse_a - st.adj))) < 1e-12,
    )
    report.ok(
        "Clark-West: mean f = 2 mean(e_N (e_N - e_A)) (eq. (4.1))",
        bool(abs(st.CW_mean - 2 * np.mean(e_n * (e_n - e_a))) < 1e-12),
    )
    report.ok(
        "ENC = P mean(f) / (2 MSE_A)", abs(st.ENC - st.P * st.CW_mean / (2 * st.mse_a)) < 1e-12
    )
    report.ok(
        "R2_OS and DeltaRMSE have the same sign", bool(np.sign(st.R2_OS) == np.sign(st.dRMSE))
    )
    print("     forecasts A", np.round(fa, 4), "N", np.round(fn, 4))
    print(
        f"     P {st.P}, MSE_N {st.mse_n:.4f}, MSE_A {st.mse_a:.4f}, adj {st.adj:.4f}, R2_OS"
        f" {st.R2_OS:.4f}, MSE-F {st.MSE_F:.4f}, ENC {st.ENC:.4f}, CW mean {st.CW_mean:.4f}, CW t"
        f" {st.CW_t:.4f}"
    )


def check_timing(report: CheckReport) -> None:
    """B2: overwriting the future leaves earlier forecasts unchanged."""
    print("\n== B2. timing: overwriting the future leaves earlier forecasts unchanged")
    rng_t = np.random.default_rng(7)
    xt, yt = rng_t.normal(size=60), rng_t.normal(size=60)
    forecast = RecursiveForecasts.of(xt, yt, 20)
    base_a, base_n = forecast.regression, forecast.mean
    for cut in (25, 40, 55):
        y2, x2 = yt.copy(), xt.copy()
        y2[cut:] = 1e6  # the forecast of y[cut] must not see y[cut] itself
        # x[i] is known before y[i]; forecasts of y[i], i <= cut, use x[i] and pairs before i
        x2[cut + 1 :] = -1e6
        forecast = RecursiveForecasts.of(x2, y2, 20)
        a2, n2 = forecast.regression, forecast.mean
        m = cut - 20 + 1
        report.ok(
            f"forecasts for periods up to {cut} unchanged",
            np.array_equal(a2[:m], base_a[:m]) and np.array_equal(n2[:m], base_n[:m]),
        )


def simulate_dgp1(
    rng: np.random.Generator, reps: int, n: int, gamma: float
) -> tuple[Floats, Floats]:
    """Return (x, y) of Clark and West's DGP 1 (eq. (6.1)), reps x n, y[t] predicted by z[t]."""
    u1, u2 = rng.standard_normal((2, reps, n))
    v = np.sqrt(0.025) * u1
    e = np.sqrt(18.0) * (-0.75 * u1 + np.sqrt(1 - 0.75**2) * u2)
    z = np.empty((reps, n + 1))
    z[:, 0] = 3.0 + np.sqrt(0.025 / (1 - 0.95**2)) * rng.standard_normal(reps)
    for t in range(n):
        z[:, t + 1] = 0.15 + 0.95 * z[:, t] + v[:, t]
    y = 0.5 + gamma * z[:, :-1] + e  # y[t] uses z[t], which precedes it
    return z[:, :-1], y


def mc_rates(x: Floats, y: Floats, first: int) -> tuple[Floats, Floats, Floats]:
    """Return each replication's mean MSPE difference and its Clark-West and unadjusted t."""
    forecast = RecursiveForecasts.of(x, y, first)
    fa, fn = forecast.regression, forecast.mean
    yy = y[:, first:]
    e_a, e_n = yy - fa, yy - fn
    d = e_n**2 - e_a**2
    f = d + (fn - fa) ** 2
    return d.mean(axis=1), mean_t(f), mean_t(d)


def size_gap(ours: float, n_ours: int, pub: float, n_pub: int = 5000) -> tuple[float, float]:
    """Return the difference of two simulated rejection rates and its standard error."""
    se = np.sqrt(ours * (1 - ours) / n_ours + pub * (1 - pub) / n_pub)
    return ours - pub, float(se)


class SizeResults(Record):
    """Part B3's simulated rejection rates.

    Attributes:
        mc: (Clark-West, unadjusted) size at each P.
        power: (Clark-West, unadjusted) power at gamma = 0.35, P = 240.
    """

    mc: dict[int, tuple[float, float]]
    power: tuple[float, float]


def check_size(report: CheckReport) -> SizeResults:
    """B3: Monte Carlo of Clark and West's DGP 1, recursive, R = 120, 5,000 replications."""
    print(
        "\n== B3. Monte Carlo, Clark and West's DGP 1 (eq. (6.1)), recursive, R = 120, 5,000"
        " replications"
    )
    rng = np.random.default_rng(20261022)
    published = {120: (0.085, 0.028), 240: (0.070, 0.012)}
    mc = {}
    for P in (120, 240):
        x, y = simulate_dgp1(rng, REPS, R0 + P, 0.0)
        dmean, t_cw, t_n = mc_rates(x, y, R0)
        mc_t = dmean.mean() / (dmean.std(ddof=1) / np.sqrt(REPS))
        rej_cw, rej_n = float(np.mean(t_cw > 1.282)), float(np.mean(t_n > 1.282))
        mc[P] = (rej_cw, rej_n)
        print(
            f"     P = {P}: mean MSE_N - MSE_A = {dmean.mean():.3f} (MC t {mc_t:.1f}); Clark-West"
            f" size {rej_cw:.3f} (published {published[P][0]}); unadjusted {rej_n:.3f} (published"
            f" {published[P][1]})"
        )
        report.ok(
            f"P = {P}: the unadjusted MSPE difference favours the historical mean under the null",
            bool(mc_t < -5),
        )
        report.ok(
            f"P = {P}: Clark-West size in [0.04, 0.11] and within 0.02 of Clark and West",
            0.04 <= rej_cw <= 0.11 and abs(rej_cw - published[P][0]) <= 0.02,
        )
        report.ok(f"P = {P}: unadjusted test rejects in less than 3% of replications", rej_n < 0.03)
    x, y = simulate_dgp1(rng, REPS, R0 + 240, 0.35)
    _, t_cw, t_n = mc_rates(x, y, R0)
    pow_cw, pow_n = float(np.mean(t_cw > 1.282)), float(np.mean(t_n > 1.282))
    report.ok(
        "gamma = 0.35, P = 240: Clark-West rejects more often than the unadjusted test",
        pow_cw > pow_n,
        f"{pow_cw:.3f} against {pow_n:.3f}",
    )
    for P in (120, 240):
        d, se = size_gap(mc[P][0], REPS, published[P][0])
        print(
            f"     P = {P}, Clark-West size {mc[P][0]:.3f} less published {published[P][0]:.3f} ="
            f" {d:+.3f}; standard error of the difference {se:.4f} (both runs, 5,000 replications"
            f" each), {d / se:+.1f} standard errors"
        )
    return SizeResults(mc=mc, power=(pow_cw, pow_n))


def simulate_source_design(
    rng: np.random.Generator, reps: int, n_total: int, gamma: float, chunk: int = 2000
) -> Iterator[tuple[Floats, Floats, Floats]]:
    """Yield Clark and West's (2006, p. 15) design in chunks of replications.

    One path of R + 720 observations per replication, shared by every P; the first
    observation of (y, z) drawn from the stationary distribution (here by drawing the lagged z,
    which gives the same joint law); y_1 has no observed lagged z, so the regression uses pairs
    from observation 2 and the mean uses all.
    """
    for start in range(0, reps, chunk):
        x, y = simulate_dgp1(rng, min(chunk, reps - start), n_total, gamma)
        yield x[:, 1:], y[:, 1:], y


def window_sums(a: Floats) -> Floats:
    """Return running sums along rows with a leading zero column."""
    sums: Floats = np.concatenate([np.zeros((a.shape[0], 1)), np.cumsum(a, axis=1)], axis=1)
    return sums


def source_rates(
    x2: Floats, y2: Floats, y: Floats, R: int, P: int, window: int | None = None
) -> tuple[NDArray[np.bool_], Floats]:
    """Return each replication's rejections (Clark-West, unadjusted) and three mean statistics.

    Recursive forecasts when window is None; otherwise rolling, on the last R observations
    (R - 1 pairs for the regression, whose first pair needs y_{t-R}).
    """
    n = y.shape[1]
    if window is None:
        fa = RecursiveForecasts.of(x2, y2, R - 1).regression
        fn = RecursiveForecasts.of(y, y, R).mean
    else:
        i = np.arange(R, n)
        sy = window_sums(y)
        fn = (sy[:, i] - sy[:, i - R]) / R
        X, Y = x2, y2
        sx, syy, sxx, sxy = window_sums(X), window_sums(Y), window_sums(X * X), window_sums(X * Y)
        j, j0 = i - 1, i - R  # pairs at positions j0, ..., j - 1 of the shifted arrays
        m = (j - j0).astype(float)
        gx, gy, gxx, gxy = (q[:, j] - q[:, j0] for q in (sx, syy, sxx, sxy))
        b = (m * gxy - gx * gy) / (m * gxx - gx * gx)
        fa = (gy - b * gx) / m + b * x2[:, j]
    fa, fn, yy = fa[:, :P], fn[:, :P], y[:, R : R + P]
    e_a, e_n = yy - fa, yy - fn
    d = e_n**2 - e_a**2
    f = d + (fn - fa) ** 2
    return np.c_[mean_t(f) > 1.282, mean_t(d) > 1.282], np.c_[
        d.mean(1), f.mean(1), ((fn - fa) ** 2).mean(1)
    ]


def report_source_design() -> dict[tuple[str, int], tuple[Floats, Floats]]:
    """B3b: the size gap in the source's own design, seed 20261104 (reported only)."""
    print(
        "\n== B3b. investigation of the size gap (reported only; no verdict): the source's design,"
        " seed 20261104"
    )
    rng_x = np.random.default_rng(20261104)
    parts: dict[tuple[str, int], list[tuple[NDArray[np.bool_], Floats]]] = {
        (s, P): [] for s in ("recursive", "rolling") for P in PS_X
    }
    for x2, y2, y in simulate_source_design(rng_x, REPS_X, R0 + 720, 0.0):
        for scheme, window in (("recursive", None), ("rolling", R0)):
            for P in PS_X:
                parts[(scheme, P)].append(source_rates(x2, y2, y, R0, P, window))
    inv = {
        key: (
            np.concatenate([v[0] for v in vals]).mean(axis=0),
            np.concatenate([v[1] for v in vals]).mean(axis=0),
        )
        for key, vals in parts.items()
    }
    table1 = {
        ("recursive", 120): (0.085, 0.028),
        ("recursive", 240): (0.070, 0.012),
        ("recursive", 720): (0.054, 0.003),
        ("rolling", 120): (0.085, 0.018),
        ("rolling", 240): (0.078, 0.006),
        ("rolling", 720): (0.091, 0.000),
    }
    for (scheme, P), (rates, _) in inv.items():
        d, se = size_gap(float(rates[0]), REPS_X, table1[(scheme, P)][0])
        print(
            f"     {scheme:9s} P = {P}: Clark-West {rates[0]:.4f} (Table 1"
            f" {table1[(scheme, P)][0]:.3f}; difference {d:+.4f}, s.e. {se:.4f}, {d / se:+.1f}"
            f" s.e.), unadjusted {rates[1]:.4f} ({table1[(scheme, P)][1]:.3f})"
        )
    m720 = inv[("rolling", 720)][1]
    print(
        f"     rolling, P = 720, means over replications: MSE_N - MSE_A {m720[0]:+.3f}, adjusted"
        f" {m720[1]:+.3f}, mean squared forecast difference {m720[2]:.3f} (Clark and West, p. 16:"
        " -0.24, 0.01 and 0.25)"
    )
    return inv


def annual_oos(ann: Annual, lo: int, hi: int, first_year: int) -> tuple[NestedComparison, Floats]:
    """Return the dividend-price model against the historical mean, and the recursive slopes."""
    w = ann.panel.rows(lo, hi)
    x, y = ann.panel.dp_lag[w], ann.eqp[w]
    first = int(np.where(ann.panel.labels[w] == first_year)[0][0])
    forecast = RecursiveForecasts.of(x, y, first)
    fa, fn, b = forecast.regression, forecast.mean, forecast.slope
    return NestedComparison.of(y[first:], fa, fn), b


def check_welch_goyal(report: CheckReport, ann: Annual) -> dict[int, NestedComparison]:
    """B4: Welch and Goyal's annual dividend-price row (data 1872-2005); B5 start dates."""
    print("\n== B4. Welch and Goyal's annual dividend-price row (data 1872-2005)")
    w = ann.panel.rows(1872, 2005)
    eqp = ann.eqp[w]
    X = np.column_stack([np.ones(int(w.sum())), ann.panel.dp_lag[w]])
    coef, res = np.linalg.lstsq(X, eqp, rcond=None)[:2]
    r2_is = 1 - res[0] / np.sum((eqp - eqp.mean()) ** 2)
    r2_is_adj = 100 * adj_r2(float(r2_is), int(w.sum()))
    print(
        f"     in sample: slope {coef[1]:.4f}, R2 {100 * r2_is:.2f}%, adjusted {r2_is_adj:.2f}%"
        " (Welch and Goyal 0.49)"
    )
    report.ok("in-sample adjusted R2 within 0.25 points of 0.49", abs(r2_is_adj - 0.49) <= 0.25)
    wg = {}
    for first_year, pub_adj, pub_drmse in ((1892, -2.06, -0.11), (1965, -3.69, -0.09)):
        s, _ = annual_oos(ann, 1872, 2005, first_year)
        wg[first_year] = s
        adj = 100 * adj_r2(s.R2_OS, s.P)
        print(
            f"     forecasts from {first_year}: P {s.P}, R2_OS {100 * s.R2_OS:.2f}%, adjusted"
            f" {adj:.2f}% (published {pub_adj}), DeltaRMSE {100 * s.dRMSE:.2f} (published"
            f" {pub_drmse}), MSE-F {s.MSE_F:.2f}, ENC {s.ENC:.2f}, Clark-West t {s.CW_t:.2f}"
        )
        report.ok(
            f"forecasts from {first_year}: DeltaRMSE within 0.05 points of {pub_drmse}",
            abs(100 * s.dRMSE - pub_drmse) <= 0.05,
        )
    print("\n== B5. start-date sensitivity (reported only)")
    for hi in (2005, 2025):
        for first_year in (1892, 1927, 1947, 1965, 1985):
            s, b = annual_oos(ann, 1872, hi, first_year)
            print(
                f"     {first_year}-{hi}: P {s.P:3d}, R2_OS {100 * s.R2_OS:6.2f}%, Clark-West t"
                f" {s.CW_t:5.2f}, slope range {b.min():.3f} to {b.max():.3f}"
            )
    return wg


def check_weights_hand_example(report: CheckReport) -> None:
    """C1: weights, portfolio returns and utility on three months."""
    print("\n== C1. hand example: weights, portfolio returns and utility")
    mu = np.array([0.006, -0.002, 0.030])
    var = np.array([0.0020, 0.0020, 0.0018])
    r_m = np.array([0.020, -0.050, 0.010])
    r_f = np.array([0.003, 0.003, 0.003])
    wts = np.clip(mu / (GAMMA * var), 0.0, W_MAX)
    report.ok(
        "weights 1.0, 0 (no short sales) and 1.5 (leverage cap)",
        np.allclose(wts, [1.0, 0.0, 1.5], atol=1e-12, rtol=0),
        str(np.round(mu / (GAMMA * var), 4)),
    )
    rp = r_f + wts * (r_m - r_f)
    report.ok(
        "portfolio returns 0.020, 0.003 and 0.0135",
        np.allclose(rp, [0.020, 0.003, 0.0135], atol=1e-12, rtol=0),
    )
    u = rp.mean() - GAMMA / 2 * rp.var(ddof=1)
    report.ok(
        "utility = mean - (gamma/2) var",
        bool(abs(u - (0.0365 / 3 - 1.5 * np.sum((rp - 0.0365 / 3) ** 2) / 2)) < 1e-15),
        f"{100 * u:.4f}% a month",
    )


class TimingResults(Record):
    """Campbell and Thompson's comparison over one sample.

    Attributes:
        P: The number of forecast months.
        R2_unres: R2_OS of the unrestricted forecast.
        R2_res: R2_OS of the restricted forecast against the floored mean.
        u_mean: Utility of the historical-mean investor, a month.
        du_unres: Utility change of the unrestricted forecast.
        du_res: Utility change of the restricted forecast.
        share_neg_slope: Share of months with a negative slope.
        share_zero_weight: Share of months with a zero restricted weight.
        share_capped: Share of months with the restricted weight at the cap.
        mean_w: Mean weights of the mean, unrestricted and restricted investors.
    """

    P: int
    R2_unres: float
    R2_res: float
    u_mean: float
    du_unres: float
    du_res: float
    share_neg_slope: float
    share_zero_weight: float
    share_capped: float
    mean_w: tuple[float, float, float]


def ct_run(monthly: ReturnPanel, xr: Floats, hi: int, first_ym: int = 192701) -> TimingResults:
    """Return Campbell and Thompson's comparison for forecasts from first_ym through hi."""
    m = monthly.rows(187102, hi)
    x, y = monthly.dp_lag[m], xr[m]
    first = int(np.where(monthly.labels[m] == first_ym)[0][0])
    forecast = RecursiveForecasts.of(x, y, first)
    fa, fn, b = forecast.regression, forecast.mean, forecast.slope
    fr = np.where(b < 0, fn, fa)  # wrong (negative) slope: drop the predictor, keep the mean
    fr = np.maximum(fr, 0.0)
    fn_floor = np.maximum(fn, 0.0)
    var_hist = np.array([y[:i].var(ddof=1) for i in range(first, len(y))])
    yy, rf = y[first:], monthly.Rfree[m][first:]

    def utility(fc: Floats) -> tuple[float, Floats]:
        wv = np.clip(fc / (GAMMA * var_hist), 0.0, W_MAX)
        rp = rf + wv * yy
        return float(rp.mean() - GAMMA / 2 * rp.var(ddof=1)), wv

    u_n, w_n = utility(fn)
    u_a, w_a = utility(fa)
    u_r, w_r = utility(fr)
    return TimingResults(
        P=len(yy),
        R2_unres=NestedComparison.of(yy, fa, fn).R2_OS,
        R2_res=NestedComparison.of(yy, fr, fn_floor).R2_OS,
        u_mean=u_n,
        du_unres=u_a - u_n,
        du_res=u_r - u_n,
        share_neg_slope=float(np.mean(b < 0)),
        share_zero_weight=float(np.mean(w_r == 0)),
        share_capped=float(np.mean(w_r == W_MAX)),
        mean_w=(float(w_n.mean()), float(w_a.mean()), float(w_r.mean())),
    )


def check_campbell_thompson(
    report: CheckReport, monthly: ReturnPanel, xr: Floats
) -> tuple[TimingResults, TimingResults]:
    """C2 and C3: Campbell and Thompson's dividend-price comparison, to 2003 and to 2025."""
    print(
        "\n== C2. Campbell and Thompson's dividend-price comparison, monthly, forecasts 1927-2003,"
        " gamma = 3, weights in [0, 1.5]"
    )
    ct = ct_run(monthly, xr, 200312)
    print(
        f"     P {ct.P}; R2_OS unrestricted {100 * ct.R2_unres:.3f}%, restricted"
        f" {100 * ct.R2_res:.3f}% (published, restricted: 0.001%)\n"
        f"     utility of the historical-mean investor {100 * ct.u_mean:.3f}% a month (published"
        f" 0.501%); change unrestricted {100 * ct.du_unres:+.3f}% (published -0.016%),"
        f" restricted {100 * ct.du_res:+.3f}% (published -0.024%)\n"
        f"     negative slope in {100 * ct.share_neg_slope:.1f}% of months; restricted weight 0 in"
        f" {100 * ct.share_zero_weight:.1f}%, at 1.5 in {100 * ct.share_capped:.1f}%; mean weights"
        f" (mean, unrestricted, restricted) {np.round(ct.mean_w, 3)}"
    )
    report.ok(
        "historical-mean investor's utility within 0.05 points of 0.501% a month",
        abs(100 * ct.u_mean - 0.501) <= 0.05,
    )
    report.ok(
        "both utility changes within 0.05 points of zero",
        abs(100 * ct.du_unres) <= 0.05 and abs(100 * ct.du_res) <= 0.05,
    )
    print("\n== C3. extended to December 2025 (reported only)")
    ct25 = ct_run(monthly, xr, 202512)
    print(
        f"     P {ct25.P}; R2_OS unrestricted {100 * ct25.R2_unres:.3f}%, restricted"
        f" {100 * ct25.R2_res:.3f}%; utility {100 * ct25.u_mean:.3f}%, change unrestricted"
        f" {100 * ct25.du_unres:+.3f}%, restricted {100 * ct25.du_res:+.3f}%"
    )
    return ct, ct25


def util(fc: Floats, yy: Floats, var_h: Floats) -> tuple[Floats, float]:
    """Return each replication's utility and the share of months at the weight cap."""
    wv = np.clip(fc / (GAMMA * var_h), 0.0, W_MAX)
    rp = wv * yy
    return rp.mean(axis=1) - GAMMA / 2 * rp.var(axis=1, ddof=1), float(np.mean(wv == W_MAX))


def history_variance(ys: Floats) -> Floats:
    """Return the variance of the outcomes observed before each forecast month from 240.

    Positions 239, ..., 718 of the running sums hold 240, ..., 719 outcomes.
    """
    csum, csum2 = np.cumsum(ys, axis=1)[:, 239:-1], np.cumsum(ys**2, axis=1)[:, 239:-1]
    nobs = np.arange(240, ys.shape[1])
    var_h: Floats = (csum2 - csum**2 / nobs) / (nobs - 1)
    return var_h


def check_synthetic_mechanism(report: CheckReport) -> Floats:
    """C4 and C5: the restriction's effect on simulated DGP 1 paths; return C5's two gains."""
    print(
        "\n== C4. synthetic mechanism: DGP 1 in monthly decimals, gamma* = 0.35, R = 240, P = 480,"
        " 1,000 replications"
    )
    rng_c = np.random.default_rng(20261023)
    xs, ys = simulate_dgp1(rng_c, 1000, 240 + 480, 0.35)
    ys = ys / 100
    forecast = RecursiveForecasts.of(xs, ys, 240)
    fa, fn, b = forecast.regression, forecast.mean, forecast.slope
    fr = np.maximum(np.where(b < 0, fn, fa), 0.0)
    var_h = history_variance(ys)
    yy = ys[:, 240:]
    (u_a, cap_a), (u_r, _), (u_n, cap_n) = (util(f, yy, var_h) for f in (fa, fr, fn))
    g_unres, g_res = u_a - u_n, u_r - u_n
    print(
        "     mean gain over the historical mean, % a month: unrestricted"
        f" {100 * g_unres.mean():.4f},"
        f" restricted {100 * g_res.mean():.4f}; share of samples with a gain:"
        f" {np.mean(g_unres > 0):.3f}, {np.mean(g_res > 0):.3f}\n"
        f"     weight at the 1.5 cap in {100 * cap_n:.1f}% of months (historical mean) and"
        f" {100 * cap_a:.1f}% (unrestricted); DGP 1's mean excess return, 0.5 + 0.35 x 3 = 1.55% a"
        " month against a variance of 18 (percent squared), asks for a weight near 2.9, so the cap"
        " binds and the predictor can hardly be used"
    )
    # C5, a supplement outside the protocol's verdicts: the same design with the intercept
    # lowered so that the mean excess return is 0.5% a month, close to the historical premium.
    print(
        "\n== C5. supplement: C4 with a mean excess return of 0.5% a month (intercept -0.55), seed"
        " 20261024"
    )
    rng_s = np.random.default_rng(20261024)
    xs5, ys5 = simulate_dgp1(rng_s, 1000, 240 + 480, 0.35)
    ys5 = (ys5 - 1.05) / 100
    forecast = RecursiveForecasts.of(xs5, ys5, 240)
    fa5, fn5, b5 = forecast.regression, forecast.mean, forecast.slope
    fr5 = np.maximum(np.where(b5 < 0, fn5, fa5), 0.0)
    var5 = history_variance(ys5)
    yy5 = ys5[:, 240:]
    (u_a5, cap_a5), (u_r5, _), (u_n5, cap_n5) = (util(f, yy5, var5) for f in (fa5, fr5, fn5))
    g5u, g5r = u_a5 - u_n5, u_r5 - u_n5
    print(
        f"     mean gain, % a month: unrestricted {100 * g5u.mean():.4f}, restricted"
        f" {100 * g5r.mean():.4f}; share with a gain {np.mean(g5u > 0):.3f},"
        f" {np.mean(g5r > 0):.3f}; restricted better than unrestricted in"
        f" {np.mean(g5r > g5u):.3f} of samples; tied in {np.mean(g5r == g5u):.3f}; cap binds in"
        f" {100 * cap_n5:.1f}% and {100 * cap_a5:.1f}% of months"
    )
    var_x = 0.35**2 * 0.025 / (1 - 0.95**2)  # variance of the predictable part, percent squared
    pop_r2, pop_s2 = var_x / (var_x + 18), 0.5**2 / (var_x + 18)
    # R2 and S2 are unit-free, so this is a decimal return
    bench = (1 / (2 * GAMMA)) * pop_r2 / (1 - pop_r2) * (1 + pop_s2)
    print(
        f"     population R2 {pop_r2:.4f}, S2 {pop_s2:.4f}; known-parameter, uncapped utility gain"
        f" (1/(2gamma))(R2/(1-R2))(1+S2) = {100 * bench:.4f}% a month (half the expected-return"
        " gain of Campbell and Thompson's eq. (8); a conditional\n"
        "     mean-variance reference: the realised measure above also counts the variation of the"
        " timed mean, so it is lower)"
    )
    xs2, ys2 = xs[:1].copy(), ys[:1].copy()
    ys2[0, 400:] = 9.0
    forecast = RecursiveForecasts.of(xs2, ys2, 240)
    fa2, fn2 = forecast.regression, forecast.mean
    report.ok(
        "C4 timing: forecasts before the overwritten months are unchanged",
        np.array_equal(fa2[0, : 400 - 240], fa[0, : 400 - 240])
        and np.array_equal(fn2[0, : 400 - 240], fn[0, : 400 - 240]),
    )
    return np.array([g5u.mean(), g5r.mean()])


def main(argv: Sequence[str] | None = None) -> int:
    """Print the versions, then run parts A, B and C and the recorded values with one report.

    Worked numbers of res:campbell-shiller-identity, meth:nested-forecast-tests and
    meth:restricted-forecast-value, under return-predictability-protocol.md (definitions, timing
    and tolerances written before the first run).

    Data: goyal-annual-1871-2025.csv and goyal-monthly-1871-2025.csv, extracted by
    trading_notes.research.return_predictability.goyal_extract from the workbook on Amit Goyal's
    page labelled "Original data (up to 2005) used in the paper", served on 2026-10-22 with data
    to December 2025 (a 2026 vintage, not the file behind the 2008 tables). Synthetic data from
    fixed seeds (20261022, 20261023, 20261024, 20261104) where the true model must be known.

    Part A builds one return from Index and D12 in every year; the working-paper linearisation
    point uses log(1 + mean R), as printed on p. 5 of NBER WP 2100, not the mean log return;
    the Taylor remainder is checked against log(1 + e^x) less its tangent and its convexity
    bounds. Independent routes: recursive OLS by running sums against numpy.linalg.lstsq
    refitted at each origin; the Clark-West statistic as the mean of f against
    2 mean(e_N (e_N - e_A)) and against MSE_N - (MSE_A - adj); ENC against the Clark-West
    numerator; the exact return identity against the log-linear one with its error kept;
    forecasts recomputed after the future is overwritten (timing). Recorded output:
    return-predictability-results.txt.

    Args:
        argv: Command-line arguments: `--root DIR`, the repository root that holds the data
            (default: the working directory).

    Returns:
        The exit status, 0 or 1.
    """
    root = repository_root(__doc__ or "", argv)
    print_versions(np, pd)
    annual_table = LabelledTable.read(root / DATA / "goyal-annual-1871-2025.csv", "yyyy")
    monthly_table = LabelledTable.read(root / DATA / "goyal-monthly-1871-2025.csv", "yyyymm")
    annual, monthly = ReturnPanel.of(annual_table, 1), ReturnPanel.of(monthly_table, 12)
    crsp_annual, crsp_monthly = (t.first_valid("CRSP_SPvw") for t in (annual_table, monthly_table))
    if crsp_annual is None or crsp_monthly is None:
        raise ValueError("an extract has no CRSP_SPvw returns")
    print(
        f"annual {annual.labels[0]}-{annual.labels[-1]}, monthly {monthly.labels[0]}-"
        f"{monthly.labels[-1]}; CRSP returns from {crsp_annual} (annual), {crsp_monthly}"
        " (monthly)"
    )
    # Part A uses one coherent annual return built from the same Index and D12 as the
    # price-dividend ratio, for every year; the CRSP return (used by parts B and C) differs
    # from it and is compared separately.
    ann = Annual(
        panel=annual,
        r_A=np.log1p(annual.index_return),
        eqp=np.log1p(annual.R) - np.log1p(annual.Rfree),
        crsp=annual_table["CRSP_SPvw"],
    )
    xr = monthly.R - monthly.Rfree
    report = CheckReport()
    check_linearisation_points(report)
    check_exact_identity(report, ann)
    a_results = check_taylor_remainder(report, ann)
    check_forward_solution(report, ann)
    a4 = check_coefficient_restriction(report, ann)
    check_hand_example(report)
    check_timing(report)
    size = check_size(report)
    inv = report_source_design()
    wg = check_welch_goyal(report, ann)
    check_weights_hand_example(report)
    ct, ct25 = check_campbell_thompson(report, monthly, xr)
    gains = check_synthetic_mechanism(report)
    print("\n== Recorded values of the first run, at their printed rounding (drift check)")
    report.ok(
        "A: pure remainder variance ratios 0.00021 and 0.00077 at the mean-pd point (rho 0.9547,"
        " 0.9634), 0.00089 and 0.00728 at the working-paper point (rho 0.9348, 0.9364)",
        [
            round(a_results[(1872, hi, n)][1], 5)
            for n in ("mean pd", "working paper")
            for hi in (1986, 2025)
        ]
        == [0.00021, 0.00077, 0.00089, 0.00728]
        and [
            round(a_results[(1872, hi, n)][0], 4)
            for n in ("mean pd", "working paper")
            for hi in (1986, 2025)
        ]
        == [0.9547, 0.9634, 0.9348, 0.9364],
    )
    report.ok(
        "A4: b_r 0.066 and 0.024, b_eps -0.0029 and -0.0032 (1927-2004, 1872-2025)",
        [round(a4[k][0], 3) for k in a4] == [0.066, 0.024]
        and [round(a4[k][4], 4) for k in a4] == [-0.0029, -0.0032],
    )
    report.ok(
        "B3b: source-design sizes, recursive 0.0722, 0.0657, 0.0551; rolling 0.0722, 0.0730,"
        " 0.0856",
        [round(float(inv[(s, P)][0][0]), 4) for s in ("recursive", "rolling") for P in PS_X]
        == [0.0722, 0.0657, 0.0551, 0.0722, 0.0730, 0.0856],
    )
    report.ok(
        "B3: Clark-West sizes 0.069 and 0.059; unadjusted 0.023 and 0.010; power 0.156 against"
        " 0.033",
        [round(v, 3) for v in (*size.mc[120], *size.mc[240], *size.power)]
        == [0.069, 0.023, 0.059, 0.010, 0.156, 0.033],
    )
    report.ok(
        "B4: R2_OS -1.32% and -1.67%; DeltaRMSE -0.13 and -0.13; Clark-West t 0.26 and 0.46",
        [round(100 * wg[y].R2_OS, 2) for y in (1892, 1965)] == [-1.32, -1.67]
        and [round(100 * wg[y].dRMSE, 2) for y in (1892, 1965)] == [-0.13, -0.13]
        and [round(wg[y].CW_t, 2) for y in (1892, 1965)] == [0.26, 0.46],
    )
    report.ok(
        "C2/C3: utility 0.492%, changes -0.018% and -0.024%; to 2025 0.517%, -0.051% and -0.055%",
        [
            round(100 * v, 3)
            for v in (ct.u_mean, ct.du_unres, ct.du_res, ct25.u_mean, ct25.du_unres, ct25.du_res)
        ]
        == [0.492, -0.018, -0.024, 0.517, -0.051, -0.055],
    )
    report.ok(
        "C5: mean gains 0.0171% and 0.0214% a month",
        [round(100 * float(g), 4) for g in gains] == [0.0171, 0.0214],
    )
    print(f"\n{report.count} checks executed")
    if report.failures:
        print("FAILED:", report.failures)
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
