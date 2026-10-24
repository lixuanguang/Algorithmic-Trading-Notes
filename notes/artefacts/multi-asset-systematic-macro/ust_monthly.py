"""Rebuild the monthly 10-year minus 3-month (and 10-year minus 2-year) Treasury spreads from daily data.

Source: U.S. Treasury, Daily Treasury Par Yield Curve Rates, one CSV per year, retrieved 2026-10-16 from
  https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/{YEAR}/all
      ?type=daily_treasury_yield_curve&field_tdr_date_value={YEAR}&page&_format=csv
for YEAR = 2006 ... 2026. These are constant-maturity (CMT) par yields, a proxy for, and not the same series as,
Estrella and Trubin's three-month secondary-market bill rate on a bond-equivalent basis (H.15).

Usage (standard library only):
  uv run --frozen --no-editable python ust_monthly.py --extract RAW_DIR   # rebuild ust-daily-3m-2y-10y.csv from the yearly Treasury CSVs
  uv run --frozen --no-editable python ust_monthly.py                     # rebuild ust-10y3m-monthly.csv from ust-daily-3m-2y-10y.csv
Checks: dates unique and strictly increasing; every month from the first to the last present (no gaps);
the month of the last observation flagged incomplete when it is the retrieval month (October 2026).
"""

import csv
import datetime as dt
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DAILY = os.path.join(HERE, "ust-daily-3m-2y-10y.csv")
MONTHLY = os.path.join(HERE, "ust-10y3m-monthly.csv")
RETRIEVED = dt.date(2026, 10, 16)


def extract(raw_dir):
    rows = []
    for path in sorted(glob.glob(os.path.join(raw_dir, "y*.csv"))):
        for r in csv.DictReader(open(path)):
            d = dt.datetime.strptime(r["Date"], "%m/%d/%Y").date()
            rows.append((d.isoformat(), r.get("3 Mo", ""), r.get("2 Yr", ""), r.get("10 Yr", "")))
    rows.sort()
    with open(DAILY, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "cmt_3m", "cmt_2y", "cmt_10y"])
        w.writerows(rows)
    return len(rows)


def monthly():
    rows = list(csv.DictReader(open(DAILY)))
    dates = [r["date"] for r in rows]
    assert len(dates) == len(set(dates)), "duplicate dates"
    assert dates == sorted(dates), "dates not increasing"
    by = {}
    for r in rows:
        if not (r["cmt_3m"] and r["cmt_10y"]):
            continue  # a day missing either yield is skipped
        m = r["date"][:7]
        by.setdefault(m, []).append(r)
    months = sorted(by)
    y0, m0 = map(int, months[0].split("-"))
    expected = []
    y, m = y0, m0
    while f"{y:04d}-{m:02d}" <= months[-1]:
        expected.append(f"{y:04d}-{m:02d}")
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    assert months == expected, "gap in months"
    last_obs = dt.date.fromisoformat(dates[-1])
    out = []
    for mo in months:
        rs = by[mo]
        s3 = sum(float(r["cmt_10y"]) - float(r["cmt_3m"]) for r in rs) / len(rs)
        r2 = [r for r in rs if r["cmt_2y"]]
        s2 = sum(float(r["cmt_10y"]) - float(r["cmt_2y"]) for r in r2) / len(r2)
        complete = not (mo == last_obs.strftime("%Y-%m") and mo == RETRIEVED.strftime("%Y-%m"))
        out.append([mo, f"{s3:.4f}", f"{s2:.4f}", len(rs), "yes" if complete else "no"])
    with open(MONTHLY, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["month", "spread_10y_3m_cmt", "spread_10y_2y_cmt", "days", "complete"])
        w.writerows(out)
    return len(out), dates[0], dates[-1]


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--extract":
        print("daily rows:", extract(sys.argv[2]))
    print("months, first day, last day:", monthly())
