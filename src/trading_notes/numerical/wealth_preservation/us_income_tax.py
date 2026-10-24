"""US federal income tax of a married couple filing jointly: bands, preferential rates and NIIT."""

import itertools
import math

from trading_notes.records import Record


class TaxReturn(Record):
    """A household's federal income tax for one year.

    Attributes:
        agi: Adjusted gross income (equal to MAGI here).
        ti: Taxable income.
        ord: Ordinary taxable income, excluding dividends and gains.
        tax: Regular tax.
        niit: Net investment income tax.
        at0: Preferential income taxed at 0%.
        at15: ... at 15%.
        at20: ... at 20%.
    """

    agi: float
    ti: float
    ord: float
    tax: float
    niit: float
    at0: float
    at15: float
    at20: float


class JointIncomeTax(Record):
    """The joint-return rate schedule, the preferential rate amounts and the NIIT.

    Attributes:
        brackets: (lower edge of the band, rate), from zero.
        zero_max: The maximum zero rate amount.
        fifteen_max: The maximum 15% rate amount.
        standard_deduction: The standard deduction.
        niit_threshold: The MAGI threshold of the NIIT (sec. 1411(b)(1), not indexed).
        niit_rate: The NIIT rate.
    """

    brackets: tuple[tuple[float, float], ...]
    zero_max: float
    fifteen_max: float
    standard_deduction: float
    niit_threshold: float
    niit_rate: float

    def ordinary(self, ti: float) -> float:
        """Return the regular tax on taxable income ti from the bands."""
        edges = [*self.brackets, (math.inf, 0.0)]  # the open top band's rate is unused
        return sum(
            rate * max(0.0, min(ti, hi) - lo) for (lo, rate), (hi, _) in itertools.pairwise(edges)
        )

    def capital_gains(self, ti: float, ancg: float) -> tuple[float, float, float, float]:
        """Return sec. 1(h)(1)(A)-(D), as modified by 1(j)(5), on the adjusted net capital gain.

        Qualified dividends are included (sec. 1(h)(11)); no unrecaptured 1250 or collectibles
        gain.

        Returns:
            The tax, and the amounts taxed at 0%, 15% and 20%.
        """
        ancg = min(ancg, ti)
        a = ti - ancg  # (A): taxable income reduced by the gain, taxed at ordinary rates
        b = min(ancg, max(0.0, self.zero_max - a))  # (B): 0% up to the maximum zero rate amount
        c = min(ancg - b, max(0.0, self.fifteen_max - (a + b)))  # (C): 15% up to the 15% amount
        d = ancg - b - c  # (D): 20% on the rest
        return min(self.ordinary(a) + 0.15 * c + 0.20 * d, self.ordinary(ti)), b, c, d

    def stacked(self, ti: float, pref: float) -> float:
        """Return the tax with ordinary income filling the bands first, an independent route.

        Each preferential dollar from ti - pref to ti is taxed at the rate of the layer it
        occupies, integrated piece by piece.
        """
        tax, lo = self.ordinary(ti - pref), ti - pref
        for top, rate in ((self.zero_max, 0.0), (self.fifteen_max, 0.15), (math.inf, 0.20)):
            hi = min(ti, top)
            if hi > lo:
                tax += rate * (hi - lo)
                lo = hi
        return tax

    def household(
        self,
        wages: float = 650_000.0,
        deferral: float = 49_000.0,
        interest: float = 2_400.0,
        qdiv: float = 6_000.0,
        ltcg: float = 60_000.0,
    ) -> TaxReturn:
        """Return the household's tax and NIIT; state and payroll taxes are ignored.

        The defaults are the Okafors' 2026 income.
        """
        agi = wages - deferral + interest + qdiv + ltcg  # MAGI = AGI: no foreign income excluded
        ti = agi - self.standard_deduction
        tax, at0, at15, at20 = self.capital_gains(ti, qdiv + ltcg)
        niit = self.niit_rate * min(interest + qdiv + ltcg, max(0.0, agi - self.niit_threshold))
        return TaxReturn(
            agi=agi, ti=ti, ord=ti - qdiv - ltcg, tax=tax, niit=niit, at0=at0, at15=at15, at20=at20
        )
