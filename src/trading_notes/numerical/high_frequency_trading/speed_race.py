"""The make/take speed race of Foucault, Kadan and Kandel, and cyclic currency arbitrage."""

import numpy as np
from numpy.typing import NDArray
from scipy import optimize

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]


class SpeedRaceEquilibrium(Record):
    """The symmetric Nash equilibrium of the speed race.

    Attributes:
        maker_intensity: Each market maker's monitoring intensity mu.
        taker_intensity: Each investor's monitoring intensity tau.
        trade_rate: R = mubar taubar / (mubar + taubar), with mubar and taubar the sums.
    """

    maker_intensity: float
    taker_intensity: float
    trade_rate: float


class SpeedRace(Record):
    """M market makers and N investors who pay quadratic costs to monitor the market faster.

    Each market maker m maximises (mu_m / mubar) piM R - beta mu_m^2 / 2, and each investor n
    (tau_n / taubar) piT R - gamma tau_n^2 / 2, where piM and piT are the margins a trade gives
    each side.

    Attributes:
        makers: M.
        takers: N.
        beta: Market makers' monitoring cost.
        gamma: Investors' monitoring cost.
    """

    makers: float
    takers: float
    beta: float
    gamma: float

    def equilibrium(self, maker_margin: float, taker_margin: float) -> SpeedRaceEquilibrium:
        """Return the symmetric equilibrium for the two margins, from the first-order conditions.

        Raises:
            AssertionError: If the root solve fails, an internal error rather than a finding.
        """
        M, N, beta, gamma = self.makers, self.takers, self.beta, self.gamma

        def foc(x: Floats) -> list[float]:
            mu, tau = np.exp(x)
            mb, tb = M * mu, N * tau
            s = mb + tb
            f1 = maker_margin * tb * (s - mu) / s**2 - beta * mu
            f2 = taker_margin * mb * (s - tau) / s**2 - gamma * tau
            return [f1 / (beta * mu), f2 / (gamma * tau)]

        sol = optimize.root(foc, x0=[0.0, 0.0], tol=1e-12)
        mu, tau = np.exp(sol.x)
        assert sol.success
        mb, tb = M * mu, N * tau
        return SpeedRaceEquilibrium(
            maker_intensity=float(mu),
            taker_intensity=float(tau),
            trade_rate=float(mb * tb / (mb + tb)),
        )

    def best_maker_margin(self, total: float) -> float:
        """Return the maker's share of the total margin G that maximises the trade rate."""

        def neg_rate(x: float) -> float:
            return -self.equilibrium(x, total - x).trade_rate

        r = optimize.minimize_scalar(
            neg_rate,
            bounds=(1e-6 * total, total * (1 - 1e-6)),
            method="bounded",
            options={"xatol": 1e-10},
        )
        return float(r.x)


def cycle_returns(quotes: dict[str, tuple[float, float]]) -> tuple[float, float]:
    """Return the gross return of each direction round the EUR-USD-JPY cycle from one euro.

    Args:
        quotes: (bid, ask) for EURUSD ($ per euro), USDJPY (yen per $) and EURJPY (yen per euro).

    Returns:
        Euro to dollars to yen to euro, and euro to yen to dollars to euro.
    """
    (eu_b, eu_a), (uj_b, uj_a), (ej_b, ej_a) = quotes["EURUSD"], quotes["USDJPY"], quotes["EURJPY"]
    via_usd = eu_b * uj_b / ej_a
    via_jpy = ej_b / uj_a / eu_a
    return via_usd, via_jpy
