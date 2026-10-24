"""GSW's published 10-year yield recomputed from its parameters, and Kim-Wright against ACM."""

import math
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import ClassVar, Final, Self

import numpy as np

from trading_notes.numerical.newey_west import Month
from trading_notes.records import Record
from trading_notes.research.gsw_treasury_curve.fed_data import AcmEstimates, FedsTable, number
from trading_notes.research.workflow import WorkflowArguments

TOLERANCE: Final = 0.001  # 0.1 bp


class SvenssonCurve(Record):
    """One day's published Svensson parameters (FEDS 2006-28, eq. (22)).

    Attributes:
        beta0: BETA0.
        beta1: BETA1.
        beta2: BETA2.
        beta3: BETA3, None when missing.
        tau1: TAU1, in years.
        tau2: TAU2, in years, None when missing.
    """

    beta0: float
    beta1: float
    beta2: float
    beta3: float | None
    tau1: float
    tau2: float | None

    @property
    def three_term(self) -> bool:
        """Return whether the fourth term is dropped: BETA3 or TAU2 missing or zero."""
        return not (self.beta3 and self.tau2)

    def zero_yield(self, n: float) -> float:
        """Return the n-year continuously compounded zero yield, in percent."""
        e1 = math.exp(-n / self.tau1)
        y = (
            self.beta0
            + self.beta1 * (1 - e1) / (n / self.tau1)
            + self.beta2 * ((1 - e1) / (n / self.tau1) - e1)
        )
        if self.beta3 and self.tau2:
            e2 = math.exp(-n / self.tau2)
            return y + self.beta3 * ((1 - e2) / (n / self.tau2) - e2)
        return y


class RecomputedYields(Record):
    """Each day's 10-year zero yield recomputed from its parameters, beside SVENY10.

    Attributes:
        days: (|recomputed - published|, date, recomputed, published) in date order.
        three_term_days: The days whose curve has three terms.
    """

    days: list[tuple[float, str, float, float]]
    three_term_days: int

    @classmethod
    def of(cls, table: FedsTable) -> Self:
        """Return the days of feds200628.csv with every parameter and SVENY10 reported."""
        c = {h: k for k, h in enumerate(table.head)}
        days: list[tuple[float, str, float, float]] = []
        n_ns = 0
        for r in table.body:
            b0, b1, b2, b3, t1, t2, y10 = (
                number(r[c[k]])
                for k in ("BETA0", "BETA1", "BETA2", "BETA3", "TAU1", "TAU2", "SVENY10")
            )
            if b0 is None or b1 is None or b2 is None or t1 is None or y10 is None:
                continue
            curve = SvenssonCurve(beta0=b0, beta1=b1, beta2=b2, beta3=b3, tau1=t1, tau2=t2)
            y = curve.zero_yield(10.0)
            n_ns += curve.three_term
            days.append((abs(y - y10), r[0], y, y10))
        return cls(days=days, three_term_days=n_ns)

    def report(self) -> None:
        """Print how closely the recomputed yields match the published ones.

        Raises:
            ValueError: If any day differs by 0.1 bp or more.
        """
        d = np.array([x[0] for x in self.days])
        w = max(self.days)
        print(
            f"GSW: {len(self.days)} days with a 10-year yield; recomputed minus published |diff|"
            f" max {d.max():.5f} pp ({w[1]}: {w[2]:.4f} vs {w[3]:.4f}), 99th percentile"
            f" {np.percentile(d, 99):.5f}; three-term days {self.three_term_days}"
        )
        last = self.days[-1]
        print(f"  last day {last[1]}: recomputed {last[2]:.4f}, published {last[3]:.4f}")
        if not d.max() < TOLERANCE:
            raise ValueError("published SVENY10 not reproduced to 0.1 bp")


class TermPremia(Record):
    """Kim-Wright's and ACM's 10-year term premia by month.

    Attributes:
        kim_wright: THREEFYTP1000.B on each month's last reported day, with that date.
        acm: ACMTP10, end of month.
    """

    kim_wright: dict[Month, tuple[str, float]]
    acm: dict[Month, float]

    @classmethod
    def of(cls, kw_table: FedsTable, acm: AcmEstimates) -> Self:
        """Return the two premia from feds200533.csv and the ACM workbook."""
        col = kw_table.column("THREEFYTP1000.B")
        kw: dict[Month, tuple[str, float]] = {}
        for r in kw_table.body:
            v = number(r[col])
            if v is not None:
                y, m, _ = map(int, r[0].split("-"))
                kw[(y, m)] = (r[0], v)  # rows are in date order, so the last day of each month wins
        return cls(kim_wright=kw, acm=acm.by_month("ACMTP10"))

    def report(self) -> None:
        """Print the comparison on common months."""
        kw, tp = self.kim_wright, self.acm
        common = sorted(set(kw) & set(tp))
        a = np.array([kw[k][1] for k in common])
        b = np.array([tp[k] for k in common])
        print(
            f"KW vs ACM, 10-year term premium: {len(common)} common months, {common[0]} to"
            f" {common[-1]}"
        )
        print(
            f"  correlation {np.corrcoef(a, b)[0, 1]:.3f}; KW - ACM mean {np.mean(a - b):+.2f} pp,"
            f" range {np.min(a - b):+.2f} to {np.max(a - b):+.2f}"
        )
        print(
            f"  months both below zero {int(((a < 0) & (b < 0)).sum())}; KW below zero"
            f" {int((a < 0).sum())}; ACM below zero {int((b < 0).sum())}"
        )
        for k in ((1990, 12), (2020, 6), common[-1]):
            if k in kw and k in tp:
                print(f"  {k[0]}-{k[1]:02d}: KW {kw[k][1]:+.2f} ({kw[k][0]}), ACM {tp[k]:+.2f}")


class Arguments(WorkflowArguments):
    """The curve checks' arguments.

    Attributes:
        gsw: The Board's feds200628.csv.
        kim_wright: The Board's feds200533.csv.
        acm: The New York Fed's ACMTermPremium.xls.
    """

    folder: ClassVar[str] = "curve-term-structure"
    gsw: Path
    kim_wright: Path
    acm: Path


def main(argv: Sequence[str] | None = None) -> int:
    """Print the two descriptive checks of data:gsw-treasury-curve and the term premia.

    1. GSW: each day's 10-year zero yield recomputed from the published BETA0-BETA3, TAU1
       and TAU2 against the published SVENY10; days with a missing parameter skipped.
    2. Kim-Wright's THREEFYTP1000.B (daily, sampled on each month's last day) against ACMTP10
       (end of month): both are revised model outputs, so this compares two vintages.

    Returns:
        0.
    """
    parser = Arguments.parser(__doc__ or "")
    parser.add_argument("gsw", type=Path, help="feds200628.csv")
    parser.add_argument("kim_wright", type=Path, help="feds200533.csv")
    parser.add_argument("acm", type=Path, help="ACMTermPremium.xls")
    args = Arguments.parse(parser, argv)
    RecomputedYields.of(FedsTable.read(args.gsw)).report()
    TermPremia.of(FedsTable.read(args.kim_wright), AcmEstimates.read(args.acm)).report()
    return 0


if __name__ == "__main__":
    sys.exit(main())
