"""Extract the annual predictor columns used by forecast-combination-scoring-checks.py (2026-10-22).

Source: the same workbook as goyal_extract.py, Amit Goyal's "Original data (up to 2005) used in the paper",
downloaded 2026-10-22 from Google Drive file id 1qwpl2R_DNujpU5YUkk8lacP1tTeMb9iJ (PredictorData2005_original.xlsx,
485,064 bytes, SHA-256 8d210b779442a5a9206702060aac67c1de4283186c0f167ebdb4488d149be872). It runs to December 2025,
so it is the 2026 vintage of the series, not the file behind the 2008 tables. goyal-annual-1871-2025.csv and
goyal-monthly-1871-2025.csv, written by goyal_extract.py for the earlier batch, are left unchanged.

Columns kept from the Annual sheet, as printed (no transformation here):
  Index      S&P 500 index level at the end of the year
  D12, E12   dividends and earnings over the trailing twelve months
  tbl        three-month Treasury bill rate (decimal)
  AAA, BAA   Moody's corporate bond yields (decimal)
  lty        long-term government bond yield (decimal)
  Rfree      risk-free return over the year
  CRSP_SPvw  CRSP value-weighted S&P 500 return including dividends (from 1926)
The check script derives the log equity premium and the four predictors from these columns.

Run: uv run --frozen --no-editable --group empirical python goyal_extract_predictors.py <path to PredictorData2005_original.xlsx>
Writes goyal-annual-predictors-1871-2025.csv next to this script.
"""

# standard library imports
import hashlib
import sys
import warnings
from pathlib import Path

# third party library imports
import pandas as pd

EXPECTED_SHA256 = "8d210b779442a5a9206702060aac67c1de4283186c0f167ebdb4488d149be872"
KEEP = ["Index", "D12", "E12", "tbl", "AAA", "BAA", "lty", "Rfree", "CRSP_SPvw"]
HERE = Path(__file__).resolve().parent

src = Path(sys.argv[1])
digest = hashlib.sha256(src.read_bytes()).hexdigest()
if digest != EXPECTED_SHA256:
    sys.exit(f"workbook hash {digest} differs from the recorded {EXPECTED_SHA256}")

with warnings.catch_warnings():
    warnings.simplefilter("ignore")  # openpyxl cannot parse the sheets' header and footer
    annual = pd.read_excel(src, sheet_name="Annual")

out = HERE / "goyal-annual-predictors-1871-2025.csv"
with out.open("w") as fh:
    fh.write(f"# source sha256 {digest}\n")
    annual[["yyyy", *KEEP]].to_csv(fh, index=False, float_format="%.10g")
print(f"{out.name}: {len(annual)} rows, {annual['yyyy'].iloc[0]} to {annual['yyyy'].iloc[-1]}")
