"""Delta hedging a call at the actual or the implied volatility when the two differ."""

import math

import numpy as np
from numpy.typing import NDArray
from scipy import stats

from trading_notes.records import MutableRecord, Record

type Floats = NDArray[np.float64]


class VanillaCall(Record):
    """A European call under BSM, valued at a price or an array of prices.

    Attributes:
        strike: Strike price.
        maturity: Years to expiry.
        rate: Continuously compounded rate.
        dividend_yield: Continuous dividend yield.
    """

    strike: float
    maturity: float
    rate: float
    dividend_yield: float

    def d12[X: (float, Floats)](self, S: X, tau: float, vol: float) -> tuple[X, X]:
        """Return BSM's d1 and d2 for the call, at a price or an array of prices."""
        d1: X = (np.log(S / self.strike) + (self.rate - self.dividend_yield + vol**2 / 2) * tau) / (
            vol * np.sqrt(tau)
        )
        return d1, d1 - vol * np.sqrt(tau)

    def price[X: (float, Floats)](self, S: X, tau: float, vol: float) -> X:
        """Return the BSM call value."""
        d1, d2 = self.d12(S, tau, vol)
        value: X = S * np.exp(-self.dividend_yield * tau) * stats.norm.cdf(
            d1
        ) - self.strike * np.exp(-self.rate * tau) * stats.norm.cdf(d2)
        return value

    def delta[X: (float, Floats)](self, S: X, tau: float, vol: float) -> X:
        """Return the BSM call delta."""
        value: X = np.exp(-self.dividend_yield * tau) * stats.norm.cdf(self.d12(S, tau, vol)[0])
        return value

    def gamma[X: (float, Floats)](self, S: X, tau: float, vol: float) -> X:
        """Return the BSM gamma."""
        value: X = (
            np.exp(-self.dividend_yield * tau)
            * stats.norm.pdf(self.d12(S, tau, vol)[0])
            / (S * vol * np.sqrt(tau))
        )
        return value


class CashDigital(Record):
    """A unit cash-or-nothing call under BSM with no dividends.

    Attributes:
        strike: Strike price.
        maturity: Years to expiry.
        rate: Continuously compounded rate.
    """

    strike: float
    maturity: float
    rate: float

    def d12(self, S: float, vol: float) -> tuple[float, float]:
        """Return d1 and d2 for the cash digital."""
        d1 = (math.log(S / self.strike) + (self.rate + vol**2 / 2) * self.maturity) / (
            vol * math.sqrt(self.maturity)
        )
        return d1, d1 - vol * math.sqrt(self.maturity)

    def value(self, S: float, vol: float) -> float:
        """Return the unit cash-or-nothing call's value."""
        return math.exp(-self.rate * self.maturity) * stats.norm.cdf(self.d12(S, vol)[1])

    def gamma(self, S: float, vol: float) -> float:
        """Return the cash digital's gamma in closed form."""
        d1, d2 = self.d12(S, vol)
        return (
            -math.exp(-self.rate * self.maturity)
            * stats.norm.pdf(d2)
            * d1
            / (S**2 * vol**2 * self.maturity)
        )


class Hedge(MutableRecord):
    """One delta hedge's running position, rebalanced every `every` fine steps.

    Attributes:
        every: Fine steps between rebalancing dates.
        vol: The volatility the deltas are computed at.
        delta: Shares held short, one per path.
        cash: The cash account, one per path.
    """

    every: int
    vol: float
    delta: Floats
    cash: Floats


class Simulation(Record):
    """The hedges' discounted P&L and the implied-delta hedge's pathwise integrals.

    Attributes:
        pnl: Present value of each path's P&L, by (grid, "a" or "i" for the hedging volatility).
        integral: The left-point Riemann sum of the pathwise integral, by grid.
    """

    pnl: dict[tuple[str, str], Floats]
    integral: dict[str, Floats]


class MismatchExperiment(Record):
    """A call bought at implied volatility and delta hedged while the stock moves at another.

    The stock follows dS = mu S dt + sigma_a S dW; the call is marked at the implied
    volatility; the hedge is short delta shares with cash at r and no costs, on a fine grid and
    on a coarse one that uses every few fine dates.

    Attributes:
        call: The option.
        spot: Initial stock price.
        drift: Actual drift mu.
        actual_vol: Actual volatility sigma_a.
        implied_vol: Implied volatility.
        n_paths: Paths simulated.
        n_fine: Fine rebalancing dates.
        coarse_every: Fine dates per coarse rebalancing.
    """

    call: VanillaCall
    spot: float
    drift: float
    actual_vol: float
    implied_vol: float
    n_paths: int
    n_fine: int
    coarse_every: int

    def simulate(self, rng: np.random.Generator, Vi: float) -> Simulation:
        """Hedge the call bought at Vi on common paths: both grids, both hedging volatilities.

        One normal vector per fine step drives every hedge, so the four share their paths.
        """
        T, R, K = self.call.maturity, self.call.rate, self.call.strike
        S0, MU, SIG_A, SIG_I = self.spot, self.drift, self.actual_vol, self.implied_vol
        N_PATHS, N_FINE, COARSE_EVERY = self.n_paths, self.n_fine, self.coarse_every
        dt = T / N_FINE
        S = np.full(N_PATHS, S0)
        hedges: dict[tuple[str, str], Hedge] = {}
        integral: dict[str, Floats] = {}
        for name, every in (("fine", 1), ("coarse", COARSE_EVERY)):
            for hedge_vol in ("a", "i"):
                vol = SIG_A if hedge_vol == "a" else SIG_I
                d = self.call.delta(S, T, vol)
                hedges[(name, hedge_vol)] = Hedge(every=every, vol=vol, delta=d, cash=-Vi + d * S)
            integral[name] = np.zeros(N_PATHS)
        for k in range(N_FINE):
            t = k * dt
            for name, every in (("fine", 1), ("coarse", COARSE_EVERY)):
                # left-point Riemann sum of the pathwise integral for the implied-delta hedge
                if k % every == 0:
                    h = every * dt
                    integral[name] += (
                        0.5
                        * (SIG_A**2 - SIG_I**2)
                        * math.exp(-R * t)
                        * S**2
                        * self.call.gamma(S, T - t, SIG_I)
                        * h
                    )
            S = S * np.exp(
                (MU - SIG_A**2 / 2) * dt + SIG_A * math.sqrt(dt) * rng.standard_normal(N_PATHS)
            )
            t_new = (k + 1) * dt
            for st in hedges.values():
                st.cash = st.cash * math.exp(R * dt)
                if (k + 1) % st.every == 0 and k + 1 < N_FINE:
                    new_delta = self.call.delta(S, T - t_new, st.vol)
                    st.cash += (new_delta - st.delta) * S
                    st.delta = new_delta
        payoff = np.maximum(S - K, 0)
        pnl = {
            key: math.exp(-R * T) * (payoff - st.delta * S + st.cash) for key, st in hedges.items()
        }
        return Simulation(pnl=pnl, integral=integral)
