"""Relative PPP out of sample: the real exchange rate's deviation against a random walk (FRED)."""

import csv
import math
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import ClassVar, Final, Self

import numpy as np
from numpy.typing import ArrayLike

from trading_notes.data_folders import DataFolder
from trading_notes.numerical.macro_fx.ppp_forecasts import ExpandingForecast, StaleDataRule
from trading_notes.numerical.newey_west import Month, add, nw_t, panel_nw_t
from trading_notes.records import Record
from trading_notes.research.fred import monthly_values
from trading_notes.research.macro_fx.currencies import (
    CURRENCIES,
    US_CPI,
    US_RATE,
    RandomWalkComparison,
    turnover,
)
from trading_notes.research.workflow import WorkflowArguments

RULE: Final = StaleDataRule(monthly_lag=2, min_age=4, max_age=6)
START: Final = (1985, 1)
# Expanding-mean predictor: z needs this many real-exchange-rate observations.
MIN_HISTORY: Final = 60
COST_PER_TURNOVER: Final = 0.0005
CSV_HEADER: Final = [
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


class PppObservation(Record):
    """A predictor-eligible month of one currency.

    Attributes:
        q: The log real exchange rate from the price levels known at t.
        age: The age in months of the foreign CPI observation used.
        z: q less its expanding mean, None until MIN_HISTORY observations.
        i: The foreign three-month rate in the month, if reported.
        iu: The US three-month rate in the month, if reported.
    """

    q: float
    age: int
    z: float | None
    i: float | None
    iu: float | None


type Spots = dict[str, dict[Month, float]]
type Predictors = dict[str, dict[Month, PppObservation]]


def summarise_returns(label: str, returns: ArrayLike) -> tuple[float, float]:
    """Print a monthly return series' annualised mean, volatility, Sharpe and NW(12) t."""
    x = np.asarray(returns, dtype=np.float64)
    t = nw_t(x, 12)
    print(
        f"  {label}: n = {len(x)}, mean {x.mean() * 1200:+.2f}%/yr, vol"
        f" {x.std(ddof=1) * math.sqrt(12) * 100:.2f}%/yr, Sharpe"
        f" {x.mean() / x.std(ddof=1) * math.sqrt(12):+.2f}, NW t = {t:+.2f}"
    )
    return float(x.mean()), float(t)


class PppPanel(Record):
    """Each currency's log spot rate and its predictor-eligible months.

    A month is predictor-eligible when the price levels known at t pass the stale-data rule;
    the outcome needs only the spot rates at t and t + h.

    Attributes:
        spot: The log spot rate in dollars per unit of the currency, by month.
        pred: The predictor-eligible months' observations.
    """

    spot: Spots
    pred: Predictors

    @classmethod
    def read(cls, folder: Path) -> Self:
        """Read the FRED files of a folder and form each eligible month's predictor."""
        us_cpi, us_r = (
            monthly_values(folder / f"{US_CPI}.csv"),
            monthly_values(folder / f"{US_RATE}.csv"),
        )
        spot: Spots = {}
        pred: Predictors = {}
        for c, ccy in CURRENCIES.items():
            cpi, rate = (
                monthly_values(folder / f"{ccy.cpi}.csv"),
                monthly_values(folder / f"{ccy.rate}.csv"),
            )
            spot[c] = ccy.log_usd_per_unit(folder)
            rows: dict[Month, PppObservation] = {}
            qs: list[float] = []
            for t in sorted(spot[c]):
                kp = RULE.known_price(cpi, t, ccy.quarterly)
                ku = add(t, -RULE.monthly_lag)
                if kp is None or ku not in us_cpi:
                    continue
                q = spot[c][t] + math.log(kp[0]) - math.log(us_cpi[ku])
                qs.append(q)
                rows[t] = PppObservation(
                    q=q,
                    age=kp[1],
                    z=(q - sum(qs) / len(qs)) if len(qs) >= MIN_HISTORY else None,
                    i=rate.get(t),
                    iu=us_r.get(t),
                )
            pred[c] = rows
        return cls(spot=spot, pred=pred)

    def write(self, path: Path) -> None:
        """Write fx_ppp_monthly.csv: every spot month, with its predictor fields when eligible."""
        with path.open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(CSV_HEADER)
            for c in CURRENCIES:
                for t in sorted(self.spot[c]):
                    r = self.pred[c].get(t)
                    w.writerow(
                        [
                            c,
                            f"{t[0]}-{t[1]:02d}",
                            f"{self.spot[c][t]:.6f}",
                            int(r is not None),
                            "" if r is None else r.age,
                            "" if r is None else f"{r.q:.6f}",
                            "" if r is None or r.z is None else f"{r.z:.6f}",
                            "" if r is None or r.i is None else r.i,
                            "" if r is None or r.iu is None else r.iu,
                        ]
                    )

    def print_samples(self) -> None:
        """Print each currency's spot range, predictor range and CPI ages."""
        print(
            "Samples per currency: spot range; predictor-eligible range (first z, last eligible"
            " month); CPI ages"
        )
        for c in CURRENCIES:
            pred, spot = self.pred[c], self.spot[c]
            zt = [t for t in sorted(pred) if pred[t].z is not None]
            ages = [pred[t].age for t in zt]
            print(
                f"  {c}: spot {min(spot)}-{max(spot)}; z {zt[0]}-{zt[-1]}; age"
                f" {min(ages)}-{max(ages)} months (mean {np.mean(ages):.1f}); spot months after"
                f" the last eligible predictor: {sum(t > zt[-1] for t in spot)}"
            )

    def forecast_test(self, h: int) -> bool:
        """Print the h-month forecast comparisons; return whether they support PPP.

        Statistical support needs the pooled out-of-sample R^2 against a random walk above 0
        and a Clark-West t above 1.65, its scores summed across currencies within each
        forecast-origin month and Newey-West over h - 1 calendar months.
        """
        sse_m = sse_rw = 0.0
        cw_all: list[tuple[Month, float]] = []
        bsum: list[float] = []
        print(
            f"\n== h = {h} months: expanding OLS of ds on z, forecasts from "
            f"{START[0]}-{START[1]:02d}"
        )
        for c in CURRENCIES:
            z = {t: row.z for t, row in self.pred[c].items()}
            fc, ts, X, Y = ExpandingForecast(horizon=h, start=START).forecasts(self.spot[c], z)
            own = RandomWalkComparison(
                actual=np.array([x[2] for x in fc]), forecast=np.array([x[1] for x in fc])
            )
            A = np.column_stack([np.ones(len(ts)), [X[t] for t in ts]])
            bfull = np.linalg.lstsq(A, np.array([Y[t] for t in ts]), rcond=None)[0]
            bsum.append(float(bfull[1]))
            print(
                f"  {c}: n = {len(own.actual)} ({fc[0][0]} to {fc[-1][0]}), OOS R^2 vs RW ="
                f" {own.r2 * 100:+.2f}%, full-sample b = {bfull[1]:+.4f}"
            )
            sse_m += own.sse
            sse_rw += own.sse_random_walk
            cw_all.extend(zip([x[0] for x in fc], own.clark_west, strict=True))
        lags = max(h - 1, 0)
        cwt = panel_nw_t(cw_all, lags)
        r2p = 1 - sse_m / sse_rw
        print(
            f"  pooled OOS R^2 vs RW = {r2p * 100:+.2f}%, Clark-West t = {cwt:+.2f} (scores"
            f" summed by forecast-origin month, Newey-West {lags} calendar-month lags);"
            f" sensitivity with {h} lags: {panel_nw_t(cw_all, h):+.2f}; row-stacked t:"
            f" {nw_t([v for _, v in cw_all], lags):+.2f}"
        )
        print(
            f"  full-sample slopes negative for {sum(b < 0 for b in bsum)} of {len(bsum)} "
            "currencies"
        )
        return bool(r2p > 0 and cwt > 1.65)

    def value_portfolio(self) -> bool:
        """Print the long-cheap, short-dear portfolio; return whether its net mean is significant.

        Each month with at least six eligible currencies goes long the three with the lowest z
        and short the three with the highest, a third each, paying 5 bp per unit of turnover;
        the carry leg uses the interbank-rate differential. A statistical return on
        monthly-average prices, not an executable result. Support needs a net mean (with the
        carry leg) above 0 with a Newey-West t above 2.
        """
        spot, pred = self.spot, self.pred
        alltimes = sorted(set().union(*[set(s) for s in spot.values()]))
        spot_r: list[float] = []
        exc: list[tuple[float, float]] = []
        costs: list[float] = []
        used: list[Month] = []
        prev_w: dict[str, float] = {}
        for t in alltimes:
            if t < START:
                continue
            t1 = add(t, 1)
            scores = {
                c: z
                for c in CURRENCIES
                if (obs := pred[c].get(t)) is not None
                and (z := obs.z) is not None
                and t1 in spot[c]
            }
            if len(scores) < 6:
                continue
            av = sorted(scores, key=scores.__getitem__)
            wts = {c: 1 / 3 for c in av[:3]}
            wts.update({c: -1 / 3 for c in av[-3:]})
            turn = turnover(wts, prev_w)
            prev_w = wts
            ds = sum(wv * (spot[c][t1] - spot[c][t]) for c, wv in wts.items())
            spot_r.append(ds)
            costs.append(COST_PER_TURNOVER * turn)
            used.append(t)
            carry = [
                (wv, i - iu)
                for c, wv in wts.items()
                if (i := pred[c][t].i) is not None and (iu := pred[c][t].iu) is not None
            ]
            if len(carry) == len(wts):
                exc.append((ds + sum(wv * d / 1200 for wv, d in carry), COST_PER_TURNOVER * turn))
        print(
            "\n== Value portfolio on monthly-average rates (long 3 cheapest, short 3 dearest by"
            f" z), {used[0]} to {used[-1]}"
        )
        print(
            "   A statistical portfolio return on averaged prices with interbank-rate carry: not"
            " an executable result."
        )
        summarise_returns("spot, gross", spot_r)
        summarise_returns("spot, net of 5 bp turnover cost", np.array(spot_r) - np.array(costs))
        summarise_returns("with interest differential, gross", np.array([e for e, _ in exc]))
        m, tt = summarise_returns(
            "with interest differential, net of costs", np.array([e - c for e, c in exc])
        )
        print(
            f"  mean turnover cost {np.mean(costs) * 1200:.2f}%/yr; breakeven cost per unit"
            " turnover "
            f"{np.mean(spot_r) / np.mean(np.array(costs) / COST_PER_TURNOVER) * 1e4:.1f} bp (spot)"
        )
        return m > 0 and tt > 2


class Arguments(WorkflowArguments):
    """The PPP test's arguments.

    Attributes:
        source: The folder with the FRED CSV files.
    """

    folder: ClassVar[DataFolder] = DataFolder(subsection="macro_fx")
    source: Path


def main(argv: Sequence[str] | None = None) -> int:
    """Print the PPP results and write fx_ppp_monthly.csv.

    The out-of-sample test of ev:fx-valuation-factors-oos: ds_{t,t+h} = a + b z_t + e, b < 0,
    z_t the deviation of the log real exchange rate from its expanding mean; statistical
    support at h = 12 (see `PppPanel.forecast_test`) and economic support if the value portfolio's
    net mean is positive with a Newey-West t above 2. Monthly CPI is known with a two-month
    lag and nothing older is used; a quarterly CPI (AUD, NZD) is used once its quarter ended
    four to six months before t. Limitations: revised CPI rather than real-time vintages,
    monthly-average spot rates, interbank rates for the carry leg and an assumed 5 bp cost
    per unit of turnover. EUR is excluded (short history). About 2 seconds.

    Returns:
        0.
    """
    parser = Arguments.parser(__doc__ or "")
    parser.add_argument("source", type=Path, help="folder with the FRED CSV files")
    args = Arguments.parse(parser, argv)
    panel = PppPanel.read(args.source)
    panel.write(args.output_folder / "fx_ppp_monthly.csv")
    panel.print_samples()
    stat_ok = [panel.forecast_test(h) for h in (1, 12)][-1]
    econ_ok = panel.value_portfolio()
    print(
        f"\nVerdict: statistical (h = 12) {'supported' if stat_ok else 'not supported'}; "
        f"economic (statistical portfolio) {'supported' if econ_ok else 'not supported'}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
