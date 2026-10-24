"""Giacomini-White conditional predictive ability tests and the variances they need."""

from typing import Literal, Self

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]
type Kernel = Literal["uniform", "bartlett"]


class SingularInstrumentsError(ValueError):
    """The instruments are linearly dependent, so the Wald statistic is undefined."""


class InstrumentedLosses(Record):
    """Z_t = h_t dL_{t+1}: loss differences times the instruments, n x q or a stack R x n x q.

    Attributes:
        Z: The products, the last two axes time and instrument.
    """

    Z: Floats

    def singular_values(self) -> Floats:
        """Return the singular values of Z / sqrt(n).

        Raises:
            SingularInstrumentsError: If a matrix is numerically rank deficient, its smallest
                singular value below 1e-10 max(n, q) times its largest (the protocol tolerance).
        """
        n, q = self.Z.shape[-2:]
        s: Floats = np.linalg.svd(self.Z / np.sqrt(n), compute_uv=False)
        tol = 1e-10 * max(n, q)
        bad = s[..., -1] < tol * s[..., 0]
        if np.any(bad):
            sv = s.reshape(-1, q)[int(np.argmax(np.ravel(bad)))]
            rank = int(np.sum(sv > tol * sv[0]))
            raise SingularInstrumentsError(
                f"instrument matrix has rank {rank} < q = {q}; drop the redundant instrument"
            )
        return s

    def statistic(self) -> Floats:
        """Return GW eq. (4), T = n Zbar' Omega^-1 Zbar, with the uncentred one-step covariance.

        Raises:
            SingularInstrumentsError: If the instruments are linearly dependent.
        """
        Z = self.Z
        self.singular_values()
        n = Z.shape[-2]
        zbar = Z.mean(axis=-2)
        omega = np.einsum("...ti,...tj->...ij", Z, Z) / n
        return np.asarray(
            n * np.einsum("...i,...i->...", zbar, np.linalg.solve(omega, zbar[..., None])[..., 0])
        )

    def n_r2(self) -> float:
        """Return GW comment 7: n R^2 (uncentred) of a vector of ones regressed on one Z."""
        Z = self.Z
        n = Z.shape[0]
        ones = np.ones(n)
        coef = np.linalg.lstsq(Z, ones, rcond=None)[0]
        resid = ones - Z @ coef
        return float(n * (1 - resid @ resid / n))

    def omega_tilde(self, tau: int) -> Floats:
        """Return GW eq. (6): the uncentred covariance plus autocovariances at lags 1..tau-1."""
        Z = self.Z
        n = Z.shape[0]
        om: Floats = Z.T @ Z / n
        for j in range(1, tau):
            G = Z[j:].T @ Z[:-j] / n
            om = om + G + G.T
        return om


class LossDifferences(Record):
    """Loss differences dL along the last axis, one series or a stack of replications.

    Attributes:
        dl: The loss differences.
    """

    dl: Floats

    @classmethod
    def of(cls, dl: Floats) -> Self:
        """Return the differences of a float array."""
        return cls(dl=np.asarray(dl, dtype=float))

    def lrv(self, lags: int, kernel: Kernel) -> Floats:
        """Return the long-run variance of the demeaned series with uniform or Bartlett weights."""
        x = self.dl
        e = x - x.mean(axis=-1, keepdims=True)
        n = x.shape[-1]
        v = np.einsum("...t,...t->...", e, e) / n
        for j in range(1, lags + 1):
            w = 1.0 if kernel == "uniform" else 1 - j / (lags + 1)
            v = v + 2 * w * np.einsum("...t,...t->...", e[..., j:], e[..., :-j]) / n
        return np.asarray(v)

    def hac_t(self, lags: int, kernel: Kernel) -> tuple[Floats, Floats]:
        """Return the Diebold-Mariano t statistic with a HAC variance, and the variance.

        A non-positive variance gives NaN or an infinite t without a warning.
        """
        n = self.dl.shape[-1]
        v = self.lrv(lags, kernel)
        with np.errstate(invalid="ignore", divide="ignore"):
            return np.asarray(self.dl.mean(axis=-1) / np.sqrt(v / n)), v

    def subsample_t(self, K: int) -> Floats:
        """Return ZT eq. (13): K^(1/2) mean of K block means over their s.d.; compare t_{K-1}."""
        x = self.dl
        n = x.shape[-1]
        b = n // K
        means = x[..., : b * K].reshape(*x.shape[:-1], K, b).mean(axis=-1)
        return np.asarray(np.sqrt(K) * means.mean(axis=-1) / means.std(axis=-1, ddof=1))

    def signed_gw(self) -> Floats:
        """Return ZT eq. (4): sum dL / sqrt(sum dL^2), the signed root of T with h = 1."""
        return np.asarray(self.dl.sum(axis=-1) / np.sqrt((self.dl**2).sum(axis=-1)))


def ar1(rng: np.random.Generator, shape: tuple[int, int], phi: float, burn: int) -> Floats:
    """Return stationary AR(1) paths, reps x n, after a burn-in."""
    reps, n = shape
    u = rng.standard_normal((reps, n + burn))
    x = np.empty_like(u)
    x[:, 0] = u[:, 0] / np.sqrt(1 - phi**2)
    for t in range(1, n + burn):
        x[:, t] = phi * x[:, t - 1] + u[:, t]
    return x[:, burn:]


def moving_average(x: Floats, m: int) -> Floats:
    """Return the trailing m-term means along each row."""
    c = np.cumsum(np.pad(x, ((0, 0), (1, 0))), axis=1)
    ma: Floats = (c[:, m:] - c[:, :-m]) / m
    return ma


class RollingForecasts(Record):
    """Forecasts from the previous `window` outcomes: the mean (M) and OLS on a predictor (D).

    Attributes:
        years: The forecast years.
        y: The outcomes.
        fM: The rolling-mean forecasts.
        fD: The rolling-regression forecasts.
        s2M: The window variance of the outcomes.
        s2D: The window residual variance of the regression.
    """

    years: NDArray[np.int64]
    y: Floats
    fM: Floats
    fD: Floats
    s2M: Floats
    s2D: Floats

    @classmethod
    def of(cls, years: NDArray[np.int64], y: Floats, x: Floats, window: int, first: int) -> Self:
        """Return the forecasts of y[i], i >= first, x[i] the predictor dated before y[i]."""
        out = []
        for i in range(first, len(y)):
            yw, xw = y[i - window : i], x[i - window : i]
            xb, yb = xw.mean(), yw.mean()
            b = ((xw - xb) * (yw - yb)).sum() / ((xw - xb) ** 2).sum()
            a0 = yb - b * xb
            res = yw - a0 - b * xw
            out.append((y[i], yb, a0 + b * x[i], yw.var(ddof=1), res @ res / (window - 2)))
        cols = np.array(out).T
        return cls(years=years[first:], y=cols[0], fM=cols[1], fD=cols[2], s2M=cols[3], s2D=cols[4])

    def at(self, year: int) -> int:
        """Return the row of a forecast year."""
        return int(np.where(self.years == year)[0][0])
