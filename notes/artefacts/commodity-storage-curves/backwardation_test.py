"""ev:backwardation-scarcity-or-premium: corrected rerun (v2, 17 October 2026) of the bounded test on EIA's public
NYMEX futures and inventory series. The first run (v1, same day) is kept unchanged in superseded-first-run/.

Hypotheses and decision rules are the v1 protocol's, unchanged (written before v1's results were computed, by the batch
record's account; committed together with the results, so not a preregistration):
  S (scarcity, theory of storage): beta_S < 0 in  B_t = a + beta_S * I_t + e_t, supported if |t| > 2.
  P (premium): beta_P > 0 in  r_{t+1} = a + beta_P * B_t + u_{t+1} with |t| > 2, and an out-of-sample R^2 above the
    expanding historical mean with a Clark-West t above 1.65 (expanding OLS from 120 months).
The v2 corrections are implementation repairs found by an audit after v1's results were seen; they are not a new
protocol and are not preregistered. What changed:
  1. Contract identity and complete holding periods. A month pair (t, t1) is used only if (a) both are the last
     observed trading day of their calendar month and the data continue into the following month (so the final,
     incomplete month, which ends on 5 April 2024, is excluded: its C1 is the May 2024 WTI contract, not March 28's
     C2, the June contract), (b) t1 is the month after t, and (c) the delivery month of C2 at t equals that of C1 at
     t1 under the NYMEX last-trading-day rules (Rules 200102.F and 220102.F, local copies). Business days are the
     dates in EIA's daily series. For Henry Hub, the data show an earlier roll before 1997 (see the roll check
     printed below), so identity is required under the current rule and under expiry 5 and 6 business days before
     the delivery month.
  2. Price-only and inventory-dependent samples are separated. P (r on B), its out-of-sample test and the timing
     rule use every identity-valid month; S, r on I and the joint regression need the inventory deviation. v1
     restricted everything to the inventory sample, which left gas with 111 months and no out-of-sample test.
  3. Inventory availability. v1 used the last weekly observation dated at least 5 days before t, which for gas
     (Thursday release) admitted a report not yet published on Wednesday month-ends. v2 uses a documented
     conservative convention from EIA's published schedules (local copies of 17 October 2026: WPSR standard
     Wednesday 10:30 ET, WNGSR Thursday 10:30 ET; holiday releases up to Thursday noon (WPSR) or Friday 10:30
     (WNGSR), and Monday 29 December 2025 for the week ending 19 December 2025). A week ending Friday F is usable at
     settlement t if t >= F + 6 days (crude) or F + 7 days (gas), or F + 11 days when 25 December or 1 January falls
     in F+1..F+7. Release schedules before 2025 were not obtained; a sensitivity uses F + 14 days throughout.
  4. Statistical association versus executable result. The regressions and the "statistical" timing rule use
     settlement t both to form B_t and to enter: closing-price associations, not trading results. The executable
     variant forms the signal at settlement t, enters at the next trading day's settlement and exits at the
     settlement of the first trading day after t1, in the same contract (identity checked again). Settlement-price
     fills (e.g. trade-at-settlement orders) and the two-tick round-trip cost are assumptions, not measured.
  5. The v1 message "months with |r| >= 50% dropped" was wrong: those months were counted, never dropped. v2 says
     they are retained.
Data (EIA, public domain; ignored reading_materials/source-verification/empirical): RCLC1-4 and RNGC1-4 daily (end 5 April
  2024); WCESTUS1 weekly (U.S. crude stocks excl. SPR); NW2_EPG0_SWO_R48_BCF weekly (Lower-48 working gas, from 2010).
Inventory deviation I_t: ln(stocks) at the latest usable week minus the mean of ln(stocks) in the same ISO week of
  the previous five years.
Costs: two ticks per round trip (WTI $0.01, NG $0.001 per tick; NYMEX Chapters 200 and 220), an assumption.
Inference: OLS with Newey-West (12 lags). Returns are futures (collateral-excess) returns.
Run: uv run --frozen --no-editable --group empirical python backwardation_test.py <folder with EIA_*.xls>  (needs numpy and xlrd; about 3 s).
Writes backwardation_monthly.csv next to this script and prints the results.
"""

# standard library imports
import bisect
import csv
import datetime as dt
import math
import os
import sys

# third party library imports
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TICK = {"WTI": 0.01, "NG": 0.001}
LAG = {
    "WTI": 6,
    "NG": 7,
}  # days after the week-ending Friday at which the report is treated as public


def series(src, name):
    # third party library imports
    import xlrd

    b = xlrd.open_workbook(os.path.join(src, f"EIA_{name}.xls"))
    sh = b.sheet_by_name("Data 1")
    out = {}
    for r in range(3, sh.nrows):
        d, v = sh.row_values(r)[:2]
        if d == "" or v == "":
            continue
        out[dt.date(1899, 12, 30) + dt.timedelta(days=int(d))] = float(v)
    return out


def bd_before(cal, x, k):
    """k-th trading day strictly before date x in the sorted calendar cal (None before the calendar starts)."""
    if x is None:
        return None
    i = bisect.bisect_left(cal, x)
    return cal[i - k] if i - k >= 0 else None


def expiry(market, cal, y, m, ng_days=3):
    """Last trading day of the contract for delivery month (y, m) under the NYMEX rule, on the data calendar."""
    if dt.date(y, m, 1) > cal[-1]:
        return None  # beyond the data calendar: not computable
    if (
        market == "NG"
    ):  # Rule 220102.F: third business day prior to the first day of the delivery month
        return bd_before(cal, dt.date(y, m, 1), ng_days)
    py, pm = (y, m - 1) if m > 1 else (y - 1, 12)
    x = dt.date(py, pm, 25)  # Rule 200102.F
    calset = set(cal)
    if x in calset:
        return bd_before(cal, x, 3)
    return bd_before(cal, bd_before(cal, x, 1), 3)


def delivery(market, cal, d, nth=1, ng_days=3):
    """Delivery month (y, m) of the nth nearby contract on trading date d."""
    y, m = d.year, d.month
    while True:
        e = expiry(market, cal, y, m, ng_days)
        if e is None and dt.date(y, m, 1) > cal[-1]:
            # expiry falls after the data end; it is certainly after d when its anchor date (the 1st of the
            # delivery month for NG, the 25th of the month before for WTI) is more than ten days after d
            anchor = (
                dt.date(y, m, 1)
                if market == "NG"
                else dt.date(y if m > 1 else y - 1, m - 1 if m > 1 else 12, 25)
            )
            if (anchor - d).days > 10:
                break
            return None
        if e is not None and e >= d:
            break
        y, m = (y, m + 1) if m < 12 else (y + 1, 1)
    for _ in range(nth - 1):
        y, m = (y, m + 1) if m < 12 else (y + 1, 1)
    return (y, m)


RULES = {"WTI": (3,), "NG": (3, 5, 6)}


def same_contract(market, cal, d0, n0, d1, n1):
    return all(
        delivery(market, cal, d0, n0, k) == delivery(market, cal, d1, n1, k) for k in RULES[market]
    )


def complete_month_ends(cal):
    """Last trading day of each calendar month whose following month also has data."""
    out = []
    for i, d in enumerate(cal[:-1]):
        if cal[i + 1].month != d.month:
            out.append(d)
    return out


def available_week(market, stocks_dates, t, extra=None):
    """Latest weekly observation (week ending Friday F) treated as public at settlement on date t."""
    i = bisect.bisect_right(stocks_dates, t)
    for F in reversed(
        stocks_dates[max(0, i - 4) : i]
    ):  # the usable week is among the last few before t
        if extra is not None:
            lag = extra
        else:
            lag = LAG[market]
            if any(
                ((F + dt.timedelta(days=k)).month, (F + dt.timedelta(days=k)).day)
                in ((12, 25), (1, 1))
                for k in range(1, 8)
            ):
                lag = 11
        if F + dt.timedelta(days=lag) <= t:
            return F
    return None


def inv_dev(stocks, F):
    if F is None:
        return None
    wk = F.isocalendar()[1]
    hist = [
        math.log(v)
        for e, v in stocks.items()
        if e.isocalendar()[1] == wk and F.year - 5 <= e.year < F.year
    ]
    if len(hist) < 5:
        return None
    return math.log(stocks[F]) - sum(hist) / len(hist)


def ols_nw(y, X, lags=12):
    X = np.column_stack([np.ones(len(y)), X])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X @ b
    S = (X * e[:, None]).T @ (X * e[:, None])
    for L in range(1, lags + 1):
        w = 1 - L / (lags + 1)
        G = (X[L:] * e[L:, None]).T @ (X[:-L] * e[:-L, None])
        S += w * (G + G.T)
    XtXi = np.linalg.inv(X.T @ X)
    V = XtXi @ S @ XtXi
    return b, b / np.sqrt(np.diag(V))


def oos(y, x, start=120):
    if len(y) <= start + 12:
        return float("nan"), float("nan"), 0
    f_m, f_r, act = [], [], []
    for t in range(start, len(y)):
        X = np.column_stack([np.ones(t), x[:t]])
        b = np.linalg.lstsq(X, y[:t], rcond=None)[0]
        f_r.append(b[0] + b[1] * x[t])
        f_m.append(y[:t].mean())
        act.append(y[t])
    f_m, f_r, act = map(np.array, (f_m, f_r, act))
    r2 = 1 - ((act - f_r) ** 2).sum() / ((act - f_m) ** 2).sum()
    cw = (act - f_m) ** 2 - ((act - f_r) ** 2 - (f_m - f_r) ** 2)
    return r2, cw.mean() / (cw.std(ddof=1) / math.sqrt(len(cw))), len(act)


def build(market, c1, c2, c4, st):
    """Monthly rows with validity flags. Returns rows and a list of excluded month pairs with reasons."""
    cal = sorted(set(c1) & set(c2))
    ends = complete_month_ends(cal)
    stock_dates = sorted(st)
    rows, excluded = [], []
    for i, t in enumerate(ends):
        nxt = ends[i + 1] if i + 1 < len(ends) else None
        if nxt is None:
            last = cal[-1]
            excluded.append((t, f"no complete following month (data end {last})"))
            continue
        if (nxt.year * 12 + nxt.month) - (t.year * 12 + t.month) != 1:
            excluded.append((t, "gap in months"))
            continue
        if not same_contract(market, cal, t, 2, nxt, 1):
            excluded.append((t, "C2 at t is not C1 at t+1"))
            continue
        e0, e1 = cal[cal.index(t) + 1], cal[cal.index(nxt) + 1]
        exe_ok = same_contract(market, cal, t, 2, e0, 2) and same_contract(market, cal, t, 2, e1, 1)
        B = math.log(c1[t] / c2[t])
        B4 = math.log(c1[t] / c4[t]) / 3 if t in c4 and c4[t] > 0 else float("nan")
        r = c1[nxt] / c2[t] - 1
        rnet = (c1[nxt] - c2[t] - 2 * TICK[market]) / c2[t]
        if exe_ok and c2[e0] > 0:
            rx = c1[e1] / c2[e0] - 1
            rxnet = (c1[e1] - c2[e0] - 2 * TICK[market]) / c2[e0]
        else:
            rx = rxnet = None
        F = available_week(market, stock_dates, t)
        F14 = available_week(market, stock_dates, t, extra=14)
        rows.append(
            dict(
                t=t,
                t1=nxt,
                e0=e0,
                e1=e1,
                B=B,
                B4=B4,
                r=r,
                rnet=rnet,
                rx=rx,
                rxnet=rxnet,
                F=F,
                I=inv_dev(st, F),
                I14=inv_dev(st, F14),
                dC2=delivery(market, cal, t, 2),
                dC1n=delivery(market, cal, nxt, 1),
            )
        )
    return cal, rows, excluded


def roll_check(market, c1, c2, cal, years):
    """Mean of (|C1(d+1)-C1(d)| - |C1(d+1)-C2(d)|)/|C2(d)| at the rule's expiry d shifted by k trading days, over
    expiries with |C1-C2|/|C2| >= 1%. Positive at k = 0 and lower elsewhere supports the rule.
    """
    out = {}
    for k in range(-3, 4):
        v = []
        for y in years:
            for m in range(1, 13):
                e = expiry(market, cal, y, m)
                if e is None or e <= cal[5] or e >= cal[-5]:
                    continue
                i = cal.index(e)
                if abs(c1[e] - c2[e]) / abs(c2[e]) < 0.01:
                    continue
                d, n = cal[i + k], cal[i + k + 1]
                v.append((abs(c1[n] - c1[d]) - abs(c1[n] - c2[d])) / abs(c2[d]))
        out[k] = (float(np.mean(v)) if v else float("nan"), len(v))
    return out


def summarise(market, rows, excluded, c1, c2, cal):
    print(f"\n== {market}")
    for t, why in excluded:
        if why != "gap in months":
            print(f"  excluded month-end {t}: {why}")
    print(f"  excluded for gaps in months: {sum(w == 'gap in months' for _, w in excluded)}")
    blocks = [(a, min(a + 4, cal[-1].year)) for a in range(cal[0].year, cal[-1].year + 1, 5)]
    print(
        "  roll check (mean score x100 at offset -1 / 0 / +1 trading days from the rule expiry; n):"
    )
    for a, b in blocks:
        rc = roll_check(market, c1, c2, cal, range(a, b + 1))
        print(
            f"    {a}-{b}: {rc[-1][0] * 100:+.2f} / {rc[0][0] * 100:+.2f} / {rc[1][0] * 100:+.2f}  (n {rc[0][1]})"
        )
    allr = rows
    inv = [x for x in rows if x["I"] is not None]
    B = np.array([x["B"] for x in allr])
    r = np.array([x["r"] for x in allr])
    rn = np.array([x["rnet"] for x in allr])
    print(
        f"  price-only sample: {allr[0]['t']} to {allr[-1]['t']}, n = {len(allr)} (identity-valid, complete months)"
    )
    print(f"  inventory sample : {inv[0]['t']} to {inv[-1]['t']}, n = {len(inv)}")
    Bi = np.array([x["B"] for x in inv])
    B4i = np.array([x["B4"] for x in inv])
    ri = np.array([x["r"] for x in inv])
    Ii = np.array([x["I"] for x in inv])
    bS, tS = ols_nw(Bi, Ii)
    print(f"  S: B on I (inventory sample)        beta_S = {bS[1]:+.4f}  t = {tS[1]:+.2f}")
    ok4 = ~np.isnan(B4i)
    b4, t4 = ols_nw(B4i[ok4], Ii[ok4])
    print(f"  S (C1/C4 slope)                     beta   = {b4[1]:+.4f}  t = {t4[1]:+.2f}")
    inv14 = [x for x in rows if x["I14"] is not None]
    b14, t14 = ols_nw(np.array([x["B"] for x in inv14]), np.array([x["I14"] for x in inv14]))
    print(
        f"  S sensitivity, report lag F+14 days : beta_S = {b14[1]:+.4f}  t = {t14[1]:+.2f}  (n {len(inv14)})"
    )
    bP, tP = ols_nw(r, B)
    print(f"  P: r on B (price-only sample)       beta_P = {bP[1]:+.4f}  t = {tP[1]:+.2f}")
    bI, tI = ols_nw(ri, Ii)
    print(f"  P: r on I (inventory sample)        beta   = {bI[1]:+.4f}  t = {tI[1]:+.2f}")
    bJ, tJ = ols_nw(ri, np.column_stack([Bi, Ii]))
    print(
        f"  P: r on B and I (inventory sample)  beta_B = {bJ[1]:+.4f} (t {tJ[1]:+.2f}), beta_I = {bJ[2]:+.4f} (t {tJ[2]:+.2f})"
    )
    r2, cw, n = oos(r, B)
    if n:
        print(
            f"  P OOS (price-only, from month 121): R^2 = {r2 * 100:+.2f}%  Clark-West t = {cw:+.2f}  n = {n}"
            f"  (first forecast {allr[120]['t']})"
        )
    else:
        print("  P OOS: not computed (fewer than 132 months)")
    bk = B > 0
    print(
        "  statistical, settlement-to-settlement (signal and entry at the same settlement; not executable):"
    )
    print(
        f"    mean monthly r: backwardated {r[bk].mean() * 100:+.2f}% (n {bk.sum()}), contango {r[~bk].mean() * 100:+.2f}% (n {(~bk).sum()})"
    )
    ls = np.where(bk, rn, -r - (r - rn))
    print(
        f"    timing rule (long if B>0 else short), net of 2 ticks: mean {ls.mean() * 100:+.2f}%/month, "
        f"annualised Sharpe {ls.mean() / ls.std(ddof=1) * math.sqrt(12):+.2f}"
    )
    ex = [x for x in allr if x["rx"] is not None]
    rx = np.array([x["rx"] for x in ex])
    rxn = np.array([x["rxnet"] for x in ex])
    bx = np.array([x["B"] for x in ex]) > 0
    lx = np.where(bx, rxn, -rx - (rx - rxn))
    _, tl = ols_nw(lx, np.zeros((len(lx), 0)))
    print(
        f"  executable variant (signal at settlement t; enter next trading day settlement; exit first trading day after t+1), n = {len(ex)}:"
    )
    print(
        f"    mean monthly r: backwardated {rx[bx].mean() * 100:+.2f}% (n {bx.sum()}), contango {rx[~bx].mean() * 100:+.2f}% (n {(~bx).sum()})"
    )
    print(
        f"    timing rule, net of 2 ticks: mean {lx.mean() * 100:+.2f}%/month (NW t {tl[0]:+.2f}), "
        f"annualised Sharpe {lx.mean() / lx.std(ddof=1) * math.sqrt(12):+.2f}"
    )
    bD, tD = ols_nw(r, bk.astype(float))
    print(
        f"  exploratory (added after the v1 run, not pre-specified): r on 1[B>0]  diff = {bD[1] * 100:+.2f}%  t = {tD[1]:+.2f}"
    )
    print(
        f"  months with |r| >= 50% (counted, retained in every estimate): {int((np.abs(r) >= 0.5).sum())}"
    )
    S = bS[1] < 0 and abs(tS[1]) > 2
    P = bP[1] > 0 and abs(tP[1]) > 2 and n > 0 and r2 > 0 and cw > 1.65
    return S, P


def main(src):
    out = []
    verdicts = {}
    for market, names in (
        ("WTI", ("RCLC1d", "RCLC2d", "RCLC4d", "WCESTUS1w")),
        ("NG", ("RNGC1d", "RNGC2d", "RNGC4d", "NW2_EPG0_SWO_R48_BCFw")),
    ):
        c1, c2, c4, st = (series(src, n) for n in names)
        cal, rows, excluded = build(market, c1, c2, c4, st)
        verdicts[market] = summarise(market, rows, excluded, c1, c2, cal)
        for x in rows:
            f = lambda v: "" if v is None else f"{v:.6f}"
            out.append(
                (
                    market,
                    x["t"].isoformat(),
                    x["t1"].isoformat(),
                    f"{x['dC2'][0]}-{x['dC2'][1]:02d}",
                    f"{x['B']:.6f}",
                    f"{x['B4']:.6f}",
                    f"{x['r']:.6f}",
                    f"{x['rnet']:.6f}",
                    f(x["rx"]),
                    f(x["rxnet"]),
                    "" if x["F"] is None else x["F"].isoformat(),
                    f(x["I"]),
                    f(x["I14"]),
                )
            )
    with open(os.path.join(HERE, "backwardation_monthly.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(
            [
                "market",
                "month_end",
                "next_month_end",
                "held_contract_delivery",
                "B_ln_c1_c2",
                "B4_ln_c1_c4_per_month",
                "r_next_settle",
                "r_next_settle_net_2ticks",
                "r_exec_next_day",
                "r_exec_next_day_net_2ticks",
                "inventory_week_used",
                "inv_dev",
                "inv_dev_lag14",
            ]
        )
        w.writerows(out)
    for k, (S, P) in verdicts.items():
        print(
            f"\n{k}: scarcity {'supported' if S else 'not supported'}; premium {'supported' if P else 'not supported'}"
        )


if __name__ == "__main__":
    main(sys.argv[1])
