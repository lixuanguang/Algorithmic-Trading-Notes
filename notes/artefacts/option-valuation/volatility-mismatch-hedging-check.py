"""Library gap-filling Batch L1, package P4 (2026-10-21): the worked example of
res:delta-hedging-volatility-mismatch, and the vanna and volga formulas added to meth:greeks-delta-gamma-hedging.

Model: dS = mu S dt + sigma S dW with mu = 10 percent and actual
volatility sigma = 30 percent; a European call (S0 = K = 100, T = 1, r = 5 percent, q = 0) bought at the BSM
price with implied volatility 20 percent and marked at that volatility; short delta shares; cash at r; no
costs. 20,000 paths, rebalanced 252 or 2,520 times on common Brownian paths (the coarse grid uses every tenth
fine date). Profit is measured as present value at time 0. Acceptance ranges were fixed before any
run; seed 20261051. Synthetic data only: not evidence about markets.

Correction, 2026-10-21 (L1 audit finding L1-F2): the entry had dropped the condition Gamma >= 0 from the claim
that sigma > implied volatility makes the implied-volatility hedge profitable. A final deterministic section
now shows the condition matters: a unit cash-or-nothing call (S0 = 120, K = 100, r = 5 percent, q = 0, T = 1)
is worth less at 30 than at 20 percent volatility, and its gamma changes sign (where d1 = 0, S about 93). The vanilla
simulation above is unchanged.

Run: uv run --frozen --no-editable python volatility-mismatch-hedging-check.py   Exits 1 on failure. About 10 seconds.
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


S0, K, T, r, q, mu, sig_a, sig_i = 100.0, 100.0, 1.0, 0.05, 0.0, 0.10, 0.30, 0.20


def d12(S, tau, vol):
    d1 = (np.log(S / K) + (r - q + vol**2 / 2) * tau) / (vol * np.sqrt(tau))
    return d1, d1 - vol * np.sqrt(tau)


def price(S, tau, vol):
    d1, d2 = d12(S, tau, vol)
    return S * np.exp(-q * tau) * stats.norm.cdf(d1) - K * np.exp(-r * tau) * stats.norm.cdf(d2)


def delta(S, tau, vol):
    return np.exp(-q * tau) * stats.norm.cdf(d12(S, tau, vol)[0])


def gamma(S, tau, vol):
    return np.exp(-q * tau) * stats.norm.pdf(d12(S, tau, vol)[0]) / (S * vol * np.sqrt(tau))


Va, Vi = float(price(S0, T, sig_a)), float(price(S0, T, sig_i))
ok("V^a - V^i = 3.7807", abs(Va - Vi - 3.7807) < 5e-5, f"{Va:.4f} - {Vi:.4f} = {Va - Vi:.4f}")

print("== simulation on common paths")
n_paths, n_fine, coarse_every = 20_000, 2520, 10
dt = T / n_fine
rng = np.random.default_rng(20261051)
S = np.full(n_paths, S0)
state = {}
for name, every in (("fine", 1), ("coarse", coarse_every)):
    for hedge_vol in ("a", "i"):
        vol = sig_a if hedge_vol == "a" else sig_i
        d = delta(S, T, vol)
        state[(name, hedge_vol)] = {"every": every, "vol": vol, "delta": d, "cash": -Vi + d * S}
    state[(name, "integral")] = np.zeros(n_paths)
for k in range(n_fine):
    t = k * dt
    for name, every in (("fine", 1), ("coarse", coarse_every)):
        if (
            k % every == 0
        ):  # left-point Riemann sum of the pathwise integral for the implied-delta hedge
            h = every * dt
            state[(name, "integral")] += (
                0.5 * (sig_a**2 - sig_i**2) * math.exp(-r * t) * S**2 * gamma(S, T - t, sig_i) * h
            )
    S = S * np.exp((mu - sig_a**2 / 2) * dt + sig_a * math.sqrt(dt) * rng.standard_normal(n_paths))
    t_new = (k + 1) * dt
    for key, st in state.items():
        if key[1] == "integral":
            continue
        st["cash"] = st["cash"] * math.exp(r * dt)
        if (k + 1) % st["every"] == 0 and k + 1 < n_fine:
            new_delta = delta(S, T - t_new, st["vol"])
            st["cash"] += (new_delta - st["delta"]) * S
            st["delta"] = new_delta
payoff = np.maximum(S - K, 0)
pnl = {}
for (name, hedge_vol), st in state.items():
    if hedge_vol == "integral":
        continue
    pnl[(name, hedge_vol)] = math.exp(-r * T) * (payoff - st["delta"] * S + st["cash"])

print("== hedging with actual volatility locks in V^a - V^i")
for name, n in (("coarse", 252), ("fine", 2520)):
    x = pnl[(name, "a")]
    m, se = x.mean(), x.std(ddof=1) / math.sqrt(n_paths)
    ok(
        f"{n} steps: mean P&L within 3 s.e. of 3.7807",
        abs(m - (Va - Vi)) <= 3 * se,
        f"{m:.4f} (s.e. {se:.4f}, s.d. {x.std(ddof=1):.3f})",
    )
ratio = pnl[("coarse", "a")].std(ddof=1) / pnl[("fine", "a")].std(ddof=1)
ok(
    "s.d. ratio 252 against 2,520 steps in [2.8, 3.5] (sqrt(10) = 3.16)",
    2.8 <= ratio <= 3.5,
    f"{ratio:.2f}",
)

print("== hedging with implied volatility: path-dependent total")
gap = {}
for name in ("coarse", "fine"):
    gap[name] = math.sqrt(np.mean((pnl[(name, "i")] - state[(name, "integral")]) ** 2))
shrink = gap["coarse"] / gap["fine"]
ok(
    "RMS gap between each path's P&L and its pathwise integral shrinks by a factor in [2.5, 3.8]",
    2.5 <= shrink <= 3.8,
    f"{gap['coarse']:.3f} to {gap['fine']:.3f}, factor {shrink:.2f}",
)
sd_i = pnl[("fine", "i")].std(ddof=1)
ok(
    "cross-path s.d. at 2,520 steps stays above 1.5: the total remains random",
    sd_i > 1.5,
    f"{sd_i:.2f}",
)
ok(
    "with sigma > implied and gamma >= 0 the pathwise integral is positive on every path",
    (state[("fine", "integral")] > 0).all(),
)
mi = pnl[("fine", "i")]
print(
    f"  mean P&L of the implied-delta hedge {mi.mean():.4f} (s.e. {mi.std(ddof=1) / math.sqrt(n_paths):.4f});"
    " reported, not tested against V^a - V^i"
)

print("== vanna and volga (meth:greeks-delta-gamma-hedging)")
d1, d2 = d12(S0, T, sig_i)
vega = S0 * math.exp(-q * T) * stats.norm.pdf(d1) * math.sqrt(T)
vanna = -math.exp(-q * T) * stats.norm.pdf(d1) * d2 / sig_i
volga = vega * d1 * d2 / sig_i
h = 1e-4
fd_vanna = (delta(S0, T, sig_i + h) - delta(S0, T, sig_i - h)) / (2 * h)
fd_volga = (price(S0, T, sig_i + h) - 2 * price(S0, T, sig_i) + price(S0, T, sig_i - h)) / h**2
ok(
    "vanna -e^(-qT) n(d1) d2 / sigma and volga vega d1 d2 / sigma match finite differences",
    abs(fd_vanna - vanna) < 1e-6 and abs(fd_volga - volga) < 1e-3,
    f"vanna {vanna:.4f}, volga {volga:.4f}",
)

print("== the gamma condition: a cash-or-nothing call (deterministic counterexample)")
# Unit cash digital, value e^(-r tau) N(d2), gamma -e^(-r tau) n(d2) d1 / (S^2 vol^2 tau). With actual volatility
# above implied, V^a - V^i < 0 here, and Gamma^i < 0 wherever d1 > 0 (S above about 93), so neither hedge's
# profit is positive merely because sigma > implied. Values computed in closed form; no simulation.
Sd, Kd, Td = 120.0, 100.0, 1.0


def digital_d12(S, vol, k=Kd, tau=Td):
    d1 = (math.log(S / k) + (r + vol**2 / 2) * tau) / (vol * math.sqrt(tau))
    return d1, d1 - vol * math.sqrt(tau)


def digital(S, vol):
    return math.exp(-r * Td) * stats.norm.cdf(digital_d12(S, vol)[1])


def digital_gamma(S, vol):
    d1, d2 = digital_d12(S, vol)
    return -math.exp(-r * Td) * stats.norm.pdf(d2) * d1 / (S**2 * vol**2 * Td)


dig_a, dig_i = digital(Sd, sig_a), digital(Sd, sig_i)
ok(
    "S0 = 120, K = 100: the cash digital is worth less at actual 30 percent than at implied 20 percent",
    dig_a - dig_i < 0 and abs(dig_i - 0.8140556) < 5e-7 and abs(dig_a - 0.6980305) < 5e-7,
    f"V^a - V^i = {dig_a:.4f} - {dig_i:.4f} = {dig_a - dig_i:+.4f}",
)
h = 1e-3
fd_gamma = (digital(Sd + h, sig_i) - 2 * dig_i + digital(Sd - h, sig_i)) / h**2
g_low, g_high = digital_gamma(80.0, sig_i), digital_gamma(Sd, sig_i)
ok(
    "its implied-volatility gamma is positive at S = 80 and negative at S = 120 (closed form matches a"
    " finite difference)",
    g_low > 0 > g_high and abs(fd_gamma - g_high) < 1e-7,
    f"{g_low:+.6f} and {g_high:+.6f}",
)

if fails:
    print("FAILED:", ", ".join(fails))
    sys.exit(1)
print("all checks passed")
