"""source verification (2026-10-17) (audit repair): best linear projection against conditional expectation, behind
meth:forecast-scaling-ic.

1. Zero linear IC with full predictive information: g ~ N(0, 1), r = g^2 - 1 + e with e ~ N(0, s^2) independent.
   Cov(r, g) = E[g^3] = 0, so the IC and the linear refined forecast are zero, yet E[r | g] = g^2 - 1 explains a
   fraction 2 / (2 + s^2) of Var(r). Checked in closed form and by simulation.
2. The linear projection's error is uncorrelated with g (orthogonality) but not mean-independent of g: in the same
   example E[error | g] = g^2 - 1, so a nonlinear function of g still predicts the error.
3. Under joint normality the projection and the conditional mean coincide: binned conditional means of r given g
   lie on the projection line (within simulation error).
Run: uv run --frozen --no-editable python projection-checks.py   (numpy; under 1 s). Exits non-zero on failure.
"""

# standard library imports
import itertools
import sys

# third party library imports
import numpy as np

rng = np.random.default_rng(17102026)
fails = []


def check(name, ok, detail):
    print(f"  {'ok ' if ok else 'BAD'} {name}: {detail}")
    if not ok:
        fails.append(name)


n, s = 2_000_000, 1.0
g = rng.standard_normal(n)
r = g**2 - 1 + s * rng.standard_normal(n)
ic = np.corrcoef(r, g)[0, 1]
r2_true = 2 / (2 + s**2)
fitted = g**2 - 1
r2_sim = 1 - np.var(r - fitted) / np.var(r)
print("== 1. Zero IC, nonzero information")
check("IC is zero within simulation error", abs(ic) < 4 / np.sqrt(n), f"IC {ic:+.5f}")
check(
    "conditional mean explains 2/(2+s^2) of the variance",
    abs(r2_sim - r2_true) < 0.005,
    f"{r2_sim:.4f} against {r2_true:.4f}",
)
b = np.cov(r, g)[0, 1] / np.var(g)
print(f"     linear projection slope {b:+.5f}; linear R^2 {ic**2:.6f}")

print("\n== 2. Orthogonality is not mean independence")
u = r - (r.mean() + b * (g - g.mean()))
check(
    "projection error uncorrelated with g",
    abs(np.corrcoef(u, g)[0, 1]) < 4 / np.sqrt(n),
    f"{np.corrcoef(u, g)[0, 1]:+.5f}",
)
check(
    "projection error correlated with g^2",
    np.corrcoef(u, g**2)[0, 1] > 0.5,
    f"{np.corrcoef(u, g**2)[0, 1]:+.4f}",
)

print("\n== 3. Joint normality: projection = conditional mean")
cov = np.array([[1.0, 0.3], [0.3, 1.0]])
x = rng.multivariate_normal([0, 0], cov, size=n)
gg, rr = x[:, 0], x[:, 1]
edges = np.linspace(-2, 2, 9)
worst = 0.0
for lo, hi in itertools.pairwise(edges):
    m = (gg >= lo) & (gg < hi)
    worst = max(worst, abs(rr[m].mean() - 0.3 * gg[m].mean()))
check("binned conditional means on the line 0.3 g", worst < 0.01, f"largest gap {worst:.4f}")

if fails:
    print("\nFAILED:", fails)
    sys.exit(1)
print("\nall checks passed")
