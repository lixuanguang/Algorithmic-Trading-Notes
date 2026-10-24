"""Index values and returns: the worked examples of two index entries."""

import sys
from typing import Final

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.index_construction.index_mathematics import (
    BondIndexMonth,
    CapWeightedIndex,
    PriceWeightedIndex,
    one_way_turnover,
)
from trading_notes.numerical.report import CheckReport
from trading_notes.numerical.tolerance import close
from trading_notes.records import Record

type Floats = NDArray[np.float64]

# Inputs. Prices in currency units; shares in millions; IWF = investable weight factor.
P0: Final = (50.0, 20.0, 80.0)
P1: Final = (55.0, 19.0, 84.0)
SHARES0: Final = (100.0, 300.0, 50.0)
IWF: Final = (0.8, 1.0, 0.5)


class CapIndex(Record):
    """The capitalisation-weighted index after day 1's corporate actions.

    Attributes:
        index: The index after the split and the share issue.
        level1: The day 1 level.
        level2: The day 2 level.
        r1: Each stock's day 1 return.
        r2: Each stock's day 2 return.
        p1_adj: Day 1 prices adjusted for the split.
    """

    index: CapWeightedIndex
    level1: float
    level2: float
    r1: Floats
    r2: Floats
    p1_adj: Floats


def check_price_weighted(report: CheckReport) -> None:
    """Part 1: the price-weighted index and its divisor at a split."""
    print("== part 1: price-weighted index with a 2-for-1 split in C after the close of day 1")
    P0_, P1_ = np.array(P0), np.array(P1)
    base = PriceWeightedIndex.based(P0_, 100.0)
    D0 = base.divisor
    L0 = base.level(P0_)
    L1 = base.level(P1_)
    report.ok("divisor 1.5 gives a base of 100.00", bool(close(D0, 1.5) and close(L0, 100.0)))
    report.ok(
        "day 1 level 105.3333 (+5.3333%)",
        bool(close(L1, 158 / 1.5) and abs(L1 / L0 - 1 - 0.053333) < 1e-6),
    )
    w_pw = P0_ / P0_.sum()
    report.ok(
        "price weights at day 0 are 33.3, 13.3, 53.3%; C dominates because its price is highest",
        np.allclose(w_pw, [1 / 3, 2 / 15, 8 / 15]),
    )
    P1_split = P1_.copy()
    P1_split[2] /= 2  # C's price halves; its share count doubles
    split = PriceWeightedIndex.based(P1_split, L1)  # S&P DJI eq. (6): the level is kept
    D1 = split.divisor
    report.ok(
        "post-split divisor 1.101266 keeps the level at 105.3333",
        bool(close(D1, 116 / L1) and close(split.level(P1_split), L1)),
    )
    P2 = np.array([54.0, 20.0, 44.0])
    L2 = split.level(P2)
    report.ok(
        "day 2 level 107.1494 (+1.7241%)",
        bool(abs(L2 - 107.149425) < 1e-5 and abs(L2 / L1 - 1 - 0.017241) < 1e-6),
    )
    L2_wrong = base.level(P2)
    report.ok(
        "without the divisor change day 2 would print 78.67, a spurious fall of 25.3%",
        bool(abs(L2_wrong - 78.6667) < 1e-4 and abs(L2_wrong / L1 - 1 + 0.25316) < 1e-4),
    )
    # After the split C's weight halves although nothing economic happened: price-weighted
    # weights depend on price level.
    w_after = P1_split / P1_split.sum()
    report.ok(
        "C's price weight falls from 53.2% to 36.2% at the split",
        bool(abs(P1_[2] / P1_.sum() - 0.5316) < 1e-4 and abs(w_after[2] - 0.3621) < 1e-4),
    )


def check_cap_weighted(report: CheckReport) -> CapIndex:
    """Part 2: the float-adjusted capitalisation-weighted index through a split and an issue."""
    print("== part 2: float-adjusted capitalisation-weighted index")
    P0_, P1_ = np.array(P0), np.array(P1)
    shares0, iwf = np.array(SHARES0), np.array(IWF)
    q0 = shares0 * iwf
    index0 = CapWeightedIndex.based(P0_, q0, 1000.0)
    MV0 = index0.market_value(P0_)
    Dc0 = index0.divisor
    MV1 = index0.market_value(P1_)
    Lc1 = index0.level(P1_)
    report.ok(
        "index market value 12,000 (millions) and divisor 12 for a base of 1,000",
        bool(close(MV0, 12000) and close(Dc0, 12)),
    )
    report.ok("day 1 level 1,016.667 (+1.6667%)", close(Lc1, 12200 / 12))
    w0 = index0.weights(P0_)
    r1 = P1_ / P0_ - 1
    report.ok(
        "the same return as the weighted sum of constituent returns: 1/3 x 10% + 1/2 x (-5%) +"
        " 1/6 x 5%",
        close((w0 * r1).sum(), Lc1 / 1000 - 1),
    )
    # Corporate actions after the close of day 1: C splits 2-for-1 (no market-value change, no
    # divisor change); B issues 30 million new shares (IWF 1.0): market value rises by
    # 19 x 30 = 570, so the divisor rises (eq. (7)).
    shares1 = shares0 * np.array([1.0, 1.0, 2.0]) + np.array([0.0, 30.0, 0.0])
    q1 = shares1 * iwf
    P1_adj = P1_ * np.array([1.0, 1.0, 0.5])
    split_only = CapWeightedIndex(shares=shares0 * np.array([1, 1, 2]) * iwf, divisor=Dc0)
    MV1_split_only = split_only.market_value(P1_adj)
    report.ok(
        "the split alone leaves index market value at 12,200 (no divisor change)",
        close(MV1_split_only, 12200),
    )
    CMV = 19.0 * 30.0
    index1 = index0.after_issue(q1, CMV, Lc1)
    Dc1_add = index1.divisor  # additive form, eq. (7)
    Dc1_mult = index0.rescaled_divisor(index1.market_value(P1_adj), MV1)  # eq. (6)
    report.ok(
        "divisor 12.560656 by eq. (7) = eq. (6)",
        bool(close(Dc1_add, Dc1_mult) and abs(Dc1_add - 12.560656) < 1e-6),
    )
    report.ok("level unchanged across the share issue", close(index1.level(P1_adj), Lc1))
    P2c = np.array([54.0, 20.0, 44.0])
    MV2 = index1.market_value(P2c)
    Lc2 = index1.level(P2c)
    report.ok(
        "day 2 market value 13,120, level 1,044.531 (+2.7408%)",
        bool(
            close(MV2, 13120)
            and abs(Lc2 - 1044.5315) < 1e-4
            and abs(Lc2 / Lc1 - 1 - 0.027408) < 1e-6
        ),
    )
    w1 = index1.weights(P1_adj)
    r2 = P2c / P1_adj - 1
    report.ok(
        "day 2 return equals the post-action weights times returns",
        close((w1 * r2).sum(), Lc2 / Lc1 - 1),
    )
    return CapIndex(index=index1, level1=Lc1, level2=Lc2, r1=r1, r2=r2, p1_adj=P1_adj)


def check_total_return(report: CheckReport, cap: CapIndex) -> None:
    """Part 3: total and net total return on day 2, when B goes ex-dividend."""
    print("== part 3: total return and net total return on day 2 (B goes ex-dividend 0.40)")
    Lc1, Lc2 = cap.level1, cap.level2
    div = np.array([0.0, 0.40, 0.0])
    idx_div_points = cap.index.dividend_points(div)
    report.ok(
        "index dividend points = 0.40 x 330 / 12.560656 = 10.5090",
        bool(abs(idx_div_points - 10.5090) < 1e-4),
    )
    dtr = (Lc2 + idx_div_points) / Lc1 - 1
    report.ok(
        "daily total return 3.7745% against a price return of 2.7408%",
        bool(abs(dtr - 0.037745) < 1e-6),
    )
    # assume TR and price indices start together at 1,000 on day 0, no dividend on day 1
    TR1 = 1000.0 * (Lc1 / 1000.0)
    TR2 = TR1 * (1 + dtr)
    report.ok("TR index: 1,016.667 -> 1,055.040", bool(abs(TR2 - 1055.0405) < 1e-3))
    report.ok(
        "equivalent S&P form TR_t = TR_t-1 x (PR_t + dividend points) / PR_t-1",
        close(TR2, TR1 * (Lc2 + idx_div_points) / Lc1),
    )
    wht = 0.15
    ntr = (Lc2 + idx_div_points * (1 - wht)) / Lc1 - 1
    report.ok("net total return with 15% withholding: 3.6194%", bool(abs(ntr - 0.036194) < 1e-6))
    report.ok("ordering price < net total < total", bool(Lc2 / Lc1 - 1 < ntr < dtr))


def check_equal_weight(report: CheckReport, cap: CapIndex) -> None:
    """Part 4: equal weighting, drift, turnover and additional weight factors."""
    print("== part 4: equal weighting, drift and rebalancing")
    r1, r2, P1_adj = cap.r1, cap.r2, cap.p1_adj
    # Equal-weight index of the same three stocks, base 1,000 on day 0, rebalanced after the
    # close of day 1.
    w_eq0 = np.ones(3) / 3
    Le1 = 1000 * (1 + (w_eq0 * r1).sum())
    report.ok(
        "equal-weight day 1 return 3.3333% (simple average)",
        close(Le1, 1000 * (1 + (0.10 - 0.05 + 0.05) / 3)),
    )
    w_drift = w_eq0 * (1 + r1) / (1 + (w_eq0 * r1).sum())
    report.ok(
        "weights drift to 35.48, 30.65, 33.87%",
        np.allclose(np.round(w_drift, 4), [0.3548, 0.3065, 0.3387]),
    )
    turnover = one_way_turnover(w_eq0, w_drift)
    report.ok(
        "one-way turnover to rebalance = half the sum of |weight changes| = 2.69%",
        bool(abs(turnover - 0.026882) < 1e-6),
    )
    # S&P DJI: AWF_i = Z / (N x float-adjusted market value_i), so every adjusted market value
    # equals Z/N.
    fav = P1_adj * cap.index.shares
    Z = fav.sum()
    awf = cap.index.equal_weight_factors(P1_adj)
    report.ok(
        "AWFs make the adjusted market values equal and preserve the index market value",
        bool(np.allclose(awf * fav, Z / 3) and close((awf * fav).sum(), Z)),
    )
    Le2 = Le1 * (1 + (w_eq0 * r2).sum())
    report.ok(
        "rebalanced equal-weight day 2 return 2.7356% (simple average), level 1,061.601",
        bool(abs(r2.mean() - 0.027356) < 1e-6 and abs(Le2 - 1061.6013) < 1e-3),
    )


def check_bond_index(report: CheckReport) -> None:
    """Part 5: one month of a two-bond index under Bloomberg's conventions."""
    print("== part 5: fixed-income index month (Bloomberg conventions)")
    # Two bonds in the returns universe at the start of the month; par outstanding in millions;
    # prices per 100 par.
    month = BondIndexMonth(
        par=np.array([500.0, 300.0]),
        clean0=np.array([98.0, 102.5]),
        accrued0=np.array([1.00, 0.50]),
        clean1=np.array([99.0, 101.8]),
        accrued1=np.array([1.40, 0.90]),
        coupon_paid=np.array([0.0, 0.0]),
    )
    dirty0 = month.dirty0
    price_ret = month.price_returns()
    coupon_ret = month.coupon_returns()
    bond_tr = month.total_returns()
    mv0 = month.market_values()
    idx_tr = month.index_return()
    report.ok(
        "bond 1: price 1.0101%, coupon 0.4040%, total 1.4141%",
        bool(
            abs(price_ret[0] - 0.010101) < 1e-6
            and abs(coupon_ret[0] - 0.004040) < 1e-6
            and abs(bond_tr[0] - 0.014141) < 1e-6
        ),
    )
    report.ok(
        "bond 2: price -0.6796%, coupon 0.3883%, total -0.2913%",
        bool(abs(price_ret[1] + 0.006796) < 1e-6 and abs(bond_tr[1] + 0.002913) < 1e-6),
    )
    report.ok(
        "beginning market-value weights 61.6 / 38.4% (495 and 309 of 804); index total return"
        " 0.7587%",
        bool(np.allclose(mv0, [495, 309]) and abs(idx_tr - 0.007587) < 1e-6),
    )
    # A new bond issued mid-month enters the projected universe but not the returns universe
    # until month end: adding it would change the weights only from the next month, so the
    # month's return is unchanged by construction.
    dirty_end = month.clean1 + month.accrued1
    report.ok(
        "total return also equals the change in dirty value (no coupon paid)",
        np.allclose(bond_tr, (dirty_end - dirty0) / dirty0),
    )


def main() -> int:
    """Print the versions, then run the five parts with one report.

    Worked examples of meth:index-value-return-calculation and
    def:equity-fixed-income-index-types.

    Three invented stocks A, B and C over three closes (day 0, 1 and 2), a two-bond invented
    fixed-income index over one month, and the conventions of S&P DJI's Index Mathematics
    Methodology (September 2026): level = market value / divisor; the divisor is changed so that
    the level is unchanged by a constituent or share change (eqs. (6) and (7)); a stock split
    changes shares and price but not market value; a price-weighted index adjusts its divisor for a
    split; total return adds index dividend points on the ex-date; net total return deducts
    withholding first; equal weights are reset with additional weight factors at each rebalancing;
    one-way turnover is half the sum of absolute weight changes. Bond returns follow Bloomberg's
    Fixed Income Index Methodology (8 January 2026): price, coupon and paydown return on the
    beginning dirty value, weights fixed at the beginning market value of the returns universe.

    Every input is invented. No random draws.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}")
    report = CheckReport()
    check_price_weighted(report)
    cap = check_cap_weighted(report)
    check_total_return(report, cap)
    check_equal_weight(report, cap)
    check_bond_index(report)
    print()
    if report.failures:
        print(f"{len(report.failures)} check(s) failed: {report.failures}")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
