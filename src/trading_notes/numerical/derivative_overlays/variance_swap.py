"""Mark-to-market value of a seasoned variance swap on daily zero-mean log returns."""

import numpy as np

from trading_notes.records import Record


class SeasonedVarianceSwap(Record):
    """A variance swap on N daily log returns, valued after n of them have been observed.

    Realised variance is RV = scale (A / N) sum r_i^2, zero mean; the payoff at expiry is
    variance_notional (RV - variance_strike). After n returns the value is
    variance_notional P(t, T) [scale (A / N) sum_{i<=n} r_i^2 + ((N - n) / N) K_rem
    - variance_strike], where K_rem is the fair strike of the remaining N - n returns.

    Attributes:
        n_returns: N, the returns in the contract.
        annualisation: A, returns a year.
        variance_notional: Payoff per unit of variance (per point squared in points).
        variance_strike: K_var, in the same variance units as RV.
        scale: Variance units per unit of decimal variance: 1e4 for points, 1 for decimals.
        rate: Continuously compounded discount rate.
    """

    n_returns: int
    annualisation: int
    variance_notional: float
    variance_strike: float
    scale: float
    rate: float

    def value(self, sum_sq_realised: float, n_obs: int, k_rem: float, tau: float) -> float:
        """Return the seasoned value.

        Args:
            sum_sq_realised: The sum of squared returns observed so far (empty sum = 0).
            n_obs: The number of returns observed so far.
            k_rem: The fair strike of the remaining returns, in the swap's variance units.
            tau: The time to expiry in years.
        """
        N, A = self.n_returns, self.annualisation
        disc = np.exp(-self.rate * tau)
        return float(
            self.variance_notional
            * disc
            * (
                self.scale * A / N * sum_sq_realised
                + (N - n_obs) / N * k_rem
                - self.variance_strike
            )
        )
