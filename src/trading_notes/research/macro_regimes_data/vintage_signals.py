"""Vintage-dated quarters of the inflation and deflation rows: signals, responses and tests."""

import csv
from collections.abc import Sequence
from pathlib import Path
from typing import Final, Self

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.newey_west import Month, add
from trading_notes.records import Record
from trading_notes.research.macro_regimes_data.regime_inputs import (
    MonthlyResponses,
    RealTimeVintage,
    episodes,
    indicator_slope,
    welch_t,
)

type Floats = NDArray[np.float64]
type Ints = NDArray[np.int64]

CSV_HEADER: Final = [
    "vintage",
    "vintage_month",
    "last_cpi_month",
    "pi_12m",
    "accel_12m",
    "signal",
    "dy10",
    "dslope",
    "oil",
]


class VintageQuarter(Record):
    """A vintage's classification and the responses over the three months after it.

    Attributes:
        vintage: The vintage name.
        month: The vintage month m.
        last: The last CPI month L reported in the vintage.
        pi: pi(L), the 12-month inflation rate.
        accel: pi(L) - pi(L - 12).
        signal: 1 if the vintage signals the regime.
        dy10: GS10(m + 3) - GS10(m).
        dslope: The change in GS10 - TB3 over m..m + 3.
        oil: 100 ln(RWTC(m + 3) / RWTC(m)).
    """

    vintage: str
    month: Month
    last: Month
    pi: float
    accel: float
    signal: int
    dy10: float
    dslope: float
    oil: float

    def responses(self) -> dict[str, float]:
        """Return the three responses by name."""
        return {"dy10": self.dy10, "dslope": self.dslope, "oil": self.oil}

    def csv_row(self) -> list[str | int]:
        """Return the quarter as written to the vintage-quarters CSV."""
        return [
            self.vintage,
            f"{self.month[0]}-{self.month[1]:02d}",
            f"{self.last[0]}-{self.last[1]:02d}",
            f"{self.pi:.3f}",
            f"{self.accel:.3f}",
            self.signal,
            f"{self.dy10:.4f}",
            f"{self.dslope:.4f}",
            f"{self.oil:.4f}",
        ]


class ResponseDifference(Record):
    """A response's mean in signal quarters against the other quarters.

    Attributes:
        signal_mean: The mean over signal quarters.
        other_mean: The mean over the others.
        difference: signal_mean - other_mean.
        welch_t: Welch's t for the difference.
        nw_t: The Newey-West t (4 lags) of the slope on the signal indicator.
    """

    signal_mean: float
    other_mean: float
    difference: float
    welch_t: float
    nw_t: float

    @classmethod
    def of(cls, y: Floats, signal: Ints) -> Self:
        """Return the comparison of responses y between quarters with signal 1 and 0."""
        a, b = y[signal == 1], y[signal == 0]
        return cls(
            signal_mean=float(a.mean()),
            other_mean=float(b.mean()),
            difference=float(a.mean() - b.mean()),
            welch_t=welch_t(a, b),
            nw_t=indicator_slope(y, signal.astype(float))[1],
        )

    def line(self, name: str, label: str) -> str:
        """Return the response's row of the response table."""
        return (
            f"{name:8s}   {label:10s}   {self.signal_mean:+10.3f}   {self.other_mean:+10.3f}"
            f"   {self.difference:+10.3f}   {self.welch_t:+7.2f}   {self.nw_t:+7.2f}"
        )


class VintageQuarters(Record):
    """The classifiable vintages with complete responses, and the skipped ones with why.

    Attributes:
        quarters: The vintage quarters, in vintage order.
        skipped: The skipped vintages' names, each with its reason.
    """

    quarters: list[VintageQuarter]
    skipped: list[str]

    @classmethod
    def of(
        cls,
        vintages: Sequence[RealTimeVintage],
        responses: MonthlyResponses,
        signal: float,
        deflation: bool,
        incomplete: str = " (window incomplete)",
    ) -> Self:
        """Classify each vintage and attach its responses over the next three months.

        A vintage signals when its acceleration is at most `signal` (deflation) or at least it.

        Args:
            vintages: The middle-month vintages, in order.
            responses: The series the responses are built from.
            signal: The acceleration threshold, in points.
            deflation: Whether the signal is a fall to the threshold rather than a rise.
            incomplete: Appended to the name of a vintage whose 25-month window is incomplete.
        """
        obs, skipped = [], []
        for v in vintages:
            try:
                L, pil, accel = v.classify()
            except KeyError:
                skipped.append(v.name + incomplete)
                continue
            m3 = add(v.month, 3)
            if not responses.complete((v.month, m3)):
                skipped.append(v.name + " (responses incomplete)")
                continue
            flagged = accel <= signal if deflation else accel >= signal
            obs.append(
                VintageQuarter(
                    vintage=v.name,
                    month=v.month,
                    last=L,
                    pi=pil,
                    accel=accel,
                    signal=int(flagged),
                    dy10=responses.dy10(v.month, m3),
                    dslope=responses.dslope(v.month, m3),
                    oil=responses.oil_change(v.month, m3),
                )
            )
        return cls(quarters=obs, skipped=skipped)

    def used(self) -> str:
        """Return the number of vintages used and the first and last."""
        q = self.quarters
        return f"vintages used: {len(q)} ({q[0].vintage} to {q[-1].vintage})"

    def write(self, path: Path) -> None:
        """Write the vintage quarters with the shared header."""
        with path.open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(CSV_HEADER)
            w.writerows(o.csv_row() for o in self.quarters)

    def signal_summary(self) -> str:
        """Return the signal quarters line: their count, episodes and names."""
        flags = [o.signal for o in self.quarters]
        return f"signal quarters: {sum(flags)} in {episodes(flags)} episodes: " + ", ".join(
            o.vintage for o in self.quarters if o.signal
        )

    def print_responses(
        self, header: str, labels: Sequence[tuple[str, str]]
    ) -> dict[str, ResponseDifference]:
        """Print the response table under its header; return dy10, dslope and oil compared."""
        sig = np.array([o.signal for o in self.quarters])
        diffs = {
            k: ResponseDifference.of(np.array([o.responses()[k] for o in self.quarters]), sig)
            for k in ("dy10", "dslope", "oil")
        }
        print(header)
        for k, label in labels:
            print(diffs[k].line(k, label))
        return diffs
