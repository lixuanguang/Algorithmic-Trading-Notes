"""Return statistics, conditional moments, distributions and Bayesian updating, by two routes.

Batch 2 foundations (2026-10-18): the worked examples of def:return-sample-statistics,
def:return-shape-statistics, def:return-dependence, def:downside-relative-dispersion,
def:conditional-moments, def:financial-distributions and meth:bayesian-updating.

Every value is computed twice: by the formula written in the entry (plain Python) and by an
independent route (numpy or scipy implementations, enumeration of a probability table, numerical
integration, or sequential updating). The return series and the probability table are invented for
illustration; they are not data on any asset or strategy. One generator, seeded 20261018, is created
per run and draws the t(1.5) sample of the last part.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.statistics_probability
(numpy, scipy). Exits 1 on failure.
"""

import math
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Final

import numpy as np
from scipy import integrate, stats

from trading_notes.numerical.report import CheckReport

SEED: Final = 20261018
# Eight monthly returns, percent.
A: Final = (2.0, -1.5, 3.0, 0.5, -4.0, 1.5, 2.5, -0.5)
B: Final = (1.0, -0.5, 1.5, 0.0, -2.5, 1.0, 2.0, 0.5)
# Three hypotheses for the monthly up-probability, and their prior.
HYP: Final = (0.45, 0.50, 0.55)
PRIOR: Final = (0.25, 0.50, 0.25)


@dataclass(frozen=True)
class Location:
    """The location and dispersion of the two series that parts 2-4 build on.

    Attributes:
        mean_a: The mean of A.
        mean_b: The mean of B.
        median: The median of A.
        var_pop: A's population variance (divide by N).
        var_smp: A's sample variance (divide by N - 1).
    """

    mean_a: float
    mean_b: float
    median: float
    var_pop: float
    var_smp: float


def close(a: float, b: float, tol: float = 1e-6) -> bool:
    """Return whether |a - b| <= tol."""
    return abs(a - b) <= tol


def percentile_n_plus_1(y: Sequence[float], p: float) -> float:
    """The p(N+1) rule with linear interpolation, clamped at the extremes."""
    y = sorted(y)
    h = p * (len(y) + 1)
    k, d = int(h), h - int(h)
    if k == 0:
        return y[0]
    if k >= len(y):
        return y[-1]
    return y[k - 1] + d * (y[k] - y[k - 1])


def semidev(r: Iterable[float], target: float, denominator: float) -> float:
    """Return the semi-deviation below the target, dividing by the given denominator."""
    s = sum(min(v - target, 0) ** 2 for v in r)
    return math.sqrt(s / denominator)


def check_location(report: CheckReport) -> Location:
    """Part 1: location and dispersion, with population and sample denominators."""
    n = len(A)
    mean_a = sum(A) / n
    mean_b = sum(B) / n

    print("== location and dispersion (population against sample denominators)")
    report.ok(
        "mean A 0.4375", close(mean_a, 0.4375) and close(np.float64(np.mean(A)), mean_a, 1e-12)
    )
    srt = sorted(A)
    median = (srt[n // 2 - 1] + srt[n // 2]) / 2
    report.ok(
        "median A 1.0 (average of 4th and 5th ordered values)",
        bool(median == 1.0 and np.median(A) == median),
    )
    ss = sum((x - mean_a) ** 2 for x in A)
    var_pop, var_smp = ss / n, ss / (n - 1)
    report.ok(
        "population variance 4.8398 (divide by N)",
        close(var_pop, 4.83984375, 1e-12) and close(np.float64(np.var(A)), var_pop, 1e-12),
    )
    report.ok(
        "sample variance 5.5313 (divide by N-1)",
        close(var_smp, 5.53125, 1e-12) and close(np.float64(np.var(A, ddof=1)), var_smp, 1e-12),
    )
    report.ok(
        "standard deviations 2.2000 and 2.3519",
        close(math.sqrt(var_pop), 2.199964, 1e-6) and close(math.sqrt(var_smp), 2.351861, 1e-6),
    )
    report.ok("range 7.0", max(A) - min(A) == 7.0)
    aad = sum(abs(x - mean_a) for x in A) / n
    report.ok("average absolute deviation 1.8281", close(aad, 1.828125, 1e-12))
    mad = sorted(abs(x - median) for x in A)
    report.ok("median absolute deviation 1.5", (mad[3] + mad[4]) / 2 == 1.5)

    q1, q3 = percentile_n_plus_1(A, 0.25), percentile_n_plus_1(A, 0.75)
    report.ok(
        "quartiles by the p(N+1) rule -1.25 and 2.375, IQR 3.625",
        close(q1, -1.25) and close(q3, 2.375) and close(q3 - q1, 3.625),
    )
    report.ok(
        "the same rule is numpy method weibull",
        close(np.percentile(A, 25, method="weibull"), q1, 1e-12)
        and close(np.percentile(A, 75, method="weibull"), q3, 1e-12),
    )
    r7 = np.percentile(A, [25, 75])  # numpy default = Hyndman-Fan type 7
    report.ok(
        "the type-7 rule gives -0.75 and 2.125 instead", close(r7[0], -0.75) and close(r7[1], 2.125)
    )
    report.ok(
        "10th percentile: p(N+1) clamps to the minimum -4.0; type 7 gives -2.25",
        percentile_n_plus_1(A, 0.10) == -4.0 and close(np.percentile(A, 10), -2.25),
    )
    return Location(mean_a, mean_b, median, var_pop, var_smp)


def check_shape(report: CheckReport, loc: Location) -> None:
    """Part 2: skewness and kurtosis, as moment ratios and bias-adjusted."""
    n, mean_a = len(A), loc.mean_a
    print("== skewness and kurtosis (moment ratios with N denominators; excess = kurtosis - 3)")
    m2, m3, m4 = (sum((x - mean_a) ** k for x in A) / n for k in (2, 3, 4))
    g1 = m3 / m2**1.5
    kurt = m4 / m2**2
    G1 = math.sqrt(n * (n - 1)) / (n - 2) * g1
    report.ok("skewness g1 -0.7615", close(g1, -0.761486, 1e-6) and close(stats.skew(A), g1, 1e-12))
    report.ok(
        "adjusted skewness G1 -0.9497",
        close(G1, -0.949740, 1e-6) and close(stats.skew(A, bias=False), G1, 1e-12),
    )
    report.ok(
        "kurtosis 2.5138, excess kurtosis -0.4862",
        close(kurt, 2.513780, 1e-6)
        and close(stats.kurtosis(A, fisher=False), kurt, 1e-12)
        and close(stats.kurtosis(A), kurt - 3, 1e-12),
    )
    G2 = (n - 1) / ((n - 2) * (n - 3)) * ((n + 1) * (kurt - 3) + 6)
    report.ok(
        "bias-adjusted excess kurtosis +0.3789 (sign differs from the moment ratio)",
        close(G2, 0.378939, 1e-6) and close(stats.kurtosis(A, bias=False), G2, 1e-12),
    )
    report.ok("mean below median with negative skewness", mean_a < loc.median and g1 < 0)


def check_covariance(report: CheckReport, loc: Location) -> None:
    """Part 3: covariance with both denominators, correlation, and units."""
    n, mean_a, mean_b = len(A), loc.mean_a, loc.mean_b
    print("== covariance and correlation")
    cov_pop = sum((a - mean_a) * (b - mean_b) for a, b in zip(A, B)) / n
    cov_smp = cov_pop * n / (n - 1)
    sd_b_pop = math.sqrt(sum((b - mean_b) ** 2 for b in B) / n)
    corr = cov_pop / (math.sqrt(loc.var_pop) * sd_b_pop)
    report.ok(
        "covariance 2.7734 (N) and 3.1696 (N-1), percent squared",
        close(cov_pop, 2.7734375, 1e-12)
        and close(cov_smp, 3.169643, 1e-6)
        and close(np.cov(A, B)[0, 1], cov_smp, 1e-12),
    )
    report.ok(
        "correlation 0.9573, the same with either denominator",
        close(corr, 0.957263, 1e-6) and close(np.corrcoef(A, B)[0, 1], corr, 1e-12),
    )
    report.ok(
        "covariance in decimals is 1/10,000 of the percent figure; correlation unchanged",
        close(np.cov(np.array(A) / 100, np.array(B) / 100)[0, 1], cov_smp / 1e4, 1e-15)
        and close(np.corrcoef(np.array(A) / 100, np.array(B) / 100)[0, 1], corr, 1e-12),
    )
    x = [-2, -1, 0, 1, 2]
    y = [v * v for v in x]
    report.ok(
        "a perfect nonlinear dependence can have zero correlation",
        close(np.corrcoef(x, y)[0, 1], 0.0, 1e-12),
    )


def check_semideviation(report: CheckReport, loc: Location) -> None:
    """Part 4: semi-deviation under four conventions, and the coefficient of variation."""
    n, mean_a, mean_b = len(A), loc.mean_a, loc.mean_b
    print("== semi-deviation and coefficient of variation")
    report.ok(
        "target 0, divide by N (all observations): 1.5207", close(semidev(A, 0, n), 1.520691, 1e-6)
    )
    report.ok("target 0, divide by N-1: 1.6257", close(semidev(A, 0, n - 1), 1.625687, 1e-6))
    report.ok(
        "target 0, divide by the 3 shortfalls only: 2.4833", close(semidev(A, 0, 3), 2.483277, 1e-6)
    )
    report.ok(
        "target = mean 0.4375, divide by N: 1.7437", close(semidev(A, mean_a, n), 1.743711, 1e-6)
    )
    shortfalls = np.minimum(np.array(A), 0)
    report.ok(
        "vectorised route agrees", close(np.sqrt(np.mean(shortfalls**2)), semidev(A, 0, n), 1e-12)
    )
    sym = [-2.0, -1.0, 0.0, 1.0, 2.0]
    report.ok(
        "symmetric data: semi-deviation about the mean (N) = s.d.(N)/sqrt(2)",
        close(semidev(sym, 0.0, 5), np.float64(np.std(sym) / math.sqrt(2)), 1e-12),
    )
    report.ok(
        "asset A ratio 0.79 > 0.707 (heavier downside)",
        close(semidev(A, mean_a, n) / math.sqrt(loc.var_pop), 0.792617, 1e-5),
    )
    cv_a = math.sqrt(loc.var_smp) / mean_a
    cv_b = np.float64(np.std(B, ddof=1) / mean_b)
    report.ok(
        "CV A 5.38, CV B 3.75 (sample s.d. / mean)",
        close(cv_a, 5.375682, 1e-6) and close(cv_b, 3.754363, 1e-6),
    )
    shifted = [v - 0.5 for v in A]
    cv_shift = np.float64(np.std(shifted, ddof=1) / np.mean(shifted))
    report.ok(
        "shifting returns by -0.5 points leaves s.d. unchanged and makes CV -37.63",
        close(np.float64(np.std(shifted, ddof=1)), math.sqrt(loc.var_smp), 1e-12)
        and close(cv_shift, -37.629775, 1e-5),
    )


def check_conditional_moments(report: CheckReport) -> None:
    """Part 5: moments of a probability table, and the laws of total expectation and variance."""
    print("== unconditional and conditional moments from a probability table")
    # state, equity return X, bond return Z (percent), probability
    cells = [
        ("boom", 12, 0, 0.125),
        ("boom", 8, 2, 0.125),
        ("normal", 6, 2, 0.25),
        ("normal", 4, 3, 0.25),
        ("recession", -6, 6, 0.125),
        ("recession", -10, 8, 0.125),
    ]
    p = np.array([c[3] for c in cells])
    X = np.array([c[1] for c in cells], float)
    Z = np.array([c[2] for c in cells], float)
    EX, EZ = p @ X, p @ Z
    VX, VZ = p @ (X - EX) ** 2, p @ (Z - EZ) ** 2
    CXZ = p @ ((X - EX) * (Z - EZ))
    report.ok("probabilities sum to one", close(p.sum(), 1.0, 1e-15))
    report.ok("E[X] 3.0, E[Z] 3.25", close(EX, 3.0) and close(EZ, 3.25))
    report.ok(
        "Var X 47.0, Var Z 5.6875, Cov -16.25, corr -0.9939",
        close(VX, 47.0)
        and close(VZ, 5.6875)
        and close(CXZ, -16.25)
        and close(CXZ / math.sqrt(VX * VZ), -0.993902, 1e-6),
    )
    report.ok("E[X^2] - E[X]^2 agrees", close(p @ X**2 - EX**2, VX))
    states = {}
    for s in ("boom", "normal", "recession"):
        mask = np.array([c[0] == s for c in cells])
        ps = p[mask].sum()
        w = p[mask] / ps
        ex, ez = w @ X[mask], w @ Z[mask]
        states[s] = (ps, ex, ez, w @ (X[mask] - ex) ** 2, w @ ((X[mask] - ex) * (Z[mask] - ez)))
    report.ok(
        "E[X|boom] 10, E[X|normal] 5, E[X|recession] -8",
        [round(states[s][1], 9) for s in states] == [10, 5, -8],
    )
    report.ok("Var(X|state) 4, 1, 4", [round(states[s][3], 9) for s in states] == [4, 1, 4])
    tot_e = sum(ps * ex for ps, ex, *_ in states.values())
    e_var = sum(ps * v for ps, ex, ez, v, c in states.values())
    var_e = sum(ps * (ex - EX) ** 2 for ps, ex, *_ in states.values())
    e_cov = sum(ps * c for ps, ex, ez, v, c in states.values())
    cov_e = sum(ps * (ex - EX) * (ez - EZ) for ps, ex, ez, v, c in states.values())
    report.ok("total expectation: sum of P(state) E[X|state] = 3.0", close(tot_e, EX))
    report.ok(
        "total variance: E[Var] 2.5 + Var[E] 44.5 = 47.0",
        close(e_var, 2.5) and close(var_e, 44.5) and close(e_var + var_e, VX),
    )
    report.ok(
        "total covariance: E[Cov] -1.25 + Cov[E] -15.0 = -16.25",
        close(e_cov, -1.25) and close(cov_e, -15.0) and close(e_cov + cov_e, CXZ),
    )


def check_distributions(report: CheckReport) -> None:
    """Part 6: normal, lognormal, Student t, binomial and uniform closed forms."""
    print("== distributions: closed forms against scipy and numerical integration")
    mu, sd = 0.8, 4.0
    report.ok(
        "normal: P(R < -5) 7.35%; 5% quantile -5.7794",
        close(stats.norm.cdf(-5, mu, sd), 0.073529, 1e-6)
        and close(mu - 1.6448536 * sd, -5.779414, 1e-6)
        and close(stats.norm.ppf(0.05, mu, sd), -5.779415, 1e-6),
    )
    S0, m, s = 100.0, 0.05, 0.20
    w = math.exp(s * s)
    ln_mean, ln_med, ln_mode = (
        S0 * math.exp(m + s * s / 2),
        S0 * math.exp(m),
        S0 * math.exp(m - s * s),
    )
    ln_var = ln_mean**2 * (w - 1)
    pdf = stats.lognorm(s=s, scale=S0 * math.exp(m)).pdf
    num_mean = integrate.quad(lambda v: v * pdf(v), 0, np.inf)[0]
    num_var = integrate.quad(lambda v: (v - num_mean) ** 2 * pdf(v), 0, np.inf)[0]
    report.ok(
        "lognormal mean 107.2508 > median 105.1271 > mode 101.0050",
        close(ln_mean, 107.250818, 1e-5)
        and close(ln_med, 105.127110, 1e-5)
        and close(ln_mode, 101.005017, 1e-5),
    )
    report.ok(
        "lognormal mean and variance by integration",
        close(num_mean, ln_mean, 1e-6) and close(num_var, ln_var, 1e-4),
        f"{ln_var:.4f}",
    )
    report.ok(
        "lognormal skewness 0.6143, kurtosis 3.6784 (NIST forms)",
        close((w + 2) * math.sqrt(w - 1), 0.614295, 1e-6)
        and close(w**4 + 2 * w**3 + 3 * w**2 - 3, 3.678366, 1e-6),
    )
    for nu, var, exk in ((5, 5 / 3, 6.0), (10, 1.25, 1.0)):
        tvar = integrate.quad(lambda v: v * v * stats.t.pdf(v, nu), -np.inf, np.inf)[0]
        report.ok(
            f"t({nu}): variance {var:.4f} by integration, excess kurtosis {exk}",
            close(tvar, var, 1e-7)
            and close(3 * (nu - 2) / (nu - 4) - 3, exk, 1e-12)
            and close(stats.t.stats(nu, moments="k"), exk, 1e-12),
        )
    partial = [
        integrate.quad(lambda v: v * v * stats.t.pdf(v, 2), -L, L, limit=200)[0]
        for L in (10, 100, 1000)
    ]
    report.ok(
        "t(2): truncated second moment keeps growing (no finite variance)",
        partial[0] < partial[1] < partial[2] and partial[2] > 10,
        ", ".join(f"{v:.2f}" for v in partial),
    )
    nu = 5
    report.ok(
        "unit-variance t(5) scale sqrt(3/5) = 0.7746",
        close(math.sqrt((nu - 2) / nu), 0.774597, 1e-6)
        and close(stats.t.var(nu, scale=math.sqrt((nu - 2) / nu)), 1.0, 1e-12),
    )
    nb, pb = 12, 0.55
    pmf = [math.comb(nb, k) * pb**k * (1 - pb) ** (nb - k) for k in range(nb + 1)]
    mean_e = sum(k * q for k, q in enumerate(pmf))
    var_e2 = sum((k - mean_e) ** 2 * q for k, q in enumerate(pmf))
    sk_e = sum((k - mean_e) ** 3 * q for k, q in enumerate(pmf)) / var_e2**1.5
    ku_e = sum((k - mean_e) ** 4 * q for k, q in enumerate(pmf)) / var_e2**2
    npq = nb * pb * (1 - pb)
    report.ok(
        "binomial(12, 0.55): mean 6.6, variance 2.97 by enumeration",
        close(mean_e, 6.6, 1e-12) and close(var_e2, 2.97, 1e-12),
    )
    report.ok(
        "skewness -0.0580 and kurtosis 2.8367 by enumeration and by formula",
        close(sk_e, (1 - 2 * pb) / math.sqrt(npq), 1e-12)
        and close(ku_e, 3 - 6 / nb + 1 / npq, 1e-12)
        and close(ku_e, 2.836700, 1e-6),
    )

    ua, ub = -3.0, 5.0
    umean = integrate.quad(lambda v: v / (ub - ua), ua, ub)[0]
    uvar = integrate.quad(lambda v: (v - umean) ** 2 / (ub - ua), ua, ub)[0]
    uk = integrate.quad(lambda v: (v - umean) ** 4 / (ub - ua), ua, ub)[0] / uvar**2
    report.ok(
        "uniform(-3, 5): mean 1.0, s.d. 2.3094 = 8/sqrt(12), kurtosis 9/5 by integration",
        close(umean, 1.0, 1e-12)
        and close(math.sqrt(uvar), 8 / math.sqrt(12), 1e-12)
        and close(uk, 1.8, 1e-12),
    )


def check_bayesian(report: CheckReport) -> None:
    """Part 7: a Bayesian update over three hypotheses, at once and month by month."""
    print("== Bayesian update over three hypotheses for the monthly up-probability")
    k_up, N = 14, 20
    lik = [math.comb(N, k_up) * h**k_up * (1 - h) ** (N - k_up) for h in HYP]
    joint = [a * b for a, b in zip(lik, PRIOR)]
    evidence = sum(joint)
    post = [j / evidence for j in joint]
    report.ok("evidence (normalising constant) 0.040877", close(evidence, 0.040877, 1e-6))
    report.ok(
        "posterior 0.0916, 0.4521, 0.4562; sums to one",
        close(post[0], 0.091621, 1e-6)
        and close(post[1], 0.452139, 1e-6)
        and close(post[2], 0.456241, 1e-6)
        and close(sum(post), 1.0, 1e-15),
    )
    seq = [1] * k_up + [0] * (N - k_up)
    seq = seq[::2] + seq[1::2]  # any order of 14 ups and 6 downs
    belief = list(PRIOR)
    for up in seq:
        belief = [b * (h if up else 1 - h) for b, h in zip(belief, HYP)]
        total = sum(belief)
        belief = [b / total for b in belief]
    report.ok(
        "updating one month at a time, in any order, gives the same posterior",
        all(close(a, b, 1e-12) for a, b in zip(belief, post)),
    )
    pred_prior = sum(a * b for a, b in zip(PRIOR, HYP))
    pred_post = sum(a * b for a, b in zip(post, HYP))
    report.ok(
        "predictive P(up next month): 0.5000 before, 0.5182 after",
        close(pred_prior, 0.5, 1e-12) and close(pred_post, 0.518231, 1e-6),
    )
    report.ok(
        "the 0.70 sample frequency is not the posterior estimate",
        close(k_up / N, 0.70) and pred_post < 0.55,
    )


def check_corrections(report: CheckReport, rng: np.random.Generator) -> None:
    """Part 8: the counterexamples behind the corrections of 2026-10-18."""
    print("== corrections of 2026-10-18: counterexamples")
    # (1) Unbiasedness of s^2 needs independent observations: X1 = X2 = Z, Z = -1 or +1
    # equally likely.
    samples = [([-1.0, -1.0], 0.5), ([1.0, 1.0], 0.5)]
    exp_s2 = np.float64(sum(pr * np.var(x, ddof=1) for x, pr in samples))
    report.ok(
        "perfectly dependent pair: marginal variance 1, expected sample variance 0",
        close(exp_s2, 0.0, 1e-15),
    )
    # Exact enumeration with independent X1, X2 (same marginal) recovers 1.
    exp_s2_iid = np.float64(
        sum(0.25 * np.var([a, b], ddof=1) for a in (-1.0, 1.0) for b in (-1.0, 1.0))
    )
    report.ok(
        "independent pair: expected sample variance 1 (unbiased)", close(exp_s2_iid, 1.0, 1e-15)
    )
    # (2) High kurtosis without central mass.
    vals, prs = np.array([-10.0, -1.0, 1.0, 10.0]), np.array([0.005, 0.495, 0.495, 0.005])
    v = prs @ vals**2
    k = (prs @ vals**4) / v**2
    sdv = math.sqrt(v)
    report.ok(
        "variance 1.99, kurtosis 25.5019",
        close(v, 1.99, 1e-12) and close(k, 25.501881, 1e-5),
        f"{k:.6f}",
    )
    report.ok(
        "no mass within half a s.d. of the mean; matching normal has 0.3829",
        bool(
            prs[np.abs(vals) < 0.5 * sdv].sum() == 0
            and close(stats.norm.cdf(0.5) - stats.norm.cdf(-0.5), 0.382925, 1e-6)
        ),
    )
    # (3) A finite sample from t(1.5) has finite sample variance; the population variance is
    # infinite.
    draw = stats.t.rvs(1.5, size=1000, random_state=rng)
    report.ok(
        "t(1.5): finite sample variance; population variance infinite",
        bool(np.isfinite(np.var(draw, ddof=1)) and np.isinf(stats.t.var(1.5))),
    )
    report.ok(
        "t(0.9): mean undefined (nu <= 1); t(2.5): finite variance 5 (nu > 2)",
        bool(not np.isfinite(stats.t.mean(0.9)) and close(stats.t.var(2.5), 5.0, 1e-12)),
    )
    report.ok(
        "t(1.5) mean 0 exists, variance inf; t(3.5) kurtosis inf; t(4.5) finite",
        bool(
            stats.t.mean(1.5) == 0
            and np.isinf(stats.t.var(1.5))
            and np.isinf(stats.t.stats(3.5, moments="k"))
            and np.isfinite(stats.t.stats(4.5, moments="k"))
        ),
    )
    # (4) GBM drift against mean log return: drift 0.07, log mean 0.05, sigma 0.20.
    report.ok(
        "mean price uses drift: 100 exp(0.05 + 0.02) = 100 exp(0.07)",
        close(100 * math.exp(0.05 + 0.02), 100 * math.exp(0.07), 1e-12),
    )
    # (5) Conditional, not unconditional, independence in the Bayesian prior mixture.
    p_uu = sum(pr * h * h for pr, h in zip(PRIOR, HYP))
    p_u = sum(pr * h for pr, h in zip(PRIOR, HYP))
    report.ok(
        "P(up, up) = 0.25125 > P(up)^2 = 0.25",
        close(p_uu, 0.25125, 1e-12) and close(p_u**2, 0.25, 1e-12),
    )


def main() -> int:
    """Run the eight parts with one report.

    Returns:
        The exit status, 0 or 1.
    """
    rng = np.random.default_rng(SEED)
    report = CheckReport()
    loc = check_location(report)
    check_shape(report, loc)
    check_covariance(report, loc)
    check_semideviation(report, loc)
    check_conditional_moments(report)
    check_distributions(report)
    check_bayesian(report)
    check_corrections(report, rng)
    if report.failures:
        print("FAILED:", ", ".join(report.failures))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
