"""Inference and simulation: intervals, tests, bootstrap and Monte Carlo against closed forms.

Batch 2 foundations (2026-10-18): the worked examples of meth:confidence-intervals,
meth:hypothesis-testing, meth:nonparametric-tests, meth:historical-simulation,
meth:bootstrap-resampling and meth:monte-carlo-simulation.

Each result is computed twice: by the formula in the entry and by an independent route (scipy's
implementation, exact enumeration, an exact quadratic-form expectation, or a seeded simulation
compared within a stated multiple of its own standard error). Seeds were fixed before any run
(20261018 and offsets) and are not tuned; Monte Carlo comparisons use a tolerance of four standard
errors, stated in advance. All data are invented for illustration.

Extended 2026-10-21 (library gap-filling Batch L1): a control variate with an estimated coefficient
and the Euler discretisation bias, both for meth:monte-carlo-simulation; seed 20261018 + 11 added
for the latter.

Environment: the locked project environment (Python 3.14.7, NumPy 2.4.6, SciPy 1.18.1). The first
recorded run used Python 3.10.16, NumPy 1.23.5 and SciPy 1.10.1; both runs agree apart from the
printed version line, which reports the versions the script ran under.

One generator, seeded 20261018, serves parts 1 and 2 in order: part 2 is passed the generator and
the simulated samples that part 1 has drawn.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.inference_simulation
(numpy, scipy). Exits 1 on failure.
"""

import itertools
import math
import sys
from typing import Final

import numpy as np
import scipy
from numpy.typing import ArrayLike, NDArray
from scipy import stats

from trading_notes.numerical.report import CheckReport

type Floats = NDArray[np.float64]

SEED: Final = 20261018
R: Final = 40000  # replications of the coverage, power and Type I error simulations
M: Final = 100_000  # Monte Carlo draws of the analytic benchmark
S0: Final = 100.0
K: Final = 105.0
r: Final = 0.03
sg: Final = 0.20
T: Final = 1.0


def close(a: float, b: float, tol: float = 1e-6) -> bool:
    """Return whether |a - b| <= tol."""
    return abs(a - b) <= tol


def manager_stats(x: Floats) -> tuple[int, float, float, float, float, tuple[float, float]]:
    """Return n, the mean, the sample s.d., the standard error, the t quantile and the 95% interval.

    Args:
        x: The monthly returns.
    """
    n = len(x)
    m, s = x.mean(), x.std(ddof=1)
    se = s / math.sqrt(n)
    tq = stats.t.ppf(0.975, n - 1)
    return n, m, s, se, tq, (m - tq * se, m + tq * se)


def var_es(losses: ArrayLike, weights: ArrayLike, c: float) -> tuple[float, float]:
    """Lower loss quantile and exact-tail-mass ES (Acerbi and Tasche, Definitions 2.2 and 2.6)."""
    p = 1 - c
    levels, inv = np.unique(-np.asarray(losses, float), return_inverse=True)
    levels = -levels  # distinct losses, largest first
    w = np.bincount(inv, weights=np.asarray(weights, float))
    cum = np.cumsum(w)
    k = int(np.argmax(cum > p + 1e-12))
    above = cum[k - 1] if k else 0.0
    return levels[k], (np.dot(w[:k], levels[:k]) + (p - above) * levels[k]) / p


def es_integral(losses: ArrayLike, weights: ArrayLike, c: float, grid: int = 200_000) -> np.float64:
    """ES as the average of VaR_u over u in (c, 1), by a midpoint rule on the quantile function."""
    u = c + (np.arange(grid) + 0.5) * (1 - c) / grid
    order = np.argsort(losses)
    srt = np.asarray(losses, float)[order]
    cdf = np.cumsum(np.asarray(weights, float)[order])
    idx = np.searchsorted(cdf, u - 1e-12, side="left")
    mean: np.float64 = srt[np.minimum(idx, len(srt) - 1)].mean()
    return mean


def check_confidence(report: CheckReport, rng: np.random.Generator, x: Floats) -> Floats:
    """Part 1: confidence intervals, their coverage and the effect of dependence.

    Args:
        report: The run's report.
        rng: The run's generator, advanced by this part's draws.
        x: The twelve monthly returns.

    Returns:
        The coverage simulation's samples, which part 2 reuses.
    """
    print("== confidence intervals")
    n, m, s, se, tq, ci_t = manager_stats(x)
    report.ok(
        "mean 0.5333, s 1.1106, standard error 0.3206",
        close(m, 0.533333) and close(s, 1.110555) and close(se, 0.320590),
    )
    report.ok(
        "exact t interval (normal i.i.d.): -0.172 to 1.239, t(0.975, 11) = 2.2010",
        close(tq, 2.200985) and close(ci_t[0], -0.172280) and close(ci_t[1], 1.238947),
    )
    report.ok(
        "scipy interval agrees",
        np.allclose(stats.t.interval(0.95, n - 1, loc=m, scale=se), ci_t),
    )
    report.ok(
        "normal-approximation interval is narrower: -0.095 to 1.162",
        close(m - 1.959964 * se, -0.095011) and close(m + 1.959964 * se, 1.161678),
    )
    chi_lo, chi_hi = (
        (n - 1) * s**2 / stats.chi2.ppf(0.975, n - 1),
        (n - 1) * s**2 / stats.chi2.ppf(0.025, n - 1),
    )
    report.ok(
        "chi-square interval for the variance 0.619 to 3.555 (s.d. 0.787 to 1.886)",
        close(chi_lo, 0.618916)
        and close(chi_hi, 3.555441)
        and close(math.sqrt(chi_lo), 0.786712)
        and close(math.sqrt(chi_hi), 1.885588),
    )
    # Repeated-sampling meaning: draw many normal samples of 12 with known mean; count interval
    # coverage.
    sims = rng.normal(0.5, 1.0, (R, n))
    mm, ss = sims.mean(1), sims.std(1, ddof=1)
    cover = np.mean(np.abs(mm - 0.5) <= tq * ss / math.sqrt(n))
    cover_se = math.sqrt(0.95 * 0.05 / R)
    report.ok(
        f"coverage of the t interval in {R} normal samples is 95% within 4 s.e.",
        abs(cover - 0.95) <= 4 * cover_se,
        f"{cover:.4f}",
    )
    # Dependent data: AR(1) phi = 0.5 samples of 12; the i.i.d. t interval under-covers.
    phi = 0.5
    e = rng.normal(0, 1, (R, n))
    ar = np.empty_like(e)
    ar[:, 0] = e[:, 0] / math.sqrt(1 - phi**2)
    for t in range(1, n):
        ar[:, t] = phi * ar[:, t - 1] + e[:, t]
    cover_ar = np.mean(np.abs(ar.mean(1)) <= tq * ar.std(1, ddof=1) / math.sqrt(n))
    report.ok(
        "with AR(1) dependence (phi 0.5) the same interval covers far less than 95%",
        cover_ar < 0.85,
        f"{cover_ar:.4f}",
    )
    return sims


def check_tests(report: CheckReport, rng: np.random.Generator, x: Floats, sims: Floats) -> None:
    """Part 2: hypothesis tests, their errors and power, and the F test of two variances.

    Args:
        report: The run's report.
        rng: The generator of part 1, as part 1 left it.
        x: The twelve monthly returns.
        sims: The coverage simulation's samples from part 1.
    """
    print("== hypothesis tests, errors and power")
    n, m, s, se, _, ci_t = manager_stats(x)
    tstat = m / se
    p_two, p_one = 2 * stats.t.sf(abs(tstat), n - 1), stats.t.sf(tstat, n - 1)
    report.ok(
        "t = 1.6636; one-sided p 0.0622, two-sided p 0.1244",
        close(tstat, 1.663601) and close(p_one, 0.062195) and close(p_two, 0.124390),
    )
    report.ok(
        "scipy one-sample t-test agrees",
        close(stats.ttest_1samp(x, 0).pvalue, p_two, 1e-12),
    )
    report.ok(
        "decision at 5%: not rejected; 0 lies inside the 95% interval",
        p_one > 0.05 and ci_t[0] < 0 < ci_t[1],
    )
    crit = stats.t.ppf(0.95, n - 1)
    power = stats.nct.sf(crit, n - 1, 0.5 * math.sqrt(n))
    report.ok(
        "power against a true mean of 0.5 s.d., one-sided 5%, n = 12: 0.492 (noncentral t)",
        close(power, 0.491884, 1e-5),
    )
    sim_power = np.mean(
        sims.mean(1) / (sims.std(1, ddof=1) / math.sqrt(n)) > crit
    )  # sims have mean 0.5, s.d. 1
    report.ok(
        "simulated power agrees within 4 s.e.",
        abs(sim_power - power) <= 4 * math.sqrt(power * (1 - power) / R),
        f"{sim_power:.4f}",
    )
    report.ok(
        "power 0.903 at n = 36 and 0.985 at n = 60",
        close(stats.nct.sf(stats.t.ppf(0.95, 35), 35, 0.5 * 6), 0.902575, 1e-5)
        and close(stats.nct.sf(stats.t.ppf(0.95, 59), 59, 0.5 * math.sqrt(60)), 0.985489, 1e-5),
    )
    null_sims = rng.normal(0.0, 1.0, (R, n))
    type1 = np.mean(null_sims.mean(1) / (null_sims.std(1, ddof=1) / math.sqrt(n)) > crit)
    report.ok(
        "Type I error rate under the null is 5% within 4 s.e.",
        abs(type1 - 0.05) <= 4 * math.sqrt(0.05 * 0.95 / R),
        f"{type1:.4f}",
    )
    # Correction of 2026-10-18: the F test needs independent samples. The second sample is drawn
    # independently of x from N(0, 0.5^2), n = 15, first draw of seed SEED + 7, rounded to one
    # decimal.
    y = np.round(np.random.default_rng(SEED + 7).normal(0.0, 0.5, 15), 1)
    report.ok(
        "independent second sample of 15 values as printed in the entry",
        np.array_equal(
            y, [-0.2, 0.1, 0.3, 0.4, 0.8, 0.2, 0.4, 0.4, 0.3, 0.1, -0.7, 0.0, -0.3, 1.5, 0.3]
        )
        and close(y.std(ddof=1), 0.496847, 1e-6),
    )
    n2 = len(y)
    F = x.var(ddof=1) / y.var(ddof=1)
    pF = 2 * min(stats.f.sf(F, n - 1, n2 - 1), stats.f.cdf(F, n - 1, n2 - 1))
    report.ok(
        "F = 4.996 on (11, 14) d.f. > critical 3.095; two-sided p 0.0062",
        close(F, 4.996142, 1e-5)
        and close(stats.f.ppf(0.975, 11, 14), 3.094590)
        and close(stats.f.ppf(0.025, 11, 14), 0.297724)
        and close(pF, 0.006154, 1e-6),
    )
    report.ok(
        "F from the two standard deviations; two-sided p is twice the upper tail (checks"
        " arithmetic, not suitability)",
        close(F, (1.110555 / 0.496847) ** 2, 1e-4) and close(pF, 2 * stats.f.sf(F, 11, 14), 1e-12),
    )
    # Counterexample: equal variances, paired months with correlation 0.9, n = 12; the ordinary F
    # calibration fails.
    rng_c = np.random.default_rng(SEED + 9)
    Rc, rho_c = 40_000, 0.9
    z1 = rng_c.normal(size=(Rc, n))
    z2 = rho_c * z1 + math.sqrt(1 - rho_c**2) * rng_c.normal(size=(Rc, n))
    z3 = rng_c.normal(size=(Rc, n))
    lo = stats.f.ppf(0.025, n - 1, n - 1)
    hi = stats.f.ppf(0.975, n - 1, n - 1)

    def reject_rate(a: Floats, b: Floats) -> float:
        ratio = a.var(1, ddof=1) / b.var(1, ddof=1)
        return float(np.mean((ratio < lo) | (ratio > hi)))

    rej_corr, rej_ind = reject_rate(z1, z2), reject_rate(z1, z3)
    pow_corr, pow_ind = reject_rate(1.5 * z1, z2), reject_rate(1.5 * z1, z3)
    report.ok(
        "independent equal-variance samples reject at 5% within 4 s.e.",
        abs(rej_ind - 0.05) <= 4 * math.sqrt(0.05 * 0.95 / Rc),
        f"{rej_ind:.4f}",
    )
    report.ok(
        "correlated (rho 0.9) equal-variance samples reject far below 5%",
        rej_corr < 0.005,
        f"{rej_corr:.4f}",
    )
    report.ok(
        "with a true s.d. ratio of 1.5, correlation cuts rejections from about 24% to about 6%",
        abs(pow_ind - 0.24) < 0.02 and abs(pow_corr - 0.06) < 0.02,
        f"independent {pow_ind:.4f}, correlated {pow_corr:.4f}",
    )
    chi_stat = (n - 1) * s**2 / 1.0
    report.ok(
        "chi-square test of sigma = 1: statistic 13.567, two-sided p 0.516",
        close(chi_stat, 13.566667)
        and close(
            2 * min(stats.chi2.sf(chi_stat, 11), stats.chi2.cdf(chi_stat, 11)), 0.515810, 1e-5
        ),
    )


def check_nonparametric(report: CheckReport, x: Floats) -> None:
    """Part 3: the sign test, the signed-rank test and its normal approximation.

    Args:
        report: The run's report.
        x: The twelve monthly returns.
    """
    print("== nonparametric tests")
    n = len(x)
    pos = int((x > 0).sum())
    p_sign = sum(math.comb(n, k) for k in range(pos, n + 1)) / 2**n
    report.ok(
        "sign test: 8 of 12 positive, exact one-sided p 0.1938",
        pos == 8
        and close(p_sign, 0.193848)
        and close(stats.binomtest(pos, n, 0.5, alternative="greater").pvalue, p_sign, 1e-12),
    )
    ranks = stats.rankdata(np.abs(x))
    w_plus = ranks[x > 0].sum()
    null_w = [
        sum(rank for rank, sg_i in zip(ranks, signs) if sg_i)
        for signs in itertools.product((0, 1), repeat=n)
    ]
    p_w = np.mean(np.array(null_w) >= w_plus)
    report.ok(
        "signed-rank W+ = 58; exact one-sided p 0.0757 by enumerating 4,096 sign patterns",
        w_plus == 58
        and close(p_w, 0.075684, 1e-6)
        and close(stats.wilcoxon(x, alternative="greater").pvalue, p_w, 1e-12),
    )
    mu_w, sd_w = n * (n + 1) / 4, math.sqrt(n * (n + 1) * (2 * n + 1) / 24)
    report.ok(
        "normal approximation to W+: mean 39, s.d. 12.75, one-sided p 0.0734 with continuity"
        " correction",
        close(mu_w, 39)
        and close(sd_w, 12.747549)
        and close(stats.norm.sf((w_plus - 0.5 - mu_w) / sd_w), 0.073354, 1e-5),
    )


def check_historical(report: CheckReport) -> None:
    """Part 4: historical simulation of a 20-day scenario set, its quantile and ES definitions.

    Args:
        report: The run's report.
    """
    print("== historical simulation")
    ra = np.array(
        [
            0.5,
            -1.2,
            0.3,
            0.8,
            -0.4,
            1.1,
            -2.5,
            0.2,
            0.6,
            -0.7,
            0.9,
            -0.3,
            0.4,
            -1.8,
            1.3,
            0.1,
            -0.6,
            0.7,
            -1.0,
            0.2,
        ]
    )
    rb = np.array(
        [
            0.2,
            -0.3,
            0.1,
            0.4,
            -0.1,
            0.3,
            -0.9,
            0.0,
            0.2,
            -0.2,
            0.3,
            -0.1,
            0.1,
            -0.5,
            0.4,
            0.1,
            -0.2,
            0.2,
            -0.4,
            0.1,
        ]
    )
    value = 1_000_000
    loss = -value * (0.6 * ra + 0.4 * rb) / 100
    worst = np.sort(loss)[::-1]
    report.ok(
        "20 scenarios; worst losses 18,600 (day 7) and 12,800 (day 14)",
        close(worst[0], 18600) and close(worst[1], 12800) and int(np.argmax(loss)) + 1 == 7,
    )

    eq = np.full(len(loss), 1 / len(loss))
    v_eq, es_eq = var_es(loss, eq, 0.90)
    report.ok(
        "equal weights, canonical lower quantile: 90% VaR 8,400 (3rd largest), ES 15,700",
        close(v_eq, 8400)
        and close(es_eq, 15700, 1e-6)
        and close(np.quantile(loss, 0.90, method="inverted_cdf"), 8400),
    )
    report.ok(
        "exact CDF boundary: np = 2, so the two worst losses carry the whole tail; Hull's rank"
        " gives 12,800",
        close(worst[:2].mean(), es_eq, 1e-6) and close(worst[1], 12800),
    )
    report.ok(
        "ES equals the integral of VaR_u over the tail",
        close(es_integral(loss, eq, 0.90), 15700, 1e-3),
    )
    manual = sorted([value * 0.6 * a / 100 + value * 0.4 * b / 100 for a, b in zip(ra, rb)])
    report.ok(
        "scenario P&L recomputed by hand route",
        close(-manual[1], 12800) and close(-manual[2], 8400),
    )
    lam, N = 0.9, len(loss)
    wts = lam ** (N - np.arange(1, N + 1)) * (1 - lam) / (1 - lam**N)
    v_age, es_age = var_es(loss, wts, 0.90)
    report.ok(
        "weights sum to one; with lambda 0.9 the 90% VaR is also 8,400 (day 2)",
        close(wts.sum(), 1.0, 1e-12)
        and close(v_age, 8400)
        and int(np.argmax(loss == 8400)) + 1 == 2,
    )
    report.ok(
        "the two worst days carry weights 0.0289 and 0.0605 because they are old; W2 = 0.0894",
        close(wts[6], 0.028937, 1e-5)
        and close(wts[13], 0.060499, 1e-5)
        and close(wts[6] + wts[13], 0.089436, 1e-5),
    )
    report.ok(
        "age-weighted ES 14,014 = (w7*18,600 + w14*12,800 + (0.1 - W2)*8,400)/0.1, about 11% below"
        " 15,700",
        close(
            es_age,
            (wts[6] * 18600 + wts[13] * 12800 + (0.1 - wts[6] - wts[13]) * 8400) / 0.1,
            1e-6,
        )
        and close(es_age, 14013.516, 1e-3)
        and close(1 - es_age / es_eq, 0.10742, 1e-4)
        and close(es_integral(loss, wts, 0.90), es_age, 0.1),
    )
    # Uniform weights reproduce the unweighted lower quantile; ties are merged; fractional tails
    # are weighted.
    rng_v = np.random.default_rng(SEED + 10)
    agree = True
    for m_ in (10, 20, 25, 40, 250):
        sample = np.round(rng_v.normal(0, 1000, m_), -2)  # rounding creates ties
        for c_ in (0.9, 0.95, 0.99):
            v_, e_ = var_es(sample, np.full(m_, 1 / m_), c_)
            agree &= close(v_, np.quantile(sample, c_, method="inverted_cdf"), 1e-9)
            agree &= close(e_, es_integral(sample, np.full(m_, 1 / m_), c_), 1e-2)
    report.ok(
        "uniform weights = unweighted lower quantile, and ES = tail integral, on samples with ties",
        agree,
    )
    v_t, e_t = var_es([5, 5, 5, 3, 1, 0, 0, 0, 0, 0], np.full(10, 0.1), 0.85)
    report.ok(
        "tied losses: three losses of 5 at 85% give VaR 5 and ES 5",
        close(v_t, 5) and close(e_t, 5),
    )
    f25 = np.arange(25, 0, -1) * 100.0
    v_f, e_f = var_es(f25, np.full(25, 0.04), 0.90)
    report.ok(
        "fractional tail: n = 25 at 90% gives np = 2.5, ES = (l1 + l2 + 0.5 l3)/2.5 = 2,420",
        close(v_f, 2300) and close(e_f, (2500 + 2400 + 0.5 * 2300) / 2.5) and close(e_f, 2420),
    )
    report.ok(
        "averaging losses strictly beyond a VaR of 12,800 (Hull rank) leaves only 18,600, not the"
        " ES of 15,700",
        close(loss[loss > v_eq].mean(), 15700) and close(loss[loss > 12800].mean(), 18600),
    )


def check_bootstrap(report: CheckReport, x: Floats) -> None:
    """Part 5: the bootstrap of the mean, and the block bootstrap under dependence.

    Args:
        report: The run's report.
        x: The twelve monthly returns.
    """
    print("== bootstrap resampling")
    n = len(x)
    rng = np.random.default_rng(SEED + 1)
    B = 10000
    bmeans = x[rng.integers(0, n, (B, n))].mean(1)
    ideal = x.std(ddof=0) / math.sqrt(n)
    report.ok(
        "ideal i.i.d. bootstrap s.e. of the mean 0.3069 (divides by n)",
        close(ideal, 0.306941),
    )
    report.ok(
        f"B = {B} resamples: s.e. within 4% of the ideal value",
        abs(bmeans.std(ddof=1) / ideal - 1) < 0.04,
        f"{bmeans.std(ddof=1):.4f}",
    )
    pct = np.percentile(bmeans, [2.5, 97.5])
    report.ok(
        "percentile interval about -0.08 to 1.13 (resampling noise in the second decimal)",
        abs(pct[0] + 0.08) < 0.05 and abs(pct[1] - 1.13) < 0.05,
        f"{pct[0]:.3f} to {pct[1]:.3f}",
    )
    # Dependence: exact expectations for an AR(1) with phi = 0.5, n = 120, unit innovation
    # variance.
    phi, Nn, b = 0.5, 120, 12
    idx = np.arange(Nn)
    Sig = phi ** np.abs(idx[:, None] - idx[None, :]) / (1 - phi**2)
    var_mean = Sig.sum() / Nn**2
    e_iid = (np.trace(Sig) - Sig.sum() / Nn) / Nn**2
    L, kb = Nn - b + 1, Nn // b
    A = np.zeros((L, Nn))
    for j in range(L):
        A[j, j : j + b] = 1 / b
    Cm = np.eye(L) - np.ones((L, L)) / L
    e_mbb = np.trace(A.T @ Cm @ A @ Sig) / L / kb
    report.ok(
        "exact variance of the mean 0.03296; i.i.d. bootstrap expects 0.01084 (33%)",
        close(var_mean, 0.032963, 1e-6)
        and close(e_iid, 0.010836, 1e-6)
        and close(e_iid / var_mean, 0.328745, 1e-5),
    )
    report.ok(
        "moving blocks of 12 expect 0.02610 (79%): better, still biased down",
        close(e_mbb, 0.026105, 1e-6) and close(e_mbb / var_mean, 0.791935, 1e-5),
    )
    rng = np.random.default_rng(SEED + 2)
    reps = 4000
    e2 = rng.normal(0, 1, (reps, Nn))
    arr = np.empty_like(e2)
    arr[:, 0] = e2[:, 0] / math.sqrt(1 - phi**2)
    for t in range(1, Nn):
        arr[:, t] = phi * arr[:, t - 1] + e2[:, t]
    sim_var = arr.mean(1).var(ddof=1)
    sim_iid = np.mean(arr.var(1, ddof=0) / Nn)
    report.ok(
        "simulated AR(1) series agree with the exact values within 8%",
        abs(sim_var / var_mean - 1) < 0.08 and abs(sim_iid / e_iid - 1) < 0.08,
        f"{sim_var:.5f}, {sim_iid:.5f}",
    )


def check_monte_carlo(report: CheckReport) -> tuple[Floats, Floats, float]:
    """Part 6: Monte Carlo of a call against Black-Scholes, quantiles and variance reduction.

    Args:
        report: The run's report.

    Returns:
        The simulated terminal prices, the discounted payoffs and the closed-form value, which
        the control variate of part 7 uses.
    """
    print("== Monte Carlo against an analytic benchmark")
    d1 = (math.log(S0 / K) + (r + sg**2 / 2) * T) / (sg * math.sqrt(T))
    d2 = d1 - sg * math.sqrt(T)
    bsm = S0 * stats.norm.cdf(d1) - K * math.exp(-r * T) * stats.norm.cdf(d2)
    rng = np.random.default_rng(SEED)
    z = rng.standard_normal(M)
    ST = S0 * np.exp((r - sg**2 / 2) * T + sg * math.sqrt(T) * z)
    pay = math.exp(-r * T) * np.maximum(ST - K, 0)
    est, mse = pay.mean(), pay.std(ddof=1) / math.sqrt(M)
    report.ok("closed-form value 7.1281", close(bsm, 7.128065, 1e-5))
    report.ok(
        "100,000 draws, seed 20261018: estimate 7.1161, s.e. 0.0396, within 4 s.e. of the closed"
        " form",
        close(est, 7.116078, 1e-5) and close(mse, 0.039551, 1e-5) and abs(est - bsm) <= 4 * mse,
    )
    pr = float(np.mean(ST < 90))
    pr_exact = stats.norm.cdf((math.log(90 / S0) - (r - sg**2 / 2) * T) / (sg * math.sqrt(T)))
    report.ok(
        "P(S_T < 90): estimate 0.2821 against exact 0.2820, s.e. 0.0014",
        bool(
            close(pr, 0.28208, 1e-9)
            and close(pr_exact, 0.282036, 1e-5)
            and abs(pr - pr_exact) <= 4 * math.sqrt(pr * (1 - pr) / M)
        ),
    )
    report.ok(
        "quadrupling the draws halves the standard error (sqrt(M) rule)",
        close(pay[:25000].std(ddof=1) / math.sqrt(25000) / mse, 2.0, 0.05),
    )
    anti = 0.5 * (
        pay
        + math.exp(-r * T)
        * np.maximum(S0 * np.exp((r - sg**2 / 2) * T - sg * math.sqrt(T) * z) - K, 0)
    )
    report.ok(
        "antithetic pairs reduce the s.e. per payoff evaluated",
        anti.std(ddof=1) / math.sqrt(M) < mse / math.sqrt(2) * 1.0,
    )
    return ST, pay, bsm


def check_control_variate(report: CheckReport, ST: Floats, pay: Floats, bsm: float) -> None:
    """Part 7: the discounted terminal price as a control variate with an estimated coefficient.

    Args:
        report: The run's report.
        ST: The simulated terminal prices, from part 6.
        pay: The discounted payoffs, from part 6.
        bsm: The closed-form value, from part 6.
    """
    # Library gap-filling Batch L1 (2026-10-21), extension of meth:monte-carlo-simulation.
    # Acceptance fixed in before running: the same 100,000 draws, the discounted terminal price as
    # control (known mean S0), variance reduced by a factor above 2, estimate within 3 s.e. of
    # 7.1281.
    print("== control variate with an estimated coefficient")
    ctrl = math.exp(-r * T) * ST
    b_hat = np.cov(pay, ctrl)[0, 1] / ctrl.var(ddof=1)
    adj = pay - b_hat * (ctrl - S0)
    cv_est, cv_se = adj.mean(), adj.std(ddof=1) / math.sqrt(M)
    rho = np.corrcoef(pay, ctrl)[0, 1]
    report.ok(
        "estimated coefficient 0.542 and correlation 0.875; variance falls by 1/(1 - rho^2) = 4.25"
        " (above 2)",
        close(b_hat, 0.5421, 5e-4)
        and pay.var(ddof=1) / adj.var(ddof=1) > 2
        and close(pay.var(ddof=1) / adj.var(ddof=1), 1 / (1 - rho**2), 1e-3),
        f"b {b_hat:.4f}, rho {rho:.4f}, factor {pay.var(ddof=1) / adj.var(ddof=1):.2f}",
    )
    report.ok(
        "controlled estimate within 3 s.e. of 7.1281",
        abs(cv_est - bsm) <= 3 * cv_se,
        f"{cv_est:.4f} (s.e. {cv_se:.4f})",
    )
    report.ok(
        "Hull's fixed coefficient of 1 (eq. (21.20)) reduces the variance less here",
        (pay - (ctrl - S0)).var(ddof=1) > adj.var(ddof=1),
    )


def check_discretisation(report: CheckReport) -> None:
    """Part 8: Euler discretisation bias against sampling error, on the same Brownian paths.

    Args:
        report: The run's report.
    """
    # Discretisation bias against sampling error: Euler steps of dS = r S dt + sigma S dW on the
    # same Brownian paths as the exact solution. Criterion fixed before running: the bias at 2
    # steps exceeds 4 s.e. of the paired difference, and each halving of the step changes the bias
    # by a factor in [1.5, 2.5] (first order).
    print("== discretisation bias against sampling error")
    rng_e = np.random.default_rng(SEED + 11)
    Me, steps = 400_000, 16
    dWe = rng_e.standard_normal((Me, steps)) * math.sqrt(T / steps)
    exact_pay = math.exp(-r * T) * np.maximum(
        S0 * np.exp((r - sg**2 / 2) * T + sg * dWe.sum(1)) - K, 0
    )
    bias: dict[int, float] = {}
    bias_se: dict[int, float] = {}
    for n_steps in (2, 4, 8):
        inc = dWe.reshape(Me, n_steps, steps // n_steps).sum(2)
        s_e = np.full(Me, S0)
        for k in range(n_steps):
            s_e = s_e * (1 + r * T / n_steps + sg * inc[:, k])
        diff = math.exp(-r * T) * np.maximum(s_e - K, 0) - exact_pay
        bias[n_steps], bias_se[n_steps] = diff.mean(), diff.std(ddof=1) / math.sqrt(Me)
    report.ok(
        "Euler bias at 2 steps exceeds 4 s.e. of the paired difference",
        abs(bias[2]) > 4 * bias_se[2],
        ", ".join(f"{n}: {bias[n]:+.4f} (s.e. {bias_se[n]:.4f})" for n in bias),
    )
    report.ok(
        "the bias halves with the step (ratios in [1.5, 2.5]); more paths would not remove it",
        1.5 <= bias[2] / bias[4] <= 2.5 and 1.5 <= bias[4] / bias[8] <= 2.5,
        f"{bias[2] / bias[4]:.2f}, {bias[4] / bias[8]:.2f}",
    )


def main() -> int:
    """Print the versions, then run the eight parts with one report.

    Parts 1 and 2 share one generator, which part 2 continues from where part 1 left it.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
    x = np.array([1.2, -0.4, 0.8, 2.1, -1.5, 0.6, 1.9, -0.2, 0.3, 1.4, -0.9, 1.1])
    rng = np.random.default_rng(SEED)
    report = CheckReport()
    sims = check_confidence(report, rng, x)
    check_tests(report, rng, x, sims)
    check_nonparametric(report, x)
    check_historical(report)
    check_bootstrap(report, x)
    ST, pay, bsm = check_monte_carlo(report)
    check_control_variate(report, ST, pay, bsm)
    check_discretisation(report)
    if report.failures:
        print("FAILED:", ", ".join(report.failures))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
