"""Whether WTI commercial hedging pressure (CFTC Commitments of Traders) predicts returns."""

import bisect
import csv
import datetime as dt
import io
import sys
import zipfile
from collections.abc import Sequence
from pathlib import Path
from typing import ClassVar, Final, Self

import numpy as np

from trading_notes.records import Record
from trading_notes.research.commodity_curves.backwardation import OutOfSample
from trading_notes.research.regressions import NeweyWestOls
from trading_notes.research.workflow import WorkflowArguments

WTI_CODE: Final = "067651"
COLUMNS: Final = (
    "Market and Exchange Names",
    "As of Date in Form YYYY-MM-DD",
    "CFTC Contract Market Code",
    "Commercial Positions-Long (All)",
    "Commercial Positions-Short (All)",
)


class HedgingPressure(Record):
    """Weekly commercial hedging pressure of one contract market, from the legacy COT report.

    Attributes:
        by_date: HP = (commercial short - commercial long) / (short + long) by positions date.
        names: The first and last positions date reported under each market name.
    """

    by_date: dict[dt.date, float]
    names: dict[str, tuple[dt.date, dt.date]]

    @classmethod
    def read(cls, folder: Path, code: str = WTI_CODE) -> Self:
        """Read the futures-only reports in the deacot*.zip files of a folder, in name order."""
        rep: dict[dt.date, float] = {}
        names: dict[str, tuple[dt.date, dt.date]] = {}
        for path in sorted(folder.glob("deacot*.zip")):
            with zipfile.ZipFile(path) as z:
                for n in z.namelist():
                    r = csv.reader(io.TextIOWrapper(z.open(n), encoding="latin-1"))
                    h = next(r)
                    ci = {k: h.index(k) for k in COLUMNS}
                    for row in r:
                        if row[ci["CFTC Contract Market Code"]].strip() != code:
                            continue
                        d = dt.date.fromisoformat(row[ci["As of Date in Form YYYY-MM-DD"]].strip())
                        lo = float(row[ci["Commercial Positions-Long (All)"]])
                        sh = float(row[ci["Commercial Positions-Short (All)"]])
                        rep[d] = (sh - lo) / (sh + lo)
                        name = row[ci["Market and Exchange Names"]].strip()
                        first, last = names.get(name, (d, d))
                        names[name] = (min(first, d), max(last, d))
        return cls(by_date=rep, names=names)


class HedgingMonth(Record):
    """A WTI month-end with the hedging pressure of the latest report known at it.

    Attributes:
        t: The month-end settlement date.
        positions: The positions date R of the report used, with R + 3 days <= t.
        hp: Its hedging pressure.
        basis: ln(C1/C2) at t, from the backwardation panel.
        r: The held contract's simple return to the next month-end, from the same panel.
    """

    t: dt.date
    positions: dt.date
    hp: float
    basis: float
    r: float


class HedgingSample(Record):
    """The WTI months of the backwardation panel with the hedging pressure known at each.

    Attributes:
        pressure: The weekly hedging pressure.
        rows: The months, in order.
    """

    pressure: HedgingPressure
    rows: list[HedgingMonth]

    @classmethod
    def of(cls, pressure: HedgingPressure, panel: Path) -> Self:
        """Return the WTI months of backwardation_monthly.csv that have a report known by then."""
        dates = sorted(pressure.by_date)
        rows = []
        with panel.open() as f:
            for x in csv.DictReader(f):
                if x["market"] != "WTI":
                    continue
                t = dt.date.fromisoformat(x["month_end"])
                i = bisect.bisect_right(dates, t - dt.timedelta(days=3)) - 1
                if i < 0:
                    continue
                rows.append(
                    HedgingMonth(
                        t=t,
                        positions=dates[i],
                        hp=pressure.by_date[dates[i]],
                        basis=float(x["B_ln_c1_c2"]),
                        r=float(x["r_next_settle"]),
                    )
                )
        return cls(pressure=pressure, rows=rows)

    def report(self) -> None:
        """Print the sample, the predictive regression, its out-of-sample test and the verdict."""
        rows = self.rows
        dates = sorted(self.pressure.by_date)
        print(f"COT {WTI_CODE}: {len(dates)} weekly reports, {dates[0]} to {dates[-1]}")
        for k, (first, last) in sorted(self.pressure.names.items(), key=lambda x: x[1][0]):
            print(f'  name "{k}": {first} to {last}')
        print(
            f"sample: {rows[0].t} to {rows[-1].t}, n = {len(rows)} months; report age at"
            f" month-end {min((x.t - x.positions).days for x in rows)}-"
            f"{max((x.t - x.positions).days for x in rows)} days"
        )
        hp = np.array([x.hp for x in rows])
        r = np.array([x.r for x in rows])
        B = np.array([x.basis for x in rows])
        print(
            f"HP: mean {hp.mean():+.3f}, sd {hp.std(ddof=1):.3f}, min {hp.min():+.3f}, max"
            f" {hp.max():+.3f}"
        )
        fit = NeweyWestOls.fit(r, hp)
        b, tstat = fit.coefficients, fit.t_stats
        print(f"H: r on HP   beta = {b[1]:+.4f}  NW t = {tstat[1]:+.2f}")
        oos = OutOfSample.of(r, hp)
        print(
            f"H OOS (from month 121): R^2 = {oos.r2 * 100:+.2f}%  Clark-West t = {oos.cw_t:+.2f}"
            f"  n = {oos.n}  (first forecast {rows[120].t})"
        )
        print(f"alongside: corr(HP, B) = {np.corrcoef(hp, B)[0, 1]:+.3f}")
        joint = NeweyWestOls.fit(r, np.column_stack([B, hp]))
        bj, tj = joint.coefficients, joint.t_stats
        print(
            f"alongside: r on B and HP   beta_B = {bj[1]:+.4f} (t {tj[1]:+.2f}), beta_HP ="
            f" {bj[2]:+.4f} (t {tj[2]:+.2f})"
        )
        ok = b[1] > 0 and tstat[1] > 2 and oos.n > 0 and oos.r2 > 0 and oos.cw_t > 1.65
        print(f"\nVerdict: hedging pressure {'supported' if ok else 'not supported'}")

    def write(self, path: Path) -> None:
        """Write hedging_pressure_monthly.csv."""
        with path.open("w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["month_end", "cot_positions_date", "hp", "B_ln_c1_c2", "r_next_settle"])
            for x in self.rows:
                w.writerow(
                    [
                        x.t.isoformat(),
                        x.positions.isoformat(),
                        f"{x.hp:.6f}",
                        f"{x.basis:.6f}",
                        f"{x.r:.6f}",
                    ]
                )


class Arguments(WorkflowArguments):
    """The hedging-pressure test's arguments.

    Attributes:
        source: The folder with the CFTC deacot*.zip files.
    """

    folder: ClassVar[str] = "commodity-storage-curves"
    source: Path


def main(argv: Sequence[str] | None = None) -> int:
    """Print the hedging-pressure results and write hedging_pressure_monthly.csv.

    The test under hedging-pressure-protocol.md: HP_t from the CFTC legacy futures-only
    report for contract market 067651, the latest report with positions date R and
    R + 3 days <= t; hypothesis H, beta > 0 in r_{t+1} = a + beta HP_t + u, r the WTI
    held-contract return of backwardation_monthly.csv (read from the artefact folder below
    the root), supported if the Newey-West (12 lags) t > 2 and the expanding out-of-sample
    R^2 from month 121 is positive with a Clark-West t > 1.65.

    Returns:
        0.
    """
    parser = Arguments.parser(__doc__ or "")
    parser.add_argument("source", type=Path, help="folder with the deacot*.zip files")
    args = Arguments.parse(parser, argv)
    sample = HedgingSample.of(
        HedgingPressure.read(args.source), args.artefacts / "backwardation_monthly.csv"
    )
    sample.report()
    sample.write(args.output_folder / "hedging_pressure_monthly.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
