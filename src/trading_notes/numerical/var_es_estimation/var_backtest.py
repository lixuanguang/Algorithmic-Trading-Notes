"""Historical and filtered historical simulation VaR, backtested on a GARCH(1,1)-t path."""

import math

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]
type Hits = NDArray[np.bool_]


class GarchPath(Record):
    """One simulated GARCH(1,1)-t path.

    Attributes:
        returns: r_t, one per day.
        variances: sigma2_t, the variance r_t was drawn with, known at t - 1.
    """

    returns: Floats
    variances: Floats


class GarchT(Record):
    """GARCH(1,1) variance sigma2_{t+1} = omega + alpha r_t^2 + beta sigma2_t with Student-t shocks.

    Attributes:
        omega: Constant of the variance recursion.
        alpha: Weight on the squared return.
        beta: Weight on the previous variance.
        nu: Degrees of freedom of the shocks, scaled to unit variance.
    """

    omega: float
    alpha: float
    beta: float
    nu: int

    def simulate(self, rng: np.random.Generator, days: int) -> GarchPath:
        """Simulate `days` returns from the long-run variance omega / (1 - alpha - beta).

        All shocks are drawn at once and scaled by sqrt(nu / (nu - 2)).
        """
        z = rng.standard_t(self.nu, days) / math.sqrt(self.nu / (self.nu - 2))
        s2 = np.empty(days)
        r = np.empty(days)
        s2[0] = self.omega / (1 - self.alpha - self.beta)
        for t in range(days):
            r[t] = math.sqrt(s2[t]) * z[t]
            if t + 1 < days:
                s2[t + 1] = self.omega + self.alpha * r[t] ** 2 + self.beta * s2[t]
        return GarchPath(returns=r, variances=s2)


class Violations(Record):
    """Each method's VaR violations on the backtest days, in day order.

    Attributes:
        hs: Historical Simulation violations.
        fhs: Filtered Historical Simulation violations.
    """

    hs: Hits
    fhs: Hits


class VaRBacktest(Record):
    """A rolling-window backtest of HS and FHS VaR.

    Attributes:
        window: Days of history behind each VaR.
        p: VaR tail probability.
    """

    window: int
    p: float

    def run(self, path: GarchPath) -> Violations:
        """Backtest both methods on every day from `window` on.

        Day t's VaR uses days t - window to t - 1 only, with np.quantile's default (linear)
        interpolation. HS takes the p-quantile of those returns. FHS takes the p-quantile of the
        same returns divided by their own sigma_t, then scales it by day t's sigma_t, known the
        day before. A violation is a return strictly below -VaR.
        """
        r, s2, window, p = path.returns, path.variances, self.window, self.p
        days = len(r) - window
        hs = np.empty(days, dtype=np.bool_)
        fhs = np.empty(days, dtype=np.bool_)
        for i, t in enumerate(range(window, len(r))):
            past = r[t - window : t]
            var_hs = -np.quantile(past, p)
            zq = np.quantile(past / np.sqrt(s2[t - window : t]), p)
            var_fhs = -math.sqrt(s2[t]) * zq
            hs[i] = r[t] < -var_hs
            fhs[i] = r[t] < -var_fhs
        return Violations(hs=hs, fhs=fhs)


def unconditional_coverage(hits: Hits, p: float) -> float:
    """Return Christoffersen's unconditional coverage statistic LR_uc, chi2(1) under the null.

    Applied as written: with no violations, or only violations, a log of zero raises
    ValueError; no clipping or pseudocount is added.

    Args:
        hits: The violation indicators, one per backtest day.
        p: The VaR tail probability.
    """
    T1 = int(hits.sum())
    T0 = len(hits) - T1
    pi = T1 / len(hits)
    return -2 * (
        T0 * math.log(1 - p) + T1 * math.log(p) - T0 * math.log(1 - pi) - T1 * math.log(pi)
    )


def rate_after_violation(hits: Hits) -> float:
    """Return the violation rate on days that follow a violation.

    Without a violation before the last day this is the mean of no days: NumPy warns and
    returns nan.
    """
    return float(hits[1:][hits[:-1]].mean())
