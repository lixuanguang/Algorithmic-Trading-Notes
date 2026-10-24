"""ev:global-macro-returns-after-2013: a bounded run of the protocol recorded in the pathway backlog on 17 October 2026
(batch of that date, before any index data were obtained), on the only public monthly series found, 2022 onward.

Protocol (as recorded): does a named macro hedge-fund index show positive returns and low or negative co-movement
with equities in equity down months? Monthly net-of-fee index returns with the download date (indices revise and
backfill); benchmark Ken French's Mkt (public proxy for the S&P 500 total return); down months = benchmark excess
return below zero; report mean, volatility, Sharpe with Lo's standard error, correlation and beta separately in down
and up months with confidence intervals, and the mean in the ten worst benchmark months; 'crisis protection' only if
the down-month mean is positive with t > 2.
Choices fixed on 17 October 2026 before computing, because the public data differ from those the protocol assumed:
  * Series: Barclay Global Macro Index, monthly net returns, as displayed on BarclayHedge's public page on 2026-10-17
    (local copy; the page shows January 2022 onward only). The protocol's start, January 2014, cannot be met.
  * Months the page marks as estimated (August and September 2026) are excluded; the sample ends July 2026, the last
    complete month with French data (French file ends August 2026).
  * Index excess return = index return - French RF; Sharpe on excess returns, monthly, with Lo's IID standard error
    sqrt((1 + SR^2/2)/T) (normal-moment form; see meth:sharpe-ratio-standard-error for its conditions).
  * Confidence intervals: correlation by Fisher z; beta and means by OLS / t with T-1 df (independence assumed).
  * Ten worst benchmark months: the ten lowest Mkt-RF months in the window.
This is not the protocol's 2014-2026 test: the window is 55 months, about 20 of them down months, and the index's
history before 2022 was not available without registration. Results are bounded accordingly.
Run: uv run --frozen --no-editable python global_macro_down_months_test.py <BarclayHedge html> <French factors csv>   (numpy, scipy; under 1 s).
Writes global_macro_monthly.csv next to this script.
"""

import csv
import html
import math
import os
import re
import sys

import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))


def barclay(path):
    t = open(path, errors="replace").read()
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
    t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t)))
    block = t[t.index("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec YTD") :]
    out = {}
    for m in re.finditer(r"(20\d\d) ((?:\S+ ){13})", block):
        y = int(m.group(1))
        cells = m.group(2).split()[:12]
        for k, c in enumerate(cells):
            if re.fullmatch(r"-?\d+\.\d+%", c):
                out[(y, k + 1)] = float(c[:-1]) / 100
    return out


def french(path):
    out = {}
    for line in open(path):
        p = [x.strip() for x in line.split(",")]
        if len(p[0]) == 6 and p[0].isdigit():
            out[(int(p[0][:4]), int(p[0][4:]))] = (float(p[1]) / 100, float(p[4]) / 100)
        elif out and (not p[0] or not p[0].isdigit()):
            break
    return out


def main(bh_path, ff_path):
    idx, ff = barclay(bh_path), french(ff_path)
    months = sorted(m for m in idx if m in ff and m <= (2026, 7))
    rows = [(m, idx[m], ff[m][0], ff[m][1]) for m in months]
    with open(os.path.join(HERE, "global_macro_monthly.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["month", "barclay_global_macro", "mkt_rf", "rf"])
        for m, r, mk, rf in rows:
            w.writerow([f"{m[0]}-{m[1]:02d}", f"{r:.4f}", f"{mk:.4f}", f"{rf:.4f}"])
    r = np.array([x[1] for x in rows])
    mk = np.array([x[2] for x in rows])
    rf = np.array([x[3] for x in rows])
    ex = r - rf
    T = len(r)
    sr = ex.mean() / ex.std(ddof=1)
    print(
        f"Window {months[0]} to {months[-1]}, T = {T} months (Barclay Global Macro Index, net; French Mkt-RF)"
    )
    print(
        f"All months: mean {r.mean() * 100:+.2f}%/month, vol {r.std(ddof=1) * math.sqrt(12) * 100:.2f}%/yr, "
        f"monthly Sharpe (excess) {sr:+.3f} (Lo IID s.e. {math.sqrt((1 + sr**2 / 2) / T):.3f}), "
        f"annualised {sr * math.sqrt(12):+.2f}"
    )
    for name, sel in (("down", mk < 0), ("up", mk >= 0)):
        a, b = r[sel], mk[sel]
        n = len(a)
        tmean = a.mean() / (a.std(ddof=1) / math.sqrt(n))
        rho = np.corrcoef(a, b)[0, 1]
        z = np.arctanh(rho)
        half = 1.96 / math.sqrt(n - 3)
        lr = stats.linregress(b, a)
        tcrit = stats.t.ppf(0.975, n - 2)
        print(
            f"{name:5s} months (n {n}): mean {a.mean() * 100:+.2f}% (t {tmean:+.2f}), correlation {rho:+.2f} "
            f"[{math.tanh(z - half):+.2f}, {math.tanh(z + half):+.2f}], beta {lr.slope:+.3f} "
            f"[{lr.slope - tcrit * lr.stderr:+.3f}, {lr.slope + tcrit * lr.stderr:+.3f}]"
        )
        if name == "down":
            down_mean, down_t = a.mean(), tmean
    worst = np.argsort(mk)[:10]
    print(
        f"ten worst benchmark months: benchmark mean {mk[worst].mean() * 100:+.2f}%, index mean {r[worst].mean() * 100:+.2f}% "
        f"({', '.join(f'{months[i][0]}-{months[i][1]:02d}' for i in sorted(worst))})"
    )
    ok = down_mean > 0 and down_t > 2
    print(
        f"Verdict (pre-set rule): crisis protection {'supported' if ok else 'not supported'} in this window"
    )


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
