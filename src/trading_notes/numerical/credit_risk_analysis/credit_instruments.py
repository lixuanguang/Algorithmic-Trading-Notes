"""Credit instruments: priority of claims, a risky bond, CDS legs and mortgage pass-throughs."""

from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]


def absolute_priority_recovery(value: float, classes: list[tuple[str, float]]) -> dict[str, float]:
    """Return each class's recovery rate when the value pays the claims in order of priority."""
    out: dict[str, float] = {}
    for name, claim in classes:
        paid = min(value, claim)
        out[name] = paid / claim
        value -= paid
    return out


def tranche_loss(loss: float, attach: float, detach: float) -> float:
    """Return the fraction of a tranche between attachment and detachment that a loss wipes out."""
    return min(max(loss - attach, 0.0), detach - attach) / (detach - attach)


class RiskyBondValue(Record):
    """A risky bond's default-free value and its expected loss, year by year.

    Attributes:
        default_free_value: The bond discounted at the risk-free rate.
        exposure: The bond's value just before each payment, discounted to that date.
        default_probability: The unconditional probability of default in each year.
        loss_given_default: Exposure less the recovery in each year.
        credit_value_adjustment: The present value of the expected losses.
    """

    default_free_value: float
    exposure: Floats
    default_probability: Floats
    loss_given_default: Floats
    credit_value_adjustment: float


class RiskyBond(Record):
    """An annual-pay bond that can default just before each payment, recovering a share of par.

    Attributes:
        hazard: The constant annual default probability conditional on survival.
        recovery: The recovery rate as a share of par.
        rate: The risk-free rate, annual compounding.
        coupon: The annual coupon per 100 of par.
        years: The maturity in years.
    """

    hazard: float
    recovery: float
    rate: float
    coupon: float
    years: int

    def value(self) -> RiskyBondValue:
        """Return the default-free value and the expected loss from defaults."""
        t = np.arange(1, self.years + 1)
        cfs = np.full(self.years, self.coupon)
        cfs[-1] += 100.0
        df = (1 + self.rate) ** -t
        vnd = (cfs * df).sum()
        exposure = np.array(
            [(cfs[i:] * (1 + self.rate) ** -(t[i:] - t[i])).sum() for i in range(self.years)]
        )
        s_prev = (1 - self.hazard) ** (t - 1)
        pod = self.hazard * s_prev
        lgd = exposure - self.recovery * 100.0
        cva = (lgd * pod * df).sum()
        return RiskyBondValue(
            default_free_value=float(vnd),
            exposure=np.asarray(exposure, dtype=np.float64),
            default_probability=np.asarray(pod, dtype=np.float64),
            loss_given_default=np.asarray(lgd, dtype=np.float64),
            credit_value_adjustment=float(cva),
        )


class CreditDefaultSwap(Record):
    """A CDS valued with defaults at mid-period and continuous discounting.

    Attributes:
        rate: The risk-free rate, continuously compounded.
        recovery: The recovery rate R.
        maturity: T, in years.
        frequency: Premium payments a year.
    """

    rate: float
    recovery: float
    maturity: float
    frequency: int

    def legs(self, hazard: Callable[[float], float]) -> tuple[float, float]:
        """Return the premium leg per unit spread, accrual included, and the protection leg.

        Args:
            hazard: The hazard rate at time t, evaluated at each period's midpoint.
        """
        r, freq = self.rate, self.frequency
        n = round(self.maturity * freq)
        dt = 1.0 / freq
        t = np.arange(1, n + 1) * dt
        cumh = np.cumsum([hazard(ti - dt / 2) * dt for ti in t])
        S = np.exp(-cumh)
        S_prev = np.concatenate([[1.0], S[:-1]])
        q = S_prev - S
        tm = t - dt / 2
        prem = (S * np.exp(-r * t) * dt).sum()
        acc = (q * np.exp(-r * tm) * dt / 2).sum()
        prot = (q * (1 - self.recovery) * np.exp(-r * tm)).sum()
        return float(prem + acc), float(prot)


class MortgagePool(Record):
    """A level-payment mortgage pool passed through to investors.

    Attributes:
        balance: The pool balance at the start.
        wac: The weighted-average coupon, annual.
        pass_through_rate: The coupon paid to investors, annual.
        wam: The weighted-average remaining term in months.
        age: The pool's age in months at the start.
    """

    balance: float
    wac: float
    pass_through_rate: float
    wam: int
    age: int

    def cash_flows(self, psa: float) -> Floats:
        """Return the month-by-month cash flows at a PSA speed (1.0 is 100% PSA).

        Columns: month, opening balance, SMM, mortgage payment, net interest, scheduled principal,
        prepayment, total principal.
        """
        rows = []
        bal = self.balance
        m = self.wac / 12
        for kk in range(1, self.wam + 1):
            age = self.age + kk
            cpr = psa * 0.06 * min(age, 30) / 30
            smm = 1 - (1 - cpr) ** (1 / 12)
            n = self.wam - kk + 1
            pay = bal * m / (1 - (1 + m) ** -n)
            sched = pay - bal * m
            prep = smm * (bal - sched)
            rows.append(
                (kk, bal, smm, pay, bal * self.pass_through_rate / 12, sched, prep, sched + prep)
            )
            bal -= sched + prep
        return np.array(rows)


def sequential_payoff_months(cash_flows: Floats, pars: list[float]) -> list[int | None]:
    """Return the month each sequential-pay class is retired, principal paid in class order.

    Args:
        cash_flows: A pool's monthly cash flows, as MortgagePool.cash_flows returns them.
        pars: The classes' par amounts, most senior first.
    """
    rem = list(pars)
    payoff: list[int | None] = [None] * len(pars)
    for kk, prin in zip(cash_flows[:, 0], cash_flows[:, 7], strict=True):
        for j in range(len(rem)):
            if rem[j] > 1e-6:
                xx = min(prin, rem[j])
                rem[j] -= xx
                prin -= xx
                if rem[j] <= 1e-6:
                    payoff[j] = int(kk)
                if prin <= 1e-9:
                    break
    return payoff
