"""A leveraged buyout's debt paydown by cash sweep, and its equity at entry and exit."""

from collections.abc import Sequence

from trading_notes.records import Record


class LboYear(Record):
    """One year of the buyout.

    Attributes:
        ebitda: EBITDA.
        cash_int: Cash interest paid.
        debt: Debt outstanding at year end.
    """

    ebitda: float
    cash_int: float
    debt: float


class LboResult(Record):
    """The buyout's equity at entry and exit, its multiple and IRR, and the yearly path.

    Attributes:
        eq0: Equity at entry.
        eqx: Equity at exit.
        moic: eqx / eq0.
        irr: The equity IRR with no interim flows.
        path: Each year's EBITDA, interest and debt.
    """

    eq0: float
    eqx: float
    moic: float
    irr: float
    path: list[LboYear]


class LeveragedBuyout(Record):
    """A buyout whose free cash flow sweeps the most senior debt first.

    Unlevered free cash flow is a share of EBITDA; the interest tax shield is added.

    Attributes:
        ebitda: EBITDA at entry.
        fees: Transaction fees, funded by equity.
        entry_multiple: The entry EV / EBITDA.
        exit_multiple: The exit EV / EBITDA.
        growth: Annual EBITDA growth.
        conversion: Unlevered free cash flow as a share of EBITDA.
        tax: The tax rate of the interest shield.
        years: The holding period.
    """

    ebitda: float
    fees: float
    entry_multiple: float
    exit_multiple: float
    growth: float = 0.06
    conversion: float = 0.5
    tax: float = 0.25
    years: int = 5

    def run(self, struct: Sequence[tuple[str, float, float, float]]) -> LboResult:
        """Return the buyout financed by (name, amount, cash rate, PIK rate) in seniority order."""
        debt = {k: a for k, a, _, _ in struct}
        rate = {k: (c, pk) for k, _, c, pk in struct}
        eq0 = self.ebitda * self.entry_multiple + self.fees - sum(debt.values())
        ebitda = self.ebitda
        path: list[LboYear] = []
        for _ in range(self.years):
            ebitda *= 1 + self.growth
            cash_int = sum(debt[k] * rate[k][0] for k in debt)
            pik = sum(debt[k] * rate[k][1] for k in debt)
            free = self.conversion * ebitda + self.tax * (cash_int + pik) - cash_int
            for k in debt:
                debt[k] += debt[k] * rate[k][1]
            for k, *_ in struct:
                pay = min(max(free, 0.0), debt[k])
                debt[k] -= pay
                free -= pay
            path.append(LboYear(ebitda=ebitda, cash_int=cash_int, debt=sum(debt.values())))
        eqx = ebitda * self.exit_multiple - sum(debt.values())
        return LboResult(
            eq0=eq0, eqx=eqx, moic=eqx / eq0, irr=(eqx / eq0) ** (1 / self.years) - 1, path=path
        )
