"""Performance presentation standards: the worked GIPS examples.

Performance presentation standards (2026-10-18): the worked examples of
meth:gips-return-calculations, meth:gips-composite-membership and ex:gips-composite-report.

Educational only: every portfolio, flow, fee and return below is invented; nothing describes a
real firm or claims compliance. Rules applied are those of GIPS for Firms (2020 edition) as
cited in the entries: time-weighted returns with sub-period returns at large cash flows
(2.A.24), composite returns asset-weighted by beginning value, by beginning value plus weighted
flows, or by the aggregate method (2.A.36), internal dispersion and the three-year annualised
ex post standard deviation from 36 monthly returns (4.A.1(i)-(j)), with n or n - 1 chosen and
applied consistently (GIPS Handbook for Firms, Nov. 2020, pp. 196-199), and a model fee no lower
than the actual fee (2.A.31). The membership calendar applies an invented composite policy, not
a GIPS rule.

No random draws.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.gips (numpy). Exits 1 on
failure.
"""

# standard library imports
import math
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Final

# third party library imports
import numpy as np
from numpy.typing import NDArray

# project library imports
from trading_notes.numerical.report import CheckReport

type Floats = NDArray[np.float64]


def close(a: float, b: float, tol: float = 1e-9) -> bool:
    """Return whether |a - b| <= tol."""
    return abs(a - b) <= tol


def mod_dietz(bmv: float, emv: float, flows: Sequence[tuple[float, float]]) -> float:
    """Return the Modified Dietz return.

    Args:
        bmv: Beginning market value.
        emv: Ending market value.
        flows: Each external flow as (amount, weight = fraction of the period remaining).
    """
    return (emv - bmv - sum(f for f, _ in flows)) / (bmv + sum(f * wt for f, wt in flows))


@dataclass(frozen=True)
class MembershipRule:
    """One portfolio's dates under the invented composite policy, in fractional months.

    Attributes:
        start: When it was funded; 0 if held all year.
        end: When it was terminated, if it was.
        sig_flow_month: The month of a client-directed flow of 25% or more, if any.
        mandate_change: When the client changed its mandate, if it did.
        nondiscretionary: Whether it is non-discretionary.
    """

    start: float
    end: float | None = None
    sig_flow_month: int | None = None
    mandate_change: float | None = None
    nondiscretionary: bool = False

    def member(self, m: int) -> bool:
        """Return whether the portfolio is in the composite in month m (1 to 12)."""
        if self.nondiscretionary:
            return False
        if self.start != 0 and m < math.floor(self.start) + 1:  # first full month after funding
            return False
        if self.end is not None and m >= math.floor(self.end):
            return False
        if self.sig_flow_month is not None and m in (self.sig_flow_month, self.sig_flow_month + 1):
            return False
        return not (self.mandate_change is not None and m >= math.floor(self.mandate_change) + 1)


# Policy (invented, documented ex ante): new portfolios enter at the first full month after
# funding; a client-directed flow of 25% or more of beginning value removes the portfolio for
# that month and the next; terminated portfolios stay through the last full month; a documented
# mandate change moves the portfolio at the next full month and its history stays in the old
# composite; non-discretionary portfolios are never included.
POLICY: Final = {
    "P1": MembershipRule(start=0),  # held all year
    "P2": MembershipRule(start=3.4),  # funded 12 March
    "P3": MembershipRule(start=0, sig_flow_month=8),  # 30% withdrawal on 15 August
    "P4": MembershipRule(start=0, end=11.67),  # terminated 20 November
    "P5": MembershipRule(start=0, mandate_change=6.3),  # client changes mandate on 10 June
    "P6": MembershipRule(start=0, nondiscretionary=True),
}


def monthly_returns() -> tuple[Floats, Floats]:
    """Return 60 invented monthly composite and benchmark returns, in percent."""
    t = np.arange(60)
    comp = 0.7 + 3.2 * np.sin(0.55 * t) + 0.6 * np.cos(1.7 * t)
    bench = 0.6 + 3.0 * np.sin(0.55 * t) + 0.5 * np.cos(1.7 * t + 0.3)
    return comp, bench


def check_one_portfolio(report: CheckReport) -> float:
    """Part 1: the true time-weighted return against Modified Dietz; return the former."""
    print("== part 1: one portfolio, one 30-day month, a large inflow on day 10")
    bmv, v10, flow, emv = 10.0, 10.30, 3.0, 13.90  # millions; v10 is the value just before the flow
    twr = (v10 / bmv) * (emv / (v10 + flow)) - 1
    md = mod_dietz(bmv, emv, [(flow, 20 / 30)])
    report.ok(
        "true time-weighted return 7.6466% (sub-periods split at the flow)",
        abs(twr - 0.076466) < 1e-6,
    )
    report.ok("Modified Dietz 7.50% (end-of-day flow, weight 20/30)", close(md, 0.075))
    report.ok(
        "the flow is 30% of value, above a 10% large-cash-flow threshold, so the sub-period method"
        " is required",
        flow / v10 > 0.10,
    )
    return twr


def check_composite_return(report: CheckReport, rX: float) -> None:
    """Part 2: the composite return by the three permitted approaches."""
    print("== part 2: composite return by the three permitted approaches")
    # X: the portfolio of part 1. Y: withdrawal of 2.0 on day 20 (8% of value: not large), so
    # Modified Dietz applies.
    rY = mod_dietz(25.0, 23.6, [(-2.0, 10 / 30)])
    rZ = mod_dietz(40.0, 41.2, [])
    report.ok("Y returns 2.4658%, Z 3.0%", abs(rY - 0.024658) < 1e-6 and close(rZ, 0.03))
    B = np.array([10.0, 25.0, 40.0])
    R = np.array([rX, rY, rZ])
    comp_bmv = B @ R / B.sum()
    adj = B + np.array([3.0 * 20 / 30, -2.0 * 10 / 30, 0.0])
    comp_flows = adj @ R / adj.sum()
    agg = mod_dietz(B.sum(), 13.9 + 23.6 + 41.2, [(3.0, 20 / 30), (-2.0, 10 / 30)])
    print(
        f"    beginning-value {comp_bmv:.6f}, with weighted flows {comp_flows:.6f}, aggregate"
        f" {agg:.6f}"
    )
    report.ok("beginning-value weighting 3.4415%", bool(abs(comp_bmv - 0.034415) < 1e-6))
    report.ok(
        "beginning value plus weighted flows 3.5602% (X's inflow raises its weight)",
        bool(abs(comp_flows - 0.035602) < 1e-6),
    )
    report.ok(
        "aggregate method (one combined Modified Dietz, ignoring X's large flow) 3.5371%",
        abs(agg - 0.035371) < 1e-6,
    )
    report.ok(
        "the three answers span 0.12 points; none is biased in general, so the method is a"
        " disclosed policy",
        bool(
            abs(max(comp_bmv, comp_flows, agg) - min(comp_bmv, comp_flows, agg) - 0.001187) < 1e-6
        ),
    )


def check_dispersion(report: CheckReport) -> None:
    """Part 3: internal dispersion of the seven full-year portfolios."""
    print(
        "== part 3: internal dispersion for the seven portfolios held all of 2025 (gross annual"
        " returns, percent)"
    )
    ret = np.array([10.0, 10.9, 9.2, 12.1, 10.6, 8.7, 11.4])
    bv = np.array([12.0, 30.0, 8.0, 20.0, 15.0, 5.0, 10.0])
    eq_sd = ret.std(ddof=0)
    eq_sd1 = ret.std(ddof=1)
    wv = bv / bv.sum()
    aw_mean = wv @ ret
    aw_sd = math.sqrt(wv @ (ret - aw_mean) ** 2)
    q1, q3 = np.percentile(ret, [75, 25])
    print(
        f"    equal-weighted sd {eq_sd:.4f} (n), {eq_sd1:.4f} (n-1); asset-weighted mean"
        f" {aw_mean:.4f}, sd {aw_sd:.4f}; high {ret.max()} low {ret.min()}; IQR {q1 - q3:.3f}"
    )
    report.ok(
        "equal-weighted mean 10.41, sd 1.11 (n) or 1.20 (n - 1)",
        bool(
            abs(ret.mean() - 10.4143) < 1e-4
            and abs(eq_sd - 1.1128) < 1e-4
            and abs(eq_sd1 - 1.2020) < 1e-4
        ),
    )
    report.ok(
        "asset-weighted mean 10.791, asset-weighted sd 0.94",
        bool(abs(aw_mean - 10.791) < 1e-9 and abs(aw_sd - 0.9408) < 1e-4),
    )
    report.ok(
        "high 12.1, low 8.7, range 3.4 points", bool(abs(ret.max() - ret.min() - 3.4) < 1e-12)
    )
    report.ok(
        "more than five full-year portfolios, so a dispersion measure must be presented",
        len(ret) > 5,
    )


def check_ex_post_sd(report: CheckReport, comp: Floats) -> float:
    """Part 4: the n and n - 1 three-year standard deviations; return the n version."""
    print("== part 4: three-year annualised ex post standard deviation")
    last36 = comp[24:60]
    sd36: float = last36.std(ddof=0) * math.sqrt(12)
    sd36_1 = last36.std(ddof=1) * math.sqrt(12)
    report.ok(
        "n and n - 1 versions differ by the factor sqrt(36/35)",
        bool(abs(sd36_1 / sd36 - math.sqrt(36 / 35)) < 1e-12),
    )
    return sd36


def check_membership(report: CheckReport) -> None:
    """Part 5: the membership calendar under the invented policy."""
    print("== part 5: membership calendar under an invented composite policy")
    months = list(range(1, 13))
    table = {p: [rule.member(m) for m in months] for p, rule in POLICY.items()}
    counts = [sum(table[p][m - 1] for p in POLICY) for m in months]
    print(f"    portfolios in the composite by month: {counts}")
    report.ok("P2 (funded 12 March) first counts in April", table["P2"].index(True) + 1 == 4)
    report.ok(
        "P3 is out for August and September only",
        [m for m in months if not table["P3"][m - 1]] == [8, 9],
    )
    report.ok(
        "P4 (terminated 20 November) counts through October",
        [m for m in months if table["P4"][m - 1]][-1] == 10,
    )
    report.ok(
        "P5 leaves from July; January-June stay in this composite's history",
        [m for m in months if table["P5"][m - 1]] == [1, 2, 3, 4, 5, 6],
    )
    report.ok("P6 (non-discretionary) never counts", not any(table["P6"]))
    report.ok(
        "monthly counts 4, 4, 4, 5, 5, 5, 4, 3, 3, 4, 3, 3",
        counts == [4, 4, 4, 5, 5, 5, 4, 3, 3, 4, 3, 3],
    )
    report.ok(
        "only P1 is a full-year member, so only P1 would enter this year's internal dispersion",
        [p for p in POLICY if all(table[p])] == ["P1"],
    )


def check_net_of_fee(report: CheckReport, comp: Floats, model_fee: float) -> None:
    """Part 6: net-of-fee returns with a model fee no lower than the actual fee."""
    print("== part 6: net-of-fee returns with a model fee")
    actual_fee = 0.0075  # annual rate, charged monthly
    gross12 = comp[48:60] / 100
    net12 = (1 + gross12) / (1 + model_fee / 12) - 1
    g_ann, n_ann = float(np.prod(1 + gross12) - 1), float(np.prod(1 + net12) - 1)
    report.ok(
        "annual net = (1 + gross)/(1 + 1%/12)^12 - 1",
        close(1 + n_ann, (1 + g_ann) / (1 + model_fee / 12) ** 12),
    )
    report.ok(
        "model fee 1.00% >= actual 0.75%: model net returns are not higher than actual-fee net"
        " returns (2.A.31)",
        bool((1 + g_ann) / (1 + model_fee / 12) ** 12 <= (1 + g_ann) / (1 + actual_fee / 12) ** 12),
    )


def check_composite_report(
    report: CheckReport, comp: Floats, bench: Floats, model_fee: float, sd36: float
) -> None:
    """Part 7: the five-year report's rows, and its three-year standard deviations."""
    print("== part 7: synthetic five-year report (inception 1 January 2021; years 2021-2025)")
    rows = []
    for y in range(5):
        c = comp[12 * y : 12 * y + 12] / 100
        b_ = bench[12 * y : 12 * y + 12] / 100
        cg = np.prod(1 + c) - 1
        cn = np.prod((1 + c) / (1 + model_fee / 12)) - 1
        bb = np.prod(1 + b_) - 1
        if y >= 2:
            sdc = comp[12 * y - 24 : 12 * y + 12].std(ddof=0) * math.sqrt(12)
            sdb = bench[12 * y - 24 : 12 * y + 12].std(ddof=0) * math.sqrt(12)
        else:
            sdc = sdb = float("nan")
        rows.append((2021 + y, 100 * cg, 100 * cn, 100 * bb, sdc, sdb))
        print(
            f"    {2021 + y}: gross {100 * cg:7.2f}  net {100 * cn:7.2f}  benchmark {100 * bb:7.2f}"
            f"  3y sd comp {sdc:6.2f}  bench {sdb:6.2f}"
        )
    report.ok(
        "three-year sd is reported only from 2023, when 36 monthly returns exist",
        math.isnan(rows[1][4]) and not math.isnan(rows[2][4]),
    )
    report.ok("every net return is below its gross return", all(r[2] < r[1] for r in rows))
    report.ok("2025's three-year sd uses months 25-60, the same as part 4", close(rows[4][4], sd36))
    print(f"    composite and benchmark sd (2025): {rows[4][4]:.4f}, {rows[4][5]:.4f}")


def main() -> int:
    """Print the versions, then run the seven parts with one report.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}")
    report = CheckReport()
    twr = check_one_portfolio(report)
    check_composite_return(report, twr)
    check_dispersion(report)
    comp, bench = monthly_returns()
    sd36 = check_ex_post_sd(report, comp)
    check_membership(report)
    model_fee = 0.0100  # annual rate, charged monthly
    check_net_of_fee(report, comp, model_fee)
    check_composite_report(report, comp, bench, model_fee, sd36)
    print()
    if report.failures:
        print(f"{len(report.failures)} check(s) failed: {report.failures}")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
