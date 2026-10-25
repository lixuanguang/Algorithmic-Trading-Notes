"""Amit Goyal's predictor workbook, checked against its recorded hash, and its CSV extracts."""

import hashlib
import sys
import warnings
from collections.abc import Sequence
from pathlib import Path
from typing import ClassVar, Final, Self

import numpy as np
import pandas as pd

from trading_notes.data_folders import DataFolder
from trading_notes.records import Record
from trading_notes.research.workflow import WorkflowArguments

# PredictorData2005_original.xlsx, linked on Goyal's page as "Original data (up to 2005) used in
# the paper" and downloaded 2026-10-22 (485,064 bytes); it runs to December 2025.
EXPECTED_SHA256: Final = "8d210b779442a5a9206702060aac67c1de4283186c0f167ebdb4488d149be872"


class WorkbookHashError(ValueError):
    """The workbook is not the recorded download."""


class GoyalWorkbook(Record):
    """The predictor workbook, checked against its recorded hash.

    Attributes:
        path: The workbook.
        sha256: Its SHA-256, equal to EXPECTED_SHA256.
    """

    path: Path
    sha256: str

    @classmethod
    def open(cls, path: Path) -> Self:
        """Return the workbook at path once its hash is checked.

        Raises:
            WorkbookHashError: If its SHA-256 differs from the recorded one.
        """
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != EXPECTED_SHA256:
            raise WorkbookHashError(
                f"workbook hash {digest} differs from the recorded {EXPECTED_SHA256}"
            )
        return cls(path=path, sha256=digest)

    def sheet(self, name: str) -> pd.DataFrame:
        """Return a sheet; openpyxl's warnings on its header and footer are ignored."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")  # openpyxl cannot parse the sheets' header and footer
            return pd.read_excel(self.path, sheet_name=name)

    def write_extract(self, out: Path, sheet: str, key: str, columns: Sequence[str]) -> str:
        """Write a sheet's key and columns as printed, under a source-hash comment.

        Returns:
            A summary line: the file name, its rows and its first and last keys.
        """
        frame = self.sheet(sheet)
        with out.open("w") as fh:
            fh.write(f"# source sha256 {self.sha256}\n")
            frame[[key, *columns]].to_csv(fh, index=False, float_format="%.10g")
        labels = frame[key].to_numpy(dtype=np.int64)
        return f"{out.name}: {len(frame)} rows, {labels[0]} to {labels[-1]}"


class GoyalArguments(WorkflowArguments):
    """An extract's arguments.

    Attributes:
        workbook: PredictorData2005_original.xlsx.
    """

    folder: ClassVar[DataFolder] = DataFolder(subsection="return_predictability")
    workbook: Path

    def extract(self, sheets: Sequence[tuple[str, str, str]], columns: Sequence[str]) -> int:
        """Write each (file name, sheet, key) extract and print its summary.

        Returns:
            0, or 1, with the reason on stderr and nothing written, when the workbook is not
            the recorded download.
        """
        try:
            book = GoyalWorkbook.open(self.workbook)
        except WorkbookHashError as exc:
            print(exc, file=sys.stderr)
            return 1
        for name, sheet, key in sheets:
            print(book.write_extract(self.extract_folder / name, sheet, key, columns))
        return 0
