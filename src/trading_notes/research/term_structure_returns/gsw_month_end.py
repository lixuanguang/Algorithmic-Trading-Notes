"""Month-end Gurkaynak-Sack-Wright zero-coupon yields, January 1986 to September 2026."""

import csv
import hashlib
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import ClassVar, Final, Self

from trading_notes.records import Record
from trading_notes.research.workflow import WorkflowArguments

RAW: Final = Path("reading_materials") / "derivatives-validation" / "empirical" / "feds200628.csv"
MATS: Final = [1, 2, 3, 5, 7, 10, 20, 30]
# The feds200628.csv used, which ends on 9 October 2026.
EXPECTED_SHA: Final = "7286435090933f0df1dcaeb15629f3a9129c083baee4c42ae5df03d0bb89335c"
FIRST_MONTH: Final = "1986-01"  # the first month with a 30-year yield in every later month
LAST_MONTH: Final = "2026-09"  # the partial October 2026 is excluded


class MonthEndYields(Record):
    """The last business day's zero yields SVENYxx of each complete month, in percent.

    Attributes:
        rows: By YYYY-MM, the date and the yields at MATS years, as published.
    """

    rows: dict[str, list[str]]

    @classmethod
    def read(cls, raw: Path) -> Self:
        """Read the month ends of feds200628.csv, skipping days with a yield missing."""
        with raw.open(newline="") as fh:
            lines = fh.read().splitlines()
        start = next(i for i, line in enumerate(lines) if line.startswith("Date,"))
        last = {}
        for row in csv.DictReader(lines[start:]):
            ym = row["Date"][:7]
            vals = [row[f"SVENY{m:02d}"] for m in MATS]
            if "NA" in vals or "" in vals:
                continue
            if FIRST_MONTH <= ym <= LAST_MONTH:
                last[ym] = [row["Date"], *vals]  # rows are in date order: the month's last wins
        return cls(rows=last)

    def write(self, out: Path) -> None:
        """Write gsw-month-end-zero.csv: the date and one column per maturity."""
        with out.open("w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["date"] + [f"y{m}" for m in MATS])
            for ym in sorted(self.rows):
                w.writerow(self.rows[ym])


class Arguments(WorkflowArguments):
    """The extract's arguments.

    Attributes:
        raw: The Board's feds200628.csv, or None for ROOT/reading_materials/....
    """

    folder: ClassVar[str] = "term-structure-dynamics"
    raw: Path | None = None


def main(argv: Sequence[str] | None = None) -> int:
    """Write gsw-month-end-zero.csv for maturities 1-30 years; exit 1 on a hash mismatch.

    Input: the Federal Reserve Board's feds200628.csv (fitted off-the-run Treasury curve,
    daily continuously compounded zero yields SVENYxx in percent), kept outside Git.

    Returns:
        0, or 1 when the input is not the recorded file.
    """
    parser = Arguments.parser(__doc__ or "")
    parser.add_argument("raw", type=Path, nargs="?", default=None, help="feds200628.csv")
    args = Arguments.parse(parser, argv)
    raw = args.raw or args.root / RAW
    digest = hashlib.sha256(raw.read_bytes()).hexdigest()
    if digest != EXPECTED_SHA:
        print(f"unexpected input file hash {digest}", file=sys.stderr)
        return 1
    yields = MonthEndYields.read(raw)
    out = args.output_folder / "gsw-month-end-zero.csv"
    yields.write(out)
    print(f"wrote {len(yields.rows)} months to {out.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
