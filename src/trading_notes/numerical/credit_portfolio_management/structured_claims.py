"""Claims on a pool of loans: securitisation tranches against covered bonds."""

from trading_notes.records import Record


class Securitisation(Record):
    """Tranches paid from the pool alone, most senior first.

    Attributes:
        tranches: (name, size) of each tranche, most senior first.
    """

    tranches: tuple[tuple[str, float], ...]

    def payoff(self, pool_value: float) -> dict[str, float]:
        """Return each tranche's payoff from the pool, senior first."""
        out, left = {}, pool_value
        for k, size in self.tranches:
            out[k] = min(left, size)
            left -= out[k]
        return out


class CoveredBond(Record):
    """Bonds the issuer pays, with a priority claim on the cover pool if the issuer fails.

    Attributes:
        notional: The covered bonds outstanding.
    """

    notional: float

    def payoff(self, pool_value: float, issuer_solvent: bool, unsecured_recovery: float) -> float:
        """Return the issuer's payment, or the pool's plus a pari passu unsecured claim."""
        if issuer_solvent:
            return self.notional  # the issuer pays; the pool is security, not the source of payment
        priority = min(pool_value, self.notional)
        return priority + (self.notional - priority) * unsecured_recovery
