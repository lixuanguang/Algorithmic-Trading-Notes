"""Forecast combination and proper scoring: the annual combination example and scoring rules."""

import sys
from collections.abc import Callable, Sequence
from fractions import Fraction
from pathlib import Path
from typing import Final

import numpy as np
import pandas as pd
import scipy
from numpy.typing import NDArray
from scipy import integrate, stats

from trading_notes.numerical.report import CheckReport, print_versions
from trading_notes.numerical.repository import repository_root
from trading_notes.numerical.return_predictability.forecast_evaluation import (
    RecursiveForecasts,
    lstsq_forecasts,
)
from trading_notes.numerical.return_predictability.labelled_table import LabelledTable
from trading_notes.numerical.return_predictability.scoring_rules import (
    CentralInterval,
    NormalForecast,
    crps_quadrature,
)
from trading_notes.records import Record

type Floats = NDArray[np.float64]

DATA: Final = Path("notes/artefacts/return-predictability/goyal-annual-predictors-1871-2025.csv")
PREDICTORS: Final = ("dp", "ep", "tms", "dfy")
FIRST_OUTCOME, FIRST_FORECAST, LAST = 1927, 1947, 2025
SHOW_YEARS: Final = (1947, 1970, 1990, 2010, 2025)
ALPHA: Final = 0.1


class Forecasts(Record):
    """Recursive forecasts of the annual log equity premium, from FIRST_FORECAST on.

    Attributes:
        years: The forecast years.
        y: The outcomes in those years.
        F: One column of regression forecasts per predictor.
        bench: The historical-mean forecasts.
        X: The predictors dated t - 1, for every outcome from FIRST_OUTCOME.
        y_all: Every outcome from FIRST_OUTCOME.
        first: The number of outcomes before the first forecast.
    """

    years: NDArray[np.int64]
    y: Floats
    F: Floats
    bench: Floats
    X: Floats
    y_all: Floats
    first: int

    @classmethod
    def of(cls, raw: LabelledTable) -> Forecasts:
        """Return the forecasts from the predictors dated t - 1 for outcomes FIRST_OUTCOME..LAST."""
        pred = {
            "dp": np.log(raw["D12"]) - np.log(raw["Index"]),
            "ep": np.log(raw["E12"]) - np.log(raw["Index"]),
            "tms": raw["lty"] - raw["tbl"],
            "dfy": raw["BAA"] - raw["AAA"],
        }
        premium = np.log1p(raw["CRSP_SPvw"]) - np.log1p(raw["Rfree"])
        years = np.arange(FIRST_OUTCOME, LAST + 1)
        X = np.column_stack([raw.at(pred[p], years - 1) for p in PREDICTORS])
        y = raw.at(premium, years)
        first = FIRST_FORECAST - FIRST_OUTCOME
        F = np.column_stack(
            [RecursiveForecasts.of(X[:, j], y, first).regression for j in range(X.shape[1])]
        )
        bench = RecursiveForecasts.of(X[:, 0], y, first).mean
        return cls(years=years[first:], y=y[first:], F=F, bench=bench, X=X, y_all=y, first=first)


def stats_vs_mean(y: Floats, f: Floats, bench: Floats) -> tuple[float, float, float, float]:
    """Return MSE, R2_OS (percent), DeltaRMSE (pp) and the Clark-West t against the benchmark."""
    eN, eA = y - bench, y - f
    mseN, mseA = np.mean(eN**2), np.mean(eA**2)
    fcw = eN**2 - (eA**2 - (bench - f) ** 2)
    t = fcw.mean() / (fcw.std(ddof=1) / np.sqrt(len(fcw)))
    return (
        float(mseA),
        float(100 * (1 - mseA / mseN)),
        float(100 * (np.sqrt(mseN) - np.sqrt(mseA))),
        float(t),
    )


def evaluation(
    label: str, y: Floats, F: Floats, bench: Floats, comb: Floats
) -> dict[str, tuple[float, float, float, float]]:
    """Print and return each forecast's statistics against the historical mean."""
    print(f"\n  {label}: P = {len(y)}")
    print(f"  {'forecast':10s} {'MSFE x100':>10s} {'R2_OS %':>9s} {'dRMSE pp':>9s} {'CW t':>7s}")
    mseN = np.mean((y - bench) ** 2)
    print(f"  {'hist mean':10s} {100 * mseN:10.4f}")
    rows = {}
    for name, f in [*zip(PREDICTORS, F.T, strict=True), ("mean comb", comb)]:
        rows[name] = stats_vs_mean(y, f, bench)
        mse, r2, drmse, t = rows[name]
        print(f"  {name:10s} {100 * mse:10.4f} {r2:9.2f} {drmse:9.2f} {t:7.2f}")
    return rows


def fraction_mean(values: Sequence[Fraction]) -> Fraction:
    """Return the exact mean of fractions."""
    return sum(values, Fraction(0)) / len(values)


class CombinationResults(Record):
    """What the recorded-value checks read from part F.

    Attributes:
        main: The 1947-2025 statistics of each forecast.
        sub: The 1947-2005 statistics.
        mse_c: The combination's MSE.
        mean_mse: The mean of the individual MSEs.
        spread: The mean squared spread of the forecasts around the combination.
    """

    main: dict[str, tuple[float, float, float, float]]
    sub: dict[str, tuple[float, float, float, float]]
    mse_c: float
    mean_mse: float
    spread: float


def check_combination(report: CheckReport, raw: LabelledTable) -> CombinationResults:
    """Part F: forecast combination of the annual log equity premium with four predictors."""
    print("\nF. Forecast combination, annual log equity premium, four predictors")
    fc = Forecasts.of(raw)
    fy, y_out, F, bench, X, y_all, first = fc.years, fc.y, fc.F, fc.bench, fc.X, fc.y_all, fc.first
    comb = F.mean(axis=1)
    print(
        f"  outcomes {FIRST_OUTCOME}-{LAST} ({len(y_all)}), first forecast {FIRST_FORECAST} after"
        f" {first} observations, P = {len(fy)}"
    )
    # F1. running sums against lstsq
    dev = max(
        np.max(np.abs(lstsq_forecasts(X[:, j], y_all, first) - F[:, j]))
        for j in range(len(PREDICTORS))
    )
    report.ok(
        "F1 recursive OLS by running sums equals lstsq refits", dev < 1e-10, f"max |diff| {dev:.1e}"
    )
    # F2. chronological indexing: overwrite the future in the raw data
    for t in (1970, 2000):
        rng = np.random.default_rng(t)
        later = raw.labels > t
        junk = {}
        for c, col in raw.columns.items():
            col = col.copy()
            col[later] = rng.uniform(0.5, 2.0, later.sum()) * np.nanmean(np.abs(col[later]))
            junk[c] = col
        fc2 = Forecasts.of(LabelledTable(labels=raw.labels, columns=junk))
        keep = fy <= t + 1
        d = max(
            np.max(np.abs(fc2.F[keep] - F[keep])), np.max(np.abs(fc2.bench[keep] - bench[keep]))
        )
        report.ok(
            f"F2 chronological indexing: forecasts through {t + 1} unchanged when later rows are"
            " overwritten",
            d == 0.0,
            f"max |diff| {d:.1e}",
        )
    main = evaluation("Evaluation 1947-2025", y_out, F, bench, comb)
    w05 = fy <= 2005
    sub = evaluation("Evaluation 1947-2005", y_out[w05], F[w05], bench[w05], comb[w05])
    # F3. error algebra
    E = y_out[:, None] - F
    ec = y_out - comb
    N = len(PREDICTORS)
    S = E.T @ E / len(y_out)
    mse_c = np.mean(ec**2)
    spread = np.mean((F - comb[:, None]) ** 2)
    report.ok(
        "F3 combination error = mean of individual errors",
        np.max(np.abs(ec - E.mean(axis=1))) < 1e-12,
    )
    report.ok(
        "F3 MSE_c = 1'S1 / N^2 (S = mean error products)", abs(mse_c - S.sum() / N**2) < 1e-12
    )
    report.ok(
        "F3 ambiguity decomposition MSE_c = mean MSE_i - mean spread",
        abs(mse_c - (np.mean(E**2) - spread)) < 1e-12,
        f"{100 * mse_c:.4f} = {100 * np.mean(E**2):.4f} - {100 * spread:.4f} (x100)",
    )
    check_biased_errors(report)
    report_correlations(E, F, bench, y_out)
    print(
        "\n  Predeclared rows (percent): forecast for year, actual, hist mean, dp, ep, tms, dfy,"
        " mean comb"
    )
    for yr in SHOW_YEARS:
        i = int(np.where(fy == yr)[0][0])
        print(
            f"    {yr}  actual {100 * y_out[i]:7.2f}  mean {100 * bench[i]:6.2f}  "
            + "  ".join(f"{p} {100 * F[i, j]:6.2f}" for j, p in enumerate(PREDICTORS))
            + f"  comb {100 * comb[i]:6.2f}"
        )
    check_diversification(report)
    check_weights(report, E)
    return CombinationResults(
        main=main,
        sub=sub,
        mse_c=float(mse_c),
        mean_mse=float(np.mean(E**2)),
        spread=float(spread),
    )


def check_biased_errors(report: CheckReport) -> None:
    """F6: the error identities hold exactly with nonzero individual error biases."""
    biased_errors = [
        [Fraction(3), Fraction(2), Fraction(3)],
        [Fraction(0), Fraction(3), Fraction(3)],
        [Fraction(0), Fraction(1), Fraction(3)],
    ]
    T_bias, N_bias = len(biased_errors), len(biased_errors[0])
    combo_errors = [fraction_mean(row) for row in biased_errors]
    biases = [fraction_mean([biased_errors[t][i] for t in range(T_bias)]) for i in range(N_bias)]
    bias_bar = fraction_mean(biases)
    combo_mse = fraction_mean([e**2 for e in combo_errors])
    combo_variance = fraction_mean([(e - bias_bar) ** 2 for e in combo_errors])
    second_moment_mse = (
        sum(
            (
                fraction_mean([biased_errors[t][i] * biased_errors[t][j] for t in range(T_bias)])
                for i in range(N_bias)
                for j in range(N_bias)
            ),
            Fraction(0),
        )
        / N_bias**2
    )
    member_mse = fraction_mean(
        [fraction_mean([biased_errors[t][i] ** 2 for t in range(T_bias)]) for i in range(N_bias)]
    )
    forecast_spread = fraction_mean(
        [
            fraction_mean([(biased_errors[t][i] - combo_errors[t]) ** 2 for i in range(N_bias)])
            for t in range(T_bias)
        ]
    )
    report.ok(
        "F6 biased errors: combination MSE = variance + mean bias squared",
        combo_mse == combo_variance + bias_bar**2,
        f"biases {', '.join(map(str, biases))}; {combo_mse} = {combo_variance} + {bias_bar}^2",
    )
    report.ok(
        "F6 biased errors: second-moment and ambiguity identities still hold",
        combo_mse == second_moment_mse == member_mse - forecast_spread,
        f"{combo_mse} = {second_moment_mse} = {member_mse} - {forecast_spread}",
    )


def report_correlations(E: Floats, F: Floats, bench: Floats, y_out: Floats) -> None:
    """Print the correlations and standard deviations of the errors and deviations."""
    corr_e = np.asarray(np.corrcoef(E.T))
    D = F - bench[:, None]
    corr_d = np.asarray(np.corrcoef(D.T))
    print("\n  1947-2025 correlation of forecast errors (dp, ep, tms, dfy):")
    for i, r in zip(PREDICTORS, corr_e, strict=True):
        print(f"    {i:4s} " + " ".join(f"{v:6.3f}" for v in r))
    print("  1947-2025 correlation of forecast deviations from the historical mean:")
    for i, r in zip(PREDICTORS, corr_d, strict=True):
        print(f"    {i:4s} " + " ".join(f"{v:6.3f}" for v in r))
    sd_d = D.std(axis=0, ddof=0)
    print(
        "  sd of deviations (pp): "
        + ", ".join(f"{p} {100 * s:.2f}" for p, s in zip(PREDICTORS, sd_d, strict=True))
        + f"; combination {100 * D.mean(axis=1).std(ddof=0):.2f}"
    )
    print(
        f"  sd of outcome (pp): {100 * y_out.std(ddof=0):.2f}; sd of benchmark error"
        f" {100 * (y_out - bench).std(ddof=0):.2f}"
    )


def check_diversification(report: CheckReport) -> None:
    """F4: the MSE of an average of equicorrelated errors tends to rho + (1 - rho) / N."""
    rng = np.random.default_rng(20261105)
    n, N = 200_000, len(PREDICTORS)
    for rho in (0.0, 0.5, 0.9, 0.99):
        z0 = rng.standard_normal(n)
        Z = rng.standard_normal((n, N))
        e = np.sqrt(rho) * z0[:, None] + np.sqrt(1 - rho) * Z
        got, want = np.mean(e.mean(axis=1) ** 2), rho + (1 - rho) / N
        report.ok(
            f"F4 rho = {rho}: MSE of average near rho + (1 - rho)/N",
            abs(got - want) < 0.01,
            f"{got:.4f} vs {want:.4f}",
        )


def check_weights(report: CheckReport, E: Floats) -> None:
    """F5: Bates-Granger weights, and the ex post minimum-MSE weights of the four forecasts."""
    N = len(PREDICTORS)
    sig2 = np.array([1.0, 2.0, 4.0, 0.5])
    Sd = np.diag(sig2)
    w_mv = np.linalg.solve(Sd, np.ones(4))
    w_mv /= w_mv.sum()
    w_inv = (1 / sig2) / np.sum(1 / sig2)
    report.ok(
        "F5 diagonal covariance: minimum-variance weights = inverse-MSE weights",
        np.max(np.abs(w_mv - w_inv)) < 1e-12,
    )
    Ec = np.cov(E.T, ddof=0) + np.outer(E.mean(0), E.mean(0))  # mean error products, as S
    w_mv = np.linalg.solve(Ec, np.ones(N))
    w_mv /= w_mv.sum()
    w_inv = (1 / np.diag(Ec)) / np.sum(1 / np.diag(Ec))
    print(
        "  ex post 1947-2025 weights, minimum-MSE (sum to one): "
        + ", ".join(f"{p} {w:.2f}" for p, w in zip(PREDICTORS, w_mv, strict=True))
    )
    print(
        "  ex post 1947-2025 weights, inverse MSE:             "
        + ", ".join(f"{p} {w:.3f}" for p, w in zip(PREDICTORS, w_inv, strict=True))
    )
    print(
        "  ex post minimum-MSE combination MSFE x100:"
        f" {100 / np.sum(np.linalg.solve(Ec, np.ones(N))):.4f}"
    )


class ScoringResults(Record):
    """What the recorded-value checks read from part S.

    Attributes:
        exp_log: Expected log score on the grid of forecast standard deviations.
        exp_crps: Expected CRPS on the grid.
        exp_is: Expected interval score on the grid.
        avg_is: The average interval score of intervals I, J and K.
        pool_scores: Expected log score and CRPS of the pool and of N(4, 10^2), truth the pool.
    """

    exp_log: list[float]
    exp_crps: list[float]
    exp_is: list[float]
    avg_is: dict[str, float]
    pool_scores: tuple[float, float, float, float]


def check_hand_example(report: CheckReport) -> None:
    """S1: two normal forecasts scored by every rule, closed forms against other routes."""
    fc = {"A": (5.0, 10.0), "B": (5.0, 20.0)}
    rng = np.random.default_rng(20261106)
    print("\n  S1 hand example: A = N(5, 10^2), B = N(5, 20^2); 90% central intervals")
    print(
        f"  {'':3s} {'x':>5s} {'sq. err':>8s} {'-log f (pct)':>12s} {'-log f (dec)':>12s}"
        f" {'CRPS':>7s} {'interval':>16s} {'IS':>7s}"
    )
    for x in (5.0, -15.0, -40.0):
        for k, (mu, s) in fc.items():
            forecast = NormalForecast(mean=mu, sd=s)
            interval = forecast.central_interval(ALPHA)
            lo, hi = interval.lower, interval.upper
            ls_pct = forecast.log_score(x)
            ls_dec = NormalForecast(mean=mu / 100, sd=s / 100).log_score(x / 100)
            cr = forecast.crps(x)
            IS = interval.score(x)
            print(
                f"  {k:3s} {x:5.0f} {(x - mu) ** 2:8.0f} {ls_pct:12.3f} {ls_dec:12.3f} {cr:7.3f}"
                f" [{lo:6.2f}, {hi:5.2f}] {IS:7.2f}"
            )

            def cdf(u: float, mu: float = mu, s: float = s) -> float:
                return float(stats.norm.cdf((u - mu) / s))

            cq = crps_quadrature(cdf, x)
            report.ok(
                f"S1 {k}, x = {x:.0f}: closed-form CRPS = quadrature of eq. (20)",
                abs(cr - cq) < 1e-7,
                f"{abs(cr - cq):.1e}",
            )
            X1 = rng.normal(mu, s, 1_000_000)
            X2 = rng.normal(mu, s, 1_000_000)
            h = np.abs(X1 - x) - 0.5 * np.abs(X1 - X2)
            se = h.std(ddof=1) / np.sqrt(h.size)
            report.ok(
                f"S1 {k}, x = {x:.0f}: kernel form eq. (21) by Monte Carlo within 4 se",
                abs(h.mean() - cr) < 4 * se,
                f"{h.mean():.3f} (se {se:.3f})",
            )
            lower, upper = interval.quantiles()
            qsum = (2 / ALPHA) * (lower.score(x) + upper.score(x))
            report.ok(
                f"S1 {k}, x = {x:.0f}: interval score = (2/alpha) x sum of quantile scores",
                abs(qsum - IS) < 1e-12,
            )
            report.ok(
                f"S1 {k}, x = {x:.0f}: log score in decimals = in percent - log 100",
                abs(ls_dec - (ls_pct - np.log(100))) < 1e-12,
            )


def check_propriety(report: CheckReport) -> tuple[list[float], list[float], list[float]]:
    """S2: expected scores by quadrature under the truth N(5, 15^2); return them on the grid."""
    print("\n  S2 truth Q = N(5, 15^2); forecasts N(5, s^2)")
    grid = np.arange(5.0, 30.0 + 1e-9, 0.5)
    lim = (5 - 15 * 12, 5 + 15 * 12)

    def q(x: float) -> float:
        return float(stats.norm.pdf(x, 5, 15))

    def expect(fun: Callable[[float], float]) -> float:
        return integrate.quad(
            lambda x: fun(x) * q(x), *lim, epsabs=1e-11, epsrel=1e-11, limit=400, points=[5.0]
        )[0]

    exp_log, exp_crps, exp_is, exp_lin = [], [], [], []
    for s in grid:
        sd = float(s)
        forecast = NormalForecast(mean=5.0, sd=sd)
        interval = forecast.central_interval(ALPHA)

        def density_at(x: float, sd: float = sd) -> float:
            return float(stats.norm.pdf(x, 5, sd))

        exp_log.append(expect(forecast.log_score))
        exp_crps.append(expect(forecast.crps))

        def scored(x: float, interval: CentralInterval[float] = interval) -> float:
            return interval.score(x) * q(x)

        exp_is.append(
            integrate.quad(
                scored,
                *lim,
                points=[interval.lower, interval.upper],
                limit=400,
                epsabs=1e-11,
                epsrel=1e-11,
            )[0]
        )
        exp_lin.append(expect(density_at))
    for name, v in (("log score", exp_log), ("CRPS", exp_crps), ("interval score", exp_is)):
        report.ok(
            f"S2 expected {name} smallest at s = 15",
            grid[np.argmin(v)] == 15.0,
            f"argmin {grid[np.argmin(v)]:.1f}",
        )
    report.ok(
        "S2 expected linear score (improper) largest at the smallest s",
        grid[np.argmax(exp_lin)] == grid[0],
    )
    for s in (10.0, 15.0, 20.0):
        i = int(np.where(grid == s)[0][0])
        print(
            f"    s = {s:4.1f}: E[-log f] {exp_log[i]:.4f}  E[CRPS] {exp_crps[i]:.4f}  E[IS90]"
            f" {exp_is[i]:.3f}  E[f(x)] {exp_lin[i]:.5f}"
        )
    return exp_log, exp_crps, exp_is


def bilinear(n: int, burn: int, seed: int) -> Floats:
    """Return n values of the bilinear process (44) after a burn-in, from its own generator."""
    eps = np.random.default_rng(seed).standard_normal(n + burn).tolist()
    out = np.empty(n + burn)
    x = 0.0
    for t, e in enumerate(eps):
        out[t] = x
        x = 0.5 * x + 0.5 * x * e + e
    return out[burn:]


def check_table_2(report: CheckReport) -> dict[str, float]:
    """S3: Gneiting and Raftery's Table 2 by simulation; return the average interval scores."""
    print(
        "\n  S3 bilinear process (44), one-step 95% intervals I, J, K; Gneiting and Raftery Table 2"
        " in brackets"
    )
    path = bilinear(100_001, 1_000, 20261107)
    long = bilinear(10_000_000, 1_000, 20261108)
    jlo, jhi = np.quantile(long, [0.025, 0.975])
    print(f"    J's unconditional quantiles from 10^7 draws: [{jlo:.3f}, {jhi:.3f}]")
    xt, xn = path[:-1], path[1:]
    c = stats.norm.ppf(0.975)
    m, sc = xt / 2, np.abs(1 + xt / 2)
    gam = np.where(sc <= 7.36, np.sqrt(2 * np.clip(np.log(7.36) - np.log(sc), 0, None)) * sc, 0.0)
    ints: dict[str, tuple[Floats, Floats]] = {
        "I": (m - c * sc, m + c * sc),
        "J": (np.full_like(xt, jlo), np.full_like(xt, jhi)),
        "K": (m - gam, m + gam),
    }
    pub = {"I": (95.01, 4.00, 4.77), "J": (95.08, 5.45, 8.04), "K": (94.98, 3.79, 5.32)}
    avg_is = {}
    for k, (lo, hi) in ints.items():
        cov = 100 * np.mean((xn >= lo) & (xn <= hi))
        wid = np.mean(hi - lo)
        sc_k = CentralInterval(lower=lo, upper=hi, alpha=0.05).score(xn)
        avg_is[k] = float(sc_k.mean())
        se = sc_k.reshape(100, -1).mean(axis=1).std(ddof=1) / 10
        pc, pw, ps = pub[k]
        print(
            f"    {k}: coverage {cov:6.2f}% ({pc}), width {wid:5.2f} ({pw}), interval score"
            f" {avg_is[k]:5.2f} ({ps}), batch-means se {se:.3f}"
        )
        report.ok(f"S3 {k} coverage within 0.5 pp", bool(abs(cov - pc) < 0.5))
        report.ok(f"S3 {k} width within 2%", bool(abs(wid / pw - 1) < 0.02))
        report.ok(f"S3 {k} interval score within 3%", abs(avg_is[k] / ps - 1) < 0.03)
    report.ok("S3 order by interval score I < K < J", avg_is["I"] < avg_is["K"] < avg_is["J"])
    return avg_is


def check_linear_pool(report: CheckReport) -> tuple[float, float, float, float]:
    """S4: a linear pool against the Gaussian around the averaged point forecast."""
    print("\n  S4 forecasts N(0, 10^2) and N(8, 10^2): equal-weight linear pool against N(4, 10^2)")
    Phi, phi = stats.norm.cdf, stats.norm.pdf
    MU, SD, W = np.array([0.0, 8.0]), np.array([10.0, 10.0]), np.array([0.5, 0.5])

    def pool_pdf(x: float) -> float:
        return float(np.sum(W * stats.norm.pdf(x, MU, SD)))

    def pool_cdf(x: float) -> float:
        return float(np.sum(W * Phi((x - MU) / SD)))

    mean_pool = integrate.quad(lambda x: x * pool_pdf(x), -200, 210, limit=400, epsabs=1e-12)[0]
    var_pool = integrate.quad(
        lambda x: (x - mean_pool) ** 2 * pool_pdf(x), -200, 210, limit=400, epsabs=1e-12
    )[0]
    report.ok(
        "S4 pool variance = 100 + 16 = 116 by quadrature",
        abs(var_pool - 116) < 1e-8,
        f"{var_pool:.10f}, mean {mean_pool:.10f}",
    )

    def abs_mean(m: Floats | float, s: Floats | float) -> Floats:
        """Return E|X| for X ~ N(m, s^2), elementwise."""
        return np.asarray(m * (2 * Phi(m / s) - 1) + 2 * s * phi(m / s))

    def crps_pool(x: float) -> float:
        t1 = np.sum(W * abs_mean(MU - x, SD))
        t2 = sum(
            W[i] * W[j] * abs_mean(MU[i] - MU[j], np.hypot(SD[i], SD[j]))
            for i in range(2)
            for j in range(2)
        )
        return float(t1 - 0.5 * t2)

    averaged = NormalForecast(mean=4.0, sd=10.0)
    for x in (-15.0, 4.0, 20.0):
        cp, cq = crps_pool(x), crps_quadrature(pool_cdf, x)
        report.ok(
            f"S4 pool CRPS at x = {x:.0f}: closed form = quadrature of eq. (20)",
            abs(cp - cq) < 1e-7,
        )
        print(
            f"    x = {x:5.0f}: pool -log f {-np.log(pool_pdf(x)):.3f}, CRPS {cp:.3f};  N(4,10^2)"
            f" -log f {averaged.log_score(x):.3f}, CRPS {averaged.crps(x):.3f}"
        )
    lim4 = (-200, 210)
    E_pool_log = integrate.quad(
        lambda x: -np.log(pool_pdf(x)) * pool_pdf(x), *lim4, limit=400, epsabs=1e-11
    )[0]
    E_avg_log = integrate.quad(
        lambda x: averaged.log_score(x) * pool_pdf(x), *lim4, limit=400, epsabs=1e-11
    )[0]
    E_pool_crps = integrate.quad(
        lambda x: crps_pool(x) * pool_pdf(x), *lim4, limit=400, epsabs=1e-11
    )[0]
    E_avg_crps = integrate.quad(
        lambda x: averaged.crps(x) * pool_pdf(x), *lim4, limit=400, epsabs=1e-11
    )[0]
    print(
        f"    truth = pool: E[-log f] pool {E_pool_log:.4f}, N(4,10^2) {E_avg_log:.4f}; E[CRPS]"
        f" pool {E_pool_crps:.4f}, N(4,10^2) {E_avg_crps:.4f}"
    )
    report.ok(
        "S4 truth = pool: pool has the lower expected log score", bool(E_pool_log < E_avg_log)
    )
    report.ok("S4 truth = pool: pool has the lower expected CRPS", bool(E_pool_crps < E_avg_crps))
    return E_pool_log, E_avg_log, E_pool_crps, E_avg_crps


def check_scoring(report: CheckReport) -> ScoringResults:
    """Part S: proper scoring rules (negatively oriented losses)."""
    print(
        "\nS. Proper scoring rules (negatively oriented losses; units: percentage points unless"
        " stated)"
    )
    check_hand_example(report)
    exp_log, exp_crps, exp_is = check_propriety(report)
    avg_is = check_table_2(report)
    pool = check_linear_pool(report)
    return ScoringResults(
        exp_log=exp_log, exp_crps=exp_crps, exp_is=exp_is, avg_is=avg_is, pool_scores=pool
    )


def check_recorded(
    report: CheckReport, combination: CombinationResults, scoring: ScoringResults
) -> None:
    """Part R: the first run's values, at their printed rounding."""
    print("\nR. Recorded values of the first run, at their printed rounding (drift check)")
    main, sub = combination.main, combination.sub
    r2_main = [round(main[k][1], 2) for k in [*PREDICTORS, "mean comb"]]
    r2_sub = [round(sub[k][1], 2) for k in [*PREDICTORS, "mean comb"]]
    report.ok(
        "R R2_OS 1947-2025 (dp, ep, tms, dfy, comb)",
        r2_main == [-1.83, -2.28, -3.60, -0.83, 2.56],
        f"{[float(v) for v in r2_main]}",
    )
    report.ok(
        "R R2_OS 1947-2005 (dp, ep, tms, dfy, comb)",
        r2_sub == [1.34, 4.61, -3.70, -1.00, 5.82],
        f"{[float(v) for v in r2_sub]}",
    )
    report.ok(
        "R combination CW t 1947-2025 and 1947-2005",
        [round(main["mean comb"][3], 2), round(sub["mean comb"][3], 2)] == [1.44, 2.13],
    )
    report.ok(
        "R ambiguity terms x100",
        [
            round(100 * combination.mse_c, 4),
            round(100 * combination.mean_mse, 4),
            round(100 * combination.spread, 4),
        ]
        == [2.65, 2.7777, 0.1277],
    )
    report.ok(
        "R S2 expected scores at s = 15",
        [
            round(scoring.exp_log[20], 4),
            round(scoring.exp_crps[20], 4),
            round(scoring.exp_is[20], 3),
        ]
        == [4.127, 8.4628, 61.881],
    )
    report.ok(
        "R S3 average interval scores I, J, K",
        [round(scoring.avg_is[k], 2) for k in "IJK"] == [4.76, 8.03, 5.29],
    )
    report.ok(
        "R S4 expected scores, truth = pool",
        [round(v, 4) for v in scoring.pool_scores] == [3.7957, 3.8015, 6.0816, 6.0903],
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Print the versions, run parts F, S and R with one report, and print the count.

    Worked numbers of meth:forecast-combination and meth:proper-scoring-rules, under
    forecast-combination-scoring-protocol.md (predictors, sample, transformations, seeds and
    tolerances written before the first run).

    Data: goyal-annual-predictors-1871-2025.csv, extracted by
    trading_notes.research.return_predictability.goyal_extract_predictors from
    the workbook on Amit Goyal's page labelled "Original data (up to 2005) used in the paper",
    served on 2026-10-22 with data to December 2025 (a 2026 vintage). Synthetic data from seeds
    20261105-20261108.

    Independent routes: recursive OLS by running sums against numpy.linalg.lstsq refitted at
    each origin; the combination's MSE from its errors, from the matrix of error products and
    from the ambiguity decomposition; forecasts recomputed after the future is overwritten
    (chronological indexing); the normal CRPS in closed form against quadrature of the
    threshold integral (Gneiting and Raftery eq. (20)) and against Monte Carlo of the kernel
    form (eq. (21)); the interval score (43) against the sum of two quantile scores (41); the
    published Table 2 by simulation in its design. Recorded output:
    forecast-combination-scoring-results.txt.

    Args:
        argv: Command-line arguments: `--root DIR`, the repository root that holds the data
            (default: the working directory).

    Returns:
        The exit status, 0 or 1.
    """
    root = repository_root(__doc__ or "", argv)
    print_versions(np, pd, scipy)
    raw = LabelledTable.read(root / DATA, "yyyy")
    report = CheckReport()
    combination = check_combination(report, raw)
    scoring = check_scoring(report)
    check_recorded(report, combination, scoring)
    print(f"\n{report.count} checks, {len(report.failures)} failed")
    if report.failures:
        print("FAILED: " + "; ".join(report.failures))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
