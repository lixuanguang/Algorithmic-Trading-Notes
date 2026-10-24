"""Basel counterparty capital: SA-CCR exposure at default and the reduced basic CVA approach."""

import math
from collections.abc import Sequence
from typing import Final

from trading_notes.numerical.records import Record

ALPHA: Final = 1.4
FLOOR: Final = 0.05


def supervisory_duration(s: float, e: float) -> float:
    """CRE52.34: SD = (exp(-0.05 S) - exp(-0.05 E)) / 0.05."""
    return (math.exp(-0.05 * s) - math.exp(-0.05 * e)) / 0.05


def maturity_factor_unmargined(m: float) -> float:
    """CRE52.48: MF = sqrt(min(M, 1) / 1), M floored at 10 business days (10/250 years)."""
    return math.sqrt(min(max(m, 10 / 250), 1.0))


def ir_hedging_set_effective_notional(d1: float, d2: float, d3: float) -> float:
    """CRE52.57, step 5 with offsets across the three maturity buckets."""
    return math.sqrt(d1**2 + d2**2 + d3**2 + 1.4 * d1 * d2 + 1.4 * d2 * d3 + 0.6 * d1 * d3)


def multiplier(v_minus_c: float, addon: float) -> float:
    """CRE52.23: min{1; floor + (1 - floor) exp((V - C) / (2 (1 - floor) AddOn))}."""
    return min(1.0, FLOOR + (1 - FLOOR) * math.exp(v_minus_c / (2 * (1 - FLOOR) * addon)))


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


def sa_ccr_ead(v: float, c: float, addon: float, alpha: float = ALPHA) -> SaCcrExposure:
    """Return the exposure of an unmargined netting set worth V with collateral C held."""
    rc = max(v - c, 0.0)
    pfe = multiplier(v - c, addon) * addon
    return SaCcrExposure(ead=alpha * (rc + pfe), replacement_cost=rc, potential_future_exposure=pfe)


def supervisory_df(m: float) -> float:
    """MAR50.15: DF = (1 - exp(-0.05 M)) / (0.05 M) for banks not using the IMM."""
    return (1 - math.exp(-0.05 * m)) / (0.05 * m)


def k_reduced(scva: Sequence[float], rho: float) -> float:
    """MAR50.14: K = sqrt((rho sum SCVA)^2 + (1 - rho^2) sum SCVA^2)."""
    return math.sqrt((rho * sum(scva)) ** 2 + (1 - rho**2) * sum(s * s for s in scva))
