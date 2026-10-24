"""Simulated delta hedging of a European call under geometric Brownian motion."""

import math

import numpy as np
from numpy.typing import NDArray
from scipy.stats import norm

from trading_notes.numerical.option_pricing.black_scholes import BlackScholes
from trading_notes.records import Record

type Floats = NDArray[np.float64]


class DeltaHedgedCall(Record):
    """A European call on a non-dividend stock, hedged with Black-Scholes deltas.

    Attributes:
        spot: Initial stock price.
        strike: Strike price.
        rate: Continuously compounded risk-free rate.
        vol: Volatility used for pricing and deltas.
        maturity: Time to expiry in years.
    """

    spot: float
    strike: float
    rate: float
    vol: float
    maturity: float

    def option(self, vol: float | None = None) -> BlackScholes:
        """Return the call at inception, at the given volatility or the hedging one."""
        return BlackScholes(
            spot=self.spot,
            strike=self.strike,
            maturity=self.maturity,
            rate=self.rate,
            vol=self.vol if vol is None else vol,
        )

    def writer_cost_ratio(
        self,
        step_weeks: float,
        rng: np.random.Generator,
        n_paths: int = 20_000,
        mu: float = 0.13,
    ) -> tuple[float, float]:
        """Return the s.d. of the PV cost of writing and delta hedging the call, over its price.

        Hull's Table 19.4 measure; the stock drifts at mu. The generator is advanced by one
        normal draw per path and rebalancing date.

        Args:
            step_weeks: Weeks between rebalancing dates; the life is 20 weeks.
            rng: The generator the paths are drawn from.
            n_paths: Number of paths.
            mu: Real-world drift of the stock.

        Returns:
            The s.d. ratio and the mean PV cost.
        """
        S0, K, r, sig, T = self.spot, self.strike, self.rate, self.vol, self.maturity
        n = round(20 / step_weeks)
        dt = T / n
        st = np.full(n_paths, S0)
        dlt = np.array([self.option().call_delta()] * n_paths)
        cost = dlt * st
        for i in range(1, n + 1):
            z = rng.standard_normal(n_paths)
            st = st * np.exp((mu - sig**2 / 2) * dt + sig * math.sqrt(dt) * z)
            cost = cost * math.exp(r * dt)
            new: Floats
            if i < n:
                tau = T - i * dt
                d1v = (np.log(st / K) + (r + sig**2 / 2) * tau) / (sig * math.sqrt(tau))
                new = norm.cdf(d1v)
            else:
                new = (st > K).astype(float)
            cost += (new - dlt) * st
            dlt = new
        cost -= np.where(st > K, K, 0.0)
        pv = cost * math.exp(-r * T)
        return pv.std() / self.option().call(), pv.mean()

    def holder_pnl(
        self, realised_vol: float, rng: np.random.Generator, n_paths: int, n_steps: int
    ) -> Floats:
        """Return the P&L of buying the call and delta hedging it while volatility differs.

        The call is bought and marked at the hedging volatility and hedged every step with
        deltas at that volatility, while the stock moves at `realised_vol` with drift equal to
        the risk-free rate. The cash account accrues interest.

        Args:
            realised_vol: Volatility of the simulated stock.
            rng: The generator the paths are drawn from.
            n_paths: Number of paths.
            n_steps: Number of hedging steps over the life.

        Returns:
            The terminal P&L of each path.
        """
        S0, K, r, sig, T = self.spot, self.strike, self.rate, self.vol, self.maturity
        dtd = T / n_steps
        st = np.full(n_paths, S0)
        c_old = np.full(n_paths, self.option().call())
        dl = np.full(n_paths, self.option().call_delta())
        pnl = np.zeros(n_paths)
        for i in range(n_steps):
            z = rng.standard_normal(n_paths)
            st_new = st * np.exp(
                (r - realised_vol**2 / 2) * dtd + realised_vol * math.sqrt(dtd) * z
            )
            tau2 = T - (i + 1) * dtd
            c_new: Floats
            dl_new: Floats
            if tau2 > 1e-12:
                d1v = (np.log(st_new / K) + (r + sig**2 / 2) * tau2) / (sig * math.sqrt(tau2))
                c_new = st_new * norm.cdf(d1v) - K * math.exp(-r * tau2) * norm.cdf(
                    d1v - sig * math.sqrt(tau2)
                )
                dl_new = norm.cdf(d1v)
            else:
                c_new = np.maximum(st_new - K, 0.0)
                dl_new = np.zeros(n_paths)
            pnl = (
                pnl * math.exp(r * dtd)
                + (c_new - c_old)
                - dl * (st_new - st)
                - (math.exp(r * dtd) - 1) * (c_old - dl * st)
            )
            st, c_old, dl = st_new, c_new, dl_new
        return pnl
