"""ev:fx-valuation-factors-oos: corrected rerun (v2, 17 October 2026) of the out-of-sample test of relative PPP
(the real exchange rate) against a random walk, on public FRED data. The first run (v1, same day) is kept unchanged
in superseded-first-run/.

Hypothesis, data, h, start date, training rule, portfolio, costs and decision rules are v1's, unchanged (written
before v1's results were computed, by the batch record's account; committed with the results, so not preregistered):
  ds_{t,t+h} = a + b z_t + e, b < 0, z_t the deviation of the log real exchange rate from its expanding mean;
  statistical support if the pooled h = 12 OOS R^2 against a random walk is > 0 and the Clark-West t > 1.65;
  economic support if the net excess-return portfolio's mean is positive with Newey-West t > 2.
v2 repairs, found by an audit after v1's results were seen (not a new protocol, not preregistered):
  1. Predictor and outcome eligibility are separate. A month t is predictor-eligible if the price levels known at
     t pass the stale-data rule below; the outcome ds_{t,t+h} needs only spot rates at t and t+h. v1 built one
     panel that required CPI at t+h as well, so an outcome was dropped whenever future CPI was missing.
  2. Stale-data rule. Monthly CPI: the observation for month t-2 (a two-month publication lag) and nothing older;
     if it is missing the month is not predictor-eligible. Quarterly CPI (AUD, NZD): the latest quarter ending at
     least four months before t, accepted only if it ended at most six months before t (one normal quarterly
     cycle); v1 carried the last quarter (2025Q1) forward without limit, to September 2026. Ages and effective
     endpoints are printed.
  3. Expanding training is unchanged: at t, only pairs whose outcome month t'+h <= t enter the fit.
Limitations kept explicit: revised CPI, not real-time vintages (a small look-ahead); spot rates are monthly averages
  of noon buying rates (H.10/G.5), not month-end rates, so the portfolio is a statistical return on averaged
  prices, not an executable trading result, and averaging induces autocorrelation in monthly changes; the carry
  leg uses three-month interbank rates (IR3TIB01), not the forward points or funding rates a trader would pay;
  the 5 bp cost per unit of turnover is an assumption. EUR is excluded (short history).
Inference repair (derivatives and empirical validation (2026-10-17), after the results were seen; v2 as committed in 012aa19 is kept in
  superseded-row-lag-inference/). The pooled Clark-West t stacked currency rows and applied Newey-West to the stacked vector, so it
  ignored contemporaneous dependence across currencies (all nine are dollar rates, so their forecast errors share the
  dollar's move) and mixed currencies at the stacking boundaries. It now uses panel_nw_t: the CW scores are summed
  across currencies within each forecast-origin month, and the Bartlett/Newey-West long-run variance is taken over
  calendar months (h-1 lags, the protocol's lag count, now in months; h lags as a sensitivity, because 12-month changes
  of monthly-average prices overlap for h months, not h-1). Each currency-month keeps weight 1/N, so the pooled mean
  and the pooled OOS R^2 are unchanged; only the standard error changes. Forecast-origin months are kept with each score.
Run: uv run python fx_ppp_oos_test.py <folder with the FRED csv files>  (numpy only; about 2 s).
Writes fx_ppp_monthly.csv (derived panel) next to this script.
"""

# standard library imports
import csv
import math
import os
import sys

# third party library imports
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CCY = {  # spot id, quoted as foreign per USD?, CPI id, quarterly?, rate id
    "JPY": ("EXJPUS", True, "JPNCPIALLMINMEI", False, "IR3TIB01JPM156N"),
    "GBP": ("EXUSUK", False, "GBRCPIALLMINMEI", False, "IR3TIB01GBM156N"),
    "CHF": ("EXSZUS", True, "CHECPIALLMINMEI", False, "IR3TIB01CHM156N"),
    "CAD": ("EXCAUS", True, "CANCPIALLMINMEI", False, "IR3TIB01CAM156N"),
    "AUD": ("EXUSAL", False, "AUSCPIALLQINMEI", True, "IR3TIB01AUM156N"),
    "NZD": ("EXUSNZ", False, "NZLCPIALLQINMEI", True, "IR3TIB01NZM156N"),
    "SEK": ("EXSDUS", True, "SWECPIALLMINMEI", False, "IR3TIB01SEM156N"),
    "NOK": ("EXNOUS", True, "NORCPIALLMINMEI", False, "IR3TIB01NOM156N"),
    "DKK": ("EXDNUS", True, "DNKCPIALLMINMEI", False, "IR3TIB01DKM156N"),
}
MONTHLY_LAG = 2
QTR_MIN_AGE, QTR_MAX_AGE = 4, 6
START = (1985, 1)


def load(src, i):
    out = {}
    with open(os.path.join(src, i + ".csv")) as f:
        r = csv.reader(f)
        next(r)
        for d, v in r:
            if v not in ("", "."):
                y, m, _ = map(int, d.split("-"))
                out[(y, m)] = float(v)
    return out


def add(ym, k):
    n = ym[0] * 12 + ym[1] - 1 + k
    return (n // 12, n % 12 + 1)


def mdiff(a, b):
    return (a[0] * 12 + a[1]) - (b[0] * 12 + b[1])


def known_price(cpi, t, quarterly):
    """(price level, age in months of the observation's last month) known at t under the stale-data rule, or None."""
    if not quarterly:
        k = add(t, -MONTHLY_LAG)
        return (cpi[k], MONTHLY_LAG) if k in cpi else None
    # quarterly series are dated at the quarter's first month; the quarter ends two months later
    cands = [k for k in cpi if mdiff(t, add(k, 2)) >= QTR_MIN_AGE]
    if not cands:
        return None
    k = max(cands)
    age = mdiff(t, add(k, 2))
    return (cpi[k], age) if age <= QTR_MAX_AGE else None


def build(src):
    us_cpi, us_r = load(src, "CPIAUCNS"), load(src, "IR3TIB01USM156N")
    spot, pred = {}, {}
    for c, (sid, inv, cid, qtr, rid) in CCY.items():
        sp, cpi, rate = load(src, sid), load(src, cid), load(src, rid)
        spot[c] = {t: (-math.log(v) if inv else math.log(v)) for t, v in sp.items()}
        rows, qs = {}, []
        for t in sorted(spot[c]):
            kp = known_price(cpi, t, qtr)
            ku = add(t, -MONTHLY_LAG)
            if kp is None or ku not in us_cpi:
                continue
            q = spot[c][t] + math.log(kp[0]) - math.log(us_cpi[ku])
            qs.append(q)
            rows[t] = dict(
                q=q,
                age=kp[1],
                z=(q - sum(qs) / len(qs)) if len(qs) >= 60 else None,
                i=rate.get(t),
                iu=us_r.get(t),
            )
        pred[c] = rows
    return spot, pred


def nw_t(x, lags):
    x = np.asarray(x)
    xc = x - x.mean()
    n = len(x)
    s2 = (xc @ xc) / n + 2 * sum(
        (1 - L / (lags + 1)) * (xc[L:] @ xc[:-L]) / n for L in range(1, lags + 1)
    )
    return x.mean() / math.sqrt(s2 / n)


def panel_nw_t(rows, lags):
    """t statistic for the mean of pooled scores rows = [(forecast-origin month, score), ...], in calendar time.

    The scores are summed within each origin month (S_m, n_m rows), giving one observation per calendar month; months
    with no rows count as zero on a complete monthly grid. With mu the pooled mean (every row weighted 1/N), the
    long-run variance of sum_m (S_m - n_m mu) is estimated with Bartlett weights over `lags` calendar months, and
    Var(mu) = LRV / N^2. Contemporaneous dependence across currencies is absorbed in S_m; overlap is handled by the lags.
    With one row per month this equals nw_t.
    """
    by = {}
    for m, v in rows:
        s, n = by.get(m, (0.0, 0))
        by[m] = (s + v, n + 1)
    lo, hi = min(by), max(by)
    grid = [add(lo, k) for k in range(mdiff(hi, lo) + 1)]
    S = np.array([by.get(m, (0.0, 0))[0] for m in grid])
    n = np.array([by.get(m, (0.0, 0))[1] for m in grid])
    N = n.sum()
    mu = S.sum() / N
    u = S - n * mu
    lrv = u @ u + 2 * sum((1 - L / (lags + 1)) * (u[L:] @ u[:-L]) for L in range(1, lags + 1))
    return mu / math.sqrt(lrv / N**2)


def forecasts(spot, pred, c, h):
    """Expanding-OLS forecasts for currency c: list of (t, forecast, actual)."""
    ts = [t for t in sorted(pred[c]) if pred[c][t]["z"] is not None and add(t, h) in spot[c]]
    X = {t: pred[c][t]["z"] for t in ts}
    Y = {t: spot[c][add(t, h)] - spot[c][t] for t in ts}
    out = []
    for j, t in enumerate(ts):
        if t < START:
            continue
        tr = [k for k in ts[:j] if add(k, h) <= t]  # only outcomes known at t
        if len(tr) < 60:
            continue
        A = np.column_stack([np.ones(len(tr)), [X[k] for k in tr]])
        b = np.linalg.lstsq(A, np.array([Y[k] for k in tr]), rcond=None)[0]
        out.append((t, b[0] + b[1] * X[t], Y[t]))
    return out, ts, X, Y


def main(src):
    spot, pred = build(src)
    with open(os.path.join(HERE, "fx_ppp_monthly.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "ccy",
                "month",
                "s_ln_usd_per_fx",
                "predictor_eligible",
                "cpi_age_months",
                "q_ln_real",
                "z_dev",
                "i_fx",
                "i_us",
            ]
        )
        for c in CCY:
            for t in sorted(spot[c]):
                r = pred[c].get(t)
                w.writerow(
                    [
                        c,
                        f"{t[0]}-{t[1]:02d}",
                        f"{spot[c][t]:.6f}",
                        int(r is not None),
                        "" if r is None else r["age"],
                        "" if r is None else f"{r['q']:.6f}",
                        "" if r is None or r["z"] is None else f"{r['z']:.6f}",
                        "" if r is None or r["i"] is None else r["i"],
                        "" if r is None or r["iu"] is None else r["iu"],
                    ]
                )

    print(
        "Samples per currency: spot range; predictor-eligible range (first z, last eligible month); CPI ages"
    )
    for c in CCY:
        zt = [t for t in sorted(pred[c]) if pred[c][t]["z"] is not None]
        ages = [pred[c][t]["age"] for t in zt]
        print(
            f"  {c}: spot {min(spot[c])}-{max(spot[c])}; z {zt[0]}-{zt[-1]}; age {min(ages)}-{max(ages)} months "
            f"(mean {np.mean(ages):.1f}); spot months after the last eligible predictor: {sum(t > zt[-1] for t in spot[c])}"
        )

    stat_ok = False
    for h in (1, 12):
        sse_m = sse_rw = 0.0
        cw_all, bsum = [], []
        print(
            f"\n== h = {h} months: expanding OLS of ds on z, forecasts from {START[0]}-{START[1]:02d}"
        )
        for c in CCY:
            fc, ts, X, Y = forecasts(spot, pred, c, h)
            f = np.array([x[1] for x in fc])
            a = np.array([x[2] for x in fc])
            r2 = 1 - ((a - f) ** 2).sum() / (a**2).sum()
            A = np.column_stack([np.ones(len(ts)), [X[t] for t in ts]])
            bfull = np.linalg.lstsq(A, np.array([Y[t] for t in ts]), rcond=None)[0]
            bsum.append(bfull[1])
            print(
                f"  {c}: n = {len(a)} ({fc[0][0]} to {fc[-1][0]}), OOS R^2 vs RW = {r2 * 100:+.2f}%, full-sample b = {bfull[1]:+.4f}"
            )
            sse_m += ((a - f) ** 2).sum()
            sse_rw += (a**2).sum()
            cw_all.extend(zip([x[0] for x in fc], a**2 - ((a - f) ** 2 - f**2)))
        lags = max(h - 1, 0)
        cwt = panel_nw_t(cw_all, lags)
        r2p = 1 - sse_m / sse_rw
        print(
            f"  pooled OOS R^2 vs RW = {r2p * 100:+.2f}%, Clark-West t = {cwt:+.2f} (scores summed by forecast-origin "
            f"month, Newey-West {lags} calendar-month lags); sensitivity with {h} lags: {panel_nw_t(cw_all, h):+.2f}; "
            f"superseded row-stacked t: {nw_t([v for _, v in cw_all], lags):+.2f}"
        )
        print(
            f"  full-sample slopes negative for {sum(b < 0 for b in bsum)} of {len(bsum)} currencies"
        )
        if h == 12:
            stat_ok = r2p > 0 and cwt > 1.65

    # statistical portfolio on monthly-average rates (not an executable trading result)
    alltimes = sorted(set().union(*[set(s) for s in spot.values()]))
    spot_r, exc, costs, used = [], [], [], []
    prev_w = {}
    for t in alltimes:
        if t < START:
            continue
        t1 = add(t, 1)
        av = [c for c in CCY if t in pred[c] and pred[c][t]["z"] is not None and t1 in spot[c]]
        if len(av) < 6:
            continue
        av.sort(key=lambda c: pred[c][t]["z"])
        wts = {c: 1 / 3 for c in av[:3]}
        wts.update({c: -1 / 3 for c in av[-3:]})
        turn = sum(abs(wts.get(c, 0) - prev_w.get(c, 0)) for c in set(wts) | set(prev_w))
        prev_w = wts
        ds = sum(wv * (spot[c][t1] - spot[c][t]) for c, wv in wts.items())
        spot_r.append(ds)
        costs.append(0.0005 * turn)
        used.append(t)
        if all(pred[c][t]["i"] is not None and pred[c][t]["iu"] is not None for c in wts):
            exc.append(
                (
                    ds
                    + sum(
                        wv * (pred[c][t]["i"] - pred[c][t]["iu"]) / 1200 for c, wv in wts.items()
                    ),
                    0.0005 * turn,
                )
            )

    def summ(label, x):
        x = np.array(x)
        t = nw_t(x, 12)
        print(
            f"  {label}: n = {len(x)}, mean {x.mean() * 1200:+.2f}%/yr, vol {x.std(ddof=1) * math.sqrt(12) * 100:.2f}%/yr, "
            f"Sharpe {x.mean() / x.std(ddof=1) * math.sqrt(12):+.2f}, NW t = {t:+.2f}"
        )
        return x.mean(), t

    print(
        f"\n== Value portfolio on monthly-average rates (long 3 cheapest, short 3 dearest by z), {used[0]} to {used[-1]}"
    )
    print(
        "   A statistical portfolio return on averaged prices with interbank-rate carry: not an executable result."
    )
    summ("spot, gross", spot_r)
    summ("spot, net of 5 bp turnover cost", np.array(spot_r) - np.array(costs))
    ex = np.array([e for e, _ in exc])
    exn = np.array([e - c for e, c in exc])
    summ("with interest differential, gross", ex)
    m, tt = summ("with interest differential, net of costs", exn)
    print(
        f"  mean turnover cost {np.mean(costs) * 1200:.2f}%/yr; breakeven cost per unit turnover "
        f"{np.mean(spot_r) / np.mean(np.array(costs) / 0.0005) * 1e4:.1f} bp (spot)"
    )
    econ_ok = m > 0 and tt > 2
    print(
        f"\nVerdict: statistical (h = 12) {'supported' if stat_ok else 'not supported'}; "
        f"economic (statistical portfolio) {'supported' if econ_ok else 'not supported'}"
    )


if __name__ == "__main__":
    main(sys.argv[1])
