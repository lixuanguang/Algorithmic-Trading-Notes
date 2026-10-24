"""Stock returns built from an index and its dividends, and the Campbell-Shiller linearisation."""

from typing import Self

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.return_predictability.labelled_table import LabelledTable, lagged
from trading_notes.records import Record

type Floats = NDArray[np.float64]


def log1pexp(x: Floats | float) -> Floats:
    """Return log(1 + e^x), elementwise and without overflow."""
    return np.asarray(np.logaddexp(0.0, x))


class ReturnPanel(Record):
    """Returns and dividend ratios of Goyal's S&P 500 series at one frequency.

    Attributes:
        labels: Year or yyyymm of each row.
        R: The simple return: CRSP's where it exists, else built from Index and D12.
        r: log(1 + R).
        dp: log D12 - log Index.
        dd: The change in log D12 from the previous row.
        dp_lag: dp in the previous row.
        Rfree: The risk-free return.
        index_return: The return built from Index and D12 in every row.
    """

    labels: NDArray[np.int64]
    R: Floats
    r: Floats
    dp: Floats
    dd: Floats
    dp_lag: Floats
    Rfree: Floats
    index_return: Floats

    @classmethod
    def of(cls, table: LabelledTable, per_year: int) -> Self:
        """Return the panel of an annual (per_year 1) or monthly (12) Goyal extract."""
        index, d12, crsp = table["Index"], table["D12"], table["CRSP_SPvw"]
        built = (index + d12 / per_year) / lagged(index) - 1
        R = np.where(~np.isnan(crsp), crsp, built)
        dp = np.log(d12) - np.log(index)
        log_d = np.log(d12)
        return cls(
            labels=table.labels,
            R=R,
            r=np.log1p(R),
            dp=dp,
            dd=log_d - lagged(log_d),
            dp_lag=lagged(dp),
            Rfree=table["Rfree"],
            index_return=built,
        )

    @property
    def pd(self) -> Floats:
        """Return the log price-dividend ratio -dp."""
        return -self.dp

    def rows(self, lo: int, hi: int) -> NDArray[np.bool_]:
        """Return the mask of rows labelled lo..hi inclusive."""
        mask: NDArray[np.bool_] = (self.labels >= lo) & (self.labels <= hi)
        return mask

    def position(self, label: int) -> int:
        """Return the row of a label within the panel."""
        return int(np.where(self.labels == label)[0][0])


class Linearisation(Record):
    """r_t ~ k + rho pd_t - pd_{t-1} + dd_t, expanding log(1 + e^x) at x = pd-bar.

    Attributes:
        point: pd-bar.
    """

    point: float

    @classmethod
    def working_paper(cls, R: Floats, dd: Floats) -> Self:
        """Return Campbell and Shiller's (1986, printed p. 5) point.

        delta = -pd-bar is log(exp(r - g) - 1) with r = log(1 + sample mean of the simple
        return), not the mean log return, and g = mean log dividend growth; then
        rho = exp(-(r - g)).

        Raises:
            ValueError: If log(1 + mean R) is not above mean dividend growth.
        """
        rbar, g = np.log1p(np.mean(R)), np.mean(dd)
        if not rbar > g:
            raise ValueError("the working-paper point needs log(1 + mean R) > mean dividend growth")
        return cls(point=float(-np.log(np.expm1(rbar - g))))

    @property
    def rho(self) -> float:
        """Return 1 / (1 + e^{-pd-bar})."""
        return float(1 / (1 + np.exp(-self.point)))

    @property
    def k(self) -> float:
        """Return log(1 + e^{pd-bar}) - rho pd-bar."""
        return float(log1pexp(self.point) - self.rho * self.point)

    def approximation(self, pd: Floats, dd: Floats) -> Floats:
        """Return k + rho pd_t - pd_{t-1} + dd_t, NaN in the first row."""
        approx: Floats = self.k + self.rho * pd - lagged(pd) + dd
        return approx
