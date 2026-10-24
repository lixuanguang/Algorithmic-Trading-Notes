"""Risk-neutral GBM paths, BSM closed forms and the shared draws of Monte Carlo Greek estimators."""

import numpy as np
from numpy.typing import NDArray
from scipy import stats

from trading_notes.records import Record

type Floats = NDArray[np.float64]


class ClosedForms(Record):
    """The BSM values and Greeks (q = 0) the estimators are checked against.

    Attributes:
        call: The call's value.
        call_delta: Its delta.
        call_vega: Its vega.
        call_gamma: Its gamma.
        call_dK: Its derivative with respect to the strike.
        dig_delta: The unit cash digital's delta.
        dig_dK: The unit cash digital's derivative with respect to the strike.
    """

    call: float
    call_delta: float
    call_vega: float
    call_gamma: float
    call_dK: float
    dig_delta: float
    dig_dK: float


class GbmModel(Record):
    """Risk-neutral geometric Brownian motion without dividends.

    The discount factor and sqrt(T) are NumPy's exp and sqrt, so every scalar matches the
    recorded output to the last bit.

    Attributes:
        spot: S0.
        rate: r, continuously compounded.
        volatility: sigma.
        maturity: T in years.
    """

    spot: float
    rate: float
    volatility: float
    maturity: float

    @property
    def discount(self) -> float:
        """Return e^{-rT}."""
        return float(np.exp(-self.rate * self.maturity))

    @property
    def sqrt_t(self) -> float:
        """Return sqrt(T)."""
        return float(np.sqrt(self.maturity))

    def terminal(self, s0: float, vol: float, z: Floats) -> Floats:
        """Terminal price as a function of S0 and sigma on fixed normals z (B-G eq. (4))."""
        st: Floats = s0 * np.exp((self.rate - vol**2 / 2) * self.maturity + vol * self.sqrt_t * z)
        return st

    def normal_of(self, x: float, s0: float, vol: float) -> float:
        """Return the standard normal that puts S_T at x."""
        z: float = (np.log(x / s0) - (self.rate - vol**2 / 2) * self.maturity) / (vol * self.sqrt_t)
        return z

    def log_density(self, x: float, s0: float, vol: float) -> float:
        """Log of the lognormal density of S_T (eqs. (10)-(11))."""
        d = self.normal_of(x, s0, vol)
        return float(stats.norm.logpdf(d) - np.log(x * vol * self.sqrt_t))

    def closed_forms(self, strike: float) -> ClosedForms:
        """Return the BSM call and cash-digital values and Greeks at the strike."""
        S0, K, SIG, R, T = self.spot, strike, self.volatility, self.rate, self.maturity
        DISC, SQT = self.discount, self.sqrt_t
        d1 = (np.log(S0 / K) + (R + SIG**2 / 2) * T) / (SIG * SQT)
        d2 = d1 - SIG * SQT
        return ClosedForms(
            call=S0 * stats.norm.cdf(d1) - K * DISC * stats.norm.cdf(d2),
            call_delta=stats.norm.cdf(d1),
            call_vega=S0 * SQT * stats.norm.pdf(d1),
            call_gamma=stats.norm.pdf(d1) / (S0 * SIG * SQT),
            call_dK=-DISC * stats.norm.cdf(d2),
            dig_delta=DISC * stats.norm.pdf(d2) / (S0 * SIG * SQT),
            dig_dK=-DISC * stats.norm.pdf(d2) / (K * SIG * SQT),
        )


class Draws(Record):
    """The shared normals and what every estimator computes from them.

    Attributes:
        z: The standard normals.
        st: The terminal prices.
        itm: Whether each path ends above the strike.
        pay: The discounted call payoff.
        score_s0: The likelihood-ratio score for S0, Z / (S0 sigma sqrt T).
        score_sig: The likelihood-ratio score for sigma, (Z^2 - 1) / sigma - sqrt(T) Z.
    """

    z: Floats
    st: Floats
    itm: NDArray[np.bool_]
    pay: Floats
    score_s0: Floats
    score_sig: Floats

    @classmethod
    def draw(cls, model: GbmModel, strike: float, rng: np.random.Generator, m: int) -> Draws:
        """Draw m normals and compute the shared quantities for a call at the strike."""
        S0, SIG, SQT = model.spot, model.volatility, model.sqrt_t
        Z = rng.standard_normal(m)
        ST = model.terminal(S0, SIG, Z)
        return cls(
            z=Z,
            st=ST,
            itm=ST > strike,
            pay=model.discount * np.maximum(ST - strike, 0.0),
            score_s0=Z / (S0 * SIG * SQT),
            score_sig=(Z * Z - 1) / SIG - SQT * Z,
        )


def mean_se(x: Floats) -> tuple[float, float]:
    """Return the sample mean and its standard error."""
    return float(x.mean()), float(x.std(ddof=1) / np.sqrt(x.size))
