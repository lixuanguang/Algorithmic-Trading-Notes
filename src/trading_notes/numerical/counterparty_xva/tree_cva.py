"""CVA of bonds, swaps and floaters on a calibrated binomial short-rate tree (Handbook chap. 36)."""

import itertools
import math
from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray
from scipy import optimize

from trading_notes.records import Record

type Floats = NDArray[np.float64]


class DefaultRisk(Record):
    """A counterparty's default risk: an annual piecewise-constant hazard and a recovery rate.

    Attributes:
        hazard: The hazard rate of each year 1..n.
        recovery: The share of the claim recovered on default.
    """

    hazard: tuple[float, ...]
    recovery: float

    def survival(self, n: int) -> list[float]:
        """Return the survival probabilities to dates 0..n."""
        return [math.exp(-sum(self.hazard[:t])) for t in range(n + 1)]


class ShortRateTree(Record):
    """A recombining binomial tree of one-year rates, one-half probability per branch.

    Attributes:
        rates: The one-year rates at dates 0..n-1; date t holds t + 1 nodes, lowest first.
    """

    rates: tuple[Floats, ...]

    @classmethod
    def calibrate(cls, par: Sequence[float], sigma: float) -> ShortRateTree:
        """Return the lognormal tree whose lowest rates price each annual par bond at 100.

        Args:
            par: The annual par yields of maturities 1..n, as decimals.
            sigma: The volatility; adjacent nodes differ by the factor exp(2 sigma).
        """
        rates: list[Floats] = [np.array([par[0]])]
        for n in range(2, len(par) + 1):
            cpn = 100 * par[n - 1]

            def price(r_low: float) -> float:
                tree = [*rates, r_low * np.exp(2 * sigma * np.arange(n))]
                val = np.full(n + 1, 100 + cpn)
                for t in range(n - 1, -1, -1):
                    val = 0.5 * (val[:-1] + val[1:]) / (1 + tree[t]) + (cpn if t > 0 else 0)
                return float(val[0]) - 100

            rates.append(
                optimize.brentq(price, 1e-6, 0.5, xtol=1e-15, rtol=1e-15)
                * np.exp(2 * sigma * np.arange(n))
            )
        return cls(rates=tuple(rates))

    @property
    def periods(self) -> int:
        """Return the number of one-year periods n."""
        return len(self.rates)

    def state_prices(self) -> list[Floats]:
        """Return Arrow-Debreu prices AD[t][j] of a unit paid at node (t, j), dates 0..n."""
        ad: list[Floats] = [np.array([1.0])]
        for t, rate in enumerate(self.rates):
            nxt = np.zeros(t + 2)
            nxt[:-1] += 0.5 * ad[t] / (1 + rate)
            nxt[1:] += 0.5 * ad[t] / (1 + rate)
            ad.append(nxt)
        return ad

    def bond_values(self, cpn: float) -> list[Floats]:
        """Return the ex-coupon value of an n-year bond paying cpn per 100 at each node."""
        n = self.periods
        vals: list[Floats] = [np.zeros(0)] * (n + 1)
        vals[n] = np.zeros(n + 1)
        nxt = np.full(n + 1, 100 + cpn)
        for t in range(n - 1, -1, -1):
            vals[t] = 0.5 * (nxt[:-1] + nxt[1:]) / (1 + self.rates[t])
            nxt = vals[t] + cpn
        return vals

    def floater_values(self, margin: float, dm: float = 0.0) -> list[Floats]:
        """Return ex-coupon floater values; the coupon (r_t + margin) x 100 is paid at t + 1.

        Args:
            margin: The quoted margin over the tree rate, as a decimal.
            dm: The discount margin added to the tree rate when discounting.
        """
        n = self.periods
        vals: list[Floats] = [np.zeros(0)] * (n + 1)
        vals[n] = np.zeros(n + 1)
        nxt = np.full(n + 1, 100.0)
        for t in range(n - 1, -1, -1):
            rate = self.rates[t]
            up = nxt[1:] + 100 * (rate + margin)
            dn = nxt[:-1] + 100 * (rate + margin)
            vals[t] = 0.5 * (up + dn) / (1 + rate + dm)
            nxt = vals[t]
        return vals

    def bond_cva(self, cpn: float, risk: DefaultRisk) -> float:
        """Return a bond's CVA, with default just before each date-t payment."""
        n = self.periods
        vals, ad = self.bond_values(cpn), self.state_prices()
        surv = risk.survival(n)
        return sum(
            (surv[t - 1] - surv[t])
            * float(ad[t] @ (vals[t] + cpn + (100 if t == n else 0) - risk.recovery * 100))
            for t in range(1, n + 1)
        )

    def bond_path_cva(self, cpn: float, risk: DefaultRisk) -> float:
        """Return the bond's CVA by listing all 2^n paths and discounting the loss on each."""
        n = self.periods
        vals = self.bond_values(cpn)
        surv = risk.survival(n)
        total = 0.0
        for path in itertools.product((0, 1), repeat=n):
            j, disc_f, pv = 0, 1.0, 0.0
            for t in range(1, n + 1):
                disc_f /= 1 + self.rates[t - 1][j]
                j += path[t - 1]
                expo = vals[t][j] + cpn + (100 if t == n else 0)
                pv += (surv[t - 1] - surv[t]) * disc_f * (expo - risk.recovery * 100)
            total += pv / 2**n
        return total

    def swap_cva(self, fixed_rate: float, risk: DefaultRisk) -> float:
        """Return the unilateral CVA of a payer swap, with loss (1 - R) max(V, 0)."""
        n = self.periods
        fixed, ad = self.bond_values(100 * fixed_rate), self.state_prices()
        surv = risk.survival(n)
        out = 0.0
        for t in range(1, n + 1):
            v_ex = 100 - fixed[t] if t < n else np.zeros(n + 1)  # floating leg ex-coupon is par
            parent_rates = self.rates[t - 1]
            pv = 0.0
            for p_node in range(t):
                w = ad[t - 1][p_node] * 0.5 / (1 + parent_rates[p_node])
                net = 100 * (parent_rates[p_node] - fixed_rate)  # due at t, set at the parent
                pv += w * (max(v_ex[p_node] + net, 0) + max(v_ex[p_node + 1] + net, 0))
            out += (surv[t - 1] - surv[t]) * (1 - risk.recovery) * pv
        return out

    def floater_cva(self, margin: float, risk: DefaultRisk) -> float:
        """Return a floater's CVA, weighting its coupons and value by state prices and survival."""
        n = self.periods
        vals, ad = self.floater_values(margin), self.state_prices()
        surv = risk.survival(n)
        out = 0.0
        for t in range(1, n + 1):
            parent_rates = self.rates[t - 1]
            coupon = 100 * (parent_rates + margin)  # set at the parent node at t - 1, paid at t
            # exposure at child (t, j): its ex-coupon value plus the coupon set at its parent(s)
            cpn_child = np.zeros(t + 1)
            w = np.zeros(t + 1)
            cpn_child[:-1] += ad[t - 1] * 0.5 / (1 + parent_rates) * coupon
            cpn_child[1:] += ad[t - 1] * 0.5 / (1 + parent_rates) * coupon
            w[:-1] += ad[t - 1] * 0.5 / (1 + parent_rates)
            w[1:] += ad[t - 1] * 0.5 / (1 + parent_rates)
            red = 100 if t == n else 0
            pv_expo = float(cpn_child.sum() + w @ (vals[t] + red))
            out += (surv[t - 1] - surv[t]) * (pv_expo - risk.recovery * 100 * float(ad[t].sum()))
        return out
