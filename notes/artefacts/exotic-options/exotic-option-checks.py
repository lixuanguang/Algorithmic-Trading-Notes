"""Library gap-filling Batch L1, package P3 (2026-10-21): the worked examples of meth:digital-option-valuation,
meth:barrier-option-valuation and meth:asian-option-valuation.

Inputs and acceptance (implementation_plan_v2.md Section 6, P3, as corrected before any run): GBM with
S0 = 100, K = 100, r = 5 percent, q = 2 percent, sigma = 25 percent, T = 1. Every Monte Carlo check uses
100,000 paths sampled exactly on its dates, seeds 20261031, 20261032, ... in the order of the checks below.
Synthetic model data only: the checks test the formulas and the simulation under the model, not markets.

Correction, 2026-10-21 (L1 audit findings L1-F3 and L1-F5): two deterministic checks were added, with no change to
the seeds or the order of the Monte Carlo checks. (1) The cash digital's one-day delta is positive on both sides
of the strike; what changes near expiry is its size, not its sign. (2) "Both averages below the vanilla" holds for
the common inputs but is not a general ordering: with negative carry (q = 8 percent > r = 2 percent, K = 60) the
average's forward exceeds the terminal forward and the Asian call is worth more than the vanilla. The AM-GM
ordering of arithmetic over geometric average holds throughout.

Run: uv run python exotic-option-checks.py   Exits 1 on failure.
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
N = stats.norm.cdf
SEEDS = iter(range(20261031, 20261040))
M = 100_000


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


S0, K, r, q, sg, T = 100.0, 100.0, 0.05, 0.02, 0.25, 1.0


def d12(S, k, tau, vol=sg):
    d1 = (math.log(S / k) + (r - q + vol**2 / 2) * tau) / (vol * math.sqrt(tau))
    return d1, d1 - vol * math.sqrt(tau)


def call(S, k, tau, vol=sg):
    d1, d2 = d12(S, k, tau, vol)
    return S * math.exp(-q * tau) * N(d1) - k * math.exp(-r * tau) * N(d2)


def cash_digital(S, k, tau):
    return math.exp(-r * tau) * N(d12(S, k, tau)[1])


def asset_digital(S, k, tau):
    return S * math.exp(-q * tau) * N(d12(S, k, tau)[0])


def mc(x):
    return x.mean(), x.std(ddof=1) / math.sqrt(len(x))


print("== digital options")
c = call(S0, K, T)
ok(
    "asset digital minus K times the unit cash digital equals the call to 1e-12",
    abs(asset_digital(S0, K, T) - K * cash_digital(S0, K, T) - c) < 1e-12,
    f"call {c:.6f}, cash digital {cash_digital(S0, K, T):.6f}, asset digital {asset_digital(S0, K, T):.4f}",
)
ok(
    "cash call plus cash put digital equals the discount factor e^(-rT)",
    abs(cash_digital(S0, K, T) + math.exp(-r * T) * N(-d12(S0, K, T)[1]) - math.exp(-r * T))
    < 1e-14,
)
err = []
for eps in (2.0, 1.0, 0.5):
    spread = (call(S0, K - eps, T) - call(S0, K + eps, T)) / (2 * eps)
    err.append(spread - cash_digital(S0, K, T))
ok(
    "centred call spread of half-width 2, 1, 0.5: successive error ratios in [3.5, 4.5]",
    3.5 <= err[0] / err[1] <= 4.5 and 3.5 <= err[1] / err[2] <= 4.5,
    f"errors {err[0]:.2e}, {err[1]:.2e}, {err[2]:.2e}",
)
rng = np.random.default_rng(next(SEEDS))
ST = S0 * np.exp((r - q - sg**2 / 2) * T + sg * math.sqrt(T) * rng.standard_normal(M))
est, se = mc(math.exp(-r * T) * (ST > K))
ok(
    "simulated cash digital within 3 s.e. of e^(-rT) N(d2)",
    abs(est - cash_digital(S0, K, T)) <= 3 * se,
    f"{est:.4f} (s.e. {se:.4f})",
)


def cash_digital_delta(S, tau):
    return math.exp(-r * tau) * stats.norm.pdf(d12(S, K, tau)[1]) / (S * sg * math.sqrt(tau))


deltas = [cash_digital_delta(K, tau) for tau in (1.0, 1 / 12, 1 / 252)]
ok(
    "pin risk: at the strike the cash digital's delta grows like 1/sqrt(tau) (1 year, 1 month, 1 day)",
    deltas[0] < deltas[1] < deltas[2] and abs(deltas[2] / deltas[1] - math.sqrt(21)) < 0.1,
    ", ".join(f"{d:.4f}" for d in deltas),
)

one_day = [cash_digital_delta(S, 1 / 252) for S in (99.9, 100.0, 100.1)]
ok(
    "one day before expiry the delta is positive on both sides of the strike: the hedge changes size, not sign",
    min(one_day) > 0,
    "S = 99.9, 100, 100.1: " + ", ".join(f"{d:.4f}" for d in one_day),
)

print("== barrier options (down-and-out and down-and-in calls, H = 90)")
H = 90.0


def down_in_call(S, k, h, tau, vol=sg):
    """Hull sec. 26.9, H <= K, continuous monitoring."""
    lm = (r - q + vol**2 / 2) / vol**2
    y = math.log(h**2 / (S * k)) / (vol * math.sqrt(tau)) + lm * vol * math.sqrt(tau)
    return S * math.exp(-q * tau) * (h / S) ** (2 * lm) * N(y) - k * math.exp(-r * tau) * (
        h / S
    ) ** (2 * lm - 2) * N(y - vol * math.sqrt(tau))


def down_out_call(S, k, h, tau, vol=sg):
    return call(S, k, tau, vol) - down_in_call(S, k, h, tau, vol)


cdo, cdi = down_out_call(S0, K, H, T), down_in_call(S0, K, H, T)
ok("closed forms: c_do + c_di = c", abs(cdo + cdi - c) < 1e-12, f"c_do {cdo:.4f}, c_di {cdi:.4f}")
m = 252
dt = T / m
rng = np.random.default_rng(next(SEEDS))
logS = np.log(S0) + np.cumsum(
    (r - q - sg**2 / 2) * dt + sg * math.sqrt(dt) * rng.standard_normal((M, m)), axis=1
)
paths = np.exp(logS)
hit = (paths <= H).any(axis=1)
vanilla = math.exp(-r * T) * np.maximum(paths[:, -1] - K, 0)
knock_out = np.where(hit, 0.0, vanilla)
knock_in = np.where(hit, vanilla, 0.0)
ok(
    "in-out parity path by path on common paths (daily monitoring), to 1e-12",
    np.max(np.abs(knock_out + knock_in - vanilla)) < 1e-12,
)
# Continuous monitoring: weight each path by the Brownian-bridge probability of not crossing H between dates.
rng = np.random.default_rng(next(SEEDS))
logS = np.log(S0) + np.cumsum(
    (r - q - sg**2 / 2) * dt + sg * math.sqrt(dt) * rng.standard_normal((M, m)), axis=1
)
x = np.concatenate([np.full((M, 1), math.log(S0 / H)), logS - math.log(H)], axis=1)
survive_step = np.where(
    (x[:, :-1] > 0) & (x[:, 1:] > 0), 1 - np.exp(-2 * x[:, :-1] * x[:, 1:] / (sg**2 * dt)), 0.0
)
bb = math.exp(-r * T) * np.maximum(np.exp(logS[:, -1]) - K, 0) * survive_step.prod(axis=1)
est, se = mc(bb)
ok(
    "continuous down-and-out call: Brownian-bridge Monte Carlo within 3 s.e. of the closed form",
    abs(est - cdo) <= 3 * se,
    f"{est:.4f} (s.e. {se:.4f}) against {cdo:.4f}",
)
rng = np.random.default_rng(next(SEEDS))
logS = np.log(S0) + np.cumsum(
    (r - q - sg**2 / 2) * dt + sg * math.sqrt(dt) * rng.standard_normal((M, m)), axis=1
)
disc_do = (
    math.exp(-r * T) * np.maximum(np.exp(logS[:, -1]) - K, 0) * ~(logS <= math.log(H)).any(axis=1)
)
est_d, se_d = mc(disc_do)
H_shift = H * math.exp(-0.5826 * sg * math.sqrt(T / m))
bgk = down_out_call(S0, K, H_shift, T)
ok(
    "daily monitoring: Monte Carlo within 3 s.e. + 0.5 percent of the shifted-barrier closed form",
    abs(est_d - bgk) <= 3 * se_d + 0.005 * bgk,
    f"{est_d:.4f} (s.e. {se_d:.4f}) against {bgk:.4f} (barrier {H_shift:.3f}); continuous {cdo:.4f}",
)
ok("discrete monitoring knocks out less often, so it is worth more than continuous", est_d > cdo)


def vega(f, *args, h=1e-4):
    return (f(*args, vol=sg + h) - f(*args, vol=sg - h)) / (2 * h)


def up_out_call(S, k, h, tau, vol=sg):
    """Hull sec. 26.9, H > K: c_uo = c - c_ui."""
    lm = (r - q + vol**2 / 2) / vol**2
    sq = vol * math.sqrt(tau)
    y = math.log(h**2 / (S * k)) / sq + lm * sq
    x1 = math.log(S / h) / sq + lm * sq
    y1 = math.log(h / S) / sq + lm * sq
    c_ui = (
        S * N(x1) * math.exp(-q * tau)
        - k * math.exp(-r * tau) * N(x1 - sq)
        - S * math.exp(-q * tau) * (h / S) ** (2 * lm) * (N(-y) - N(-y1))
        + k * math.exp(-r * tau) * (h / S) ** (2 * lm - 2) * (N(-y + sq) - N(-y1 + sq))
    )
    return call(S, k, tau, vol) - c_ui


v_far, v_near = vega(down_out_call, 130.0, K, H, T), vega(down_out_call, 91.0, K, H, T)
ok(
    "down-and-out call (H = 90 < K): vega shrinks towards zero near the barrier (below a tenth of its value at 130)",
    0 < v_near < 0.1 * v_far,
    f"S = 130: {v_far:.2f}; S = 91: {v_near:.2f}",
)
v_uo = vega(up_out_call, 115.0, K, 120.0, T)
ok(
    "up-and-out call (K = 100, H = 120) near the barrier (S = 115): negative vega",
    v_uo < 0,
    f"{v_uo:.2f}; value {up_out_call(115.0, K, 120.0, T):.4f}",
)

print("== Asian options (12 monthly averaging dates, S0 excluded)")
n = 12
mu_g = math.log(S0) + (r - q - sg**2 / 2) * T * (n + 1) / (2 * n)
var_g = sg**2 * T * (n + 1) * (2 * n + 1) / (6 * n**2)


def geo_asian_call(mu, var):
    d2 = (mu - math.log(K)) / math.sqrt(var)
    d1 = d2 + math.sqrt(var)
    return math.exp(-r * T) * (math.exp(mu + var / 2) * N(d1) - K * N(d2))


geo_cf = geo_asian_call(mu_g, var_g)
rng = np.random.default_rng(next(SEEDS))
dta = T / n
logS = np.log(S0) + np.cumsum(
    (r - q - sg**2 / 2) * dta + sg * math.sqrt(dta) * rng.standard_normal((M, n)), axis=1
)
geo_pay = math.exp(-r * T) * np.maximum(np.exp(logS.mean(axis=1)) - K, 0)
ari_pay = math.exp(-r * T) * np.maximum(np.exp(logS).mean(axis=1) - K, 0)
est, se = mc(geo_pay)
ok(
    "geometric average call: discrete closed form against Monte Carlo within 3 s.e.",
    abs(est - geo_cf) <= 3 * se,
    f"{est:.4f} (s.e. {se:.4f}) against {geo_cf:.4f}",
)
b = np.cov(ari_pay, geo_pay)[0, 1] / geo_pay.var(ddof=1)
ctrl = ari_pay - b * (geo_pay - geo_cf)
a_est, a_se = mc(ari_pay)
c_est, c_se = mc(ctrl)
vr = ari_pay.var(ddof=1) / ctrl.var(ddof=1)
ok(
    "arithmetic average call: variance-reduction factor of the geometric control above 10",
    vr > 10,
    f"{vr:.0f}",
)
ok(
    "controlled and uncontrolled estimates differ by less than 3 uncontrolled s.e.",
    abs(c_est - a_est) < 3 * a_se,
    f"{a_est:.4f} (s.e. {a_se:.4f}) and {c_est:.4f} (s.e. {c_se:.5f}), b = {b:.4f}",
)
ok(
    "arithmetic >= geometric (AM-GM); with these inputs (positive carry) both lie below the vanilla call",
    geo_cf < c_est < c,
    f"vanilla {c:.4f}",
)
# Continuous averaging as the limit n -> infinity: volatility sigma/sqrt(3), Wilmott's explicit formula.
mu_c = math.log(S0) + (r - q - sg**2 / 2) * T / 2
var_c = sg**2 * T / 3
cont = geo_asian_call(mu_c, var_c)


def geo_discrete(nn):
    return geo_asian_call(
        math.log(S0) + (r - q - sg**2 / 2) * T * (nn + 1) / (2 * nn),
        sg**2 * T * (nn + 1) * (2 * nn + 1) / (6 * nn**2),
    )


# The discrete mean and variance differ from their limits by O(1/n), so the price converges at first order:
# doubling the number of dates from 500 to 1,000 halves the gap (ratio in [1.9, 2.1]).
gaps = [geo_discrete(nn) - cont for nn in (12, 500, 1000)]
ok(
    "discrete formula tends to the continuous one at first order in 1/n",
    1.9 <= gaps[1] / gaps[2] <= 2.1,
    f"gap {gaps[0]:.4f} at 12 dates, {gaps[1]:.5f} at 500, {gaps[2]:.5f} at 1,000",
)
q_kv = 0.5 * (r + q + sg**2 / 6)
d1kv = (math.log(S0 / K) + (r - q_kv + sg**2 / 6) * T) / (sg / math.sqrt(3) * math.sqrt(T))
kv = S0 * math.exp(-q_kv * T) * N(d1kv) - K * math.exp(-r * T) * N(
    d1kv - sg / math.sqrt(3) * math.sqrt(T)
)
ok(
    "continuous form equals Black-Scholes with sigma/sqrt(3) and yield (r + q + sigma^2/6)/2",
    abs(kv - cont) < 1e-12,
    f"{cont:.4f}",
)
q_w = q + sg**2 / 6
d1w = (math.log(S0 / K) + (r - q_w + sg**2 / 6) * T) / (sg / math.sqrt(3) * math.sqrt(T))
wil = S0 * math.exp(-q_w * T) * N(d1w) - K * math.exp(-r * T) * N(
    d1w - sg / math.sqrt(3) * math.sqrt(T)
)
ok(
    "a yield of q + sigma^2/6 alone (as printed in Wilmott's sec. 25.9.1 summary) does not reproduce it",
    abs(wil - cont) > 0.1,
    f"{wil:.4f}",
)

print("== Asian against vanilla: the ordering depends on carry (deterministic counterexample)")
# Averaging lowers dispersion but also moves the forward level: E[A] = S0 mean_i e^((r - q) t_i). With q > r the
# average's forward is above the terminal forward, and for a deep in-the-money call that effect dominates.
# Same 12 monthly dates, S0 excluded. E[(A - K)+] >= E[A] - K bounds the arithmetic call below, model-free given E[A].
S0n, Kn, rn, qn, sgn, Tn = 100.0, 60.0, 0.02, 0.08, 0.20, 1.0
d1n = (math.log(S0n / Kn) + (rn - qn + sgn**2 / 2) * Tn) / (sgn * math.sqrt(Tn))
vanilla_n = S0n * math.exp(-qn * Tn) * N(d1n) - Kn * math.exp(-rn * Tn) * N(
    d1n - sgn * math.sqrt(Tn)
)
m_n = math.log(S0n) + (rn - qn - sgn**2 / 2) * Tn * (n + 1) / (2 * n)
v_n = sgn**2 * Tn * (n + 1) * (2 * n + 1) / (6 * n**2)
d2n = (m_n - math.log(Kn)) / math.sqrt(v_n)
geo_n = math.exp(-rn * Tn) * (math.exp(m_n + v_n / 2) * N(d2n + math.sqrt(v_n)) - Kn * N(d2n))
EA = S0n * sum(math.exp((rn - qn) * i * Tn / n) for i in range(1, n + 1)) / n
ari_lb = math.exp(-rn * Tn) * (EA - Kn)
ok(
    "S0 = 100, K = 60, r = 2, q = 8 percent: geometric Asian call and the arithmetic lower bound both exceed"
    " the vanilla call",
    vanilla_n < geo_n < ari_lb
    and abs(vanilla_n - 33.56113) < 5e-5
    and abs(geo_n - 35.76006) < 5e-5
    and abs(ari_lb - 36.08765) < 5e-5,
    f"vanilla {vanilla_n:.4f}, geometric {geo_n:.4f}, arithmetic >= {ari_lb:.4f}",
)

if fails:
    print("FAILED:", ", ".join(fails))
    sys.exit(1)
print("all checks passed")
