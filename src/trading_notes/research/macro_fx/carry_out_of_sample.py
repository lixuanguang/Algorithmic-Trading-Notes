"""Carry out of sample: the lagged rate differential against a random walk, and a portfolio."""

import csv
import math
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import ClassVar, Final, Self

import numpy as np

from trading_notes.numerical.newey_west import Month, add, nw_t, panel_nw_t
from trading_notes.records import Record
from trading_notes.research.fred import monthly_values
from trading_notes.research.macro_fx.currencies import (
    CURRENCIES,
    US_RATE,
    RandomWalkComparison,
    turnover,
)
from trading_notes.research.workflow import WorkflowArguments

START: Final = (1985, 1)
FIRST_FORECAST: Final = (1995, 1)
COST_PER_TURNOVER: Final = 0.0005

type Series = dict[str, dict[Month, float]]


class CarryPanel(Record):
    """Each currency's log spot rate, three-month rate and carry predictor, by month.

    Attributes:
        spot: The log spot rate in dollars per unit of the currency.
        rate: The currency's three-month interbank rate, in percent a year.
        us: The US three-month interbank rate.
        x: The predictor x_t, last month's foreign less US rate, from START on.
    """

    spot: Series
    rate: Series
    us: dict[Month, float]
    x: Series

    @classmethod
    def read(cls, folder: Path) -> Self:
        """Read the FRED files of a folder and form the predictor."""
        us = monthly_values(folder / f"{US_RATE}.csv")
        spot = {c: ccy.log_usd_per_unit(folder) for c, ccy in CURRENCIES.items()}
        rate = {c: monthly_values(folder / f"{ccy.rate}.csv") for c, ccy in CURRENCIES.items()}
        x = {
            c: {
                t: rate[c][add(t, -1)] - us[add(t, -1)]
                for t in spot[c]
                if add(t, -1) in rate[c] and add(t, -1) in us and t >= START
            }
            for c in CURRENCIES
        }
        return cls(spot=spot, rate=rate, us=us, x=x)

    def write(self, path: Path) -> None:
        """Write fx_carry_monthly.csv: each predictor month with its spot rate and both rates."""
        with path.open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(
                ["ccy", "month", "s_ln_usd_per_fx", "x_diff_prev_month", "i_fx_month", "i_us_month"]
            )
            for c in CURRENCIES:
                for t in sorted(self.x[c]):
                    w.writerow(
                        [
                            c,
                            f"{t[0]}-{t[1]:02d}",
                            f"{self.spot[c][t]:.6f}",
                            f"{self.x[c][t]:.4f}",
                            self.rate[c].get(t, ""),
                            self.us.get(t, ""),
                        ]
                    )

    def forecast_test(self, h: int) -> bool:
        """Print the pooled h-month forecast comparison; return whether it supports carry.

        Pooled expanding OLS of ds on x across currencies, each origin fitted on pairs whose
        outcome is known by then (at least 60), forecasts from FIRST_FORECAST. Support needs
        the pooled out-of-sample R^2 above 0 and a Clark-West t above 1.65.
        """
        spot, x = self.spot, self.x
        pairs = sorted(
            (t, c, x[c][t], spot[c][add(t, h)] - spot[c][t])
            for c in CURRENCIES
            for t in x[c]
            if add(t, h) in spot[c]
        )
        months = sorted({p[0] for p in pairs if p[0] >= FIRST_FORECAST})
        a_all: list[float] = []
        f_all: list[float] = []
        o_all: list[Month] = []
        by_c: dict[str, list[tuple[float, float]]] = {}
        last_b = np.zeros(2)
        for t in months:
            tr = [p for p in pairs if add(p[0], h) <= t]
            if len(tr) < 60:
                continue
            A = np.column_stack([np.ones(len(tr)), [p[2] for p in tr]])
            b = np.linalg.lstsq(A, np.array([p[3] for p in tr]), rcond=None)[0]
            last_b = b
            for p in pairs:
                if p[0] == t:
                    fc = b[0] + b[1] * p[2]
                    f_all.append(fc)
                    a_all.append(p[3])
                    o_all.append(t)
                    by_c.setdefault(p[1], []).append((fc, p[3]))
        pooled = RandomWalkComparison(actual=np.array(a_all), forecast=np.array(f_all))
        lags = max(h - 1, 0)
        scores = list(zip(o_all, pooled.clark_west, strict=True))
        cwt = panel_nw_t(scores, lags)
        A = np.column_stack([np.ones(len(pairs)), [p[2] for p in pairs]])
        bfull = np.linalg.lstsq(A, np.array([p[3] for p in pairs]), rcond=None)[0]
        print(
            f"\n== h = {h}: pooled expanding OLS of ds on x, forecasts {months[0]} onward,"
            f" n = {len(a_all)}"
        )
        print(
            f"  full-sample pooled slope b = {bfull[1]:+.5f} per percentage point (UIP benchmark"
            f" {-h / 1200:+.5f}); last expanding b = {last_b[1]:+.5f}"
        )
        for c in CURRENCIES:
            if c in by_c:
                own = RandomWalkComparison(
                    actual=np.array([q[1] for q in by_c[c]]),
                    forecast=np.array([q[0] for q in by_c[c]]),
                )
                print(f"  {c}: n = {len(own.actual)}, OOS R^2 vs RW = {own.r2 * 100:+.2f}%")
        print(
            f"  pooled OOS R^2 vs RW = {pooled.r2 * 100:+.2f}%, Clark-West t = {cwt:+.2f} (scores"
            f" summed by forecast-origin month, Newey-West {lags} calendar-month lags);"
            f" sensitivity with {h} lags: {panel_nw_t(scores, h):+.2f}; row-stacked t:"
            f" {nw_t(pooled.clark_west, lags):+.2f}"
        )
        return bool(pooled.r2 > 0 and cwt > 1.65)

    def portfolio(self) -> bool:
        """Print the median-split carry portfolio; return whether its net mean is significant.

        Each month with at least six currencies goes long those above the median x, short those
        below, equally weighted on each side, earning the rate differential and paying 5 bp per
        unit of turnover. Support needs a net mean above 0 with a Newey-West t above 2.
        """
        spot, rate, us, x = self.spot, self.rate, self.us, self.x
        rets: list[tuple[float, float]] = []
        used: list[Month] = []
        prev: dict[str, float] = {}
        for t in sorted(set().union(*[set(x[c]) for c in CURRENCIES])):
            t1 = add(t, 1)
            av = [c for c in CURRENCIES if t in x[c] and t1 in spot[c] and t in rate[c] and t in us]
            if len(av) < 6:
                continue
            med = float(np.median([x[c][t] for c in av]))
            lo = [c for c in av if x[c][t] > med]
            sh = [c for c in av if x[c][t] < med]
            if not lo or not sh:
                continue
            wts = {**{c: 1 / len(lo) for c in lo}, **{c: -1 / len(sh) for c in sh}}
            turn = turnover(wts, prev)
            prev = wts
            g = sum(
                wv * (spot[c][t1] - spot[c][t] + (rate[c][t] - us[t]) / 1200)
                for c, wv in wts.items()
            )
            rets.append((g, g - COST_PER_TURNOVER * turn))
            used.append(t)
        gr = np.array([r[0] for r in rets])
        nt = np.array([r[1] for r in rets])
        tn = nw_t(nt, 12)
        print(
            f"\n== Carry portfolio (median split on x), {used[0]} to {used[-1]}, n = {len(nt)}"
            " months"
        )
        print(
            f"  gross: mean {gr.mean() * 1200:+.2f}%/yr; net: mean {nt.mean() * 1200:+.2f}%/yr, vol"
            f" {nt.std(ddof=1) * math.sqrt(12) * 100:.2f}%/yr, "
            f"Sharpe {nt.mean() / nt.std(ddof=1) * math.sqrt(12):+.2f}, NW t = {tn:+.2f}"
        )
        worst = np.argsort(nt)[:3]
        print(
            "  three worst months: "
            + ", ".join(f"{used[i][0]}-{used[i][1]:02d} {nt[i] * 100:+.2f}%" for i in sorted(worst))
        )
        return bool(nt.mean() > 0 and tn > 2)


class Arguments(WorkflowArguments):
    """The carry test's arguments.

    Attributes:
        source: The folder with the FRED CSV files.
    """

    folder: ClassVar[str] = "fx-determination-forecasting"
    source: Path


def main(argv: Sequence[str] | None = None) -> int:
    """Print the carry results and write fx_carry_monthly.csv.

    The carry predictor x_t is last month's foreign less US three-month interbank rate; the
    outcome the h-month change in the log spot rate. Statistical support at h = 12 needs a
    pooled out-of-sample R^2 above 0 and a Clark-West t above 1.65; economic support a net
    portfolio mean above 0 with a Newey-West t above 2. The returns are on monthly-average
    spot rates, so they are statistical, not executable.

    Returns:
        0.
    """
    parser = Arguments.parser(__doc__ or "")
    parser.add_argument("source", type=Path, help="folder with the FRED CSV files")
    args = Arguments.parse(parser, argv)
    panel = CarryPanel.read(args.source)
    panel.write(args.output_folder / "fx_carry_monthly.csv")
    print(
        "Samples (predictor available): "
        + "; ".join(f"{c} {min(xc)}-{max(xc)}" for c, xc in panel.x.items() if xc)
    )
    stat_ok = [panel.forecast_test(h) for h in (1, 12)][-1]
    econ_ok = panel.portfolio()
    print(
        f"\nVerdict: statistical (h = 12) {'supported' if stat_ok else 'not supported'}; "
        f"economic (statistical portfolio) {'supported' if econ_ok else 'not supported'}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
