"""A household's human capital, policy portfolio, goals and longevity, in real terms."""

import math

from trading_notes.records import Record


class MarketAssumptions(Record):
    """Real capital market assumptions for a stock-bond mix.

    Attributes:
        mu_e: Equity expected arithmetic return.
        sd_e: Equity volatility.
        mu_b: Bond expected arithmetic return.
        sd_b: Bond volatility.
        rho: Their correlation.
    """

    mu_e: float
    sd_e: float
    mu_b: float
    sd_b: float
    rho: float

    def mix(self, w_eq: float) -> tuple[float, float, float, float]:
        """Return the mix arithmetic mean, volatility, compound real return and its 5% quantile.

        The compound return is median-adjusted for a lognormal return.
        """
        m = w_eq * self.mu_e + (1 - w_eq) * self.mu_b
        sd = math.sqrt(
            (w_eq * self.sd_e) ** 2
            + ((1 - w_eq) * self.sd_b) ** 2
            + 2 * w_eq * (1 - w_eq) * self.rho * self.sd_e * self.sd_b
        )
        s2 = math.log(1 + sd**2 / (1 + m) ** 2)
        ml = math.log(1 + m) - s2 / 2
        return m, sd, math.exp(ml) - 1, math.exp(ml - 1.645 * math.sqrt(s2)) - 1


class HumanCapital(Record):
    """After-tax real earnings from age 40, growing until retirement.

    Attributes:
        earnings: Earnings at 40.
        growth: Annual real earnings growth.
        rate: The discount rate.
        retirement: The retirement age.
    """

    earnings: float
    growth: float
    rate: float
    retirement: int

    def value(self, age: int) -> float:
        """Return the PV at `age` of earnings from then to retirement."""
        g, r = self.growth, self.rate
        e = self.earnings * (1 + g) ** (age - 40)
        return sum(
            e * (1 + g) ** (t - 1) / (1 + r) ** t for t in range(1, self.retirement - age + 1)
        )


class GoalsPlan(Record):
    """A policy portfolio funding education payments and retirement spending.

    Saving and education payments fall at year-ends; retirement spending is valued at the
    horizon.

    Attributes:
        policy: The goal-funding policy portfolio today.
        save: Planned saving at each year-end until the horizon.
        years: The horizon, the retirement date.
        education: (years from now, payment) of each education payment.
        retirement_need: The PV at the horizon of retirement spending less Social Security.
    """

    policy: float
    save: float
    years: int
    education: tuple[tuple[int, float], ...]
    retirement_need: float

    def project(self, rr: float, years: int | None = None) -> float:
        """Return the policy portfolio after `years` (the horizon by default) at return rr."""
        x = self.policy
        for t in range(1, (self.years if years is None else years) + 1):
            x = x * (1 + rr) + self.save - sum(c for tt, c in self.education if tt == t)
        return x

    def funded_gap(self, rr: float, p0: float | None = None) -> float:
        """Return the surplus at the horizon for return rr, after education and retirement."""
        years = self.years
        p = self.policy if p0 is None else p0
        fv_assets = p * (1 + rr) ** years + sum(
            self.save * (1 + rr) ** (years - t) for t in range(1, years + 1)
        )
        fv_edu = sum(c * (1 + rr) ** (years - t) for t, c in self.education)
        return fv_assets - fv_edu - self.retirement_need

    def funded_ratio(self, d: float, save: float | None = None) -> tuple[float, float, float]:
        """Return PV of resources, PV of goals and their ratio at discount rate d."""
        sv = self.save if save is None else save
        res_ = self.policy + sum(sv / (1 + d) ** t for t in range(1, self.years + 1))
        goals_ = (
            sum(c / (1 + d) ** t for t, c in self.education)
            + self.retirement_need / (1 + d) ** self.years
        )
        return res_, goals_, res_ / goals_


class Gompertz(Record):
    """A Gompertz mortality law.

    Attributes:
        mode: The modal age at death.
        dispersion: The dispersion b.
    """

    mode: float
    dispersion: float

    def survival(self, x: float, t: float) -> float:
        """Return the probability that a person aged x survives t more years."""
        return math.exp(
            math.exp((x - self.mode) / self.dispersion) * (1 - math.exp(t / self.dispersion))
        )
