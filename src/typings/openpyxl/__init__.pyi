import datetime
from collections.abc import Iterator
from os import PathLike
from typing import Literal

# Only the calls the research workflows make: read-only workbooks read row by row as values.
type CellValue = str | int | float | datetime.datetime | None

class ReadOnlyWorksheet:
    def iter_rows(self, *, values_only: Literal[True]) -> Iterator[tuple[CellValue, ...]]: ...

class Workbook:
    def __getitem__(self, key: str) -> ReadOnlyWorksheet: ...
    def close(self) -> None: ...

def load_workbook(filename: str | PathLike[str], *, read_only: Literal[True]) -> Workbook: ...
