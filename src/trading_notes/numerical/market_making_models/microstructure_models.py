"""Closed forms of Grossman-Miller with fees, Kyle's single auction and Roll's spread model."""

from trading_notes.records import Record


class GrossmanMillerFees(Record):
    """Grossman and Miller's date-1 market with a per-share fee on market makers' round trips.

    For a positive imbalance the outside trader LT1's fee cancels, so it demands
    (mu - S1) / (gamma sigma^2), while each market maker demands (mu - S1 - 2 eta) / (gamma
    sigma^2); the price clears i = n q_MM + q_LT1.

    Attributes:
        mu: Expected date-2 value.
        gamma: Risk aversion.
        variance: sigma^2, the variance of the date-2 value.
        market_makers: n.
        imbalance: i, positive.
        fee: eta, per share and trade.
    """

    mu: float
    gamma: float
    variance: float
    market_makers: int
    imbalance: float
    fee: float

    def excess_demand(self, price: float) -> float:
        """Return n q_MM + q_LT1 - i at the date-1 price."""
        g, s2 = self.gamma, self.variance
        q_mm = (self.mu - price - 2 * self.fee) / (g * s2)
        q_lt = (self.mu - price) / (g * s2)
        return self.market_makers * q_mm + q_lt - self.imbalance

    def price(self) -> float:
        """Return the clearing price mu - g s2 i / (n + 1) - 2 n eta / (n + 1)."""
        n = self.market_makers
        return (
            self.mu
            - self.gamma * self.variance * self.imbalance / (n + 1)
            - 2 * n * self.fee / (n + 1)
        )

    def trader_demand(self) -> float:
        """Return LT1's holding i / (n + 1) + 2 n eta / ((n + 1) g s2)."""
        n = self.market_makers
        return self.imbalance / (n + 1) + 2 * n / (n + 1) * self.fee / (self.gamma * self.variance)

    def liquidity(self) -> float:
        """Return lambda = -gamma sigma^2 / n in P1 - mu = lambda Q, without fees."""
        return -self.gamma * self.variance / self.market_makers


class KyleAuction(Record):
    """Kyle's single auction with one insider, noise traders and a competitive market maker.

    Attributes:
        sigma_v: Standard deviation of the asset's value.
        sigma_u: Standard deviation of the noise order flow.
        mean: The value's prior mean.
    """

    sigma_v: float
    sigma_u: float
    mean: float

    @property
    def beta(self) -> float:
        """Return the insider's trading intensity sigma_u / sigma_v."""
        return self.sigma_u / self.sigma_v

    @property
    def price_impact(self) -> float:
        """Return lambda = sigma_v / (2 sigma_u)."""
        return self.sigma_v / (2 * self.sigma_u)

    @property
    def expected_profit(self) -> float:
        """Return the insider's expected profit sigma_v sigma_u / 2."""
        return self.sigma_v * self.sigma_u / 2

    @property
    def posterior_variance(self) -> float:
        """Return Var(v | y) = sigma_v^2 / 2."""
        return self.sigma_v**2 / 2


class RollModel(Record):
    """Roll's model: an efficient random walk plus half the spread times the trade sign.

    Attributes:
        spread: S, the bid-ask spread.
        sigma: Standard deviation of the efficient price change.
    """

    spread: float
    sigma: float

    def price_change_variance(self) -> float:
        """Return Var(dP) = sigma^2 + S^2 / 2."""
        return self.sigma**2 + self.spread**2 / 2

    def first_autocovariance(self) -> float:
        """Return Cov(dP_t, dP_{t-1}) = -S^2 / 4."""
        return -(self.spread**2) / 4
