"""ETF-trick timing and capital, label spans and the returns they use."""

import sys

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.financial_data_structures.etf_trick import EtfTrickBasket
from trading_notes.numerical.labelling_sample_weights.labels import LabelIndicators
from trading_notes.numerical.report import section

type Floats = NDArray[np.float64]


def show_next_open_sizing() -> Floats:
    """Show that ETF-trick holdings depend on the next open; return the second opening print."""
    section(
        "ETF trick: holdings h = w K / (o_{t+1} phi sum|w|) need the next open, unknown at"
        " decision time t"
    )
    K, w, phi = 1.0, np.array([0.6, -0.4]), np.array([1.0, 1.0])
    basket = EtfTrickBasket(weights=w)
    o_next = np.array([[100.0, 50.0], [101.5, 49.2]])  # two possible opening prints
    o: Floats
    for o in o_next:
        h = basket.holdings(K, o, phi)
        print(
            "open",
            o,
            "-> holdings",
            h.round(6),
            " gross exposure at that open",
            round(float((np.abs(h) * o * phi).sum()), 6),
        )
    print(
        "same causal weights, different opens -> different quantities: the quantity is not"
        " fixed at t"
    )
    # a notional-sized order filled at the single opening price reproduces the convention exactly
    notional = w * K / np.abs(w).sum()  # currency amounts per leg, fixed at t
    o = o_next[1]
    print(
        "notional per leg fixed at t",
        notional,
        "-> quantity at the opening print",
        (notional / (o * phi)).round(6),
        "(equals the convention when every leg fills in full at o_{t+1})",
    )
    # an order sized at t on the last close leaves a residual exposure when the open gaps
    p_close = np.array([100.0, 50.0])
    h_close = basket.holdings(K, p_close, phi)
    print(
        "quantities sized on p_t, valued at o_{t+1}: gross",
        round(float((np.abs(h_close) * o * phi).sum()), 6),
        "not 1",
    )
    return o


def show_capital_signs(o: Floats) -> None:
    """Show the holdings for capital K <= 0 and for a negative open, at the open o."""
    section(
        "ETF trick: gross exposure = |K| only with positive o*phi; K <= 0 inverts or zeroes"
        " the holdings"
    )
    phi = np.array([1.0, 1.0])
    basket = EtfTrickBasket(weights=np.array([0.6, -0.4]))
    for Kt in [1.0, 0.3, 0.0, -0.2]:
        h = basket.holdings(Kt, o, phi)
        print(
            f"K={Kt:5}: holdings {h.round(6)}  gross {float((np.abs(h) * o * phi).sum()):.4f}"
            f"  sign of long leg {np.sign(h[0]):+.0f}"
        )
    o_neg = np.array([-5.0, 50.0])  # a negative price (e.g. a rolled or spread series)
    h = basket.holdings(1.0, o_neg, phi)
    print(
        "negative open on leg 1 (w_1 = +0.6): holding",
        h.round(6),
        "-> a short position although w_1 > 0;",
        "sum |h| o phi =",
        round(float((np.abs(h) * o_neg * phi).sum()), 4),
        "is no longer the gross exposure",
    )


def show_label_spans() -> None:
    """Show which returns each label uses under the ending-time and inclusive rules."""
    section(
        "label spans: returns r_{t-1,t} indexed by ending time t; label on (t0, t1] uses"
        " t0 < t <= t1"
    )
    # AFML sec. 4.5.3: y1=f(r_{0,3}), y2=f(r_{2,4}), y3=f(r_{4,6})
    labels = [(0, 3), (2, 4), (4, 6)]
    T = 6
    # brute force: which one-bar returns does each label's return compound?
    for j, (a, b) in enumerate(labels):
        used = [t for t in range(1, T + 1) if a < t <= b]
        print(f"label {j + 1} on r_({a},{b}) compounds r_(t-1,t) for t in {used}")
    ending_labels = LabelIndicators.by_rule(
        labels, range(1, T + 1), lambda a, b, t: float(a < t <= b)
    )
    ending = ending_labels.matrix
    c, u = ending_labels.concurrency(), ending_labels.average_uniqueness()
    print(
        "ending-time rule, rows t=1..6:\n",
        ending.astype(int),
        "\nconcurrency",
        c,
        "average uniqueness",
        u.round(4),
    )
    start = LabelIndicators.by_rule(
        [(a, b - 1) for a, b in labels], range(0, T), lambda a, b, s: float(a <= s <= b)
    ).matrix
    print(
        "consistent reindexing by start time s (r_{s,s+1}, t0 <= s < t1; AFML Snippet 4.6 codes"
        " t1 = {0:2, 2:3, 4:5}): identical matrix:",
        bool((start == ending).all()),
    )
    incl_labels = LabelIndicators.by_rule(
        labels, range(0, T + 1), lambda a, b, t: float(a <= t <= b)
    )
    incl = incl_labels.matrix
    c2, u2 = incl_labels.concurrency(), incl_labels.average_uniqueness()
    print(
        "inclusive [t0, t1] on ending-time rows t=0..6 (getIndMatrix applied to the events"
        " themselves):\n",
        incl.astype(int),
        "\nconcurrency",
        c2,
        "average uniqueness",
        u2.round(4),
    )
    print(
        "labels 2 and 3 are adjacent (one ends at 4, the other starts at 4) yet share row t=4,"
        " the return r_{3,4} that label 3 never uses"
    )

    # attribution weights on a toy log-price path: the inclusive rule adds a return from
    # before the label starts
    logp = np.log(np.array([100, 101, 103, 102, 104, 103, 106.0]))
    r = np.diff(logp)  # r[t-1] = r_{t-1,t}, t = 1..6
    w_end = [abs(sum(r[t - 1] / c[t - 1] for t in range(a + 1, b + 1))) for a, b in labels]
    w_inc = [
        abs(sum((r[t - 1] if t >= 1 else 0.0) / c2[t] for t in range(a, b + 1))) for a, b in labels
    ]
    print(
        "attribution |sum r/c|: ending-time rule",
        np.round(w_end, 5),
        " inclusive rule",
        np.round(w_inc, 5),
    )


def main() -> int:
    """Print the ETF-trick sizing, its capital signs and the label spans.

    Holdings and spans are recomputed by brute force where possible, independently of the
    entries' formulas. A demonstration: it prints the holdings, indicator matrices and weights
    and asserts nothing.

    Returns:
        The exit status, always 0.
    """
    o = show_next_open_sizing()
    show_capital_signs(o)
    show_label_spans()
    return 0


if __name__ == "__main__":
    sys.exit(main())
