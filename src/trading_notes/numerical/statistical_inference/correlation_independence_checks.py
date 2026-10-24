"""Worked examples of tests of correlation and independence, and their size by simulation."""

import math
import sys
from collections.abc import Callable
from typing import Final

import numpy as np
import scipy
from numpy.typing import NDArray
from scipy import stats

from trading_notes.numerical.report import CheckReport, print_versions
from trading_notes.numerical.statistical_inference.correlation_tests import (
    ContingencyTable,
    CorrelationTTest,
    spearman,
    spearman_shortcut,
)

type Floats = NDArray[np.float64]

SEED_SIZE: Final = 20261101  # Part 2b
SEED_FORMULAS: Final = 20261102  # Part 2
SEED_OVERLAP: Final = 20261103  # Part 3


def check_openstax(report: CheckReport) -> ContingencyTable:
    """Part 1: the OpenStax examples; return Example 11.6's table."""
    print("== Part 1: OpenStax examples")
    test = CorrelationTTest(pairs=11)
    t, p = test.statistic(0.6631), test.p_value(0.6631)
    report.ok(
        "sec. 12.4: r = 0.6631, n = 11 gives p = 0.026",
        round(p, 3) == 0.026,
        f"t {t:.4f}, p {p:.5f}",
    )
    crit = {11: 0.602, 10: 0.632, 14: 0.532, 6: 0.811, 19: 0.456, 9: 0.666}
    got = {n: CorrelationTTest(pairs=n).critical_r() for n in crit}
    report.ok(
        "critical values of r at 5% for n = 11, 10, 14, 6, 19, 9 are 0.602, 0.632, 0.532, 0.811,"
        " 0.456, 0.666",
        all(round(got[n], 3) == v for n, v in crit.items()),
        ", ".join(f"{got[n]:.4f}" for n in crit),
    )
    vol = ContingencyTable(counts=((111, 96, 48), (96, 133, 61), (91, 150, 53)))
    stat, df, p, e = vol.statistic(), vol.dof, vol.p_value(), vol.expected()
    report.ok(
        "Example 11.6: chi-square 12.9909, df 4, p = 0.0113; expected counts 90.57 ... 56.77",
        round(stat, 4) == 12.9909
        and df == 4
        and round(p, 4) == 0.0113
        and round(e[0, 0], 2) == 90.57
        and round(e[2, 2], 2) == 56.77,
        f"{stat:.4f}, {df}, {p:.5f}",
    )
    speed = 305 * 70 / 755
    report.ok(
        "Example 11.5: expected count for phone use and a violation is 28.3",
        round(speed, 1) == 28.3,
        f"{speed:.3f}",
    )
    return vol


def check_formulas(report: CheckReport, rng: np.random.Generator, vol: ContingencyTable) -> None:
    """Part 2: the formulas against SciPy, ties and transforms."""
    print("== Part 2: formulas against SciPy, ties and transforms")
    x = rng.standard_normal(40)
    y = 0.4 * x + rng.standard_normal(40)
    r = float(np.corrcoef(x, y)[0, 1])
    report.ok(
        "the t-test p-value equals scipy.stats.pearsonr to 1e-12",
        bool(abs(CorrelationTTest(pairs=40).p_value(r) - stats.pearsonr(x, y).pvalue) < 1e-12),
    )
    xt = np.array([1, 2, 2, 3, 4, 4, 4, 5, 6, 7, 7, 8], dtype=float)
    yt = np.array([2, 1, 3, 3, 5, 4, 6, 6, 5, 8, 9, 9], dtype=float)
    for name, (a, b) in {"without ties": (x, y), "with ties": (xt, yt)}.items():
        sp = stats.spearmanr(a, b)
        report.ok(
            f"Spearman equals Pearson on midranks and scipy.stats.spearmanr, {name}, to 1e-12",
            abs(spearman(a, b) - float(sp.statistic)) < 1e-12,
            f"{spearman(a, b):.6f}",
        )
    rs = spearman(xt, yt)
    report.ok(
        "with ties the shortcut 1 - 6 sum d^2 / (n(n^2 - 1)) differs from Pearson on midranks;"
        " without ties they agree",
        abs(spearman_shortcut(xt, yt) - rs) > 1e-4
        and abs(spearman_shortcut(x, y) - spearman(x, y)) < 1e-12,
        f"tied fixture: midrank Pearson {rs:.6f}, shortcut {spearman_shortcut(xt, yt):.6f}",
    )
    inc: list[Callable[[Floats], Floats]] = [np.exp, lambda v: v**3 + v]
    report.ok(
        "unchanged to 1e-12 by strictly increasing transforms of either variable, ties included",
        all(
            abs(spearman(f(xt), yt) - rs) < 1e-12 and abs(spearman(xt, f(yt)) - rs) < 1e-12
            for f in inc
        ),
    )
    report.ok(
        "a strictly decreasing transform of one variable flips the sign; of both leaves it"
        " unchanged",
        abs(spearman(-xt, yt) + rs) < 1e-12 and abs(spearman(np.exp(-xt), -(yt**3)) - rs) < 1e-12,
    )
    weak = np.floor(xt / 3)
    print(
        f"  (not tested) a weakly monotone transform, floor(x/3), creates ties and gives"
        f" {spearman(weak, yt):.6f}"
    )
    report.ok(
        "the chi-square statistic equals scipy.stats.chi2_contingency without continuity"
        " correction to 1e-12",
        bool(
            abs(vol.statistic() - stats.chi2_contingency(vol.counts, correction=False).statistic)
            < 1e-12
        ),
    )


def check_size(report: CheckReport, rng: np.random.Generator) -> None:
    """Part 2b: the size of the 5% tests on 20,000 independent normal pairs of n = 30."""
    print("== Part 2b: size of the 5% tests, 20,000 independent normal pairs of n = 30")
    n, reps = 30, 20_000
    test = CorrelationTTest(pairs=n)
    rej_p = rej_s = rej_z = 0
    for _ in range(reps):
        a, b = rng.standard_normal(n), rng.standard_normal(n)
        r = float(np.corrcoef(a, b)[0, 1])
        rej_p += test.p_value(r) < 0.05
        rho = spearman(a, b)
        rej_s += test.p_value(rho) < 0.05
        rej_z += 2 * stats.norm.sf(abs(rho) * math.sqrt(n - 1)) < 0.05
    report.ok(
        "Pearson t-test rejects in 5 +- 0.5% of replications",
        abs(100 * rej_p / reps - 5) <= 0.5,
        f"{100 * rej_p / reps:.2f}%",
    )
    report.ok(
        "Spearman (t approximation on midranks) rejects in 5 +- 0.5% of replications",
        abs(100 * rej_s / reps - 5) <= 0.5,
        f"{100 * rej_s / reps:.2f}%",
    )
    print(
        f"  (reported) Spearman with NIST's normal approximation z = rho sqrt(n - 1):"
        f" {100 * rej_z / reps:.2f}%"
    )


def report_overlap(rng: np.random.Generator) -> None:
    """Part 3 (diagnostic): rejection rates against one-day and overlapping 20-day returns."""
    print(
        "== Part 3 (diagnostic): overlapping horizons, a persistent signal and independent returns"
    )
    T, h, phi, reps3 = 500, 20, 0.95, 2_000
    test = CorrelationTTest(pairs=T)
    rej_daily = rej_overlap = 0
    for _ in range(reps3):
        e = rng.standard_normal(T + h)
        s = np.empty(T + h)
        s[0] = e[0] / math.sqrt(1 - phi**2)
        for i in range(1, T + h):
            s[i] = phi * s[i - 1] + e[i]
        ret = rng.standard_normal(T + h)
        # sum of returns t+1..t+h, overlapping
        fwd = np.convolve(ret, np.ones(h), mode="valid")[1 : T + 1]
        rej_daily += test.p_value(float(np.corrcoef(s[:T], ret[1 : T + 1])[0, 1])) < 0.05
        rej_overlap += test.p_value(float(np.corrcoef(s[:T], fwd)[0, 1])) < 0.05
    print(
        f"  signal AR(1) phi 0.95 against independent returns, T = 500, 2,000 replications: 5%"
        f" t-test rejects"
        f" {100 * rej_daily / reps3:.1f}% with one-day returns and"
        f" {100 * rej_overlap / reps3:.1f}% with overlapping 20-day returns"
    )


def main() -> int:
    """Print the versions, then run the parts with one report, each part's generator its own.

    Part 1 reproduces OpenStax Introductory Statistics 2e, sec. 12.4 (r = 0.6631 with n = 11
    gives p = 0.026; the critical values of r) and sec. 11.3, Example 11.6 (chi-square 12.9909,
    df 4, p = 0.0113). Part 2 checks the formulas against SciPy, Spearman's rank correlation with
    and without ties and under monotone transforms, and the size of the 5 percent tests on 20,000
    replications of independent normal pairs with n = 30. The Spearman test for the size check
    is the t approximation on midranks, t = rho_s sqrt(n - 2)/sqrt(1 - rho_s^2) with n - 2
    degrees of freedom (as scipy.stats.spearmanr computes it); NIST Dataplot's normal
    approximation z = rho_s sqrt(n - 1) is reported beside it. Part 3 is our own diagnostic: the
    rejection rate of the t-test when a persistent signal is correlated with overlapping
    multi-day returns, all independent. Seeds: SEED_FORMULAS, SEED_SIZE and SEED_OVERLAP.

    Returns:
        The exit status, 0 or 1.
    """
    print_versions(np, scipy)
    report = CheckReport()
    vol = check_openstax(report)
    check_formulas(report, np.random.default_rng(SEED_FORMULAS), vol)
    check_size(report, np.random.default_rng(SEED_SIZE))
    report_overlap(np.random.default_rng(SEED_OVERLAP))
    if report.failures:
        print("FAILED:", ", ".join(report.failures))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
