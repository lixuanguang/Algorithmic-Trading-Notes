"""Static against rolling minimum-variance hedges of Gulf Coast jet fuel with NYMEX contract 1."""

import datetime as dt
import itertools
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import ClassVar, Final, Self

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.commodity_curves.nymex_contracts import ContractCalendar, Market
from trading_notes.records import Record
from trading_notes.research.spreadsheets import eia_series
from trading_notes.research.workflow import WorkflowArguments

type Floats = NDArray[np.float64]
type Prices = dict[dt.date, float]

# The first usable weeks that fit the static hedge; later weeks are out of sample.
STATIC_WEEKS: Final = 260
ROLLING_WEEKS: Final = (104, 52)


def ols_h(s: Floats, f: Floats) -> float:
    """Return the minimum-variance hedge ratio Cov(s, f) / Var(f) by OLS with an intercept."""
    f0 = f - f.mean()
    return float(f0 @ (s - s.mean()) / (f0 @ f0))


class WeeklyChanges(Record):
    """Weekly dollar changes per gallon of the exposure and of the hedge's contract 1.

    Attributes:
        spot: dS, the exposure's change.
        futures: dF, the hedge's change, scaled to dollars per gallon.
        dates: The date ending each change.
        dropped: Weeks excluded because contract 1 changed delivery month, or because its
            delivery month at either end is unknown.
    """

    spot: Floats
    futures: Floats
    dates: list[dt.date]
    dropped: int

    @classmethod
    def of(cls, exposure: Prices, futures: Prices, market: Market, scale: float) -> Self:
        """Return the changes between the last common dates of consecutive ISO weeks.

        A week is kept only if contract 1 is known to be the same contract at both ends.
        """
        calendar = ContractCalendar(market=market, days=tuple(sorted(set(futures))))
        weekly: dict[tuple[int, int], dt.date] = {}
        for d in sorted(set(exposure) & set(futures)):
            weekly[d.isocalendar()[:2]] = d  # last common date of each ISO week
        wd = [weekly[k] for k in sorted(weekly)]
        dS, dF, used, dropped = [], [], [], 0
        for a, b in itertools.pairwise(wd):
            if not calendar.same_contract(a, 1, b, 1):
                dropped += 1
                continue
            dS.append(exposure[b] - exposure[a])
            dF.append((futures[b] - futures[a]) * scale)
            used.append(b)
        return cls(spot=np.array(dS), futures=np.array(dF), dates=used, dropped=dropped)

    def report(self, name: Market) -> None:
        """Print the hedge ratios and the out-of-sample variance reductions of one hedge.

        The header counts the excluded weeks, rolls and unknown contracts together.
        """
        dS, dF, used = self.spot, self.futures, self.dates
        print(
            f"\n== hedge: {name} contract 1; {len(dS)} usable weekly changes {used[0]} to"
            f" {used[-1]}; {self.dropped} weeks excluded (roll or unknown contract)"
        )
        h_static = ols_h(dS[:STATIC_WEEKS], dF[:STATIC_WEEKS])
        out = slice(STATIC_WEEKS, None)
        res = {"static (first 260 weeks)": dS[out] - h_static * dF[out]}
        h_roll = np.empty(0)
        for win in ROLLING_WEEKS:
            hs = np.array(
                [ols_h(dS[i - win : i], dF[i - win : i]) for i in range(STATIC_WEEKS, len(dS))]
            )
            res[f"rolling {win} weeks"] = dS[out] - hs * dF[out]
            if win == 104:
                h_roll = hs
        v0 = dS[out].var(ddof=1)
        print(
            f"  static h = {h_static:.3f}; rolling-104 h ranged {h_roll.min():.3f} to"
            f" {h_roll.max():.3f}; full-sample (in-sample) h = {ols_h(dS, dF):.3f}"
        )
        vr = {k: 1 - v.var(ddof=1) / v0 for k, v in res.items()}
        for k, v in vr.items():
            print(f"  out-of-sample VR, {k}: {v * 100:.1f}%")
        half = (len(dS) - STATIC_WEEKS) // 2
        for lab, sl in (("first half", slice(0, half)), ("second half", slice(half, None))):
            base = dS[out][sl].var(ddof=1)
            dates = used[STATIC_WEEKS:][sl]
            static = 1 - res["static (first 260 weeks)"][sl].var(ddof=1) / base
            rolling = 1 - res["rolling 104 weeks"][sl].var(ddof=1) / base
            print(
                f"  {lab} ({dates[0]} to {dates[-1]}): static {static:.1%}, rolling-104"
                f" {rolling:.1%}"
            )
        print(
            "  verdict: rolling helps"
            if vr["rolling 104 weeks"] > vr["static (first 260 weeks)"]
            else "  verdict: rolling does not help"
        )


class Arguments(WorkflowArguments):
    """The jet-fuel hedge test's arguments.

    Attributes:
        jet: The EIA jet-fuel spot workbook (EIA_<series>.xls).
        heating_oil: The folder with EIA_EER_EPD2F_PE1_Y35NY_DPGd.xls.
        crude: The folder with EIA_RCLC1d.xls.
    """

    folder: ClassVar[str] = "commodity-hedging"
    jet: Path
    heating_oil: Path
    crude: Path


def main(argv: Sequence[str] | None = None) -> int:
    """Print the static and rolling hedge results for heating-oil and WTI hedges.

    The test of meth:time-varying-hedge-ratio under jet-fuel-hedge-protocol.md: weekly
    changes at the last common date of each ISO week; weeks whose contract 1 changes delivery
    month dropped, under the heating-oil expiry for the heating-oil hedge and NYMEX Rule
    200102.F for WTI (42 gallons a barrel); a static h from the first 260 usable weeks against
    rolling h from the previous 104 (sensitivity 52) weeks; out-of-sample variance reduction
    VR = 1 - Var(dS - h dF) / Var(dS) after week 260.

    Returns:
        0.
    """
    parser = Arguments.parser(__doc__ or "")
    parser.add_argument("jet", type=Path, help="the EIA jet-fuel spot .xls")
    parser.add_argument("heating_oil", type=Path, help="folder with the heating-oil futures")
    parser.add_argument("crude", type=Path, help="folder with the WTI futures")
    args = Arguments.parse(parser, argv)
    jet = eia_series(args.jet)
    hedges: dict[Market, tuple[Prices, float]] = {
        "HO": (eia_series(args.heating_oil / "EIA_EER_EPD2F_PE1_Y35NY_DPGd.xls"), 1.0),
        "WTI": (eia_series(args.crude / "EIA_RCLC1d.xls"), 1 / 42),
    }
    print(f"jet fuel: {min(jet)} to {max(jet)}, {len(jet)} days")
    for name, (futures, scale) in hedges.items():
        WeeklyChanges.of(jet, futures, name, scale).report(name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
