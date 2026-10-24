"""Spot and forward curves bootstrapped from annual par yields, and month-end GSW zero yields."""

import csv
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]


def bootstrap(par: Floats) -> Floats:
    """Return the discount factors of annual-pay par yields for 1..N years, on a coupon date."""
    dfs: list[float] = []
    for c in par:
        dfs.append((1 - c * sum(dfs)) / (1 + c))
    return np.array(dfs)


class AnnualCurve(Record):
    """Discount factors, spot rates and one-year forwards at annual maturities 1..N.

    Attributes:
        discount: DF_n.
        spot: s_n = DF_n^(-1/n) - 1, annually compounded.
        forward: f(n-1, n) = DF_(n-1) / DF_n - 1.
    """

    discount: Floats
    spot: Floats
    forward: Floats

    @classmethod
    def from_par(cls, par: Floats) -> AnnualCurve:
        """Return the curve bootstrapped from annual par yields."""
        df = bootstrap(par)
        n = np.arange(1, len(par) + 1)
        return cls(
            discount=df,
            spot=df ** (-1 / n) - 1,
            forward=np.r_[df[0] ** -1, df[:-1] / df[1:]] - 1,
        )


class MonthEndYields(Record):
    """Month-end zero yields, in percent, at fixed maturities.

    Attributes:
        dates: ISO month-end dates, oldest first.
        maturities: The maturities in years.
        yields: One row per date, one column per maturity.
    """

    dates: tuple[str, ...]
    maturities: tuple[int, ...]
    yields: Floats

    @classmethod
    def read(cls, path: Path, maturities: tuple[int, ...]) -> MonthEndYields:
        """Read a file with a `date` column and one `y<m>` column per maturity m."""
        with path.open() as fh:
            rows = list(csv.DictReader(fh))
        return cls(
            dates=tuple(r["date"] for r in rows),
            maturities=maturities,
            yields=np.array([[float(r[f"y{m}"]) for m in maturities] for r in rows]),
        )


class PrincipalComponents(Record):
    """Principal components of yield changes, largest first, signed so the loadings sum >= 0.

    Attributes:
        variances: The eigenvalues of the covariance matrix.
        loadings: The eigenvectors, one column per component.
    """

    variances: Floats
    loadings: Floats

    @classmethod
    def of(cls, changes: Floats, signed: int | None = None) -> PrincipalComponents:
        """Return the components of the sample covariance of the changes, one row per date.

        Args:
            changes: The changes, shape (dates, maturities), with at least two dates.
            signed: How many leading components to flip so their loadings sum to a
                non-negative value; None signs every component.

        Raises:
            ValueError: If changes is not a matrix of at least two rows, or signed is outside
                0..maturities.
        """
        if changes.ndim != 2 or changes.shape[0] < 2 or changes.shape[1] < 1:
            raise ValueError(
                f"changes must have shape (dates >= 2, maturities >= 1), got {changes.shape}"
            )
        components = changes.shape[1]
        if signed is None:
            signed = components
        elif not 0 <= signed <= components:
            raise ValueError(f"signed must be in 0..{components}, got {signed}")
        cov = np.atleast_2d(np.cov(changes, rowvar=False))
        eigval, eigvec = np.linalg.eigh(cov)
        order = np.argsort(eigval)[::-1]
        eigval, eigvec = eigval[order], eigvec[:, order]
        for k in range(signed):
            if eigvec[:, k].sum() < 0:
                eigvec[:, k] *= -1
        return cls(variances=eigval, loadings=eigvec)

    def shares(self) -> Floats:
        """Return each component's share of the total variance."""
        return np.asarray(self.variances / self.variances.sum(), dtype=np.float64)
