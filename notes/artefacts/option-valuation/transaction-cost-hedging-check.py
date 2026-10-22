"""Library gap-filling Batch L5, package L5-b (2026-10-21): the worked examples of meth:transaction-cost-hedging.

Inputs, conventions and acceptance were frozen before the first run. Wilmott, PWOQF 2nd ed., chap. 48: trading nu shares at S costs
kappa |nu| S; rebalancing every dt = T/N; Leland's volatilities (48.5)-(48.6), sigma_hat^2, sigma_check^2 = sigma^2
+/- 2 kappa sigma sqrt(2/(pi dt)); K = kappa/(sigma sqrt(dt)) (48.7).

Conventions: position sign s = +1 long, -1 short one call; stock holding h_k = -s Delta_k with the BSM delta at the
position's Leland volatility (sigma_check long, sigma_hat short); trades nu_k = h_k - h_{k-1} at S(t_k); cash grows at r
and pays trades and costs; physical settlement, so at T the holding moves to the payoff delta -s 1{S_T > K} (the N-th,
costed trade). The opening trade and the cash-settled close are reported separately. Risk-neutral simulation (mu = r),
q = 0, so the discounted stock is a martingale.

Comparable quantity (Interpretation): BSM(sigma_hat) - BSM(sigma) = E^Q int e^{-rt} kappa sigma
sqrt(2/(pi dt)) S^2 Gamma_hat dt exactly, the expected present value of Wilmott's leading-order cost (48.2) under the
sigma_hat delta. The simulated estimand C_N is the expected present value of the actual costs of trades 1..N under the
same rule; e_N = C_N - L is the approximation residual, and E[e^{-rT} W_T] = -e_N for the writer at the Leland price.

Part 1 deterministic; part 2 simulation, default_rng(20261023), 100,000 paths of 208 log-exact steps drawn in ten
blocks of 10,000, nested grids N = 13, 52, 208, Leland numbers K = 0.1 and 0.4; part 3 the call-spread hedge-cost
demonstration on the same paths (N = 52, kappa = 0.2 percent, BSM deltas at sigma). Synthetic model data only.

Run: uv run python transaction-cost-hedging-check.py   Exits 1 on failure. About 20 seconds.
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


S0, KS, sig, r, T = 100.0, 100.0, 0.2, 0.05, 1.0  # Wilmott sec. 48.12 setting; q = 0


def bs_call(S, K, tau, vol):
    d1 = (math.log(S / K) + (r + vol**2 / 2) * tau) / (vol * math.sqrt(tau))
    return S * stats.norm.cdf(d1) - K * math.exp(-r * tau) * stats.norm.cdf(
        d1 - vol * math.sqrt(tau)
    )


def bs_delta(S, K, tau, vol):
    return stats.norm.cdf((np.log(S / K) + (r + vol**2 / 2) * tau) / (vol * np.sqrt(tau)))


def leland_var(kappa, dt, sign):
    """sigma_hat^2 (sign = +1, short) or sigma_check^2 (sign = -1, long), eqs. (48.5)-(48.6)."""
    return sig**2 + sign * 2 * kappa * sig * math.sqrt(2 / (math.pi * dt))


# ---------------------------------------------------------------- part 1
print("== part 1: Leland volatilities, limits, domain, Wilmott's spread approximation")
worst = 0.0
for kappa in (0.0005, 0.002, 0.01):
    for dt in (1 / 252, 1 / 52, 1 / 13):
        for sign in (+1, -1):
            if leland_var(kappa, dt, sign) <= 0:
                continue
            printed = sig * (1 + sign * math.sqrt(8 / (math.pi * dt)) * kappa / sig) ** 0.5
            worst = max(worst, abs(math.sqrt(leland_var(kappa, dt, sign)) / printed - 1))
ok(
    "(48.5)-(48.6) equal the printed sigma (1 -/+ sqrt(8/(pi dt)) kappa/sigma)^(1/2)",
    worst <= 1e-14,
    f"{worst:.1e}",
)
dt52 = 1 / 52
signs_ok = all(
    math.sqrt(leland_var(k, dt52, -1)) < sig < math.sqrt(leland_var(k, dt52, +1))
    for k in (1e-5, 0.002, 0.01)
)
ok(
    "signs: sigma_check < sigma < sigma_hat for kappa > 0 (long valued lower, short higher)",
    signs_ok,
)
ok(
    "zero-cost limit: kappa = 0 gives sigma_check = sigma_hat = sigma and a zero premium adjustment",
    leland_var(0.0, dt52, 1) == leland_var(0.0, dt52, -1) == sig**2
    and bs_call(S0, KS, T, math.sqrt(leland_var(0.0, dt52, 1))) - bs_call(S0, KS, T, sig) == 0.0,
)
Kstar = math.sqrt(math.pi / 8)
kap_star = Kstar * sig * math.sqrt(dt52)
ok(
    "domain of the long formula: sigma_check^2 = 0 at K* = sqrt(pi/8), negative above",
    abs(leland_var(kap_star, dt52, -1)) <= 1e-15 * sig**2
    and leland_var(1.01 * kap_star, dt52, -1) < 0,
    f"K* = {Kstar:.4f}; at dt = 1/52 kappa* = sigma sqrt(pi dt/8) = {kap_star:.5f}; the bound printed on p. 789,"
    f" sigma/sqrt(8 pi dt), would be {sig / math.sqrt(8 * math.pi * dt52):.4f}",
)
d1 = (math.log(S0 / KS) + (r + sig**2 / 2) * T) / (sig * math.sqrt(T))
rel = {}
for K in (0.01, 0.001):
    kap = K * sig * math.sqrt(dt52)
    L = bs_call(S0, KS, T, math.sqrt(leland_var(kap, dt52, 1))) - bs_call(S0, KS, T, sig)
    approx = 2 * kap * S0 * stats.norm.pdf(d1) * math.sqrt(T) / math.sqrt(2 * math.pi * dt52)
    rel[K] = abs(approx / L - 1)
ok(
    "Wilmott's spread 2 kappa S N'(d1) sqrt(tau)/sqrt(2 pi dt) is first order: relative error falls 5-20 times from K = 0.01 to 0.001",
    5 <= rel[0.01] / rel[0.001] <= 20,
    f"{rel[0.01]:.2e} and {rel[0.001]:.2e}",
)

# ---------------------------------------------------------------- part 2
print(
    "== part 2: simulated hedging costs against the Leland adjustment (risk-neutral, nested grids)"
)
rng = np.random.default_rng(20261023)
n_paths, n_fine, block = 100_000, 208, 10_000
grids = (13, 52, 208)
cases = [(s, K) for s in (-1, +1) for K in (0.1, 0.4)]
cost_acc = {(s, K, n): [0.0, 0.0] for s, K in cases for n in grids}
ledger = {
    s: {"id_err": 0.0, "test": [], "pnl": [], "open": [], "cash_close": [], "settle": []}
    for s in (-1, +1)
}
fixed = {n: {"cost": [], "pnl": []} for n in grids}
spread = {"sep": [], "agg": [], "step_ok": True, "same_ok": True}
for _ in range(n_paths // block):
    z = rng.standard_normal((block, n_fine))
    dtf = T / n_fine
    S = np.empty((block, n_fine + 1))
    S[:, 0] = S0
    S[:, 1:] = S0 * np.exp(np.cumsum((r - sig**2 / 2) * dtf + sig * math.sqrt(dtf) * z, axis=1))
    for n in grids:
        Sk = S[:, :: n_fine // n]
        dt = T / n
        t = np.arange(n + 1) * dt
        disc = np.exp(-r * t)
        itm = (Sk[:, -1] > KS).astype(float)
        for s, K in cases:
            kappa = K * sig * math.sqrt(dt)
            vol = math.sqrt(
                leland_var(kappa, dt, -s)
            )  # short (s = -1) uses sigma_hat, long sigma_check
            delta = np.empty_like(Sk)
            delta[:, :-1] = bs_delta(Sk[:, :-1], KS, T - t[:-1], vol)
            delta[:, -1] = itm
            h = -s * delta
            nu = np.diff(h, axis=1)
            cost = kappa * Sk[:, 1:] * np.abs(nu)
            pv_cost = cost @ disc[1:]
            cost_acc[(s, K, n)][0] += pv_cost.sum()
            cost_acc[(s, K, n)][1] += (pv_cost**2).sum()
            if n == 52 and K == 0.1:
                V = bs_call(S0, KS, T, sig)
                P = bs_call(S0, KS, T, vol)
                cash = -s * P - h[:, 0] * S0
                for k in range(1, n + 1):
                    cash = cash * math.exp(r * dt) - nu[:, k - 1] * Sk[:, k] - cost[:, k - 1]
                lhs = math.exp(-r * T) * (cash + h[:, -1] * Sk[:, -1])
                gains = (h[:, :-1] * np.diff(Sk * disc, axis=1)).sum(axis=1)
                rhs = -s * P + gains - pv_cost
                ledger[s]["id_err"] = max(
                    ledger[s]["id_err"], float(np.max(np.abs(lhs - rhs) / (1 + np.abs(lhs))))
                )
                payoff = np.maximum(Sk[:, -1] - KS, 0)
                W = lhs + s * math.exp(-r * T) * payoff  # discounted terminal wealth
                ledger[s]["test"].append(gains + s * (math.exp(-r * T) * payoff - V))
                ledger[s]["pnl"].append(W)
                ledger[s]["open"].append(kappa * np.abs(h[:, 0]) * S0)
                ledger[s]["cash_close"].append(
                    math.exp(-r * T) * kappa * np.abs(h[:, -2]) * Sk[:, -1]
                )
                ledger[s]["settle"].append(math.exp(-r * T) * cost[:, -1])
        # fixed kappa = 0.2 percent, short call hedged with the BSM delta at sigma, premium V
        delta = np.empty_like(Sk)
        delta[:, :-1] = bs_delta(Sk[:, :-1], KS, T - t[:-1], sig)
        delta[:, -1] = itm
        h = delta
        nu = np.diff(h, axis=1)
        pv_cost = (0.002 * Sk[:, 1:] * np.abs(nu)) @ disc[1:]
        gains = (h[:, :-1] * np.diff(Sk * disc, axis=1)).sum(axis=1)
        V = bs_call(S0, KS, T, sig)
        fixed[n]["cost"].append(pv_cost)
        fixed[n]["pnl"].append(
            V + gains - pv_cost - math.exp(-r * T) * np.maximum(Sk[:, -1] - KS, 0)
        )
        if n == 52:
            # part 3: bull spread, long K1 = 95, short K2 = 105, BSM deltas at sigma, kappa = 0.2 percent
            legs = []
            for Kl, sl in ((95.0, +1), (105.0, -1)):
                dl = np.empty_like(Sk)
                dl[:, :-1] = bs_delta(Sk[:, :-1], Kl, T - t[:-1], sig)
                dl[:, -1] = (Sk[:, -1] > Kl).astype(float)
                legs.append(np.diff(-sl * dl, axis=1))
            c_sep = 0.002 * Sk[:, 1:] * (np.abs(legs[0]) + np.abs(legs[1]))
            c_agg = 0.002 * Sk[:, 1:] * np.abs(legs[0] + legs[1])
            spread["step_ok"] &= bool((c_agg <= c_sep + 1e-12).all())
            spread["sep"].append(c_sep @ disc[1:])
            spread["agg"].append(c_agg @ disc[1:])
            # long and short the same call: net holding zero
            nu_long = np.diff(-delta, axis=1)
            nu_short = np.diff(delta, axis=1)
            agg_same = (0.002 * Sk[:, 1:] * np.abs(nu_long + nu_short)) @ disc[1:]
            sep_same = (0.002 * Sk[:, 1:] * (np.abs(nu_long) + np.abs(nu_short))) @ disc[1:]
            single = (0.002 * Sk[:, 1:] * np.abs(nu_short)) @ disc[1:]
            spread["same_ok"] &= bool(
                (agg_same == 0).all() and (np.abs(sep_same - 2 * single) <= 1e-12).all()
            )

V = bs_call(S0, KS, T, sig)
for s in (-1, +1):
    for key in ("test", "pnl", "open", "cash_close", "settle"):
        ledger[s][key] = np.concatenate(ledger[s][key])
name = {-1: "short", +1: "long"}
for s in (-1, +1):
    ok(
        f"{name[s]}, K = 0.1, N = 52: ledger identity on every path (signs, financing and discounting)",
        ledger[s]["id_err"] <= 1e-9,
        f"largest relative error {ledger[s]['id_err']:.1e}",
    )
    x = ledger[s]["test"]
    m, se = x.mean(), x.std(ddof=1) / math.sqrt(n_paths)
    ok(
        f"{name[s]}: mean discounted wealth within 4 s.e. of -s(P - V) - C_N (exact in expectation)",
        abs(m) <= 4 * se,
        f"difference {m:+.4f} (s.e. {se:.4f}), z = {m / se:+.2f}",
    )

print("    residual e_N = C_N - L (s.e. of C_N), relative to L")
for s, K in cases:
    dt_ref = {n: T / n for n in grids}
    res = {}
    for n in grids:
        kappa = K * sig * math.sqrt(dt_ref[n])
        vol = math.sqrt(leland_var(kappa, dt_ref[n], -s))
        L = -s * (bs_call(S0, KS, T, vol) - V)
        sm, sq = cost_acc[(s, K, n)]
        C = sm / n_paths
        se = math.sqrt((sq / n_paths - C**2) / (n_paths - 1))
        res[n] = C - L
        print(
            f"    {name[s]:5s} K = {K}: N = {n:3d}, kappa = {kappa:.5f}, vol = {vol:.4f}, L = {L:.4f}, C_N = {C:.4f}"
            f" (s.e. {se:.4f}), e_N = {C - L:+.4f} ({(C - L) / L:+.2%})"
        )
    a = [abs(res[n]) for n in grids]
    ok(
        f"{name[s]} K = {K}: |e_13| > |e_52| > |e_208| and |e_208| <= |e_13| / 2",
        a[0] > a[1] > a[2] and a[2] <= 0.5 * a[0],
        f"{a[0]:.4f}, {a[1]:.4f}, {a[2]:.4f}",
    )

for s in (-1, +1):
    w = ledger[s]["pnl"]
    print(
        f"    {name[s]} at the Leland price, K = 0.1, N = 52: mean discounted P&L {w.mean():+.4f} (s.e."
        f" {w.std(ddof=1) / math.sqrt(n_paths):.4f}), s.d. {w.std(ddof=1):.3f}, 5th percentile {np.percentile(w, 5):+.3f};"
        f" opening cost {ledger[s]['open'].mean():.4f}; settlement trade {ledger[s]['settle'].mean():.4f} against a"
        f" cash-settled close {ledger[s]['cash_close'].mean():.4f}"
    )
for n in grids:
    c, p = np.concatenate(fixed[n]["cost"]), np.concatenate(fixed[n]["pnl"])
    print(
        f"    fixed kappa = 0.2%, BSM delta, short call, N = {n:3d}: mean PV cost {c.mean():.4f}, P&L s.d. {p.std(ddof=1):.3f},"
        f" premium for a loss only 5 percent of the time {V - np.percentile(p, 5):.3f}"
    )

# ---------------------------------------------------------------- part 3
print(
    "== part 3: nonadditivity, a hedge-cost demonstration on the same paths (not a solved valuation)"
)
sep, agg = np.concatenate(spread["sep"]), np.concatenate(spread["agg"])
ok(
    "bull spread: aggregated trade cost never exceeds the separately hedged legs (every step, every path)",
    spread["step_ok"],
)
d = sep - agg
m, se = d.mean(), d.std(ddof=1) / math.sqrt(n_paths)
ok(
    "bull spread: mean saving from netting positive by more than 4 paired s.e.",
    m > 4 * se,
    f"separate {sep.mean():.4f}, aggregated {agg.mean():.4f}, saving {m:.4f} (s.e. {se:.5f})",
)
ok(
    "long and short the same call: aggregated cost 0 on every path, separate cost exactly twice one leg",
    spread["same_ok"],
)
kap, dtx = 0.002, 1 / 52
vc, vh = math.sqrt(leland_var(kap, dtx, -1)), math.sqrt(leland_var(kap, dtx, +1))
leg_by_leg = bs_call(S0, 95.0, T, vc) - bs_call(S0, 105.0, T, vh)
bs_spread = bs_call(S0, 95.0, T, sig) - bs_call(S0, 105.0, T, sig)
print(
    f"    reported, approximate: BSM spread {bs_spread:.4f}; leg-by-leg Leland {leg_by_leg:.4f} (long at {vc:.4f},"
    f" short at {vh:.4f}); BSM less simulated costs: separate {bs_spread - sep.mean():.4f}, aggregated"
    f" {bs_spread - agg.mean():.4f}"
)

if fails:
    print("FAILED:", ", ".join(fails))
    sys.exit(1)
print("all checks passed")
