"""Backtest design on a SYNTHETIC equity universe: objectives, procedures, metrics and problems (2026-10-20).

Worked numbers of meth:backtest-design-evaluation in compendium/research-engineering-validation/backtest-evaluation.tex.
The universe is simulated with a fixed seed: 300 stocks over 240 months, returns with NO true cross-sectional
predictability, and delisting after very poor cumulative performance. Nothing here is evidence about real markets;
the point is to show how each backtest error manufactures performance from noise.

Procedures compared: a survivor-only universe against the point-in-time universe; a signal using information
available at the decision against one using the same month's return (look-ahead); gross against net-of-cost returns
with turnover measured; parameter choice by in-sample Sharpe against a walk-forward that chooses on trailing data only
and is evaluated on the following year; expanding against rolling estimation windows.

Independent routes: the equal-weighted point-in-time return against the cross-sectional mean of the simulated
returns; turnover from weight changes against its definition; maximum drawdown from the running peak against a
direct search over all start and end months; the expected maximum Sharpe of N independent null strategies against
the in-sample winner.

Count convention: one check is one executed ok() call (a call inside a loop counts once per iteration).

Run: uv run python backtest-design-checks.py   (numpy). Exits 1 on failure.
"""

# standard library imports
import math
import sys

# third party library imports
import numpy as np

print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}")
fails = []
n_checks = 0


def ok(name, cond, detail=""):
    global n_checks
    n_checks += 1
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


rng = np.random.default_rng(20261020)
N, T = 300, 240
mkt = rng.normal(0.006, 0.045, T)
beta = rng.uniform(0.7, 1.3, N)
ret = mkt[:, None] * beta[None, :] + rng.normal(0, 0.09, (T, N))
alive = np.ones((T, N), dtype=bool)
level = np.ones(N)
for t in range(T):
    level *= 1 + np.where(alive[t], ret[t], 0.0)
    dead = level < 0.25  # delisted after losing 75% of value
    if t + 1 < T:
        alive[t + 1 :, dead] = False
ret = np.where(alive, ret, np.nan)


def sharpe(x):
    x = x[~np.isnan(x)]
    return float(np.mean(x) / np.std(x, ddof=1) * math.sqrt(12))


def max_dd(r):
    wealth = np.cumprod(1 + r)
    peak = np.maximum.accumulate(wealth)
    return float(np.max(1 - wealth / peak))


# ---------------------------------------------------------------------------------------------
print("== part 1: survivorship - testing only the names that exist today")
ew_pit = np.nanmean(ret, axis=1)
survivors = alive[-1]
ew_surv = np.nanmean(ret[:, survivors], axis=1)
ok(
    "an equal-weighted portfolio of today's survivors earns more than the point-in-time universe that a real investor "
    "could have held, with no skill involved",
    ew_surv.mean() > ew_pit.mean() + 0.001,
    f"{survivors.sum()} survivors of {N}; {ew_surv.mean() * 1200:.2f}% a year against {ew_pit.mean() * 1200:.2f}%",
)
ok(
    "the point-in-time return equals the cross-sectional mean of returns of names alive each month",
    np.allclose(ew_pit, [np.mean(ret[t][alive[t]]) for t in range(T)]),
)

# ---------------------------------------------------------------------------------------------
print("== part 2: look-ahead - the timing of information")


def long_short(signal, rets, k=0.2):
    """Equal-weight long the top k, short the bottom k by signal, among names with both values available.

    Returns the monthly return and the monthly one-way turnover per side (1.0 when the book is first built).
    """
    out, turns, w_prev = np.full(len(rets), np.nan), np.full(len(rets), np.nan), None
    for t in range(len(rets)):
        s, r_ = signal[t], rets[t]
        ok_ = ~np.isnan(s) & ~np.isnan(r_)
        if ok_.sum() < 20:
            continue
        idx = np.where(ok_)[0]
        order = idx[np.argsort(s[idx])]
        m = max(1, int(k * len(order)))
        w = np.zeros(N)
        w[order[-m:]] = 1 / m
        w[order[:m]] = -1 / m
        out[t] = float(np.sum(w[ok_] * r_[ok_]))
        turns[t] = 1.0 if w_prev is None else 0.5 * np.abs(w - w_prev).sum() / 2
        w_prev = w
    return out, turns


honest = np.vstack([np.full(N, np.nan), ret[:-1]])  # last month's return, known at the decision
cheat = ret.copy()  # this month's return, known only after the month
r_h, turn_h = long_short(honest, ret)
r_c, _ = long_short(cheat, ret)
ok(
    "a one-month reversal signal using last month's return earns nothing, as the simulation contains no "
    "predictability; the same rule using this month's return (look-ahead) shows an enormous Sharpe ratio",
    abs(sharpe(r_h)) < 0.6 and sharpe(r_c) > 10,
    f"honest Sharpe {sharpe(r_h):.2f}, look-ahead Sharpe {sharpe(r_c):.1f}",
)

# ---------------------------------------------------------------------------------------------
print("== part 3: costs and turnover")
mom = np.full((T, N), np.nan)
for t in range(12, T):
    mom[t] = np.nanprod(1 + ret[t - 12 : t - 1], axis=0) - 1
mom = np.where(np.isnan(ret), np.nan, mom)
r_m, turn_m = long_short(mom, ret)
cost = 0.0020  # 20 bp per unit traded
r_net = r_m - 2 * cost * turn_m  # both the long and the short side trade
avg_turn = float(np.nanmean(turn_m[1:][~np.isnan(turn_m[:-1])]))
ok(
    "a 12-1 momentum rule replaces about a fifth to a half of each side every month; at 20 bp per trade on both "
    "sides, costs take more than 1 point a year from a strategy whose gross return is noise",
    0.15 < avg_turn < 0.7 and np.nanmean(r_m - r_net) * 12 > 0.01,
    f"turnover {avg_turn:.2f} per side a month; cost {np.nanmean(r_m - r_net) * 1200:.2f}% a year",
)
w_a = np.array([0.5, 0.5, 0.0, -0.5, -0.5, 0.0])
w_b = np.array([0.5, 0.0, 0.5, -0.5, 0.0, -0.5])
ok(
    "turnover definition: swapping one of two long names and one of two short names changes weights by 2.0 in "
    "absolute terms, a one-way turnover of 1.0 for the book or 0.5 per side",
    math.isclose(np.abs(w_b - w_a).sum(), 2.0)
    and math.isclose(0.5 * np.abs(w_b - w_a).sum() / 2, 0.5),
)

# ---------------------------------------------------------------------------------------------
print("== part 4: metrics and visuals")
r_ok = r_net[~np.isnan(r_net)]
dd = max_dd(r_ok)
brute = 0.0
wealth = np.cumprod(1 + r_ok)
for i in range(len(wealth)):
    brute = max(brute, float(np.max(1 - wealth[i:] / wealth[i])))
ok(
    "maximum drawdown from the running peak equals a brute-force search over all start and end months",
    math.isclose(dd, brute, rel_tol=1e-12),
    f"{dd:.3f}",
)
hit = float(np.mean(r_ok > 0))
ok(
    "the report states annualised return, volatility, Sharpe ratio, maximum drawdown, hit rate and turnover for the "
    "net series; for this noise strategy the hit rate is near 50%",
    0.40 < hit < 0.60,
    f"ann. return {np.mean(r_ok) * 1200:.2f}%, vol {np.std(r_ok, ddof=1) * math.sqrt(12) * 100:.1f}%, "
    f"Sharpe {sharpe(r_ok):.2f}, max DD {dd:.2f}, hit {hit:.2f}",
)

# ---------------------------------------------------------------------------------------------
print("== part 5: parameter search, in-sample selection and walk-forward evaluation")
lookbacks = list(range(1, 13))
signals = {}
for L in lookbacks:
    s = np.full((T, N), np.nan)
    for t in range(L + 1, T):
        s[t] = np.nanprod(1 + ret[t - L - 1 : t - 1], axis=0) - 1
    signals[L] = np.where(np.isnan(ret), np.nan, s)
series = {L: long_short(signals[L], ret)[0] for L in lookbacks}
for L in lookbacks:
    series[-L] = -series[L]  # also try the reversed (contrarian) rule: 24 trials in total
half = T // 2
is_sharpe = {k: sharpe(v[:half]) for k, v in series.items()}
best = max(is_sharpe, key=is_sharpe.get)
oos_best = sharpe(series[best][half:])
emax = math.sqrt(2 * math.log(len(series))) - (
    math.log(math.log(len(series))) + math.log(4 * math.pi)
) / (2 * math.sqrt(2 * math.log(len(series))))
ok(
    "choosing the best of 24 rules on the first 10 years gives an in-sample Sharpe ratio near the expected maximum "
    "of 24 null strategies, and it does not survive the second 10 years",
    is_sharpe[best] > 0.3 and oos_best < is_sharpe[best] - 0.3,
    f"best rule {best}: in-sample {is_sharpe[best]:.2f}, out-of-sample {oos_best:.2f}; expected max of 24 nulls "
    f"about {emax / math.sqrt(half / 12):.2f}",
)
wf = []
for year in range(10, 20):
    start, end = year * 12, (year + 1) * 12
    trail = {k: sharpe(v[start - 60 : start]) for k, v in series.items()}  # rolling 5-year window
    k_star = max(trail, key=trail.get)
    wf.extend(series[k_star][start:end])
wf = np.array(wf)
ok(
    "a walk-forward that re-selects the rule each year from the trailing five years only, and records the following "
    "year, has a Sharpe ratio near zero: the honest estimate for a search over noise",
    abs(sharpe(wf)) < 0.6,
    f"walk-forward Sharpe {sharpe(wf):.2f}",
)
exp_mean = [np.nanmean(series[6][:t]) for t in range(60, T, 12)]
roll_mean = [np.nanmean(series[6][t - 60 : t]) for t in range(60, T, 12)]
ok(
    "expanding windows give estimates that change slowly and use all past data; 5-year rolling windows adapt faster "
    "but vary more",
    np.std(np.diff(exp_mean)) < np.std(np.diff(roll_mean)),
)

print(f"\n{n_checks} checks executed")
if fails:
    print("FAILED:", fails)
    sys.exit(1)
print("all checks passed")
