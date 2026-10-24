"""Extract month-end Gurkaynak-Sack-Wright zero-coupon yields for term-structure-checks.py (2026-10-18).

Input: the Federal Reserve Board's feds200628.csv (fitted off-the-run Treasury curve, daily, continuously compounded
zero yields SVENYxx in percent), kept outside Git at reading_materials/derivatives-validation/empirical/. The file
used here ends on 9 October 2026 (SHA-256 7286435090933f0df1dcaeb15629f3a9129c083baee4c42ae5df03d0bb89335c).

Output: gsw-month-end-zero.csv, the last available business day of each complete month from January 1986 (the
first month with a 30-year yield in every month that follows) to September 2026, maturities 1, 2, 3, 5, 7, 10, 20
and 30 years. The partial October 2026 month is excluded.

Run from this folder: uv run --frozen --no-editable python gsw-month-end-extract.py
"""

import csv
import hashlib
import sys
from pathlib import Path

RAW = (
    Path(__file__).resolve().parents[3]
    / "reading_materials/derivatives-validation/empirical/feds200628.csv"
)
OUT = Path(__file__).resolve().parent / "gsw-month-end-zero.csv"
MATS = [1, 2, 3, 5, 7, 10, 20, 30]
EXPECTED_SHA = "7286435090933f0df1dcaeb15629f3a9129c083baee4c42ae5df03d0bb89335c"

digest = hashlib.sha256(RAW.read_bytes()).hexdigest()
if digest != EXPECTED_SHA:
    sys.exit(f"unexpected input file hash {digest}")
with RAW.open(newline="") as fh:
    lines = fh.read().splitlines()
start = next(i for i, line in enumerate(lines) if line.startswith("Date,"))
rows = list(csv.DictReader(lines[start:]))
last = {}
for row in rows:
    ym = row["Date"][:7]
    vals = [row[f"SVENY{m:02d}"] for m in MATS]
    if "NA" in vals or "" in vals:
        continue
    if "1986-01" <= ym <= "2026-09":
        last[ym] = [row["Date"], *vals]  # rows are in date order, so the last one per month wins
with OUT.open("w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["date"] + [f"y{m}" for m in MATS])
    for ym in sorted(last):
        w.writerow(last[ym])
print(f"wrote {len(last)} months to {OUT.name}")
