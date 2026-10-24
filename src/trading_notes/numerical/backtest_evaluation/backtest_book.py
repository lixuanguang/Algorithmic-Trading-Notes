"""A simulated equity universe and a long-short book traded through a cash ledger with costs."""

import math
from collections.abc import Sequence
from typing import Self

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]
type Bools = NDArray[np.bool_]


class Universe(Record):
    """A point-in-time universe of monthly stock returns.

    Attributes:
        ret: Monthly returns, months by stocks; NaN once a stock has delisted.
        alive: Whether each stock is listed in each month.
    """

    ret: Floats
    alive: Bools

    @classmethod
    def simulate(cls, rng: np.random.Generator, months: int, stocks: int) -> Self:
        """Simulate returns with no cross-sectional predictability, delisting after a 75% loss.

        Returns are a market factor with uniform betas in [0.7, 1.3] plus independent noise;
        a stock that has lost 75 percent of its value is delisted from the next month on.
        """
        mkt = rng.normal(0.006, 0.045, months)
        beta = rng.uniform(0.7, 1.3, stocks)
        ret = mkt[:, None] * beta[None, :] + rng.normal(0, 0.09, (months, stocks))
        alive = np.ones((months, stocks), dtype=bool)
        level = np.ones(stocks)
        for t in range(months):
            level *= 1 + np.where(alive[t], ret[t], 0.0)
            dead = level < 0.25
            if t + 1 < months:
                alive[t + 1 :, dead] = False
        return cls(ret=np.where(alive, ret, np.nan), alive=alive)


def annualised_sharpe(x: Floats) -> float:
    """Return the annualised Sharpe ratio of monthly returns, ignoring NaN."""
    x = x[~np.isnan(x)]
    return float(np.mean(x) / np.std(x, ddof=1) * math.sqrt(12))


def max_drawdown(r: Sequence[float] | Floats) -> float:
    """Return the maximum drawdown of the wealth path that starts at 1 before the first return."""
    wealth = np.concatenate([[1.0], np.cumprod(1 + np.asarray(r, dtype=float))])
    peak = np.maximum.accumulate(wealth)
    return float(np.max(1 - wealth / peak))


class LongShortRule(Record):
    """Equal weight long the top fraction and short the bottom fraction of names by signal.

    Attributes:
        fraction: k, the share of names on each side.
        minimum_names: Fewer names with both a signal and a return leave the month in cash.
    """

    fraction: float = 0.2
    minimum_names: int = 20

    def book(self, signal: Floats, rets: Floats) -> tuple[Floats, Floats]:
        """Return the target book's monthly gross returns and its target weights.

        The book is rebalanced to target at each month's start, without costs, among names with
        both a signal and a return. Target weights are fractions of post-trade NAV; a zero row
        means cash, and its month's return is NaN.
        """
        out, targets = np.full(len(rets), np.nan), np.zeros(rets.shape)
        for t in range(len(rets)):
            s, r_ = signal[t], rets[t]
            ok_ = ~np.isnan(s) & ~np.isnan(r_)
            if ok_.sum() < self.minimum_names:
                continue
            idx = np.where(ok_)[0]
            order = idx[np.argsort(s[idx])]
            m = max(1, int(self.fraction * len(order)))
            targets[t, order[-m:]] = 1 / m
            targets[t, order[:m]] = -1 / m
            out[t] = float(np.sum(targets[t, ok_] * r_[ok_]))
        return out, targets


class Trade(Record):
    """One rebalancing of a book.

    Attributes:
        holdings: Signed holdings after the trade, in currency.
        cash: Cash after the trade and the fee.
        fee: The fee paid.
        traded: Traded notional, purchases plus sales.
    """

    holdings: Floats
    cash: float
    fee: float
    traded: float


class LedgerRun(Record):
    """A book's monthly ledger.

    Attributes:
        net: Net monthly returns; NaN before the first trade.
        traded_fraction: Traded notional as a fraction of pre-trade NAV.
        fees: Fees paid each month.
        worst_gap: The largest |cash + positions - NAV| seen after any trade.
    """

    net: Floats
    traded_fraction: Floats
    fees: Floats
    worst_gap: float


class TradingLedger(Record):
    """A cash ledger that trades a book to target weights and pays a fee on traded notional.

    NAV is cash plus the signed market value of the positions. Short-sale proceeds stay in
    cash; cash, collateral and short rebates earn zero and there is no borrow fee or margin, so
    returns are excess-of-cash returns.

    Attributes:
        cost: c, the fee per unit of traded notional, purchases and sales alike.
    """

    cost: float

    def rebalance(self, h: Floats, cash: float, w_star: Floats) -> Trade:
        """Trade signed holdings h to target weights w_star of post-trade NAV.

        Post-trade NAV is NAV less the fee, so the fee solves f = c sum|w* (V - f) - h|, a
        contraction when c times gross exposure is below 1, found by iteration.
        """
        v_pre = cash + h.sum()
        fee = 0.0
        for _ in range(50):
            fee_new = self.cost * np.abs(w_star * (v_pre - fee) - h).sum()
            if abs(fee_new - fee) < 1e-15:
                break
            fee = fee_new
        h_new = w_star * (v_pre - fee)
        traded = np.abs(h_new - h).sum()
        # purchases use cash; sales and short sales raise it
        cash_new = cash - (h_new - h).sum() - fee
        return Trade(holdings=h_new, cash=cash_new, fee=fee, traded=traded)

    def run(self, targets: Floats, rets: Floats, v0: float = 1.0) -> LedgerRun:
        """Start in cash, trade to each month's targets, then earn that month's returns.

        A position in a name that delists earns nothing after the trade, as if sold at its last
        value.
        """
        h, cash, v = np.zeros(targets.shape[1]), v0, v0
        net = np.full(len(rets), np.nan)
        traded_frac, fees = np.zeros(len(rets)), np.zeros(len(rets))
        started, worst = False, 0.0
        for t in range(len(rets)):
            if targets[t].any() or h.any():
                trade = self.rebalance(h, cash, targets[t])
                h, cash = trade.holdings, trade.cash
                worst = max(worst, abs(cash + h.sum() - (v - trade.fee)))
                traded_frac[t], fees[t] = trade.traded / v, trade.fee
                started = True
            h = h * (1 + np.nan_to_num(rets[t]))
            v_new = cash + h.sum()
            if started:
                net[t] = v_new / v - 1
            v = v_new
        return LedgerRun(net=net, traded_fraction=traded_frac, fees=fees, worst_gap=worst)
