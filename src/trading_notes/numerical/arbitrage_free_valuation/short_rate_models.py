"""The Svensson forward curve and the Hull-White one-factor model fitted to it."""

import math
from typing import Final, overload

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]


class SvenssonCurve(Record):
    """A Svensson instantaneous forward curve, continuously compounded.

    Attributes:
        b0: beta0, as a decimal.
        b1: beta1, as a decimal.
        b2: beta2, as a decimal.
        b3: beta3, as a decimal.
        t1: tau1, in years.
        t2: tau2, in years.
    """

    b0: float
    b1: float
    b2: float
    b3: float
    t1: float
    t2: float

    def forward(self, t: float) -> float:
        """Return the instantaneous forward rate f(0, t)."""
        e1, e2 = math.exp(-t / self.t1), math.exp(-t / self.t2)
        return self.b0 + self.b1 * e1 + self.b2 * (t / self.t1) * e1 + self.b3 * (t / self.t2) * e2

    def forward_slope(self, t: float) -> float:
        """Return the analytic derivative of f(0, t) with respect to t."""
        t1, t2 = self.t1, self.t2
        e1, e2 = math.exp(-t / t1), math.exp(-t / t2)
        return (
            -self.b1 / t1 * e1 + self.b2 / t1 * e1 * (1 - t / t1) + self.b3 / t2 * e2 * (1 - t / t2)
        )

    def zero_yield(self, t: float) -> float:
        """Return the zero yield y(0, t), the average of f(0, u) on [0, t]; f(0, 0) at t = 0."""
        if t == 0:
            return self.forward(0.0)
        x1, x2 = t / self.t1, t / self.t2
        g1, g2 = (1 - math.exp(-x1)) / x1, (1 - math.exp(-x2)) / x2
        return (
            self.b0 + self.b1 * g1 + self.b2 * (g1 - math.exp(-x1)) + self.b3 * (g2 - math.exp(-x2))
        )

    def discount(self, t: float) -> float:
        """Return the discount factor P(0, t)."""
        return math.exp(-self.zero_yield(t) * t)


# The Federal Reserve Board's Gurkaynak-Sack-Wright parameters for 30 September 2026, in percent
# for the betas and years for the taus (feds200628.csv).
GSW_2026_09_30: Final = {
    "BETA0": 2.220637762132e-14,
    "BETA1": 3.9277698129101,
    "BETA2": 5.27031980138786,
    "BETA3": 17.0928160768659,
    "TAU1": 1.86454967884118,
    "TAU2": 15.7025187144884,
}
GSW_CURVE: Final = SvenssonCurve(
    b0=GSW_2026_09_30["BETA0"] / 100,
    b1=GSW_2026_09_30["BETA1"] / 100,
    b2=GSW_2026_09_30["BETA2"] / 100,
    b3=GSW_2026_09_30["BETA3"] / 100,
    t1=GSW_2026_09_30["TAU1"],
    t2=GSW_2026_09_30["TAU2"],
)


class HullWhite(Record):
    """The Hull-White model r = x + alpha(t), x an Ornstein-Uhlenbeck factor with x(0) = 0.

    Attributes:
        curve: The initial forward curve the model fits.
        a: Mean reversion.
        sigma: Short-rate volatility.
    """

    curve: SvenssonCurve
    a: float
    sigma: float

    def b(self, tau: float) -> float:
        """Return the B function (1 - e^{-a tau}) / a."""
        return (1 - math.exp(-self.a * tau)) / self.a

    def theta(self, t: float) -> float:
        """Hull eq. (32.5): F_t(0,t) + a F(0,t) + sigma^2 (1 - exp(-2at)) / (2a)."""
        a, sg = self.a, self.sigma
        return (
            self.curve.forward_slope(t)
            + a * self.curve.forward(t)
            + sg**2 / (2 * a) * (1 - math.exp(-2 * a * t))
        )

    def alpha(self, t: float) -> float:
        """Return the drift that fits the curve: F(0,t) + sigma^2 (1 - e^{-at})^2 / (2a^2)."""
        a, sg = self.a, self.sigma
        return self.curve.forward(t) + sg**2 / (2 * a**2) * (1 - math.exp(-a * t)) ** 2

    def var_int(self, t: float) -> float:
        """Return Var(int_0^t x du) for the factor started at 0."""
        a, sg = self.a, self.sigma
        return sg**2 / a**2 * (t - 2 * self.b(t) + (1 - math.exp(-2 * a * t)) / (2 * a))

    def bond(self, t: float, T: float, x: Floats) -> Floats:
        """Hull eqs. (32.6)-(32.8): P(t, T) given the factor x on each path."""
        if T <= t:
            return np.ones_like(x)
        a, sg, P0 = self.a, self.sigma, self.curve.discount
        B = self.b(T - t)
        lnA = (
            math.log(P0(T) / P0(t))
            + B * self.curve.forward(t)
            - sg**2
            / (4 * a**3)
            * (math.exp(-a * T) - math.exp(-a * t)) ** 2
            * (math.exp(2 * a * t) - 1)
        )
        return np.exp(lnA - B * (x + self.alpha(t)))

    @overload
    def path_discount(self, t: float, integ: float) -> float: ...
    @overload
    def path_discount(self, t: float, integ: Floats) -> Floats: ...
    def path_discount(self, t: float, integ: float | Floats) -> float | Floats:
        """D(0, t) = exp(-int_0^t r du) given I = int_0^t x du.

        E[x] = 0, so the mean short-rate integral is int_0^t alpha du = -ln P0(t) + var_int(t) / 2,
        and D(0, t) = P0(t) exp(-var_int(t) / 2 - I). Since I ~ N(0, var_int(t)),
        E[D(0, t)] = P0(t).

        Args:
            t: The horizon in years.
            integ: I on one path, or one value per path.

        Returns:
            A float for a scalar I, otherwise an array of I's shape.
        """
        discount = self.curve.discount(t) * np.exp(-0.5 * self.var_int(t) - integ)
        if isinstance(integ, np.ndarray):
            return discount
        return float(discount)

    def step_covariance(self, dt: float) -> Floats:
        """Return the covariance of the increments of (x, I) over a step dt, from x = 0."""
        a, sg = self.a, self.sigma
        e1 = math.exp(-a * dt)
        vx = sg**2 * (1 - e1**2) / (2 * a)
        vi = sg**2 / a**2 * (dt - 2 * self.b(dt) + (1 - e1**2) / (2 * a))
        cv = sg**2 / (2 * a**2) * (1 - e1) ** 2
        return np.array([[vx, cv], [cv, vi]])


class CoxIngersollRoss(Record):
    """The CIR model dr = a(b - r) dt + sigma sqrt(r) dW.

    Attributes:
        a: Mean reversion.
        b: The long-run rate.
        sigma: Volatility.
    """

    a: float
    b: float
    sigma: float

    def price(self, r: float, tau: float) -> float:
        """Return the zero-coupon bond price for short rate r and maturity tau (Hull eq. 31.10)."""
        a, b, s = self.a, self.b, self.sigma
        g = math.sqrt(a * a + 2 * s * s)
        den = (g + a) * (math.exp(g * tau) - 1) + 2 * g
        B = 2 * (math.exp(g * tau) - 1) / den
        A = (2 * g * math.exp((a + g) * tau / 2) / den) ** (2 * a * b / s**2)
        return float(A * math.exp(-B * r))
