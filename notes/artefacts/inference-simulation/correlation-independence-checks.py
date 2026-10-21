"""Library gap-filling Batch L2, package P11a (2026-10-21): the worked examples of
meth:correlation-independence-tests.

Part 1 reproduces OpenStax Introductory Statistics 2e, sec. 12.4 (r = 0.6631 with n = 11 gives p = 0.026; the
critical values of r) and sec. 11.3, Example 11.6 (chi-square 12.9909, df 4, p = 0.0113). Part 2 checks the
formulas against SciPy, Spearman's rank correlation with and without ties and under monotone transforms, and the size
of the 5 percent tests on 20,000 replications of independent normal pairs with n = 30 (seed 20261101; the formula checks draw from seed 20261102). The Spearman
test for the size check is the t approximation on midranks, t = rho_s sqrt(n - 2)/sqrt(1 - rho_s^2) with n - 2 degrees
of freedom (as scipy.stats.spearmanr computes it), fixed before the first run; NIST Dataplot's normal approximation
z = rho_s sqrt(n - 1) is reported beside it. Part 3 is a diagnostic of my own: the rejection rate of the t-test when a
persistent signal is correlated with overlapping multi-day returns, all independent (seed 20261103).

Run: uv run python correlation-independence-checks.py   (numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import math
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


def corr_t_test(r, n):
    """OpenStax sec. 12.4: t = r sqrt(n - 2)/sqrt(1 - r^2), n - 2 degrees of freedom, two-sided p-value."""
    t = r * math.sqrt(n - 2) / math.sqrt(1 - r * r)
    return t, 2 * stats.t.sf(abs(t), n - 2)


def critical_r(n, alpha=0.05):
    tc = stats.t.ppf(1 - alpha / 2, n - 2)
    return tc / math.sqrt(tc * tc + n - 2)


def midranks(x):
    return stats.rankdata(x, method="average")


def spearman(x, y):
    return float(np.corrcoef(midranks(x), midranks(y))[0, 1])


def shortcut(x, y):
    d = midranks(x) - midranks(y)
    n = len(x)
    return 1 - 6 * float(np.sum(d * d)) / (n * (n * n - 1))


def chi2_independence(table):
    o = np.asarray(table, dtype=float)
    e = np.outer(o.sum(axis=1), o.sum(axis=0)) / o.sum()
    stat = float(np.sum((o - e) ** 2 / e))
    df = (o.shape[0] - 1) * (o.shape[1] - 1)
    return stat, df, stats.chi2.sf(stat, df), e


print("== Part 1: OpenStax examples")
t, p = corr_t_test(0.6631, 11)
ok("sec. 12.4: r = 0.6631, n = 11 gives p = 0.026", round(p, 3) == 0.026, f"t {t:.4f}, p {p:.5f}")
crit = {11: 0.602, 10: 0.632, 14: 0.532, 6: 0.811, 19: 0.456, 9: 0.666}
got = {n: critical_r(n) for n in crit}
ok(
    "critical values of r at 5% for n = 11, 10, 14, 6, 19, 9 are 0.602, 0.632, 0.532, 0.811, 0.456, 0.666",
    all(round(got[n], 3) == v for n, v in crit.items()),
    ", ".join(f"{got[n]:.4f}" for n in crit),
)
vol = [[111, 96, 48], [96, 133, 61], [91, 150, 53]]
stat, df, p, e = chi2_independence(vol)
ok(
    "Example 11.6: chi-square 12.9909, df 4, p = 0.0113; expected counts 90.57 ... 56.77",
    round(stat, 4) == 12.9909
    and df == 4
    and round(p, 4) == 0.0113
    and round(e[0, 0], 2) == 90.57
    and round(e[2, 2], 2) == 56.77,
    f"{stat:.4f}, {df}, {p:.5f}",
)
speed = 305 * 70 / 755
ok(
    "Example 11.5: expected count for phone use and a violation is 28.3",
    round(speed, 1) == 28.3,
    f"{speed:.3f}",
)

print("== Part 2: formulas against SciPy, ties and transforms")
rng = np.random.default_rng(20261102)
x = rng.standard_normal(40)
y = 0.4 * x + rng.standard_normal(40)
r = float(np.corrcoef(x, y)[0, 1])
ok(
    "the t-test p-value equals scipy.stats.pearsonr to 1e-12",
    abs(corr_t_test(r, 40)[1] - stats.pearsonr(x, y).pvalue) < 1e-12,
)
xt = np.array([1, 2, 2, 3, 4, 4, 4, 5, 6, 7, 7, 8], dtype=float)
yt = np.array([2, 1, 3, 3, 5, 4, 6, 6, 5, 8, 9, 9], dtype=float)
for name, (a, b) in {"without ties": (x, y), "with ties": (xt, yt)}.items():
    sp = stats.spearmanr(a, b)
    ok(
        f"Spearman equals Pearson on midranks and scipy.stats.spearmanr, {name}, to 1e-12",
        abs(spearman(a, b) - float(sp.statistic)) < 1e-12,
        f"{spearman(a, b):.6f}",
    )
rs = spearman(xt, yt)
ok(
    "with ties the shortcut 1 - 6 sum d^2 / (n(n^2 - 1)) differs from Pearson on midranks; without ties they agree",
    abs(shortcut(xt, yt) - rs) > 1e-4 and abs(shortcut(x, y) - spearman(x, y)) < 1e-12,
    f"tied fixture: midrank Pearson {rs:.6f}, shortcut {shortcut(xt, yt):.6f}",
)
inc = [np.exp, lambda v: v**3 + v]
ok(
    "unchanged to 1e-12 by strictly increasing transforms of either variable, ties included",
    all(
        abs(spearman(f(xt), yt) - rs) < 1e-12 and abs(spearman(xt, f(yt)) - rs) < 1e-12 for f in inc
    ),
)
ok(
    "a strictly decreasing transform of one variable flips the sign; of both leaves it unchanged",
    abs(spearman(-xt, yt) + rs) < 1e-12 and abs(spearman(np.exp(-xt), -(yt**3)) - rs) < 1e-12,
)
weak = np.floor(xt / 3)
print(
    f"  (not tested) a weakly monotone transform, floor(x/3), creates ties and gives {spearman(weak, yt):.6f}"
)
ok(
    "the chi-square statistic equals scipy.stats.chi2_contingency without continuity correction to 1e-12",
    abs(stat - stats.chi2_contingency(vol, correction=False).statistic) < 1e-12,
)

print("== Part 2b: size of the 5% tests, 20,000 independent normal pairs of n = 30")
rng = np.random.default_rng(20261101)
n, reps = 30, 20_000
rej_p = rej_s = rej_z = 0
for _ in range(reps):
    a, b = rng.standard_normal(n), rng.standard_normal(n)
    r = float(np.corrcoef(a, b)[0, 1])
    rej_p += corr_t_test(r, n)[1] < 0.05
    rho = spearman(a, b)
    rej_s += corr_t_test(rho, n)[1] < 0.05
    rej_z += 2 * stats.norm.sf(abs(rho) * math.sqrt(n - 1)) < 0.05
ok(
    "Pearson t-test rejects in 5 +- 0.5% of replications",
    abs(100 * rej_p / reps - 5) <= 0.5,
    f"{100 * rej_p / reps:.2f}%",
)
ok(
    "Spearman (t approximation on midranks) rejects in 5 +- 0.5% of replications",
    abs(100 * rej_s / reps - 5) <= 0.5,
    f"{100 * rej_s / reps:.2f}%",
)
print(
    f"  (reported) Spearman with NIST's normal approximation z = rho sqrt(n - 1): {100 * rej_z / reps:.2f}%"
)

print("== Part 3 (diagnostic): overlapping horizons, a persistent signal and independent returns")
rng = np.random.default_rng(20261103)
T, h, phi, reps3 = 500, 20, 0.95, 2_000
rej_daily = rej_overlap = 0
for _ in range(reps3):
    e = rng.standard_normal(T + h)
    s = np.empty(T + h)
    s[0] = e[0] / math.sqrt(1 - phi**2)
    for i in range(1, T + h):
        s[i] = phi * s[i - 1] + e[i]
    ret = rng.standard_normal(T + h)
    fwd = np.convolve(ret, np.ones(h), mode="valid")[
        1 : T + 1
    ]  # sum of returns t+1..t+h, overlapping
    rej_daily += corr_t_test(float(np.corrcoef(s[:T], ret[1 : T + 1])[0, 1]), T)[1] < 0.05
    rej_overlap += corr_t_test(float(np.corrcoef(s[:T], fwd)[0, 1]), T)[1] < 0.05
print(
    f"  signal AR(1) phi 0.95 against independent returns, T = 500, 2,000 replications: 5% t-test rejects"
    f" {100 * rej_daily / reps3:.1f}% with one-day returns and {100 * rej_overlap / reps3:.1f}% with overlapping 20-day returns"
)

if fails:
    print("FAILED:", ", ".join(fails))
    sys.exit(1)
print("all checks passed")
