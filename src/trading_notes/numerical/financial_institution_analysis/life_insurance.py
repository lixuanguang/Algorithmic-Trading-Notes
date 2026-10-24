"""Life-insurance liabilities under Gompertz mortality: Solvency II and new-business value."""

from typing import overload

import numpy as np
from numpy.typing import NDArray

from trading_notes.records import Record

type Floats = NDArray[np.float64]
type Ages = NDArray[np.intp] | Floats


class LifeTable(Record):
    """Gompertz mortality q_x = base exp(slope x), capped at one, and a flat risk-free rate.

    Attributes:
        base: The mortality rate at age 0.
        slope: The Gompertz growth rate per year of age.
        rate: The flat annual risk-free rate.
    """

    base: float
    slope: float
    rate: float

    @overload
    def mortality(self, age: float, mult: float = 1.0) -> float: ...
    @overload
    def mortality(self, age: Ages, mult: float = 1.0) -> Floats: ...
    def mortality(self, age: float | Ages, mult: float = 1.0) -> float | Floats:
        """Return q_x scaled by mult, for one age or an array of ages."""
        if isinstance(age, np.ndarray):
            rates: Floats = np.minimum(1.0, mult * self.base * np.exp(self.slope * age))
            return rates
        return float(np.minimum(1.0, mult * self.base * np.exp(self.slope * age)))

    def survival(self, age0: int, n: int, mult: float = 1.0) -> tuple[Floats, Floats]:
        """Return the survival probabilities at the start of each of n years and the q_x."""
        qs = self.mortality(age0 + np.arange(n), mult)
        return np.concatenate([[1.0], np.cumprod(1 - qs)[:-1]]), qs

    def discount(self, n: int, r: float | None = None) -> Floats:
        """Return the discount factors for years 1 to n, at the risk-free rate unless r is given."""
        rate = self.rate if r is None else r
        return np.asarray((1 + rate) ** -np.arange(1, n + 1), dtype=np.float64)


class SolvencyPosition(Record):
    """A life insurer's Solvency II balance sheet and standard-formula life and market risk.

    Attributes:
        annuity: Best estimate of the annuities.
        term: Best estimate of the term policies (claims less premiums).
        savings: Best estimate of the savings policies.
        best_estimate: Total best estimate.
        own_funds: Assets less best estimate and risk margin.
        rates_up: Change in own funds when rates rise by 50 bp.
        rates_down: Change in own funds when rates fall by 50 bp.
        longevity: Best-estimate increase under the longevity shock (mortality -20%).
        mortality: Best-estimate increase under the mortality shock (+15%).
        lapse: The mass-lapse loss (40% of the surrender strain).
        life_scr: The life SCR, the three shocks aggregated.
        scr: The SCR, life and market aggregated.
        ratio: Own funds / SCR.
    """

    annuity: float
    term: float
    savings: float
    best_estimate: float
    own_funds: float
    rates_up: float
    rates_down: float
    longevity: float
    mortality: float
    lapse: float
    life_scr: float
    scr: float
    ratio: float


class LifeBook(Record):
    """A life insurer's annuities from age 65, term policies at ages 45-64 and savings.

    Shocks follow Delegated Regulation (EU) 2015/35 Arts. 137 (mortality +15%), 138 (longevity
    -20%) and 142(6)(b) (mass lapse 40%); correlations Art. 136 and Directive 2009/138/EC
    Annex IV (life-market 0.25). Assets are bonds of one duration revalued at the shocked rate.

    Attributes:
        table: Mortality and the risk-free rate.
        pension: Annual annuity payment, at year ends to survivors from 65 for 46 years.
        sum_assured: Term-policy claim, at the end of the year of death.
        premium: Term premium, in advance, ages 45-64.
        guarantee: Savings payment due in 10 years.
        surrender_value: Savings surrender value today.
        assets: Asset value.
        asset_term: The assets' term in years.
        risk_margin: The risk margin, an input.
    """

    table: LifeTable
    pension: float
    sum_assured: float
    premium: float
    guarantee: float
    surrender_value: float
    assets: float
    asset_term: int
    risk_margin: float = 40.0

    def annuity_value(self, r: float | None = None, mult: float = 1.0, n: int = 46) -> float:
        """Return the best estimate of the annuities paid at year ends to survivors from 65."""
        s_, q_ = self.table.survival(65, n, mult)
        return float(np.sum(self.pension * s_ * (1 - q_) * self.table.discount(n, r)))

    def term_value(self, r: float | None = None, mult: float = 1.0, n: int = 20) -> float:
        """Return the best estimate of the term policies: claims less premiums in advance."""
        rate = self.table.rate if r is None else r
        s_, q_ = self.table.survival(45, n, mult)
        d_ = self.table.discount(n, r)
        return float(
            np.sum(self.sum_assured * s_ * q_ * d_) - np.sum(self.premium * s_ * d_ * (1 + rate))
        )

    def savings_value(self, r: float | None = None, years: int = 10) -> float:
        """Return the present value of the savings guarantee."""
        return self.guarantee / (1 + (self.table.rate if r is None else r)) ** years

    def best_estimate(
        self, r: float | None = None, annuity_mult: float = 1.0, term_mult: float = 1.0
    ) -> float:
        """Return the total best estimate at rate r with the two mortality multipliers."""
        return (
            self.annuity_value(r, annuity_mult)
            + self.term_value(r, term_mult)
            + self.savings_value(r)
        )

    def solvency(self) -> SolvencyPosition:
        """Return the Solvency II position: best estimates, shocks, life SCR and SCR."""
        r_f = self.table.rate
        corr_life = np.array([[1, -0.25, 0.0], [-0.25, 1, 0.25], [0.0, 0.25, 1]])

        def assets_at(r: float) -> float:
            return self.assets * ((1 + r_f) / (1 + r)) ** self.asset_term

        b0 = self.best_estimate()
        own_funds = self.assets - b0 - self.risk_margin
        up = (assets_at(r_f + 0.005) - self.best_estimate(r_f + 0.005)) - (self.assets - b0)
        dn = (assets_at(r_f - 0.005) - self.best_estimate(r_f - 0.005)) - (self.assets - b0)
        mkt = max(0.0, -up, -dn)
        longev = self.best_estimate(annuity_mult=0.8) - b0
        mort = self.best_estimate(term_mult=1.15) - b0
        lapse = 0.4 * max(self.surrender_value - self.savings_value(), 0.0)
        v = np.array([max(mort, 0.0), max(longev, 0.0), lapse])
        life = float(np.sqrt(v @ corr_life @ v))
        scr = float(np.sqrt(life**2 + mkt**2 + 2 * 0.25 * life * mkt))
        return SolvencyPosition(
            annuity=self.annuity_value(),
            term=self.term_value(),
            savings=self.savings_value(),
            best_estimate=b0,
            own_funds=own_funds,
            rates_up=up,
            rates_down=dn,
            longevity=longev,
            mortality=mort,
            lapse=lapse,
            life_scr=life,
            scr=scr,
            ratio=own_funds / scr,
        )


class NewBusinessValue(Record):
    """The present value of a new cohort of term business at issue.

    Attributes:
        pvnbp: Present value of new-business premiums.
        claims: Present value of claims.
        expenses: Present value of expenses.
        profit: Premiums less claims and expenses.
        risk_adjustment: The IFRS 17 risk adjustment.
        csm: The contractual service margin.
        loss: The day-one loss of an onerous group.
        vnb: The value of new business after tax and the cost of capital.
    """

    pvnbp: float
    claims: float
    expenses: float
    profit: float
    risk_adjustment: float
    csm: float
    loss: float
    vnb: float


class TermCohort(Record):
    """A cohort of term policies written at age 45 for 20 years, priced with a loading.

    Attributes:
        table: Mortality and the risk-free rate.
        sum_assured: The claim on death.
        loading: The premium loading over the expected claims.
        acquisition: Acquisition cost at issue.
        expense_rate: Maintenance expenses as a share of premiums.
        tax: Tax rate.
        cost_of_capital: Cost-of-capital rate on the mortality SCR.
        risk_adjustment_rate: Risk adjustment as a share of claims.
        years: Policy term.
    """

    table: LifeTable
    sum_assured: float
    loading: float
    acquisition: float = 5.0
    expense_rate: float = 0.03
    tax: float = 0.25
    cost_of_capital: float = 0.06
    risk_adjustment_rate: float = 0.05
    years: int = 20

    def value(self) -> NewBusinessValue:
        """Return the cohort's present values, CSM or loss, and value of new business."""
        n, r_f = self.years, self.table.rate
        s_, q_ = self.table.survival(45, n)
        d_ = self.table.discount(n)
        claims = self.sum_assured * s_ * q_
        P = (1 + self.loading) * np.sum(claims * d_) / np.sum(s_ * d_ * (1 + r_f))
        pv_claims = float(np.sum(claims * d_))
        pvnbp = float(np.sum(P * s_ * d_ * (1 + r_f)))
        pv_exp = self.acquisition + self.expense_rate * pvnbp
        s2, q2 = self.table.survival(45, n, 1.15)
        scr_new = float(np.sum(self.sum_assured * s2 * q2 * d_)) - pv_claims
        remaining = np.array(
            [np.sum(claims[t_:] * (1 + r_f) ** -(np.arange(t_, n) - t_ + 1)) for t_ in range(n)]
        )
        coc_cost = self.cost_of_capital * scr_new * float(np.sum(remaining / remaining[0] * d_))
        ra = self.risk_adjustment_rate * pv_claims
        profit = pvnbp - pv_claims - pv_exp
        return NewBusinessValue(
            pvnbp=pvnbp,
            claims=pv_claims,
            expenses=pv_exp,
            profit=profit,
            risk_adjustment=ra,
            csm=max(profit - ra, 0.0),
            loss=max(ra - profit, 0.0),
            vnb=profit * (1 - self.tax) - coc_cost,
        )
