"""The ETF trick's holdings and principal-component risk budgets (AFML sec. 2.4)."""

import numpy as np
from numpy.typing import NDArray

from trading_notes.records import Record

type Floats = NDArray[np.float64]


class EtfTrickBasket(Record):
    """A basket of legs with allocation weights w, sized as the ETF trick sizes them.

    Attributes:
        weights: The allocation w of each leg, signed.
    """

    weights: Floats

    def holdings(self, capital: float, opens: Floats, multipliers: Floats) -> Floats:
        """Return h = w K / (o phi sum|w|): units of each leg at the next open o.

        Args:
            capital: The basket's value K.
            opens: The next opening price o of each leg.
            multipliers: phi, the currency value of one point of each leg.
        """
        w = self.weights
        h: Floats = w * capital / (opens * multipliers * np.abs(w).sum())
        return h


class PrincipalRiskBudget(Record):
    """Weights that distribute a portfolio's variance across principal components.

    Attributes:
        variances: The eigenvalues lambda of the covariance, largest first.
        loadings: The eigenvectors W, one column per component, in the same order.
    """

    variances: Floats
    loadings: Floats

    @classmethod
    def of(cls, covariance: Floats) -> PrincipalRiskBudget:
        """Return the components of a covariance matrix, largest variance first."""
        lam, W = np.linalg.eigh(covariance)
        idx = lam.argsort()[::-1]
        return cls(variances=lam[idx], loadings=W[:, idx])

    def component_weights(self, targets: Floats, sigma: float) -> Floats:
        """Return beta = sigma sqrt(R / lambda), the exposure to each component."""
        beta: Floats = sigma * np.sqrt(targets / self.variances)
        return beta

    def risk_shares(self, weights: Floats, covariance: Floats) -> Floats:
        """Return each component's share (W' w)^2 lambda / (w' V w) of the variance."""
        shares: Floats = (
            (self.loadings.T @ weights) ** 2 * self.variances / (weights @ covariance @ weights)
        )
        return shares
