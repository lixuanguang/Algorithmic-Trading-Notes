"""Leland's adjusted volatilities and a simulation of delta hedging with transaction costs."""

import math

import numpy as np
from numpy.typing import NDArray
from pydantic import Field
from scipy import stats

from trading_notes.numerical.option_pricing.black_scholes import BlackScholes
from trading_notes.records import MutableRecord, Record

type Floats = NDArray[np.float64]


def call_delta(rate: float, S: Floats, K: float, tau: Floats, vol: float) -> Floats:
    """Return the BSM call delta (no dividends) at each price, tau broadcast along the time axis."""
    return stats.norm.cdf((np.log(S / K) + (rate + vol**2 / 2) * tau) / (vol * np.sqrt(tau)))


class Ledger(MutableRecord):
    """One position's per-path results at K = 0.1, N = 52, appended block by block.

    Attributes:
        id_err: The largest relative error of the ledger identity so far.
        test: Discounted gains plus s(discounted payoff - V), whose mean the identity sets to 0.
        pnl: Discounted terminal wealth at the Leland price.
        opening: The opening trade's cost.
        cash_close: The discounted cost of a cash-settled close instead of delivery.
        settle: The discounted cost of the settlement trade.
    """

    id_err: float = 0.0
    test: list[Floats] = Field(default_factory=list)
    pnl: list[Floats] = Field(default_factory=list)
    opening: list[Floats] = Field(default_factory=list)
    cash_close: list[Floats] = Field(default_factory=list)
    settle: list[Floats] = Field(default_factory=list)


class FixedHedge(MutableRecord):
    """The short call hedged at sigma with kappa = 0.2 percent, on one grid, block by block.

    Attributes:
        cost: Each path's present value of costs.
        pnl: Each path's discounted P&L at the BSM premium.
    """

    cost: list[Floats] = Field(default_factory=list)
    pnl: list[Floats] = Field(default_factory=list)


class SpreadCosts(MutableRecord):
    """Part 3's costs of hedging a bull spread's legs separately and netted, block by block.

    Attributes:
        sep: Each path's present value of the separately hedged legs' costs.
        agg: The same with the legs' trades netted.
        step_ok: Whether netting never cost more, at every step of every path so far.
        same_ok: Whether long and short the same call netted to zero cost, at twice one leg apart.
    """

    sep: list[Floats] = Field(default_factory=list)
    agg: list[Floats] = Field(default_factory=list)
    step_ok: bool = True
    same_ok: bool = True


class Simulation(Record):
    """What the simulation accumulates.

    Attributes:
        cost_acc: The sum and the sum of squares of the costs' present values, by
            (sign, K, N).
        ledger: Per-path results by position sign.
        fixed: Per-path results of the fixed-kappa hedge by grid.
        spread: The call-spread demonstration's costs.
    """

    cost_acc: dict[tuple[int, float, int], list[float]]
    ledger: dict[int, Ledger]
    fixed: dict[int, FixedHedge]
    spread: SpreadCosts


class LelandExperiment(Record):
    """A call hedged on nested rebalancing grids with proportional costs, on common paths.

    Trading nu shares at S costs kappa |nu| S. Position sign s = +1 is long and -1 short one
    call; the stock holding is -s times the BSM delta at the position's Leland volatility
    (sigma_check long, sigma_hat short); cash grows at r and pays trades and costs; settlement
    is physical, so the last, costed trade moves the holding to the payoff delta. The
    simulation is risk neutral (mu = r) with no dividends.

    Attributes:
        spot: Initial stock price.
        strike: Strike of the call.
        sigma: Volatility of the stock.
        rate: Continuously compounded rate.
        maturity: Years to expiry.
        n_paths: Paths simulated.
        n_fine: Steps of the finest grid; the coarser grids take every few fine dates.
        block: Paths drawn at a time.
        grids: Rebalancing grids, as numbers of steps.
        cases: (position sign, Leland number K) pairs hedged on every grid.
    """

    spot: float
    strike: float
    sigma: float
    rate: float
    maturity: float
    n_paths: int
    n_fine: int
    block: int
    grids: tuple[int, ...]
    cases: tuple[tuple[int, float], ...]

    def leland_variance(self, kappa: float, dt: float, sign: int) -> float:
        """Return sigma_hat^2 (sign +1, short) or sigma_check^2 (sign -1, long), eqs. 48.5-48.6.

        sigma^2 +/- 2 kappa sigma sqrt(2 / (pi dt)); it can be negative for a long position.
        """
        return self.sigma**2 + sign * 2 * kappa * self.sigma * math.sqrt(2 / (math.pi * dt))

    def simulate(self, rng: np.random.Generator) -> Simulation:
        """Simulate the paths in blocks and hedge every case on every grid, on the same paths.

        Each block draws one normal per fine step and path; the coarser grids take every 4th or
        16th fine date.
        """
        r, sig, n_fine = self.rate, self.sigma, self.n_fine
        S0, KS, T = self.spot, self.strike, self.maturity
        CASES, GRIDS, BLOCK = self.cases, self.grids, self.block
        cost_acc = {(s, K, n): [0.0, 0.0] for s, K in CASES for n in GRIDS}
        ledger = {s: Ledger() for s in (-1, +1)}
        fixed = {n: FixedHedge() for n in GRIDS}
        spread = SpreadCosts()
        for _ in range(self.n_paths // BLOCK):
            z = rng.standard_normal((BLOCK, n_fine))
            dtf = T / n_fine
            S = np.empty((BLOCK, n_fine + 1))
            S[:, 0] = S0
            S[:, 1:] = S0 * np.exp(
                np.cumsum((r - sig**2 / 2) * dtf + sig * math.sqrt(dtf) * z, axis=1)
            )
            for n in GRIDS:
                Sk = S[:, :: n_fine // n]
                dt = T / n
                # Float64 dates: the integers convert exactly, as they would in the product.
                t = np.arange(n + 1, dtype=np.float64) * dt
                disc = np.exp(-r * t)
                itm = (Sk[:, -1] > KS).astype(float)
                for s, K in CASES:
                    kappa = K * sig * math.sqrt(dt)
                    # short (s = -1) uses sigma_hat, long sigma_check
                    vol = math.sqrt(self.leland_variance(kappa, dt, -s))
                    delta = np.empty_like(Sk)
                    delta[:, :-1] = call_delta(r, Sk[:, :-1], KS, T - t[:-1], vol)
                    delta[:, -1] = itm
                    h = -s * delta
                    nu = np.diff(h, axis=1)
                    cost = kappa * Sk[:, 1:] * np.abs(nu)
                    pv_cost = cost @ disc[1:]
                    cost_acc[(s, K, n)][0] += pv_cost.sum()
                    cost_acc[(s, K, n)][1] += (pv_cost**2).sum()
                    if n == 52 and K == 0.1:
                        led = ledger[s]
                        V = BlackScholes(spot=S0, strike=KS, maturity=T, rate=r, vol=sig).call()
                        P = BlackScholes(spot=S0, strike=KS, maturity=T, rate=r, vol=vol).call()
                        cash = -s * P - h[:, 0] * S0
                        for k in range(1, n + 1):
                            cash = (
                                cash * math.exp(r * dt) - nu[:, k - 1] * Sk[:, k] - cost[:, k - 1]
                            )
                        lhs = math.exp(-r * T) * (cash + h[:, -1] * Sk[:, -1])
                        gains = (h[:, :-1] * np.diff(Sk * disc, axis=1)).sum(axis=1)
                        rhs = -s * P + gains - pv_cost
                        led.id_err = max(
                            led.id_err, float(np.max(np.abs(lhs - rhs) / (1 + np.abs(lhs))))
                        )
                        payoff = np.maximum(Sk[:, -1] - KS, 0)
                        W = lhs + s * math.exp(-r * T) * payoff  # discounted terminal wealth
                        led.test.append(gains + s * (math.exp(-r * T) * payoff - V))
                        led.pnl.append(W)
                        led.opening.append(kappa * np.abs(h[:, 0]) * S0)
                        led.cash_close.append(
                            math.exp(-r * T) * kappa * np.abs(h[:, -2]) * Sk[:, -1]
                        )
                        led.settle.append(math.exp(-r * T) * cost[:, -1])
                # fixed kappa = 0.2 percent: short call hedged with BSM deltas at sigma, premium V
                delta = np.empty_like(Sk)
                delta[:, :-1] = call_delta(r, Sk[:, :-1], KS, T - t[:-1], sig)
                delta[:, -1] = itm
                h = delta
                nu = np.diff(h, axis=1)
                pv_cost = (0.002 * Sk[:, 1:] * np.abs(nu)) @ disc[1:]
                gains = (h[:, :-1] * np.diff(Sk * disc, axis=1)).sum(axis=1)
                V = BlackScholes(spot=S0, strike=KS, maturity=T, rate=r, vol=sig).call()
                fixed[n].cost.append(pv_cost)
                fixed[n].pnl.append(
                    V + gains - pv_cost - math.exp(-r * T) * np.maximum(Sk[:, -1] - KS, 0)
                )
                if n == 52:
                    # part 3: bull spread, long K1 = 95, short K2 = 105, BSM deltas at sigma,
                    # kappa = 0.2 percent
                    legs = []
                    for Kl, sl in ((95.0, +1), (105.0, -1)):
                        dl = np.empty_like(Sk)
                        dl[:, :-1] = call_delta(r, Sk[:, :-1], Kl, T - t[:-1], sig)
                        dl[:, -1] = (Sk[:, -1] > Kl).astype(float)
                        legs.append(np.diff(-sl * dl, axis=1))
                    c_sep = 0.002 * Sk[:, 1:] * (np.abs(legs[0]) + np.abs(legs[1]))
                    c_agg = 0.002 * Sk[:, 1:] * np.abs(legs[0] + legs[1])
                    spread.step_ok &= bool((c_agg <= c_sep + 1e-12).all())
                    spread.sep.append(c_sep @ disc[1:])
                    spread.agg.append(c_agg @ disc[1:])
                    # long and short the same call: net holding zero
                    nu_long = np.diff(-delta, axis=1)
                    nu_short = np.diff(delta, axis=1)
                    agg_same = (0.002 * Sk[:, 1:] * np.abs(nu_long + nu_short)) @ disc[1:]
                    sep_same = (0.002 * Sk[:, 1:] * (np.abs(nu_long) + np.abs(nu_short))) @ disc[1:]
                    single = (0.002 * Sk[:, 1:] * np.abs(nu_short)) @ disc[1:]
                    spread.same_ok &= bool(
                        (agg_same == 0).all() and (np.abs(sep_same - 2 * single) <= 1e-12).all()
                    )
        return Simulation(cost_acc=cost_acc, ledger=ledger, fixed=fixed, spread=spread)
