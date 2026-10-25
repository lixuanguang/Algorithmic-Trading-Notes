"""The regime map's inflation-shock row on the quarterly CPI vintages, against the monthly ones."""

import sys
from collections.abc import Sequence
from typing import Self

from trading_notes.numerical.newey_west import Month
from trading_notes.records import Record
from trading_notes.research.macro_regimes_data.inflation_regime import (
    HEADER,
    HYPOTHESES,
    THRESHOLD,
    print_verdict,
)
from trading_notes.research.macro_regimes_data.regime_inputs import (
    MONTHLY_CPI,
    QUARTERLY_CPI,
    RealTimeVintage,
    RowArguments,
)
from trading_notes.research.macro_regimes_data.vintage_signals import VintageQuarters


def month_text(vm: Month) -> str:
    """Return a month as YYYY-MM."""
    return f"{vm[0]}-{vm[1]:02d}"


class VintageLabels(Record):
    """Each classifiable vintage's last CPI month and signal, by vintage month.

    Attributes:
        by_month: (last CPI month L, 1 if the acceleration reaches THRESHOLD else 0).
    """

    by_month: dict[Month, tuple[Month, int]]

    @classmethod
    def of(cls, vintages: Sequence[RealTimeVintage]) -> Self:
        """Return the labels of the vintages whose 25-month window is complete."""
        out = {}
        for v in vintages:
            try:
                L, _, accel = v.classify()
            except KeyError:
                continue
            out[v.month] = (L, int(accel >= THRESHOLD))
        return cls(by_month=out)

    def compare(self, monthly: VintageLabels, used: set[Month]) -> None:
        """Print how these quarterly labels and the monthly ones differ on common months."""
        qlab, mlab = self.by_month, monthly.by_month
        common = sorted(set(qlab) & set(mlab))
        dL = [vm for vm in common if qlab[vm][0] != mlab[vm][0]]
        dS = [vm for vm in common if qlab[vm][1] != mlab[vm][1]]
        print(
            "\nDiagnostic (not part of the verdict): quarterly vs monthly middle-month vintages,"
            " classifiable in both"
        )
        print(
            f"common vintage months: {len(common)} ({month_text(common[0])} to"
            f" {month_text(common[-1])}); {sum(v in used for v in common)} of them have responses"
            " (the monthly-vintage test uses 111 vintages)"
        )
        print(
            f"latest CPI month differs: {len(dL)} (monthly later in"
            f" {sum(mlab[v][0] > qlab[v][0] for v in dL)}, quarterly later in"
            f" {sum(qlab[v][0] > mlab[v][0] for v in dL)})"
        )
        print(
            f"signal label differs: {len(dS)}: "
            + ", ".join(f"{month_text(v)} (Q {qlab[v][1]}, M {mlab[v][1]})" for v in dS)
        )


def main(argv: Sequence[str] | None = None) -> int:
    """Print the quarterly inflation row and write inflation_quarterly_vintage_quarters.csv.

    The protocol of inflation-row-protocol.md on the file it names, the quarterly CPI
    vintages (cpiQvMd.xlsx): vintage CPIyyQq dated in its quarter's middle month m, signal
    pi(L) - pi(L - 12) >= 1.0 point, vintages with a missing month in the 25-month window
    skipped and listed; responses and tests as in the monthly-vintage run. A diagnostic, not
    part of the verdict, compares the quarterly and monthly vintages' classifications.

    Returns:
        0.
    """
    args = RowArguments.parse(RowArguments.parser(__doc__ or ""), argv)
    responses = args.responses()
    quarterly = list(RealTimeVintage.read_all(args.materials / QUARTERLY_CPI, "cpi", "CPI", True))
    quarters = VintageQuarters.of(quarterly, responses, THRESHOLD, deflation=False)
    quarters.write(args.output_folder / "inflation_quarterly_vintage_quarters.csv")
    print("Quarterly CPI vintages (cpiQvMd.xlsx), the protocol as written")
    print(quarters.used())
    print(f"skipped: {len(quarters.skipped)}: {', '.join(quarters.skipped)}")
    print(quarters.signal_summary())
    print_verdict(quarters.print_responses(HEADER, HYPOTHESES))
    monthly = list(RealTimeVintage.read_all(args.materials / MONTHLY_CPI, "pcpi", "PCPI", False))
    VintageLabels.of(quarterly).compare(
        VintageLabels.of(monthly), {o.month for o in quarters.quarters}
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
