"""Library gap-filling Batch L4, package L4-b (2026-10-21): the seasoned variance swap added to
meth:volatility-derivative-applications.

Contract: N = 252 daily
log returns r_i = ln(S_i / S_{i-1}), zero mean, annualisation A = 252, realised variance RV = 10^4 (A/N) sum r_i^2
in variance points; K_vol = 20 vol points, K_var = K_vol^2 = 400 points squared; vega notional 100,000, so
N_var = 100,000 / (2 K_vol) = 2,500 per point squared; payoff N_var (RV - K_var) at T.
After n returns, V_t = N_var P(t,T) [10^4 (A/N) sum_{i<=n} r_i^2 + ((N-n)/N) K_rem - K_var], where K_rem is the
fair variance strike of the remaining N - n returns of the same contract. A labelled derivation
from Demeterfi et al.'s definitions and additivity, not a formula printed in the sources.

Example: n = 126, realised volatility 25 over them, quoted K_rem = 324, r = 4 percent continuously compounded,
q = 1 percent, T - t = 0.5. Under risk-neutral GBM with sigma = 18 percent the exact discrete K_rem is
10^4 [sigma^2 + (r - q - sigma^2/2)^2 / A]; option-strip replication gives the continuous 324, reported
separately with its deterministic difference.

Frozen before the first run: default_rng(20261021), 200,000 paths of 126 returns in four blocks of 50,000;
deterministic checks to 1e-6 currency or relative 1e-9; the simulated value within 4 standard errors of the
value at the exact discrete K_rem. Synthetic inputs only: not evidence about markets.

Run: uv run --frozen --no-editable python seasoned-variance-swap-check.py   Exits 1 on failure. About two seconds.
"""

# standard library imports
import sys

# third party library imports
import numpy as np
import scipy
from scipy import integrate, stats

print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
fails = []


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


def rel(a, b):
    return abs(a - b) / abs(b)


A, N, n = 252, 252, 126
K_vol, vega_notional = 20.0, 100_000.0
K_var = K_vol**2
N_var = vega_notional / (2 * K_vol)
r, q, sig_rem = 0.04, 0.01, 0.18
K_rem_quoted = 324.0
PTS = 1e4  # variance points (vol points squared) per unit of decimal variance


def value(sum_sq_realised, n_obs, k_rem, tau, scale=PTS, n_var=N_var, k_var=K_var):
    """Seasoned value; sum_sq_realised is the sum of squared returns observed so far (empty sum = 0)."""
    disc = np.exp(-r * tau)
    return n_var * disc * (scale * A / N * sum_sq_realised + (N - n_obs) / N * k_rem - k_var)


# realised returns: a deterministic series with a non-zero mean, scaled to realised volatility 25 (zero mean)
raw = np.sin(1.7 * np.arange(1, n + 1)) + 0.15
c = np.sqrt(0.25**2 * n / (A * np.sum(raw**2)))
ret = c * raw
sum_sq = float(np.sum(ret**2))
rv_realised = PTS * A / n * sum_sq
tau = (N - n) / A

print("== 1. limits and the worked value")
v = value(sum_sq, n, K_rem_quoted, tau)
print(
    f"  N_var = {N_var:,.1f} per point squared; realised RV over {n} returns = {rv_realised:.6f} points^2"
)
ok(
    "worked value 2,500 e^{-0.02} (312.5 + 162 - 400) = 182,562.00",
    abs(v - 182_562.00) < 0.01,
    f"{v:,.4f}",
)
v0 = value(0.0, 0, K_var, N / A)
ok("inception (n = 0, empty realised sum, K_rem = K_var) is zero", abs(v0) <= 1e-6, f"{v0:.2e}")
full = np.sum(np.concatenate([ret, ret]) ** 2)  # the series twice: 252 returns with realised RV 625
v_T = value(full, N, 0.0, 0.0)  # the remaining term has weight zero, so its strike is irrelevant
ok(
    "expiry (n = N, P = 1) equals the payoff N_var (RV - K_var)",
    abs(v_T - N_var * (625 - K_var)) <= 1e-6,
    f"{v_T:,.4f}",
)

print("== 2. units and notionals")
v_dec = value(sum_sq, n, K_rem_quoted / PTS, tau, scale=1.0, n_var=N_var * PTS, k_var=K_var / PTS)
ok(
    "decimal variance with N_var x 10^4 gives the same value",
    rel(v_dec, v) <= 1e-9,
    f"{v_dec:,.4f}",
)
payoff = lambda s: N_var * (s**2 - K_var)
dP = (payoff(K_vol + 1e-3) - payoff(K_vol - 1e-3)) / 2e-3
ok(
    "dPayoff/dsigma_R at K_vol = 2 K_vol N_var = vega notional",
    rel(dP, vega_notional) <= 1e-9,
    f"{dP:,.4f}",
)

print("== 3. realised leg from the return series")
ok(
    "observation weights from data",
    rel(PTS * A / N * sum_sq, n / N * 625.0) <= 1e-9,
    f"{PTS * A / N * sum_sq:.6f} = (126/252) x 625",
)
dm = ret - ret.mean()
print(
    f"  contract alternatives (reported): mean-subtracted over n {PTS * A / n * np.sum(dm**2):.4f}, "
    f"over n - 1 {PTS * A / (n - 1) * np.sum(dm**2):.4f}, against zero-mean {rv_realised:.4f} points^2"
)

print("== 4. exact discrete expectation under risk-neutral GBM")
dt = 1.0 / A
mu = r - q - sig_rem**2 / 2
m_r, s_r = mu * dt, sig_rem * np.sqrt(dt)
quad, _ = integrate.quad(
    lambda x: x * x * stats.norm.pdf(x, m_r, s_r),
    m_r - 12 * s_r,
    m_r + 12 * s_r,
    epsabs=0,
    epsrel=1e-13,
)
ok(
    "E[r^2] by quadrature = sigma^2 dt + mu^2 dt^2",
    rel(quad, s_r**2 + m_r**2) <= 1e-9,
    f"{quad:.12e}",
)
K_rem_exact = PTS * (sig_rem**2 + mu**2 / A)
v_exact = value(sum_sq, n, K_rem_exact, tau)
v_cont = value(sum_sq, n, PTS * sig_rem**2, tau)
print(
    f"  K_rem exact discrete {K_rem_exact:.6f} against continuous {PTS * sig_rem**2:.6f} points^2"
)
print(
    f"  value at exact K_rem {v_exact:,.4f}; continuous approximation {v_cont:,.4f}; difference {v_exact - v_cont:,.4f} (deterministic)"
)

print("== 5. simulation of the remaining 126 returns")
rng = np.random.default_rng(20261021)
blocks, per = 4, 50_000
pv = np.empty(blocks * per)
for b in range(blocks):
    z = rng.standard_normal((per, N - n))
    rr = m_r + s_r * z
    rv_rem = PTS * A / (N - n) * np.sum(rr**2, axis=1)
    pv[b * per : (b + 1) * per] = (
        N_var * np.exp(-r * tau) * (PTS * A / N * sum_sq + (N - n) / N * rv_rem - K_var)
    )
m, se = float(pv.mean()), float(pv.std(ddof=1) / np.sqrt(pv.size))
zsc = (m - v_exact) / se
ok(
    "simulated value within 4 s.e. of the exact discrete value",
    abs(zsc) <= 4,
    f"{m:,.2f} (s.e. {se:,.2f}) vs {v_exact:,.2f}, z {zsc:+.2f}",
)
print(
    f"  (against the continuous approximation the z-score would be {(m - v_cont) / se:+.2f}; not a check)"
)

print("== 6. reported, not binding")
cal = N_var * np.exp(-r * tau) * (182 / 365 * 625.0 + 183 / 365 * K_rem_quoted - K_var)
print(f"  calendar-day weights 182/365 instead of 126/252: {cal:,.2f} (difference {cal - v:,.2f})")

print("FAILED: " + ", ".join(fails) if fails else "all checks passed")
sys.exit(1 if fails else 0)
