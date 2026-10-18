"""Source follow-up of order books and order flow / dealer models and information reviews and the macro markets and pricing review audit (2026-10-16): checks of derivations added from primary sources.

1. Refresh time (Barndorff-Nielsen, Hansen, Lunde and Shephard, CREATES RP 2008-63, Definition 1, sec. 2.1.1) and the
   Hayashi-Yoshida estimator (Bernoulli 11(2), 2005, Definition 3.1, read in the second follow-up), against previous-tick sampling on two
   correlated Brownian motions observed at independent Poisson times, without noise. Refresh time alone leaves one
   stale price per refresh interval, so the plain realised covariance at refresh times is still biased down; one lead
   and one lag remove the bias here (the paper's kernel includes lags; its n. 2 limits staleness to one refresh lag).
2. Frequent batch auctions (Budish, Cramton and Shim, QJE 2015, sec. VII.B and n. 34): the share of time in which a speed
   advantage matters, delta/tau, and the sniping exposure epsilon/(2 tau) with uniform latency draws, by simulation.
3. Rate arithmetic of the refresh-time footnote: confidence intervals widen by 4^(1/2) - 1 = 100% at rate n^(1/2) and by
   4^(1/5) - 1 = 32% at rate n^(1/5) when the sample falls by a factor of 4 (CREATES RP 2008-63, n. 3).
4. Huang, Lehalle and Rosenbaum's Model I (arXiv v2, sec. 2.3): the invariant law of a queue from the arrival/departure
   ratio rho(n) = lambda_L(n) / (lambda_C(n + 1) + lambda_M(n + 1)) against a direct solution of the generator, and their
   maximum-likelihood estimates (inverse mean waiting time by queue size, split by event shares) on a simulated queue.
5. The Lee-Ready, EMO and CLNV rules as Jurkatis states them (BoE Staff Working Paper 896, sec. 2.1) on trades inside a
   10-cent spread after a downtick, where they disagree, and Holden and Jacobsen's interpolated time stamps as he
   describes them (sec. 2.2; the same formula as their JF 2014 eq. (16), read in the second follow-up).
6. The EU tick-size table (Delegated Regulation (EU) 2017/588, Annex, unchanged by its amendments of 2019 and 2023):
   lookups and the range of the relative tick in the most and least liquid bands; the large-in-scale table for shares
   (Delegated Regulation (EU) 2017/587, Annex II, Table 1, unchanged by its 2019, 2023 and 2025 amendments).
7. Platinum demand and refined-supply shares for 2025 from the WPIC Platinum Quarterly Q2 2026, Table 1 (Metals Focus data).
Run: uv run python market-estimators-rules-checks.py   (numpy; fixed seeds; a few seconds). Exits non-zero on failure.
"""

# standard library imports
import sys

# third party library imports
import numpy as np

rng = np.random.default_rng(20261016)
fails = []


def check(name, got, want, tol):
    ok = abs(got - want) <= tol
    print(f"  {'ok ' if ok else 'BAD'} {name}: {got:.6f} (want {want}, tol {tol})")
    if not ok:
        fails.append(name)


def head(t):
    print("\n== " + t)


# ------------------------------------------------------------------ 1. refresh time and Hayashi-Yoshida
head("1. Refresh time and Hayashi-Yoshida against previous-tick sampling")


def refresh_times(times):
    """Definition 1: tau_1 = max_i t_1^(i); tau_{j+1} = max_i (first observation of asset i strictly after tau_j)."""
    out, cur = [], -np.inf
    while True:
        nxt = []
        for t in times:
            k = np.searchsorted(t, cur, side="right")
            if k >= len(t):
                return np.array(out)
            nxt.append(t[k])
        cur = max(nxt)
        out.append(cur)


def last_value(t, x, at):
    """Previous-tick value of the series observed at times t (x[0] is the value at time 0)."""
    return x[np.searchsorted(t, at, side="right")]


def hayashi_yoshida(t1, x1, t2, x2):
    """Sum of r1_i r2_j over all pairs of observation intervals that overlap (standard form)."""
    a0, a1, r1 = np.r_[0.0, t1[:-1]], t1, np.diff(x1)
    b0, b1, r2 = np.r_[0.0, t2[:-1]], t2, np.diff(x2)
    tot, j = 0.0, 0
    for i in range(len(r1)):
        while j < len(r2) and b1[j] <= a0[i]:
            j += 1
        k = j
        while k < len(r2) and b0[k] < a1[i]:
            tot += r1[i] * r2[k]
            k += 1
    return tot


# Figure 1's retention ratio: N = 7 refresh times from 8, 9 and 10 observations, p = d N / sum n = 21/27
check("retention p = dN / sum n(i), Figure 1", 3 * 7 / (8 + 9 + 10), 21 / 27, 1e-12)
# a small hand example: asset 1 at 1, 4, 5, 9; asset 2 at 2, 3, 7, 8 -> refresh times 2, 4, 7, 9
rt = refresh_times([np.array([1.0, 4.0, 5.0, 9.0]), np.array([2.0, 3.0, 7.0, 8.0])])
check("hand example: refresh times 2, 4, 7, 9 (count)", len(rt), 4, 0)
check("hand example: second refresh time", rt[1], 4.0, 0)
check("hand example: last refresh time", rt[-1], 9.0, 0)

rho, sig, T, lam = 0.6, 1.0, 1.0, 400.0
est = {
    "prev-tick 1/200": [],
    "prev-tick 1/5000": [],
    "refresh time": [],
    "refresh time + lag 1": [],
    "Hayashi-Yoshida": [],
}
grid = np.linspace(0, T, 20001)
for path in range(60):
    dW = rng.standard_normal((2, len(grid) - 1)) * np.sqrt(np.diff(grid))
    w1 = np.r_[0, np.cumsum(dW[0])] * sig
    w2 = np.r_[0, np.cumsum(rho * dW[0] + np.sqrt(1 - rho**2) * dW[1])] * sig
    obs = []
    for w in (w1, w2):
        t = np.sort(rng.uniform(0, T, rng.poisson(lam * T)))
        idx = np.searchsorted(grid, t)
        obs.append(
            (t, np.r_[0.0, w[idx]])
        )  # x[0] = 0 at time 0, then the value at each observation
    (t1, x1), (t2, x2) = obs
    for step, key in ((1 / 200, "prev-tick 1/200"), (1 / 5000, "prev-tick 1/5000")):
        g = np.arange(0, T + 1e-12, step)
        est[key].append(np.sum(np.diff(last_value(t1, x1, g)) * np.diff(last_value(t2, x2, g))))
    r = np.r_[0.0, refresh_times([t1, t2])]
    y1, y2 = np.diff(last_value(t1, x1, r)), np.diff(last_value(t2, x2, r))
    est["refresh time"].append(np.sum(y1 * y2))
    # one lead and one lag, unweighted: the staleness that refresh time leaves is at most one refresh lag (n. 2)
    est["refresh time + lag 1"].append(
        np.sum(y1 * y2) + np.sum(y1[1:] * y2[:-1]) + np.sum(y1[:-1] * y2[1:])
    )
    est["Hayashi-Yoshida"].append(hayashi_yoshida(t1, x1, t2, x2))
target = rho * sig**2 * T
for k, v in est.items():
    print(f"  {k:18} mean {np.mean(v):.4f}  sd {np.std(v):.4f}  (integrated covariance {target})")
check(
    "Hayashi-Yoshida unbiased without noise (mean over 60 paths)",
    np.mean(est["Hayashi-Yoshida"]),
    target,
    0.06,
)
check(
    "refresh-time realised covariance alone is biased down (mean below 0.5: 1 = yes)",
    float(np.mean(est["refresh time"]) < 0.5),
    1.0,
    0,
)
check(
    "adding one lead and lag at refresh times removes the bias",
    np.mean(est["refresh time + lag 1"]),
    target,
    0.06,
)
check(
    "previous tick at a 1/5000 grid shows the Epps effect (mean below 0.3: 1 = yes)",
    float(np.mean(est["prev-tick 1/5000"]) < 0.3),
    1.0,
    0,
)

# ------------------------------------------------------------------ 2. frequent batch auctions
head("2. Batch auctions: share of time a speed advantage matters")
tau, d_slow, d_fast = 0.100, 0.003, 0.0029  # 100 ms batch, 100 microsecond speed difference
check("delta/tau for 100 us at a 100 ms batch", (d_slow - d_fast) / tau, 1 / 1000, 1e-12)
jumps = rng.uniform(0, tau, 2_000_000)  # jump times within a batch interval
asym = np.mean((jumps > tau - d_slow) & (jumps <= tau - d_fast))
check("simulated share of jumps seen only by the fast firm", asym, 1 / 1000, 1e-4)
eps = 100e-6  # n. 34: latency delta_fast + U[0, eps], liquidity provider draw u
u = rng.uniform(0, eps, len(jumps))
sniped = (jumps > tau - d_fast - eps) & (jumps < tau - d_fast) & (jumps > tau - d_fast - u)
check(
    "simulated sniping exposure, eps = 100 us, tau = 100 ms", np.mean(sniped), eps / (2 * tau), 5e-5
)
check("eps/(2 tau) at eps = 100 us, tau = 1 s", 100e-6 / 2, 0.00005, 1e-15)

# ------------------------------------------------------------------ 3. convergence-rate arithmetic
head("3. Confidence-interval widening when the sample falls by a factor of 4")
check("rate n^(1/2): widening", 4**0.5 - 1, 1.00, 1e-12)
check("rate n^(1/5): widening (paper: about 32%)", 4**0.2 - 1, 0.32, 0.005)

# ------------------------------------------------------------------ 4. queue-reactive Model I (Huang, Lehalle, Rosenbaum)
head(
    "4. Model I: invariant law from rho(n) = lambda_L(n) / (lambda_C(n+1) + lambda_M(n+1)), and the MLE"
)
nmax = 60
lamL = lambda n: 1.2 if n > 0 else 0.6  # insertion, lower at an empty queue
lamC = lambda n: (
    0.0 if n == 0 else 0.35 * min(n, 6) ** 0.8
)  # concave cancellation, zero at an empty queue
lamM = lambda n: 0.0 if n == 0 else 0.9 * np.exp(-0.3 * n)  # market orders, decreasing in size
rho_ = [lamL(n) / (lamC(n + 1) + lamM(n + 1)) for n in range(nmax)]
w = np.r_[1.0, np.cumprod(rho_)]
pi_formula = w / w.sum()
Q = np.zeros((nmax + 1, nmax + 1))  # generator truncated at nmax, solved directly
for n in range(nmax + 1):
    if n < nmax:
        Q[n, n + 1] = lamL(n)
    if n > 0:
        Q[n, n - 1] = lamC(n) + lamM(n)
    Q[n, n] = -Q[n].sum()
A = np.vstack([Q.T, np.ones(nmax + 1)])
pi_solve = np.linalg.lstsq(A, np.r_[np.zeros(nmax + 1), 1.0], rcond=None)[0]
check(
    "invariant law: product formula = generator solution (max abs diff)",
    np.max(np.abs(pi_formula - pi_solve)),
    0.0,
    1e-10,
)
rho_same = [lamL(n) / (lamC(n) + lamM(n)) if n > 0 else np.inf for n in range(1, nmax)]
print(
    f"  rho(n) with the shift, n=1..4: {[round(float(r), 3) for r in rho_[1:5]]}; same-size ratio: {[round(float(r), 3) for r in rho_same[:4]]}"
)
# simulate the queue and estimate by HLR's formulas: Lambda(n) = 1/mean(wait | q = n), lambda_type(n) = Lambda(n) * share
q, waits, types, sizes = 3, [], [], []
for _ in range(400_000):
    rates = np.array([lamL(q), lamC(q), lamM(q)])
    tot = rates.sum()
    waits.append(rng.exponential(1 / tot))
    sizes.append(q)
    k = rng.choice(3, p=rates / tot)
    types.append(k)
    q += 1 if k == 0 else -1
waits, types, sizes = np.array(waits), np.array(types), np.array(sizes)
for n in (1, 4):
    m = sizes == n
    Lam = 1 / waits[m].mean()
    check(f"MLE lambda_L({n})", Lam * np.mean(types[m] == 0), lamL(n), 0.03)
    check(f"MLE lambda_C({n})", Lam * np.mean(types[m] == 1), lamC(n), 0.03)
    check(f"MLE lambda_M({n})", Lam * np.mean(types[m] == 2), lamM(n), 0.03)
emp = np.bincount(sizes, weights=waits, minlength=nmax + 1)[: nmax + 1] / waits.sum()
check("time-weighted occupation of size 2 matches the invariant law", emp[2], pi_formula[2], 0.01)

# ------------------------------------------------------------------ 5. trade-classification rules (Jurkatis, BoE SWP 896, sec. 2)
head("5. LR, EMO and CLNV on trades inside the spread; Holden-Jacobsen interpolated times")
# standard library imports
from decimal import Decimal as Dm  # noqa: E402 (section-local import)


def tick_test(p, prev):
    """+1 if p above the last different earlier price, -1 if below, 0 if none."""
    for q in reversed(prev):
        if q != p:
            return 1 if p > q else -1
    return 0


def lr(p, bid, ask, prev):
    mid = (bid + ask) / 2
    return 1 if p > mid else -1 if p < mid else tick_test(p, prev)


def emo(p, bid, ask, prev):
    return 1 if p == ask else -1 if p == bid else tick_test(p, prev)


def clnv(p, bid, ask, prev):
    spr = ask - bid
    if ask - Dm("0.3") * spr <= p <= ask:
        return 1
    if bid <= p <= bid + Dm("0.3") * spr:
        return -1
    return tick_test(p, prev)


bid, ask = Dm("10.00"), Dm("10.10")
prev_down = [Dm("10.09")]  # previous trade at 10.09: each trade below it is a downtick
cases = {
    Dm("10.08"): (1, -1, 1),
    Dm("10.06"): (1, -1, -1),
    Dm("10.05"): (-1, -1, -1),
    Dm("10.10"): (1, 1, 1),
}
for p, want in cases.items():
    got = (lr(p, bid, ask, prev_down), emo(p, bid, ask, prev_down), clnv(p, bid, ask, prev_down))
    check(f"(LR, EMO, CLNV) at {p} after a downtick: {got}", float(got == want), 1.0, 0)
# Holden-Jacobsen interpolation as described by Jurkatis: t = s + (2i - 1)/(2I), i = 1..I, within the recorded second s
I = 4
ts = [0 + (2 * i - 1) / (2 * I) for i in range(1, I + 1)]
check(
    "interpolated times for 4 trades in one second: 0.125, 0.375, 0.625, 0.875 (sum)",
    sum(ts),
    2.0,
    1e-12,
)
check("interpolated times stay inside the second (max)", max(ts), 0.875, 1e-12)

# ------------------------------------------------------------------ 6. EU tick-size table (RTS 11 Annex) and LIS table (RTS 1 Annex II Table 1)
head("6. RTS 11 tick sizes: relative tick by liquidity band; RTS 1 large-in-scale thresholds")
edges = [
    0,
    0.1,
    0.2,
    0.5,
    1,
    2,
    5,
    10,
    20,
    50,
    100,
    200,
    500,
    1000,
    2000,
    5000,
    10000,
    20000,
    50000,
]
band6 = [
    0.0001,
    0.0001,
    0.0001,
    0.0001,
    0.0002,
    0.0005,
    0.001,
    0.002,
    0.005,
    0.01,
    0.02,
    0.05,
    0.1,
    0.2,
    0.5,
    1,
    2,
    5,
    10,
]
# table columns are shifted copies: band b (1..6) at price row r equals band 6 at row r + (6 - b), capped at row 0's values
table = {6: band6}
col1 = [
    0.0005,
    0.001,
    0.002,
    0.005,
    0.01,
    0.02,
    0.05,
    0.1,
    0.2,
    0.5,
    1,
    2,
    5,
    10,
    20,
    50,
    100,
    200,
    500,
]
col3 = [
    0.0001,
    0.0002,
    0.0005,
    0.001,
    0.002,
    0.005,
    0.01,
    0.02,
    0.05,
    0.1,
    0.2,
    0.5,
    1,
    2,
    5,
    10,
    20,
    50,
    100,
]
table[1], table[3] = col1, col3


def tick(price, adnt, tab):
    band = (
        1
        if adnt < 10
        else 2
        if adnt < 80
        else 3
        if adnt < 600
        else 4
        if adnt < 2000
        else 5
        if adnt < 9000
        else 6
    )
    row = max(i for i, e in enumerate(edges) if price >= e)
    return tab[band][row] if band in tab else None


check("EUR 25 share, 12,000 trades a day: tick 0.005", tick(25, 12000, table), 0.005, 1e-12)
check("EUR 25 share, 5 trades a day: tick 0.2", tick(25, 5, table), 0.2, 1e-12)
check("EUR 25 share, 300 trades a day: tick 0.05", tick(25, 300, table), 0.05, 1e-12)
rel = [band6[i] / edges[i + 1] for i in range(3, len(edges) - 1)] + [
    band6[i] / edges[i] for i in range(3, len(edges))
]
check(
    "most liquid band, price >= 0.5: relative tick at least 1 bp (min, bp)",
    1e4 * min(rel),
    1.0,
    1e-9,
)
check(
    "most liquid band, price >= 0.5: relative tick at most 2.5 bp (max, bp)",
    1e4 * max(rel),
    2.5,
    1e-9,
)
rel1 = [col1[i] / edges[i + 1] for i in range(3, len(edges) - 1)] + [
    col1[i] / edges[i] for i in range(3, len(edges))
]
check(
    "least liquid band, price >= 0.5: relative tick at least 40 bp (min, bp)",
    1e4 * min(rel1),
    40.0,
    1e-9,
)
check(
    "least liquid band, price >= 0.5: relative tick at most 100 bp (max, bp)",
    1e4 * max(rel1),
    100.0,
    1e-9,
)
lis_edges = [0, 50e3, 100e3, 500e3, 1e6, 5e6, 25e6, 50e6, 100e6]
lis = [15e3, 30e3, 60e3, 100e3, 200e3, 300e3, 400e3, 500e3, 650e3]
lis_of = lambda adt: lis[max(i for i, e in enumerate(lis_edges) if adt >= e)]
check("LIS for ADT EUR 30m: EUR 400,000", lis_of(30e6), 400e3, 0)
check("LIS for ADT EUR 30m as share of ADT (%)", 100 * lis_of(30e6) / 30e6, 1.3333, 1e-3)
check("LIS for ADT EUR 120m as share of ADT (%)", 100 * lis_of(120e6) / 120e6, 0.5417, 1e-3)

# ------------------------------------------------------------------ 7. platinum shares (WPIC Platinum Quarterly Q2 2026, Table 1, 2025 column, koz)
head("7. Platinum 2025: demand and mine-supply shares")
dem = {"automotive": 3039, "jewellery": 2214, "industrial": 2266, "investment": 1152}
check("demand components sum to total 8,671 koz", sum(dem.values()), 8671, 0)
for k, want in (
    ("automotive", 35.0),
    ("jewellery", 25.5),
    ("industrial", 26.1),
    ("investment", 13.3),
):
    check(f"{k} share of demand (%)", 100 * dem[k] / 8671, want, 0.05)
mine = {"South Africa": 3957, "Zimbabwe": 515, "North America": 212, "Russia": 677, "Other": 196}
check("refined production components sum to 5,557 koz", sum(mine.values()), 5557, 0)
check("South Africa share of refined production (%)", 100 * mine["South Africa"] / 5557, 71.2, 0.05)

print("\nFAILURES:", fails if fails else "none")
sys.exit(1 if fails else 0)
