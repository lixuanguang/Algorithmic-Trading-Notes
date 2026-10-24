"""Extract the annual and monthly S&P 500 series used by return-predictability-checks.py (2026-10-22).

Source: Amit Goyal's data page (https://sites.google.com/view/agoyal145), the workbook linked as "Original data
(up to 2005) used in the paper", downloaded 2026-10-22 from Google Drive file id 1qwpl2R_DNujpU5YUkk8lacP1tTeMb9iJ
(PredictorData2005_original.xlsx, 485,064 bytes, SHA-256
8d210b779442a5a9206702060aac67c1de4283186c0f167ebdb4488d149be872). Despite its label, the workbook served on that
date runs to December 2025 in the column layout of Welch and Goyal (2008); it is therefore the 2026 vintage of the
series, not the file behind the 2008 tables. No earlier vintage was available from the page.

Columns kept, as printed in the workbook (no transformation here):
  Index      S&P 500 index level at the end of the period
  D12        dividends over the trailing twelve months
  Rfree      risk-free return over the period (annual sheet: the year; monthly sheet: the month)
  CRSP_SPvw  CRSP value-weighted S&P 500 return including dividends (from 1926)
The check script derives returns, the dividend-price ratio and excess returns from these columns.

Run: uv run --frozen --no-editable --group empirical python goyal_extract.py <path to PredictorData2005_original.xlsx>
Writes goyal-annual-1871-2025.csv and goyal-monthly-1871-2025.csv next to this script.
"""

import hashlib
import sys
import warnings
from pathlib import Path

import pandas as pd

EXPECTED_SHA256 = "8d210b779442a5a9206702060aac67c1de4283186c0f167ebdb4488d149be872"
KEEP = ["Index", "D12", "Rfree", "CRSP_SPvw"]
HERE = Path(__file__).resolve().parent

src = Path(sys.argv[1])
digest = hashlib.sha256(src.read_bytes()).hexdigest()
if digest != EXPECTED_SHA256:
    sys.exit(f"workbook hash {digest} differs from the recorded {EXPECTED_SHA256}")

with warnings.catch_warnings():
    warnings.simplefilter("ignore")  # openpyxl cannot parse the sheets' header and footer
    annual = pd.read_excel(src, sheet_name="Annual")
    monthly = pd.read_excel(src, sheet_name="Monthly")

header = f"# source sha256 {digest}\n"
for frame, key, name in ((annual, "yyyy", "annual"), (monthly, "yyyymm", "monthly")):
    out = HERE / f"goyal-{name}-1871-2025.csv"
    with out.open("w") as fh:
        fh.write(header)
        frame[[key, *KEEP]].to_csv(fh, index=False, float_format="%.10g")
    print(f"{out.name}: {len(frame)} rows, {frame[key].iloc[0]} to {frame[key].iloc[-1]}")
