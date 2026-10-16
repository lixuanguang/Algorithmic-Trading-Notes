"""Estrella and Trubin's spread from the Federal Reserve's H.15 release, monthly averages.

Source: Board of Governors, H.15 Selected Interest Rates, full data package (SDMX XML) from
  https://www.federalreserve.gov/datadownload/Output.aspx?rel=H15&filetype=zip   (retrieved 2026-10-16)
series RIFSGFSM03_N.B (3-month Treasury bill, secondary market, discount basis, business day) and
RIFLGFCY10_N.B (10-year Treasury constant maturity, business day); only observations with status "A".
Extract kept in h15-daily-3m-10y.csv (from 1962, when the 10-year series begins).

Transformation, as in Estrella and Trubin (2006), n. 4: bond-equivalent = 100*(365*d/100)/(360-91*d/100),
d the discount yield in percentage points; daily spread = 10-year CMT - bond-equivalent bill; monthly average
of business days. Checks: unique, increasing dates; no missing months; the month of the last observation
flagged incomplete when it is the retrieval month (October 2026).

Usage: python3 h15_monthly.py --extract H15_data.xml   (rebuild the daily extract)
       python3 h15_monthly.py                          (rebuild h15-spread-monthly.csv)
"""
import csv
import datetime as dt
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DAILY = os.path.join(HERE, "h15-daily-3m-10y.csv")
MONTHLY = os.path.join(HERE, "h15-spread-monthly.csv")
RETRIEVED = dt.date(2026, 10, 16)


def extract(xml_path):
    import xml.etree.ElementTree as ET
    want = {"RIFSGFSM03_N.B": "tb3m_discount", "RIFLGFCY10_N.B": "cmt_10y"}
    data = {v: {} for v in want.values()}
    cur = None
    for ev, el in ET.iterparse(xml_path, events=("start", "end")):
        tag = el.tag.split("}")[-1]
        if ev == "start" and tag == "Series":
            cur = want.get(el.get("SERIES_NAME"))
        elif ev == "end" and tag == "Obs":
            if cur and el.get("OBS_STATUS") == "A":
                data[cur][el.get("TIME_PERIOD")] = el.get("OBS_VALUE")
            el.clear()
        elif ev == "end" and tag == "Series":
            cur = None
    dates = sorted(d for d in set(data["tb3m_discount"]) & set(data["cmt_10y"]) if d >= "1962-01-01")
    with open(DAILY, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "tb3m_discount", "cmt_10y"])
        for d in dates:
            w.writerow([d, data["tb3m_discount"][d], data["cmt_10y"][d]])
    return len(dates)


def bond_equivalent(d):
    return 100 * (365 * d / 100) / (360 - 91 * d / 100)


def monthly():
    rows = list(csv.DictReader(open(DAILY)))
    dates = [r["date"] for r in rows]
    assert len(dates) == len(set(dates)) and dates == sorted(dates), "dates not unique and increasing"
    by = {}
    for r in rows:
        s = float(r["cmt_10y"]) - bond_equivalent(float(r["tb3m_discount"]))
        by.setdefault(r["date"][:7], []).append(s)
    months = sorted(by)
    y, m = map(int, months[0].split("-"))
    expected = []
    while f"{y:04d}-{m:02d}" <= months[-1]:
        expected.append(f"{y:04d}-{m:02d}")
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    assert months == expected, "gap in months"
    last = dt.date.fromisoformat(dates[-1]).strftime("%Y-%m")
    with open(MONTHLY, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["month", "spread_10y_3m_be", "days", "complete"])
        for mo in months:
            v = by[mo]
            done = not (mo == last and mo == RETRIEVED.strftime("%Y-%m"))
            w.writerow([mo, f"{sum(v) / len(v):.4f}", len(v), "yes" if done else "no"])
    return len(months), dates[0], dates[-1]


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--extract":
        print("daily rows:", extract(sys.argv[2]))
    print("months, first day, last day:", monthly())
