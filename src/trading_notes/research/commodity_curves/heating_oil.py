"""Backwardation as scarcity or premium in NY Harbor heating oil futures and distillate stocks."""

import csv
import datetime as dt
import math
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import ClassVar, Final, Self

import numpy as np

from trading_notes.records import Record
from trading_notes.research.commodity_curves.backwardation import (
    CurvePanel,
    CurveSample,
    MonthRow,
    OutOfSample,
    decimal,
)
from trading_notes.research.regressions import NeweyWestOls
from trading_notes.research.spreadsheets import eia_series
from trading_notes.research.workflow import WorkflowArguments

CONTRACT_1: Final = "EER_EPD2F_PE1_Y35NY_DPGd"
CONTRACT_2: Final = "EER_EPD2F_PE2_Y35NY_DPGd"
STOCKS: Final = "WDISTUS1w"
CSV_HEADER: Final = [
    "month_end",
    "next_month_end",
    "held_contract_delivery",
    "B_ln_c1_c2",
    "r_log_next_settle",
    "r_simple",
    "days_before_last_date_either_contract",
    "inventory_week_used",
    "inv_dev",
    "inv_dev_lag14",
]


class HeatingOilMonth(Record):
    """A month pair of the heating-oil panel, with the protocol's log return and its calendar gaps.

    Attributes:
        row: The month row as the shared builder makes it (its r is the simple return).
        r_log: The protocol's held-contract return, ln(C1(t1)/C2(t)).
        gap: Days from t to the last date of its month on which EIA reports either contract.
        gap1: The same for t1.
    """

    row: MonthRow
    r_log: float
    gap: int
    gap1: int

    def csv_row(self) -> list[str | int]:
        """Return the month as written to heating_oil_monthly.csv."""
        x = self.row
        return [
            x.t.isoformat(),
            x.t1.isoformat(),
            f"{x.held_delivery[0]}-{x.held_delivery[1]:02d}",
            f"{x.basis:.6f}",
            f"{self.r_log:.6f}",
            f"{x.r:.6f}",
            self.gap,
            "" if x.week is None else x.week.isoformat(),
            decimal(x.inventory),
            decimal(x.inventory_lag14),
        ]


class HeatingOilSample(Record):
    """The heating-oil month pairs, with the log returns the protocol records.

    Attributes:
        sample: The shared builder's rows and exclusions.
        months: Each row with its log return and calendar gaps.
    """

    sample: CurveSample
    months: list[HeatingOilMonth]

    @classmethod
    def of(cls, panel: CurvePanel) -> Self:
        """Return the panel's month pairs with their gaps to the month's last date in the data.

        "Month-end" is the last date of the month on which EIA reports both contracts; the last
        date with either contract stands in for the month's last trading day.
        """
        sample = panel.build()
        c1, c2 = panel.c1, panel.c2
        last_any: dict[tuple[int, int], dt.date] = {}
        for d in sorted(set(c1) | set(c2)):
            last_any[(d.year, d.month)] = d
        months = [
            HeatingOilMonth(
                row=x,
                r_log=math.log(c1[x.t1] / c2[x.t]),
                gap=(last_any[(x.t.year, x.t.month)] - x.t).days,
                gap1=(last_any[(x.t1.year, x.t1.month)] - x.t1).days,
            )
            for x in sample.rows
        ]
        return cls(sample=sample, months=months)

    def print_gaps(self) -> None:
        """Print how often the selected month-end falls before the proxy last trading day."""
        ho = self.months
        gaps = np.array([m.gap for m in ho])
        worst = max(ho, key=lambda m: m.gap)
        print(
            "  selected month-end vs last date in the month with either contract (proxy last"
            f" trading day): equal in {int((gaps == 0).sum())} of {len(ho)}, earlier by 1-5 days"
            f" in {int(((gaps > 0) & (gaps <= 5)).sum())}, by more than 5 days in"
            f" {int((gaps > 5).sum())} (largest {worst.gap} days, {worst.row.t});"
            f" {sum(m.gap > 0 for m in ho if m.row.t.year < 2007)} of the earlier dates fall"
            " before 2007"
        )

    def report(self) -> None:
        """Print the roll check, the samples, S, P, the exploratory variants and the verdict."""
        sample, ho = self.sample, self.months
        cal = sample.panel.calendar.days
        rows = sample.rows
        print("== HO (NY Harbor No. 2 heating oil / ULSD futures; distillate stocks)")
        print(f"  calendar {cal[0]} to {cal[-1]} ({len(cal)} trading days with both contracts)")
        sample.print_exclusions()
        support = sample.panel.print_roll_check("assumed")
        print(
            f"  roll check supports the assumed expiry in {sum(support)} of {len(support)}"
            " five-year blocks"
        )
        self.print_gaps()
        inv = sample.inventory_rows()
        B = sample.basis()
        r = np.array([m.r_log for m in ho])
        print(f"  price-only sample: {rows[0].t} to {rows[-1].t}, n = {len(rows)}")
        print(f"  inventory sample : {inv[0].t} to {inv[-1].t}, n = {len(inv)}")
        s_fit = sample.scarcity()
        bS, tS = s_fit.coefficients, s_fit.t_stats
        print(f"  S: B on I (inventory sample)        beta_S = {bS[1]:+.4f}  t = {tS[1]:+.2f}")
        sample.print_scarcity_lag14()
        p_fit = NeweyWestOls.fit(r, B)
        bP, tP = p_fit.coefficients, p_fit.t_stats
        print(
            f"  P: r on B (price-only sample)       beta_P = {bP[1]:+.4f}  t = {tP[1]:+.2f}"
            "  (r = log held-contract return)"
        )
        simple = NeweyWestOls.fit(np.array([x.r for x in rows]), B)
        print(
            f"  simple-return P                     beta_P = {simple.coefficients[1]:+.4f}"
            f"  t = {simple.t_stats[1]:+.2f}"
        )
        oos = OutOfSample.of(r, B)
        print(
            f"  P OOS (price-only, from month 121): R^2 = {oos.r2 * 100:+.2f}%"
            f"  Clark-West t = {oos.cw_t:+.2f}  n = {oos.n}"
            f"  (first forecast {rows[120].t})"
        )
        exact = [m for m in ho if m.gap == 0 and m.gap1 == 0]
        e_fit = NeweyWestOls.fit(
            np.array([m.r_log for m in exact]), np.array([m.row.basis for m in exact])
        )
        print(
            "  exploratory (after results; not the verdict): P on pairs whose dates are both the"
            f" proxy last trading day: beta_P = {e_fit.coefficients[1]:+.4f}"
            f"  t = {e_fit.t_stats[1]:+.2f}  n = {len(exact)}"
        )
        executable = sample.executable()
        if executable is not None:
            rule, t_rule = executable
            print(
                "  exploratory, not part of the verdict: executable timing rule net of 2 ticks,"
                f" mean {rule.returns.mean() * 100:+.2f}%/month (NW t {t_rule:+.2f}, n"
                f" {len(rule.gross)})"
            )
        else:
            print(
                "  exploratory executable variant: not computed. HO expires on the last trading"
                " day of the month, so the contract that is C2 at month-end t is already C1 on the"
                " next trading day, and the executable rule (same contract as C2 the next day) has"
                " no valid month; not part of the protocol's verdict"
            )
        S = bS[1] < 0 and tS[1] < -2
        P = bP[1] > 0 and tP[1] > 2 and oos.n > 0 and oos.r2 > 0 and oos.cw_t > 1.65
        ok_roll = sum(support) >= len(support) - 1
        print(
            f"\nHO: roll rule {'supported' if ok_roll else 'NOT supported (verdict not read)'}; "
            f"scarcity {'supported' if S else 'not supported'}; premium"
            f" {'supported' if P else 'not supported'}"
        )


class Arguments(WorkflowArguments):
    """The heating-oil extension's arguments.

    Attributes:
        source: The folder with the two heating-oil futures and the distillate-stocks series.
    """

    folder: ClassVar[str] = "commodity-storage-curves"
    source: Path


def main(argv: Sequence[str] | None = None) -> int:
    """Print the heating-oil results and write heating_oil_monthly.csv.

    The extension of ev:backwardation-scarcity-or-premium to heating oil, under the protocol
    in heating-oil-protocol.md: the same builder, contract identity, inventory deviation,
    availability lag (F + 6 days, distillate stocks from the WPSR) and inference as the WTI
    and Henry Hub test, with the held-contract return taken as the log return the protocol
    records. The roll check must support the assumed expiry before the verdict is read; it
    runs on EIA's calendar of dates with both contracts, so it does not establish the exact
    expiry date. Data (EIA): EER_EPD2F_PE1_Y35NY_DPG and EER_EPD2F_PE2_Y35NY_DPG daily (both
    labelled "New York Harbor No. 2 Heating Oil Future"; contract 2 from February 1994; both
    end 5 April 2024) and WDISTUS1 weekly.

    Returns:
        0.
    """
    parser = Arguments.parser(__doc__ or "")
    parser.add_argument("source", type=Path, help="folder with the EIA_*.xls series")
    args = Arguments.parse(parser, argv)
    c1, c2, st = (
        eia_series(args.source / f"EIA_{n}.xls") for n in (CONTRACT_1, CONTRACT_2, STOCKS)
    )
    ho = HeatingOilSample.of(CurvePanel.of("HO", c1, c2, {}, st))
    ho.report()
    with (args.output_folder / "heating_oil_monthly.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(CSV_HEADER)
        w.writerows(m.csv_row() for m in ho.months)
    return 0


if __name__ == "__main__":
    sys.exit(main())
