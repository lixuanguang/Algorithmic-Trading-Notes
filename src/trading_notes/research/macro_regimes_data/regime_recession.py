"""The regime map's recession row, on a Sahm-type signal from real-time unemployment vintages."""

import csv
import math
import sys
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import ClassVar, Final, Self

import numpy as np

from trading_notes.numerical.newey_west import Month, add, mdiff
from trading_notes.records import Record
from trading_notes.research.fred import monthly_means
from trading_notes.research.macro_regimes_data.regime_inputs import (
    RealTimeVintage,
    episodes,
    indicator_slope,
)
from trading_notes.research.workflow import WorkflowArguments

type Series = dict[Month, float]
type Industries = dict[Month, dict[str, float]]

SAHM_THRESHOLD: Final = 0.5
# Goods-only broad dollar (TWEXBMTH) to 2019-12; DTWEXBGS (goods and services) afterwards.
DOLLAR_SPLICE: Final = (2019, 12)
# NBER business-cycle peaks and troughs since 1969: a month m with peak < m <= trough is a
# recession month.
PEAKS_TROUGHS: Final = (
    ((1969, 12), (1970, 11)),
    ((1973, 11), (1975, 3)),
    ((1980, 1), (1980, 7)),
    ((1981, 7), (1982, 11)),
    ((1990, 7), (1991, 3)),
    ((2001, 3), (2001, 11)),
    ((2007, 12), (2009, 6)),
    ((2020, 2), (2020, 4)),
)
NBER: Final = {
    p_k for p, t in PEAKS_TROUGHS for p_k in (add(p, k) for k in range(1, mdiff(t, p) + 1))
}
# Each response, its hypothesised sign in recession, and its label in the report.
WANT: Final = {"dy10": -1, "dcred": +1, "eq": -1, "dfn": +1, "usd_g": +1, "usd_gs": +1, "usd": +1}
LABEL: Final = {
    "usd_g": "usd (goods only, TWEXBMTH, to 2019)",
    "usd_gs": "usd (goods+services, DTWEXBGS, 2006-)",
    "usd": "usd (v1 splice; definition break 2020-01)",
}
CSV_HEADER: Final = [
    "vintage_month",
    "sahm_realtime",
    "signal",
    "nber_any_overlap",
    "nber_all_months",
    "dy10",
    "dcred",
    "eq",
    "dfn",
    "usd_goods_only",
    "usd_goods_services",
    "usd_splice_v1",
]


def french(path: Path, cols: set[str], section_header: str | None = None) -> Industries:
    """Return the monthly rows of a Ken French CSV file, the named columns only, in percent.

    With a section header, reading starts after the line containing it and stops at the end
    of that section's monthly block.
    """
    out: Industries = {}
    on = section_header is None
    header: list[str] = []
    with path.open() as f:
        for line in f:
            if section_header and section_header in line:
                on = True
                continue
            if not on:
                continue
            parts = [p.strip() for p in line.split(",")]
            if parts[0] == "" and len(parts) > 1 and parts[1]:
                header = parts
                continue
            if len(parts[0]) == 6 and parts[0].isdigit():
                out[(int(parts[0][:4]), int(parts[0][4:]))] = {
                    h: float(x) for h, x in zip(header[1:], parts[1:], strict=False) if h in cols
                }
            elif out and (parts[0] == "" or not parts[0].isdigit()):
                break
    return out


def log_change(src: Series, a: Month, b: Month) -> float | None:
    """Return 100 ln(src[b] / src[a]), or None if either month is missing."""
    if a not in src or b not in src:
        return None
    return 100 * math.log(src[b] / src[a])


def spliced_log_change(goods: Series, broad: Series, a: Month, b: Month) -> float | None:
    """Return 100 ln of the dollar's change from a to b, chained across the splice by changes."""
    tot, m = 0.0, a
    while m < b:
        n = add(m, 1)
        src = goods if n <= DOLLAR_SPLICE else broad
        if m not in src or n not in src:
            return None
        tot += 100 * math.log(src[n] / src[m])
        m = n
    return tot


class SahmSignals(Record):
    """The real-time Sahm-type indicator of each unemployment vintage.

    Attributes:
        by_month: (three-month average at L less the minimum three-month average over
            L-12..L-1, L) by vintage month, L the last month reported.
        skipped: Vintages with a missing month inside the 15-month window.
    """

    by_month: dict[Month, tuple[float, Month]]
    skipped: list[str]

    @classmethod
    def of(cls, vintages: Sequence[RealTimeVintage]) -> Self:
        """Return the indicator of each vintage that has its whole window."""
        signals: dict[Month, tuple[float, Month]] = {}
        skipped: list[str] = []
        for v in vintages:
            u = v.levels
            L = max(u)

            def a3(m: Month, u: Series = u) -> float:
                return sum(u[add(m, -k)] for k in range(3)) / 3

            try:
                cur = a3(L)
                prev = min(a3(add(L, -k)) for k in range(1, 13))
            except KeyError:
                skipped.append(v.name)  # a month inside the 15-month window is missing (#N/A)
                continue
            signals[v.month] = (cur - prev, L)
        return cls(by_month=signals, skipped=skipped)


class RegimeQuarter(Record):
    """A vintage month's regime flags and the responses over the next three months.

    Attributes:
        month: The vintage month m.
        sahm: The real-time indicator.
        signal: Whether it is at least 0.5 point.
        nber_any: Whether any response month lies in an NBER recession.
        nber_all: Whether all three do.
        responses: dy10, dcred, eq, dfn and the three dollar measures (None where missing).
    """

    month: Month
    sahm: float
    signal: bool
    nber_any: bool
    nber_all: bool
    responses: dict[str, float | None]

    def csv_row(self) -> list[str | int]:
        """Return the quarter as written to regime_quarters.csv."""
        row: list[str | int] = [
            f"{self.month[0]}-{self.month[1]:02d}",
            f"{self.sahm:.3f}",
            int(self.signal),
            int(self.nber_any),
            int(self.nber_all),
        ]
        for k in ("dy10", "dcred", "eq", "dfn", "usd_g", "usd_gs", "usd"):
            v = self.responses[k]
            row.append("" if v is None else f"{v:.4f}")
        return row


class MarketData(Record):
    """The monthly responses' sources.

    Attributes:
        gs10: FRED GS10, monthly average.
        baa: FRED Moody's Baa yield, monthly average.
        dollar_goods: The goods-only broad dollar index (TWEXBMTH).
        dollar_broad: The goods-and-services broad dollar index (DTWEXBGS), monthly average.
        factors: Ken French's Mkt-RF and RF.
        industries: French's value-weighted NoDur, Utils and Hlth returns.
    """

    gs10: Series
    baa: Series
    dollar_goods: Series
    dollar_broad: Series
    factors: Industries
    industries: Industries

    @classmethod
    def read(cls, source: Path) -> Self:
        """Read the FRED and French files below the empirical folder."""
        return cls(
            gs10=monthly_means(source / "fred" / "GS10.csv"),
            baa=monthly_means(source / "fred" / "BAA.csv"),
            dollar_goods=monthly_means(source / "fred" / "TWEXBMTH.csv"),
            dollar_broad=monthly_means(source / "fred" / "DTWEXBGS.csv"),
            factors=french(source / "french" / "F-F_Research_Data_Factors.csv", {"Mkt-RF", "RF"}),
            industries=french(
                source / "french" / "12_Industry_Portfolios.csv",
                {"NoDur", "Utils", "Hlth"},
                "Average Value Weighted Returns -- Monthly",
            ),
        )

    def quarter(self, vm: Month, sahm: float) -> RegimeQuarter | None:
        """Return the regime quarter of vintage month vm, or None if a response is unavailable."""
        win = [add(vm, k) for k in (1, 2, 3)]
        m3 = win[-1]
        ff, ind, gs10, baa = self.factors, self.industries, self.gs10, self.baa
        if (
            not all(w in ff and w in ind for w in win)
            or m3 not in gs10
            or vm not in gs10
            or m3 not in baa
        ):
            return None
        return RegimeQuarter(
            month=vm,
            sahm=sahm,
            signal=sahm >= SAHM_THRESHOLD,
            nber_any=any(w in NBER for w in win),
            nber_all=all(w in NBER for w in win),
            responses={
                "usd_g": log_change(self.dollar_goods, vm, m3),
                "usd_gs": log_change(self.dollar_broad, vm, m3),
                "dy10": gs10[m3] - gs10[vm],
                "dcred": (baa[m3] - gs10[m3]) - (baa[vm] - gs10[vm]),
                "eq": sum(ff[w]["Mkt-RF"] for w in win),
                "dfn": sum(
                    (ind[w]["NoDur"] + ind[w]["Utils"] + ind[w]["Hlth"]) / 3
                    - (ff[w]["Mkt-RF"] + ff[w]["RF"])
                    for w in win
                ),
                "usd": spliced_log_change(self.dollar_goods, self.dollar_broad, vm, m3),
            },
        )


class RegimeQuarters(Record):
    """The vintage quarters with every response source available, in order.

    Attributes:
        quarters: The quarters.
        skipped: The unemployment vintages skipped for a missing month in their window.
    """

    quarters: list[RegimeQuarter]
    skipped: list[str]

    @classmethod
    def of(cls, signals: SahmSignals, data: MarketData) -> Self:
        """Return each signal's quarter whose responses are available."""
        quarters = [
            q
            for vm in sorted(signals.by_month)
            if (q := data.quarter(vm, signals.by_month[vm][0])) is not None
        ]
        return cls(quarters=quarters, skipped=signals.skipped)

    def write(self, path: Path) -> None:
        """Write regime_quarters.csv."""
        with path.open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(CSV_HEADER)
            w.writerows(r.csv_row() for r in self.quarters)

    def describe(self) -> None:
        """Print the quarters, the signal quarters, the skipped vintages and the NBER overlaps."""
        recs = self.quarters
        sig = [r for r in recs if r.signal]
        print(
            f"Quarters: {len(recs)} ({recs[0].month} to {recs[-1].month}); real-time signal in "
            f"{len(sig)}:"
        )
        print("  " + ", ".join(f"{r.month[0]}-{r.month[1]:02d}" for r in sig))
        print(
            "Vintages skipped for a missing month in the window: "
            f"{', '.join(self.skipped) or 'none'}"
        )
        print(
            f"NBER quarters: any overlap {sum(r.nber_any for r in recs)} (overlap with signal"
            f" {sum(r.nber_any and r.signal for r in recs)}); all three months inside"
            f" {sum(r.nber_all for r in recs)} (overlap with signal"
            f" {sum(r.nber_all and r.signal for r in recs)})"
        )

    def test(self, flag: Callable[[RegimeQuarter], bool], title: str) -> dict[str, bool]:
        """Print each response's mean in and out of the flagged quarters; return the decisions.

        A sign is supported if the difference has the hypothesised sign with |Welch t| > 2.
        """
        print(f"\n== {title}")
        out = {}
        for k, sgn in WANT.items():
            sub = [(r, v) for r in self.quarters if (v := r.responses[k]) is not None]
            a = np.array([v for r, v in sub if flag(r)])
            b = np.array([v for r, v in sub if not flag(r)])
            d = a.mean() - b.mean()
            t = d / math.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
            _, tn = indicator_slope(
                np.array([v for _, v in sub]), np.array([float(flag(r)) for r, _ in sub])
            )
            ok = bool(np.sign(d) == sgn and abs(t) > 2)
            span = f"{sub[0][0].month[0]}-{sub[-1][0].month[0]}"
            print(
                f"  {LABEL.get(k, k):42s} {span}: regime {a.mean():+.3f} (n {len(a)},"
                f" {episodes([flag(r) for r, _ in sub])} episodes), other {b.mean():+.3f}"
                f" (n {len(b)}), diff {d:+.3f}, Welch t {t:+.2f}, NW(4) t {tn:+.2f}"
                f"  -> {'sign as hypothesised with |Welch t| > 2' if ok else 'threshold not met'}"
            )
            out[k] = ok
        return out


class Arguments(WorkflowArguments):
    """The recession row's arguments.

    Attributes:
        source: The empirical folder with rucqvmd.xlsx, fred/*.csv and french/*.csv.
    """

    folder: ClassVar[str] = "macro-regimes-stock-bond"
    source: Path


def main(argv: Sequence[str] | None = None) -> int:
    """Print the recession row's real-time test and ex-post description; write regime_quarters.csv.

    The test of ev:regime-asset-responses-tested's recession row (def:macro-regime-asset-map):
    in recession, yields fall, credit spreads widen, equities fall, the dollar rises and
    defensive sectors lead. The regime is real time: in each RUC vintage (Philadelphia Fed
    Real-Time Data Set, quarterly vintages of monthly unemployment, dated in the quarter's
    middle month), the signal is set if the three-month average at the last reported month
    exceeds the minimum three-month average of the 12 months before by at least 0.5 point.
    Responses over the three months after the vintage month: dy10 (GS10), dcred (Baa less
    GS10), eq (sum of Mkt-RF), dfn (defensive industries less the market) and the dollar on
    the goods-only index (1973-2019, the primary dollar result), on DTWEXBGS (2006 onward) and
    on their splice (for continuity only). A sign is supported if the real-time difference has
    the hypothesised sign with |Welch t| > 2; Newey-West t (4 lags) and episode counts are
    sensitivities. The NBER blocks use dates announced later: a description, not a test.

    Returns:
        0.
    """
    parser = Arguments.parser(__doc__ or "")
    parser.add_argument("source", type=Path, help="folder with rucqvmd.xlsx, fred/ and french/")
    args = Arguments.parse(parser, argv)
    signals = SahmSignals.of(
        list(RealTimeVintage.read_all(args.source / "rucqvmd.xlsx", "ruc", "RUC", True))
    )
    recs = RegimeQuarters.of(signals, MarketData.read(args.source))
    recs.write(args.output_folder / "regime_quarters.csv")
    recs.describe()
    print("\nREAL-TIME TEST (the only test; decision rule: hypothesised sign with |Welch t| > 2)")
    verdict = recs.test(
        lambda r: r.signal, "real-time Sahm signal: mean in regime minus mean outside"
    )
    print(
        "\nEX-POST DESCRIPTION (NBER dates known only later; not a test of a usable classification)"
    )
    recs.test(lambda r: r.nber_any, "ex-post NBER window, ANY OVERLAP (v1 definition)")
    recs.test(lambda r: r.nber_all, "ex-post NBER window, ALL MONTHS inside (sensitivity)")
    print(
        "\nVerdict (real time): "
        + "; ".join(
            f"{LABEL.get(k, k)} {'supported' if v else 'not supported'}" for k, v in verdict.items()
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
