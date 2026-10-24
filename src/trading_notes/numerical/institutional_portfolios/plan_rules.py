"""Pension surplus risk and minimum funding, and endowment spending against NPC 553(d)."""

import math
from typing import Literal

import numpy as np

from trading_notes.numerical.records import Record


def annuity(r: float, n: float) -> float:
    """Return the present value of an end-of-year annuity of 1 for n years at rate r."""
    discount: float = (1 + r) ** -n
    return (1 - discount) / r


def annuity_due(n: int, r: float) -> float:
    """Return the annuity-due factor: n level installments, the first on the valuation date."""
    return annuity(r, n) * (1 + r) if n > 0 else 0.0


class PensionPlan(Record):
    """A defined benefit plan's assets and liabilities exposed to equities and one rate factor.

    Attributes:
        assets: Plan assets.
        liabilities: The liability (PBO).
        liability_duration: Its duration.
        equity_vol: Equity volatility.
        rate_vol: The annual volatility of the discount rate.
        equity_rate_correlation: Equity returns against rate changes.
    """

    assets: float
    liabilities: float
    liability_duration: float
    equity_vol: float
    rate_vol: float
    equity_rate_correlation: float = -0.2

    def surplus_vol(self, w_eq: float, d_bond: float) -> float:
        """Return the annual surplus volatility with equity weight w_eq, the rest in bonds.

        Args:
            w_eq: The equity weight of the assets.
            d_bond: The duration of the bonds held.
        """
        rho = self.equity_rate_correlation  # rates up -> both bonds and equities lower
        w_b = 1 - w_eq
        # dollar exposures to (equity return, rate change)
        a_eq = self.assets * w_eq
        a_rate = -self.assets * w_b * d_bond
        l_rate = -self.liabilities * self.liability_duration
        cov = np.array(
            [
                [self.equity_vol**2, rho * self.equity_vol * self.rate_vol],
                [rho * self.equity_vol * self.rate_vol, self.rate_vol**2],
            ]
        )
        x = np.array([a_eq, a_rate - l_rate])  # surplus = assets - liabilities
        return math.sqrt(x @ cov @ x)


class MinimumContribution(Record):
    """The minimum required contribution and the pieces of its shortfall charge.

    Attributes:
        contribution: Target normal cost plus the shortfall charge (not below zero).
        new_base: This year's shortfall amortisation base.
        pv_old: The present value of the installments still due on earlier bases.
        old_installments: This year's installments on earlier bases.
    """

    contribution: float
    new_base: float
    pv_old: float
    old_installments: float


class MinimumFunding(Record):
    """IRC 430's minimum funding, one effective rate standing in for the segment rates.

    Installments fall on the valuation date of each plan year.

    Attributes:
        rate: The effective interest rate.
        years: The amortisation period of each shortfall base (15 under 430(c)(8)).
        plan_year: The plan year being valued.
    """

    rate: float
    years: int
    plan_year: int

    def installment_factor(self, n: int | None = None) -> float:
        """Return the annuity-due factor of n installments (the full period by default)."""
        return annuity_due(self.years if n is None else n, self.rate)

    def required(
        self, assets: float, ft: float, tnc: float, prior: dict[int, float]
    ) -> MinimumContribution:
        """Return the minimum under 430(a) and (c) given the bases set in earlier plan years.

        Args:
            assets: The value of plan assets.
            ft: The funding target.
            tnc: The target normal cost.
            prior: Each earlier plan year's base.
        """
        if (
            assets >= ft
        ):  # 430(a)(2), (c)(5)-(6): no new base, earlier bases zeroed, TNC less the excess
            return MinimumContribution(
                contribution=max(0.0, tnc - (assets - ft)),
                new_base=0.0,
                pv_old=0.0,
                old_installments=0.0,
            )
        full = self.installment_factor()
        inst = {y: b / full for y, b in prior.items()}
        # installments still due, this year's included
        left = {y: self.years - (self.plan_year - y) for y in prior}
        pv_old = sum(inst[y] * self.installment_factor(left[y]) for y in prior)
        new_base = (ft - assets) - pv_old  # 430(c)(3): shortfall less PV of existing installments
        charge = max(0.0, sum(inst.values()) + new_base / full)  # 430(c)(1): not less than zero
        return MinimumContribution(
            contribution=tnc + charge,
            new_base=new_base,
            pv_old=pv_old,
            old_installments=sum(inst.values()),
        )


class SpendingPath(Record):
    """Spending over value year by year, and the quarter-end values behind the averages.

    Attributes:
        current: Spending over the year's opening value.
        average: Spending over the NPC 553(d) five-year average of quarter-end values.
        quarters: Every quarter-end value, the prior history first.
    """

    current: list[float]
    average: list[float]
    quarters: list[float]


class SpendingRule(Record):
    """An endowment spending rule, run on its own asset path.

    Attributes:
        rule: "pure" spends the rate times value; "smoothed" 70% of last year's spending grown
            with inflation plus 30% of the rate times value.
        value: The opening value.
        rate: The spending rate.
        inflation: The inflation the smoothed rule grows spending with.
    """

    rule: Literal["pure", "smoothed"]
    value: float
    rate: float
    inflation: float

    def path(self, returns: list[float], prior: list[float] | None = None) -> SpendingPath:
        """Return the rule's spending ratios and quarter-end values over the returns.

        Each rule's quarter-end values come from its own spending. `prior` holds the 20
        quarter-end values before the simulation (assumed flat at the opening value).
        """
        quarters = list(prior) if prior is not None else [self.value] * 20
        mv, sp, cur, avg = self.value, self.rate * self.value, [], []
        for rr in returns:
            sp = (
                self.rate * mv
                if self.rule == "pure"
                else 0.7 * sp * (1 + self.inflation) + 0.3 * self.rate * mv
            )
            # NPC 553(d): quarterly values averaged over the five preceding years
            avg5 = sum(quarters[-20:]) / 20
            cur.append(sp / mv)
            avg.append(sp / avg5)
            start = mv - sp
            quarters += [start * (1 + rr) ** (q / 4) for q in range(1, 5)]
            mv = start * (1 + rr)
        return SpendingPath(current=cur, average=avg, quarters=quarters)
