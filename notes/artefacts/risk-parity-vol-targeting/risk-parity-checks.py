"""derivatives and empirical validation (2026-10-17): own checks behind the risk-parity passages.

1. Qian (PanAgora, September 2005, p. 1): with stock and bond excess-return volatilities 15.1% and 4.6% and correlation
   0.2 (Russell 1000 and Lehman Aggregate, 1983-2004), a 60/40 portfolio takes about 93% of its variance from stocks,
   and the two-asset equal-risk-contribution weights are about 23/77 (p. 2).
2. Maillard, Roncalli and Teiletche (2009, sec. 4.1): with volatilities 10/20/30/40% and a common correlation, ERC is
   48/24/16/12% (inverse volatility).
Run: uv run python risk-parity-checks.py   (numpy). Exits 1 on failure.
"""

# standard library imports
import sys

# third party library imports
import numpy as np

fails = []


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


s, b, r = 0.151, 0.046, 0.2
S = np.array([[s * s, r * s * b], [r * s * b, b * b]])
w = np.array([0.6, 0.4])
rc = w * (S @ w) / (w @ S @ w)
ok(
    "60/40: stocks carry about 93% of variance",
    round(rc[0] * 100) == 93,
    f"{rc[0] * 100:.1f}% stocks, {rc[1] * 100:.1f}% bonds",
)
we = np.array([1 / s, 1 / b]) / (1 / s + 1 / b)
rce = we * (S @ we) / (we @ S @ we)
ok(
    "two-asset ERC weights about 23/77 with equal contributions",
    round(we[0] * 100) == 23 and abs(rce[0] - 0.5) < 1e-12,
    f"{we[0] * 100:.1f}/{we[1] * 100:.1f}",
)
v = np.array([0.1, 0.2, 0.3, 0.4])
iv = (1 / v) / (1 / v).sum()
ok(
    "MRT sec. 4.1: 48/24/16/12",
    np.allclose(np.round(iv * 100), [48, 24, 16, 12]),
    ", ".join(f"{x * 100:.1f}" for x in iv),
)
if fails:
    print("\nFAILED:", fails)
    sys.exit(1)
print("\nall checks passed")
