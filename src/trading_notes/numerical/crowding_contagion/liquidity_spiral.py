"""Brunnermeier and Pedersen's price response to a selling shock under margin and loss spirals."""

from trading_notes.records import Record


class LiquiditySpiral(Record):
    """Proposition 5 of Brunnermeier and Pedersen: dp1/deta1 = 1 / (k - l), eq. (24).

    k = 2 m / (gamma sigma2^2) and l = -(dm/dp) x1 + x0 under selling pressure (Z1 > 0): the
    first term of l is the margin spiral, the second the loss spiral.

    Attributes:
        gamma: Risk aversion.
        sigma2: Volatility of the period-2 price.
        margin: The margin m.
        position: x1, the prior position facing a margin that rises as the price falls.
        loss_position: x0, the position whose losses feed the loss spiral.
        margin_slope: dm/dp.
    """

    gamma: float
    sigma2: float
    margin: float
    position: float
    loss_position: float
    margin_slope: float

    @property
    def k(self) -> float:
        """Return k = 2 m / (gamma sigma2^2)."""
        return 2 * self.margin / (self.gamma * self.sigma2**2)

    @property
    def margin_loop(self) -> float:
        """Return the margin component of l, -(dm/dp) x1."""
        return -self.margin_slope * self.position

    @property
    def loss_loop(self) -> float:
        """Return the loss component of l, x0."""
        return self.loss_position

    def response(self, ell: float) -> float:
        """Return the closed form dp1/deta1 = 1 / (k - l) for a loop strength l."""
        return 1 / (self.k - ell)

    def series_response(self, ell: float, terms: int) -> float:
        """Return the loop series 1/k + l/k^2 + l^2/k^3 + ..., one term per loop of the spiral.

        Summed term by term, independently of the closed form; it converges for |l| < k.
        """
        k = self.k
        return sum(ell**n / k ** (n + 1) for n in range(terms))
