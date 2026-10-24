"""Recursive out-of-sample forecasts and nested-model comparisons (Clark and West, ENC, R2_OS)."""

from typing import Self

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]


class RecursiveForecasts(Record):
    """Forecasts of y[i], i >= first, from OLS of y[s] on (1, x[s]) for s < i, and the mean.

    x[i] is the predictor known before y[i] (already lagged). The fits use running sums, so
    arrays may carry leading replication axes; each field has the inputs' leading axes and
    one entry per forecast origin i = first..n - 1 on the last.

    Attributes:
        regression: The regression forecasts.
        mean: The historical-mean forecasts.
        slope: The fitted slopes.
    """

    regression: Floats
    mean: Floats
    slope: Floats

    @classmethod
    def of(cls, x: Floats, y: Floats, first: int) -> Self:
        """Return the forecasts of y from x at the origins first..n - 1."""
        n = np.arange(1, x.shape[-1] + 1, dtype=float)
        sx, sy = np.cumsum(x, axis=-1), np.cumsum(y, axis=-1)
        sxx, sxy = np.cumsum(x * x, axis=-1), np.cumsum(x * y, axis=-1)
        # sums through s = i - 1 sit at position i - 1
        sl = slice(first - 1, x.shape[-1] - 1)
        nn, sx, sy, sxx, sxy = n[sl], sx[..., sl], sy[..., sl], sxx[..., sl], sxy[..., sl]
        b = (nn * sxy - sx * sy) / (nn * sxx - sx * sx)
        a = (sy - b * sx) / nn
        xi = x[..., first:]
        return cls(regression=a + b * xi, mean=sy / nn, slope=b)


def lstsq_forecasts(x: Floats, y: Floats, first: int) -> Floats:
    """Return the regression forecasts of RecursiveForecasts by numpy.linalg.lstsq refits.

    An independent reference for the running sums: one series, refitted at each origin.
    """
    out = []
    for i in range(first, len(y)):
        X = np.column_stack([np.ones(i), x[:i]])
        coef = np.linalg.lstsq(X, y[:i], rcond=None)[0]
        out.append(coef[0] + coef[1] * x[i])
    return np.array(out)


def mean_t(v: Floats) -> Floats:
    """Return the t statistic of the mean of v along its last axis (ordinary standard error).

    The result has v's leading axes: a zero-dimensional array for a single series.
    """
    return np.asarray(v.mean(axis=-1) / (v.std(axis=-1, ddof=1) / np.sqrt(v.shape[-1])))


def ols_slope(x: Floats, y: Floats) -> float:
    """Return the OLS slope of y on x with an intercept."""
    xc = x - x.mean()
    return float(np.sum(xc * (y - y.mean())) / np.sum(xc * xc))


class NestedComparison(Record):
    """Out-of-sample errors of a model A against the nested benchmark N (the historical mean).

    Attributes:
        P: The number of forecasts.
        R2_OS: 1 - MSE_A / MSE_N.
        dRMSE: RMSE_N - RMSE_A.
        MSE_F: P (MSE_N - MSE_A) / MSE_A.
        ENC: sum(e_N (e_N - e_A)) / MSE_A.
        CW_t: Clark and West's t statistic of f = e_N^2 - (e_A^2 - (f_N - f_A)^2).
        CW_mean: The mean of f.
        adj: The mean squared forecast difference.
        mse_a: MSE_A.
        mse_n: MSE_N.
    """

    P: int
    R2_OS: float
    dRMSE: float
    MSE_F: float
    ENC: float
    CW_t: float
    CW_mean: float
    adj: float
    mse_a: float
    mse_n: float

    @classmethod
    def of(cls, y: Floats, yhat_a: Floats, yhat_n: Floats) -> NestedComparison:
        """Return the comparison of the two forecast series for the outcomes y."""
        e_a, e_n = y - yhat_a, y - yhat_n
        mse_a, mse_n = np.mean(e_a**2), np.mean(e_n**2)
        p = len(y)
        f = e_n**2 - (e_a**2 - (yhat_n - yhat_a) ** 2)
        return cls(
            P=p,
            R2_OS=float(1 - mse_a / mse_n),
            dRMSE=float(np.sqrt(mse_n) - np.sqrt(mse_a)),
            MSE_F=float(p * (mse_n - mse_a) / mse_a),
            ENC=float(np.sum(e_n * (e_n - e_a)) / mse_a),
            CW_t=float(mean_t(f)),
            CW_mean=float(f.mean()),
            adj=float(np.mean((yhat_n - yhat_a) ** 2)),
            mse_a=float(mse_a),
            mse_n=float(mse_n),
        )
