"""Short-run costs of a competitive firm, a long-run cost curve and symmetric Cournot oligopoly."""

import numpy as np

from trading_notes.records import Record


class CubicCostFirm(Record):
    """A firm with variable cost y^3 - 12 y^2 + 60 y and a fixed cost.

    Attributes:
        fixed_cost: Cost incurred whatever the output.
    """

    fixed_cost: float

    def variable_cost(self, y: float) -> float:
        """Return the variable cost y^3 - 12 y^2 + 60 y."""
        return y**3 - 12 * y**2 + 60 * y

    def marginal_cost(self, y: float) -> float:
        """Return the marginal cost 3 y^2 - 24 y + 60."""
        return 3 * y**2 - 24 * y + 60

    def average_variable_cost(self, y: float) -> float:
        """Return the average variable cost."""
        return self.variable_cost(y) / y

    def average_total_cost(self, y: float) -> float:
        """Return the average total cost."""
        return (self.variable_cost(y) + self.fixed_cost) / y

    def best_output(self, p: float) -> float:
        """Return the output on the rising branch of MC = p; zero below minimum AVC, 24."""
        if p < 24.0:
            return 0.0
        return float((24 + np.sqrt(576 - 12 * (60 - p))) / 6)


def long_run_average_cost(y: float) -> float:
    """Return the long-run average cost 2,000/y + 20 + 0.004y of the scale example."""
    return 2000 / y + 20 + 0.004 * y


class LinearCournot(Record):
    """Cournot competition with inverse demand p = intercept - Y and constant marginal cost.

    Attributes:
        intercept: Demand intercept.
        marginal_cost: Each firm's marginal cost.
    """

    intercept: float
    marginal_cost: float

    def equilibrium(self, n: int) -> tuple[float, float]:
        """Return each firm's symmetric equilibrium output and the price with n firms."""
        q = (self.intercept - self.marginal_cost) / (n + 1)
        return q, self.intercept - n * q
