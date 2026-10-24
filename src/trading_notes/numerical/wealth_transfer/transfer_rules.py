"""Residence tests, Rule 10b5-1 cooling-off, US estate tax and UK inheritance tax relief."""

import datetime

from trading_notes.numerical.records import Record


class PresenceDays(Record):
    """Days present in a country this year and in each of the two years before.

    Attributes:
        current: Days this year.
        previous: Days last year.
        before_previous: Days the year before that.
    """

    current: int
    previous: int = 0
    before_previous: int = 0

    def us_weighted_days(self) -> float:
        """Return the substantial presence count: this year's days, 1/3 and 1/6 of earlier ones."""
        return self.current + self.previous / 3 + self.before_previous / 6

    def us_substantial_presence(self) -> bool:
        """Return whether the US test (s. 7701(b)(3)) is met: 31 days now and 183 weighted."""
        return self.current >= 31 and self.us_weighted_days() >= 183

    def uk_ties_needed(self, resident_recently: bool) -> int | None:
        """Return the UK ties needed this year (RDR3 Tables A and B), or None if no row applies.

        Args:
            resident_recently: Whether UK resident in any of the previous three years (Table A).
        """
        table_a = [(16, 45, 4), (46, 90, 3), (91, 120, 2), (121, 182, 1)]
        table_b = [(46, 90, 4), (91, 120, 3), (121, 182, 2)]
        for lo, hi, k in table_a if resident_recently else table_b:
            if lo <= self.current <= hi:
                return k
        return None


class TradingPlan(Record):
    """An officer's Rule 10b5-1 trading plan.

    Attributes:
        adopted: The adoption date.
    """

    adopted: datetime.date

    def first_trade_date(self, ten_q_filed: datetime.date) -> datetime.date:
        """Return the first trade date under Rule 10b5-1(c)(1)(ii)(B)(1).

        The later of 90 days after adoption and 2 business days after the 10-Q, capped at
        120 days after adoption.
        """
        a = self.adopted + datetime.timedelta(days=90)
        b, k = ten_q_filed, 0
        while k < 2:
            b += datetime.timedelta(days=1)
            if b.weekday() < 5:
                k += 1
        return min(max(a, b), self.adopted + datetime.timedelta(days=120))


class EstateTax(Record):
    """US estate tax as a flat rate above the unified exemption.

    Attributes:
        exemption: The basic exclusion amount.
        rate: The rate above it (the s. 2001(c) top rate).
    """

    exemption: float
    rate: float = 0.40

    def tax(self, taxable: float, exemption_used: float = 0.0) -> float:
        """Return the tax on a taxable estate after lifetime gifts used part of the exemption."""
        return self.rate * max(0.0, taxable - (self.exemption - exemption_used))


class InheritanceTax(Record):
    """UK inheritance tax relief on lifetime gifts and the residence nil-rate band.

    Attributes:
        residence_band: The residence nil-rate band.
        taper_threshold: The estate above which the residence band tapers (IHTA 1984 s. 8D).
    """

    residence_band: float
    taper_threshold: float

    def taper_rate(self, years_before_death: float) -> float:
        """Return the rate on a failed potentially exempt transfer above the nil-rate band."""
        for limit, rate in ((3, 0.40), (4, 0.32), (5, 0.24), (6, 0.16), (7, 0.08)):
            if years_before_death < limit:
                return rate
        return 0.0

    def residence_nil_rate_band(
        self, estate: float, home: float, transferred: float = 0.0
    ) -> float:
        """Return the band: the allowance less 1 per 2 of estate above the threshold.

        The allowance (plus any transferred) is capped at the value of the qualifying home
        passing to direct descendants. `estate` is the net value at death before exemptions and
        reliefs, excluding lifetime gifts.
        """
        adjusted = max(
            0.0, self.residence_band + transferred - max(0.0, estate - self.taper_threshold) / 2
        )
        return min(home, adjusted)
