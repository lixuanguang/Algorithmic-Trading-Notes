"""Backwardation as scarcity or premium: WTI and Henry Hub futures against inventories (EIA)."""

import csv
import datetime as dt
import math
import sys
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import ClassVar, Final, Self

import numpy as np
from numpy.typing import NDArray

from trading_notes.data_folders import DataFolder
from trading_notes.numerical.commodity_curves.nymex_contracts import (
    ContractCalendar,
    Market,
    Month,
    available_week,
)
from trading_notes.records import Record
from trading_notes.research.regressions import NeweyWestOls
from trading_notes.research.spreadsheets import eia_series
from trading_notes.research.workflow import WorkflowArguments

type Floats = NDArray[np.float64]
type Bools = NDArray[np.bool_]
type Prices = dict[dt.date, float]

# Two ticks per round trip: WTI $0.01 and NG $0.001 per tick (NYMEX Chapters 200 and 220), an
# assumption; heating oil $0.0001 per gallon, an assumption (rule text not obtained).
TICK: Final[dict[Market, float]] = {"WTI": 0.01, "NG": 0.001, "HO": 0.0001}
# EIA series of each market: contracts 1, 2 and 4 (daily) and stocks (weekly).
SERIES: Final[dict[Market, tuple[str, str, str, str]]] = {
    "WTI": ("RCLC1d", "RCLC2d", "RCLC4d", "WCESTUS1w"),
    "NG": ("RNGC1d", "RNGC2d", "RNGC4d", "NW2_EPG0_SWO_R48_BCFw"),
}
CSV_HEADER: Final = [
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


class StocksHistory(Record):
    """Weekly stocks by the Friday that ends each week.

    Attributes:
        levels: Stocks by week-ending date.
    """

    levels: dict[dt.date, float]

    def dates(self) -> list[dt.date]:
        """Return the week-ending dates in order."""
        return sorted(self.levels)

    def deviation(self, week: dt.date | None) -> float | None:
        """Return ln(stocks) less the mean ln(stocks) of the same ISO week in the five years before.

        None for no week, or when fewer than five earlier years have that ISO week.
        """
        if week is None:
            return None
        wk = week.isocalendar()[1]
        hist = [
            math.log(v)
            for e, v in self.levels.items()
            if e.isocalendar()[1] == wk and week.year - 5 <= e.year < week.year
        ]
        if len(hist) < 5:
            return None
        return math.log(self.levels[week]) - sum(hist) / len(hist)


class MonthRow(Record):
    """One identity-valid month pair (t, t1) of month-end settlements.

    Attributes:
        t: The month-end settlement date.
        t1: The next month's.
        e0: The trading day after t, the executable entry.
        e1: The trading day after t1, the executable exit.
        basis: ln(C1/C2) at t.
        basis4: ln(C1/C4)/3 at t, NaN without contract 4.
        r: The held contract's simple return, C1(t1)/C2(t) - 1.
        r_net: r net of two ticks.
        rx: The executable variant's return, None when its contract identity fails.
        rx_net: rx net of two ticks.
        week: The stocks week public at t, or None.
        inventory: The inventory deviation of that week, or None.
        inventory_lag14: The deviation with a report lag of F + 14 days, or None.
        held_delivery: The delivery month of contract 2 at t.
        next_front: The delivery month of contract 1 at t1.
    """

    t: dt.date
    t1: dt.date
    e0: dt.date
    e1: dt.date
    basis: float
    basis4: float
    r: float
    r_net: float
    rx: float | None
    rx_net: float | None
    week: dt.date | None
    inventory: float | None
    inventory_lag14: float | None
    held_delivery: Month
    next_front: Month | None


class OutOfSample(Record):
    """Expanding-OLS forecasts of y from x against the expanding historical mean.

    Attributes:
        r2: The out-of-sample R^2 against the mean; NaN when too few observations.
        cw_t: The Clark-West t statistic; NaN when too few observations.
        n: The number of forecasts, 0 when too few observations.
    """

    r2: float
    cw_t: float
    n: int

    @classmethod
    def of(cls, y: Floats, x: Floats, start: int = 120) -> Self:
        """Return the comparison of forecasts from observation `start` on (needs start + 13)."""
        if len(y) <= start + 12:
            return cls(r2=float("nan"), cw_t=float("nan"), n=0)
        f_m, f_r, act = [], [], []
        for t in range(start, len(y)):
            X = np.column_stack([np.ones(t), x[:t]])
            b = np.linalg.lstsq(X, y[:t], rcond=None)[0]
            f_r.append(b[0] + b[1] * x[t])
            f_m.append(y[:t].mean())
            act.append(y[t])
        fm, fr, a = np.array(f_m), np.array(f_r), np.array(act)
        r2 = 1 - ((a - fr) ** 2).sum() / ((a - fm) ** 2).sum()
        cw = (a - fm) ** 2 - ((a - fr) ** 2 - (fm - fr) ** 2)
        return cls(
            r2=float(r2), cw_t=float(cw.mean() / (cw.std(ddof=1) / math.sqrt(len(cw)))), n=len(a)
        )


class CurvePanel(Record):
    """A market's nearby futures settlements and stocks on the trading days of the data.

    Attributes:
        calendar: The contract calendar on the dates with both contracts 1 and 2.
        c1: Contract 1 settlements.
        c2: Contract 2 settlements.
        c4: Contract 4 settlements; may be empty.
        stocks: Weekly stocks.
    """

    calendar: ContractCalendar
    c1: Prices
    c2: Prices
    c4: Prices
    stocks: StocksHistory

    @classmethod
    def of(cls, market: Market, c1: Prices, c2: Prices, c4: Prices, stocks: Prices) -> Self:
        """Return the panel on the calendar of dates that have both contracts 1 and 2."""
        calendar = ContractCalendar(market=market, days=tuple(sorted(set(c1) & set(c2))))
        return cls(calendar=calendar, c1=c1, c2=c2, c4=c4, stocks=StocksHistory(levels=stocks))

    def build(self) -> CurveSample:
        """Return the identity-valid month rows and the excluded month-ends with their reasons.

        A pair (t, t1) is used only if both are complete month-ends, t1 is the month after t,
        and contract 2 at t is contract 1 at t1 under every identity rule.
        """
        cal, market = self.calendar, self.calendar.market
        days = cal.days
        ends = cal.complete_month_ends()
        stock_dates = self.stocks.dates()
        c1, c2, c4 = self.c1, self.c2, self.c4
        rows: list[MonthRow] = []
        excluded: list[tuple[dt.date, str]] = []
        for i, t in enumerate(ends):
            nxt = ends[i + 1] if i + 1 < len(ends) else None
            if nxt is None:
                last = days[-1]
                excluded.append((t, f"no complete following month (data end {last})"))
                continue
            if (nxt.year * 12 + nxt.month) - (t.year * 12 + t.month) != 1:
                excluded.append((t, "gap in months"))
                continue
            if not cal.same_contract(t, 2, nxt, 1):
                excluded.append((t, "C2 at t is not C1 at t+1"))
                continue
            e0, e1 = days[days.index(t) + 1], days[days.index(nxt) + 1]
            exe_ok = cal.same_contract(t, 2, e0, 2) and cal.same_contract(t, 2, e1, 1)
            B = math.log(c1[t] / c2[t])
            B4 = math.log(c1[t] / c4[t]) / 3 if t in c4 and c4[t] > 0 else float("nan")
            r = c1[nxt] / c2[t] - 1
            rnet = (c1[nxt] - c2[t] - 2 * TICK[market]) / c2[t]
            rx: float | None
            rxnet: float | None
            if exe_ok and c2[e0] > 0:
                rx = c1[e1] / c2[e0] - 1
                rxnet = (c1[e1] - c2[e0] - 2 * TICK[market]) / c2[e0]
            else:
                rx = rxnet = None
            F = available_week(market, stock_dates, t)
            F14 = available_week(market, stock_dates, t, extra=14)
            dC2 = cal.delivery(t, 2)
            if dC2 is None:
                raise ValueError(f"no delivery month of contract 2 at {t}")
            rows.append(
                MonthRow(
                    t=t,
                    t1=nxt,
                    e0=e0,
                    e1=e1,
                    basis=B,
                    basis4=B4,
                    r=r,
                    r_net=rnet,
                    rx=rx,
                    rx_net=rxnet,
                    week=F,
                    inventory=self.stocks.deviation(F),
                    inventory_lag14=self.stocks.deviation(F14),
                    held_delivery=dC2,
                    next_front=cal.delivery(nxt, 1),
                )
            )
        return CurveSample(panel=self, rows=rows, excluded=excluded)

    def roll_check(self, years: Iterable[int]) -> dict[int, tuple[float, int]]:
        """Return, by offset k of -3..3 trading days from the rule's expiry, the mean roll score.

        The score is (|C1(d+1) - C1(d)| - |C1(d+1) - C2(d)|) / |C2(d)| at the shifted expiry d,
        over expiries with |C1 - C2| / |C2| >= 1%; positive at k = 0 and lower elsewhere
        supports the rule. Each entry is (mean, count).
        """
        cal, c1, c2 = self.calendar.days, self.c1, self.c2
        years = list(years)
        out = {}
        for k in range(-3, 4):
            v = []
            for y in years:
                for m in range(1, 13):
                    e = self.calendar.expiry(y, m)
                    if e is None or e <= cal[5] or e >= cal[-5]:
                        continue
                    i = cal.index(e)
                    if abs(c1[e] - c2[e]) / abs(c2[e]) < 0.01:
                        continue
                    d, n = cal[i + k], cal[i + k + 1]
                    v.append((abs(c1[n] - c1[d]) - abs(c1[n] - c2[d])) / abs(c2[d]))
            out[k] = (float(np.mean(v)) if v else float("nan"), len(v))
        return out

    def five_year_blocks(self) -> list[tuple[int, int]]:
        """Return the five-year blocks of calendar years from the data's first to its last."""
        days = self.calendar.days
        first, last = days[0].year, days[-1].year
        return [(a, min(a + 4, last)) for a in range(first, last + 1, 5)]

    def print_roll_check(self, expiry: str) -> list[bool]:
        """Print the roll check by five-year block; return whether each block supports the rule.

        A block supports it when the score at offset 0 exceeds those at -1 and +1.

        Args:
            expiry: How the expiry is described: "rule" or "assumed".
        """
        print(
            "  roll check (mean score x100 at offset -1 / 0 / +1 trading days from the"
            f" {expiry} expiry; n):"
        )
        support = []
        for a, b in self.five_year_blocks():
            rc = self.roll_check(range(a, b + 1))
            print(
                f"    {a}-{b}: {rc[-1][0] * 100:+.2f} / {rc[0][0] * 100:+.2f} /"
                f" {rc[1][0] * 100:+.2f}  (n {rc[0][1]})"
            )
            support.append(rc[0][0] > max(rc[-1][0], rc[1][0]))
        return support


class TimingRule(Record):
    """Long the held contract if backwardated (B > 0), else short, net of two ticks a month.

    Attributes:
        gross: The held contract's monthly returns.
        net: The same returns net of two ticks.
        backwardated: Whether B > 0 at each signal.
    """

    gross: Floats
    net: Floats
    backwardated: Bools

    @property
    def returns(self) -> Floats:
        """Return the rule's net monthly returns: a short pays the ticks as well."""
        r, rn = self.gross, self.net
        return np.where(self.backwardated, rn, -r - (r - rn))

    def sharpe(self) -> float:
        """Return the rule's annualised Sharpe ratio."""
        x = self.returns
        return float(x.mean() / x.std(ddof=1) * math.sqrt(12))

    def means_by_state(self) -> str:
        """Return the mean gross return in backwardated and contango months."""
        r, bk = self.gross, self.backwardated
        return (
            f"mean monthly r: backwardated {r[bk].mean() * 100:+.2f}% (n {bk.sum()}), contango"
            f" {r[~bk].mean() * 100:+.2f}% (n {(~bk).sum()})"
        )


class CurveSample(Record):
    """A panel's identity-valid month rows, and the month-ends excluded with their reasons.

    Attributes:
        panel: The panel the rows were built from.
        rows: The month rows, in order.
        excluded: The excluded month-ends and why.
    """

    panel: CurvePanel
    rows: list[MonthRow]
    excluded: list[tuple[dt.date, str]]

    def print_exclusions(self) -> None:
        """Print each excluded month-end except gaps, then the number of gaps."""
        for t, why in self.excluded:
            if why != "gap in months":
                print(f"  excluded month-end {t}: {why}")
        gaps = sum(w == "gap in months" for _, w in self.excluded)
        print(f"  excluded for gaps in months: {gaps}")

    def basis(self) -> Floats:
        """Return B = ln(C1/C2) at each month-end."""
        return np.array([x.basis for x in self.rows])

    def inventory_rows(self) -> list[MonthRow]:
        """Return the rows with a usable stocks week."""
        return [x for x in self.rows if x.inventory is not None]

    def scarcity(self) -> NeweyWestOls:
        """Return the fit of B on the inventory deviation I, on the inventory sample."""
        inv = self.inventory_rows()
        return NeweyWestOls.fit(
            np.array([x.basis for x in inv]), np.array([x.inventory for x in inv])
        )

    def print_scarcity_lag14(self) -> None:
        """Print the scarcity fit with the stocks report public at F + 14 days."""
        inv14 = [x for x in self.rows if x.inventory_lag14 is not None]
        fit14 = NeweyWestOls.fit(
            np.array([x.basis for x in inv14]), np.array([x.inventory_lag14 for x in inv14])
        )
        print(
            f"  S sensitivity, report lag F+14 days : beta_S = {fit14.coefficients[1]:+.4f}"
            f"  t = {fit14.t_stats[1]:+.2f}  (n {len(inv14)})"
        )

    def executable(self) -> tuple[TimingRule, float] | None:
        """Return the executable timing rule and its Newey-West t, or None without a valid month.

        The executable variant enters on the trading day after t and exits on the trading day
        after t1, kept only when the contract identity holds on both days.
        """
        ex = [x for x in self.rows if x.rx is not None]
        if not ex:
            return None
        rule = TimingRule(
            gross=np.array([x.rx for x in ex]),
            net=np.array([x.rx_net for x in ex]),
            backwardated=np.array([x.basis for x in ex]) > 0,
        )
        lx = rule.returns
        return rule, float(NeweyWestOls.fit(lx, np.zeros((len(lx), 0))).t_stats[0])

    def report(self) -> tuple[bool, bool]:
        """Print the market's results; return whether scarcity (S) and premium (P) are supported."""
        rows = self.rows
        print(f"\n== {self.panel.calendar.market}")
        self.print_exclusions()
        self.panel.print_roll_check("rule")
        inv = self.inventory_rows()
        B = self.basis()
        r = np.array([x.r for x in rows])
        rn = np.array([x.r_net for x in rows])
        print(
            f"  price-only sample: {rows[0].t} to {rows[-1].t}, n = {len(rows)} (identity-valid,"
            " complete months)"
        )
        print(f"  inventory sample : {inv[0].t} to {inv[-1].t}, n = {len(inv)}")
        Bi = np.array([x.basis for x in inv])
        B4i = np.array([x.basis4 for x in inv])
        ri = np.array([x.r for x in inv])
        Ii = np.array([x.inventory for x in inv])
        s_fit = self.scarcity()
        bS, tS = s_fit.coefficients, s_fit.t_stats
        print(f"  S: B on I (inventory sample)        beta_S = {bS[1]:+.4f}  t = {tS[1]:+.2f}")
        ok4 = ~np.isnan(B4i)
        fit4 = NeweyWestOls.fit(B4i[ok4], Ii[ok4])
        print(
            f"  S (C1/C4 slope)                     beta   = {fit4.coefficients[1]:+.4f}"
            f"  t = {fit4.t_stats[1]:+.2f}"
        )
        self.print_scarcity_lag14()
        p_fit = NeweyWestOls.fit(r, B)
        bP, tP = p_fit.coefficients, p_fit.t_stats
        print(f"  P: r on B (price-only sample)       beta_P = {bP[1]:+.4f}  t = {tP[1]:+.2f}")
        i_fit = NeweyWestOls.fit(ri, Ii)
        print(
            f"  P: r on I (inventory sample)        beta   = {i_fit.coefficients[1]:+.4f}"
            f"  t = {i_fit.t_stats[1]:+.2f}"
        )
        j_fit = NeweyWestOls.fit(ri, np.column_stack([Bi, Ii]))
        bJ, tJ = j_fit.coefficients, j_fit.t_stats
        print(
            f"  P: r on B and I (inventory sample)  beta_B = {bJ[1]:+.4f} (t {tJ[1]:+.2f}),"
            f" beta_I = {bJ[2]:+.4f} (t {tJ[2]:+.2f})"
        )
        oos = OutOfSample.of(r, B)
        if oos.n:
            print(
                f"  P OOS (price-only, from month 121): R^2 = {oos.r2 * 100:+.2f}%"
                f"  Clark-West t = {oos.cw_t:+.2f}  n = {oos.n}"
                f"  (first forecast {rows[120].t})"
            )
        else:
            print("  P OOS: not computed (fewer than 132 months)")
        settle = TimingRule(gross=r, net=rn, backwardated=B > 0)
        print(
            "  statistical, settlement-to-settlement (signal and entry at the same settlement;"
            " not executable):"
        )
        print(f"    {settle.means_by_state()}")
        print(
            "    timing rule (long if B>0 else short), net of 2 ticks: mean"
            f" {settle.returns.mean() * 100:+.2f}%/month, annualised Sharpe {settle.sharpe():+.2f}"
        )
        executable = self.executable()
        if executable is None:
            raise ValueError(f"{self.panel.calendar.market}: no executable month")
        rule, t_rule = executable
        print(
            "  executable variant (signal at settlement t; enter next trading day settlement; exit"
            f" first trading day after t+1), n = {len(rule.gross)}:"
        )
        print(f"    {rule.means_by_state()}")
        print(
            f"    timing rule, net of 2 ticks: mean {rule.returns.mean() * 100:+.2f}%/month (NW t"
            f" {t_rule:+.2f}), annualised Sharpe {rule.sharpe():+.2f}"
        )
        d_fit = NeweyWestOls.fit(r, (B > 0).astype(float))
        print(
            "  exploratory (not pre-specified): r on 1[B>0]  diff ="
            f" {d_fit.coefficients[1] * 100:+.2f}%  t = {d_fit.t_stats[1]:+.2f}"
        )
        print(
            "  months with |r| >= 50% (counted, retained in every estimate):"
            f" {int((np.abs(r) >= 0.5).sum())}"
        )
        S = bool(bS[1] < 0 and abs(tS[1]) > 2)
        P = bool(bP[1] > 0 and abs(tP[1]) > 2 and oos.n > 0 and oos.r2 > 0 and oos.cw_t > 1.65)
        return S, P

    def csv_rows(self) -> list[list[str]]:
        """Return the month rows as written to backwardation_monthly.csv."""
        return [csv_row(self.panel.calendar.market, x) for x in self.rows]


def decimal(v: float | None) -> str:
    """Return a value to six decimals, or an empty field for None."""
    return "" if v is None else f"{v:.6f}"


def csv_row(market: Market, x: MonthRow) -> list[str]:
    """Return a month row as written to backwardation_monthly.csv."""
    return [
        market,
        x.t.isoformat(),
        x.t1.isoformat(),
        f"{x.held_delivery[0]}-{x.held_delivery[1]:02d}",
        f"{x.basis:.6f}",
        f"{x.basis4:.6f}",
        f"{x.r:.6f}",
        f"{x.r_net:.6f}",
        decimal(x.rx),
        decimal(x.rx_net),
        "" if x.week is None else x.week.isoformat(),
        decimal(x.inventory),
        decimal(x.inventory_lag14),
    ]


class Arguments(WorkflowArguments):
    """The backwardation test's arguments.

    Attributes:
        source: The folder with the EIA_*.xls series.
    """

    folder: ClassVar[DataFolder] = DataFolder(subsection="commodity_curves")
    source: Path


def main(argv: Sequence[str] | None = None) -> int:
    """Print the WTI and Henry Hub results and write backwardation_monthly.csv.

    The bounded test of ev:backwardation-scarcity-or-premium on EIA's public NYMEX futures and
    inventory series (RCLC1-4 and RNGC1-4 daily, to 5 April 2024; WCESTUS1 and
    NW2_EPG0_SWO_R48_BCF weekly). S (scarcity, theory of storage) is supported if beta_S < 0
    in B_t = a + beta_S I_t + e_t with |t| > 2; P (premium) if beta_P > 0 in
    r_{t+1} = a + beta_P B_t + u_{t+1} with |t| > 2, and the expanding out-of-sample R^2 from
    month 121 is positive with a Clark-West t above 1.65. OLS t statistics are Newey-West with
    12 lags, on futures (collateral-excess) returns. P and the timing rules use every
    identity-valid month, S and the inventory regressions the months with a usable stocks
    week. About 3 seconds.

    Returns:
        0.
    """
    parser = Arguments.parser(__doc__ or "")
    parser.add_argument("source", type=Path, help="folder with the EIA_*.xls series")
    args = Arguments.parse(parser, argv)
    out: list[list[str]] = []
    verdicts = {}
    for market, names in SERIES.items():
        c1, c2, c4, st = (eia_series(args.source / f"EIA_{n}.xls") for n in names)
        sample = CurvePanel.of(market, c1, c2, c4, st).build()
        verdicts[market] = sample.report()
        out.extend(sample.csv_rows())
    with (args.output_folder / "backwardation_monthly.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(CSV_HEADER)
        w.writerows(out)
    for k, (S, P) in verdicts.items():
        print(
            f"\n{k}: scarcity {'supported' if S else 'not supported'}; premium"
            f" {'supported' if P else 'not supported'}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
