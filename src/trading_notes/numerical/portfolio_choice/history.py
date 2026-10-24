"""Loading the annual US asset-class return history transcribed from Damodaran's workbook."""

import csv
from pathlib import Path
from typing import Self

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]


class AssetClassHistory(Record):
    """Annual total returns, in decimals, by calendar year.

    Attributes:
        years: Calendar years, in order.
        series: Returns by column name (sp500, tbill_3m, ..., cpi_inflation), aligned with years.
    """

    years: NDArray[np.int_]
    series: dict[str, Floats]

    @classmethod
    def read(cls, path: Path) -> Self:
        """Read a CSV whose comment lines start with '#', then a header with a `year` column.

        Raises:
            OSError: If the file cannot be read.
            ValueError: If a field is not a number.
        """
        with path.open(encoding="utf-8") as f:
            rows = list(csv.reader(line for line in f if line[0] != "#"))
        header, data = rows[0], np.array([[float(x) for x in r] for r in rows[1:]])
        years = data[:, header.index("year")].astype(int)
        series = {name: data[:, i] for i, name in enumerate(header) if name != "year"}
        return cls(years=years, series=series)
