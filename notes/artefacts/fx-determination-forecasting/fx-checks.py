"""source verification (2026-10-17) (audit repair): focused checks for the failures found in fx_ppp_oos_test.py v1.

1. Outcome eligibility does not depend on future CPI: on synthetic series whose CPI stops early, forecasts are
   still made for months whose spot outcome exists (v1 needed the panel row, hence CPI, at t+h).
2. Stale-data rule: quarterly CPI is accepted four to six months after its quarter ends and refused at seven;
   monthly CPI must be exactly two months old.
3. Expanding training uses only outcomes known at the forecast date (t' + h <= t).
4. Rebuilt outputs: AUD and NZD predictors end in September 2025, not September 2026; the panel records CPI ages;
   the results label the portfolio as not executable; v1's outputs are preserved.
Run: uv run --frozen --no-editable python fx-checks.py   (numpy; under 1 s). Exits non-zero on failure.
"""

import csv
import hashlib
import importlib.util
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("fx", os.path.join(HERE, "fx_ppp_oos_test.py"))
fx = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fx)
fails = []


def same(name, got, want):
    ok = got == want
    print(f"  {'ok ' if ok else 'BAD'} {name}: {got} (want {want})")
    if not ok:
        fails.append(name)


print("== 2. stale-data rule")
q_cpi = {(2025, 1): 100.0}  # 2025Q1, dated at its first month; quarter ends March 2025
same("quarterly, July 2025 (age 4)", fx.known_price(q_cpi, (2025, 7), True), (100.0, 4))
same("quarterly, September 2025 (age 6)", fx.known_price(q_cpi, (2025, 9), True), (100.0, 6))
same("quarterly, October 2025 (age 7) refused", fx.known_price(q_cpi, (2025, 10), True), None)
same("quarterly, June 2025 (age 3) not yet known", fx.known_price(q_cpi, (2025, 6), True), None)
m_cpi = {(2025, 1): 100.0}
same("monthly, March 2025 uses January", fx.known_price(m_cpi, (2025, 3), False), (100.0, 2))
same(
    "monthly, April 2025 refuses a three-month-old value",
    fx.known_price(m_cpi, (2025, 4), False),
    None,
)

print("== 1 and 3. outcome eligibility and training cutoffs on synthetic data")
months = [fx.add((1980, 1), k) for k in range(240)]
spot = {"XXX": {t: 0.01 * math.sin(i / 7.0) for i, t in enumerate(months)}}
last_cpi = months[150]
pred = {"XXX": {t: {"z": 0.02 * math.cos(i / 5.0)} for i, t in enumerate(months) if t <= last_cpi}}
fx.START = months[70]
fc, ts, X, Y = fx.forecasts(spot, pred, "XXX", 12)
same("last forecast at the last predictor month (outcome from spot only)", fc[-1][0], last_cpi)
same(
    "outcome of the last forecast is the spot change to t+12",
    abs(fc[-1][2] - (spot["XXX"][fx.add(last_cpi, 12)] - spot["XXX"][last_cpi])) < 1e-15,
    True,
)
# training cutoff: refit by hand at the first forecast date using only pairs with t' + 12 <= t
t0 = fc[0][0]
tr = [k for k in ts if k < t0 and fx.add(k, 12) <= t0]
b1, b0 = np.polyfit([X[k] for k in tr], [Y[k] for k in tr], 1)
same(
    "first forecast equals an OLS fit on outcomes observed by its date only",
    abs(fc[0][1] - (b0 + b1 * X[t0])) < 1e-12,
    True,
)
tr_leaky = [k for k in ts if k < t0]
c1, c0 = np.polyfit([X[k] for k in tr_leaky], [Y[k] for k in tr_leaky], 1)
same(
    "...and differs from a fit that also uses the 11 unobserved outcomes",
    abs(fc[0][1] - (c0 + c1 * X[t0])) > 1e-6,
    True,
)

print("== 4. rebuilt outputs")
rows = list(csv.DictReader(open(os.path.join(HERE, "fx_ppp_monthly.csv"))))
for c in ("AUD", "NZD"):
    z = [r["month"] for r in rows if r["ccy"] == c and r["z_dev"]]
    same(f"{c} last eligible predictor", z[-1], "2025-09")
same(
    "ages recorded and within the rule",
    all(
        r["cpi_age_months"] in ("2", "4", "5", "6") for r in rows if r["predictor_eligible"] == "1"
    ),
    True,
)
res = open(os.path.join(HERE, "fx_ppp_results.txt")).read()
same("portfolio labelled not executable", "not an executable result" in res, True)
v1 = open(os.path.join(HERE, "superseded-first-run", "fx_ppp_monthly.csv"), "rb").read()
same("v1 panel preserved (SHA-256 prefix)", hashlib.sha256(v1).hexdigest()[:8], "da1bb9d4")

if fails:
    print("\nFAILED:", fails)
    sys.exit(1)
print("\nall checks passed")
