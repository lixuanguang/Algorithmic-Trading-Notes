from os import PathLike

# Only the calls the research workflows make, typed as xlrd 2.0 returns them for .xls files.
# A cell value is text, or a number for numeric, date, boolean and error cells.
type CellValue = str | float

class Sheet:
    nrows: int
    def row_values(self, rowx: int) -> list[CellValue]: ...

class Book:
    def sheet_by_name(self, sheet_name: str) -> Sheet: ...
    def sheet_by_index(self, sheetx: int) -> Sheet: ...

def open_workbook(filename: str | PathLike[str]) -> Book: ...
