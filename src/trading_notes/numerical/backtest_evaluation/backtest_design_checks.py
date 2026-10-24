"""Backtest design: how survivorship, look-ahead, costs and search make performance from noise."""

import math
import sys
from collections.abc import Iterable, Sequence
from typing import Final

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.backtest_evaluation.backtest_book import (
    LongShortRule,
    TradingLedger,
    Universe,
    annualised_sharpe,
    max_drawdown,
)
from trading_notes.numerical.report import CheckReport
from trading_notes.records import Record

type Floats = NDArray[np.float64]
type Bools = NDArray[np.bool_]

SEED: Final = 20261020
N: Final = 300  # stocks
T: Final = 240  # months
RULE: Final = LongShortRule()


class MomentumBook(Record):
    """Part 3's momentum backtest, which part 4 measures.

    Attributes:
        gross: The target book's monthly gross returns; NaN in a month without a book.
        net: The ledger's net monthly returns; NaN before the first trade.
        live: The months with a gross return.
    """

    gross: Floats
    net: Floats
    live: Bools


def max_dd_pairs(r: Iterable[float]) -> float:
    """Independent route: the largest loss from any date i to any later date j.

    Date 0 is at wealth 1.
    """
    wealth = [1.0]
    for x in r:
        wealth.append(wealth[-1] * (1 + x))
    return max(
        (1 - wealth[j] / wealth[i] for i in range(len(wealth)) for j in range(i, len(wealth))),
        default=0.0,
    )


def max_dd_omitting_start(r: Sequence[float]) -> float:
    """Return a drawdown whose running peak starts after the first return, omitting wealth 1.

    This alternative definition misses any fall in the first period.
    """
    wealth = np.cumprod(1 + np.asarray(r, dtype=float))
    return float(np.max(1 - wealth / np.maximum.accumulate(wealth)))


def check_survivorship(report: CheckReport, u: Universe) -> None:
    """Part 1: today's survivors against the point-in-time universe."""
    print("== part 1: survivorship - testing only the names that exist today")
    ret, alive = u.ret, u.alive
    ew_pit = np.nanmean(ret, axis=1)
    survivors = alive[-1]
    ew_surv = np.nanmean(ret[:, survivors], axis=1)
    report.ok(
        "an equal-weighted portfolio of today's survivors earns more than the point-in-time"
        " universe that a real investor could have held, with no skill involved",
        bool(ew_surv.mean() > ew_pit.mean() + 0.001),
        f"{survivors.sum()} survivors of {N}; {ew_surv.mean() * 1200:.2f}% a year against"
        f" {ew_pit.mean() * 1200:.2f}%",
    )
    report.ok(
        "the point-in-time return equals the cross-sectional mean of returns of names alive each"
        " month",
        np.allclose(ew_pit, [np.mean(ret[t][alive[t]]) for t in range(T)]),
    )


def check_look_ahead(report: CheckReport, u: Universe) -> None:
    """Part 2: a signal known at the decision against the same month's return."""
    print("== part 2: look-ahead - the timing of information")
    ret = u.ret
    honest = np.vstack([np.full(N, np.nan), ret[:-1]])  # last month's return, known at the decision
    cheat = ret.copy()  # this month's return, known only after the month
    r_h, _ = RULE.book(honest, ret)
    r_c, _ = RULE.book(cheat, ret)
    report.ok(
        "a one-month reversal signal using last month's return earns nothing, as the simulation"
        " contains no predictability; the same rule using this month's return (look-ahead) shows"
        " an enormous Sharpe ratio",
        abs(annualised_sharpe(r_h)) < 0.6 and annualised_sharpe(r_c) > 10,
        f"honest Sharpe {annualised_sharpe(r_h):.2f},"
        f" look-ahead Sharpe {annualised_sharpe(r_c):.1f}",
    )


def check_costs(report: CheckReport, u: Universe) -> MomentumBook:
    """Part 3: hand-reconciled ledgers, then the momentum book gross and net of costs."""
    print("== part 3: costs, traded notional and the book's ledger")
    ret = u.ret
    cost = 0.0020  # 20 bp of traded notional, on purchases and sales alike
    ledger = TradingLedger(cost=cost)

    # hand-reconciled small ledgers (closed forms derived by hand; the simulator must
    # reproduce them)
    trade = ledger.rebalance(np.zeros(2), 100.0, np.array([0.5, 0.5]))
    h, cash, fee, traded = trade.holdings, trade.cash, trade.fee, trade.traded
    f_hand = 100 * cost / (1 + cost)  # all purchases: f = c (100 - f)
    report.ok(
        "establishment from 100 of cash at 50/50 long-only: the fee solves f = c(100 - f) ="
        " 0.19960, each position is 49.9002 and cash is exactly zero (purchases 99.8004 plus fee"
        " 0.1996)",
        math.isclose(fee, f_hand, rel_tol=1e-12)
        and np.allclose(h, 0.5 * (100 - f_hand))
        and abs(cash) < 1e-12
        and math.isclose(traded + fee, 100.0, rel_tol=1e-12),
        f"fee {fee:.5f}, positions {h[0]:.4f}, cash {cash:.1e}",
    )
    trade = ledger.rebalance(np.array([55.0, 45.0]), 0.0, np.array([0.5, 0.5]))
    h, cash, fee, traded = trade.holdings, trade.cash, trade.fee, trade.traded
    report.ok(
        "unchanged 50/50 targets after returns of +10% and -10% (holdings 55 and 45, NAV 100): the"
        " successive target weights do not change, so a target-difference turnover is zero, but"
        " the book must sell 5.01 and buy 4.99, traded notional 10.00 and fee 0.0200; cash stays"
        " zero (5.01 - 4.99 - 0.02)",
        math.isclose(traded, 10.0, rel_tol=1e-12)
        and math.isclose(fee, 0.02, rel_tol=1e-12)
        and np.allclose(h, [49.99, 49.99])
        and abs(cash) < 1e-12,
        f"traded {traded:.4f}, fee {fee:.4f}, cash {cash:.1e}",
    )
    w_a = np.array([0.5, 0.5, 0.0, -0.5, -0.5, 0.0])
    w_b = np.array([0.5, 0.0, 0.5, -0.5, 0.0, -0.5])
    trade = ledger.rebalance(w_a.copy(), 1.0, w_b)
    h, cash, fee, traded = trade.holdings, trade.cash, trade.fee, trade.traded
    # target-difference turnover: a quarter of the change in target weights, costed at 2c
    old_turn = 0.5 * np.abs(w_b - w_a).sum() / 2
    report.ok(
        "long-short swap of one of two longs and one of two shorts from NAV 1 (cash 1 = capital"
        " plus short proceeds): absolute trades total 2.0, so the fee is 0.004; target-difference"
        " turnover would deduct 2 x 0.002 x 0.5 = 0.002. After the trade cash is 0.996, longs"
        " 0.996, shorts -0.996, NAV 0.996 and gross exposure 2",
        math.isclose(traded, 2.0, rel_tol=1e-12)
        and math.isclose(fee, 0.004, rel_tol=1e-12)
        and math.isclose(2 * cost * old_turn, 0.002)
        and math.isclose(cash, 0.996, rel_tol=1e-12)
        and math.isclose(h[h > 0].sum(), 0.996)
        and math.isclose(np.abs(h).sum() / (cash + h.sum()), 2.0),
        f"fee {fee:.4f} against {2 * cost * old_turn:.4f} under target-difference turnover",
    )
    trade = ledger.rebalance(
        np.array([0.6, 0.5, -0.5, -0.5]), 1.0, np.array([0.5, 0.5, -0.5, -0.5])
    )
    h, cash, fee, traded = trade.holdings, trade.cash, trade.fee, trade.traded
    # traded = 0.2 - f: sell 0.05 + f/2 of A, buy 0.05 - f/2 of B, short more C and D
    f_hand = 0.2 * cost / (1 + cost)
    report.ok(
        "long-short drift: the first long rises 20% (NAV 1.1) with targets unchanged; traded"
        " notional is 0.2 - f and f = 0.2c/(1 + c) = 0.000399, after which every weight is"
        " exactly +-0.5 of NAV",
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
    r_m, tgt_m = RULE.book(mom, ret)
    run = ledger.run(tgt_m, ret)
    r_net, traded_m, fee_m, worst = run.net, run.traded_fraction, run.fees, run.worst_gap
    r_zero = TradingLedger(cost=0.0).run(tgt_m, ret).net
    live = ~np.isnan(r_m)
    report.ok(
        "with a zero cost rate the ledger reproduces the gross target-book return every month,"
        " and cash plus positions equals NAV after every trade",
        np.allclose(r_zero[live], r_m[live], atol=1e-13) and worst < 1e-12,
        f"largest ledger gap {worst:.1e}",
    )
    wealth_pre = np.concatenate([[1.0], np.cumprod(1 + np.nan_to_num(r_net))])[:-1]
    report.ok(
        "each net month equals (post-fee NAV / pre-trade NAV) x (1 + target-weighted return), and"
        " the fee equals 20 bp of the traded notional",
        np.allclose(
            1 + r_net[live], (1 - fee_m[live] / wealth_pre[live]) * (1 + r_m[live]), atol=1e-13
        )
        and np.allclose(fee_m, cost * traded_m * wealth_pre, rtol=1e-9, atol=1e-15),
    )
    first = int(np.argmax(live))
    old_rule = np.full(T, np.nan)
    w_prev: Floats | None = None
    for t in np.where(live)[0]:
        old_rule[t] = 1.0 if w_prev is None else 0.5 * np.abs(tgt_m[t] - w_prev).sum() / 2
        w_prev = tgt_m[t]
    old_drag = float(np.nanmean(2 * cost * old_rule)) * 12
    target_diff = float(
        np.mean([np.abs(tgt_m[t] - tgt_m[t - 1]).sum() for t in range(first + 1, T)])
    )
    avg_traded = float(np.mean(traded_m[first + 1 :]))
    drag = float(np.mean((r_m - r_net)[live])) * 12
    report.ok(
        "the book is established at month 12 by trading 2.0 of NAV (gross exposure 2); thereafter"
        " it trades about 1.0 of NAV a month, more than the change in successive targets because"
        " drift must also be traded back, and the cost drag is about twice that of"
        " target-difference turnover",
        math.isclose(traded_m[first], 2.0 / (1 + 2 * cost), rel_tol=1e-9)
        and avg_traded > target_diff
        and drag > 1.8 * old_drag,
        f"establishment {traded_m[first]:.4f} of opening NAV; monthly traded {avg_traded:.3f} of"
        f" NAV against {target_diff:.3f} from target changes; drag {drag * 100:.2f}% a year"
        f" against {old_drag * 100:.2f}% by target differences",
    )
    return MomentumBook(gross=r_m, net=r_net, live=live)


def check_metrics(report: CheckReport, book: MomentumBook) -> None:
    """Part 4: maximum drawdown by two routes, and the net series' report."""
    print("== part 4: metrics and visuals")
    for path, want in (([-0.10, 0.05], 0.10), ([-0.05], 0.05), ([0.01, 0.02, 0.03], 0.0)):
        report.ok(
            f"maximum drawdown of {path} is {want:.2f} with the initial wealth of 1 in the peak,"
            " by the running peak and by the pair search; a peak that starts after the first return"
            " gets it wrong whenever the first return is negative",
            math.isclose(max_drawdown(path), want, abs_tol=1e-12)
            and math.isclose(max_dd_pairs(path), want, abs_tol=1e-12),
            f"peak after the first return {max_dd_omitting_start(path):.3f}",
        )
    report.ok(
        "the decisive cases separate the two definitions: a peak after the first return gives 0"
        " for [-0.10, +0.05] and for a single negative return",
        max_dd_omitting_start([-0.10, 0.05]) == 0.0 and max_dd_omitting_start([-0.05]) == 0.0,
    )
    r_m, r_net, live = book.gross, book.net, book.live
    r_ok = r_net[~np.isnan(r_net)]
    dd = max_drawdown(r_ok)
    report.ok(
        "on the net series the running-peak drawdown equals the pair search over every date,"
        " including the start",
        math.isclose(dd, max_dd_pairs(r_ok), rel_tol=1e-12),
        f"{dd:.3f}",
    )
    hit = float(np.mean(r_ok > 0))
    report.ok(
        "the report states annualised return, volatility, Sharpe ratio, maximum drawdown, hit rate"
        " and traded notional for the net series; for this noise strategy costs push the hit rate"
        " a little below 50%",
        0.40 < hit < 0.60,
        f"ann. return {np.mean(r_ok) * 1200:.2f}%, vol"
        f" {np.std(r_ok, ddof=1) * math.sqrt(12) * 100:.1f}%,"
        f" Sharpe {annualised_sharpe(r_ok):.2f}, max DD {dd:.2f}, hit {hit:.2f};"
        f" gross ann. return {np.nanmean(r_m) * 1200:.2f}%,"
        f" Sharpe {annualised_sharpe(r_m):.2f}, max DD {max_drawdown(r_m[live]):.2f}",
    )


def check_parameter_search(report: CheckReport, u: Universe) -> None:
    """Part 5: in-sample selection over 24 rules, a walk-forward, and estimation windows."""
    print("== part 5: parameter search, in-sample selection and walk-forward evaluation")
    ret = u.ret
    lookbacks = list(range(1, 13))
    signals: dict[int, Floats] = {}
    for L in lookbacks:
        s = np.full((T, N), np.nan)
        for t in range(L + 1, T):
            s[t] = np.nanprod(1 + ret[t - L - 1 : t - 1], axis=0) - 1
        signals[L] = np.where(np.isnan(ret), np.nan, s)
    series = {L: RULE.book(signals[L], ret)[0] for L in lookbacks}
    for L in lookbacks:
        series[-L] = -series[L]  # also try the reversed (contrarian) rule: 24 trials in total
    half = T // 2
    is_sharpe = {k: annualised_sharpe(v[:half]) for k, v in series.items()}
    best = max(is_sharpe, key=is_sharpe.__getitem__)
    oos_best = annualised_sharpe(series[best][half:])
    emax = math.sqrt(2 * math.log(len(series))) - (
        math.log(math.log(len(series))) + math.log(4 * math.pi)
    ) / (2 * math.sqrt(2 * math.log(len(series))))
    report.ok(
        "choosing the best of 24 rules on the first 10 years gives an in-sample Sharpe ratio near"
        " the expected maximum of 24 null strategies, and it does not survive the second 10 years",
        is_sharpe[best] > 0.3 and oos_best < is_sharpe[best] - 0.3,
        f"best rule {best}: in-sample {is_sharpe[best]:.2f}, out-of-sample {oos_best:.2f};"
        f" expected max of 24 nulls about {emax / math.sqrt(half / 12):.2f}",
    )
    wf_returns: list[float] = []
    for year in range(10, 20):
        start, end = year * 12, (year + 1) * 12
        # rolling 5-year window
        trail = {k: annualised_sharpe(v[start - 60 : start]) for k, v in series.items()}
        k_star = max(trail, key=trail.__getitem__)
        wf_returns.extend(series[k_star][start:end])
    wf = np.array(wf_returns)
    report.ok(
        "a walk-forward that re-selects the rule each year from the trailing five years only, and"
        " records the following year, has a Sharpe ratio near zero: the honest estimate for a"
        " search over noise",
        abs(annualised_sharpe(wf)) < 0.6,
        f"walk-forward Sharpe {annualised_sharpe(wf):.2f}",
    )
    exp_mean = [np.nanmean(series[6][:t]) for t in range(60, T, 12)]
    roll_mean = [np.nanmean(series[6][t - 60 : t]) for t in range(60, T, 12)]
    report.ok(
        "expanding windows give estimates that change slowly and use all past data; 5-year rolling"
        " windows adapt faster but vary more",
        bool(np.std(np.diff(exp_mean)) < np.std(np.diff(roll_mean))),
    )


def main() -> int:
    """Print the version, simulate the universe, then run the five parts with one report.

    The universe is synthetic, simulated with a fixed seed: 300 stocks over 240 months, returns
    with no true cross-sectional predictability, and delisting after very poor cumulative
    performance. Nothing here is evidence about real markets; the point is to show how each
    backtest error manufactures performance from noise.

    Procedures compared: a survivor-only universe against the point-in-time universe; a signal
    using information available at the decision against one using the same month's return
    (look-ahead); gross against net-of-cost returns with traded notional measured; parameter
    choice by in-sample Sharpe against a walk-forward that chooses on trailing data only and is
    evaluated on the following year; expanding against rolling estimation windows.

    Book and cost conventions (part 3) are those of TradingLedger: a long-short target is +1 of
    NAV long and -1 short (gross exposure 2, net 0); targets are fractions of post-trade NAV; at
    the start of each month last month's positions, after their own returns, are traded to the
    targets and the fee is c times the traded notional. The book is established from cash, so the
    first month pays for building it; a position in a name that delists is sold at its last
    value. Costs are measured from traded notional, not as a quarter of the change in target
    weights costed at 2c (half the cost of the traded notional, ignoring drift), which part 3
    reports for contrast; drawdowns start from the initial wealth of 1, unlike a peak that starts
    after the first return, which part 4 reports for contrast.

    Independent routes: the equal-weighted point-in-time return against the cross-sectional mean
    of the simulated returns; hand-reconciled small ledgers (establishment from cash, unchanged
    targets after unequal returns, a long-short swap) against the ledger, with cash + positions =
    NAV after every trade; the simulated net growth against (post-fee NAV / pre-trade NAV) x
    (1 + w* . r) month by month; the fee against c times the traded notional recomputed from the
    ledger; maximum drawdown from the running peak including the initial wealth of 1 against an
    explicit search over all pairs of dates on the same path; the expected maximum Sharpe of N
    independent null strategies against the in-sample winner.

    One check is one executed ok() call (a call inside a loop counts once per iteration). One
    generator, seeded SEED, simulates the universe once before part 1; parts 1, 2, 3 and 5 share
    that universe, and part 4 measures part 3's momentum book.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}")
    report = CheckReport()
    universe = Universe.simulate(np.random.default_rng(SEED), months=T, stocks=N)
    check_survivorship(report, universe)
    check_look_ahead(report, universe)
    book = check_costs(report, universe)
    check_metrics(report, book)
    check_parameter_search(report, universe)
    print(f"\n{report.count} checks executed")
    if report.failures:
        print("FAILED:", report.failures)
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
