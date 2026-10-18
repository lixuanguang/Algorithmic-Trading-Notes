"""source verification (2026-10-17): checks behind mod:black-litterman.

Black and Litterman, Goldman Sachs Fixed Income Research, October 1991, Appendix, points 6-8 (PDF pp. 41-42, page
image): Pi = delta Sigma W; E[R] ~ N(Pi, tau Sigma); views P E[R] = Q + eps, eps ~ N(0, Omega), Omega diagonal;
posterior mean  Ebar = [(tau Sigma)^-1 + P' Omega^-1 P]^-1 [(tau Sigma)^-1 Pi + P' Omega^-1 Q].
Checked on a three-asset example (numbers chosen here): (1) no-view limit, Omega -> infinity, gives Pi; (2) certain
views, Omega -> 0, satisfy P Ebar = Q; (3) the formula equals the precision-weighted (Bayesian) mean computed
independently by conditioning a joint normal; (4) a view on asset 1 alone moves asset 2's expected return through
the covariance, while Sigma itself, used in the optimiser, is unchanged by the formula.
Run: uv run python black-litterman-check.py   (numpy). Exits non-zero on failure.
"""

# standard library imports
import sys

# third party library imports
import numpy as np

vol = np.array([0.15, 0.20, 0.10])
C = np.array([[1, 0.6, 0.2], [0.6, 1, 0.3], [0.2, 0.3, 1]])
Sigma = np.outer(vol, vol) * C
W = np.array([0.5, 0.3, 0.2])
delta, tau = 2.5, 0.05
Pi = delta * Sigma @ W
P = np.array([[1.0, 0, 0]])
Q = np.array([Pi[0] + 0.03])


def bl(Omega):
    A = np.linalg.inv(tau * Sigma) + P.T @ np.linalg.inv(Omega) @ P
    b = np.linalg.inv(tau * Sigma) @ Pi + P.T @ np.linalg.inv(Omega) @ Q
    return np.linalg.solve(A, b)


fails = []


def ok(name, cond, detail):
    print(f"  {'ok ' if cond else 'BAD'} {name}: {detail}")
    if not cond:
        fails.append(name)


e_none = bl(np.array([[1e12]]))
ok("no views -> equilibrium", np.allclose(e_none, Pi, atol=1e-9), np.round(e_none - Pi, 12))
e_cert = bl(np.array([[1e-12]]))
ok("certain view holds exactly", abs((P @ e_cert)[0] - Q[0]) < 1e-9, (P @ e_cert)[0] - Q[0])
Om = np.array([[0.0004]])
e = bl(Om)
# independent: E[R] ~ N(Pi, tau Sigma); observation y = P E[R] + eps = Q; conditional mean of E[R] given y
S_y = P @ (tau * Sigma) @ P.T + Om
cond = Pi + (tau * Sigma) @ P.T @ np.linalg.solve(S_y, Q - P @ Pi)
ok("equals Gaussian conditioning", np.allclose(e, cond, atol=1e-12), np.round(e - cond, 14))
ok(
    "view on asset 1 moves asset 2 (correlated)",
    e[1] - Pi[1] > 1e-4,
    f"{(e[1] - Pi[1]) * 100:+.3f} pp",
)
print(f"  equilibrium {np.round(Pi * 100, 3)} -> posterior {np.round(e * 100, 3)} (percent)")
if fails:
    sys.exit(1)
print("all checks passed")
