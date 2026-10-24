"""The CAPM's excess-return regression, the security and capital market lines, and APT pricing."""

import math

import numpy as np
from numpy.typing import NDArray

from trading_notes.records import Record

type Floats = NDArray[np.float64]


class CapmFit(Record):
    """The least-squares fit of a stock's excess returns on the market's, by the closed forms.

    Attributes:
        alpha: The intercept.
        beta: The slope Sxy / Sxx.
        residuals: y - alpha - beta x.
        sxx: The sum of squared deviations of x.
        residual_sd: The residual standard deviation, with n - 2 degrees of freedom.
        se_alpha: The intercept's standard error.
        se_beta: The slope's standard error.
        r_squared: 1 - SSE / SST.
    """

    alpha: float
    beta: float
    residuals: Floats
    sxx: float
    residual_sd: float
    se_alpha: float
    se_beta: float
    r_squared: float

    @classmethod
    def of(cls, x: Floats, y: Floats) -> CapmFit:
        """Return the fit of y on x, both one observation per period."""
        n = len(y)
        sxx = ((x - x.mean()) ** 2).sum()
        sxy = ((x - x.mean()) * (y - y.mean())).sum()
        beta = sxy / sxx
        alpha = y.mean() - beta * x.mean()
        resid = y - alpha - beta * x
        s = math.sqrt((resid**2).sum() / (n - 2))
        return cls(
            alpha=alpha,
            beta=beta,
            residuals=resid,
            sxx=sxx,
            residual_sd=s,
            se_alpha=s * math.sqrt(1 / n + x.mean() ** 2 / sxx),
            se_beta=s / math.sqrt(sxx),
            r_squared=1 - (resid**2).sum() / ((y - y.mean()) ** 2).sum(),
        )


class MarketLines(Record):
    """The security market line and the capital market line, in percent a year.

    Attributes:
        risk_free: r_f.
        premium: The market's expected excess return.
        market_sd: The market's standard deviation.
    """

    risk_free: float
    premium: float
    market_sd: float

    def sml(self, b: float) -> float:
        """Return the required return at beta b, r_f + b x premium."""
        return self.risk_free + b * self.premium

    def cml(self, sd: float) -> float:
        """Return the expected return of an efficient portfolio with standard deviation sd."""
        return self.risk_free + self.premium / self.market_sd * sd


class AptPricing(Record):
    """Arbitrage pricing: E[R] = lambda_0 + b' lambda for well-diversified portfolios.

    Attributes:
        zero_beta: lambda_0.
        premia: lambda, one premium per unit sensitivity to each factor.
    """

    zero_beta: float
    premia: Floats

    def expected(self, sensitivities: Floats) -> Floats:
        """Return the expected returns of portfolios, one row of sensitivities each."""
        e: Floats = self.zero_beta + sensitivities @ self.premia
        return e


def replicating_weights(sensitivities: Floats, target: Floats) -> Floats:
    """Return the weights, summing to one, of portfolios that match the target sensitivities.

    Args:
        sensitivities: One row of factor sensitivities per portfolio.
        target: The sensitivities to match.
    """
    w: Floats = np.linalg.solve(
        np.vstack([np.ones(len(sensitivities)), sensitivities.T]), np.concatenate([[1.0], target])
    )
    return w
