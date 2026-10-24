"""Toy calculations behind the AFML entries on bars, labels, sample weights and differencing."""

import math
import sys
from typing import Final, Literal

import numpy as np
from numpy.typing import NDArray
from statsmodels.tsa.stattools import adfuller

from trading_notes.numerical.financial_data_structures.bar_sampling import (
    CusumFilter,
    ImbalanceBars,
    tick_rule,
)
from trading_notes.numerical.financial_data_structures.etf_trick import (
    EtfTrickBasket,
    PrincipalRiskBudget,
)
from trading_notes.numerical.fractional_differentiation.fractional_weights import (
    FractionalDifference,
)
from trading_notes.numerical.labelling_sample_weights.labels import (
    LabelIndicators,
    TimeDecay,
    TripleBarrier,
)
from trading_notes.numerical.report import section

type Floats = NDArray[np.float64]
type Ints = NDArray[np.int64]

SEED: Final = 20261016


# --- tick rule and information-driven bars (pp. 29-32)
def show_tick_rule() -> None:
    """The tick rule, with the previous bar's sign carried into an unchanged first tick."""
    section("tick rule")
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
    section("information-driven bars on a toy order flow (balanced, then one-sided)")
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
        ends = ImbalanceBars(e_t0=50.0, kind=kind, runs=runs).bar_ends(side, vol)
        inside = ((ends >= 3000) & (ends < 3600)).sum()
        print(
            f"{('runs' if runs else 'imbalance'):9} {kind:6}: {len(ends):4} bars; {inside:3} end"
            f" in the 600-tick one-sided burst ({inside / 600 * 1000:.1f} per 1000 ticks against"
            f" {(len(ends) - inside) / (n - 700) * 1000:.1f} elsewhere)"
        )
    bal = np.where(rng.random(n) < 0.5, 1, -1)
    print(
        "perfectly balanced flow, tick imbalance:",
        len(ImbalanceBars(e_t0=50.0).bar_ends(bal, vol)),
        "bars from",
        n - 100,
        "ticks: |2P[b=1]-1| near 0 collapses the threshold and E0[T] then shrinks; AFML does not"
        " bound it",
    )


# --- ETF trick (pp. 33-34)
def show_etf_trick() -> None:
    """The ETF trick on a two-leg toy, against a brute-force P&L."""
    section("ETF trick: two-leg toy, rebalanced every bar t in B, holdings sized at the next open")
    o = np.array([[100, 50.0], [101, 49.0], [103, 48.5], [102, 50.0], [104, 51.0]])  # opens o_{i,t}
    pcl = np.array(
        [[100.5, 49.5], [102, 48.8], [102.5, 49.0], [103, 50.5], [105, 50.5]]
    )  # closes p_{i,t}
    phi = np.ones_like(o)  # USD per point
    d = np.zeros_like(o)
    basket = EtfTrickBasket(weights=np.array([0.5, -0.5]))  # long one leg, short the other
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
            h_new = basket.holdings(K[-1], o[t + 1], phi[t])
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
    section("PCA weights")
    A = rng.normal(size=(4, 4))
    V = A @ A.T + 0.1 * np.eye(4)
    budget = PrincipalRiskBudget.of(V)
    lam, W = budget.variances, budget.loadings
    R = np.array([0.1, 0.2, 0.3, 0.4])
    sigma = 2.0
    beta = budget.component_weights(R, sigma)
    wts = W @ beta
    contrib = budget.risk_shares(wts, V)
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
        budget.risk_shares(W @ flip, V).round(10),
        "-> 2^k allocations for k components with R_n > 0 (distinct eigenvalues)",
    )
    print(
        "typo check: (L^1/2 b)'(L^1/2 b) =",
        round(float((np.sqrt(lam) * beta) @ (np.sqrt(lam) * beta)), 10),
        "= sigma^2",
        sigma**2,
    )


# --- CUSUM (pp. 38-39, Snippet 2.4)
def show_cusum() -> None:
    """Events of the CUSUM filter, the strict inequality and the one-sided reset."""
    section("symmetric CUSUM filter with reset (Snippet 2.4 convention, E_{t-1}[y_t] = y_{t-1})")
    x = np.array([0, 0.3, 0.6, 0.9, 1.2, 1.1, 1.0, 1.05, 1.0, 1.05, 0.7, 0.4, 0.1, -0.2, -0.5])
    print(
        "series",
        x,
        "\nevents (h=0.5):",
        CusumFilter(threshold=0.5).events(x),
        "; hovering near a level triggers nothing: ",
        CusumFilter(threshold=0.5).events(np.array([1, 1.05, 1, 1.05, 1, 1.05, 1])),
    )
    print(
        "strict > in the snippet vs >= in the text: a run of exactly h ->",
        CusumFilter(threshold=0.5).events(np.array([0, 0.25, 0.5])),
        "vs",
        CusumFilter(threshold=0.5).events(np.array([0, 0.25, 0.5001])),
    )
    print("only the triggered side resets: after an up-event, S- keeps its value")


# --- triple barrier (pp. 44-50)
def show_triple_barrier() -> None:
    """Triple-barrier labels on four toy paths, and what closes cannot tell."""
    section("triple-barrier labels on toy close paths")
    paths = {
        "up first": [100, 101, 102.5, 99],
        "down first": [100, 99.4, 98.9, 103],
        "vertical, small gain": [100, 100.3, 100.6, 100.8],
        "vertical, exactly flat": [100, 100.5, 99.5, 100],
    }
    for name, pth in paths.items():
        print(
            f"{name:22}",
            TripleBarrier(profit_take=0.02, stop_loss=0.01).label(np.array(pth, float)),
            TripleBarrier(profit_take=0.02, stop_loss=0.01, label_vertical="zero").label(
                np.array(pth, float)
            ),
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
def show_concurrency(rng: np.random.Generator) -> None:
    """Concurrency and uniqueness of AFML's example, and the sequential bootstrap simulated."""
    section(
        "concurrency and average uniqueness: AFML example, Snippet 4.6 spans t1 = {0:2, 2:3, 4:5}"
    )
    labels = LabelIndicators.closed_spans([(0, 2), (2, 3), (4, 5)], 6)
    c = labels.concurrency()
    avg_u = labels.average_uniqueness()
    print("c_t", c, "average uniqueness", avg_u.round(4))
    ub, pr = labels.sequential_probabilities([1])
    print(
        "after drawing label 2: u-bar",
        ub.round(4),
        "probabilities",
        pr.round(4),
        "= {5,3,6}/14 ->",
        np.allclose(pr, np.array([5, 3, 6]) / 14),
    )
    ub3, pr3 = labels.sequential_probabilities([1, 2])
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
        indm = LabelIndicators.closed_spans(
            [(int(a), int(b)) for a, b in zip(t0, t1, strict=True)], int(t1.max()) + 1
        )
        std_u.append(indm.sample_uniqueness(list(rng.integers(0, n_labels, n_labels))))
        seq_u.append(indm.sample_uniqueness(indm.sequential_bootstrap(n_labels, rng)))
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
    section("bootstrap coverage: (1-1/I)^I and the overlap case")
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
    section("return-attribution weights")
    logp = np.log(np.array([100, 101, 103, 102, 104, 103, 105.0]))
    r = np.diff(logp)  # r_{t-1,t} for t = 1..6, indexed by t
    spans = [(1, 3), (2, 4), (5, 6)]
    c2 = LabelIndicators.closed_spans(spans, 7).concurrency()
    wt = np.array([abs(sum(r[t - 1] / c2[t] for t in range(a, b_ + 1))) for a, b_ in spans])
    wn = wt * len(wt) / wt.sum()
    print("w-tilde", wt.round(6), "normalised to sum I:", wn.round(4), "sum", wn.sum().round(10))


def show_time_decay() -> None:
    """Piecewise-linear time-decay factors on cumulative uniqueness."""
    section("piecewise-linear time decay on cumulative uniqueness x")
    ubar = np.array([0.5, 1.0, 0.25, 0.75, 0.5])
    X = np.cumsum(ubar)
    S = X[-1]
    for cdec in (1.0, 0.5, 0.0, -0.5):
        a, b_ = TimeDecay(last=cdec).coefficients(S)
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
def show_fractional_weights() -> None:
    """The weights' recurrence, sign, power-law decay and the fixed-width window."""
    section("fractional-difference weights")
    for dd in (0.0, 0.4, 1.0, 1.5, 2.0):
        fd = FractionalDifference(order=dd)
        a1, a2 = fd.weights(8), fd.binomial_weights(8)
        print(f"d={dd}: recurrence == binomial: {np.allclose(a1, a2)};", a1.round(4))
    w04 = FractionalDifference(order=0.4).weights(10001)
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
    w04_long = FractionalDifference(order=0.4).weights(100000)
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
        FractionalDifference(order=0.4).binomial_weights(4).round(4),
    )


def show_weight_loss() -> None:
    """The weight an expanding window loses for points computed from few observations."""
    section("expanding-window weight loss (Snippet 5.2 logic)")
    Tn = 200
    wexp = FractionalDifference(order=0.4).weights(Tn)
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


def show_ffd_adf(rng: np.random.Generator) -> None:
    """ADF statistics of a fractionally differenced random walk, as an illustration."""
    section("FFD and a unit-root test: an illustration, not a proof of stationarity")
    walk = np.cumsum(rng.normal(size=3000))
    train = walk[:2000]
    for dd in (0.2, 0.4, 0.6, 1.0):
        s = FractionalDifference(order=dd).fixed_width(train)
        stat, pval = adfuller(s, maxlag=1, regression="c", autolag=None, result_object=False)[:2]
        print(f"random walk, training segment, d={dd}: ADF {stat:7.2f} p={pval:.3f} (n={len(s)})")
    print(
        "theory: a random walk differenced by d is I(1-d), covariance-stationary only for d > 1/2;"
        " an ADF rejection at smaller d reflects the test, the lag choice and the truncation, so it"
        " is not a demonstration of stationarity"
    )


def main() -> int:
    """Run the parts in order with one generator.

    Independent toy calculations and boundary cases for the formulas and algorithms of the
    compendium's AFML data-cluster entries; not an implementation library. Printed page
    numbers refer to Lopez de Prado, Advances in Financial Machine Learning (Wiley 2018). One
    generator, seeded 20261016, serves the order-flow, PCA, bootstrap and unit-root parts in
    order; the ADF illustration uses statsmodels.

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
