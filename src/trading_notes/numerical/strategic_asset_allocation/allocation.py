"""Asset allocation models: human capital, mean-variance weights, rebalancing, surplus and goals."""

import math

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import minimize
from scipy.stats import norm

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]


def financial_equity_share(
    fin: float, hc: float, target: float = 0.45, hc_equity: float = 0.30
) -> float:
    """Return the equity share of financial assets that makes total wealth `target` equity.

    Args:
        fin: Financial assets.
        hc: Human capital.
        target: Equity share wanted on the whole economic balance sheet.
        hc_equity: Equity-like share of human capital.
    """
    return (target * (fin + hc) - hc_equity * hc) / fin


def mean_variance_weights(cov: Floats, mu: Floats, lam: float, cap: float = 1.0) -> Floats:
    """Return the fully invested weights in [0, cap] maximising w'mu - lam w'Sigma w / 2.

    SLSQP from equal weights.
    """

    def obj(w: Floats) -> float:
        return np.float64(-(w @ mu - 0.5 * lam * w @ cov @ w))

    def fully_invested(w: Floats) -> np.float64:
        gap: np.float64 = w.sum() - 1
        return gap

    n = len(mu)
    r = minimize(
        obj,
        np.full(n, 1 / n),
        bounds=[(0, cap)] * n,
        constraints=[{"type": "eq", "fun": fully_invested}],
        method="SLSQP",
    )
    weights: Floats = r.x
    return weights


def rebalanced_wealth(path: str, up: float, down: float) -> float:
    """Return the wealth of a 50/50 risky/cash portfolio rebalanced each period along a path.

    Args:
        path: The risky asset's moves, "u" or "d" per period.
        up: Gross risky return on an up move.
        down: Gross risky return on a down move.
    """
    w = 1.0
    for step in path:
        w = w * (0.5 * (up if step == "u" else down) + 0.5)
    return w


class SurplusModel(Record):
    """Asset classes and a liability, for surplus risk relative to funded assets.

    Attributes:
        excess_returns: Expected excess returns of the asset classes.
        cov_all: Covariance of the asset classes and, last, the liability.
        assets: Funded assets.
        liabilities: Liability value.
        liability_return: Expected excess return of the liability.
    """

    excess_returns: Floats
    cov_all: Floats
    assets: float
    liabilities: float
    liability_return: float

    def stats(self, w: Floats) -> tuple[float, float]:
        """Return the surplus mean and volatility, relative to funded assets, of asset weights w."""
        x = np.append(self.assets * w, -self.liabilities)  # money exposures, liabilities short
        mu = np.float64(
            (self.assets * w @ self.excess_returns - self.liabilities * self.liability_return)
            / self.assets
        )
        sd = math.sqrt(x @ self.cov_all @ x) / self.assets
        return mu, sd


def minimum_expected_return(mu: float, sd: float, years: float, prob: float) -> float:
    """Return the annualised return that a module exceeds with probability prob over years.

    mu - z_prob sd / sqrt(years): the minimum expectation of a goals-based module.
    """
    return mu - norm.ppf(prob) * sd / math.sqrt(years)
