"""Country risk premiums by default spread, relative volatility and the melded approach."""

from fractions import Fraction

from trading_notes.records import Record


class CountryRisk[T: (float, Fraction)](Record):
    """A country's sovereign default spread and market volatilities, in percent.

    Every premium keeps the type of the inputs, so a run in Fraction never passes through
    floating point.

    Attributes:
        spread: Sovereign default spread.
        sd_equity: Standard deviation of the country's equity market.
        sd_bond: Standard deviation of its government bond.
    """

    spread: T
    sd_equity: T
    sd_bond: T

    def default_spread_premium(self) -> T:
        """Return the country premium as the sovereign default spread."""
        return self.spread

    def melded_premium(self) -> T:
        """Return the default spread scaled by equity over bond volatility."""
        return self.spread * self.sd_equity / self.sd_bond

    def relative_sd_premium(self, mature_erp: T, sd_mature: T) -> T:
        """Return ERP sd_equity / sd_mature - ERP for the mature market's ERP and volatility."""
        return mature_erp * self.sd_equity / sd_mature - mature_erp
