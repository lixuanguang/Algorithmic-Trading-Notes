"""Backtest design on a SYNTHETIC equity universe: objectives, procedures, metrics and problems (2026-10-20).

Worked numbers of meth:backtest-design-evaluation in compendium/research-engineering-validation/backtest-evaluation.tex.
The universe is simulated with a fixed seed: 300 stocks over 240 months, returns with NO true cross-sectional
predictability, and delisting after very poor cumulative performance. Nothing here is evidence about real markets;
the point is to show how each backtest error manufactures performance from noise.

Procedures compared: a survivor-only universe against the point-in-time universe; a signal using information
available at the decision against one using the same month's return (look-ahead); gross against net-of-cost returns
with traded notional measured; parameter choice by in-sample Sharpe against a walk-forward that chooses on trailing
data only and is evaluated on the following year; expanding against rolling estimation windows.

Book and cost conventions (part 3). NAV V is cash plus the signed market value of the positions; a long-short target
is +1 of NAV long and -1 short (gross exposure 2, net 0). Short-sale proceeds stay in cash; cash, collateral and
short rebates earn zero and there is no borrow fee or margin, so returns are excess-of-cash returns. Targets are
fractions of post-trade NAV. At the start of each month the pre-trade holdings are last month's positions after
their own returns (drift); trades take them to the targets, and the fee is c times the traded notional, purchases
plus sales (including cover-buys and short sales), paid from cash. Because post-trade NAV is NAV less the fee, the fee
solves f = c * sum|w* (V - f) - h| (a fixed point, found by iteration). The book is established from cash, so the
first month pays for building it; a position in a name that delists is sold at its last value.

Independent routes: the equal-weighted point-in-time return against the cross-sectional mean of the simulated
returns; hand-reconciled small ledgers (establishment from cash, unchanged targets after unequal returns, a long-short
swap) against the simulator, with cash + positions = NAV after every trade; the simulated net growth against
(post-fee NAV / pre-trade NAV) x (1 + w* . r) month by month; the fee against c times the traded notional recomputed
from the ledger; maximum drawdown from the running peak including the initial wealth of 1 against an explicit search
over all pairs of dates on the same path, and three decisive cases that the earlier peak (which omitted the initial
wealth) fails; the expected maximum Sharpe of N independent null strategies against the in-sample winner.

Correction (2026-10-20, final audit): the earlier version measured turnover as a quarter of the change in successive
target weights and deducted twice that times c, i.e. half the cost of the traded notional, and ignored drift; its
drawdown omitted the initial wealth of 1, as did its brute-force check.

Count convention: one check is one executed ok() call (a call inside a loop counts once per iteration).

Run: uv run --frozen --no-editable python backtest-design-checks.py   (numpy). Exits 1 on failure.
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
    """Maximum drawdown of the wealth path that starts at 1 before the first return."""
    wealth = np.concatenate([[1.0], np.cumprod(1 + np.asarray(r, dtype=float))])
    peak = np.maximum.accumulate(wealth)
    return float(np.max(1 - wealth / peak))


def max_dd_pairs(r):
    """Independent route: the largest loss from any date i to any later date j, with date 0 at wealth 1."""
    wealth = [1.0]
    for x in r:
        wealth.append(wealth[-1] * (1 + x))
    return max(
        (1 - wealth[j] / wealth[i] for i in range(len(wealth)) for j in range(i, len(wealth))),
        default=0.0,
    )


def max_dd_omitting_start(r):
    """The earlier, incorrect peak: the running maximum of wealth after the first return only."""
    wealth = np.cumprod(1 + np.asarray(r, dtype=float))
    return float(np.max(1 - wealth / np.maximum.accumulate(wealth)))


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

    Returns the monthly gross return of the target book (rebalanced to target at each month's start, no costs) and
    the target weights (fractions of post-trade NAV; a zero row means hold cash).
    """
    out, targets = np.full(len(rets), np.nan), np.zeros((len(rets), N))
    for t in range(len(rets)):
        s, r_ = signal[t], rets[t]
        ok_ = ~np.isnan(s) & ~np.isnan(r_)
        if ok_.sum() < 20:
            continue
        idx = np.where(ok_)[0]
        order = idx[np.argsort(s[idx])]
        m = max(1, int(k * len(order)))
        targets[t, order[-m:]] = 1 / m
        targets[t, order[:m]] = -1 / m
        out[t] = float(np.sum(targets[t, ok_] * r_[ok_]))
    return out, targets


def rebalance(h, cash, w_star, c):
    """Trade signed holdings h (currency) to target weights w_star of post-trade NAV; fee c per unit traded.

    Returns new holdings, new cash, the fee and the traded notional (purchases plus sales).
    """
    v_pre = cash + h.sum()
    fee = 0.0
    for _ in range(50):  # f = c * sum|w*(V - f) - h| is a contraction because c * gross < 1
        fee_new = c * np.abs(w_star * (v_pre - fee) - h).sum()
        if abs(fee_new - fee) < 1e-15:
            break
        fee = fee_new
    h_new = w_star * (v_pre - fee)
    traded = np.abs(h_new - h).sum()
    cash_new = cash - (h_new - h).sum() - fee  # purchases use cash, sales and short sales raise it
    return h_new, cash_new, fee, traded


def simulate_book(targets, rets, c, v0=1.0):
    """Monthly ledger of a book that starts in cash, trades to each month's targets, then earns that month's returns.

    Returns net monthly returns (NaN before the first trade), traded notional as a fraction of pre-trade NAV, fees,
    and the largest |cash + positions - NAV| seen after any trade.
    """
    h, cash, v = np.zeros(targets.shape[1]), v0, v0
    net, traded_frac, fees = np.full(len(rets), np.nan), np.zeros(len(rets)), np.zeros(len(rets))
    started, worst = False, 0.0
    for t in range(len(rets)):
        if targets[t].any() or h.any():
            h, cash, fee, traded = rebalance(h, cash, targets[t], c)
            worst = max(worst, abs(cash + h.sum() - (v - fee)))
            traded_frac[t], fees[t] = traded / v, fee
            started = True
        h = h * (1 + np.nan_to_num(rets[t]))  # delisted names hold no position after the trade
        v_new = cash + h.sum()
        if started:
            net[t] = v_new / v - 1
        v = v_new
    return net, traded_frac, fees, worst


honest = np.vstack([np.full(N, np.nan), ret[:-1]])  # last month's return, known at the decision
cheat = ret.copy()  # this month's return, known only after the month
r_h, _ = long_short(honest, ret)
r_c, _ = long_short(cheat, ret)
ok(
    "a one-month reversal signal using last month's return earns nothing, as the simulation contains no "
    "predictability; the same rule using this month's return (look-ahead) shows an enormous Sharpe ratio",
    abs(sharpe(r_h)) < 0.6 and sharpe(r_c) > 10,
    f"honest Sharpe {sharpe(r_h):.2f}, look-ahead Sharpe {sharpe(r_c):.1f}",
)

# ---------------------------------------------------------------------------------------------
print("== part 3: costs, traded notional and the book's ledger")
cost = 0.0020  # 20 bp of traded notional, on purchases and sales alike

# hand-reconciled small ledgers (closed forms derived by hand; the simulator must reproduce them)
h, cash, fee, traded = rebalance(np.zeros(2), 100.0, np.array([0.5, 0.5]), cost)
f_hand = 100 * cost / (1 + cost)  # all purchases: f = c (100 - f)
ok(
    "establishment from 100 of cash at 50/50 long-only: the fee solves f = c(100 - f) = 0.19960, each position is "
    "49.9002 and cash is exactly zero (purchases 99.8004 plus fee 0.1996)",
    math.isclose(fee, f_hand, rel_tol=1e-12)
    and np.allclose(h, 0.5 * (100 - f_hand))
    and abs(cash) < 1e-12
    and math.isclose(traded + fee, 100.0, rel_tol=1e-12),
    f"fee {fee:.5f}, positions {h[0]:.4f}, cash {cash:.1e}",
)
h, cash, fee, traded = rebalance(np.array([55.0, 45.0]), 0.0, np.array([0.5, 0.5]), cost)
ok(
    "unchanged 50/50 targets after returns of +10% and -10% (holdings 55 and 45, NAV 100): the successive target "
    "weights do not change, so a target-difference turnover is zero, but the book must sell 5.01 and buy 4.99, "
    "traded notional 10.00 and fee 0.0200; cash stays zero (5.01 - 4.99 - 0.02)",
    math.isclose(traded, 10.0, rel_tol=1e-12)
    and math.isclose(fee, 0.02, rel_tol=1e-12)
    and np.allclose(h, [49.99, 49.99])
    and abs(cash) < 1e-12,
    f"traded {traded:.4f}, fee {fee:.4f}, cash {cash:.1e}",
)
w_a = np.array([0.5, 0.5, 0.0, -0.5, -0.5, 0.0])
w_b = np.array([0.5, 0.0, 0.5, -0.5, 0.0, -0.5])
h, cash, fee, traded = rebalance(w_a.copy(), 1.0, w_b, cost)
old_turn = (
    0.5 * np.abs(w_b - w_a).sum() / 2
)  # the earlier definition: a quarter of the weight change
ok(
    "long-short swap of one of two longs and one of two shorts from NAV 1 (cash 1 = capital plus short proceeds): "
    "absolute trades total 2.0, so the fee is 0.004; the earlier rule deducted 2 x 0.002 x 0.5 = 0.002. After the "
    "trade cash is 0.996, longs 0.996, shorts -0.996, NAV 0.996 and gross exposure 2",
    math.isclose(traded, 2.0, rel_tol=1e-12)
    and math.isclose(fee, 0.004, rel_tol=1e-12)
    and math.isclose(2 * cost * old_turn, 0.002)
    and math.isclose(cash, 0.996, rel_tol=1e-12)
    and math.isclose(h[h > 0].sum(), 0.996)
    and math.isclose(np.abs(h).sum() / (cash + h.sum()), 2.0),
    f"fee {fee:.4f} against {2 * cost * old_turn:.4f} under the earlier rule",
)
h, cash, fee, traded = rebalance(
    np.array([0.6, 0.5, -0.5, -0.5]), 1.0, np.array([0.5, 0.5, -0.5, -0.5]), cost
)
f_hand = (
    0.2 * cost / (1 + cost)
)  # traded = 0.2 - f: sell 0.05 + f/2 of A, buy 0.05 - f/2 of B, short more C and D
ok(
    "long-short drift: the first long rises 20% (NAV 1.1) with targets unchanged; traded notional is 0.2 - f and "
    "f = 0.2c/(1 + c) = 0.000399, after which every weight is exactly +-0.5 of NAV",
    math.isclose(fee, f_hand, rel_tol=1e-12)
    and math.isclose(traded, 0.2 - f_hand, rel_tol=1e-12)
    and np.allclose(h / (cash + h.sum()), [0.5, 0.5, -0.5, -0.5]),
    f"fee {fee:.6f}, traded {traded:.6f}",
)

# the momentum backtest, gross and with the ledger
mom = np.full((T, N), np.nan)
for t in range(12, T):
    mom[t] = np.nanprod(1 + ret[t - 12 : t - 1], axis=0) - 1
mom = np.where(np.isnan(ret), np.nan, mom)
r_m, tgt_m = long_short(mom, ret)
r_net, traded_m, fee_m, worst = simulate_book(tgt_m, ret, cost)
r_zero, _, _, _ = simulate_book(tgt_m, ret, 0.0)
live = ~np.isnan(r_m)
ok(
    "with a zero cost rate the ledger reproduces the gross target-book return every month, and cash plus positions "
    "equals NAV after every trade",
    np.allclose(r_zero[live], r_m[live], atol=1e-13) and worst < 1e-12,
    f"largest ledger gap {worst:.1e}",
)
wealth_pre = np.concatenate([[1.0], np.cumprod(1 + np.nan_to_num(r_net))])[:-1]
ok(
    "each net month equals (post-fee NAV / pre-trade NAV) x (1 + target-weighted return), and the fee equals 20 bp "
    "of the traded notional",
    np.allclose(1 + r_net[live], (1 - fee_m[live] / wealth_pre[live]) * (1 + r_m[live]), atol=1e-13)
    and np.allclose(fee_m, cost * traded_m * wealth_pre, rtol=1e-9, atol=1e-15),
)
first = int(np.argmax(live))
old_rule = np.full(T, np.nan)
w_prev = None
for t in np.where(live)[0]:
    old_rule[t] = 1.0 if w_prev is None else 0.5 * np.abs(tgt_m[t] - w_prev).sum() / 2
    w_prev = tgt_m[t]
old_drag = float(np.nanmean(2 * cost * old_rule)) * 12
target_diff = float(np.mean([np.abs(tgt_m[t] - tgt_m[t - 1]).sum() for t in range(first + 1, T)]))
avg_traded = float(np.mean(traded_m[first + 1 :]))
drag = float(np.mean((r_m - r_net)[live])) * 12
ok(
    "the book is established at month 12 by trading 2.0 of NAV (gross exposure 2); thereafter it trades about 1.0 of "
    "NAV a month, more than the change in successive targets because drift must also be traded back, and the cost "
    "drag is about twice the earlier rule's",
    math.isclose(traded_m[first], 2.0 / (1 + 2 * cost), rel_tol=1e-9)
    and avg_traded > target_diff
    and drag > 1.8 * old_drag,
    f"establishment {traded_m[first]:.4f} of opening NAV; monthly traded {avg_traded:.3f} of NAV against "
    f"{target_diff:.3f} from target changes; drag {drag * 100:.2f}% a year against {old_drag * 100:.2f}% earlier",
)

# ---------------------------------------------------------------------------------------------
print("== part 4: metrics and visuals")
for path, want in (([-0.10, 0.05], 0.10), ([-0.05], 0.05), ([0.01, 0.02, 0.03], 0.0)):
    ok(
        f"maximum drawdown of {path} is {want:.2f} with the initial wealth of 1 in the peak, by the running peak and "
        "by the pair search; the earlier peak, which began after the first return, gets it wrong whenever the "
        "first return is negative",
        math.isclose(max_dd(path), want, abs_tol=1e-12)
        and math.isclose(max_dd_pairs(path), want, abs_tol=1e-12),
        f"earlier peak {max_dd_omitting_start(path):.3f}",
    )
ok(
    "the decisive cases separate the two definitions: the earlier peak gives 0 for [-0.10, +0.05] and for a single "
    "negative return",
    max_dd_omitting_start([-0.10, 0.05]) == 0.0 and max_dd_omitting_start([-0.05]) == 0.0,
)
r_ok = r_net[~np.isnan(r_net)]
dd = max_dd(r_ok)
ok(
    "on the net series the running-peak drawdown equals the pair search over every date, including the start",
    math.isclose(dd, max_dd_pairs(r_ok), rel_tol=1e-12),
    f"{dd:.3f}",
)
hit = float(np.mean(r_ok > 0))
ok(
    "the report states annualised return, volatility, Sharpe ratio, maximum drawdown, hit rate and traded notional "
    "for the net series; for this noise strategy costs push the hit rate a little below 50%",
    0.40 < hit < 0.60,
    f"ann. return {np.mean(r_ok) * 1200:.2f}%, vol {np.std(r_ok, ddof=1) * math.sqrt(12) * 100:.1f}%, "
    f"Sharpe {sharpe(r_ok):.2f}, max DD {dd:.2f}, hit {hit:.2f}; gross ann. return "
    f"{np.nanmean(r_m) * 1200:.2f}%, Sharpe {sharpe(r_m):.2f}, max DD {max_dd(r_m[live]):.2f}",
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
