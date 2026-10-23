"""Library gap-filling Batch L1, package P1 (2026-10-21): the worked examples of
def:brownian-motion-quadratic-variation, res:ito-lemma-geometric-brownian-motion and
res:risk-neutral-pricing-feynman-kac.

Every check uses model-generated data with a known answer: S0 = 100, mu = 8 percent, sigma = 20 percent,
T = 1 unless stated. Seeds (20261021 and offsets) and tolerances (four standard errors, or three for the
Girsanov price) were fixed before any run and are not
tuned. The checks show that the formulas are implemented correctly under the model; they are not evidence
about markets.

Run: uv run --frozen --no-editable python stochastic-calculus-checks.py   Exits 1 on failure.
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
SEED = 20261021


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


def close(a, b, tol=1e-6):
    return abs(a - b) <= tol


S0, mu, sg, T = 100.0, 0.08, 0.20, 1.0

print("== Brownian motion and quadratic variation")
rng = np.random.default_rng(SEED)
n = 10_000
dW = rng.standard_normal(n) * math.sqrt(T / n)
W = np.concatenate(([0.0], np.cumsum(dW)))
qv = float(np.sum(dW**2))
qv_sd = math.sqrt(2 / n) * T
ok(
    "quadratic variation of W on [0, 1], 10,000 steps, within 4 s.d. (sqrt(2/n) = 0.0141) of 1",
    abs(qv - T) <= 4 * qv_sd,
    f"{qv:.5f}",
)
# Halving the step quarters the variance of the sum of squared increments: refine the same path by
# Brownian-bridge midpoints, so the coarse and fine sums use one path.
mid = 0.5 * (W[:-1] + W[1:]) + rng.standard_normal(n) * math.sqrt(T / n / 4)
fine = np.empty(2 * n + 1)
fine[0::2], fine[1::2] = W, mid
qv_fine = float(np.sum(np.diff(fine) ** 2))
ok(
    "on the refined path (20,000 steps) quadratic variation is within 4 s.d. (0.0100) of 1",
    abs(qv_fine - T) <= 4 * math.sqrt(2 / (2 * n)),
    f"{qv_fine:.5f}",
)
abs_var = float(np.sum(np.abs(dW)))
ok(
    "first variation sum |dW| grows like sqrt(2n/pi) (79.8 at n = 10,000): paths have unbounded length",
    abs(abs_var - math.sqrt(2 * n / math.pi) * T**0.5) <= 4 * math.sqrt(1 - 2 / math.pi),
    f"{abs_var:.2f}",
)
ito_int = float(np.sum(W[:-1] * dW))
ok(
    "left-point sum of W dW equals (W_T^2 - [W]_T)/2 exactly, and so is near (W_T^2 - T)/2",
    close(ito_int, 0.5 * (W[-1] ** 2 - qv), 1e-9)
    and abs(ito_int - 0.5 * (W[-1] ** 2 - T)) <= 4 * 0.5 * qv_sd,
    f"{ito_int:.5f} against {0.5 * (W[-1] ** 2 - T):.5f}",
)
ok(
    "the midpoint (Stratonovich-type) sum gives W_T^2 / 2 with no -T/2 term",
    close(float(np.sum(0.5 * (W[:-1] + W[1:]) * dW)), 0.5 * W[-1] ** 2, 1e-9),
)

print("== Ito's lemma and geometric Brownian motion")
rng = np.random.default_rng(SEED + 1)
M = 200_000
z = rng.standard_normal(M)
ST = S0 * np.exp((mu - sg**2 / 2) * T + sg * math.sqrt(T) * z)
mean_exact = S0 * math.exp(mu * T)
median_exact = S0 * math.exp((mu - sg**2 / 2) * T)
ok("exact mean S0 e^(mu T) = 108.33", close(mean_exact, 108.328707, 1e-5))
ok("exact median S0 e^((mu - sigma^2/2) T) = 106.18", close(median_exact, 106.183655, 1e-5))
m_se = ST.std(ddof=1) / math.sqrt(M)
ok(
    "200,000 exact draws: sample mean within 4 s.e. of 108.33",
    abs(ST.mean() - mean_exact) <= 4 * m_se,
    f"{ST.mean():.4f} (s.e. {m_se:.4f})",
)
dens = stats.lognorm.pdf(median_exact, sg * math.sqrt(T), scale=median_exact)
med_se = 1 / (2 * dens * math.sqrt(M))
ok(
    "sample median within 4 s.e. (1/(2 f(m) sqrt(M))) of 106.18",
    abs(np.median(ST) - median_exact) <= 4 * med_se,
    f"{np.median(ST):.4f} (s.e. {med_se:.4f})",
)
ok(
    "mean log return is mu - sigma^2/2 = 6 percent, not mu",
    abs(np.mean(np.log(ST / S0)) - 0.06) <= 4 * sg / math.sqrt(M),
)
# Ito on S^2: d(S^2) = (2 mu + sigma^2) S^2 dt + 2 sigma S^2 dW, so E[S_T^2] = S0^2 e^((2 mu + sigma^2) T).
s2_exact = S0**2 * math.exp((2 * mu + sg**2) * T)
s2 = ST**2
s2_se = s2.std(ddof=1) / math.sqrt(M)
ok("E[S_T^2] = S0^2 e^((2 mu + sigma^2) T) = 12,214.03", close(s2_exact, 12214.027582, 1e-5))
ok(
    "simulated E[S_T^2] within 4 s.e.",
    abs(s2.mean() - s2_exact) <= 4 * s2_se,
    f"{s2.mean():.2f} (s.e. {s2_se:.2f})",
)
ok(
    "the ordinary chain rule (no sigma^2 term) would give 11,735.11, rejected by the simulation",
    abs(s2.mean() - S0**2 * math.exp(2 * mu * T)) > 10 * s2_se,
)
# Euler steps of the SDE converge to the exact solution as the step shrinks. Compare 2,000 paths at 50 and
# 5,000 steps driven by the same Brownian increments.
rng = np.random.default_rng(SEED + 2)
paths, steps = 2_000, 5_000
dWf = rng.standard_normal((paths, steps)) * math.sqrt(T / steps)
exact = S0 * np.exp((mu - sg**2 / 2) * T + sg * dWf.sum(1))


def euler(dw):
    s = np.full(dw.shape[0], S0)
    h = T / dw.shape[1]
    for k in range(dw.shape[1]):
        s = s * (1 + mu * h + sg * dw[:, k])
    return s


coarse = euler(dWf.reshape(paths, 50, steps // 50).sum(2))
finer = euler(dWf)
e_c = math.sqrt(np.mean((coarse - exact) ** 2))
e_f = math.sqrt(np.mean((finer - exact) ** 2))
ok(
    "Euler scheme on the same Brownian paths: RMS error to the exact GBM falls as the step shrinks",
    e_f < e_c / 5,
    f"{e_c:.4f} at 50 steps, {e_f:.4f} at 5,000",
)

print("== Risk-neutral pricing, Girsanov and Feynman-Kac")
K, r = 105.0, 0.03
d1 = (math.log(S0 / K) + (r + sg**2 / 2) * T) / (sg * math.sqrt(T))
d2 = d1 - sg * math.sqrt(T)
bsm = S0 * stats.norm.cdf(d1) - K * math.exp(-r * T) * stats.norm.cdf(d2)
ok("BSM call (K = 105, r = 3 percent, q = 0) = 7.1281", close(bsm, 7.128065, 1e-5))
theta = (mu - r) / sg
ok("market price of risk theta = (mu - r)/sigma = 0.25", close(theta, 0.25, 1e-12))
rng = np.random.default_rng(SEED + 3)
WT = rng.standard_normal(M) * math.sqrt(T)
ST_p = S0 * np.exp((mu - sg**2 / 2) * T + sg * WT)  # real-world draws
Z = np.exp(-theta * WT - 0.5 * theta**2 * T)
ok(
    "density Z_T has mean 1 under P (within 4 s.e.)",
    abs(Z.mean() - 1) <= 4 * Z.std(ddof=1) / math.sqrt(M),
    f"{Z.mean():.5f}",
)
g = math.exp(-r * T) * Z * np.maximum(ST_p - K, 0)
g_se = g.std(ddof=1) / math.sqrt(M)
ok(
    "real-world draws reweighted by Z_T reproduce the BSM call within 3 s.e.",
    abs(g.mean() - bsm) <= 3 * g_se,
    f"{g.mean():.4f} (s.e. {g_se:.4f})",
)
ok(
    "reweighted drift: E_P[Z_T S_T] = S0 e^(r T), the risk-neutral forward",
    abs(np.mean(Z * ST_p) - S0 * math.exp(r * T)) <= 4 * (Z * ST_p).std(ddof=1) / math.sqrt(M),
)
plain = math.exp(-r * T) * np.maximum(ST_p - K, 0)
ok(
    "discounting the unweighted real-world expectation at r overstates the price",
    plain.mean() - bsm > 10 * plain.std(ddof=1) / math.sqrt(M),
    f"{plain.mean():.4f} against {bsm:.4f}",
)


# Feynman-Kac: V(S, t) = e^{-r tau} E[payoff] under dS = m S dt + sigma S dW solves
# V_t + 0.5 sigma^2 S^2 V_SS + m S V_S - r V = 0. With m = mu it is not a price; with m = r it is BSM.
def disc_exp(S, tau, m):
    a1 = (math.log(S / K) + (m + sg**2 / 2) * tau) / (sg * math.sqrt(tau))
    a2 = a1 - sg * math.sqrt(tau)
    return math.exp(-r * tau) * (
        S * math.exp(m * tau) * stats.norm.cdf(a1) - K * stats.norm.cdf(a2)
    )


def pde_residual(m, drift, S=100.0, tau=0.5, h=1e-2, k=1e-5):
    v = disc_exp(S, tau, m)
    v_s = (disc_exp(S + h, tau, m) - disc_exp(S - h, tau, m)) / (2 * h)
    v_ss = (disc_exp(S + h, tau, m) - 2 * v + disc_exp(S - h, tau, m)) / h**2
    v_t = -(disc_exp(S, tau + k, m) - disc_exp(S, tau - k, m)) / (2 * k)
    return v_t + 0.5 * sg**2 * S**2 * v_ss + drift * S * v_s - r * v


ok(
    "the discounted real-world expectation solves the PDE with mu S V_S (residual < 1e-5)",
    abs(pde_residual(mu, mu)) < 1e-5,
    f"{pde_residual(mu, mu):.2e}",
)
ok(
    "it fails the Black-Scholes PDE, whose drift term is r S V_S (residual > 1e-2)",
    abs(pde_residual(mu, r)) > 1e-2,
    f"{pde_residual(mu, r):.4f}",
)
ok(
    "the risk-neutral expectation (m = r) solves the Black-Scholes PDE and equals BSM at t = 0",
    abs(pde_residual(r, r)) < 1e-5 and close(disc_exp(S0, T, r), bsm, 1e-10),
)

if fails:
    print("FAILED:", ", ".join(fails))
    sys.exit(1)
print("all checks passed")
