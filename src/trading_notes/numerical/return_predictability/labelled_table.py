"""Columns of a CSV extract indexed by an integer label, a year or a yyyymm month."""

from pathlib import Path
from typing import Self

import numpy as np
import pandas as pd
from numpy.typing import NDArray

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]
type Labels = NDArray[np.int64]


def lagged(x: Floats, k: int = 1) -> Floats:
    """Return a column shifted k rows later with the first k rows NaN, as pandas' shift(k).

    k = 0 returns a copy; k at or beyond the length returns all NaN.

    Raises:
        ValueError: If k is negative.
    """
    if k < 0:
        raise ValueError(f"lag {k} is negative")
    out = np.full_like(x, np.nan)
    if k < len(x):
        out[k:] = x[: len(x) - k]
    return out


class LabelledTable(Record):
    """Float columns of a CSV file, one row per label, labels increasing.

    The file is read by pandas, so its numbers parse as in the original scripts; blank fields
    are NaN.

    Attributes:
        labels: The label of each row.
        columns: Each column's values in row order.
    """

    labels: Labels
    columns: dict[str, Floats]

    @classmethod
    def read(cls, path: Path, label: str) -> Self:
        """Read a file with '#' comment lines and an integer label column.

        Raises:
            ValueError: If the labels do not increase.
        """
        frame = pd.read_csv(path, comment="#")
        labels = frame[label].to_numpy(dtype=np.int64)
        if np.any(np.diff(labels) <= 0):
            raise ValueError(f"{path.name}: labels do not increase")
        return cls(
            labels=labels,
            columns={c: frame[c].to_numpy(dtype=np.float64) for c in frame if c != label},
        )

    def __getitem__(self, name: str) -> Floats:
        """Return a column."""
        return self.columns[name]

    def rows(self, lo: int, hi: int) -> NDArray[np.bool_]:
        """Return the mask of rows labelled lo..hi inclusive."""
        mask: NDArray[np.bool_] = (self.labels >= lo) & (self.labels <= hi)
        return mask

    def position(self, label: int) -> int:
        """Return the row of a label.

        Raises:
            KeyError: If no row has the label.
        """
        i = int(np.searchsorted(self.labels, label))
        if i == len(self.labels) or self.labels[i] != label:
            raise KeyError(label)
        return i

    def at(self, values: Floats, labels: Labels) -> Floats:
        """Return a column's values at the given labels.

        Raises:
            KeyError: If a label has no row.
        """
        pos = np.searchsorted(self.labels, labels)
        if np.any(pos >= len(self.labels)) or np.any(
            self.labels[np.minimum(pos, len(self.labels) - 1)] != labels
        ):
            raise KeyError("labels outside the table")
        found: Floats = values[pos]
        return found

    def first_valid(self, name: str) -> int | None:
        """Return the label of the first row where the column is not NaN, or None if none is.

        Raises:
            KeyError: If the table has no such column.
        """
        valid = np.flatnonzero(~np.isnan(self.columns[name]))
        return int(self.labels[valid[0]]) if valid.size else None
