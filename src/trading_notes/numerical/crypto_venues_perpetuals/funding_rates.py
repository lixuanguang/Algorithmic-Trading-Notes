"""Deribit's perpetual funding rate: a damper band around zero, then symmetric caps."""

from trading_notes.records import Record


def premium_rate(mark: float, index: float) -> float:
    """Return the premium of mark over index in percent."""
    return (mark - index) / index * 100.0


class FundingRule(Record):
    """The funding rate of a premium rate, both in percent per 8 hours.

    The printed closed form and an independent piecewise reading of the prose rule are kept as
    separate routes, so each can be checked against the other.

    Attributes:
        damper: The half-width of the band in which the rate is zero, in percent.
    """

    damper: float = 0.025

    def closed_form(self, premium: float, cap: float) -> float:
        """Deribit's formula: Min(MaxCap, Max(MinCap, Max(0.025%, P) + Min(-0.025%, P)))."""
        d = self.damper
        return min(cap, max(-cap, max(d, premium) + min(-d, premium)))

    def piecewise(self, premium: float, cap: float) -> float:
        """Deribit's prose: zero inside the band, else shrink towards zero by the damper; cap."""
        d = self.damper
        if -d <= premium <= d:
            raw = 0.0
        elif premium > d:
            raw = premium - d
        else:
            raw = premium + d
        return min(cap, max(-cap, raw))
