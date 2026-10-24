"""Basel counterparty capital: SA-CCR exposure at default and the reduced basic CVA approach."""

import math
from collections.abc import Sequence
from typing import Final

from trading_notes.records import Record

ALPHA: Final = 1.4
FLOOR: Final = 0.05


class IrTrade(Record):
    """An interest rate trade in an unmargined netting set, as SA-CCR measures it.

    Attributes:
        notional: Trade notional.
        start: S, years to the start of the period the trade references.
        end: E, years to its end.
        maturity: M, remaining maturity in years.
        delta: Supervisory delta, +1 for a trade long the rate (CRE52.39).
    """

    notional: float
    start: float
    end: float
    maturity: float
    delta: float = 1.0

    @property
    def supervisory_duration(self) -> float:
        """CRE52.34: SD = (exp(-0.05 S) - exp(-0.05 E)) / 0.05."""
        return (math.exp(-0.05 * self.start) - math.exp(-0.05 * self.end)) / 0.05

    @property
    def maturity_factor(self) -> float:
        """CRE52.48: MF = sqrt(min(M, 1) / 1), M floored at 10 business days (10/250 years)."""
        return math.sqrt(min(max(self.maturity, 10 / 250), 1.0))

    @property
    def adjusted_notional(self) -> float:
        """Return the effective notional d = notional x SD x MF x delta."""
        return self.notional * self.supervisory_duration * self.maturity_factor * self.delta


class IrHedgingSet(Record):
    """The interest rate hedging set of one currency, by maturity bucket.

    Attributes:
        bucket_notionals: Summed effective notionals in the buckets under one year, one to
            five years and over five years.
    """

    bucket_notionals: tuple[float, float, float]

    def effective_notional(self) -> float:
        """CRE52.57, step 5: aggregate the buckets with partial offsets across them."""
        d1, d2, d3 = self.bucket_notionals
        return math.sqrt(d1**2 + d2**2 + d3**2 + 1.4 * d1 * d2 + 1.4 * d2 * d3 + 0.6 * d1 * d3)


class SaCcrExposure(Record):
    """The SA-CCR exposure of an unmargined netting set (CRE52.1, 52.10 and 52.20).

    Attributes:
        ead: EAD = alpha (RC + PFE).
        replacement_cost: RC = max(V - C, 0).
        potential_future_exposure: PFE = multiplier x AddOn.
    """

    ead: float
    replacement_cost: float
    potential_future_exposure: float


class NettingSet(Record):
    """An unmargined netting set with its value, the collateral held and its aggregate add-on.

    Attributes:
        value: V, its mark-to-market value to the bank.
        collateral: C, collateral held.
        addon: The aggregate add-on.
        alpha: The EAD multiplier.
    """

    value: float
    collateral: float
    addon: float
    alpha: float = ALPHA

    def multiplier(self) -> float:
        """CRE52.23: min{1; floor + (1 - floor) exp((V - C) / (2 (1 - floor) AddOn))}."""
        return min(
            1.0,
            FLOOR
            + (1 - FLOOR)
            * math.exp((self.value - self.collateral) / (2 * (1 - FLOOR) * self.addon)),
        )

    def exposure(self) -> SaCcrExposure:
        """Return the replacement cost, potential future exposure and EAD."""
        rc = max(self.value - self.collateral, 0.0)
        pfe = self.multiplier() * self.addon
        return SaCcrExposure(
            ead=self.alpha * (rc + pfe), replacement_cost=rc, potential_future_exposure=pfe
        )


class CvaCounterparty(Record):
    """A counterparty in the reduced basic approach for CVA risk (MAR50.14-50.16).

    Attributes:
        risk_weight: Its supervisory risk weight (MAR50.16, Table 1).
        maturity: M, the effective maturity of its netting set in years.
    """

    risk_weight: float
    maturity: float

    @property
    def discount_factor(self) -> float:
        """MAR50.15: DF = (1 - exp(-0.05 M)) / (0.05 M) for banks not using the IMM."""
        return (1 - math.exp(-0.05 * self.maturity)) / (0.05 * self.maturity)

    def scva(self, ead: float, alpha: float = ALPHA) -> float:
        """Return its stand-alone CVA capital RW x M x EAD x DF / alpha."""
        return self.risk_weight * self.maturity * ead * self.discount_factor / alpha


class ReducedBaCva(Record):
    """The reduced basic approach's aggregation of stand-alone CVA capital (MAR50.14).

    Attributes:
        correlation: rho, the supervisory correlation between counterparties.
        discount_scalar: DS, the scalar applied to K.
    """

    correlation: float = 0.5
    discount_scalar: float = 0.65

    def k(self, scva: Sequence[float]) -> float:
        """Return K = sqrt((rho sum SCVA)^2 + (1 - rho^2) sum SCVA^2)."""
        rho = self.correlation
        return math.sqrt((rho * sum(scva)) ** 2 + (1 - rho**2) * sum(s * s for s in scva))

    def capital(self, scva: Sequence[float]) -> float:
        """Return the CVA capital DS x K."""
        return self.discount_scalar * self.k(scva)
