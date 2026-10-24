"""Financial data and labels: toy calculations behind the AFML data-cluster entries.

Numerical checks for financial data and labels review (AFML data cluster), 2026-10-16.

Independent toy calculations and boundary cases for the formulas and algorithms adopted in the
compendium entries; not an implementation library. Needs numpy and statsmodels (for one ADF
illustration). Seeds are fixed; output is deterministic. Printed page numbers refer to Lopez de
Prado, Advances in Financial Machine Learning (Wiley 2018).

It prints values to be read and asserts nothing. One generator, seeded 20261016, serves the
order-flow, PCA, bootstrap and unit-root parts in order.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.afml (numpy, statsmodels).
"""

# standard library imports
import math
import sys
from collections.abc import Sequence
from typing import Final, Literal

# third party library imports
import numpy as np
from numpy.typing import NDArray
from statsmodels.tsa.stattools import adfuller

type Floats = NDArray[np.float64]
type Ints = NDArray[np.int64]

SEED: Final = 20261016


def head(t: str) -> None:
    """Print a part's heading after a blank line."""
    print("\n== " + t)


# --- tick rule and information-driven bars (pp. 29-32)
def tick_rule(p: Floats, b0: int) -> Ints:
    """b_t = sign(dp_t), carried forward when dp_t = 0; b0 is the previous bar's terminal value."""
    b, prev = [], b0
    for dp in np.diff(p):
        prev = prev if dp == 0 else int(np.sign(dp))
        b.append(prev)
    return np.array(b)


def imbalance_bars(
    b: Ints,
    v: Floats,
    e_t0: float,
    alpha: float = 0.1,
    kind: Literal["tick", "volume"] = "tick",
    runs: bool = False,
) -> Ints:
    """Sample bar ends using expectations fixed at each bar's start from EWMAs over PRIOR bars only.

    Returns:
        The index of each bar's last tick (an empty float array if no bar closes).
    """
    ends, start = [], 0
    eT, ep = e_t0, (b[:100] == 1).mean()  # warm-up expectations from a burn-in window
    ebv = (b[:100] * v[:100]).mean()
    evb = v[:100][b[:100] == 1].mean()
    evs = v[:100][b[:100] == -1].mean()
    t = 100
    start = t
    theta: np.int64 | np.float64
    thresh: float
    while t < len(b):
        seg_b, seg_v = b[start : t + 1], v[start : t + 1]
        if not runs:
            if kind == "tick":
                theta = abs(seg_b.sum())
            else:
                theta = abs((seg_b * seg_v).sum())
            thresh = eT * abs(2 * ep - 1) if kind == "tick" else eT * abs(ebv)
        else:
            if kind == "tick":
                theta = max((seg_b == 1).sum(), (seg_b == -1).sum())
                thresh = eT * max(ep, 1 - ep)
            else:
                theta = max(seg_v[seg_b == 1].sum(), seg_v[seg_b == -1].sum())
                thresh = eT * max(ep * evb, (1 - ep) * evs)
        if theta >= thresh:
            T = t - start + 1
            ends.append(t)
            # update EWMAs with the bar just closed; the next bar's threshold uses only closed bars
            eT = (1 - alpha) * eT + alpha * T
            ep = (1 - alpha) * ep + alpha * (seg_b == 1).mean()
            ebv = (1 - alpha) * ebv + alpha * (seg_b * seg_v).mean()
            if (seg_b == 1).any():
                evb = (1 - alpha) * evb + alpha * seg_v[seg_b == 1].mean()
            if (seg_b == -1).any():
                evs = (1 - alpha) * evs + alpha * seg_v[seg_b == -1].mean()
            start = t + 1
        t += 1
    return np.array(ends)


def show_tick_rule() -> None:
    """The tick rule, with the previous bar's sign carried into an unchanged first tick."""
    head("tick rule")
    p = np.array([10.00, 10.01, 10.01, 10.00, 10.00, 10.02])
    print(
        "prices",
        p,
        "-> b",
        tick_rule(p, b0=1),
        "(b0=1)",
        tick_rule(np.array([10, 10, 10.01]), b0=-1),
        "(b0=-1, no change first)",
    )


def show_information_bars(rng: np.random.Generator) -> None:
    """Tick, volume and run bars on a toy flow with a one-sided burst, and a balanced flow."""
    head("information-driven bars on a toy order flow (balanced, then one-sided)")
    n = 6000
    side = np.where(rng.random(n) < 0.55, 1, -1)  # mildly buy-heavy flow
    side[3000:3600] = np.where(rng.random(600) < 0.85, 1, -1)  # informed buying burst
    vol = rng.integers(1, 10, n).astype(float)
    kinds: list[tuple[Literal["tick", "volume"], bool]] = [
        ("tick", False),
        ("volume", False),
        ("tick", True),
        ("volume", True),
    ]
    for kind, runs in kinds:
        ends = imbalance_bars(side, vol, e_t0=50.0, kind=kind, runs=runs)
        inside = ((ends >= 3000) & (ends < 3600)).sum()
        print(
            f"{('runs' if runs else 'imbalance'):9} {kind:6}: {len(ends):4} bars; {inside:3} end"
            f" in the 600-tick one-sided burst ({inside / 600 * 1000:.1f} per 1000 ticks against"
            f" {(len(ends) - inside) / (n - 700) * 1000:.1f} elsewhere)"
        )
    bal = np.where(rng.random(n) < 0.5, 1, -1)
    print(
        "perfectly balanced flow, tick imbalance:",
        len(imbalance_bars(bal, vol, e_t0=50.0)),
        "bars from",
        n - 100,
        "ticks: |2P[b=1]-1| near 0 collapses the threshold and E0[T] then shrinks; AFML does not"
        " bound it",
    )


# --- ETF trick (pp. 33-34)
def show_etf_trick() -> None:
    """The ETF trick on a two-leg toy, against a brute-force P&L."""
    head("ETF trick: two-leg toy, rebalanced every bar t in B, holdings sized at the next open")
    o = np.array([[100, 50.0], [101, 49.0], [103, 48.5], [102, 50.0], [104, 51.0]])  # opens o_{i,t}
    pcl = np.array(
        [[100.5, 49.5], [102, 48.8], [102.5, 49.0], [103, 50.5], [105, 50.5]]
    )  # closes p_{i,t}
    phi = np.ones_like(o)  # USD per point
    d = np.zeros_like(o)
    w = np.array([0.5, -0.5])  # allocation (long one, short the other)
    B = {0, 2}  # rebalance bars
    tau = np.array([1e-4, 1e-4])
    K = [1.0]
    h = np.zeros(2)
    hist = []
    for t in range(len(o) - 1):
        if t > 0:
            delta = pcl[t] - o[t] if (t - 1) in B else pcl[t] - pcl[t - 1]
            K.append(K[-1] + (h * phi[t] * (delta + d[t])).sum())
        if t in B:
            h_new = w * K[-1] / (o[t + 1] * phi[t] * np.abs(w).sum())
            c = ((np.abs(h) * pcl[t] + np.abs(h_new) * o[t + 1]) * phi[t] * tau).sum()
            h = h_new
            hist.append((t, h.round(6), round(float(c), 8)))
    print("K path", np.round(K, 6))
    print("holdings and rebalance cost c_t at t in B:", hist)
    print(
        "gross exposure at execution = K: ",
        round((np.abs(hist[0][1]) * o[1]).sum(), 6),
        "vs K_0 = 1",
    )
    # brute-force PnL check: a dollar-neutral portfolio's value change = sum h*(price change) over
    # the held interval
    pnl1 = (hist[0][1] * (pcl[1] - o[1])).sum() + (hist[0][1] * (pcl[2] - pcl[1])).sum()
    print(
        "consistency: K_2 - K_0 recomputed from holdings",
        round(pnl1, 6),
        "vs ETF trick",
        round(K[2] - K[0], 6),
    )
    print(
        "negative K is possible with short legs: short 1 unit-dollar leg after a +120% move ->",
        round(1 + (-1 / 100) * (220 - 100), 3),
    )


# --- PCA risk-distribution weights (p. 35)
def show_pca_weights(rng: np.random.Generator) -> None:
    """Weights that distribute risk across principal components as targeted."""
    head("PCA weights")
    A = rng.normal(size=(4, 4))
    V = A @ A.T + 0.1 * np.eye(4)
    lam, W = np.linalg.eigh(V)
    idx = lam.argsort()[::-1]
    lam, W = lam[idx], W[:, idx]
    R = np.array([0.1, 0.2, 0.3, 0.4])
    sigma = 2.0
    beta = sigma * np.sqrt(R / lam)
    wts = W @ beta
    contrib = (W.T @ wts) ** 2 * lam / (wts @ V @ wts)
    print(
        "target R",
        R,
        "-> realised",
        contrib.round(10),
        "; sigma",
        round(math.sqrt(wts @ V @ wts), 10),
    )
    flip = beta * np.array([1, -1, 1, 1])
    print(
        "flipping the sign of one beta with R_n > 0 keeps R:",
        ((W.T @ (W @ flip)) ** 2 * lam / ((W @ flip) @ V @ (W @ flip))).round(10),
        "-> 2^k allocations for k components with R_n > 0 (distinct eigenvalues)",
    )
    print(
        "typo check: (L^1/2 b)'(L^1/2 b) =",
        round(float((np.sqrt(lam) * beta) @ (np.sqrt(lam) * beta)), 10),
        "= sigma^2",
        sigma**2,
    )


# --- CUSUM (pp. 38-39, Snippet 2.4)
def cusum_events(x: Floats, hthr: float) -> list[int]:
    """Return the indices at which the symmetric CUSUM filter with reset fires."""
    ev, sp, sn = [], 0.0, 0.0
    for i in range(1, len(x)):
        dx = x[i] - x[i - 1]
        sp, sn = max(0.0, sp + dx), min(0.0, sn + dx)
        if sn < -hthr:
            sn = 0.0
            ev.append(i)
        elif sp > hthr:
            sp = 0.0
            ev.append(i)
    return ev


def show_cusum() -> None:
    """Events of the CUSUM filter, the strict inequality and the one-sided reset."""
    head("symmetric CUSUM filter with reset (Snippet 2.4 convention, E_{t-1}[y_t] = y_{t-1})")
    x = np.array([0, 0.3, 0.6, 0.9, 1.2, 1.1, 1.0, 1.05, 1.0, 1.05, 0.7, 0.4, 0.1, -0.2, -0.5])
    print(
        "series",
        x,
        "\nevents (h=0.5):",
        cusum_events(x, 0.5),
        "; hovering near a level triggers nothing: ",
        cusum_events(np.array([1, 1.05, 1, 1.05, 1, 1.05, 1]), 0.5),
    )
    print(
        "strict > in the snippet vs >= in the text: a run of exactly h ->",
        cusum_events(np.array([0, 0.25, 0.5]), 0.5),
        "vs",
        cusum_events(np.array([0, 0.25, 0.5001]), 0.5),
    )
    print("only the triggered side resets: after an up-event, S- keeps its value")


# --- triple barrier (pp. 44-50)
def triple_barrier(
    path: Floats,
    pt: float | None,
    sl: float | None,
    side: int = 1,
    label_vertical: Literal["sign", "zero"] = "sign",
) -> tuple[int, int]:
    """Return (label, index of the first touch) for one close path."""
    r = (path / path[0] - 1) * side
    for k in range(1, len(path)):
        if pt is not None and r[k] >= pt:
            return 1, k
        if sl is not None and r[k] <= -sl:
            return -1, k
    last = r[-1]
    return (int(np.sign(last)) if label_vertical == "sign" else 0), len(path) - 1


def show_triple_barrier() -> None:
    """Triple-barrier labels on four toy paths, and what closes cannot tell."""
    head("triple-barrier labels on toy close paths")
    paths = {
        "up first": [100, 101, 102.5, 99],
        "down first": [100, 99.4, 98.9, 103],
        "vertical, small gain": [100, 100.3, 100.6, 100.8],
        "vertical, exactly flat": [100, 100.5, 99.5, 100],
    }
    for name, pth in paths.items():
        print(
            f"{name:22}",
            triple_barrier(np.array(pth, float), 0.02, 0.01),
            triple_barrier(np.array(pth, float), 0.02, 0.01, label_vertical="zero"),
        )
    print(
        "intrabar: a bar with high 102.5 and low 98.9 crosses both barriers; closes alone cannot"
        " say which came first"
    )
    print(
        "meta-label (side=+1 from a primary model): label = 1 if signed return > 0 at first touch,"
        " else 0; Snippet 3.7 maps ret <= 0 to 0"
    )


# --- concurrency, uniqueness, sequential bootstrap (pp. 60-68)
def seq_probs(ind: Floats, drawn: Sequence[int]) -> tuple[Floats, Floats]:
    """Return each label's average uniqueness given those drawn, and the draw probabilities."""
    base = ind[:, drawn].sum(1) if drawn else np.zeros(ind.shape[0])
    means = []
    for j in range(ind.shape[1]):
        uj = ind[:, j] / (1 + base)
        means.append(uj[ind[:, j] > 0].mean())
    ub = np.array(means)
    return ub, ub / ub.sum()


def seq_bootstrap(ind: Floats, n: int, rng: np.random.Generator) -> list[int]:
    """Draw n labels by the sequential bootstrap."""
    drawn: list[int] = []
    for _ in range(n):
        _, pr = seq_probs(ind, drawn)
        drawn.append(rng.choice(ind.shape[1], p=pr))
    return drawn


def avg_uniqueness_of_sample(ind: Floats, s: Sequence[int]) -> np.float64:
    """Return the mean average uniqueness of the labels drawn in s."""
    sub = ind[:, s]
    cc = sub.sum(1)
    uu = np.divide(sub, cc[:, None], out=np.zeros_like(sub), where=cc[:, None] > 0)
    return np.float64((uu.sum(0) / sub.sum(0)).mean())


def show_concurrency(rng: np.random.Generator) -> None:
    """Concurrency and uniqueness of AFML's example, and the sequential bootstrap simulated."""
    head("concurrency and average uniqueness: AFML example, Snippet 4.6 spans t1 = {0:2, 2:3, 4:5}")
    ind = np.zeros((6, 3))
    for j, (a, b_) in enumerate([(0, 2), (2, 3), (4, 5)]):
        ind[a : b_ + 1, j] = 1
    c = ind.sum(1)
    u = np.divide(ind, c[:, None], out=np.zeros_like(ind), where=c[:, None] > 0)
    avg_u = u.sum(0) / ind.sum(0)
    print("c_t", c, "average uniqueness", avg_u.round(4))
    ub, pr = seq_probs(ind, [1])
    print(
        "after drawing label 2: u-bar",
        ub.round(4),
        "probabilities",
        pr.round(4),
        "= {5,3,6}/14 ->",
        np.allclose(pr, np.array([5, 3, 6]) / 14),
    )
    ub3, pr3 = seq_probs(ind, [1, 2])
    print(
        "after drawing 2 then 3 (exercise 4.6):",
        pr3.round(4),
        "=",
        [f"{x:.0f}/{ub3.sum() * 12:.0f}" for x in ub3 * 12],
    )
    std_u, seq_u = [], []
    for _it in range(400):
        n_labels, T, maxH = 10, 100, 5
        t0 = rng.integers(0, T, n_labels)
        t1 = t0 + rng.integers(1, maxH, n_labels)
        indm = np.zeros((t1.max() + 1, n_labels))
        for j in range(n_labels):
            indm[t0[j] : t1[j] + 1, j] = 1
        std_u.append(avg_uniqueness_of_sample(indm, list(rng.integers(0, n_labels, n_labels))))
        seq_u.append(avg_uniqueness_of_sample(indm, seq_bootstrap(indm, n_labels, rng)))
    print(
        "share of runs with sequential < standard:"
        f" {np.mean(np.array(seq_u) < np.array(std_u)):.3f}"
    )
    print(
        "Monte Carlo (400 runs, I=10, T=100, maxH=5, spans t1-t0 in 1..4 bars): median average"
        f" uniqueness standard {np.median(std_u):.3f}, sequential {np.median(seq_u):.3f} (AFML"
        " reports 0.6 and 0.7 on 1E6 runs)"
    )


def show_bootstrap_coverage(rng: np.random.Generator) -> None:
    """The share of rows a bootstrap sample covers, with and without overlap."""
    head("bootstrap coverage: (1-1/I)^I and the overlap case")
    for n_rows in (10, 100, 10000):
        print(
            f"I={n_rows:6}: (1-1/I)^I = {(1 - 1 / n_rows) ** n_rows:.5f}, e^-1 = {math.exp(-1):.5f}"
        )
    n_rows, Kk = 1000, 100
    print(
        f"I={n_rows}, K={Kk} effective outcomes: (1-1/K)^I = {(1 - 1 / Kk) ** n_rows:.3e};"
        f" e^(-I/K) = {math.exp(-n_rows / Kk):.3e}; AFML's e^(-K/I) = {math.exp(-Kk / n_rows):.4f}"
    )
    draws = rng.integers(
        0, Kk, size=(2000, n_rows)
    )  # each of I draws lands in one of K blocks of 10 overlapping rows
    distinct = np.array([len(np.unique(r)) for r in draws])
    print(
        "Monte Carlo: distinct effective outcomes per bootstrap sample"
        f" {distinct.mean():.1f} of K={Kk} (theory K(1-e^(-I/K)) ="
        f" {Kk * (1 - math.exp(-n_rows / Kk)):.1f}); per in-bag row"
        f" {distinct.mean() / n_rows:.3f} against 1-e^-1 = {1 - math.exp(-1):.3f} distinct rows"
        " per row under IID"
    )


# --- return attribution and time decay (pp. 68-71)
def show_return_attribution() -> None:
    """Sample weights from returns attributed by concurrency."""
    head("return-attribution weights")
    logp = np.log(np.array([100, 101, 103, 102, 104, 103, 105.0]))
    r = np.diff(logp)  # r_{t-1,t} for t = 1..6, indexed by t
    spans = [(1, 3), (2, 4), (5, 6)]
    ind2 = np.zeros((7, 3))
    for j, (a, b_) in enumerate(spans):
        ind2[a : b_ + 1, j] = 1
    c2 = ind2.sum(1)
    wt = np.array([abs(sum(r[t - 1] / c2[t] for t in range(a, b_ + 1))) for a, b_ in spans])
    wn = wt * len(wt) / wt.sum()
    print("w-tilde", wt.round(6), "normalised to sum I:", wn.round(4), "sum", wn.sum().round(10))


def show_time_decay() -> None:
    """Piecewise-linear time-decay factors on cumulative uniqueness."""
    head("piecewise-linear time decay on cumulative uniqueness x")
    ubar = np.array([0.5, 1.0, 0.25, 0.75, 0.5])
    X = np.cumsum(ubar)
    S = X[-1]
    for cdec in (1.0, 0.5, 0.0, -0.5):
        b_ = (1 - cdec) / S if cdec >= 0 else 1 / ((cdec + 1) * S)
        a = 1 - b_ * S
        dvals = np.maximum(0, a + b_ * X)
        at0 = a
        zero_at = (-cdec * S) if cdec < 0 else None
        print(
            f"c={cdec:5}: a={a:.4f} b={b_:.4f} d(0)={at0:.4f} d(S)={a + b_ * S:.4f} weights"
            f" {dvals.round(4)}"
            + (
                f"; zero for x <= -cS = {zero_at:.3f} (a share {-cdec:.2f} of cumulative"
                " uniqueness)"
                if zero_at
                else ""
            )
        )
    print(
        "the oldest observation sits at x = u-bar_1 > 0, so its factor is c + (1-c) u-bar_1 / S,"
        " not exactly c"
    )


# --- fractional differencing (pp. 77-84)
def frac_weights(dd: float, n: int) -> Floats:
    """Return the first n fractional-difference weights of order dd, by the recurrence."""
    wv = [1.0]
    for k in range(1, n):
        wv.append(-wv[-1] * (dd - k + 1) / k)
    return np.array(wv)


def binom_weights(dd: float, n: int) -> Floats:
    """Return the first n fractional-difference weights of order dd, from the binomial series."""
    return np.array(
        [(-1) ** k * math.prod(dd - i for i in range(k)) / math.factorial(k) for k in range(n)]
    )


def show_fractional_weights() -> None:
    """The weights' recurrence, sign, power-law decay and the fixed-width window."""
    head("fractional-difference weights")
    for dd in (0.0, 0.4, 1.0, 1.5, 2.0):
        a1, a2 = frac_weights(dd, 8), binom_weights(dd, 8)
        print(f"d={dd}: recurrence == binomial: {np.allclose(a1, a2)};", a1.round(4))
    w04 = frac_weights(0.4, 10001)
    print(
        "d=0.4: all w_k for k>=1 in (-1,0):",
        bool(((w04[1:] < 0) & (w04[1:] > -1)).all()),
        "; ratio |w_k/w_k-1| at k=10, 1000:",
        abs(w04[10] / w04[9]).round(4),
        abs(w04[1000] / w04[999]).round(6),
        "-> tends to 1; decay is a power law, |w_k| k^(1+d) ->",
        (abs(w04[1000]) * 1000**1.4).round(4),
        (abs(w04[10000]) * 10000**1.4).round(4),
        "vs 1/|Gamma(-d)| =",
        round(1 / abs(math.gamma(-0.4)), 4),
    )
    print(
        "sum of weights (d=0.4, 10001 terms):",
        w04.sum().round(4),
        "-> 0 as the window grows (slowly)",
    )
    w04_long = frac_weights(0.4, 100000)
    for thr in (1e-2, 1e-3, 1e-5):
        width = int(np.argmax(np.abs(w04_long) < thr))
        print(
            f"FFD d=0.4 threshold {thr:g}: keep k = 0..{width - 1} ({width} weights); kept weights"
            f" sum to {w04_long[:width].sum():.4f}"
        )
    print(
        "the weight formula with (d-1) in place of (d-i):",
        [
            round((-1) ** k * math.prod(0.4 - 1 for _ in range(k)) / math.factorial(k), 4)
            for k in range(4)
        ],
        "against",
        binom_weights(0.4, 4).round(4),
    )


def show_weight_loss() -> None:
    """The weight an expanding window loses for points computed from few observations."""
    head("expanding-window weight loss (Snippet 5.2 logic)")
    Tn = 200
    wexp = frac_weights(0.4, Tn)
    total = np.abs(wexp).sum()
    loss = np.array(
        [np.abs(wexp[t:]).sum() / total for t in range(1, Tn + 1)]
    )  # point using t observations
    print(
        "weight loss of the point computed from t observations, t = 1, 5, 20, 100, 200:",
        loss[[0, 4, 19, 99, 199]].round(4),
        "; points kept at tau=0.01 start at t =",
        int(np.argmax(loss <= 0.01)) + 1,
    )


def ffd(series: Floats, dd: float, thr: float = 1e-4) -> Floats:
    """Return the fixed-width fractionally differenced series of order dd."""
    wv = frac_weights(dd, 100000)
    width = int(np.argmax(np.abs(wv) < thr))
    wv = wv[:width]
    return np.array([wv @ series[t - np.arange(width)] for t in range(width - 1, len(series))])


def show_ffd_adf(rng: np.random.Generator) -> None:
    """ADF statistics of a fractionally differenced random walk, as an illustration."""
    head("FFD and a unit-root test: an illustration, not a proof of stationarity")
    walk = np.cumsum(rng.normal(size=3000))
    train = walk[:2000]
    for dd in (0.2, 0.4, 0.6, 1.0):
        s = ffd(train, dd)
        stat, pval = adfuller(s, maxlag=1, regression="c", autolag=None, result_object=False)[:2]
        print(f"random walk, training segment, d={dd}: ADF {stat:7.2f} p={pval:.3f} (n={len(s)})")
    print(
        "theory: a random walk differenced by d is I(1-d), covariance-stationary only for d > 1/2;"
        " an ADF rejection at smaller d reflects the test, the lag choice and the truncation, so it"
        " is not a demonstration of stationarity"
    )


def main() -> int:
    """Run the parts in order with one generator.

    Returns:
        0; the parts print values and assert nothing.
    """
    rng = np.random.default_rng(SEED)
    show_tick_rule()
    show_information_bars(rng)
    show_etf_trick()
    show_pca_weights(rng)
    show_cusum()
    show_triple_barrier()
    show_concurrency(rng)
    show_bootstrap_coverage(rng)
    show_return_attribution()
    show_time_decay()
    show_fractional_weights()
    show_weight_loss()
    show_ffd_adf(rng)
    return 0


if __name__ == "__main__":
    sys.exit(main())
