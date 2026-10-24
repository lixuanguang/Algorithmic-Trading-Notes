"""One-period cross-currency basis swap: the forward it implies and the basis a forward implies."""

from trading_notes.records import Record


class CrossCurrencySwap(Record):
    """A one-period EUR/USD swap with simple-interest legs at assumed fixings.

    Attributes:
        spot: USD per EUR today.
        usd_rate: The dollar leg's rate.
        eur_rate: The euro leg's rate, before any spread.
    """

    spot: float
    usd_rate: float
    eur_rate: float

    def forward(self, t: float, kappa: float) -> float:
        """Return the forward, USD paid per EUR received at t, with spread kappa on the euro leg."""
        return self.spot * (1 + self.usd_rate * t) / (1 + (self.eur_rate + kappa) * t)

    def dollar_basis(self, F: float, t: float) -> float:
        """Return the annualised basis b on the dollar leg implied by the forward F over t."""
        return ((F / self.spot) * (1 + self.eur_rate * t) - (1 + self.usd_rate * t)) / t
