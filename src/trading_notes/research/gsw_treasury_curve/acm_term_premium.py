"""A description of one vintage of the New York Fed's ACM 10-year term premium."""

import sys
from collections.abc import Sequence
from pathlib import Path
from typing import ClassVar, Final, Self

from trading_notes.data_folders import DataFolder
from trading_notes.records import Record
from trading_notes.research.gsw_treasury_curve.fed_data import AcmEstimates
from trading_notes.research.workflow import WorkflowArguments

SPLIT_TOLERANCE: Final = 1e-6


def below_zero(values: Sequence[float]) -> int:
    """Return how many of the values are negative."""
    return sum(1 for v in values if v < 0)


class TenYearPremium(Record):
    """The ACM 10-year term premium of one vintage, end of month, in percent.

    Attributes:
        dates: Each month's date, as DD-Mon-YYYY text.
        premium: ACMTP10.
        split_gap: The largest |ACMY10 - ACMRNY10 - ACMTP10|.
    """

    dates: list[str]
    premium: list[float]
    split_gap: float

    @classmethod
    def of(cls, acm: AcmEstimates) -> Self:
        """Return the premium and how closely the yield splits into its two parts."""
        tp, y, rn = acm.values("ACMTP10"), acm.values("ACMY10"), acm.values("ACMRNY10")
        gap = max(abs(a - b - c) for a, b, c in zip(y, rn, tp, strict=True))
        return cls(dates=acm.dates(), premium=tp, split_gap=gap)

    def report(self) -> None:
        """Print the sample, the premium's mean, sign and extremes, and each decade's.

        Raises:
            ValueError: If the yield split is off by SPLIT_TOLERANCE or more.
        """
        date, tp = self.dates, self.premium
        print(
            f"sample {date[0]} to {date[-1]}, {len(date)} months; max |ACMY10 - ACMRNY10 -"
            f" ACMTP10| = {self.split_gap:.2e}"
        )
        if not self.split_gap < SPLIT_TOLERANCE:
            raise ValueError("ACMY10 is not ACMRNY10 + ACMTP10 to rounding")
        neg = below_zero(tp)
        lo = min(range(len(tp)), key=lambda i: tp[i])
        hi = max(range(len(tp)), key=lambda i: tp[i])
        print(
            f"10-year term premium: mean {sum(tp) / len(tp):+.2f} pp; below zero in {neg} of"
            f" {len(tp)} months ({neg / len(tp) * 100:.0f}%); min {tp[lo]:+.2f} ({date[lo]}),"
            f" max {tp[hi]:+.2f} ({date[hi]}); latest {tp[-1]:+.2f} ({date[-1]})"
        )
        for start in range(1960, 2030, 10):
            sel = [v for d, v in zip(date, tp, strict=True) if start <= int(d[-4:]) < start + 10]
            if sel:
                print(
                    f"  {start}s: mean {sum(sel) / len(sel):+.2f}, below zero"
                    f" {below_zero(sel)}/{len(sel)}"
                )
        first = next(d for d, v in zip(date, tp, strict=True) if v < 0 and int(d[-4:]) > 1990)
        print(f"first month below zero after 1990: {first}")


class Arguments(WorkflowArguments):
    """The ACM summary's arguments.

    Attributes:
        acm: The New York Fed's ACMTermPremium.xls.
    """

    folder: ClassVar[DataFolder] = DataFolder(subsection="gsw_treasury_curve")
    acm: Path


def main(argv: Sequence[str] | None = None) -> int:
    """Print the ACM 10-year term premium over the sample and by decade.

    Behind the term-premium paragraph of mod:forward-rates-fra: the end-of-month estimates
    of Adrian, Crump and Moench (2013), retrieved 2026-10-17, are model outputs revised on
    re-estimation, so this describes one vintage. Reported: ACMTP10's mean, months below zero
    and extremes, by decade, and the yield split ACMY10 = ACMRNY10 + ACMTP10 to rounding.

    Returns:
        0.

    Raises:
        ValueError: If the yield split is off by 1e-6 or more.
    """
    parser = Arguments.parser(__doc__ or "")
    parser.add_argument("acm", type=Path, help="ACMTermPremium.xls")
    args = Arguments.parse(parser, argv)
    TenYearPremium.of(AcmEstimates.read(args.acm)).report()
    return 0


if __name__ == "__main__":
    sys.exit(main())
