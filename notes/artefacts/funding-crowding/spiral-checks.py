"""source verification (2026-10-17): illustration behind mod:margin-liquidity-spiral (Brunnermeier and Pedersen, Proposition 5,
eq. (24) and p. 19). Illustrative numbers only, not a calibration.

dp1/deta1 = 1 / (k - l), k = 2 m / (gamma sigma2^2), l = -(dm/dp) x1 + x0  (selling pressure, Z1 > 0).
1. 1/(k - l) equals the series 1/k + l/k^2 + l^2/k^3 + ... for |l| < k (one term per loop of the spiral).
2. Amplification when l > 0; the combined margin-and-loss effect exceeds the sum of the separate effects
   (super-additivity of 1/(k - l) in l, convexity).
Run: uv run python spiral-checks.py   (standard library). Exits non-zero on failure.
"""

# standard library imports
import sys

fails = []


def truth(name, cond):
    print(f"  {'ok ' if cond else 'BAD'} {name}")
    if not cond:
        fails.append(name)


gamma, sigma2, m = 2.0, 0.5, 0.25  # illustrative
k = 2 * m / (gamma * sigma2**2)  # = 1.0
x1, x0, dm_dp = 1.0, 0.3, -0.2  # margin rises as price falls; prior long position against selling
l_margin, l_loss = -dm_dp * x1, x0
base = 1 / k
f = lambda l: 1 / (k - l)
series = sum((l_margin + l_loss) ** n / k ** (n + 1) for n in range(200))
truth(
    f"series = closed form ({series:.6f} vs {f(l_margin + l_loss):.6f})",
    abs(series - f(l_margin + l_loss)) < 1e-12,
)
truth(f"margin spiral amplifies: {f(l_margin):.4f} > {base:.4f}", f(l_margin) > base)
truth(f"loss spiral amplifies: {f(l_loss):.4f} > {base:.4f}", f(l_loss) > base)
extra_joint = f(l_margin + l_loss) - base
extra_sum = (f(l_margin) - base) + (f(l_loss) - base)
truth(
    f"joint extra {extra_joint:.4f} > sum of separate extras {extra_sum:.4f}",
    extra_joint > extra_sum,
)
if fails:
    print("\nFAILED:", fails)
    sys.exit(1)
print("\nall checks passed")
