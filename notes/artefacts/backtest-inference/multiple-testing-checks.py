"""source verification (2026-10-17): own Monte Carlo behind meth:multiple-testing-control.

Romano and Wolf (UPF working paper 712, October 2003, secs. 2.3-3, pp. 7-11) state that Bonferroni and Holm control
the familywise error rate (FWE) but are conservative because they ignore dependence, that a single-step max-type
method (White's Reality Check, modified) controls the FWE with power gained from the joint distribution, and that
the stepwise version (StepM) controls the FWE while rejecting at least as many hypotheses. Checked here on
K = 20 jointly normal, equicorrelated (rho = 0.8) test statistics with known covariance (so the max quantiles are
simulated exactly rather than bootstrapped), 5 false nulls with mean 3.0 and 15 true nulls with mean 0, alpha 5%.
Run: uv run --frozen --no-editable python multiple-testing-checks.py   (numpy, scipy; about 5 s). Exits non-zero on failure.
"""

# standard library imports
import sys

# third party library imports
import numpy as np
from scipy.stats import norm

rng = np.random.default_rng(31)
K, rho, alpha, R = 20, 0.8, 0.05, 4000
theta = np.r_[np.full(5, 3.0), np.zeros(15)]
C = rho * np.ones((K, K)) + (1 - rho) * np.eye(K)
Lc = np.linalg.cholesky(C)
null_draws = rng.standard_normal((200000, K)) @ Lc.T  # w - theta under the model


def cmax(idx):
    return np.quantile(null_draws[:, idx].max(axis=1), 1 - alpha)


cache = {
    n: cmax(np.arange(n)) for n in range(1, K + 1)
}  # equicorrelated: the quantile depends only on the count
res = {
    m: [0, 0] for m in ("Bonferroni", "Holm", "single-step max", "StepM")
}  # [any false rejection, true rejections]
for _ in range(R):
    w = theta + Lc @ rng.standard_normal(K)
    p = 1 - norm.cdf(w)
    dec = {}
    dec["Bonferroni"] = p < alpha / K
    order = np.argsort(p)
    h = np.zeros(K, bool)
    for j, k in enumerate(order):
        if p[k] < alpha / (K - j):
            h[k] = True
        else:
            break
    dec["Holm"] = h
    c1 = cache[K]
    dec["single-step max"] = w > c1
    rej = np.zeros(K, bool)
    while True:
        left = np.where(~rej)[0]
        if len(left) == 0:
            break
        c = cache[len(left)]
        new = left[w[left] > c]
        if len(new) == 0:
            break
        rej[new] = True
    dec["StepM"] = rej
    for m, d in dec.items():
        res[m][0] += bool(d[5:].any())
        res[m][1] += int(d[:5].sum())
fails = []
for m, (fw, tr) in res.items():
    fwe, power = fw / R, tr / R / 5
    se = np.sqrt(0.05 * 0.95 / R)
    print(f"  {m:16s}: FWE {fwe:.3f}  share of false nulls rejected {power:.3f}")
    if fwe > alpha + 3 * se:
        fails.append(f"{m} FWE above alpha")
pw = {m: res[m][1] for m in res}
if not (
    pw["StepM"] >= pw["single-step max"] >= pw["Bonferroni"] and pw["Holm"] >= pw["Bonferroni"]
):
    fails.append("power ordering")
if not pw["single-step max"] > pw["Holm"]:
    fails.append("dependence-aware method not more powerful than Holm at rho 0.8")
for f in fails:
    print("BAD", f)
if fails:
    sys.exit(1)
print("all checks passed")
