"""Rows of the Excel workbooks the research workflows read, and EIA's daily and weekly series."""

import datetime as dt
from pathlib import Path

import openpyxl
import xlrd

type XlsCell = str | float
type XlsxCell = str | int | float | dt.datetime | None
# Excel's serial day 0 in the 1900 date system, as xlrd returns dates.
EXCEL_EPOCH = dt.date(1899, 12, 30)


def xls_rows(path: Path, sheet: str | int) -> list[list[XlsCell]]:
    """Return every row of a sheet of an .xls workbook, by name or index, as cell values."""
    book = xlrd.open_workbook(path)
    sh = book.sheet_by_name(sheet) if isinstance(sheet, str) else book.sheet_by_index(sheet)
    return [sh.row_values(i) for i in range(sh.nrows)]


def xlsx_rows(path: Path, sheet: str) -> list[tuple[XlsxCell, ...]]:
    """Return every row of a sheet of an .xlsx workbook, read only, as cell values."""
    book = openpyxl.load_workbook(path, read_only=True)
    try:
        return list(book[sheet].iter_rows(values_only=True))
    finally:
        book.close()


def excel_date(serial: XlsCell) -> dt.date:
    """Return the date of an Excel serial day number (its fraction of a day dropped)."""
    if isinstance(serial, str):
        raise ValueError(f"not a date serial: {serial!r}")
    return EXCEL_EPOCH + dt.timedelta(days=int(serial))


def eia_series(path: Path) -> dict[dt.date, float]:
    """Return an EIA series workbook's "Data 1" sheet as date -> value, blank rows skipped.

    The sheet's first three rows are headers; each later row starts with a date serial and a
    value.
    """
    out: dict[dt.date, float] = {}
    for row in xls_rows(path, "Data 1")[3:]:
        d, v = row[:2]
        if d == "" or v == "":
            continue
        out[excel_date(d)] = float(v)
    return out
